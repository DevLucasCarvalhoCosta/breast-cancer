from fastapi import APIRouter, HTTPException
from app.schemas.ai import (
    MedicalReportRequest, MedicalReportResponse,
    EDAStorytellingRequest, EDAStorytellingResponse
)
from app.services.gemini_service import generate_medical_report, generate_eda_storytelling

router = APIRouter(prefix="/api/ai", tags=["Generative AI"])

@router.post("/report", response_model=MedicalReportResponse)
def get_medical_report(req: MedicalReportRequest):
    try:
        report_text = generate_medical_report(
            features_data=req.features_data,
            prediction=req.prediction,
            probability=req.probability
        )
        return MedicalReportResponse(report=report_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/eda-summary", response_model=EDAStorytellingResponse)
def get_eda_summary(req: EDAStorytellingRequest):
    try:
        story_text = generate_eda_storytelling(correlation_data=req.correlation_data)
        return EDAStorytellingResponse(story=story_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
