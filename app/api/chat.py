"""Chat API endpoints."""

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)  # type: ignore[misc]
async def chat(request: ChatRequest) -> ChatResponse:
    """Process chat request and return response.

    Args:
        request: Chat request containing user message.

    Returns:
        ChatResponse: Response containing assistant's message.
    """
    # Demo response - will be replaced with actual business logic later
    return ChatResponse(response="안녕하세요.")
