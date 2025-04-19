import os
from typing import Any, Dict, Optional

from app.agent_base import BaseAgent
from google import genai


class TaxExpertAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="TaxExpert",
            description=(
                "한국 세법 전문가. 세금 관련 법률 해석, 공제 항목 안내, "
                "부동산 세금 상담 등을 전문으로 합니다."
            ),
            skills=[
                "세법 해석",
                "공제 계산",
                "부동산 세금 분석",
                "사업자 등록 상담",
            ],
        )

    def run(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Google Gemini API를 사용하여 세금 관련 프롬프트에 응답합니다.

        Args:
            prompt: 사용자 입력 프롬프트
            context: 추가 컨텍스트 정보 (선택 사항)

        Returns:
            str: Gemini API의 응답 텍스트
        """
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

            # Gemini API 클라이언트 초기화
            client = genai.Client(api_key=api_key)

            # 세법 전문가로서의 역할을 명시하는 시스템 프롬프트
            system_prompt = (
                "당신은 한국 세법 전문가입니다. "
                "다음 질문에 대해 한국 세법에 기반하여 정확하고 전문적인 답변을 제공해주세요. "
                "가능한 경우 관련 법조문을 인용하고, 구체적인 계산 예시를 들어 설명해주세요."
            )

            # Gemini 모델에 요청 전송
            response = client.models.generate_content(
                model="gemini-1.5-flash-001",
                contents=prompt,
            )

            # 응답 반환
            if response and hasattr(response, "text"):
                return str(response.text)
            else:
                return "응답을 생성할 수 없습니다."

        except Exception as e:
            # 에러 로깅 및 사용자 친화적 메시지 반환
            error_message = f"에러 발생: {str(e)}"
            print(error_message)  # 로그로 기록
            return f"죄송합니다. 세금 관련 상담을 처리하는 중 오류가 발생했습니다: {str(e)}"
