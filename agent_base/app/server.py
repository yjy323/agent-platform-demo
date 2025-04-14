import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.agent_base import BaseAgent
from app.schemas import AgentDescription, AgentResponse, PromptRequest  # type: ignore


def create_agent_app(agent: BaseAgent) -> FastAPI:
    """
    에이전트 인스턴스를 기반으로 FastAPI 앱 생성

    Args:
        agent: BaseAgent 인스턴스

    Returns:
        FastAPI: 구성된 FastAPI 애플리케이션
    """
    # FastAPI 앱 생성
    app = FastAPI(
        title=f"{agent.name} Service",
        description=f"API for {agent.name} - {agent.description}",
        version="1.0.0",
    )

    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 프로덕션에서는 특정 오리진으로 제한해야 함
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 에이전트 설명 엔드포인트 (GET)
    @app.get(
        "/agent/describe",
        response_model=AgentDescription,
        summary="에이전트 설명 조회",
        description="에이전트의 이름, 설명, 기술 및 사용 중인 모델 정보를 반환합니다.",
    )  # type: ignore[misc]
    async def get_agent_description() -> AgentDescription:
        return agent.describe()

    # 프롬프트 처리 엔드포인트 (POST)
    @app.post(
        "/agent/run",
        response_model=AgentResponse,
        summary="프롬프트 처리",
        description="사용자 프롬프트를 처리하고 에이전트의 응답을 반환합니다.",
    )  # type: ignore[misc]
    async def process_prompt(request: PromptRequest) -> dict:
        try:
            response = agent.run(request.text)
            return {"agent_name": agent.name, "response": response, "status": "success"}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail={"status": "error", "message": str(e)}
            )

    # 헬스 체크 엔드포인트
    @app.get(
        "/health",
        summary="서비스 상태 확인",
        description="서비스가 정상적으로 실행 중인지 확인합니다.",
    )  # type: ignore[misc]
    async def health_check() -> dict:
        return {"status": "healthy", "agent": agent.name}

    return app


def run_agent_app(agent: BaseAgent, host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    에이전트 애플리케이션 실행

    Args:
        agent: BaseAgent 인스턴스
        host: 서버 호스트 (기본값: "0.0.0.0")
        port: 서버 포트 (기본값: 8000)
    """
    app = create_agent_app(agent)
    uvicorn.run(app, host=host, port=port)
