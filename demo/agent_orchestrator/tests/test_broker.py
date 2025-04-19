"""Orchestrator 테스트 모듈."""

import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from app.client import BrokerClient
from app.orchestrator import Orchestrator


class TestOrchestrator(unittest.TestCase):
    """Orchestrator 클래스 테스트 케이스."""

    def setUp(self) -> None:
        """테스트 설정."""
        # 브로커 클라이언트 Mock 설정
        self.mock_broker_client = MagicMock(spec=BrokerClient)
        self.mock_broker_client.list_agents = AsyncMock()
        self.mock_broker_client.get_agent = AsyncMock()

        # 테스트용 에이전트 데이터
        self.test_agents = [
            {
                "name": "DataAnalysisExpert",
                "endpoint": "http://data-analysis-agent:8080/run",
                "description": "데이터 분석 전문 에이전트",
                "skills": ["data interpretation", "statistical analysis"],
                "type": "llm",
                "registered_at": "2023-01-01T00:00:00",
            },
            {
                "name": "CreativeWriter",
                "endpoint": "http://creative-writer-agent:8080/run",
                "description": "창작 작가 에이전트",
                "skills": ["storytelling", "creative writing"],
                "type": "llm",
                "registered_at": "2023-01-01T00:00:00",
            },
        ]

        # 브로커 클라이언트 Mock 응답 설정
        self.mock_broker_client.list_agents.return_value = self.test_agents
        self.mock_broker_client.get_agent.return_value = self.test_agents[0]

        # 오케스트레이터 생성
        self.orchestrator = Orchestrator(broker_client=self.mock_broker_client)

    @patch("google.generativeai.GenerativeModel")
    async def test_select_agent(self, mock_gen_model) -> None:
        """에이전트 선택 테스트."""
        # 모델 Mock 설정
        mock_response = MagicMock()
        mock_response.text = json.dumps(
            {
                "selected_agent": "DataAnalysisExpert",
                "selection_reason": "데이터 분석 작업에 가장 적합합니다.",
            }
        )

        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_gen_model.return_value = mock_model_instance

        # 에이전트 선택 테스트
        result = await self.orchestrator.select_agent("분석해줘", {})

        # 검증
        self.assertEqual(result["selected_agent"], "DataAnalysisExpert")
        self.assertTrue("selection_reason" in result)
        self.mock_broker_client.list_agents.assert_called_once()

    @patch("app.client.AgentClient.execute_task")
    async def test_execute_task(self, mock_execute) -> None:
        """작업 실행 테스트."""
        # 에이전트 실행 Mock 설정
        mock_execute.return_value = "작업 결과입니다."

        # 에이전트 선택 Mock 설정
        self.orchestrator.select_agent = AsyncMock()
        self.orchestrator.select_agent.return_value = {
            "selected_agent": "DataAnalysisExpert",
            "selection_reason": "데이터 분석 작업에 가장 적합합니다.",
        }

        # 작업 실행 테스트
        result = await self.orchestrator.execute_task("분석해줘", {})

        # 검증
        self.assertEqual(result["selected_agent"], "DataAnalysisExpert")
        self.assertEqual(result["result"], "작업 결과입니다.")
        self.assertTrue("task_id" in result)
        self.assertTrue("execution_time" in result)

        self.mock_broker_client.get_agent.assert_called_once_with("DataAnalysisExpert")
        mock_execute.assert_called_once()

    @patch("app.client.AgentClient.execute_task")
    async def test_execute_with_agent(self, mock_execute) -> None:
        """특정 에이전트 작업 실행 테스트."""
        # 에이전트 실행 Mock 설정
        mock_execute.return_value = "작업 결과입니다."

        # 작업 실행 테스트
        result = await self.orchestrator.execute_with_agent(
            "DataAnalysisExpert", "분석해줘", {}
        )

        # 검증
        self.assertEqual(result["selected_agent"], "DataAnalysisExpert")
        self.assertEqual(result["result"], "작업 결과입니다.")
        self.assertTrue("task_id" in result)
        self.assertTrue("execution_time" in result)

        self.mock_broker_client.get_agent.assert_called_once_with("DataAnalysisExpert")
        mock_execute.assert_called_once()

    def test_extract_json(self) -> None:
        """JSON 추출 테스트."""
        # 테스트 데이터
        text = """
        여기 JSON이 있습니다:
        ```json
        {"key": "value", "number": 123}
        ```
        """

        # JSON 추출 테스트
        result = self.orchestrator._extract_json(text)

        # 검증
        self.assertEqual(result, {"key": "value", "number": 123})


if __name__ == "__main__":
    unittest.main()
