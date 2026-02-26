from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExperimentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    test_size: float = 0.25
    random_state: int = 42
    scaler_type: str = "StandardScaler"


class ExperimentResponse(ExperimentCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TrainedModelResponse(BaseModel):
    id: int
    experiment_id: int
    model_type: str
    hyperparameters: dict
    training_time_ms: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ModelMetricResponse(BaseModel):
    metric_name: str
    metric_value: float
    class_label: Optional[str]

    class Config:
        from_attributes = True


class ModelComparisonItem(BaseModel):
    model_id: int
    model_type: str
    accuracy: float
    precision_macro: float
    recall_macro: float
    f1_macro: float
    roc_auc: Optional[float]
    training_time_ms: Optional[int]


class ConfusionMatrixData(BaseModel):
    model_type: str
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int


class ROCCurveData(BaseModel):
    model_type: str
    fpr: list[float]
    tpr: list[float]
    auc: float
