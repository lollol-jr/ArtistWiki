# MediaWiki Setup

## 시작하기

1. Docker Compose 실행:
```bash
docker-compose up -d
```

2. MediaWiki 접속:
- URL: http://localhost:5050
- Admin 계정: admin / admin_password

3. LocalSettings.php 설정:
- 초기 설치 후 생성된 LocalSettings.php 파일을 이 디렉토리에 복사
- Bot 계정 생성 및 권한 설정

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
