import json
import os
from typing import List, Optional

from google import genai

from app.agents.base_agent import BaseAgent
from app.agents.broker import AgentBroker


class LLMOrchestrator:
    _instance = None

    def __new__(cls, agent_broker: AgentBroker = None):
        if cls._instance is None:
            if agent_broker is None:
                raise ValueError("AgentBroker instance must be provided")
            cls._instance = super().__new__(cls)
            cls._instance.model = "gemini-2.0-flash-001"
            cls._instance.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            cls._instance.agent_broker = agent_broker
        return cls._instance

    def select_agent(self, user_prompt: str) -> BaseAgent:
        """
        LLM이 제시한 Agent 설명을 바탕으로 사용자의 요청에 가장 적합한 Agent를 선택한다.
        """
        # 모든 Agent의 self-description 수집
        agent_list = self.agent_broker.list_agents()

        descriptions = ""
        for agent in agent_list:
            descriptions += f"Agent 이름: {agent['name']}\n"
            descriptions += f"설명: {agent['description']}\n"
            descriptions += f"능력: {', '.join(agent['skills'])}\n\n"

        selection_prompt = (
            "당신은 여러 에이전트 중 가장 적합한 에이전트를 선택하는 역할을 맡았습니다.\n"
            f'"""\n{user_prompt}\n"""\n\n'
            "아래는 현재 선택 가능한 에이전트 목록입니다:\n\n"
            f"{descriptions}\n"
            "이 중 어떤 에이전트가 이 요청을 처리하는 데 가장 적합한지, "
            "에이전트 이름만 한 줄로 출력해 주세요."
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=selection_prompt,
        )
        selected_name = response.text.strip()
        return selected_name

    def handle_request(self, user_prompt: str) -> Optional[str]:
        print("적합한 에이전트 선택 중...")
        agent_name = self.select_agent(user_prompt)
        return agent_name
        # return agent.execute_task(user_prompt)
