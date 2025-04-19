# Agent Broker Service

에이전트 등록 및 관리를 위한 마이크로서비스입니다. 이 서비스는 여러 전문 에이전트를 등록하고 관리하는 기능을 제공합니다.

## 기능

- 에이전트 등록 및 관리
- 에이전트 메타데이터 조회
- 에이전트 목록 조회
- 에이전트 정보 업데이트
- 에이전트 등록 해제

## 디렉토리 구조

```
agent-broker-service/
│
├── app/
│   ├── __init__.py        # 패키지 정의
│   ├── main.py            # FastAPI 애플리케이션 진입점
│   ├── broker.py          # AgentBroker 클래스 구현
│   ├── schemas.py         # Pydantic 모델 (요청/응답 스키마)
│   ├── routes.py          # API 라우트 및 핸들러
│   └── config.py          # 애플리케이션 설정
│
├── tests/
│   └── test_broker.py     # 단위 테스트
│
├── Dockerfile             # 컨테이너 이미지 정의
├── requirements.txt       # 의존성 패키지
└── README.md              # 프로젝트 문서
```

## 설치 및 실행

### 로컬 환경

```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
uvicorn app.main:app --reload
```

### Docker 환경

```bash
# 이미지 빌드
docker build -t agent-broker .

# 컨테이너 실행
docker run -p 8000:8000 agent-broker
```

## API 엔드포인트

- `POST /agents`: 새 에이전트 등록
- `GET /agents`: 등록된 모든 에이전트 목록 조회
- `GET /agents/{agent_name}`: 특정 에이전트 정보 조회
- `PUT /agents/{agent_name}`: 에이전트 정보 업데이트
- `DELETE /agents/{agent_name}`: 에이전트 등록 해제
- `GET /health`: 서비스 상태 확인

## 테스트

```bash
# 단위 테스트 실행
python -m unittest discover tests
```

## 사용 예시

### 에이전트 등록

```bash
curl -X POST http://localhost:8000/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DataAnalysisExpert",
    "endpoint": "http://data-analysis-agent:8080/run",
    "description": "데이터 분석 전문 에이전트",
    "skills": ["data interpretation", "statistical analysis"],
    "type": "llm"
  }'
```

### 에이전트 목록 조회

```bash
curl http://localhost:8000/agents
```

### 에이전트 정보 조회

```bash
curl http://localhost:8000/agents/DataAnalysisExpert
```
