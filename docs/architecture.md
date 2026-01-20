# ArtistWiki 아키텍처

## 시스템 개요

```
┌─────────────┐
│   사용자    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Next.js Frontend (Port 3000)    │
│  - 커스텀 UI/UX                     │
│  - 작가/작품 브라우징                │
│  - 에이전트 대시보드                 │
└──────┬──────────────────────────────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────┐
│    FastAPI Backend (Port 8000)      │
│  ┌─────────────────────────────┐   │
│  │  Agent Orchestrator         │   │
│  │  - Crawler Agent            │   │
│  │  - Writer Agent (GPT-4)     │   │
│  │  - MediaWiki Agent          │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │  API Routes                 │   │
│  │  - Artists CRUD             │   │
│  │  - Works CRUD               │   │
│  │  - Agent Jobs               │   │
│  └─────────────────────────────┘   │
└──────┬────────────┬─────────────────┘
       │            │
       │            │ HTTP/API
       │            ▼
       │     ┌─────────────────────┐
       │     │ MediaWiki (8080)    │
       │     │ - Wiki Engine       │
       │     │ - Version Control   │
       │     │ - Edit Conflicts    │
       │     └──────┬──────────────┘
       │            │
       │            ▼
       │     ┌─────────────────────┐
       │     │ PostgreSQL          │
       │     │ (MediaWiki DB)      │
       │     └─────────────────────┘
       │
       ▼
┌─────────────────────┐
│ PostgreSQL (15436)  │
│ (Application DB)    │
│ - artists           │
│ - works             │
│ - relationships     │
│ - agent_jobs        │
└─────────────────────┘
```

## 컴포넌트 설명

### 1. Frontend (Next.js)

**역할:**
- 사용자 인터페이스 제공
- 작가/작품 검색 및 브라우징
- 에이전트 작업 모니터링 대시보드
- MediaWiki 콘텐츠 렌더링

**주요 기능:**
- Server-Side Rendering (SSR)
- 반응형 디자인
- 실시간 에이전트 상태 업데이트

### 2. Backend (FastAPI)

**역할:**
- API 엔드포인트 제공
- 에이전트 오케스트레이션
- 비즈니스 로직 처리
- MediaWiki API 연동

**주요 모듈:**

#### Agent System
```
Orchestrator
├── Crawler Agent
│   └── 외부 소스에서 작가 정보 수집
├── Writer Agent
│   └── GPT-4로 위키 페이지 생성
└── MediaWiki Agent
    └── MediaWiki API로 페이지 업로드
```

#### API Routes
- `/api/v1/artists` - 작가 CRUD
- `/api/v1/works` - 작품 CRUD
- `/api/v1/agents` - 에이전트 작업 관리
- `/api/v1/relationships` - 작가 관계 관리

### 3. MediaWiki

**역할:**
- 위키 페이지 저장 및 관리
- 버전 관리 (revision history)
- 편집 충돌 해결
- 검색 기능

**API 사용:**
- `action=edit` - 페이지 생성/수정
- `action=query` - 페이지 조회
- `action=parse` - 위키텍스트 파싱
- `action=opensearch` - 검색

### 4. PostgreSQL (Application DB)

**역할:**
- 애플리케이션 데이터 저장
- 에이전트 작업 기록
- 작가/작품 메타데이터

**주요 테이블:**
- `artists` - 작가 정보
- `works` - 작품 정보
- `relationships` - 작가 간 관계
- `agent_jobs` - 에이전트 작업 이력

## 데이터 흐름

### 작가 정보 자동 생성 워크플로우

```
1. 사용자가 작가 이름 입력
   ↓
2. Orchestrator가 워크플로우 시작
   ↓
3. Crawler Agent 실행
   - 외부 소스에서 정보 수집
   - 구조화된 데이터 추출
   ↓
4. Writer Agent 실행
   - GPT-4로 위키 페이지 생성
   - 위키텍스트 포맷팅
   ↓
5. MediaWiki Agent 실행
   - MediaWiki API로 페이지 생성
   - 페이지 ID 반환
   ↓
6. Application DB 업데이트
   - Artist 레코드 생성
   - MediaWiki 페이지 ID 저장
   ↓
7. 사용자에게 결과 표시
```

## 에이전트 오케스트레이션

### Sequential Workflow (순차 실행)
```python
workflow = [
    {
        "agent_type": "crawler",
        "task_data": {"url": "...", "artist_name": "..."}
    },
    {
        "agent_type": "writer",
        "task_data": {"artist_name": "...", "artist_type": "..."}
    },
    {
        "agent_type": "mediawiki",
        "task_data": {"action": "create", "page_title": "...", "content": "..."}
    }
]

result = await orchestrator.execute_workflow(workflow, db, context)
```

### Context Passing
각 에이전트는 이전 에이전트의 결과를 `context`로 전달받아 사용

## 보안

### API Security
- JWT 토큰 인증
- CORS 설정
- Rate Limiting

### MediaWiki Security
- Bot 계정 사용
- 최소 권한 원칙
- API 접근 제한

### Database Security
- SSH 터널링
- 암호화된 연결
- 환경 변수로 credential 관리

## 확장성

### Horizontal Scaling
- Backend: 여러 인스턴스 배포 가능
- Frontend: Vercel Edge Network
- MediaWiki: Read replica 추가 가능

### Caching
- Redis for API responses
- MediaWiki page cache
- Agent result cache

## 모니터링

### Metrics
- Agent 실행 성공률
- API 응답 시간
- MediaWiki API 호출 횟수
- Database 쿼리 성능

### Logging
- Structured logging (JSON)
- Agent 활동 상세 로그
- Error tracking

## 배포 아키텍처 (Dokploy)

```
Dokploy Server
├── PostgreSQL (Port 5436)
│   └── artistwiki database
├── Backend Container
│   ├── FastAPI app
│   └── Agent System
├── Frontend Container
│   └── Next.js app
└── MediaWiki Container
    ├── MediaWiki app
    └── PostgreSQL (MediaWiki DB)
```
