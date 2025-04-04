from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from ..agents.email_agent import EmailAgent
from ..agents.command_agent import CommandAgent
from ..services.llm_service import LLMService
from .models import EmailRequest, AnalysisResponse, CommandRequest, CommandResponse, HealthResponse

router = APIRouter()

# 의존성 주입을 위한 함수
def get_llm_service():
    return LLMService()

def get_email_agent(llm_service: LLMService = Depends(get_llm_service)):
    return EmailAgent(llm_service)

def get_command_agent(llm_service: LLMService = Depends(get_llm_service)):
    return CommandAgent(llm_service)

@router.post("/analyze_email", response_model=AnalysisResponse)
async def analyze_email(
    request: EmailRequest, 
    email_agent: EmailAgent = Depends(get_email_agent)
):
    """이메일 분석 엔드포인트"""
    try:
        result = await email_agent.process(request.email)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이메일 분석 중 오류 발생: {str(e)}")

@router.post("/process_command", response_model=CommandResponse)
async def process_command(
    request: CommandRequest, 
    command_agent: CommandAgent = Depends(get_command_agent)
):
    """명령 처리 엔드포인트"""
    try:
        result = await command_agent.process(request.command, request.emails)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"명령 처리 중 오류 발생: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check(llm_service: LLMService = Depends(get_llm_service)):
    """헬스체크 엔드포인트"""
    return {
        "status": "ok",
        "message": "이메일 관리 에이전트 API가 정상 작동 중입니다.",
        "llm_info": llm_service.get_model_info()
    }
