"""Broker related Pydantic models."""

from typing import List

from pydantic import BaseModel, Field


# ---------- Pydantic Model ----------
class AgentRegistration(BaseModel):
    """Agent registration model."""

    name: str = Field(..., example="TaxExpert")
    endpoint: str = Field(..., example="http://localhost:8001")
    description: str
    skills: List[str]
    type: str = "llm"
