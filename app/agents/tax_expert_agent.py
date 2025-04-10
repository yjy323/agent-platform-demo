from app.agents.base_agent import BaseAgent


class TaxExpertAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="TaxExpert",
            description=(
                "한국 세법에 정통하며, 세금 관련 법률 해석, 공제 항목 안내, "
                "부동산 세금 상담 등을 전문으로 합니다."
            ),
            skills=[
                "세법 해석",
                "공제 계산",
                "부동산 세금 분석",
                "사업자 등록 상담",
            ],
        )
