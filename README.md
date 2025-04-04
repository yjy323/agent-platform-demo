# 이메일 관리 에이전트 MVP

LLM 기반 이메일 관리 에이전트 프로토타입입니다. 이 시스템은 이메일을 분석하고, 요약하며, 텍스트 명령을 통해 관리할 수 있는 기능을 제공합니다.

## 기능

- 이메일 입력 및 관리
- 이메일 분석 및 요약
- 중요도 및 응답 필요성 평가
- 텍스트 명령을 통한 이메일 검색 및 필터링

## 기술 스택

- **프론트엔드**: Streamlit
- **백엔드**: FastAPI
- **LLM**: Mistral 7B (Ollama를 통해 로컬에서 실행)
- **기타**: LangChain, Docker

## 프로젝트 구조

```
email-agent-mvp/
├── backend/                  # 백엔드 서비스
│   ├── app/                  # FastAPI 애플리케이션
│   │   ├── main.py          # 메인 FastAPI 앱
│   │   ├── api/             # API 정의
│   │   ├── agents/          # 에이전트 모듈
│   │   └── services/        # 서비스 모듈
│   ├── Dockerfile           # 백엔드 Docker 설정
│   └── requirements.txt     # 백엔드 의존성
├── frontend/                 # 프론트엔드 서비스
│   ├── app.py               # Streamlit 앱
│   ├── Dockerfile           # 프론트엔드 Docker 설정
│   └── requirements.txt     # 프론트엔드 의존성
├── docker-compose.yml        # Docker Compose 설정
└── README.md                 # 프로젝트 문서
```

## 실행 방법

### Docker Compose 사용 (권장)

1. 이 저장소를 클론합니다:
```bash
git clone https://github.com/yourusername/email-agent-mvp.git
cd email-agent-mvp
```

2. Docker Compose로 애플리케이션을 실행합니다:
```bash
docker-compose up -d
```

3. 웹 브라우저에서 `http://localhost:8501`로 접속하여 애플리케이션을 사용합니다.

### Ollama와 함께 실행 (선택 사항)

더 강력한 LLM 기능을 사용하려면 로컬에 Ollama를 설치하고 Mistral 모델을 다운로드할 수 있습니다:

1. [Ollama 설치](https://ollama.ai/download)

2. Mistral 모델 다운로드:
```bash
ollama pull mistral
```

3. Docker Compose 파일에서 환경 변수를 수정합니다:
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - LLM_DUMMY_MODE=false  # true에서 false로 변경
    # ...
    # Ollama와 통신하기 위해 호스트 네트워크 추가
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

4. 서비스를 재시작합니다:
```bash
docker-compose down
docker-compose up -d
```

## 개발 환경 설정

로컬에서 개발하려면 다음 단계를 따릅니다:

1. 백엔드 설정:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd app
uvicorn main:app --reload
```

2. 프론트엔드 설정:
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 참고사항

- 이 프로토타입은 데모 목적으로 개발되었으며, 실제 이메일 시스템과 연동되지 않습니다.
- Ollama가 설치되지 않은 환경에서는 더미 LLM 모드로 작동합니다.
- 모든 데이터는 세션 내에서만 유지되며, 영구 저장되지 않습니다.
