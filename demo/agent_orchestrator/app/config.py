"""애플리케이션 설정 모듈.

환경 변수 및 설정값 관리를 담당합니다.
"""

import os
from typing import List, Optional

# 서비스 설정
SERVICE_NAME: str = "agent-orchestrator"
SERVICE_VERSION: str = "1.0.0"
SERVICE_DESCRIPTION: str = "Agent 오케스트레이션을 위한 마이크로서비스"

# 서버 설정
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8001"))
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# API 접두사
API_PREFIX: str = "/api/v1"

# CORS 설정
ALLOW_ORIGINS: List[str] = os.getenv("ALLOW_ORIGINS", "*").split(",")

# 브로커 서비스 설정
BROKER_BASE_URL: str = os.getenv("BROKER_BASE_URL", "http://localhost:8000")

# LLM API 설정
GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-pro")

# HTTP 클라이언트 설정
REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "30.0"))
RETRY_COUNT: int = int(os.getenv("RETRY_COUNT", "3"))
