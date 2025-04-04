import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .api.routes import router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# FastAPI 앱 초기화
app = FastAPI(
    title="이메일 관리 에이전트 API",
    description="LLM 기반 이메일 관리 에이전트 API",
    version="0.1.0",
)

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:8501",  # Streamlit 기본 포트
    "http://frontend:8501",   # Docker 컨테이너 서비스명
    "*",                      # 개발 환경에서 모든 출처 허용 (프로덕션에서는 제한 필요)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "이메일 관리 에이전트 API에 오신 것을 환영합니다.",
        "docs_url": "/docs",
    }

# 앱 시작 이벤트
@app.on_event("startup")
async def startup_event():
    logger.info("이메일 관리 에이전트 API 서버가 시작되었습니다.")

# 앱 종료 이벤트
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("이메일 관리 에이전트 API 서버가 종료되었습니다.")
