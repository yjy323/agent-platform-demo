# Base Agent

LLM 기반 에이전트 시스템을 위한 기본 프레임워크입니다. 이 패키지는 다양한 전문 에이전트를 구현하기 위한 공통 인터페이스와 API 서버를 제공합니다.

## 개요

Base Agent는 LLM(Large Language Model)을 활용한 에이전트를 쉽게 구현할 수 있는 추상 클래스와 FastAPI 기반 API 서버를 제공합니다. 이를 통해 다양한 특화된 에이전트를 일관된 인터페이스로 구현하고 컨테이너로 배포할 수 있습니다.

## 설치 및 사용

### 도커 이미지 빌드

```bash
docker build -t base-agent .
