"""데이터 스키마 모듈.

Pydantic 모델을 사용한 요청 및 응답 스키마를 정의합니다.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    """Agent 등록을 위한 요청 스키마."""

    name: str = Field(..., description="에이전트 고유 이름")
    endpoint: str = Field(..., description="에이전트 API 엔드포인트 URL")
    description: str = Field(..., description="에이전트 역할 설명")
    skills: List[str] = Field(..., description="에이전트가 보유한 기술 목록")


class AgentUpdate(BaseModel):
    """Agent 정보 업데이트를 위한 요청 스키마."""

    endpoint: Optional[str] = Field(None, description="에이전트 API 엔드포인트 URL")
    description: Optional[str] = Field(None, description="에이전트 역할 설명")
    skills: Optional[List[str]] = Field(None, description="에이전트가 보유한 기술 목록")


class AgentResponse(BaseModel):
    """Agent 정보 응답 스키마."""

    name: str = Field(..., description="에이전트 고유 이름")
    endpoint: str = Field(..., description="에이전트 API 엔드포인트 URL")
    description: str = Field(..., description="에이전트 역할 설명")
    skills: List[str] = Field(..., description="에이전트가 보유한 기술 목록")
    registered_at: str = Field(..., description="등록 시간 (ISO 형식)")


class HealthResponse(BaseModel):
    """상태 확인 응답 스키마."""

    status: str = Field(..., description="서비스 상태")
    service: str = Field(..., description="서비스 이름")
    version: str = Field(..., description="서비스 버전")
    timestamp: str = Field(..., description="응답 시간 (ISO 형식)")
