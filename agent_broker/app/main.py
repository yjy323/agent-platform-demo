"""애플리케이션 진입점.

FastAPI 애플리케이션 초기화 및 설정을 담당합니다.
"""

from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOW_ORIGINS, SERVICE_DESCRIPTION, SERVICE_NAME, SERVICE_VERSION
from app.routes import router

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
app.include_router(router)


# 루트 엔드포인트
@app.get("/")  # type: ignore
def root() -> Dict[str, Any]:
    """서비스 정보 제공 엔드포인트.

    Returns:
        Dict: 서비스 메타데이터
    """
    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "description": SERVICE_DESCRIPTION,
        "endpoints": [
            {
                "path": "/agents",
                "methods": ["GET", "POST"],
                "description": "에이전트 목록 조회 및 등록",
            },
            {
                "path": "/agents/{agent_name}",
                "methods": ["GET", "PUT", "DELETE"],
                "description": "특정 에이전트 조회, 업데이트, 삭제",
            },
            {"path": "/health", "methods": ["GET"], "description": "서비스 상태 확인"},
        ],
    }


if __name__ == "__main__":
    import uvicorn

    from app.config import DEBUG, HOST, PORT

    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=DEBUG)
