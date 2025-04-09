"""Chat API endpoints."""

from fastapi import APIRouter

from app.agents.agent import Agent
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

# Initialize the LLM Agent
agent = Agent()


@router.post("/chat", response_model=ChatResponse)  # type: ignore[misc]
async def chat(request: ChatRequest) -> ChatResponse:
    """Process chat request and return response using LLM Agent.

    Args:
        request: Chat request containing user message.

    Returns:
        ChatResponse: Response containing assistant's message.
    """
    # Use the LLM Agent to generate a response
    response_text = agent.generate_response(request.message)
    return ChatResponse(response=response_text)
