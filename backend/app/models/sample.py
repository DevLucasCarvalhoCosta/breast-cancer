from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Sample(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)
    original_id = Column(Integer, nullable=False)
    diagnosis = Column(String(1), nullable=False, index=True)
    diagnosis_encoded = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    features = relationship("SampleFeature", back_populates="sample", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="sample")

    def __repr__(self):
        return f"<Sample(id={self.id}, diagnosis='{self.diagnosis}')>"
