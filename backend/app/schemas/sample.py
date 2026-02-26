from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SampleBase(BaseModel):
    original_id: int
    diagnosis: str = Field(..., pattern="^[MB]$")
    diagnosis_encoded: int = Field(..., ge=0, le=1)


class SampleCreate(SampleBase):
    features: dict[str, float]


class SampleResponse(SampleBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SampleWithFeatures(SampleResponse):
    features: dict[str, float] = {}


class FeatureDefinitionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    base_feature: str
    aggregation: str
    unit: Optional[str]
    min_value: Optional[float]
    max_value: Optional[float]
    clinical_relevance: Optional[str]

    class Config:
        from_attributes = True


class PaginatedSamples(BaseModel):
    items: list[SampleWithFeatures]
    total: int
    page: int
    page_size: int
    total_pages: int


class DatasetStats(BaseModel):
    total_samples: int
    benign_count: int
    malignant_count: int
    benign_percentage: float
    malignant_percentage: float
    total_features: int
    missing_values: int
    duplicated_rows: int
