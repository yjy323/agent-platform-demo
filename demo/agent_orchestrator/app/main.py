"""애플리케이션 진입점.

FastAPI 애플리케이션 초기화 및 설정을 담당합니다.
"""

import logging
from typing import Any, Dict, List

from app.config import (
    ALLOW_ORIGINS,
    API_PREFIX,
    SERVICE_DESCRIPTION,
    SERVICE_NAME,
    SERVICE_VERSION,
)
from app.routes import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# FastAPI 애플리케이션 생성
app = FastAPI(
    title=SERVICE_NAME,
    description=SERVICE_DESCRIPTION,
    version=SERVICE_VERSION,
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(router, prefix=API_PREFIX)


# 루트 엔드포인트
@app.get("/")
def root() -> Dict[str, Any]:
    """서비스 정보 제공 엔드포인트.

    Returns:
        Dict[str, Any]: 서비스 메타데이터
    """
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "endpoints": [
            {
                "path": f"{API_PREFIX}/tasks",
                "methods": ["POST"],
                "description": "작업 제출 및 자동 에이전트 선택",
            },
            {
                "path": f"{API_PREFIX}/tasks/{{agent_name}}",
                "methods": ["POST"],
                "description": "특정 에이전트에게 직접 작업 할당",
            },
            {
                "path": f"{API_PREFIX}/select-agent",
                "methods": ["POST"],
                "description": "적합한 에이전트 선택 (작업 실행 없음)",
            },
            {
                "path": f"{API_PREFIX}/agents",
                "methods": ["GET"],
                "description": "현재 사용 가능한 에이전트 목록 조회",
            },
            {
                "path": f"{API_PREFIX}/agents/{{agent_name}}",
                "methods": ["GET"],
                "description": "특정 에이전트 정보 조회",
            },
            {
                "path": f"{API_PREFIX}/health",
                "methods": ["GET"],
                "description": "서비스 상태 확인",
            },
        ],
    }


if __name__ == "__main__":
    import uvicorn
    from app.config import DEBUG, HOST, PORT

    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=DEBUG)
