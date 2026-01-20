# ArtistWiki Project Guidelines

---

## 📍 Current Project: ArtistWiki

작가/예술가 위키 시스템 - 미디어위키 + AI 에이전트 오케스트레이션

---

## Project Overview

ArtistWiki는 미술가, 작가(문학), 음악가 등 예술가들의 정보를 체계적으로 관리하는 AI 기반 위키 플랫폼입니다.

### Core Architecture
```
[Next.js Frontend] → [FastAPI Backend + Agent System] → [MediaWiki API] → [PostgreSQL]
```

### Key Features
- 미디어위키의 모든 위키 기능 활용 (버전 관리, 편집 충돌 해결 등)
- 커스텀 프론트엔드로 독창적인 UI/UX 제공
- AI 에이전트 오케스트레이션으로 자동화된 콘텐츠 생성

---

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Wiki Engine**: MediaWiki (API 연동)
- **Database**: PostgreSQL 15+
- **AI**: OpenAI API, LangChain
- **Deployment**: Dokploy (backend), Vercel (frontend)

---

## Project Structure

```
ArtistWiki/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 앱 진입점
│   │   ├── api/                 # API 라우터
│   │   ├── agents/              # 에이전트 시스템
│   │   │   ├── orchestrator.py # 오케스트레이터
│   │   │   ├── crawler.py      # 크롤링 에이전트
│   │   │   ├── writer.py       # 작성 에이전트
│   │   │   └── mediawiki.py    # 미디어위키 연동 에이전트
│   │   ├── models/              # 데이터 모델
│   │   ├── schemas/             # Pydantic 스키마
│   │   ├── services/            # 비즈니스 로직
│   │   └── core/                # 설정, 의존성
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router
│   │   ├── components/          # React 컴포넌트
│   │   ├── lib/                 # 유틸리티
│   │   └── types/               # TypeScript 타입
│   ├── package.json
│   └── .env.local
├── mediawiki/
│   ├── docker-compose.yml       # MediaWiki + PostgreSQL
│   ├── LocalSettings.php        # MediaWiki 설정
│   └── extensions/              # MediaWiki 확장
├── agents/                      # 독립적인 에이전트 모듈
│   ├── base.py                  # 베이스 에이전트
│   ├── protocols.py             # 에이전트 프로토콜
│   └── utils.py
├── docs/
│   ├── architecture.md          # 아키텍처 문서
│   ├── agent-system.md          # 에이전트 시스템 설계
│   └── api-specs.md             # API 명세
├── .claude/
│   └── database.md              # DB 접속 정보
├── VERSION
├── README.md
└── CLAUDE.md
```

---

## Agent System Architecture

### Orchestrator Pattern
```
[Orchestrator]
    ↓
[Sub-Agent 1: Crawler]    → 외부 소스에서 정보 수집
[Sub-Agent 2: Writer]     → AI로 위키 페이지 생성
[Sub-Agent 3: MediaWiki]  → API로 페이지 업로드
```

### Agent Responsibilities

#### 🎼 Orchestrator
- 에이전트 간 워크플로우 조율
- 작업 큐 관리
- 에러 핸들링 및 재시도 로직

#### 🤖 Crawler Agent (Phase 1)
- 외부 웹사이트에서 작가 정보 크롤링
- 구조화된 데이터 추출
- 출처 URL 기록

#### 🤖 Writer Agent (Phase 1)
- AI(GPT-4)를 사용한 위키 페이지 초안 생성
- 위키 문법으로 포맷팅
- 카테고리 및 태그 자동 생성

#### 🤖 MediaWiki Agent (Phase 1)
- MediaWiki API를 통한 페이지 CRUD
- 버전 관리 및 편집 이력 추적
- 권한 관리

---

## Development Workflow

### Phase 1: MVP (현재)
1. ✅ Dokploy 프로젝트 생성
2. ✅ 로컬 프로젝트 구조 생성
3. ⏳ 백엔드 기본 설정
4. ⏳ 프론트엔드 기본 설정
5. ⏳ MediaWiki Docker 설정
6. ⏳ 오케스트레이터 구현
7. ⏳ 기본 에이전트 구현

### Phase 2: 품질 향상
- 검증 에이전트 추가
- 카테고리 에이전트 추가
- 이미지 처리 에이전트 추가

### Phase 3: 고급 기능
- 관계 분석 에이전트
- 추천 시스템
- 고급 검색

---

## Database Schema (예상)

