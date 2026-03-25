from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class AgentRequest(BaseModel):
    query: str = Field(..., description="The main input/question for the agent to process")
    session_id: Optional[str] = Field(None, description="Optional session tracking ID")

class AgentResponse(BaseModel):
    agent_name: str
    status: str = "success"
    result: Dict[str, Any]
    error: Optional[str] = None
