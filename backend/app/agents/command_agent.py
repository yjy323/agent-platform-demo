import logging
from typing import Dict, Any, List
from .base import Agent

logger = logging.getLogger(__name__)

class CommandAgent(Agent):
    """
    명령 처리 에이전트 클래스.
    사용자의 자연어 명령을 해석하고 이메일 필터링 등의 작업을 수행합니다.
    """
    
    async def process(self, command: str, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        명령 처리 실행
        
        Args:
            command: 사용자 명령 텍스트
            emails: 이메일 목록
            
        Returns:
            Dict[str, Any]: 처리 결과
        """
        logger.info(f"명령 처리 시작: {command}")
        
        # 프롬프트 생성
        prompt = self._create_command_prompt(command, emails)
        
        # LLM으로 명령 해석
        response = await self.llm_service.generate(prompt)
        
        # 키워드 기반 필터링 (간단한 구현)
        result = self._filter_emails_by_keywords(command, emails)
        
        # 결과에 LLM 응답 추가
        result["llm_response"] = response
        
        logger.info(f"명령 처리 완료: {command}")
        return result
    
    def _create_command_prompt(self, command: str, emails: List[Dict[str, Any]]) -> str:
        """
        명령 해석을 위한 프롬프트 생성
        
        Args:
            command: 사용자 명령
            emails: 이메일 목록
            
        Returns:
            str: 명령 해석 프롬프트
        """
        email_samples = str([{
            "sender": e["sender"],
            "subject": e["subject"],
            "date": e["date"],
            "important": e.get("important", False)
        } for e in emails[:3]])
        
        return f"""
        다음 명령을 해석하고 이메일 목록에서 해당하는 이메일을 찾아주세요:
        
        명령: "{command}"
        
        총 이메일 수: {len(emails)}
        첫 3개 이메일 샘플:
        {email_samples}
        
        이 명령에 대한 적절한 응답과 필터링 조건을 알려주세요.
        """
    
    def _filter_emails_by_keywords(self, command: str, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        키워드 기반 이메일 필터링 (간단한 구현)
        
        Args:
            command: 사용자 명령
            emails: 이메일 목록
            
        Returns:
            Dict[str, Any]: 필터링 결과
        """
        command = command.lower()
        filtered_emails = []
        message = "검색 결과입니다."
        
        # 간단한 키워드 기반 필터링
        if "중요" in command:
            message = "중요한 이메일을 찾았습니다."
            filtered_emails = [e for e in emails if e.get("important", False)]
        elif "모든" in command or "전체" in command:
            message = "모든 이메일을 표시합니다."
            filtered_emails = emails
        else:
            # 발신자 이름 검색
            sender_match = False
            for email in emails:
                if email["sender"].lower() in command:
                    filtered_emails.append(email)
                    sender_match = True
            
            if sender_match:
                message = f"{filtered_emails[0]['sender']}의 이메일을 찾았습니다."
            else:
                # 제목 검색
                for email in emails:
                    if any(word in email["subject"].lower() for word in command.split()):
                        filtered_emails.append(email)
        
        if not filtered_emails:
            message = "해당하는 이메일을 찾지 못했습니다."
            
        return {
            "message": message,
            "filtered_emails": filtered_emails
        }
