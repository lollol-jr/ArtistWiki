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

## 개발 시작하기

### 사전 요구사항
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+

### 설치 및 실행

1. 저장소 클론
```bash
git clone <repository-url>
cd ArtistWiki
```

2. 백엔드 실행
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

3. 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

4. MediaWiki 실행
```bash
cd mediawiki
docker-compose up -d
```

## 환경 변수

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/artistwiki
MEDIAWIKI_API_URL=http://localhost:8080/api.php
OPENAI_API_KEY=your-openai-key
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
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
