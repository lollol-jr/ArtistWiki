# Dokploy Deployment Guide

ArtistWiki를 Dokploy에 배포하는 가이드입니다.

## 사전 준비

- ✅ Dokploy 프로젝트 생성 완료 (Project ID: `4KLOWWEr8EUL-zkKExSEC`)
- GitHub 저장소 생성 및 코드 푸시 필요
- 환경 변수 준비

## 1. GitHub 저장소 생성

```bash
# GitHub에서 새 저장소 생성
# Repository name: ArtistWiki

# 로컬에서 remote 추가
cd /Users/jinwooro/Desktop/Project/ArtistWiki
git remote add origin https://github.com/<username>/ArtistWiki.git

# Push
git push -u origin main
```

## 2. PostgreSQL 데이터베이스 생성

Dokploy에서:
1. **Projects** → **ArtistWiki** → **production** 환경
2. **Add Service** → **PostgreSQL**
3. 설정:
   - Name: `artistwiki-postgres`
   - Database: `artistwiki`
   - Username: `artistwiki_user`
   - Password: 강력한 비밀번호 생성
   - PostgreSQL Version: **17**
   - Port: **5436** (외부 포트)

4. **Create** 클릭
5. 생성 완료 후 **Deploy** 클릭

## 3. Backend 배포

### 3.1 Application 생성

1. **Add Service** → **Application**
2. 설정:
   - Name: `artistwiki-backend`
   - Source: **GitHub**
   - Repository: `<username>/ArtistWiki`
   - Branch: `main`
   - Build Type: **Dockerfile**
   - Dockerfile Path: `backend/Dockerfile`
   - Context Path: `backend`

### 3.2 환경 변수 설정

**Environment Variables:**
```bash
DATABASE_URL=postgresql://artistwiki_user:<password>@artistwiki-postgres:5432/artistwiki
MEDIAWIKI_API_URL=http://artistwiki-mediawiki/api.php
MEDIAWIKI_BOT_USERNAME=admin@artistwiki
MEDIAWIKI_BOT_PASSWORD=<bot-password>
OPENAI_API_KEY=<openai-key>
ANTHROPIC_API_KEY=<anthropic-key>
SECRET_KEY=<random-secret-key>
DEBUG=False
ENVIRONMENT=production
ALLOWED_ORIGINS=https://artistwiki.jrai.space,https://wiki.artistwiki.jrai.space
HOST=0.0.0.0
PORT=8000
```

### 3.3 도메인 설정

