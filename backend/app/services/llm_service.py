import logging
from typing import Optional, Dict, Any
from langchain_community.llms import Ollama

logger = logging.getLogger(__name__)

class LLMService:
    """
    LLM 서비스 클래스.
    다양한 LLM 모델과의 통신을 추상화합니다.
    """
    
    def __init__(self, model_name: str = "mistral"):
        """
        LLM 서비스 초기화
        
        Args:
            model_name: 사용할 LLM 모델 이름
        """
        self.model_name = model_name
        self._llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """LLM 모델 초기화"""
        try:
            self._llm = Ollama(model=self.model_name)
            logger.info(f"{self.model_name} 모델 초기화 성공")
        except Exception as e:
            logger.error(f"LLM 초기화 오류: {e}")
            logger.warning("더미 LLM 모드로 실행됩니다.")
            self._llm = self._create_dummy_llm()
    
    def _create_dummy_llm(self):
        """더미 LLM 생성 (실제 LLM 사용 불가 시)"""
        class DummyLLM:
            def __call__(self, prompt):
                prompt_length = len(prompt)
                return f"[더미 LLM 응답] 입력된 프롬프트는 {prompt_length}자입니다. 실제 LLM을 설치해 주세요."
        
        return DummyLLM()
    
    async def generate(self, prompt: str) -> str:
        """
        LLM을 사용해 텍스트 생성
        
        Args:
            prompt: 입력 프롬프트
            
        Returns:
            str: 생성된 텍스트
        """
        try:
            return self._llm(prompt)
        except Exception as e:
            logger.error(f"LLM 생성 오류: {e}")
            return f"오류 발생: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        현재 LLM 모델 정보 반환
        
        Returns:
            Dict[str, Any]: 모델 정보
        """
        return {
            "model_name": self.model_name,
            "is_dummy": isinstance(self._llm, object) and self._llm.__class__.__name__ == "DummyLLM"
        }