### Artists Table
```sql
CREATE TABLE artists (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- 'painter', 'writer', 'musician'
    birth_date DATE,
    death_date DATE,
    nationality VARCHAR(100),
    mediawiki_page_id INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Works Table
```sql
CREATE TABLE works (
    id UUID PRIMARY KEY,
    artist_id UUID REFERENCES artists(id),
    title VARCHAR(500) NOT NULL,
    year INTEGER,
    type VARCHAR(100),
    mediawiki_page_id INTEGER,
    created_at TIMESTAMP
);
```

---

## MediaWiki API Integration

### Key Endpoints
- **GET /api.php?action=query** - 페이지 조회
- **POST /api.php?action=edit** - 페이지 생성/수정
- **GET /api.php?action=parse** - 위키텍스트 파싱
- **GET /api.php?action=opensearch** - 검색

### Authentication
- Bot 계정 생성 필요
- Bot password 발급
- API 요청 시 토큰 사용

---

## Environment Variables

### Backend (.env)

**로컬 개발:**
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:15436/artistwiki

# MediaWiki
MEDIAWIKI_API_URL=http://localhost:5050/api.php
MEDIAWIKI_BOT_USERNAME=bot@artistwiki
MEDIAWIKI_BOT_PASSWORD=your-bot-password

# AI
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# App
SECRET_KEY=your-secret-key
DEBUG=True
```

**프로덕션 (Dokploy):**
```bash
# Database
DATABASE_URL=postgresql://artistwiki_user:password@artistwiki-db:5432/artistwiki

# MediaWiki
MEDIAWIKI_API_URL=https://okidokiwiki.jrai.space/api.php
MEDIAWIKI_BOT_USERNAME=bot@artistwiki
MEDIAWIKI_BOT_PASSWORD=your-bot-password

# AI
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# App
SECRET_KEY=your-secret-key
DEBUG=False
```

### Frontend (.env.local)

**로컬 개발:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MEDIAWIKI_URL=http://localhost:5050
```

**프로덕션:**
```bash
NEXT_PUBLIC_API_URL=https://api-wiki.jrai.space
NEXT_PUBLIC_MEDIAWIKI_URL=https://okidokiwiki.jrai.space
```

---

## Git Workflow

### Branching Strategy
- `main`: 프로덕션 브랜치
- `develop`: 개발 브랜치
- `feature/agent-crawler`: 기능 브랜치
- `fix/mediawiki-auth`: 버그 수정 브랜치

### Commit Convention
```bash
feat: 새로운 기능 (v0.2.0)
fix: 버그 수정 (v0.1.1)
docs: 문서 업데이트
refactor: 코드 리팩토링
test: 테스트 추가
```

---

## Deployment (Dokploy)

### Services to Deploy
1. **backend**: FastAPI 애플리케이션
2. **frontend**: Next.js 애플리케이션 (또는 Vercel)
3. **mediawiki**: MediaWiki (Docker Compose)
4. **postgres**: PostgreSQL 데이터베이스

### Deployment Order
1. PostgreSQL 생성 및 실행
2. MediaWiki 배포 및 초기 설정
3. Backend 배포
4. Frontend 배포

---

## Testing Strategy

### Backend Tests
- Unit tests: pytest
- Integration tests: TestClient
- Agent tests: Mock 외부 API

### Frontend Tests
- Component tests: Jest + React Testing Library
- E2E tests: Playwright

---

## Performance Considerations

### Caching Strategy
- Redis for API response caching
- MediaWiki page caching
- Agent result caching

### Rate Limiting
- MediaWiki API: 50 requests/minute
- OpenAI API: 3500 requests/minute (GPT-4)

---

## Security Guidelines

### API Security
- JWT 토큰 인증
- CORS 설정
- Rate limiting
- Input validation

### MediaWiki Security
- Bot 계정 권한 최소화
- API 접근 IP 제한
- 정기적인 패스워드 변경

---

## Monitoring & Logging

### Logging
- Structured logging (JSON)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Agent 활동 로그 상세 기록

### Monitoring
- API response time
- Agent 실행 성공률
- MediaWiki API 호출 횟수

---

## Next Steps

1. Backend FastAPI 기본 구조 생성
2. Frontend Next.js 프로젝트 초기화
3. MediaWiki Docker 설정
4. PostgreSQL 스키마 생성
5. Orchestrator 기본 구현
6. Crawler Agent 구현
7. Writer Agent 구현
8. MediaWiki Agent 구현

---

## Notes

- 이 프로젝트는 MVP 단계부터 단계적으로 개발합니다
- 각 Phase 완료 후 사용자 피드백 반영
- 에이전트는 독립적으로 테스트 가능하도록 설계
- MediaWiki API 변경사항 지속 모니터링 필요
