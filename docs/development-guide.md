# Development Guide

## 로컬 개발 환경 설정

### 1. 사전 요구사항

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### 2. 프로젝트 클론 및 설정

```bash
cd /Users/jinwooro/Desktop/Project/ArtistWiki

# 환경 변수 파일 생성
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 환경 변수 편집 (필수)
# - OPENAI_API_KEY
# - MEDIAWIKI_BOT_USERNAME
# - MEDIAWIKI_BOT_PASSWORD
```

### 3. Docker Compose로 전체 시스템 실행

```bash
# 전체 시스템 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down

# 데이터 포함 완전 삭제
docker-compose down -v
```

**서비스 접속:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs
- MediaWiki: http://localhost:8080

### 4. 로컬 개발 (Docker 없이)

#### Backend

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
alembic upgrade head

# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

#### MediaWiki (Docker 필요)

```bash
cd mediawiki
docker-compose up -d
```

## 데이터베이스 관리

### Alembic 마이그레이션

```bash
cd backend

# 새 마이그레이션 생성
alembic revision --autogenerate -m "description"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1

# 현재 버전 확인
alembic current

# 마이그레이션 히스토리
alembic history
```

### PostgreSQL 직접 접속

```bash
# SSH 터널 설정 (Dokploy)
ssh -L 15436:127.0.0.1:5436 dokploy.jrai.space

# PostgreSQL 접속
psql postgresql://artistwiki_user:password@localhost:15436/artistwiki
```

## 개발 워크플로우

### 1. 새 기능 개발

```bash
# 1. Feature 브랜치 생성
git checkout -b feature/artist-search

# 2. 코드 작성
# backend/app/api/artists.py
# frontend/src/app/artists/page.tsx

# 3. 테스트 (추후 구현)
# pytest backend/tests/
# npm test

# 4. 커밋
git add .
git commit -m "feat: 작가 검색 기능 구현 (v0.2.0)"

# 5. Push
git push origin feature/artist-search
```

### 2. 버그 수정

```bash
git checkout -b fix/artist-date-validation
# 코드 수정
git commit -m "fix: 작가 생년월일 검증 로직 수정 (v0.1.1)"
```

## 에이전트 개발

### 새 에이전트 추가

1. **에이전트 클래스 생성**

```python
# backend/app/agents/my_agent.py
from app.agents.base import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("my_agent")

    async def execute(self, task_data):
        # 에이전트 로직 구현
        return {"result": "success"}
```

2. **오케스트레이터에 등록**

```python
# backend/app/api/agents.py
from app.agents.my_agent import MyAgent

orchestrator.register_agent("my_agent", MyAgent())
```

3. **테스트**

```python
# backend/tests/test_my_agent.py
import pytest
from app.agents.my_agent import MyAgent

@pytest.mark.asyncio
async def test_my_agent():
    agent = MyAgent()
    result = await agent.execute({"test": "data"})
    assert result["result"] == "success"
```

## API 개발

### 새 엔드포인트 추가

```python
# backend/app/api/artists.py

@router.get("/search")
async def search_artists(
    query: str,
    db: AsyncSession = Depends(get_db)
):
    # 검색 로직 구현
    pass
```

### Pydantic 스키마 추가

```python
# backend/app/schemas/artist.py

class ArtistSearch(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None
```

## 프론트엔드 개발

### 새 페이지 추가

```typescript
// frontend/src/app/artists/[id]/page.tsx

export default function ArtistDetailPage({ params }: { params: { id: string } }) {
  return <div>Artist Detail: {params.id}</div>
}
```

### API 호출

```typescript
// frontend/src/lib/api.ts
import apiClient from './api'

export async function getArtist(id: string) {
  const response = await apiClient.get(`/api/v1/artists/${id}`)
  return response.data
}
```

## MediaWiki 설정

### Bot 계정 생성

1. MediaWiki 관리자로 로그인 (http://localhost:8080)
2. **Special:BotPasswords** 페이지 접속
3. Bot 이름: `artistwiki`
4. 권한 선택: Edit existing pages, Create pages
5. Bot password 생성
6. `.env` 파일에 업데이트

```bash
MEDIAWIKI_BOT_USERNAME=admin@artistwiki
MEDIAWIKI_BOT_PASSWORD=generated-bot-password
```

### LocalSettings.php 커스터마이징

```php
# mediawiki/LocalSettings.php

# API 활성화
$wgEnableAPI = true;
$wgEnableWriteAPI = true;

# 업로드 허용
$wgEnableUploads = true;
$wgFileExtensions = array('png', 'gif', 'jpg', 'jpeg', 'webp');

# 한국어 설정
$wgLanguageCode = "ko";
```

## 트러블슈팅

### Backend가 시작되지 않음

```bash
# 로그 확인
docker-compose logs backend

# 일반적인 원인:
# 1. DATABASE_URL이 잘못됨
# 2. PostgreSQL이 준비되지 않음
# 3. 의존성 설치 실패

# 해결:
docker-compose restart backend
```

### Frontend 빌드 에러

```bash
# 캐시 삭제
rm -rf .next node_modules
npm install
npm run build
```

### MediaWiki 접속 불가

```bash
# MediaWiki 컨테이너 재시작
docker-compose restart mediawiki

# 초기화가 필요한 경우
docker-compose down -v
docker-compose up -d
# http://localhost:8080에서 초기 설정 진행
```

### Database 마이그레이션 실패

```bash
# 현재 상태 확인
alembic current

# 강제로 특정 버전으로 설정
alembic stamp head

# 처음부터 다시
alembic downgrade base
alembic upgrade head
```

## 성능 최적화

### Backend

- **N+1 쿼리 방지**: SQLAlchemy `joinedload` 사용
- **Caching**: Redis 추가 (추후)
- **비동기 처리**: AsyncIO 활용

### Frontend

- **Code Splitting**: Dynamic imports
- **Image Optimization**: Next.js Image component
- **SSR/SSG**: 적절히 활용

## 보안 체크리스트

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] API 키가 코드에 하드코딩되지 않았는지 확인
- [ ] CORS 설정이 적절한지 확인
- [ ] SQL Injection 방지 (ORM 사용)
- [ ] XSS 방지 (입력 검증)

## 유용한 명령어

```bash
# Docker 컨테이너 상태 확인
docker-compose ps

# 특정 서비스 로그만 보기
docker-compose logs -f backend

# 컨테이너 내부 접속
docker-compose exec backend bash
docker-compose exec postgres psql -U artistwiki_user -d artistwiki

# 디스크 공간 확보
docker system prune -a

# 의존성 업데이트
pip install --upgrade -r requirements.txt  # Backend
npm update  # Frontend
```
