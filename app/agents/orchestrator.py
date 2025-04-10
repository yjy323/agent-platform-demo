import os
from typing import List, Optional

from google import genai

from app.agents.base_agent import BaseAgent


class LLMOrchestrator:
    def __init__(
        self,
        agents: List[BaseAgent],
        model: str = "gemini-2.0-flash-001",
    ) -> None:
        self.agents = agents
        self.model = model
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def step1_understand_task(self, user_prompt: str) -> str:
        """Step 1: 프롬프트의 주제를 LLM에게 물어봄."""
        prompt = (
            "당신은 사용자의 요청을 분석하는 분석가입니다.\n"
            "다음 요청이 어떤 주제(분야)에 해당하는지 하나의 단어로 요약해 주세요.\n\n"
            "예: 세금, 법률, 과학, 부동산, 건강, 일반지식, 기술 등\n\n"
            f'사용자 요청:\n"""\n{user_prompt}\n"""\n\n'
            "분야:"
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return str(response.text).strip()

    def step2_select_agent(self, topic: str, user_prompt: str) -> BaseAgent:
        """Step 2: LLM에게 어떤 Agent가 가장 적절한지 선택하게 함."""
        # 모든 Agent의 self-description 수집
        descriptions = "\n".join(
            [
                f"Agent 이름: {agent.name}\n"
                f"설명: {agent.description}\n"
                f"능력: {', '.join(agent.skills)}\n"
                for agent in self.agents
            ]
        )

        selection_prompt = (
            "당신은 여러 에이전트 중 가장 적합한 에이전트를 선택하는 역할을 맡았습니다.\n"
            f'사용자의 요청 주제는 "{topic}" 입니다.\n'
            "다음은 사용자의 실제 요청입니다:\n"
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

        # 이름 매칭으로 Agent 반환
        for agent in self.agents:
            if agent.name.lower() == selected_name.lower():
                return agent

        # fallback
        return self.agents[0]

    def handle_request(self, user_prompt: str) -> Optional[str]:
        """전체 흐름 실행: 체이닝 방식으로 Step 1 → Step 2 → 결과 반환"""
        print("[🔎 Step 1] 유저 요청 주제 파악 중...")
        topic = self.step1_understand_task(user_prompt)
        print(f"→ 주제: {topic}")

        print("[🤖 Step 2] 적합한 에이전트 선택 중...")
        agent = self.step2_select_agent(topic, user_prompt)
        print(f"→ 선택된 에이전트: {agent.name}")

        return agent.execute_task(user_prompt)
