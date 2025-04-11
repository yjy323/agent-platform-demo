from typing import Dict, List

from fastapi import APIRouter, HTTPException

from app.agents.broker import AgentBroker
from app.schemas.registration_agent import RegistrationAgent

router = APIRouter()

# ---------- Global Registry ----------
broker = AgentBroker()


# ---------- API Endpoint ----------
@router.post("/agents")  # type: ignore
def register_agent(agent: RegistrationAgent) -> Dict[str, str]:
    print(agent)
    try:
        broker.register(agent.model_dump())
        return {
            "status": "success",
            "message": f"Agent '{agent.name}' registered successfully.",
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get("/agents")  # type: ignore
def list_agents() -> List[Dict]:
    return broker.list_agents()


@router.get("/agents/{name}")  # type: ignore
def get_agent(name: str) -> Dict:
    try:
        return broker.get_agent(name)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
