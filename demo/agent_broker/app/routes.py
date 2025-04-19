"""API 라우트 모듈.

Agent Broker 서비스의 엔드포인트를 정의합니다.
"""

from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.broker import AgentBroker, get_broker
from app.config import SERVICE_NAME, SERVICE_VERSION
from app.schemas import AgentCreate, AgentResponse, AgentUpdate, HealthResponse

# 라우터 생성
router = APIRouter()


@router.post(
    "/agents", response_model=AgentResponse, status_code=status.HTTP_201_CREATED
)  # type: ignore
def register_agent(
    agent_data: AgentCreate, broker: AgentBroker = Depends(get_broker)
) -> Dict[str, Any]:
    """새로운 에이전트 등록 엔드포인트.

    Args:
        agent_data: 등록할 에이전트 정보
        broker: AgentBroker 인스턴스 (의존성 주입)

    Returns:
        Dict[str, Any]: 등록된 에이전트 정보

    Raises:
        HTTPException: 에이전트 등록 실패 시
    """
    try:
        return broker.register(agent_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/agents", response_model=List[AgentResponse])  # type: ignore
def list_agents(broker: AgentBroker = Depends(get_broker)) -> List[Dict[str, Any]]:
    """등록된 모든 에이전트 목록 조회 엔드포인트.

    Args:
        broker: AgentBroker 인스턴스 (의존성 주입)

    Returns:
        List[Dict[str, Any]]: 등록된 모든 에이전트 정보 목록
    """
    return broker.list_agents()


@router.get("/agents/{agent_name}", response_model=AgentResponse)  # type: ignore
def get_agent(
    agent_name: str, broker: AgentBroker = Depends(get_broker)
) -> Dict[str, Any]:
    """특정 에이전트 정보 조회 엔드포인트.

    Args:
        agent_name: 조회할 에이전트 이름
        broker: AgentBroker 인스턴스 (의존성 주입)

    Returns:
        Dict[str, Any]: 에이전트 정보

    Raises:
        HTTPException: 에이전트가 존재하지 않을 경우
    """
    try:
        return broker.get_agent(agent_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/agents/{agent_name}", response_model=AgentResponse)  # type: ignore
def update_agent(
    agent_name: str, agent_data: AgentUpdate, broker: AgentBroker = Depends(get_broker)
) -> Dict[str, Any]:
    """에이전트 정보 업데이트 엔드포인트.

    Args:
        agent_name: 업데이트할 에이전트 이름
        agent_data: 업데이트할 정보
        broker: AgentBroker 인스턴스 (의존성 주입)

    Returns:
        Dict[str, Any]: 업데이트된 에이전트 정보

    Raises:
        HTTPException: 에이전트가 존재하지 않을 경우
    """
    try:
        # 널이 아닌 필드만 포함
        update_data = {k: v for k, v in agent_data.dict().items() if v is not None}
        return broker.update_agent(agent_name, update_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/agents/{agent_name}", status_code=status.HTTP_204_NO_CONTENT
)  # type: ignore
def delete_agent(agent_name: str, broker: AgentBroker = Depends(get_broker)) -> None:
    """에이전트 등록 해제 엔드포인트.

    Args:
        agent_name: 삭제할 에이전트 이름
        broker: AgentBroker 인스턴스 (의존성 주입)

    Raises:
        HTTPException: 에이전트가 존재하지 않을 경우
    """
    try:
        broker.delete_agent(agent_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/health", response_model=HealthResponse)  # type: ignore
def health_check() -> Dict[str, Any]:
    """서비스 상태 확인 엔드포인트.

    Returns:
        Dict[str, Any]: 서비스 상태 정보
    """
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "timestamp": datetime.now().isoformat(),
    }
