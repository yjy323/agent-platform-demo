import os
from typing import Dict, List, Optional

from google import genai


class BaseAgent:
    def __init__(
        self,
        name: str,
        description: str,
        skills: List[str],
        model: str = "gemini-2.0-flash-001",
    ) -> None:
        self.name = name
        self.description = description
        self.skills = skills
        self.model = model
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def self_describe(self) -> Dict[str, str | List[str]]:
        """에이전트의 자기 설명을 반환합니다.

        Returns:
            Dict[str, str | List[str]]: 에이전트의 이름, 설명, 스킬 정보
        """
        return {
            "name": self.name,
            "description": self.description,
            "skills": self.skills,
        }

    def execute_task(self, task_prompt: str) -> Optional[str]:
        """주어진 태스크를 실행합니다.

        Args:
            task_prompt: 실행할 태스크 프롬프트

        Returns:
            Optional[str]: 태스크 실행 결과 또는 None
        """
        print(self.name)
        response = self.client.models.generate_content(
            model=self.model,
            contents=task_prompt,
        )
        if response and hasattr(response, "text"):
            return str(response.text)
        return None
