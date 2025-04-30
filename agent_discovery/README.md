# Agent Discovery 서비스 Agile Backlog

PoC 완료 후 Prototype 및 Production 단계의 요구사항을 정리한 Agile Backlog입니다.

## 1. Prototype 단계 티켓

### 에픽: CI/CD 및 DevOps

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T0 | CI/CD 파이프라인 구축 | High | 코드 푸시부터 Staging 배포까지 자동화된 워크플로우 구성 | - GitHub Actions로 lint → unit test → Docker 빌드 → Registry 푸시 → Staging 배포 자동화<br>- PR 머지 시 CI 통과 확인 |

### 에픽: 도메인 모델 및 데이터 모델 구현

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T1 | Consul API 스키마 DTO 정의 | High | Consul HTTP API 요청/응답 페이로드를 위한 `DTO 클래스` 정의 | - DTO 클래스에 대한 단위 테스트 작성<br>- Swagger/Proto 스펙 반영 |


### 에픽: 데이터 액세스 및 저장소 계층

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T2a | DiscoveryClient 인터페이스 정의 | High | `DiscoveryClient` 인터페이스 정의 | - Repository 인터페이스 구현<br>- CRUD 메서드 정의<br>- 의존성 주입 설계 |
| T2b | ConsulDiscoveryClient 구현 | High | `DiscoveryClient` 인터페이스를 구현하는 Consul 기반 구현체 개발 | - 인터페이스 구현<br>- Consul HTTP API와의 통신 구현<br>- 단위/통합 테스트 |
| T2c | DiscoveryClient 안정성 강화 | Medium | DiscoveryClient의 예외처리 및 재시도 로직 개선, 안정성 강화 | - 네트워크 실패 시 지수 백오프 방식으로 3회 재시도 구현<br>- 타임아웃 및 오류 상황 처리 개선<br>- 연결 실패/성공 로깅 강화 |
Medium | 비즈니스 로직 내 예외 처리 및 오류 전파 전략 구현 | - 도메인 예외 정의<br>- 외부 시스템 오류 처리<br>- 일관된 예외 처리 패턴 적용 |

### 에픽: 비즈니스 로직 계층

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T3a | DiscoveryService 인터페이스 정의 | High | 비즈니스 로직을 캡슐화하는 `DiscoveryService` 인터페이스 정의 | - 서비스 인터페이스 설계<br>- 에이전트 등록/조회/갱신/삭제 메서드 정의<br>- 능력 기반 에이전트 검색 메서드 정의 |
| T3b | ConsulDiscoveryService 구현 | High | Consul 기반의 `비즈니스 로직` 구현체 | - Consul DiscoveryService 인터페이스 구현<br>- Consul HTTP API와의 통신 구현<br>- 단위/통합 테스트 |
| T3c | AgentCardToConsulDTOService 구현 | High | AgentCard ↔ Consul DTO 간 변환 로직을 담당하는 `비즈니스 로직` 구현 | - DTO→AgentCard, AgentCard→DTO 양방향 매핑 테스트 커버 100%<br>- 통합 테스트로 실제 등록/조회 검증<br>- 비즈니스 규칙 적용 |
| T3d | 예외 처리 전략 구현 | Medium | 비즈니스 로직 내 예외 처리 및 오류 전파 전략 구현 | - 도메인 예외 정의<br>- 외부 시스템 오류 처리<br>- 일관된 예외 처리 패턴 적용 |

### 에픽: FastAPI CRUD 엔드포인트

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T4a | Agent 등록 API 구현 | High | `/services` (POST) - 새 서비스 등록 및 대응 gRPC RPC 구현 | - Pydantic 모델 사용<br>- 단위 테스트 통과<br>- OpenAPI 문서 자동 노출 |
| T4b | Agent 조회 API 구현 | High | `/services` (GET) - 전체 서비스 목록 조회<br>`/services/{id}` (GET) - 특정 서비스 조회 및 대응 gRPC RPC | - 전체 및 개별 조회 기능<br>- 단위 테스트 통과 |
| T4c | Agent 수정 API 구현 | High | `/services/{id}` (PUT) - 전체 업데이트<br>`/services/{id}` (PATCH) - 부분 업데이트 및 대응 gRPC RPC | - 전체/부분 업데이트 지원<br>- 존재하지 않는 ID 오류 처리<br>- 변경사항 검증 |
| T4d | Agent 삭제 API 구현 | High | `/services/{id}` (DELETE) - 서비스 삭제 및 대응 gRPC RPC | - 삭제 성공/실패 명확한 응답<br>- 존재하지 않는 ID 오류 처리<br>- 단위 테스트 통과 |
| T4e | Agent Heartbeat API 구현 | High | `/services/{id}/heartbeat` (POST) - 생존 신호 전송 및 대응 gRPC RPC | - TTL 만료 시 인스턴스 제거<br>- 타임스탬프 업데이트 확인<br>- 테스트 통과 |

