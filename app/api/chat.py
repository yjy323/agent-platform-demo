"""Chat API endpoints."""

from fastapi import APIRouter

from app.agents import GeneralAssistantAgent, LLMOrchestrator, TaxExpertAgent
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()

# Initialize the agents
tax_agent = TaxExpertAgent()
general_agent = GeneralAssistantAgent()
agents = [tax_agent, general_agent]

# Initialize the orchestrator
orchestrator = LLMOrchestrator(agents)


@router.post("/chat", response_model=ChatResponse)  # type: ignore[misc]
async def chat(request: ChatRequest) -> ChatResponse:
    """Process chat request and return response using LLM Orchestrator.

    Args:
        request: Chat request containing user message.

    Returns:
        ChatResponse: Response containing assistant's message.
    """
    # Use the LLM Orchestrator to handle the request and generate a response
    response_text = orchestrator.handle_request(request.message)
    return ChatResponse(response=response_text)
