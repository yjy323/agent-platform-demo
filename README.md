# LLM 기반 Multi Agent 시스템

확장 가능한 LLM(Large Language Model) 기반의 멀티 에이전트 시스템입니다. 이 프로젝트는 런타임에 동적으로 에이전트를 관리할 수 있는 유연한 아키텍처를 제공합니다.

## 프로젝트 구조
```
agent-platform-demo/
├── src/                    # 소스 코드
│   ├── bad_code.py        # 코드 품질 테스트용 예시
│   └── fixed_code.py      # 수정된 코드 예시
├── tests/                 # 테스트 코드
│   └── test_quality_tools.py  # 코드 품질 도구 테스트
├── scripts/               # 스크립트
│   └── run_test.sh       # 테스트 실행 스크립트
├── venv/                  # 가상환경 (git ignored)
├── .env                   # 환경 변수
├── .git-commit-template.txt  # 커밋 메시지 템플릿
├── .gitignore            # Git 제외 파일
├── pyproject.toml        # 프로젝트 설정
├── requirements.txt      # 의존성 목록
├── setup.cfg            # 설정 파일
└── README.md            # 프로젝트 설명
```

## 프로젝트 개요

이 프로젝트는 다음과 같은 주요 목표를 가지고 있습니다:

1. FastAPI 기반의 확장 가능한 API 서버 구축
2. 런타임에 에이전트를 동적으로 관리할 수 있는 브로커 패턴 구현
3. 기본 에이전트 구현 및 통신 테스트
4. 인메모리 메시지 큐를 통한 컴포넌트 간 통신
5. 지속적인 품질 관리를 위한 Ground Rule 도입

## 시스템 아키텍처

시스템은 다음과 같은 주요 컴포넌트로 구성됩니다:

- **API Gateway**: FastAPI 기반의 엔드포인트 제공
- **Orchestrator**: 작업 분배 및 워크플로우 관리
- **Agent Broker**: 에이전트 등록/관리 및 에이전트 레지스트리 관리
- **Message Queue**: 인메모리 기반 컴포넌트 간 통신
- **Base Agents**: 기본 에이전트 구현 (ReAct, Function-Call)

## 주요 기능

- 동적 에이전트 관리 (등록/삭제/수정)
- 브로커 패턴 기반 에이전트 통신
- 확장 가능한 API 인터페이스
- 인메모리 메시지 큐 기반 비동기 통신
- 모듈화된 에이전트 아키텍처

## 기술 스택

- **Backend**: FastAPI
- **Message Queue**: 인메모리 구현 (추후 RabbitMQ 등 고려)
- **Documentation**: OpenAPI (Swagger)
- **Testing**: pytest

## Ground Rules

### 1. 코드 품질 관리

#### 1.1 코드 스타일 및 포맷팅
- **Black**: 자동 코드 포맷팅
  - 최대 줄 길이: 88자
  - 큰따옴표 문자열 사용
- **isort**: import 문 자동 정렬
  - 표준 라이브러리, 서드파티, 로컬 모듈 순 정렬
  - 알파벳 순 정렬

#### 1.2 정적 분석
- **Flake8**: 코드 스타일 및 품질 검사
  - PEP 8 준수
  - 순환 복잡도 제한: 10
  - 최대 중첩 수준: 4
- **mypy**: 타입 검사
  - Strict 모드 사용
  - 모든 함수/메서드에 타입 힌트 필수

### 2. 아키텍처 설계 원칙

#### 2.1 SOLID 원칙
- **단일 책임 원칙 (SRP)**: 각 클래스는 하나의 책임만 가짐
- **개방-폐쇄 원칙 (OCP)**: 확장에는 열려있고, 수정에는 닫혀있어야 함
- **인터페이스 분리 원칙 (ISP)**: 클라이언트는 사용하지 않는 인터페이스에 의존하지 않아야 함
- **의존성 역전 원칙 (DIP)**: 추상화에 의존하고, 구체화에 의존하지 않음

#### 2.2 모듈화
- 명확한 책임 분리
- 인터페이스 기반 설계
- 느슨한 결합도, 높은 응집도
- 순환 의존성 금지

### 3. 문서화 요구사항

#### 3.1 필수 문서
- **API 문서**: OpenAPI/Swagger 사용
- **아키텍처 문서**: 시스템 구조도, 컴포넌트 다이어그램
- **데이터 모델**: ERD, 스키마 정의
- **README**: 설치, 설정, 실행 방법

#### 3.2 코드 문서화
- **Docstring**: Google 스타일 사용
  ```python
  def function(arg: type) -> return_type:
      """함수 설명.

      Args:
          arg: 인자 설명

      Returns:
          반환값 설명

      Raises:
          예외 설명
      """
  ```
- 모든 public API에 대한 문서화 필수

### 4. 오류 처리 및 로깅

#### 4.1 예외 처리
- 커스텀 예외 계층 구조 사용
- 의미 있는 에러 메시지 제공
- 예외는 최대한 구체적으로 정의

#### 4.2 로깅
- 구조화된 로깅 사용
- 로그 레벨 적절히 구분
- 민감 정보 로깅 금지

### 5. 보안 가이드라인

#### 5.1 기본 보안
- 모든 API 엔드포인트 인증 필수
- 환경 변수를 통한 설정 관리
- HTTPS 통신 필수

#### 5.2 LLM 특화 보안
- 프롬프트 인젝션 방지
- 민감 정보 필터링
- 모델 출력 검증

### 6. 개발 프로세스

#### 6.1 버전 관리
- **브랜치 전략**: GitHub Flow
  - `main`: 프로덕션 브랜치
  - `feature/*`: 기능 개발
- **커밋 메시지 컨벤션**
  ```
	# .git-commit-template 참고

	<type>(<scope>): <subject>

	<body>

	<footer>
  ```

#### 6.2 테스트
- 단위 테스트 커버리지 80% 이상
- 통합 테스트 필수
- LLM 응답 품질 테스트
- CI 파이프라인 연동

#### 6.3 배포
- Docker 기반 컨테이너화
- CI/CD 자동화
- 무중단 배포 지원
- 모니터링 및 알림 구성

## 향후 계획

- 보안 강화
- 성능 최적화
- 분산 시스템 지원
- 영구 저장소 도입
- 모니터링 시스템 구축

## 프로젝트 설정

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
uvicorn main:app --reload
```

## 기여 가이드

1. 이슈 생성
2. 브랜치 생성 (`feature/기능명`)
3. 코드 작성 및 테스트
4. PR 생성
5. 코드 리뷰 후 머지

## 라이센스

MIT License
