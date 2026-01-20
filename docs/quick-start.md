# Quick Start Guide

ArtistWiki를 빠르게 시작하는 가이드입니다.

## 1. 환경 변수 설정

```bash
cd /Users/jinwooro/Desktop/Project/ArtistWiki

# 환경 변수 파일 복사
cp .env.example .env

# .env 파일 편집
# 필수 항목:
# - OPENAI_API_KEY: OpenAI API 키
# - MEDIAWIKI_BOT_USERNAME: MediaWiki Bot 사용자명 (초기: admin@artistwiki)
# - MEDIAWIKI_BOT_PASSWORD: MediaWiki Bot 비밀번호 (초기 설정 후 업데이트)
```

## 2. Docker Compose로 실행

```bash
# 전체 시스템 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

## 3. MediaWiki 초기 설정

1. 브라우저에서 http://localhost:8080 접속
2. 초기 설정 마법사 진행:
   - Database: PostgreSQL
   - Database host: mediawiki-db
   - Database name: mediawiki
   - Username: mediawiki
   - Password: mediawiki_password
   - Site name: ArtistWiki
   - Language: 한국어
   - Admin username: admin
   - Admin password: admin_password

3. 생성된 `LocalSettings.php` 파일을 다운로드
4. `mediawiki/LocalSettings.php`에 저장
5. MediaWiki 컨테이너 재시작:
   ```bash
   docker-compose restart mediawiki
   ```

## 4. MediaWiki Bot 설정

1. http://localhost:8080 접속
2. Admin 계정으로 로그인
3. **Special:BotPasswords** 페이지 이동
4. Bot 이름: `artistwiki`
5. 권한 선택:
   - ✅ High-volume editing
   - ✅ Edit existing pages
   - ✅ Create, edit, and move pages
6. **Create** 클릭
7. 생성된 Bot password를 `.env` 파일에 업데이트:
   ```bash
   MEDIAWIKI_BOT_USERNAME=admin@artistwiki
   MEDIAWIKI_BOT_PASSWORD=<생성된-bot-password>
   ```
8. Backend 재시작:
   ```bash
   docker-compose restart backend
   ```

## 5. 데이터베이스 마이그레이션

```bash
# Backend 컨테이너 접속
docker-compose exec backend bash

# 마이그레이션 실행
alembic upgrade head

# 종료
exit
```

## 6. 접속 확인

### Frontend
http://localhost:3000

### Backend API Docs
http://localhost:8000/docs

### MediaWiki
http://localhost:8080

## 7. 첫 작가 생성 (API 테스트)

### Option 1: Swagger UI 사용

1. http://localhost:8000/docs 접속
2. `POST /api/v1/artists` 엔드포인트 클릭
3. **Try it out** 클릭
4. Request body 입력:
   ```json
   {
     "name": "Pablo Picasso",
     "type": "painter",
     "birth_date": "1881-10-25",
     "death_date": "1973-04-08",
     "nationality": "Spanish",
     "biography": "Spanish painter, sculptor, printmaker..."
   }
   ```
5. **Execute** 클릭

### Option 2: curl 사용

```bash
curl -X POST "http://localhost:8000/api/v1/artists" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pablo Picasso",
    "type": "painter",
    "birth_date": "1881-10-25",
    "death_date": "1973-04-08",
    "nationality": "Spanish",
    "biography": "Spanish painter, sculptor, printmaker..."
  }'
```

## 8. Agent 워크플로우 테스트

작가 정보를 자동으로 수집하고 MediaWiki 페이지를 생성하는 전체 워크플로우 테스트:

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

결과 확인:
- MediaWiki에서 `Pablo_Picasso` 페이지가 생성되었는지 확인
- http://localhost:8080/wiki/Pablo_Picasso

## 트러블슈팅

### Backend가 시작되지 않음

```bash
# 로그 확인
docker-compose logs backend

# 재시작
docker-compose restart backend
```

### MediaWiki Bot 인증 실패

1. `.env` 파일의 Bot credentials 확인
2. MediaWiki에서 Bot password 재생성
3. Backend 재시작

### 데이터베이스 연결 실패

```bash
# PostgreSQL 상태 확인
docker-compose ps postgres

# PostgreSQL 재시작
docker-compose restart postgres

# 마이그레이션 재실행
docker-compose exec backend alembic upgrade head
```

## 다음 단계

- [Development Guide](./development-guide.md) - 로컬 개발 환경 설정
- [Architecture](./architecture.md) - 시스템 아키텍처 이해
- [Agent System](./agent-system.md) - 에이전트 시스템 상세
- [API Specs](./api-specs.md) - API 명세

## 중지 및 삭제

```bash
# 중지
docker-compose down

# 데이터 포함 완전 삭제 (주의!)
docker-compose down -v
```
