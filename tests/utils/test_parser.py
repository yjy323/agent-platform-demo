"""
데이터 파싱 유틸리티 테스트 (리팩토링 버전)
"""

import pytest

from agent_discovery.parser import (
    build_service_definition,
    parse_capabilities_from_tags,
    parse_host_and_port,
    parse_list_from_tags,
    parse_meta,
    parse_tags,
)
from agents.common.types import (
    AgentAuthentication,
    AgentCard,
    AgentProvider,
    AgentSkill,
)


def test_parse_host_and_port():
    """URL 파싱 테스트"""
    host, port = parse_host_and_port("http://example.com")
    assert host == "example.com"
    assert port == 80

    host, port = parse_host_and_port("https://example.com")
    assert host == "example.com"
    assert port == 443

    host, port = parse_host_and_port("http://example.com:8080")
    assert host == "example.com"
    assert port == 8080

    host, port = parse_host_and_port("invalid-url")
    assert host == "localhost"
    assert port == 80


@pytest.fixture
def sample_agent_card():
    """테스트용 에이전트 카드 픽스처"""
    return AgentCard(
        name="test-agent",
        description="Test Agent",
        url="http://localhost:8000",
        provider=AgentProvider(organization="TestOrg", url="http://testorg.com"),
        version="1.0.0",
        documentationUrl="http://docs.testorg.com",
        capabilities={
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": True,
        },
        authentication=AgentAuthentication(schemes=["bearer", "basic"]),
        defaultInputModes=["text", "voice"],
        defaultOutputModes=["text"],
        skills=[AgentSkill(id="test-skill", name="Test Skill", tags=["test"])],
    )


def test_parse_tags(sample_agent_card):
    """태그 생성 테스트"""
    tags = parse_tags(sample_agent_card)

    # 기능 태그 검증
    capabilities = sample_agent_card.capabilities.model_dump()
    for key, value in capabilities.items():
        expected_tag = f"{key}={str(value).lower()}"
        assert expected_tag in tags, f"태그 '{expected_tag}'가 없습니다"

    # 입력 모드 태그 검증
    for mode in sample_agent_card.defaultInputModes:
        expected_tag = f"input={mode}"
        assert expected_tag in tags, f"태그 '{expected_tag}'가 없습니다"

    # 출력 모드 태그 검증
    for mode in sample_agent_card.defaultOutputModes:
        expected_tag = f"output={mode}"
        assert expected_tag in tags, f"태그 '{expected_tag}'가 없습니다"

    # 인증 태그 검증
    for scheme in sample_agent_card.authentication.schemes:
        expected_tag = f"auth={scheme}"
        assert expected_tag in tags, f"태그 '{expected_tag}'가 없습니다"

    # 메타데이터 태그 검증
    assert f"meta.description={sample_agent_card.description}" in tags
    assert f"meta.version={sample_agent_card.version}" in tags
    assert (
        f"meta.provider.organization={sample_agent_card.provider.organization}" in tags
    )
    assert f"meta.provider.url={sample_agent_card.provider.url}" in tags
    assert f"meta.documentationUrl={sample_agent_card.documentationUrl}" in tags


def test_parse_meta():
    """메타데이터 추출 테스트"""
    tags = [
        "meta.description=Test Agent",
        "meta.version=1.0.0",
        "meta.provider.organization=TestOrg",
        "meta.provider.url=http://testorg.com",
        "meta.documentationUrl=http://docs.testorg.com",
    ]
    meta = parse_meta(tags)
    assert meta["description"] == "Test Agent"
    assert meta["version"] == "1.0.0"
    assert meta["provider.organization"] == "TestOrg"
    assert meta["provider.url"] == "http://testorg.com"
    assert meta["documentationUrl"] == "http://docs.testorg.com"


def test_build_service_definition(sample_agent_card):
    """서비스 정의 생성 테스트"""
    service = build_service_definition(sample_agent_card)

    assert service["Name"] == sample_agent_card.name
    assert service["ID"] == f"{sample_agent_card.name}-{sample_agent_card.version}"
    assert service["Address"] == "localhost"
    assert service["Port"] == 8000

    assert isinstance(service["Tags"], list)
    assert "Check" in service
    assert "TTL" in service["Check"]


def test_parse_capabilities_from_tags():
    """기능 추출 테스트"""
    tags = ["streaming=true", "pushNotifications=false", "stateTransitionHistory=true"]
    capabilities = parse_capabilities_from_tags(tags)
    assert capabilities["streaming"] is True
    assert capabilities["pushNotifications"] is False
    assert capabilities["stateTransitionHistory"] is True


def test_parse_list_from_tags():
    """목록 추출 테스트"""
    tags = [
        "input=text",
        "input=voice",
        "output=text",
        "output=image",
        "auth=basic",
        "auth=oauth2",
    ]
    assert parse_list_from_tags(tags, "input=") == ["text", "voice"]
    assert parse_list_from_tags(tags, "output=") == ["text", "image"]
    assert parse_list_from_tags(tags, "auth=") == ["basic", "oauth2"]
