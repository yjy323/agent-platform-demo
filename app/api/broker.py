from typing import Dict

from fastapi import APIRouter, HTTPException

from app.agents.broker import AgentRegistry
from app.schemas.broker import AgentRegistration

router = APIRouter()

# ---------- Global Registry ----------
registry = AgentRegistry()


# ---------- API Endpoint ----------
@router.post("/agents")  # type: ignore
def register_agent(agent: AgentRegistration) -> Dict[str, str]:
    print(agent)
    try:
        registry.register(agent.model_dump())
        return {
            "status": "success",
            "message": f"Agent '{agent.name}' registered successfully.",
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
