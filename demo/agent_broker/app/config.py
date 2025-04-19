"""
애플리케이션 설정 모듈.

환경 변수 및 설정값 관리를 담당합니다.
"""

import os
from typing import List

# 서비스 설정
SERVICE_NAME: str = "agent-broker"
SERVICE_VERSION: str = "1.0.0"
SERVICE_DESCRIPTION: str = "Agent 등록 및 관리를 위한 마이크로서비스"

# 서버 설정
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# API 접두사
API_PREFIX: str = "/api/v1"

# CORS 설정
ALLOW_ORIGINS: List[str] = os.getenv("ALLOW_ORIGINS", "*").split(",")
