import pandas as pd
import numpy as np
import logging
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.models import Sample, SampleFeature, FeatureDefinition, FeatureCorrelation
from app.config import get_settings

logger = logging.getLogger(__name__)

FEATURE_CLINICAL_INFO = {
    "radius": {
        "description": "Média das distâncias do centro aos pontos do perímetro do núcleo celular",
        "unit": "μm",
        "clinical_relevance": "Tumores malignos tendem a ter raio significativamente maior, indicando crescimento celular anormal e descontrolado."
    },
    "texture": {
        "description": "Desvio padrão dos valores de escala de cinza na imagem do núcleo",
        "unit": "escala de cinza",
        "clinical_relevance": "Textura irregular/heterogênea indica cromatina anormal, comum em células malignas."
    },
    "perimeter": {
        "description": "Perímetro do contorno do núcleo celular",
        "unit": "μm",
        "clinical_relevance": "Altamente correlacionado com raio e área. Tumores malignos têm perímetros maiores e mais irregulares."
    },
    "area": {
        "description": "Área da seção transversal do núcleo celular",
        "unit": "μm²",
        "clinical_relevance": "Feature mais discriminativa junto com concave_points. Células malignas têm área nuclear ampliada."
    },
    "smoothness": {
        "description": "Variação local nos comprimentos do raio (suavidade da borda)",
        "unit": "adimensional",
        "clinical_relevance": "Bordas irregulares (baixa suavidade) são indicativas de invasão celular, um marcador de malignidade."
    },
    "compactness": {
        "description": "Compactação: (perímetro² / área) - 1.0",
        "unit": "adimensional",
        "clinical_relevance": "Formas mais compactas e irregulares são características de núcleos malignos com divisão celular descontrolada."
    },
    "concavity": {
        "description": "Severidade (profundidade) das porções côncavas do contorno do núcleo",
        "unit": "adimensional",
        "clinical_relevance": "Concavidades profundas no contorno nuclear são forte indicador de malignidade."
    },
    "concave_points": {
        "description": "Número de porções côncavas (reentrâncias) do contorno do núcleo",
        "unit": "contagem",
        "clinical_relevance": "Uma das features mais importantes. Núcleos malignos têm significativamente mais pontos côncavos."
    },
    "symmetry": {
        "description": "Simetria do núcleo celular (diferença entre eixos)",
        "unit": "adimensional",
        "clinical_relevance": "Assimetria nuclear indica crescimento celular desordenado, associado a malignidade."
    },
    "fractal_dimension": {
        "description": "Dimensão fractal do contorno — complexidade da borda ('coastline approximation' - 1)",
        "unit": "adimensional",
        "clinical_relevance": "Mede a complexidade/irregularidade da borda. Menos discriminativa individualmente, mas contribui em modelos multivariados."
    },
}

AGGREGATION_DESCRIPTIONS = {
    "mean": "Média de todos os núcleos na imagem FNA",
    "se": "Erro padrão — variabilidade entre os núcleos medidos",
    "worst": "Média dos 3 piores (maiores) valores entre os núcleos"
}

FEATURE_COLUMNS = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean",
    "smoothness_mean", "compactness_mean", "concavity_mean",
    "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se",
    "smoothness_se", "compactness_se", "concavity_se",
    "concave points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst",
    "smoothness_worst", "compactness_worst", "concavity_worst",
    "concave points_worst", "symmetry_worst", "fractal_dimension_worst",
]


def _parse_feature_name(col_name: str) -> tuple[str, str]:
    for agg in ["_mean", "_se", "_worst"]:
        if col_name.endswith(agg):
            base = col_name[: -len(agg)].replace(" ", "_")
            return base, agg[1:]
    return col_name.replace(" ", "_"), "unknown"


def load_csv(csv_path: str | None = None) -> tuple[pd.DataFrame, list]:
    settings = get_settings()
    path = csv_path or settings.DATA_CSV_PATH

    logger.info(f"Carregando CSV: {path}")
    df = pd.read_csv(path)
    original_ids = df["id"].values

    cols_to_drop = [c for c in ["id", "Unnamed: 32"] if c in df.columns]
    df.drop(columns=cols_to_drop, inplace=True)
    df["diagnosis_encoded"] = df["diagnosis"].map({"M": 1, "B": 0})

    logger.info(f"Dataset: {df.shape[0]} amostras, {df.shape[1]} colunas")
    return df, original_ids


