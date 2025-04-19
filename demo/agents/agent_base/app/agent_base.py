from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseAgent(ABC):
    def __init__(self, name: str, description: str, skills: List[str]):
        """
        BaseAgent 생성자

        Args:
            name: 에이전트 이름
            description: 역할 설명
            skills: 에이전트가 가진 기술 목록
        """
        self.name = name
        self.description = description
        self.skills = skills

    def describe(self) -> dict:
        """
        에이전트의 self-description을 반환합니다.

        Returns:
            dict: 에이전트 메타데이터를 포함하는 딕셔너리
        """
        return {
            "name": self.name,
            "description": self.description,
            "skills": self.skills,
        }

    @abstractmethod
    def run(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        사용자 프롬프트를 받아 처리 결과를 문자열로 반환합니다.

        Args:
            prompt: 사용자 입력 프롬프트

        Returns:
            str: LLM으로부터의 응답 텍스트
        """
        pass
