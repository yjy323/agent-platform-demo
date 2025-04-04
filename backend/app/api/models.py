from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class EmailRequest(BaseModel):
    """이메일 분석 요청 모델"""
    email: Dict[str, Any]

class AnalysisResponse(BaseModel):
    """이메일 분석 응답 모델"""
    importance: str
    needs_response: str
    summary: str
    suggested_action: Optional[str] = None

class CommandRequest(BaseModel):
    """명령 처리 요청 모델"""
    command: str
    emails: List[Dict[str, Any]]

class CommandResponse(BaseModel):
    """명령 처리 응답 모델"""
    message: str
    filtered_emails: Optional[List[Dict[str, Any]]] = None
    llm_response: Optional[str] = None

class HealthResponse(BaseModel):
    """서버 상태 응답 모델"""
    status: str
    message: str
    llm_info: Optional[Dict[str, Any]] = None