def populate_feature_definitions(db: Session) -> None:
    existing = db.query(func.count(FeatureDefinition.id)).scalar()
    if existing > 0:
        logger.info(f"Feature definitions já existem ({existing}). Pulando.")
        return

    for col_name in FEATURE_COLUMNS:
        base, agg = _parse_feature_name(col_name)
        info = FEATURE_CLINICAL_INFO.get(base, {})

        definition = FeatureDefinition(
            name=col_name.replace(" ", "_"),
            description=info.get("description", ""),
            base_feature=base,
            aggregation=agg,
            unit=info.get("unit", ""),
            clinical_relevance=info.get("clinical_relevance", ""),
        )
        db.add(definition)

    db.commit()
    logger.info(f"{len(FEATURE_COLUMNS)} feature definitions criadas.")


def populate_samples(db: Session, csv_path: str | None = None) -> int:
    existing = db.query(func.count(Sample.id)).scalar()
    if existing > 0:
        logger.info(f"Samples já existem ({existing}). Pulando.")
        return existing

    df, original_ids = load_csv(csv_path)
    logger.info("Inserindo amostras...")

    samples_to_add = []
    features_to_add = []

    for idx, row in df.iterrows():
        sample = Sample(
            original_id=int(original_ids[idx]),
            diagnosis=row["diagnosis"],
            diagnosis_encoded=int(row["diagnosis_encoded"]),
        )
        samples_to_add.append(sample)

    db.add_all(samples_to_add)
    db.flush()

    for i, (idx, row) in enumerate(df.iterrows()):
        sample = samples_to_add[i]
        for col_name in FEATURE_COLUMNS:
            if col_name in df.columns:
                base, agg = _parse_feature_name(col_name)
                feature = SampleFeature(
                    sample_id=sample.id,
                    feature_name=col_name.replace(" ", "_"),
                    feature_value=float(row[col_name]),
                    feature_group=agg,
                    feature_base=base,
                )
                features_to_add.append(feature)

    db.add_all(features_to_add)

    for col_name in FEATURE_COLUMNS:
        if col_name in df.columns:
            clean_name = col_name.replace(" ", "_")
            definition = db.query(FeatureDefinition).filter(
                FeatureDefinition.name == clean_name
            ).first()
            if definition:
                definition.min_value = float(df[col_name].min())
                definition.max_value = float(df[col_name].max())

    db.commit()
    count = len(samples_to_add)
    logger.info(f"{count} amostras inseridas com {len(features_to_add)} valores de features.")
    return count


def populate_correlations(db: Session, csv_path: str | None = None) -> None:
    existing = db.query(func.count(FeatureCorrelation.id)).scalar()
    if existing > 0:
        logger.info(f"Correlações já existem ({existing}). Pulando.")
        return

    df, _ = load_csv(csv_path)
    feature_cols = [c for c in FEATURE_COLUMNS if c in df.columns]
    corr_matrix = df[feature_cols].corr()

    correlations_to_add = []
    for i, col_a in enumerate(feature_cols):
        for j, col_b in enumerate(feature_cols):
            if j >= i:
                corr = FeatureCorrelation(
                    feature_a=col_a.replace(" ", "_"),
                    feature_b=col_b.replace(" ", "_"),
                    correlation_value=float(corr_matrix.iloc[i, j]),
                )
                correlations_to_add.append(corr)

    db.add_all(correlations_to_add)
    db.commit()
    logger.info(f"{len(correlations_to_add)} correlações armazenadas.")


def run_full_etl(db: Session, csv_path: str | None = None) -> dict:
    logger.info("=" * 60)
    logger.info("INICIANDO ETL: CSV -> PostgreSQL")
    logger.info("=" * 60)

    populate_feature_definitions(db)
    count = populate_samples(db, csv_path)
    populate_correlations(db, csv_path)

    result = {
        "status": "success",
        "samples_loaded": count,
        "features_per_sample": len(FEATURE_COLUMNS),
        "total_feature_values": count * len(FEATURE_COLUMNS),
        "correlations_cached": len(FEATURE_COLUMNS) * (len(FEATURE_COLUMNS) + 1) // 2,
    }

    logger.info(f"ETL COMPLETO: {result}")
    return result
