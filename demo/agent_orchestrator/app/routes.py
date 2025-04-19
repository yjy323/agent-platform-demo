"""API 라우트 모듈.

Orchestrator 서비스의 엔드포인트를 정의합니다.
"""

from datetime import datetime
from typing import Any, Dict, List

from app.config import SERVICE_NAME, SERVICE_VERSION
from app.orchestrator import Orchestrator, get_orchestrator
from app.schemas import HealthResponse, TaskRequest, TaskResponse
from fastapi import APIRouter, Depends, HTTPException, status

# 라우터 생성
router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
async def submit_task(
    task_request: TaskRequest, orchestrator: Orchestrator = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """작업을 제출하고 자동으로 적합한 에이전트를 선택하여 실행합니다.

    Args:
        task_request: 작업 요청 데이터
        orchestrator: Orchestrator 인스턴스 (의존성 주입)

    Returns:
        Dict[str, Any]: 작업 실행 결과

    Raises:
        HTTPException: 작업 실행 실패 시
    """
    try:
        return await orchestrator.execute_task(
            task_request.prompt, task_request.context
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task execution failed: {str(e)}",
        )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> Dict[str, Any]:
    """서비스 상태를 확인합니다.

    Returns:
        Dict[str, Any]: 서비스 상태 정보
    """

    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "timestamp": datetime.now().isoformat(),
    }
