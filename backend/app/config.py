from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://cancermama:cancermama_2026@localhost:5434/breast_cancer"
    APP_NAME: str = "Breast Cancer Prediction API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DATA_CSV_PATH: str = "../data/data.csv"
    TEST_SIZE: float = 0.25
    RANDOM_STATE: int = 42
    SCALER_TYPE: str = "StandardScaler"
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
