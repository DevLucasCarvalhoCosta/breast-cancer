from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import math

from app.database import get_db
from app.models import Sample, SampleFeature, FeatureDefinition
from app.schemas.sample import (
    DatasetStats, SampleWithFeatures, PaginatedSamples, FeatureDefinitionResponse
)
from app.services.data_service import run_full_etl

router = APIRouter(prefix="/api/data", tags=["Dados"])


@router.get("/stats", response_model=DatasetStats)
def get_dataset_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Sample.id)).scalar()
    if total == 0:
        raise HTTPException(status_code=404, detail="Dataset não carregado. Execute POST /api/data/etl.")

    benign = db.query(func.count(Sample.id)).filter(Sample.diagnosis == "B").scalar()
    malignant = db.query(func.count(Sample.id)).filter(Sample.diagnosis == "M").scalar()

    return DatasetStats(
        total_samples=total,
        benign_count=benign,
        malignant_count=malignant,
        benign_percentage=round(benign / total * 100, 2),
        malignant_percentage=round(malignant / total * 100, 2),
        total_features=30,
        missing_values=0,
        duplicated_rows=0,
    )


@router.get("/samples", response_model=PaginatedSamples)
def list_samples(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    diagnosis: str | None = Query(None, pattern="^[MB]$"),
    db: Session = Depends(get_db),
):
    query = db.query(Sample)
    if diagnosis:
        query = query.filter(Sample.diagnosis == diagnosis)

    total = query.count()
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    samples = query.offset((page - 1) * page_size).limit(page_size).all()

    items = []
    for sample in samples:
        features_dict = {f.feature_name: f.feature_value for f in sample.features}
        items.append(SampleWithFeatures(
            id=sample.id,
            original_id=sample.original_id,
            diagnosis=sample.diagnosis,
            diagnosis_encoded=sample.diagnosis_encoded,
            created_at=sample.created_at,
            features=features_dict,
        ))

    return PaginatedSamples(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/samples/{sample_id}", response_model=SampleWithFeatures)
def get_sample(sample_id: int, db: Session = Depends(get_db)):
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    if not sample:
        raise HTTPException(status_code=404, detail=f"Amostra {sample_id} não encontrada.")

    features_dict = {f.feature_name: f.feature_value for f in sample.features}
    return SampleWithFeatures(
        id=sample.id,
        original_id=sample.original_id,
        diagnosis=sample.diagnosis,
        diagnosis_encoded=sample.diagnosis_encoded,
        created_at=sample.created_at,
        features=features_dict,
    )


@router.get("/features", response_model=list[FeatureDefinitionResponse])
def list_feature_definitions(db: Session = Depends(get_db)):
    return db.query(FeatureDefinition).order_by(FeatureDefinition.id).all()


@router.post("/etl")
def run_etl(db: Session = Depends(get_db)):
    try:
        return run_full_etl(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no ETL: {str(e)}")
