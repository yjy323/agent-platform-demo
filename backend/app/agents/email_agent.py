import re
from typing import Dict, Any
import logging
from .base import Agent

logger = logging.getLogger(__name__)

class EmailAgent(Agent):
    """
    이메일 분석 에이전트 클래스.
    이메일 분석, 요약, 중요도 평가 등의 작업을 수행합니다.
    """
    
    async def process(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        이메일 분석 처리
        
        Args:
            email: 분석할 이메일 데이터
            
        Returns:
            Dict[str, Any]: 분석 결과
        """
        logger.info(f"이메일 분석 시작: {email['subject']}")
        
        # 프롬프트 생성
        prompt = self._create_analysis_prompt(email)
        
        # LLM으로 분석 수행
        response = await self.llm_service.generate(prompt)
        
        # 결과 파싱
        analysis_result = self._parse_analysis_result(response)
        
        logger.info(f"이메일 분석 완료: {email['subject']}")
        return analysis_result
    
    def _create_analysis_prompt(self, email: Dict[str, Any]) -> str:
        """
        이메일 분석을 위한 프롬프트 생성
        
        Args:
            email: 이메일 데이터
            
        Returns:
            str: 분석 프롬프트
        """
        return f"""
        다음 이메일을 분석해주세요:
        
        제목: {email['subject']}
        보낸 사람: {email['sender']}
        날짜: {email['date']}
        내용: {email['content']}
        
        다음 형식으로 분석 결과를 제공해 주세요:
        
        중요도: (상/중/하)
        응답 필요성: (필요/선택적/불필요)
        요약: (3-5문장으로 요약)
        제안된 조치: (있는 경우에만)
        """
    
    def _parse_analysis_result(self, response: str) -> Dict[str, Any]:
        """
        LLM 응답에서 분석 결과 파싱
        
        Args:
            response: LLM 응답 텍스트
            
        Returns:
            Dict[str, Any]: 구조화된 분석 결과
        """
        result = {
            "importance": "중",
            "needs_response": "선택적",
            "summary": response,
            "suggested_action": None
        }
        
        # 정규식으로 결과 파싱 시도
        importance_match = re.search(r"중요도:\s*(\w+)", response)
        if importance_match:
            result["importance"] = importance_match.group(1)
            
        response_match = re.search(r"응답 필요성:\s*(\w+)", response)
        if response_match:
            result["needs_response"] = response_match.group(1)
            
        summary_match = re.search(r"요약:(.*?)(?=제안된 조치:|$)", response, re.DOTALL)
        if summary_match:
            result["summary"] = summary_match.group(1).strip()
            
        action_match = re.search(r"제안된 조치:(.*?)$", response, re.DOTALL)
        if action_match:
            result["suggested_action"] = action_match.group(1).strip()
        
        return result
