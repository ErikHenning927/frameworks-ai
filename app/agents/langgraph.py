import operator
from datetime import datetime
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from app.core.config import settings

class LangGraphOutput(BaseModel):
    reasoning: str = Field(description="A elaboração passo a passo do raciocínio focado nos dados de e-commerce.")
    final_answer: str = Field(description="A resposta analítica e de negócios para o usuário final.")

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    final_answer: str
    reasoning: str

def run_langgraph_agent(query: str) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
    structured_llm = llm.with_structured_output(LangGraphOutput)

    def process_node(state: AgentState):
        messages = state["messages"]
        response = structured_llm.invoke(messages)
        return {
            "messages": [AIMessage(content=response.final_answer)], 
            "final_answer": response.final_answer,
            "reasoning": response.reasoning
        }

    workflow = StateGraph(AgentState)
    workflow.add_node("process", process_node)
    
    # Simple flow: start -> process -> end
    workflow.set_entry_point("process")
    workflow.add_edge("process", END)

    app = workflow.compile()
    
    current_date = datetime.now().strftime('%d/%m/%Y')
    system_prompt = f"Você é um Analista Estratégico Especialista em E-commerce. Forneça respostas analíticas claras focadas em métricas do varejo (LTV, CAC, ROI, ticket médio) e direcione as decisões de negócio de forma acionável em Português do Brasil. Lembre-se, a data atual do sistema é {current_date}."

    inputs = {"messages": [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]}
    result = app.invoke(inputs)
    
    return {
        "engine": "LangGraph",
        "estado_final": "Concluido",
        "reasoning": result.get("reasoning", ""),
        "resposta_gerada": result.get("final_answer", "")
    }
