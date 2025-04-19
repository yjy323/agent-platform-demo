"""데이터 스키마 모듈.

Pydantic 모델을 사용한 요청 및 응답 스키마를 정의합니다.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    """작업 요청 스키마."""

    prompt: str = Field(..., description="사용자 입력 프롬프트")
    context: Optional[Dict[str, Any]] = Field(
        default=None, description="작업 컨텍스트 (선택 사항)"
    )


class TaskResponse(BaseModel):
    """작업 응답 스키마."""

    task_id: str = Field(..., description="작업 고유 식별자")
    selected_agent: str = Field(..., description="선택된 에이전트 이름")
    result: Dict[str, Any] = Field(..., description="작업 처리 결과")
    execution_time: float = Field(..., description="실행 시간 (초)")


class HealthResponse(BaseModel):
    """상태 확인 응답 스키마."""

    status: str = Field(..., description="서비스 상태")
    service: str = Field(..., description="서비스 이름")
    version: str = Field(..., description="서비스 버전")
    timestamp: str = Field(..., description="응답 시간 (ISO 형식)")
