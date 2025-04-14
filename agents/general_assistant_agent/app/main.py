import os

from app.agent import GeneralAssistantAgent
from app.server import run_agent_app


def main() -> None:
    """
    GeneralAssistantAgent 서비스 시작
    """
    # 환경 변수 검증
    if not os.getenv("GOOGLE_API_KEY"):
        print("경고: GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

    # 에이전트 초기화
    agent = GeneralAssistantAgent()

    # 서비스 포트 설정 (환경 변수 또는 기본값)
    port = int(os.getenv("PORT", "8000"))

    # 서비스 시작
    print(f"GeneralAssistant 서비스 시작 (포트: {port})...")
    run_agent_app(agent, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
