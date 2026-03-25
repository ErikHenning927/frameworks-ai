from fastapi import APIRouter, HTTPException
from app.core.models import AgentRequest, AgentResponse
from app.agents.CrewAi import run_crewai_agent
from app.agents.langgraph import run_langgraph_agent
from app.agents.pydantic import run_pydantic_agent
from app.utils.helpers import ensure_dict

router = APIRouter()

@router.post("/crewai", response_model=AgentResponse)
async def endpoint_crewai(request: AgentRequest):
    """ Edge para disparar o orquestrador CrewAI """
    try:
        resultado = run_crewai_agent(request.query)
        dict_res = ensure_dict(resultado)
        return AgentResponse(agent_name="CrewAI Orchestrator", result=dict_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do CrewAI: {str(e)}")

@router.post("/langgraph", response_model=AgentResponse)
async def endpoint_langgraph(request: AgentRequest):
    """ Edge para disparar o agente LangGraph """
    try:
        resultado = run_langgraph_agent(request.query)
        dict_res = ensure_dict(resultado)
        return AgentResponse(agent_name="LangGraph", result=dict_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do LangGraph: {str(e)}")

@router.post("/pydantic", response_model=AgentResponse)
async def endpoint_pydantic(request: AgentRequest):
    """ Edge para disparar o agente Pydantic (StructuredOutputs OpenAI) """
    try:
        resultado = run_pydantic_agent(request.query)
        dict_res = ensure_dict(resultado)
        return AgentResponse(agent_name="PydanticAI", result=dict_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do Pydantic: {str(e)}")
