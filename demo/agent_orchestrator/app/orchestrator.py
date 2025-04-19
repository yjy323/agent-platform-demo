"""오케스트레이터 모듈.

사용자 요청 분석 및 적절한 에이전트 선택/실행을 담당합니다.
"""

import json
import logging
import os
import re
import time
import uuid
from typing import Any, Dict, List, Optional

from app.config import GOOGLE_API_KEY, LLM_MODEL
from google import genai

logger = logging.getLogger(__name__)


import httpx  # 추가 필요


class Orchestrator:
    def __init__(self, model: str = LLM_MODEL):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model = model
        self.broker_url = os.getenv("BROKER_BASE_URL", "http://agent-broker:8000")

    async def _get_agents(self) -> List[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                print(f"{self.broker_url}/agents")
                response = await client.get(f"{self.broker_url}/agents")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get agents from broker: {str(e)}")
            raise

    async def _get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.broker_url}/agents/{agent_name}")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get agent info: {str(e)}")
            raise

    async def _select_agent(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """사용자 프롬프트에 가장 적합한 에이전트를 선택합니다.

        Args:
            prompt: 사용자 입력 프롬프트
            context: 추가 컨텍스트 정보 (선택 사항)

        Returns:
            Dict[str, str]: 선택된 에이전트 정보 및 선택 이유

        Raises:
            Exception: 에이전트 선택 실패 시 발생
        """
        # 에이전트 목록 조회
        agents = await self._get_agents()
        if not agents:
            raise Exception("No agents available for selection")

        # 에이전트 메타데이터 포맷팅
        agent_descriptions = ""
        for agent in agents:
            agent_descriptions += f"Agent 이름: {agent['name']}\n"
            agent_descriptions += f"설명: {agent['description']}\n"
            agent_descriptions += f"능력: {', '.join(agent['skills'])}\n\n"

        # 선택 프롬프트 구성
        selection_prompt = (
            "당신은 여러 에이전트 중 가장 적합한 에이전트를 선택하는 역할을 맡았습니다.\n"
            f'"""\n{prompt}\n"""\n\n'
            "아래는 현재 선택 가능한 에이전트 목록입니다:\n\n"
            f"{agent_descriptions}\n"
            "질문을 처리하기에 가장 적합한 에이전트를 선택하고, 그 이유를 설명해주세요.\n"
            "다음 JSON 형식으로 응답해 주세요:\n"
            "```json\n"
            "{\n"
            '  "selected_agent": "에이전트 이름",\n'
            '  "selection_reason": "선택한 이유에 대한 설명"\n'
            "}\n"
            "```"
        )

        try:
            # Gemini 모델로 에이전트 선택
            response = self.client.models.generate_content(
                model=self.model,
                contents=selection_prompt,
            )

            # JSON 추출
            json_output = self._extract_json(response.text)

            if not json_output or "selected_agent" not in json_output:
                raise ValueError("Invalid selection result from LLM")

            # 선택된 에이전트가 존재하는지 확인
            selected_name = json_output["selected_agent"]
            if not any(agent["name"] == selected_name for agent in agents):
                raise ValueError(f"Selected agent '{selected_name}' does not exist")

            return json_output

        except Exception as e:
            logger.error(f"Agent selection failed: {str(e)}")
            # 실패 시 첫 번째 에이전트를 기본값으로 선택
            return {
                "selected_agent": agents[0]["name"],
                "selection_reason": f"Default selection due to error: {str(e)}",
            }

    async def execute_task(
        self, prompt: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """사용자 요청을 분석하고 적절한 에이전트를 선택하여
        작업을 실행합니다.

        Args:
            prompt: 사용자 입력 프롬프트
            context: 작업 컨텍스트 (선택 사항)

        Returns:
            Dict[str, Any]: 작업 실행 결과

        Raises:
            Exception: 작업 실행 실패 시 발생
        """
        # 작업 ID 생성
        task_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            # 에이전트 선택
            selection_result = await self._select_agent(prompt, context)
            selected_agent_name = selection_result["selected_agent"]

            # 선택된 에이전트 정보 조회
            agent_info = await self._get_agent_info(selected_agent_name)
            try:
                async with httpx.AsyncClient() as client:
                    logger.info(f"Calling agent: {agent_info['endpoint']}")
                    logger.info(f"Prompt: {prompt}")
                    response = await client.post(
                        agent_info["endpoint"],
                        json={"prompt": prompt, "context": context},
                    )
                    response.raise_for_status()
            except Exception as e:
                logger.error(f"Failed to get agents from broker: {str(e)}")
                raise

            execution_time = time.time() - start_time

            # 결과 반환
            return {
                "task_id": task_id,
                "selected_agent": selected_agent_name,
                "result": self._extract_json(response.text),
                "execution_time": execution_time,
            }

        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            raise

    @staticmethod
    def _extract_json(text: str) -> Dict[str, Any]:
        """텍스트에서 JSON을 추출합니다.

        Args:
            text: JSON을 포함하는 텍스트

        Returns:
            Dict[str, Any]: 추출된 JSON 객체
        """
        pattern = r"```json\s*([\s\S]*?)\s*```|{[\s\S]*?}"
        match = re.search(pattern, text)
        if match:
            json_str = match.group(1) if match.group(1) else match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON: {json_str}")
                return {}
        return {}


# 오케스트레이터 인스턴스 생성
orchestrator_instance = Orchestrator()


def get_orchestrator() -> Orchestrator:
    """Orchestrator 인스턴스 반환.

    FastAPI의 의존성 주입용 함수입니다.

    Returns:
        Orchestrator: 오케스트레이터 인스턴스
    """
    return orchestrator_instance
