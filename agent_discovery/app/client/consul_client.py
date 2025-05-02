"""
Consul 레지스트리 클라이언트 구현체

Consul HTTP API를 사용하여 에이전트를 등록하고 관리하는 클라이언트 구현
"""

import logging
from typing import List

import consul  # python-consul 라이브러리

from agent_discovery.client import DiscoveryClient
from agent_discovery.parser import (
    build_service_definition,
    parse_capabilities_from_tags,
    parse_list_from_tags,
    parse_meta,
)
from agents.common.types import AgentCard

logger = logging.getLogger(__name__)


class ConsulDiscoveryClient(DiscoveryClient):
    """
    Consul HTTP API를 사용한 DiscoveryClient 구현체.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8500):
        """
        Consul 클라이언트를 초기화합니다.

        Args:
            host: Consul 서버 호스트
            port: Consul 서버 포트
        """
        self._consul = consul.Consul(host=host, port=port)
        logger.debug(f"Initialized Consul client at {host}:{port}")

    def register(self, card: AgentCard) -> None:
        """
        에이전트를 Consul에 등록합니다.

        Args:
            card: 등록할 에이전트 카드
        """
        if not card:
            raise ValueError("Agent card cannot be None")
        if not card.name:
            raise ValueError("Agent name cannot be empty")

        payload = build_service_definition(card)
        # 서비스 등록
        self._consul.agent.service.register(
            name=payload["Name"],
            service_id=payload["ID"],
            address=payload["Address"],
            port=payload["Port"],
            tags=payload.get("Tags"),
        )
        # 헬스체크 등록
        check_id = f"check:{payload['ID']}"
        self._consul.agent.check.register(
            name=check_id,
            check_id=check_id,
            service_id=payload["ID"],
            ttl=payload["Check"]["TTL"],
        )
        logger.info(
            f"Registered agent '{card.name}' ({card.version}) with ID {payload['ID']}"
        )

    def deregister(self, agent_id: str) -> None:
        """
        에이전트를 Consul에서 제거합니다.

        Args:
            agent_id: 제거할 에이전트 ID
        """
        # 서비스 해제
        self._consul.agent.service.deregister(agent_id)
        # 헬스체크 해제
        check_id = f"check:{agent_id}"
        try:
            self._consul.agent.check.deregister(check_id)
        except Exception:
            logger.warning(f"Check {check_id} may not exist or already deregistered.")
        logger.info(f"Deregistered agent ID {agent_id}")

    def list_agents(self, only_healthy: bool = True) -> List[AgentCard]:
        """
        Consul에 등록된 에이전트 목록을 반환합니다.

        Args:
            only_healthy: 건강한 에이전트만 반환할지 여부

        Returns:
            등록된 에이전트 카드 목록
        """
        # 모든 서비스 조회
        services = self._consul.agent.services()
        cards: List[AgentCard] = []
        for service_id, service in services.items():
            meta = parse_meta(service.get("Tags", []))
            card = AgentCard(
                name=service.get("Service", ""),
                description=meta.get("description", ""),
                url=f"http://{service.get('Address')}:{service.get('Port')}",
                provider=(
                    {
                        "organization": meta.get("provider.organization", ""),
                        "url": meta.get("provider.url", ""),
                    }
                    if meta.get("provider.organization")
                    else None
                ),
                version=meta.get("version", ""),
                documentationUrl=meta.get("documentationUrl", ""),
                capabilities={
                    "streaming": parse_capabilities_from_tags(
                        service.get("Tags", [])
                    ).get("streaming", False),
                    "pushNotifications": parse_capabilities_from_tags(
                        service.get("Tags", [])
                    ).get("pushNotifications", False),
                    "stateTransitionHistory": parse_capabilities_from_tags(
                        service.get("Tags", [])
                    ).get("stateTransitionHistory", False),
                },
                authentication={
                    "schemes": parse_list_from_tags(service.get("Tags", []), "auth=")
                },
                defaultInputModes=parse_list_from_tags(
                    service.get("Tags", []), "input="
                ),
                defaultOutputModes=parse_list_from_tags(
                    service.get("Tags", []), "output="
                ),
                skills=[],
            )
            cards.append(card)
        logger.debug(f"Listed {len(cards)} agents (healthy={only_healthy})")
        return cards

    def update(self, card: AgentCard) -> None:
        """
        Consul에 등록된 에이전트 정보를 업데이트합니다.

        Args:
            card: 업데이트할 에이전트 카드
        """
        # Consul은 register 호출만으로 덮어쓰기가 가능
        self.register(card)
        logger.info(f"Updated agent '{card.name}' metadata")
