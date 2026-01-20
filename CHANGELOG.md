# Changelog

## [0.1.1] - 2026-01-21

### Changed - 안전한 의존성 업데이트

#### Frontend
- **Node.js 18 → 24 (LTS Krypton)**
  - Active LTS로 2028년까지 지원
  - 보안 패치 및 성능 개선

#### Backend
- **FastAPI 0.109.0 → 0.128.0**
  - Pydantic v2 완전 전환
  - 19개 버전 업그레이드
  - 보안 및 버그 수정

- **Uvicorn 0.27.0 → 0.34.0**
  - 보안 패치
  - 성능 개선

- **Pydantic 2.5.3 → 2.10.5**
  - 버그 수정
  - 타입 시스템 개선

- **SQLAlchemy 2.0.25 → 2.0.36**
  - 버그 수정
  - 안정성 개선

- **AsyncPG 0.29.0 → 0.30.0**
  - PostgreSQL 17 최적화

- **Alembic 1.13.1 → 1.14.0**
  - 마이그레이션 개선

- **HTTP Clients**
  - HTTPX 0.26.0 → 0.28.1
  - AIOHTTP 3.9.1 → 3.11.11
  - Requests 2.31.0 → 2.32.3

- **Utilities**
  - python-dotenv 1.0.0 → 1.0.1
  - python-dateutil 2.8.2 → 2.9.0
  - pytz 2023.3 → 2024.2
  - pydantic-extra-types 2.3.0 → 2.10.0

- **AI & LLM** (의존성 충돌 해결)
  - OpenAI 1.10.0 → 1.66.1
  - Anthropic 0.9.0 → 0.76.0
  - LangChain 0.1.0 → 0.3.18
  - LangChain-OpenAI 0.0.2 → 0.2.14
  - LangChain-Anthropic 0.1.1 → 0.3.9

### Fixed
- **의존성 충돌 해결**
  - anthropic 0.9.0과 langchain-anthropic 0.1.1 버전 충돌 해결
  - AI 패키지를 최신 호환 버전으로 업데이트

- **설정 파일 수정**
  - `.env.example` ALLOWED_ORIGINS 형식을 JSON 배열로 수정
  - Pydantic Settings 2.5.0 호환성 개선

### Tested
- ✅ Backend 서버 시작 (FastAPI 0.128 + Python 3.11)
- ✅ Frontend 빌드 (Next.js 14 + Node 24)
- ✅ Docker Compose 전체 시스템 빌드
- ✅ 모든 의존성 설치 및 호환성 검증

### Notes
- 모든 업데이트는 하위 호환성 유지
- Breaking changes 없음
- 프로덕션 배포 가능

---

## [0.1.0] - 2026-01-20

### Added - 초기 프로젝트 설정

#### Infrastructure
- Dokploy 프로젝트 생성 (ArtistWiki)
- Git 저장소 초기화
- Docker Compose 전체 시스템 통합

#### Backend (FastAPI)
- Python 3.11 + FastAPI 프로젝트 구조
- PostgreSQL 17 AsyncIO 연동
- SQLAlchemy 모델 4개 (Artist, Work, Relationship, AgentJob)
- Pydantic 스키마
- Alembic 마이그레이션
- API 라우터 3개 (Artists, Works, Agents)

#### Agent System
- Orchestrator (워크플로우 조율)
- Crawler Agent (정보 수집)
- Writer Agent (GPT-4 페이지 생성)
- MediaWiki Agent (API 연동)

#### Frontend (Next.js 14)
- TypeScript + Tailwind CSS
- App Router 구조
- API 클라이언트 (SSR 지원)
- TypeScript 타입 정의

#### MediaWiki
- MediaWiki 1.45 Docker 설정
- PostgreSQL 17 통합
- 한국어 설정

#### Documentation
- README.md
- Quick Start Guide
- Architecture 문서
- Agent System 설계
- API Specifications
- Development Guide
- Deployment Guide (Dokploy)
