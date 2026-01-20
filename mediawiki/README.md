# MediaWiki Setup

## 로컬 개발 환경

1. Docker Compose 실행:
```bash
docker-compose up -d
```

2. MediaWiki 설치 마법사 접속:
- URL: http://localhost:5050/mw-config/index.php

3. 데이터베이스 설정:
- Database type: **MySQL**
- Database host: **database**
- Database name: **mediawiki**
- Database username: **mediawiki**
- Database password: **mediawiki_password**

4. LocalSettings.php 설정:
- 초기 설치 완료 후 LocalSettings.php 파일 다운로드
- 이 디렉토리에 저장
- docker-compose.yml에서 LocalSettings.php 마운트 주석 해제
- `docker-compose restart` 실행

## 프로덕션 환경 (Dokploy)

- MediaWiki: https://okidokiwiki.jrai.space
- 설치 후 Bot 계정 생성 및 권한 설정

## Bot 계정 설정

1. MediaWiki 관리자로 로그인
2. Special:BotPasswords 페이지 접속
3. 새 Bot 비밀번호 생성
4. Backend .env 파일에 Bot 정보 업데이트

## API 테스트

```bash
# 페이지 조회
curl "http://localhost:5050/api.php?action=query&titles=Main_Page&format=json"

# 검색
curl "http://localhost:5050/api.php?action=opensearch&search=artist&format=json"
```

## 중지

```bash
docker-compose down
```

## 데이터 초기화

```bash
docker-compose down -v
```
