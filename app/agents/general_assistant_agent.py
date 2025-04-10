from app.agents.base_agent import BaseAgent


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
