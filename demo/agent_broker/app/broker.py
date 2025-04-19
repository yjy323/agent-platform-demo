"""Agent Broker 서비스 모듈.

에이전트 등록 및 관리를 위한 핵심 클래스를 제공합니다.
"""

from datetime import datetime
from typing import Any, Dict, List


class AgentBroker:
    """Agent Broker 클래스.

    에이전트 등록 및 관리를 위한 싱글톤 클래스입니다.
    현재는 인메모리 방식으로 구현되어 있습니다.
    """

    _instance = None

    def __new__(cls) -> "AgentBroker":
        """싱글톤 인스턴스 생성.

        Returns:
            AgentBroker: 싱글톤 인스턴스
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.agents = {}  # 타입 선언 제거, __init__에서 설정
        return cls._instance

    def __init__(self) -> None:
        """인스턴스 초기화."""
        # 초기화 코드를 __new__에서 __init__으로 이동
        # agents가 초기화되지 않았을 때만 초기화
        if not hasattr(self, "agents"):
            self.agents: Dict[str, Dict[str, Any]] = {}

    def register(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """새로운 에이전트 등록.

        Args:
            agent_data: 에이전트 정보를 담은 딕셔너리

        Returns:
            Dict[str, Any]: 등록된 에이전트 정보

        Raises:
            ValueError: 동일한 이름의 에이전트가 이미 존재할 경우
        """
        name = agent_data["name"]
        if name in self.agents:
            raise ValueError(f"Agent '{name}' already exists.")

        agent_info = {
            "name": name,
            "endpoint": agent_data["endpoint"],
            "description": agent_data["description"],
            "skills": agent_data["skills"],
            "registered_at": datetime.now().isoformat(),
        }

        self.agents[name] = agent_info
        return agent_info

    def get_agent(self, name: str) -> Dict[str, Any]:
        """이름으로 특정 에이전트 정보 조회.

        Args:
            name: 에이전트 이름

        Returns:
            Dict[str, Any]: 에이전트 정보

        Raises:
            ValueError: 해당 이름의 에이전트가 존재하지 않을 경우
        """
        if name not in self.agents:
            raise ValueError(f"Agent '{name}' not found.")
        return self.agents[name]

    def list_agents(self) -> List[Dict[str, Any]]:
        """등록된 모든 에이전트 목록 반환.

        Returns:
            List[Dict[str, Any]]: 에이전트 정보 목록
        """
        return list(self.agents.values())

    def update_agent(self, name: str, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """기존 에이전트 정보 업데이트.

        Args:
            name: 에이전트 이름
            agent_data: 업데이트할 에이전트 정보

        Returns:
            Dict[str, Any]: 업데이트된 에이전트 정보

        Raises:
            ValueError: 해당 이름의 에이전트가 존재하지 않을 경우
        """
        if name not in self.agents:
            raise ValueError(f"Agent '{name}' not found.")

        # 기존 정보 유지하되 업데이트된 필드만 변경
        agent_info = self.agents[name]

        if "endpoint" in agent_data:
            agent_info["endpoint"] = agent_data["endpoint"]
        if "description" in agent_data:
            agent_info["description"] = agent_data["description"]
        if "skills" in agent_data:
            agent_info["skills"] = agent_data["skills"]

        self.agents[name] = agent_info
        return agent_info

    def delete_agent(self, name: str) -> bool:
        """에이전트 등록 해제.

        Args:
            name: 에이전트 이름

        Returns:
            bool: 삭제 성공 여부

        Raises:
            ValueError: 해당 이름의 에이전트가 존재하지 않을 경우
        """
        if name not in self.agents:
            raise ValueError(f"Agent '{name}' not found.")

        del self.agents[name]
        return True


# 싱글톤 인스턴스
broker_instance = AgentBroker()


def get_broker() -> AgentBroker:
    """AgentBroker 싱글톤 인스턴스 반환.

    FastAPI의 의존성 주입용 함수입니다.

    Returns:
        AgentBroker: 싱글톤 인스턴스
    """
    return broker_instance
