import os

from google import genai

from app.agent_base import BaseAgent


class GeneralAssistantAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="GeneralAssistant",
            description=(
                "비전문 분야 전반에 걸친 일반 작업을 처리합니다. "
                "요약, 설명, 정보 검색, 창의적 콘텐츠 생성 등 "
                "세무 외의 광범위한 작업을 지원합니다."
            ),
            skills=[
                "텍스트 요약",
                "일반 상식 응답",
                "간단한 추론",
                "설명 생성",
                "창의적 글쓰기",
            ],
        )

    def run(self, prompt: str) -> str:
        """
        Google Gemini API를 사용하여 프롬프트에 응답합니다.

        Args:
            prompt: 사용자 입력 프롬프트

        Returns:
            str: Gemini API의 응답 텍스트
        """
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

            # Gemini API 클라이언트 초기화
            client = genai.Client(api_key=api_key)

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
            return f"죄송합니다. 요청을 처리하는 중 오류가 발생했습니다: {str(e)}"