### 에픽: Agent 능력 기반 조회

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T5 | QueryAgents 기능 구현 | High | `capabilities`, `modalities`, `version`, `tags` 기반 Agent 조회 API (`/services/query`) 구현 | - 필터 조합 테스트 통과<br>- API 문서 (Swagger, Proto) 반영 |

### 에픽: API 문서화 & 자동화

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T6 | OpenAPI·Proto 스펙 자동화 | Medium | FastAPI Swagger UI (`/docs`) 및 `.proto` 스펙 자동 생성 스크립트 추가 | - `make docs`로 OpenAPI JSON/YAML 및 `.proto` 생성<br>- CI 파이프라인에서 문서 검증 |

### 에픽: 성능 최적화

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T7 | 캐싱 레이어 도입 | Medium | 자주 조회되는 Agent 정보에 대한 캐싱 메커니즘 구현 | - Redis 캐싱 구현<br>- 캐시 무효화 전략 구현<br>- 성능 측정 및 개선 확인 |
| T8 | 부하 테스트 및 최적화 | Medium | 고부하 상황에서 서비스 성능 검증 및 최적화 | - 동시 요청 처리 성능 측정<br>- 병목 지점 식별 및 개선<br>- 성능 메트릭 수집 및 분석 |

### 에픽: 보안 및 모니터링

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T9 | TLS 설정 (HTTPS/gRPC TLS) | Medium | HTTPS 및 gRPC TLS, Consul ACL 토큰 검증 기능 추가 | - mTLS 핸드쉐이크 성공 시 연결 허용<br>- 잘못된 ACL 토큰 요청 시 `401 Unauthorized` |
| T10 | Prometheus 메트릭 노출 | Medium | 요청 지연, 오류율, Heartbeat 실패 카운터 등 메트릭 수집 및 `/metrics` 엔드포인트 제공 | - `/metrics`에서 `REQUEST_LATENCY`, `ERROR_COUNT` 확인<br>- 기본 Grafana 대시보드 샘플 제공 |

### 에픽: UI/CLI 대체 전략 (옵션)

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T11 | Swagger UI & CLI 스크립트 활용 | Low | React/Vue 대시보드 대신 Swagger UI와 CLI 도구로 CRUD 검증 | - `/docs` (Swagger UI) 정상 작동<br>- `discovery-cli list` 등 CLI 명령어로 CRUD 수행 |

## 2. Production 단계 티켓

### 에픽: 보안 및 운영 강화

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T12 | mTLS & Consul ACL 통합 | High | 서비스 간 상호 TLS 인증, Consul Token 권한 관리 | - 인증 실패 시 연결 거부<br>- 토큰별 권한 검증 |
| T13 | 분산 추적·감사 로깅 | Medium | OpenTracing/Jaeger 통합, Audit Log 저장소 구축 | - Trace ID 연동 확인<br>- 감사 로그 검색 및 모니터링 가능 |

### 에픽: 스케일링 & 복제

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T14 | 멀티 리전 복제 구성 | High | Consul Federation / etcd 복제 설정 및 문서화 | - 리전 간 데이터 동기화 시나리오 테스트 통과 |
| T15 | DNS 통합 지원 | Medium | External-DNS 또는 DNS-SRV 레코드 자동화 | - 신규 인스턴스 등록 시 DNS 레코드 확인 |

### 에픽: 고급 검색·이벤트

| 티켓 ID | 제목 | 우선순위 | 설명 | 수용 기준(AC) |
|---------|------|---------|------|--------------|
| T16 | Elasticsearch 연동 검색 API | Low | Agent 카탈로그 색인 및 추천 엔드포인트 구현 | - 대규모 색인 후 P95 응답 ≤100ms |
| T17 | Kafka 이벤트 퍼블리싱 | Low | 등록·해제·상태 변경 이벤트를 Kafka 토픽으로 전송 | - Consumer에서 이벤트 수신 확인 |

## 노트

- **AgentCard 모델 정의**는 이미 구현되어 있어 현재 백로그에서 제거되었습니다.
- **우선순위**: Prototype 단계 High → Medium → Low 순으로 스프린트에 배치하세요.
- **티켓 분할**: T4(T4a~T4c)로 CRUD 세분화하여 커밋 단위 명확화
- **UI 전략**: 초기 Prototype에서는 Swagger UI / CLI 도구 활용으로 비용 절감
- T5~T7은 T0~T3 병렬로 진행 가능
- 중요도 대비 개발 비용 최적화 고려
