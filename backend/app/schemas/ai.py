from pydantic import BaseModel, Field

class MedicalReportRequest(BaseModel):
    features_data: dict[str, float] = Field(..., description="Dicionário com os dados das features da amostra")
    prediction: int = Field(..., description="Predição final do modelo (0 para Benigno, 1 para Maligno)")
    probability: float = Field(..., description="Probabilidade associada à predição (0.0 a 1.0)")

class MedicalReportResponse(BaseModel):
    report: str = Field(..., description="Laudo médico explicativo em Markdown gerado pelo Gemini")

class EDAStorytellingRequest(BaseModel):
    correlation_data: dict = Field(..., description="Dados agregados ou matriz de correlação para gerar o storytelling")

class EDAStorytellingResponse(BaseModel):
    story: str = Field(..., description="Resumo em Markdown descrevendo a história dos dados contado pelo Gemini")
