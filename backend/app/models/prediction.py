from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("trained_models.id", ondelete="CASCADE"), nullable=False, index=True)
    sample_id = Column(Integer, ForeignKey("samples.id", ondelete="CASCADE"), nullable=False, index=True)
    true_label = Column(Integer, nullable=False)
    predicted_label = Column(Integer, nullable=False)
    prediction_probability = Column(Float, nullable=True)
    is_train = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    model = relationship("TrainedModel", back_populates="predictions")
    sample = relationship("Sample", back_populates="predictions")

    def __repr__(self):
        acerto = "V" if self.true_label == self.predicted_label else "X"
        return f"<Prediction({acerto} real={self.true_label}, pred={self.predicted_label})>"
