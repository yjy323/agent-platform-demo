"""
Consul 레지스트리 클라이언트 테스트
"""

import time
from copy import deepcopy
from typing import Optional

import pytest

from agent_discovery.consul_client import ConsulDiscoveryClient
from agents.common.types import AgentCard


def get_agent_id(card: AgentCard) -> str:
    """에이전트 ID를 생성합니다."""
    return f"{card.name}-{card.version}"


def wait_for_check_status(
    consul_client: ConsulDiscoveryClient,
    check_id: str,
    expected_status: str,
    timeout: float = 1.0,
    interval: float = 0.1,
) -> bool:
    """
    헬스체크 상태가 변경되기를 기다립니다.

    Args:
        consul_client: Consul 클라이언트
        check_id: 체크 ID
        expected_status: 기대하는 상태
        timeout: 최대 대기 시간 (초)
        interval: 체크 간격 (초)

    Returns:
        상태가 변경되었으면 True, 타임아웃이면 False
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        checks = consul_client._consul.agent.checks()
        if check_id in checks and checks[check_id]["Status"] == expected_status:
            return True
        time.sleep(interval)
    return False


@pytest.fixture
def unique_agent_card(sample_agent_card, request):
    """테스트마다 고유한 이름을 가진 에이전트 카드를 생성합니다."""
    card = deepcopy(sample_agent_card)
    card.name = f"{card.name}-{request.node.name}"
    return card


@pytest.fixture
def registered_agent(
    consul_client: ConsulDiscoveryClient, unique_agent_card: AgentCard, request
):
    """테스트용 에이전트를 등록하고 테스트 종료 후 삭제합니다."""
    consul_client.register(unique_agent_card)
    yield unique_agent_card
    consul_client.deregister(get_agent_id(unique_agent_card))


def find_agent_by_name(agents: list[AgentCard], name: str) -> Optional[AgentCard]:
    """에이전트 목록에서 이름으로 에이전트를 찾습니다."""
    return next((a for a in agents if a.name == name), None)


def test_consul_connection(consul_client: ConsulDiscoveryClient):
    """Consul 서버 연결 테스트"""
    # 기본 서비스 목록 조회
    index, services = consul_client._consul.catalog.services()
    assert isinstance(services, dict)

    # Consul 상태 확인
    leader = consul_client._consul.status.leader()
    assert leader is not None
    assert ":" in leader  # IP:Port 형식


def test_register_and_list_agent(
    consul_client: ConsulDiscoveryClient, unique_agent_card: AgentCard
):
    """에이전트 등록 및 조회 테스트"""
    # 등록
    consul_client.register(unique_agent_card)
    try:
        # 등록 직후 목록 조회 (비정상 상태 포함)
        agents = consul_client.list_agents(only_healthy=False)
        assert len(agents) > 0

        # 등록한 에이전트 찾기
        agent = find_agent_by_name(agents, unique_agent_card.name)
        assert agent is not None
        assert agent.version == unique_agent_card.version
        assert agent.capabilities.streaming == unique_agent_card.capabilities.streaming
        assert (
            agent.capabilities.pushNotifications
            == unique_agent_card.capabilities.pushNotifications
        )
        assert (
            agent.capabilities.stateTransitionHistory
            == unique_agent_card.capabilities.stateTransitionHistory
        )
    finally:
        # 정리
        consul_client.deregister(get_agent_id(unique_agent_card))


def test_update_agent(
    consul_client: ConsulDiscoveryClient, registered_agent: AgentCard
):
    """에이전트 수정 테스트"""
    # 수정할 카드 생성
    updated_card = deepcopy(registered_agent)
    updated_card.description = "Updated Description"
    updated_card.capabilities.streaming = not registered_agent.capabilities.streaming

    # 수정
    consul_client.update(updated_card)

    # 수정된 내용 확인
    agents = consul_client.list_agents(only_healthy=False)
    agent = find_agent_by_name(agents, updated_card.name)
    assert agent is not None
    assert agent.description == updated_card.description
    assert agent.capabilities.streaming == updated_card.capabilities.streaming


def test_deregister_agent(
    consul_client: ConsulDiscoveryClient, registered_agent: AgentCard
):
    """에이전트 삭제 테스트"""
    # 삭제
    consul_client.deregister(get_agent_id(registered_agent))

    # 삭제 확인
    agents = consul_client.list_agents(only_healthy=False)
    agent = find_agent_by_name(agents, registered_agent.name)
    assert agent is None


def test_agent_health_check(
    consul_client: ConsulDiscoveryClient, registered_agent: AgentCard
):
    """에이전트 헬스체크 테스트"""
    check_id = f"check:{get_agent_id(registered_agent)}"

    # 초기 상태는 critical (TTL 체크가 pass되지 않음)
    assert wait_for_check_status(consul_client, check_id, "critical")

    # 헬스체크 pass
    consul_client._consul.agent.check.ttl_pass(check_id)
    assert wait_for_check_status(consul_client, check_id, "passing")

    # 헬스체크 fail
    consul_client._consul.agent.check.ttl_fail(check_id)
    assert wait_for_check_status(consul_client, check_id, "critical")
