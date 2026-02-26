from pydantic import BaseModel
from typing import Optional


class DistributionData(BaseModel):
    feature_name: str
    values_benign: list[float]
    values_malignant: list[float]


class BoxPlotData(BaseModel):
    feature_name: str
    benign: list[float]
    malignant: list[float]


class ScatterData(BaseModel):
    x_feature: str
    y_feature: str
    x_values: list[float]
    y_values: list[float]
    diagnoses: list[str]


class CorrelationMatrix(BaseModel):
    feature_names: list[str]
    matrix: list[list[float]]


class DescriptiveStats(BaseModel):
    feature_name: str
    count: int
    mean: float
    std: float
    min: float
    q25: float
    median: float
    q75: float
    max: float
    skewness: float
    kurtosis: float


class FeatureImportanceItem(BaseModel):
    feature_name: str
    importance: float
