"""
파서 유틸리티
"""

from typing import Dict, List
from urllib.parse import urlparse

from agents.common.types import AgentCard


def parse_host_and_port(url: str) -> tuple[str, int]:
    """
    URL에서 호스트와 포트를 추출합니다.

    Args:
        url: URL 문자열

    Returns:
        (호스트, 포트) 튜플
    """
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return host, port


def parse_tags(card: AgentCard) -> List[str]:
    """
    에이전트 카드에서 태그 목록을 생성합니다.

    Args:
        card: 에이전트 카드

    Returns:
        태그 목록
    """
    tags = []

    # 기능 태그
    capabilities = card.capabilities.model_dump()
    for key, value in capabilities.items():
        tags.append(f"{key}={str(value).lower()}")

    # 입출력 모드 태그
    for mode in card.defaultInputModes:
        tags.append(f"input={mode}")
    for mode in card.defaultOutputModes:
        tags.append(f"output={mode}")

    # 인증 태그
    if card.authentication and card.authentication.schemes:
        for scheme in card.authentication.schemes:
            tags.append(f"auth={scheme}")

    # 메타데이터 태그
    tags.append(f"meta.description={card.description}")
    tags.append(f"meta.version={card.version}")
    if card.provider:
        tags.append(f"meta.provider.organization={card.provider.organization}")
        if card.provider.url:
            tags.append(f"meta.provider.url={card.provider.url}")
    if card.documentationUrl:
        tags.append(f"meta.documentationUrl={card.documentationUrl}")

    return tags


def parse_meta(tags: List[str]) -> Dict[str, str]:
    """
    태그 목록에서 메타데이터를 추출합니다.

    Args:
        tags: 태그 목록

    Returns:
        메타데이터 사전
    """
    meta = {}
    for tag in tags:
        if tag.startswith("meta."):
            key = tag[5:]  # "meta." 제거
            if "=" in key:
                key, value = key.split("=", 1)
                meta[key] = value
    return meta


def build_service_definition(card: AgentCard) -> Dict:
    """
    에이전트 카드에서 서비스 정의를 생성합니다.

    Args:
        card: 에이전트 카드

    Returns:
        서비스 정의 사전
    """
    host, port = parse_host_and_port(card.url)
    service_id = f"{card.name}-{card.version}"

    return {
        "Name": card.name,
        "ID": service_id,
        "Address": host,
        "Port": port,
        "Tags": parse_tags(card),
        "Check": {"TTL": "10s"},
    }


def parse_capabilities_from_tags(tags: List[str]) -> Dict[str, bool]:
    """
    태그 목록에서 기능을 추출합니다.

    Args:
        tags: 태그 목록

    Returns:
        기능 사전
    """
    capabilities = {}
    for tag in tags:
        if "=" in tag:
            key, value = tag.split("=", 1)
            if key in ("streaming", "pushNotifications", "stateTransitionHistory"):
                capabilities[key] = value.lower() == "true"
    return capabilities


def parse_list_from_tags(tags: List[str], prefix: str) -> List[str]:
    """
    태그 목록에서 특정 접두사를 가진 값들을 추출합니다.

    Args:
        tags: 태그 목록
        prefix: 태그 접두사

    Returns:
        값 목록
    """
    values = []
    for tag in tags:
        if tag.startswith(prefix):
            value = tag[len(prefix) :]
            values.append(value)
    return values
