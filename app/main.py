import sys
import os
# Adiciona o diretório raiz ao PYTHONPATH para resolver as importações 'app....'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API com Arquitetura Moderna para agentes CrewAI, LangGraph e Pydantic via OpenAI"
)

app.include_router(api_router, prefix="/api/agents", tags=["Agents"])

@app.get("/")
def read_root():
    return {
        "message": "Agentes de IA prontos. Consulte o Swagger UI em /docs para testar os endpoints.",
        "endpoints": [
            "/api/agents/crewai",
            "/api/agents/langgraph",
            "/api/agents/pydantic"
        ]
    }

if __name__ == "__main__":
    # Comando útil para rodar na raíz do projeto: 
    # uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
