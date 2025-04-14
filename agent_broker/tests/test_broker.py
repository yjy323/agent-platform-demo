"""
Agent Broker 테스트 모듈
"""

import unittest
from typing import Any, Dict, cast

from app.broker import AgentBroker


class TestAgentBroker(unittest.TestCase):
    """AgentBroker 클래스 테스트 케이스"""

    def setUp(self) -> None:
        """테스트 설정"""
        self.broker = AgentBroker()
        # 테스트를 위해 에이전트 저장소 초기화
        self.broker.agents = {}

        # 테스트용 에이전트 데이터
        self.test_agent: Dict[str, Any] = {
            "name": "TestAgent",
            "endpoint": "http://test-agent:8080/run",
            "description": "테스트용 에이전트",
            "skills": ["testing", "debugging"],
            "type": "test",
        }

    def test_register_agent(self) -> None:
        """에이전트 등록 테스트"""
        result = self.broker.register(self.test_agent)

        # 반환값 확인
        self.assertEqual(result["name"], self.test_agent["name"])
        self.assertEqual(result["endpoint"], self.test_agent["endpoint"])
        self.assertEqual(result["description"], self.test_agent["description"])
        self.assertEqual(result["skills"], self.test_agent["skills"])
        self.assertEqual(result["type"], self.test_agent["type"])
        self.assertIn("registered_at", result)

        # 저장소에 추가되었는지 확인
        self.assertIn(cast(str, self.test_agent["name"]), self.broker.agents)

        # 중복 등록 예외 발생 확인
        with self.assertRaises(ValueError):
            self.broker.register(self.test_agent)

    def test_get_agent(self) -> None:
        """에이전트 조회 테스트"""
        # 먼저 에이전트 등록
        self.broker.register(self.test_agent)

        # 존재하는 에이전트 조회
        result = self.broker.get_agent(cast(str, self.test_agent["name"]))
        self.assertEqual(result["name"], self.test_agent["name"])

        # 존재하지 않는 에이전트 조회 시 예외 발생 확인
        with self.assertRaises(ValueError):
            self.broker.get_agent("NonExistentAgent")

    def test_list_agents(self) -> None:
        """에이전트 목록 조회 테스트"""
        # 초기 상태 확인 (빈 목록)
        self.assertEqual(len(self.broker.list_agents()), 0)

        # 에이전트 등록
        self.broker.register(self.test_agent)

        # 등록 후 목록 확인
        agent_list = self.broker.list_agents()
        self.assertEqual(len(agent_list), 1)
        self.assertEqual(agent_list[0]["name"], self.test_agent["name"])

    def test_update_agent(self) -> None:
        """에이전트 업데이트 테스트"""
        # 먼저 에이전트 등록
        self.broker.register(self.test_agent)

        # 업데이트 데이터
        update_data = {
            "description": "업데이트된 설명",
            "skills": ["testing", "debugging", "monitoring"],
        }

        # 업데이트 실행
        result = self.broker.update_agent(
            cast(str, self.test_agent["name"]), update_data
        )

        # 업데이트된 필드 확인
        self.assertEqual(result["description"], update_data["description"])
        self.assertEqual(result["skills"], update_data["skills"])

        # 업데이트되지 않은 필드 원래 값 유지 확인
        self.assertEqual(result["endpoint"], self.test_agent["endpoint"])
        self.assertEqual(result["type"], self.test_agent["type"])

        # 존재하지 않는 에이전트 업데이트 시 예외 발생 확인
        with self.assertRaises(ValueError):
            self.broker.update_agent("NonExistentAgent", update_data)

    def test_delete_agent(self) -> None:
        """에이전트 삭제 테스트"""
        # 먼저 에이전트 등록
        self.broker.register(self.test_agent)

        # 삭제 실행
        result = self.broker.delete_agent(cast(str, self.test_agent["name"]))

        # 삭제 결과 확인
        self.assertTrue(result)

        # 저장소에서 제거되었는지 확인
        self.assertNotIn(cast(str, self.test_agent["name"]), self.broker.agents)

        # 존재하지 않는 에이전트 삭제 시 예외 발생 확인
        with self.assertRaises(ValueError):
            self.broker.delete_agent(cast(str, self.test_agent["name"]))


if __name__ == "__main__":
    unittest.main()
