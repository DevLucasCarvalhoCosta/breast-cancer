# 🏗️ Projeto: Previsão de Câncer de Mama — Documento de Arquitetura

> **Versão:** 1.0  
> **Data:** 19/02/2026  
> **Status:** Planejamento  
> **Referência:** [Breast Cancer Wisconsin SVM Classification (Kaggle)](https://www.kaggle.com/code/buddhiniw/breast-cancer-prediction/notebook)

---

## 📋 Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Dataset — Análise e Justificativas](#2-dataset--análise-e-justificativas)
3. [Pipeline de Machine Learning — Etapas e Decisões](#3-pipeline-de-machine-learning--etapas-e-decisões)
4. [Arquitetura do Sistema](#4-arquitetura-do-sistema)
5. [Modelagem do Banco de Dados (PostgreSQL)](#5-modelagem-do-banco-de-dados-postgresql)
6. [Estrutura de Diretórios](#6-estrutura-de-diretórios)
7. [Stack Tecnológica — Justificativas](#7-stack-tecnológica--justificativas)
8. [Funcionalidades da Interface Web](#8-funcionalidades-da-interface-web)
9. [Roadmap de Implementação](#9-roadmap-de-implementação)

---

## 1. Visão Geral do Projeto

### Objetivo
Construir uma aplicação web profissional e interativa que reproduza e **expanda** o pipeline de classificação de câncer de mama do notebook de referência, transformando uma análise estática em uma experiência visual, educativa e funcional.

### O que o notebook original faz
| Etapa | O que faz | Limitação |
|-------|-----------|-----------|
| Data Loading | `pd.read_csv()` do Kaggle | Sem persistência, sem versionamento |
| Data Cleaning | Remove `id` e `Unnamed: 32` | Sem log de transformações |
| EDA | Gráficos estáticos (matplotlib/seaborn) | Não interativos, sem filtros |
| Preprocessing | Encoding, Split, Imputer, Scaler | Sem rastreabilidade dos parâmetros |
| Modeling | SVM Linear + SVM RBF | Apenas 2 modelos, sem comparação estruturada |
| Evaluation | Accuracy, Confusion Matrix, Report | Sem persistência de métricas |

### O que nosso projeto vai fazer
| Etapa | Nosso Approach | Vantagem |
|-------|---------------|----------|
| Data Storage | PostgreSQL relacional | Persistência, queries, integridade |
| Data Pipeline | ETL automatizado com log | Reprodutibilidade total |
| EDA | Plotly.js interativo no browser | Zoom, hover, filtros, tooltips |
| Preprocessing | Pipeline parametrizável via API | Configurável e rastreável |
| Modeling | SVM + Random Forest + LogReg + KNN | Comparação rica de trade-offs |
| Evaluation | Dashboard comparativo em tempo real | Métricas lado a lado, visual |
| Interface | React + TypeScript SPA | Profissional, responsiva, moderna |

---

## 2. Dataset — Análise e Justificativas

### Fonte
- **Nome:** Breast Cancer Wisconsin (Diagnostic) Data Set
- **Origem:** UCI Machine Learning Repository
- **Coleta:** Imagens FNA (Fine Needle Aspirate) de massas mamárias
- **Amostras:** 569 (357 benignas + 212 malignas)

### Estrutura das Features (30 features numéricas)

As features são computadas a partir de imagens digitalizadas de aspirações por agulha fina (FNA). Para **cada núcleo celular**, 10 características são medidas:

| Feature | Descrição | Por que é relevante |
|---------|-----------|-------------------|
| `radius` | Média das distâncias do centro aos pontos do perímetro | Tumores malignos tendem a ser maiores |
| `texture` | Desvio padrão dos valores de escala de cinza | Textura irregular indica malignidade |
| `perimeter` | Perímetro do núcleo | Correlacionado com tamanho/forma |
| `area` | Área do núcleo | Tumores malignos têm área maior |
| `smoothness` | Variação local nos comprimentos do raio | Suavidade da borda do núcleo |
| `compactness` | (perímetro² / área) - 1.0 | Forma irregular = mais compacto |
| `concavity` | Severidade das porções côncavas do contorno | Concavidades profundas → maligno |
| `concave_points` | Número de porções côncavas | Quanto mais pontos côncavos → pior |
| `symmetry` | Simetria do núcleo | Assimetria indica crescimento anormal |
| `fractal_dimension` | Aproximação "coastline" - 1 | Complexidade da borda |

Para cada uma dessas 10, são calculados **3 agregadores**:
- **mean** — Média de todos os núcleos na imagem
- **se** — Erro padrão (variabilidade entre núcleos)
- **worst** — Média dos 3 piores valores (mais extremos)

> **Total: 10 × 3 = 30 features preditivas**

### Colunas a remover e justificativa
| Coluna | Motivo da remoção |
|--------|------------------|
| `id` | Identificador arbitrário, sem valor preditivo. Mantê-lo causaria data leakage |
| `Unnamed: 32` | Coluna completamente vazia (0 valores não-nulos), artefato do CSV |

### Qualidade dos dados
- **Sem valores Missing:** 569/569 em todas as 30 features → nenhuma imputação necessária
- **Sem duplicatas:** 0 registros duplicados
- **Desbalanceamento leve:** 62.7% benigno vs 37.3% maligno → aceitável, sem necessidade de SMOTE/undersampling

---

## 3. Pipeline de Machine Learning — Etapas e Decisões

### ETAPA 1: Carregamento e Limpeza

```
CSV → PostgreSQL → DataFrame limpo
```

**Decisões:**
- **Por que PostgreSQL vs CSV direto?**
  - Persistência entre sessões
  - Queries SQL para exploração rápida
  - Integridade referencial entre tabelas (dados, resultados, métricas)
  - Suporte a múltiplos usuários simultâneos
  - Versionamento de experimentos

### ETAPA 2: Análise Exploratória (EDA)

**O que o notebook faz → O que nós faremos:**

| Análise | Original (estático) | Nosso (interativo) |
|---------|---------------------|-------------------|
| Distribuição do diagnóstico | `sns.countplot` | Plotly donut/bar com % e contagem |
| Histogramas das features | `sns.histplot` com KDE | Plotly com seletor de feature, toggle KDE |
| Boxplots por diagnóstico | `sns.boxplot` individual | Grid comparativo com filtros |
| Scatter plots | `sns.scatterplot` fixo | Scatter com seletor X/Y, colorido por classe |
| Heatmap de correlação | `sns.heatmap` estático | Heatmap interativo com hover, filtro por threshold |

**Por que cada gráfico foi escolhido:**

1. **Countplot / Donut → Distribuição do Target**
   - *Por que:* Verificar desbalanceamento de classes. Se fosse severo (>80/20), precisaríamos de técnicas de resampling
   - *Resultado esperado:* 62.7% B / 37.3% M → desbalanceamento moderado, aceitável

2. **Histogramas com KDE → Distribuição de Features**
   - *Por que:* Visualizar se as distribuições de cada feature diferem entre B e M. Features com distribuições separadas são mais discriminativas
   - *Features chave:* `radius_mean`, `perimeter_mean`, `area_mean` mostram separação clara

3. **Boxplots → Outliers e Separabilidade**
   - *Por que:* Identificar outliers que podem afetar o SVM e confirmar quais features separam melhor as classes
   - *Insight:* `radius_worst`, `perimeter_worst`, `area_worst` têm separação nítida entre B e M

4. **Scatter Plots → Relações entre Features**
   - *Por que:* Verificar se a fronteira de decisão é linear ou não-linear (justifica a escolha de kernel RBF)
   - *Insight:* `radius_mean` vs `area_mean` mostra clusters com fronteira curva → SVM linear não é suficiente

5. **Heatmap de Correlação → Multicolinearidade**
   - *Por que:* Features altamente correlacionadas (>0.9) são redundantes e podem afetar performance
   - *Insight:* radius/perimeter/area são fortemente correlacionados → confirma redundância, mas SVM lida bem com isso

### ETAPA 3: Pré-processamento

**3.1 Encoding do Target**
```python
diagnosis: M → 1 (maligno), B → 0 (benigno)
```
- *Por que:* Algoritmos de ML requerem valores numéricos
- *Por que 1=Maligno:* Convenção médica — a classe positiva (1) é a doença, facilitando interpretação de recall/precision

**3.2 Train/Test Split (75/25)**
- *Por que 75/25:* Padrão da literatura para datasets de tamanho médio (~500 amostras)
- *Por que não 80/20:* Com 569 amostras, 25% teste = ~142 amostras, suficiente para avaliação robusta
- *random_state=42:* Reprodutibilidade garantida

**3.3 Imputação (SimpleImputer - média)**
- *Por que incluir mesmo sem missing values:* Robustez do pipeline. Se novos dados tiverem missings, o pipeline não quebra
- *Por que média:* Para features com distribuição aproximadamente normal, a média é o estimador mais estável

**3.4 Feature Scaling (StandardScaler)**
```
z = (x - μ) / σ
```
- *Por que é CRÍTICO para SVM:* O SVM calcula distâncias entre pontos. Sem escalonamento, features com ranges maiores (ex: `area_mean` ~100-2500) dominariam features com ranges menores (ex: `smoothness_mean` ~0.05-0.16)
- *Por que StandardScaler vs MinMaxScaler:* StandardScaler é mais robusto a outliers e produz distribuições centradas em 0, ideal para kernels SVM
- *Por que fit no treino e transform no teste:* Prevenir data leakage — o teste não pode influenciar as estatísticas de normalização

### ETAPA 4: Modelagem

**Modelos escolhidos e justificativas:**

| Modelo | Por que incluir | Hiperparâmetros | Justificativa dos parâmetros |
|--------|----------------|-----------------|------------------------------|
| **SVM Linear** | Baseline — verificar se a fronteira é linearmente separável | `kernel='linear', C=1` | C=1 é o default, bom equilíbrio entre margem e erro |
| **SVM RBF** | Capturar fronteiras não-lineares (como visto nos scatter plots) | `kernel='rbf', C=2, gamma=0.01` | C=2 permite mais flexibilidade; gamma=0.01 evita overfitting |
| **Random Forest** | Ensemble de árvores — robusto, fornece feature importance | `n_estimators=100, random_state=42` | 100 árvores é padrão estável |
| **Logistic Regression** | Modelo interpretável — fornece probabilidades e coeficientes | `max_iter=1000, random_state=42` | max_iter alto para garantir convergência |
| **KNN** | Comparação não-paramétrica baseada em vizinhança | `n_neighbors=5` | k=5 é padrão, previne overfitting |

**Por que esses 5 modelos especificamente:**
1. **Diversidade de famílias:** Linear (LogReg, SVM Linear), Não-linear (SVM RBF, RF, KNN)
2. **Interpretabilidade vs Performance:** LogReg é interpretável, RF dá feature importance, SVM maximiza performance
3. **Contexto médico:** Em diagnóstico, queremos **maximizar Recall** (minimizar falsos negativos = casos de câncer não detectados)

### ETAPA 5: Avaliação

**Métricas e por que cada uma importa:**

| Métrica | O que mede | Relevância clínica |
|---------|-----------|-------------------|
| **Accuracy** | % total de acertos | Visão geral, mas enganosa com dados desbalanceados |
| **Precision** | Dos que o modelo disse "maligno", quantos realmente são | Evitar cirurgias/tratamentos desnecessários |
| **Recall (Sensibilidade)** | Dos que realmente são malignos, quantos o modelo detectou | **MAIS IMPORTANTE** — não perder diagnósticos de câncer |
| **F1-Score** | Média harmônica de Precision e Recall | Equilíbrio entre as duas |
| **Confusion Matrix** | Tabela de VP, FP, VN, FN | Visualização direta dos erros |
| **ROC-AUC** | Área sob a curva ROC | Capacidade discriminativa geral do modelo |
| **Cross-Validation** | Média de performance em K folds | Robustez e generalização |

> ⚠️ **Decisão crítica:** Em diagnóstico médico, **Recall > Precision**.  
> Um falso negativo (câncer não detectado) é **muito mais grave** que um falso positivo (alarme falso investigado por biópsia).

---

## 4. Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + TypeScript)            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ Dashboard│ │   EDA    │ │ Modelos  │ │ Predição │          │
│  │  Geral   │ │Interativo│ │Comparação│ │  Online  │          │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘          │
│       │             │            │             │                │
│  ┌────┴─────────────┴────────────┴─────────────┴────┐          │
│  │              Plotly.js (Gráficos)                 │          │
│  └──────────────────────┬───────────────────────────┘          │
└─────────────────────────┼──────────────────────────────────────┘
                          │ HTTP/REST (JSON)
┌─────────────────────────┼──────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ /api/data│ │ /api/eda │ │/api/model│ │/api/pred │          │
│  │  CRUD    │ │ Gráficos │ │Train/Eval│ │ Inferir  │          │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘          │
│       │             │            │             │                │
│  ┌────┴─────────────┴────────────┴─────────────┴────┐          │
│  │          Service Layer (scikit-learn)              │          │
│  └──────────────────────┬───────────────────────────┘          │
│                         │                                      │
│  ┌──────────────────────┴───────────────────────────┐          │
│  │         SQLAlchemy ORM + Alembic Migrations       │          │
│  └──────────────────────┬───────────────────────────┘          │
└─────────────────────────┼──────────────────────────────────────┘
                          │ SQL
┌─────────────────────────┼──────────────────────────────────────┐
│                    PostgreSQL                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ samples  │ │ features │ │ models   │ │ metrics  │          │
│  │(amostras)│ │(metadata)│ │(treinados│ │(avaliação│          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└────────────────────────────────────────────────────────────────┘
```

---

## 5. Modelagem do Banco de Dados (PostgreSQL)

### Diagrama Relacional

```sql
-- Tabela principal: armazena cada amostra do dataset
CREATE TABLE samples (
    id SERIAL PRIMARY KEY,
    original_id INTEGER,           -- ID original do dataset
    diagnosis VARCHAR(1) NOT NULL, -- 'M' ou 'B'
    diagnosis_encoded INTEGER,     -- 1 ou 0
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de features: valores numéricos de cada amostra
CREATE TABLE sample_features (
    id SERIAL PRIMARY KEY,
    sample_id INTEGER REFERENCES samples(id),
    feature_name VARCHAR(50) NOT NULL,
    feature_value FLOAT NOT NULL,
    feature_group VARCHAR(10),     -- 'mean', 'se', 'worst'
    feature_base VARCHAR(30)       -- 'radius', 'texture', etc.
);

-- Definição de features (metadata)
CREATE TABLE feature_definitions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    base_feature VARCHAR(30),
    aggregation VARCHAR(10),       -- 'mean', 'se', 'worst'
    unit VARCHAR(20),
    min_value FLOAT,
    max_value FLOAT,
    clinical_relevance TEXT
);

-- Experimentos de treinamento
CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    test_size FLOAT DEFAULT 0.25,
    random_state INTEGER DEFAULT 42,
    scaler_type VARCHAR(30) DEFAULT 'StandardScaler',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Modelos treinados
CREATE TABLE trained_models (
    id SERIAL PRIMARY KEY,
    experiment_id INTEGER REFERENCES experiments(id),
    model_type VARCHAR(50) NOT NULL,   -- 'SVM_Linear', 'SVM_RBF', etc.
    hyperparameters JSONB,              -- {'C': 1, 'kernel': 'linear'}
    model_blob BYTEA,                   -- modelo serializado (pickle)
    training_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Métricas de avaliação
CREATE TABLE model_metrics (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES trained_models(id),
    metric_name VARCHAR(30),    -- 'accuracy', 'precision', 'recall', etc.
    metric_value FLOAT,
    class_label VARCHAR(10),    -- 'B', 'M', 'weighted', 'macro'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Resultados de predição (confusion matrix detalhada)
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES trained_models(id),
    sample_id INTEGER REFERENCES samples(id),
    true_label INTEGER,
    predicted_label INTEGER,
    prediction_probability FLOAT,
    is_train BOOLEAN DEFAULT FALSE
);

-- Correlações entre features (cache)
CREATE TABLE feature_correlations (
    id SERIAL PRIMARY KEY,
    feature_a VARCHAR(50),
    feature_b VARCHAR(50),
    correlation_value FLOAT,
    experiment_id INTEGER REFERENCES experiments(id)
);
```

### Por que modelar assim (e não simplesmente uma tabela flat)?

1. **`samples` + `sample_features` (normalizado):** Permite queries flexíveis como "me dê todas as amostras onde `radius_mean > 15`" sem hardcode de colunas
2. **`feature_definitions`:** Metadata clinica de cada feature para tooltips na interface  
3. **`experiments`:** Cada execução do pipeline é um experimento versionado — permite comparar configurações
4. **`trained_models` + `model_metrics`:** Rastreabilidade completa — qual modelo, com quais parâmetros, produziu quais métricas
5. **`predictions`:** Permite recalcular confusion matrix, ROC curves, etc. sob demanda
6. **`feature_correlations`:** Cache para evitar recálculo pesado na interface

---

## 6. Estrutura de Diretórios

```
CancerMama/
├── docs/
│   ├── ARQUITETURA.md              ← Este documento
│   └── API.md                       ← Documentação dos endpoints
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  ← FastAPI app entry point
│   │   ├── config.py                ← Configurações (DB, etc.)
│   │   ├── database.py              ← Engine SQLAlchemy + Session
│   │   │
│   │   ├── models/                  ← SQLAlchemy ORM Models
│   │   │   ├── __init__.py
│   │   │   ├── sample.py
│   │   │   ├── feature.py
│   │   │   ├── experiment.py
│   │   │   └── prediction.py
│   │   │
│   │   ├── schemas/                 ← Pydantic Schemas (request/response)
│   │   │   ├── __init__.py
│   │   │   ├── sample.py
│   │   │   ├── eda.py
│   │   │   ├── model.py
│   │   │   └── prediction.py
│   │   │
│   │   ├── routers/                 ← API Endpoints
│   │   │   ├── __init__.py
│   │   │   ├── data.py              ← /api/data — CRUD de amostras
│   │   │   ├── eda.py               ← /api/eda — gráficos e estatísticas
│   │   │   ├── preprocessing.py     ← /api/preprocessing — pipeline
│   │   │   ├── models.py            ← /api/models — treino e avaliação
│   │   │   └── predictions.py       ← /api/predictions — inferência
│   │   │
│   │   ├── services/                ← Lógica de negócio
│   │   │   ├── __init__.py
│   │   │   ├── data_service.py      ← ETL, carga do CSV → PostgreSQL
│   │   │   ├── eda_service.py       ← Cálculos estatísticos
│   │   │   ├── ml_service.py        ← Treinamento e avaliação
│   │   │   └── prediction_service.py
│   │   │
│   │   └── ml/                      ← Pipeline de Machine Learning
│   │       ├── __init__.py
│   │       ├── preprocessing.py     ← Scaler, Imputer, Encoder
│   │       ├── training.py          ← Treino dos modelos
│   │       ├── evaluation.py        ← Métricas, confusion matrix
│   │       └── models_config.py     ← Config dos 5 modelos
│   │
│   ├── alembic/                     ← Migrations do banco
│   │   └── versions/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/              ← Header, Sidebar, Footer
│   │   │   ├── charts/              ← Componentes Plotly reutilizáveis
│   │   │   │   ├── DistributionChart.tsx
│   │   │   │   ├── CorrelationHeatmap.tsx
│   │   │   │   ├── BoxPlotGrid.tsx
│   │   │   │   ├── ScatterPlot.tsx
│   │   │   │   ├── ConfusionMatrix.tsx
│   │   │   │   └── ROCCurve.tsx
│   │   │   └── ui/                  ← Buttons, Cards, Tables
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx        ← Visão geral do projeto
│   │   │   ├── DataExplorer.tsx     ← Explorar o dataset
│   │   │   ├── EDA.tsx              ← Análise exploratória interativa
│   │   │   ├── Preprocessing.tsx    ← Visualizar pipeline
│   │   │   ├── Models.tsx           ← Comparação de modelos
│   │   │   └── Prediction.tsx       ← Predição com novos dados
│   │   │
│   │   ├── services/
│   │   │   └── api.ts               ← Client HTTP (axios/fetch)
│   │   │
│   │   ├── types/
│   │   │   └── index.ts             ← TypeScript interfaces
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── data/
│   └── data.csv                     ← Dataset original (já baixado)
│
├── docker-compose.yml               ← PostgreSQL + Backend + Frontend
└── README.md
```

---

## 7. Stack Tecnológica — Justificativas

### Backend: FastAPI
| Critério | Justificativa |
|----------|--------------|
| Performance | Async nativo, 3-10x mais rápido que Flask |
| Documentação | Swagger/OpenAPI gerado automaticamente |
| Type Safety | Pydantic para validação de dados |
| ML Integration | Integra nativamente com numpy/pandas |
| Data Science | Padrão da indústria para APIs de ML |

### Frontend: React + TypeScript + Plotly.js
| Critério | Justificativa |
|----------|--------------|
| Interatividade | Plotly.js oferece zoom, hover, seleção, pan nativos |
| Componentização | Cada gráfico é um componente reutilizável |
| Type Safety | TypeScript previne erros em dados complexos |
| Ecossistema | Maior ecossistema de bibliotecas UI |
| Performance | Virtual DOM para re-renders eficientes em dashboards pesados |

### Banco: PostgreSQL
| Critério | Justificativa |
|----------|--------------|
| JSONB | Armazenar hiperparâmetros e configurações como JSON nativo |
| Performance | Índices e queries otimizados para agregações analíticas |
| Integridade | Foreign keys, constraints, transactions ACID |
| Escalabilidade | Suportaria milhões de registros se o dataset crescer |
| Ferramental | pgAdmin, extensões (PostGIS, pg_trgm), backup nativo |

### ORM: SQLAlchemy + Alembic
| Critério | Justificativa |
|----------|--------------|
| Migrations | Alembic gerencia evoluções do schema de forma versionada |
| Abstração | ORM permite trocar de banco sem reescrever queries |
| Raw SQL | Permite SQL direto quando performance importa |

---

## 8. Funcionalidades da Interface Web

### Página 1: Dashboard Geral
- KPIs: total de amostras, % benigno/maligno, melhor modelo, melhor recall
- Mini-gráficos resumo
- Status do pipeline (dados carregados, modelos treinados)

### Página 2: Explorador de Dados
- Tabela interativa com paginação, busca e ordenação
- Estatísticas descritivas por coluna (hover)
- Download filtrado

### Página 3: EDA Interativa
- **Distribuição do Target:** Donut chart + bar chart com contagens
- **Histogramas:** Seletor de feature, toggle KDE, split por diagnóstico
- **Boxplots:** Grade comparativa 2×5 (mean vs worst), filtro por grupo
- **Scatter Plot:** Seletores X/Y livres, colorido por diagnóstico
- **Heatmap de Correlação:** Interativo com hover, slider de threshold, clusterização
- **Pairplot:** Features top-5 mais discriminativas

### Página 4: Pré-processamento
- Visualização antes/depois do scaling
- Distribuição do train/test split
- Pipeline visual (diagrama de fluxo)

### Página 5: Comparação de Modelos
- Tabela comparativa: Accuracy, Precision, Recall, F1, AUC
- Confusion Matrix lado a lado (5 modelos)
- Curvas ROC sobrepostas
- Feature Importance (Random Forest)
- Tempo de treinamento

### Página 6: Predição Online
- Formulário com os 30 campos (com tooltips explicando cada feature)
- Resultado: Benigno/Maligno + probabilidade
- Seletor de modelo para comparar predições

---

## 9. Roadmap de Implementação

### Fase 1 — Infraestrutura (Fundação)
- [ ] Setup do projeto (diretórios, configs)
- [ ] Docker Compose com PostgreSQL
- [ ] Backend FastAPI básico + SQLAlchemy + Alembic
- [ ] Migrations do banco de dados
- [ ] ETL: CSV → PostgreSQL

### Fase 2 — API de Dados e EDA
- [ ] Endpoints CRUD de dados (/api/data)
- [ ] Endpoints de estatísticas (/api/eda)
- [ ] Cálculos: distribuição, correlação, descritivos

### Fase 3 — Pipeline de ML
- [ ] Pipeline de preprocessing parametrizável
- [ ] Treinamento dos 5 modelos
- [ ] Avaliação e persistência de métricas
- [ ] Cross-validation

### Fase 4 — Frontend Base
- [ ] Setup React + TypeScript + Vite
- [ ] Layout: Sidebar, Header, Routing
- [ ] Integração com API (axios)
- [ ] Dashboard Geral

### Fase 5 — Visualizações Interativas
- [ ] Componentes Plotly: histogramas, boxplots, scatter
- [ ] Heatmap de correlação interativo
- [ ] Confusion matrix comparativa
- [ ] Curvas ROC

### Fase 6 — Predição e Polimento
- [ ] Formulário de predição online
- [ ] Responsividade mobile
- [ ] Dark mode
- [ ] Documentação final

---

> **Próximo passo:** Confirmar esta arquitetura e iniciar a Fase 1 — Setup da infraestrutura.
