# ArtistWiki

작가/예술가를 위한 AI 기반 위키 시스템

## 개요

ArtistWiki는 미술가, 작가(문학), 음악가 등 예술가들의 정보를 체계적으로 관리하고, AI 에이전트 오케스트레이션을 통해 자동화된 콘텐츠 생성 및 관리 기능을 제공하는 위키 플랫폼입니다.

## 아키텍처

```
[사용자]
   ↓
[Next.js 프론트엔드] - 커스텀 UI/UX
   ↓
[FastAPI 백엔드] - 오케스트레이터 + 에이전트 시스템
   ↓
[MediaWiki API] - 위키 엔진 (버전 관리, 편집 충돌 해결 등)
   ↓
[PostgreSQL] - 데이터베이스
```

## 주요 기능

### Phase 1: 기본 시스템 (MVP)
- 🎼 **오케스트레이터**: 전체 워크플로우 조율
- 🤖 **크롤링 에이전트**: 외부에서 작가 정보 수집
- 🤖 **작성 에이전트**: AI로 위키 페이지 초안 생성
- 🤖 **미디어위키 연동 에이전트**: API로 페이지 CRUD

### Phase 2: 품질 향상
- 🤖 **검증 에이전트**: 정보 정확성 체크
- 🤖 **카테고리 에이전트**: 자동 분류
- 🤖 **이미지 처리 에이전트**: 이미지 최적화

### Phase 3: 고급 기능
- 🤖 **관계 분석 에이전트**: 작가 간 관계 그래프
- 🤖 **추천 에이전트**: 유사 작가 추천
- 기타 확장...

## 기술 스택

- **Backend**: Python 3.11, FastAPI
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Wiki Engine**: MediaWiki (API 연동)
- **Database**: PostgreSQL
- **Deployment**: Dokploy (backend), Vercel (frontend)
- **AI**: OpenAI API, LangChain (에이전트 시스템)

## 프로젝트 구조

```
ArtistWiki/
├── backend/          # FastAPI 백엔드 + 에이전트 시스템
├── frontend/         # Next.js 프론트엔드
├── mediawiki/        # MediaWiki 설정 및 Docker 구성
├── agents/           # 에이전트 모듈 (독립적)
├── docs/             # 프로젝트 문서
├── .claude/          # Claude 설정 및 데이터베이스 정보
├── VERSION           # 버전 정보
└── README.md
```

## 빠른 시작

### Docker Compose로 전체 시스템 실행

```bash
# 1. 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필수 값 입력 (OPENAI_API_KEY 등)

# 2. 시스템 시작
docker-compose up -d

# 3. 접속
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000/docs
# - MediaWiki: http://localhost:8080
```

**자세한 내용은 [Quick Start Guide](./docs/quick-start.md)를 참조하세요.**

## 문서

- 📘 [Quick Start Guide](./docs/quick-start.md) - 빠른 시작 가이드
- 🏗️ [Architecture](./docs/architecture.md) - 시스템 아키텍처
- 🤖 [Agent System](./docs/agent-system.md) - 에이전트 시스템 설계
- 📖 [API Specifications](./docs/api-specs.md) - API 명세
- 💻 [Development Guide](./docs/development-guide.md) - 개발 가이드
- 🚀 [Deployment (Dokploy)](./docs/deployment-dokploy.md) - 배포 가이드

## 주요 기능 데모

### 작가 정보 자동 생성

```bash
curl -X POST "http://localhost:8000/api/v1/agents/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": [
      {
        "agent_type": "crawler",
        "task_data": {
          "url": "https://en.wikipedia.org/wiki/Pablo_Picasso",
          "artist_name": "Pablo Picasso"
        }
      },
      {
        "agent_type": "writer",
        "task_data": {
          "artist_name": "Pablo Picasso",
          "artist_type": "painter"
        }
      },
      {
        "agent_type": "mediawiki",
        "task_data": {
          "action": "create",
          "page_title": "Pablo_Picasso"
        }
      }
    ]
  }'
```

## 개발 가이드라인

- **Semantic Versioning** 사용 (MAJOR.MINOR.PATCH)
- **feat**: 새로운 기능 추가 시 MINOR 버전 증가
- **fix**: 버그 수정 시 PATCH 버전 증가
- 커밋 메시지: `feat: 기능 설명 (v0.2.0)`

## 라이선스

MIT License

## 기여

이슈 및 PR은 언제나 환영합니다!
