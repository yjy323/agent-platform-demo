# GeneralAssistant 마이크로서비스

**Gemini 기반의 범용 작업 처리 에이전트**

GeneralAssistant는 Google Gemini API를 활용해 텍스트 요약, 설명 생성, 정보 검색, 창의적 콘텐츠 작성 등 일반적인 작업을 수행하는 마이크로서비스입니다.

---

## 주요 기능

- 텍스트 요약
- 일반 상식 질문 응답
- 간단한 추론
- 설명 생성
- 창의적 글쓰기

---

## 필요 조건

- Docker
- Google Gemini API 키 (`GOOGLE_API_KEY` 환경 변수로 설정)

---

## 설치 및 실행 방법

### 1. 환경 변수 설정

```bash
export GOOGLE_API_KEY=your_api_key_here
```

### 2. 도커 이미지 빌드

```bash
# base-agent 이미지 빌드
cd ../base-agent
docker build -t base-agent .

# general-assistant 이미지 빌드
cd ../general-assistant-agent
docker build -t general-assistant-agent .
```

### 3. 컨테이너 실행

```bash
docker run -p 8000:8000 -e GOOGLE_API_KEY=$GOOGLE_API_KEY general-assistant-agent
```

---

## API 사용법

### 에이전트 정보 조회

```bash
curl http://localhost:8000/agent/describe
```

### 프롬프트 처리

```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"text": "인공지능에 대해 간단히 설명해줘"}'
```

### 서비스 상태 확인

```bash
curl http://localhost:8000/health
```

---

## 디렉토리 구조

```
general-assistant/
├── Dockerfile
├── main.py
├── agent.py
├── requirements.txt
└── README.md
```

---

## 라이선스

MIT License
