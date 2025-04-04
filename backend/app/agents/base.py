from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Agent(ABC):
    """
    Agent 추상 기본 클래스.
    모든 에이전트는 이 클래스를 상속받아 구현합니다.
    """
    
    def __init__(self, llm_service):
        """
        에이전트 초기화
        
        Args:
            llm_service: LLM 서비스 인스턴스
        """
        self.llm_service = llm_service
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        """
        에이전트 작업 처리 메서드
        
        Returns:
            Dict[str, Any]: 처리 결과
        """
        pass
