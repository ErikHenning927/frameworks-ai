import json
from typing import Any, Dict

def ensure_dict(response_data: Any) -> Dict[str, Any]:
    """ Ensures the response from any agent is always a structured dictionary. """
    if isinstance(response_data, dict):
        return response_data
    if hasattr(response_data, "model_dump"):
        return response_data.model_dump()
    if hasattr(response_data, "dict"):
        return response_data.dict()
    if isinstance(response_data, str):
        try:
            return json.loads(response_data)
        except (json.JSONDecodeError, TypeError):
            return {"raw_output": response_data}
    
    return {"raw_output": str(response_data)}
