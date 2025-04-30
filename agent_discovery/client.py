"""
레지스트리 클라이언트 인터페이스

다양한 서비스 레지스트리 구현체에 대한 추상 인터페이스를 정의합니다.
"""

import logging
from abc import ABC, abstractmethod
from typing import List

from agents.common.types import AgentCard

logger = logging.getLogger(__name__)


class DiscoveryClient(ABC):
    """
    추상화된 Discovery 클라이언트 인터페이스.
    Consul, Etcd 등 다양한 구현체를 교체 가능하도록 정의.
    """

    @abstractmethod
    def register(self, card: AgentCard) -> None:
        """
        에이전트를 레지스트리에 등록합니다.

        Args:
            card: 등록할 에이전트 카드
        """
        pass

    @abstractmethod
    def deregister(self, agent_id: str) -> None:
        """
        에이전트를 레지스트리에서 제거합니다.

        Args:
            agent_id: 제거할 에이전트 ID
        """
        pass

    @abstractmethod
    def list_agents(self, only_healthy: bool = True) -> List[AgentCard]:
        """
        레지스트리에 등록된 에이전트 목록을 반환합니다.

        Args:
            only_healthy: 건강한 에이전트만 반환할지 여부

        Returns:
            등록된 에이전트 카드 목록
        """
        pass

    @abstractmethod
    def update(self, card: AgentCard) -> None:
        """
        레지스트리에 등록된 에이전트 정보를 업데이트합니다.

        Args:
            card: 업데이트할 에이전트 카드
        """
        pass
