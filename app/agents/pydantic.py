from datetime import datetime
from pydantic import BaseModel, Field
from openai import OpenAI
from app.core.config import settings

class PydanticAgentOutput(BaseModel):
    reasoning: str = Field(description="A linha de raciocínio passo a passo utilizada na inteligência dos dados (chain of thought).")
    summary: str = Field(description="O resumo direto da resposta processada pelo agente.")
    bullet_points: list[str] = Field(description="Uma lista de pontos-chave derivados da resposta.")
    confidence_score: float = Field(description="Um número de 0.0 a 1.0 indicando a confiabilidade da resposta.")

def run_pydantic_agent(query: str) -> dict:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        current_date = datetime.now().strftime('%d/%m/%Y')
        system_prompt = f"Você é um renomado Analista de Dados de E-commerce. Seu foco absoluto é processar e detalhar métricas de varejo online (LTV, CAC, ROI, ticket médio) fornecendo sempre JSON perfeitamente estruturado. Leve em consideração que hoje é {current_date}."

        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            response_format=PydanticAgentOutput
        )
        
        parsed_result = response.choices[0].message.parsed
        if parsed_result:
            return parsed_result.model_dump()
        else:
            return {"error": "A API não retornou o formato estruturado esperado."}
            
    except Exception as e:
        return {"error": f"Erro interno no agente Pydantic: {str(e)}"}