1. **Domains** 섹션
2. **Add Domain**
3. Host: `api.artistwiki.jrai.space` (또는 원하는 도메인)
4. HTTPS: ✅ (Let's Encrypt)
5. Port: `8000`

### 3.4 배포

**Deploy** 클릭

## 4. MediaWiki 배포

### 4.1 PostgreSQL (MediaWiki용) 생성

1. **Add Service** → **PostgreSQL**
2. 설정:
   - Name: `mediawiki-postgres`
   - Database: `mediawiki`
   - Username: `mediawiki`
   - Password: 강력한 비밀번호
   - PostgreSQL Version: **17**

### 4.2 MediaWiki Application 생성

1. **Add Service** → **Compose**
2. 설정:
   - Name: `artistwiki-mediawiki`
   - Source Type: **Raw**

3. **Docker Compose 내용:**
```yaml
version: '3.8'

services:
  mediawiki:
    image: mediawiki:1.45
    restart: always
    environment:
      - MEDIAWIKI_DB_TYPE=postgres
      - MEDIAWIKI_DB_HOST=mediawiki-postgres
      - MEDIAWIKI_DB_NAME=mediawiki
      - MEDIAWIKI_DB_USER=mediawiki
      - MEDIAWIKI_DB_PASSWORD=${MEDIAWIKI_DB_PASSWORD}
      - MEDIAWIKI_SITE_NAME=ArtistWiki
      - MEDIAWIKI_SITE_LANG=ko
      - MEDIAWIKI_ADMIN_USER=admin
      - MEDIAWIKI_ADMIN_PASS=${MEDIAWIKI_ADMIN_PASS}
    volumes:
      - mediawiki_images:/var/www/html/images

volumes:
  mediawiki_images:
```

4. **Environment Variables:**
```bash
MEDIAWIKI_DB_PASSWORD=<mediawiki-postgres-password>
MEDIAWIKI_ADMIN_PASS=<admin-password>
```

### 4.3 도메인 설정

1. **Add Domain**
2. Host: `wiki.artistwiki.jrai.space`
3. HTTPS: ✅
4. Port: `80`

### 4.4 배포 및 초기 설정

1. **Deploy** 클릭
2. `wiki.artistwiki.jrai.space` 접속
3. MediaWiki 초기 설정 완료
4. **LocalSettings.php** 다운로드
5. Dokploy에서 파일 업로드 또는 환경 변수로 추가

### 4.5 Bot 계정 설정

1. Admin으로 로그인
2. **Special:BotPasswords**
3. Bot 생성 후 password를 Backend 환경 변수에 업데이트

## 5. Frontend 배포 (Optional - Vercel 추천)

### Option A: Vercel 배포 (추천)

1. Vercel 프로젝트 생성
2. GitHub 저장소 연결
3. Root Directory: `frontend`
4. Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://api.artistwiki.jrai.space
   NEXT_PUBLIC_MEDIAWIKI_URL=https://wiki.artistwiki.jrai.space
   ```
5. Deploy

### Option B: Dokploy 배포

1. **Add Service** → **Application**
2. 설정:
   - Name: `artistwiki-frontend`
   - Source: GitHub
   - Repository: `<username>/ArtistWiki`
   - Branch: `main`
   - Build Type: **Dockerfile**
   - Dockerfile Path: `frontend/Dockerfile`
   - Context Path: `frontend`

3. Environment Variables:
   ```bash
   NEXT_PUBLIC_API_URL=https://api.artistwiki.jrai.space
   NEXT_PUBLIC_MEDIAWIKI_URL=https://wiki.artistwiki.jrai.space
   ```

4. Domain: `artistwiki.jrai.space`
5. Deploy

## 6. 배포 후 확인

### 6.1 서비스 상태 확인

Dokploy에서 각 서비스의 상태가 **Running**인지 확인

### 6.2 데이터베이스 마이그레이션

```bash
# Backend 컨테이너 접속
# Dokploy 대시보드 → artistwiki-backend → Terminal

alembic upgrade head
```

### 6.3 API 테스트

```bash
curl https://api.artistwiki.jrai.space/health
```

Expected:
```json
{"status": "healthy"}
```

### 6.4 MediaWiki 테스트

브라우저에서 `https://wiki.artistwiki.jrai.space` 접속

### 6.5 Frontend 테스트

브라우저에서 `https://artistwiki.jrai.space` 접속

## 7. SSH 터널 설정 (로컬 접속용)

로컬에서 Dokploy PostgreSQL에 접속하려면:

```bash
ssh -L 15436:127.0.0.1:5436 dokploy.jrai.space

# 연결 확인
psql postgresql://artistwiki_user:<password>@localhost:15436/artistwiki
```

## 8. 자동 배포 설정

### GitHub Webhook

Dokploy는 자동으로 GitHub webhook을 설정합니다.

**자동 배포 동작:**
- `main` 브랜치에 push → 자동 배포
- Pull Request 머지 → 자동 배포

### 수동 배포

Dokploy 대시보드에서 **Redeploy** 클릭

## 9. 모니터링

### Logs

Dokploy 대시보드 → 서비스 선택 → **Logs**

### Metrics

각 서비스의 CPU, Memory 사용량 모니터링

## 10. 백업

### 데이터베이스 백업

```bash
# Dokploy 대시보드에서 PostgreSQL 서비스 선택
# Backup 탭에서 백업 설정
```

또는 수동 백업:

```bash
# SSH 접속
ssh dokploy.jrai.space

# 백업
docker exec artistwiki-postgres pg_dump -U artistwiki_user artistwiki > backup.sql

# 복원
cat backup.sql | docker exec -i artistwiki-postgres psql -U artistwiki_user artistwiki
```

## 트러블슈팅

### 배포 실패

1. Dokploy 로그 확인
2. Dockerfile 경로 확인
3. 환경 변수 확인

### 데이터베이스 연결 실패

1. PostgreSQL 서비스 상태 확인
2. `DATABASE_URL` 환경 변수 확인
3. 네트워크 연결 확인

### MediaWiki 접속 불가

1. MediaWiki 서비스 로그 확인
2. PostgreSQL (MediaWiki용) 상태 확인
3. 도메인 설정 확인

## 보안 체크리스트

- [ ] 모든 비밀번호가 강력한지 확인
- [ ] HTTPS 활성화 확인
- [ ] 환경 변수에 민감한 정보가 없는지 확인
- [ ] CORS 설정 확인
- [ ] Rate Limiting 설정 (추후)
- [ ] 정기 백업 설정

## 다음 단계

- CI/CD 파이프라인 구축
- 모니터링 및 알림 설정
- 성능 최적화
- 스케일링 전략
