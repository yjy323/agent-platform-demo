"""
테스트를 위한 공통 픽스처
"""

import pytest

from agent_discovery.consul_client import ConsulDiscoveryClient
from agents.common.types import (
    AgentAuthentication,
    AgentCapabilities,
    AgentCard,
    AgentProvider,
    AgentSkill,
)


@pytest.fixture
def consul_client() -> ConsulDiscoveryClient:
    """Consul 클라이언트 픽스처"""
    return ConsulDiscoveryClient(host="localhost", port=8500)


@pytest.fixture
def sample_agent_card() -> AgentCard:
    """샘플 에이전트 카드 픽스처"""
    return AgentCard(
        name="test-agent",
        description="Test Agent Description",
        version="1.0.0",
        url="http://localhost:8000",
        capabilities=AgentCapabilities(
            streaming=True, pushNotifications=False, stateTransitionHistory=True
        ),
        authentication=AgentAuthentication(schemes=["basic", "oauth2"]),
        provider=AgentProvider(organization="Test Org", url="http://test.org"),
        documentationUrl="http://docs.test.org",
        defaultInputModes=["text", "voice"],
        defaultOutputModes=["text", "image"],
        skills=[
            AgentSkill(
                id="test-skill",
                name="Test Skill",
                description="A test skill",
                tags=["test"],
            )
        ],
    )
