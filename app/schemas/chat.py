"""Chat related Pydantic models."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str


class ChatResponse(BaseModel):
    """Chat response model."""

    response: str
