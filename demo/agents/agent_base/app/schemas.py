from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    """API 요청에 사용되는 프롬프트 모델"""

    prompt: str = Field(..., description="사용자 입력 프롬프트")
    context: Optional[Dict[str, Any]] = Field(
        default={}, description="추가 컨텍스트 정보 (선택 사항)"
    )


class AgentDescription(BaseModel):
    """에이전트 자기 설명 정보 모델"""

    name: str = Field(..., description="에이전트 이름")
    description: str = Field(..., description="에이전트 역할 설명")
    skills: List[str] = Field(..., description="에이전트 기술 목록")


class AgentResponse(BaseModel):
    """API 응답에 사용되는 에이전트 응답 모델"""

    agent_name: str = Field(..., description="응답한 에이전트 이름")
    response: str = Field(..., description="LLM의 응답 내용")
    status: str = Field(default="success", description="처리 상태")


class ErrorResponse(BaseModel):
    """API 에러 응답 모델"""

    status: str = Field(default="error", description="에러 상태")
    message: str = Field(..., description="에러 메시지")
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="추가 에러 세부정보"
    )
