from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, LargeBinary, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    test_size = Column(Float, default=0.25)
    random_state = Column(Integer, default=42)
    scaler_type = Column(String(30), default="StandardScaler")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    models = relationship("TrainedModel", back_populates="experiment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Experiment(id={self.id}, name='{self.name}')>"


class TrainedModel(Base):
    __tablename__ = "trained_models"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False)
    model_type = Column(String(50), nullable=False, index=True)
    hyperparameters = Column(JSONB, default={})
    model_blob = Column(LargeBinary, nullable=True)
    scaler_blob = Column(LargeBinary, nullable=True)
    training_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    experiment = relationship("Experiment", back_populates="models")
    metrics = relationship("ModelMetric", back_populates="model", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="model", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TrainedModel(id={self.id}, type='{self.model_type}')>"


class ModelMetric(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("trained_models.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(30), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    class_label = Column(String(10), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    model = relationship("TrainedModel", back_populates="metrics")

    def __repr__(self):
        return f"<ModelMetric({self.metric_name}={self.metric_value:.4f}, class={self.class_label})>"
