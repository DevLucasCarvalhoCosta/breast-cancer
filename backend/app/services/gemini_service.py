import json
from google import genai
from google.genai import types

from app.config import get_settings

settings = get_settings()

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_medical_report(features_data: dict, prediction: int, probability: float) -> str:
    """
    Usa o Gemini para gerar um laudo explicativo baseado nos dados do tumor.
    """
    if not settings.GEMINI_API_KEY:
        return "Aviso: A chave da API do Gemini (GEMINI_API_KEY) não está configurada."

    diagnosis = "Maligno" if prediction == 1 else "Benigno"
    
    prompt = f"""
    Você é um oncologista sênior analisando um exame de câncer de mama.
    O sistema de Machine Learning previu que o tumor é: **{diagnosis}**
    com uma probabilidade do modelo de {probability * 100:.1f}%.

    Por favor, escreva um "Laudo Médico Explicativo" curto e profissional para o paciente (máx 3 parágrafos).
    
    Use as seguintes métricas do exame celular para embasar sua explicação técnica (foque nos valores mais discrepantes que indicam a malignidade ou benignidade):
    {json.dumps(features_data, indent=2)}

    Siga esta estrutura:
    1. **Conclusão Direta:** Informe o diagnóstico do modelo.
    2. **Justificativa Técnica:** Explique em linguagem compreensível quais fatores celulares (ex: raio, textura, área, concavidade) mais influenciaram esse resultado comparado a um tecido normal.
    3. **Aviso Médico:** Adicione um disclaimer de que este é um laudo gerado por IA/ML e o diagnóstico final deve ser feito por um patologista humano com biópsia.

    Formate a resposta em Markdown (sem usar blocos de código markdown como ```markdown).
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Erro ao gerar o laudo com Gemini: {e}"

def generate_eda_storytelling(correlation_data: dict) -> str:
    """
    Gera um resumo narrativo sobre a correlação dos dados.
    """
    if not settings.GEMINI_API_KEY:
        return "Aviso: Chave do Gemini não configurada."

    prompt = f"""
    Você é um Analista de Dados e Pesquisador Médico de Oncologia. 
    Abaixo, você tem um resumo das correlações dos dados celulares do nosso banco de dados:
    
    {json.dumps(correlation_data, indent=2)}
    
    Escreva um parágrafo que resume a história geal contada por estes dados (Data Storytelling). 
    Foque no que é mais importante (correlações fortes) para um médico saber ao classificar um tumor. 
    Mantenha em no máximo 5 linhas, tom profissional e formatado com Markdown.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Erro ao gerar storytelling com Gemini: {e}"
