from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class SampleFeature(Base):
    __tablename__ = "sample_features"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id", ondelete="CASCADE"), nullable=False, index=True)
    feature_name = Column(String(50), nullable=False, index=True)
    feature_value = Column(Float, nullable=False)
    feature_group = Column(String(10), nullable=False)
    feature_base = Column(String(30), nullable=False)

    sample = relationship("Sample", back_populates="features")

    def __repr__(self):
        return f"<SampleFeature(sample_id={self.sample_id}, {self.feature_name}={self.feature_value})>"


class FeatureDefinition(Base):
    __tablename__ = "feature_definitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    base_feature = Column(String(30), nullable=False)
    aggregation = Column(String(10), nullable=False)
    unit = Column(String(20))
    min_value = Column(Float)
    max_value = Column(Float)
    clinical_relevance = Column(Text)

    def __repr__(self):
        return f"<FeatureDefinition(name='{self.name}')>"


class FeatureCorrelation(Base):
    __tablename__ = "feature_correlations"

    id = Column(Integer, primary_key=True, index=True)
    feature_a = Column(String(50), nullable=False, index=True)
    feature_b = Column(String(50), nullable=False, index=True)
    correlation_value = Column(Float, nullable=False)
    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=True)

    def __repr__(self):
        return f"<FeatureCorrelation({self.feature_a} <> {self.feature_b}: {self.correlation_value:.3f})>"
