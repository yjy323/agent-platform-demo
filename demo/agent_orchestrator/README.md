# Agent Orchestrator Service

Agent Orchestrator 서비스는 사용자 요청을 분석하고 적절한 에이전트를 선택하여 작업을 실행하는 마이크로서비스입니다.

## 기능

- 사용자 요청 분석 및 적합한 에이전트 자동 선택
- 선택된 에이전트에 작업 실행 위임
- 특정 에이전트에 직접 작업 할당
- 사용 가능한 에이전트 목록 조회

## 아키텍처

Orchestrator 서비스는 다음과 같은 마이크로서비스 아키텍처로 구성되어 있습니다:

1. **Orchestrator 서비스**: 사용자 요청 분석 및 에이전트 선택
2. **Agent Broker 서비스**: 에이전트 등록 및 관리
3. **Agent 서비스들**: 전문화된 작업 실행

## 디렉토리 구조

```
orchestrator-service/
├── app/
│   ├── __init__.py        # 패키지 정의
│   ├── main.py            # FastAPI 애플리케이션 진입점
│   ├── orchestrator.py    # 오케스트레이터 핵심 로직
│   ├── client.py          # HTTP 클라이언트 (Broker, Agent 호출)
│   ├── schemas.py         # Pydantic 모델 (요청/응답 스키마)
│   ├── routes.py          # API 라우트 및 핸들러
│   └── config.py          # 애플리케이션 설정
│
├── tests/
│   └── test_orchestrator.py  # 단위 테스트
│
├── Dockerfile               # 컨테이너 이미지 정의
├── docker-compose.yml       # 개발 환경 컨테이너 구성
├── requirements.txt         # 의존성 패키지
└── README.md                # 프로젝트 문서
```

## 설치 및 실행

### 필수 요구사항

- Python 3.9+
- Docker 및 Docker Compose (선택 사항)

### 환경 변수 설정

```bash
# Gemini API 키 설정
export GEMINI_API_KEY=your-gemini-api-key

# 브로커 서비스 URL 설정 (선택 사항)
export BROKER_BASE_URL=http://localhost:8000
```

### 로컬 환경

```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
uvicorn app.main:app --reload --port 8000
```

### Docker 환경

```bash
# 이미지 빌드
docker build -t agent-orchestrator .

# 컨테이너 실행
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  -e BROKER_BASE_URL=http://host.docker.internal:8001 \
  agent-orchestrator-service
```

### Docker Compose

```bash
# 모든 서비스 실행 (Broker + Orchestrator)
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

## API 엔드포인트

### 작업 관련 엔드포인트

- `POST /api/v1/tasks`: 작업 제출 및 자동 에이전트 선택
- `POST /api/v1/tasks/{agent_name}`: 특정 에이전트에게 직접 작업 할당
- `POST /api/v1/select-agent`: 적합한 에이전트 선택 (작업 실행 없음)

### 에이전트 관련 엔드포인트

- `GET /api/v1/agents`: 현재 사용 가능한 에이전트 목록 조회
- `GET /api/v1/agents/{agent_name}`: 특정 에이전트 정보 조회

### 상태 확인 엔드포인트

- `GET /api/v1/health`: 서비스 상태 확인

## 사용 예시

### 작업 제출 및 자동 에이전트 선택

```bash
curl -X POST http://localhost:8001/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "2020년부터 2023년까지의 판매 데이터를 분석해서 추세를 알려줘",
    "context": {
      "format": "table",
      "data_source": "sales_db"
    }
  }'
```

### 특정 에이전트에게 직접 작업 할당

```bash
curl -X POST http://localhost:8001/api/v1/tasks/DataAnalysisExpert \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "2020년부터 2023년까지의 판매 데이터를 분석해서 추세를 알려줘",
    "context": {
      "format": "table",
      "data_source": "sales_db"
    }
  }'
```

### 적합한 에이전트 선택 (작업 실행 없음)

```bash
curl -X POST http://localhost:8001/api/v1/select-agent \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "새로운 SF 소설 아이디어를 제안해줘"
  }'
```

## 테스트

```bash
# 단위 테스트 실행
python -m unittest discover tests
```
