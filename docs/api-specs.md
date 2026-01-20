# API Specifications

## Base URL

```
Development: http://localhost:8000
Production: https://api.artistwiki.com
```

## Authentication

```http
Authorization: Bearer <jwt_token>
```

---

## Artists API

### GET /api/v1/artists

작가 목록 조회

**Query Parameters:**
- `type` (optional): painter, writer, musician
- `search` (optional): 검색어
- `limit` (optional, default: 20): 페이지 크기
- `offset` (optional, default: 0): 오프셋

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Pablo Picasso",
      "type": "painter",
      "birth_date": "1881-10-25",
      "death_date": "1973-04-08",
      "nationality": "Spanish",
      "biography": "...",
      "mediawiki_page_id": 12345,
      "mediawiki_page_title": "Pablo_Picasso",
      "created_at": "2024-01-20T10:00:00Z",
      "updated_at": "2024-01-20T10:00:00Z"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

### GET /api/v1/artists/{artist_id}

작가 상세 조회

**Response:**
```json
{
  "id": "uuid",
  "name": "Pablo Picasso",
  "type": "painter",
  "birth_date": "1881-10-25",
  "death_date": "1973-04-08",
  "nationality": "Spanish",
  "biography": "...",
  "mediawiki_page_id": 12345,
  "mediawiki_page_title": "Pablo_Picasso",
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-20T10:00:00Z"
}
```

### POST /api/v1/artists

작가 생성

**Request Body:**
```json
{
  "name": "Pablo Picasso",
  "type": "painter",
  "birth_date": "1881-10-25",
  "death_date": "1973-04-08",
  "nationality": "Spanish",
  "biography": "..."
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Pablo Picasso",
  ...
}
```

### PUT /api/v1/artists/{artist_id}

작가 정보 수정

**Request Body:**
```json
{
  "name": "Pablo Picasso",
  "biography": "Updated biography..."
}
```

### DELETE /api/v1/artists/{artist_id}

작가 삭제

**Response:**
```json
{
  "message": "Artist deleted successfully"
}
```

---

## Works API

### GET /api/v1/works

작품 목록 조회

**Query Parameters:**
- `artist_id` (optional): 작가 ID
- `year` (optional): 제작 연도
- `limit` (optional, default: 20)
- `offset` (optional, default: 0)

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "artist_id": "uuid",
      "title": "Guernica",
      "year": 1937,
      "type": "Oil on canvas",
      "description": "...",
      "mediawiki_page_id": 67890,
      "mediawiki_page_title": "Guernica_(Picasso)",
      "created_at": "2024-01-20T10:00:00Z",
      "updated_at": "2024-01-20T10:00:00Z"
    }
  ],
  "total": 50,
  "limit": 20,
  "offset": 0
}
```

### GET /api/v1/works/{work_id}

작품 상세 조회

### POST /api/v1/works

작품 생성

**Request Body:**
```json
{
  "artist_id": "uuid",
  "title": "Guernica",
  "year": 1937,
  "type": "Oil on canvas",
  "description": "..."
}
```

### PUT /api/v1/works/{work_id}

작품 정보 수정

### DELETE /api/v1/works/{work_id}

작품 삭제

---

## Agent Jobs API

### POST /api/v1/agents/jobs

에이전트 작업 생성 및 실행

**Request Body:**
```json
{
  "workflow": [
    {
      "agent_type": "crawler",
      "task_data": {
        "url": "https://example.com/artist/picasso",
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
        "page_title": "Pablo Picasso"
      }
    }
  ]
}
```

**Response:**
```json
{
  "status": "completed",
  "results": [
    {
      "status": "success",
      "job_id": "uuid",
      "output": {...}
    },
    {
      "status": "success",
      "job_id": "uuid",
      "output": {...}
    },
    {
      "status": "success",
      "job_id": "uuid",
      "output": {...}
    }
  ],
  "context": {...}
}
```

### GET /api/v1/agents/jobs

에이전트 작업 목록 조회

**Query Parameters:**
- `status` (optional): pending, running, success, failed
- `job_type` (optional): crawler, writer, mediawiki
- `limit` (optional, default: 20)
- `offset` (optional, default: 0)

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "job_type": "crawler",
      "status": "success",
      "target_id": "uuid",
      "target_type": "artist",
      "input_data": {...},
      "output_data": {...},
      "error_message": null,
      "started_at": "2024-01-20T10:00:00Z",
      "completed_at": "2024-01-20T10:01:00Z",
      "created_at": "2024-01-20T10:00:00Z"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

### GET /api/v1/agents/jobs/{job_id}

에이전트 작업 상세 조회

---

## Relationships API

### GET /api/v1/relationships

관계 목록 조회

**Query Parameters:**
- `artist_id` (optional): 작가 ID
- `relationship_type` (optional): collaborator, teacher, student, etc.

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "source_artist_id": "uuid",
      "target_artist_id": "uuid",
      "relationship_type": "collaborator",
      "description": "Collaborated on Cubism movement",
      "created_at": "2024-01-20T10:00:00Z"
    }
  ],
  "total": 10
}
```

### POST /api/v1/relationships

관계 생성

**Request Body:**
```json
{
  "source_artist_id": "uuid",
  "target_artist_id": "uuid",
  "relationship_type": "collaborator",
  "description": "Collaborated on Cubism movement"
}
```

### DELETE /api/v1/relationships/{relationship_id}

관계 삭제

---

## MediaWiki Integration API

### GET /api/v1/mediawiki/pages/{page_title}

MediaWiki 페이지 조회

**Response:**
```json
{
  "page_title": "Pablo_Picasso",
  "page_id": 12345,
  "content": "== Biography ==\n...",
  "exists": true
}
```

### POST /api/v1/mediawiki/pages

MediaWiki 페이지 생성/수정

**Request Body:**
```json
{
  "page_title": "Pablo_Picasso",
  "content": "== Biography ==\n...",
  "action": "create"
}
```

**Response:**
```json
{
  "page_title": "Pablo_Picasso",
  "page_id": 12345,
  "status": "success"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "name",
      "message": "Name is required"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Artist not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error": "..."
}
```

---

## Rate Limiting

- **Authenticated users**: 100 requests/minute
- **Anonymous users**: 20 requests/minute

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## Pagination

모든 리스트 API는 페이지네이션을 지원합니다.

**Query Parameters:**
- `limit`: 페이지 크기 (max: 100)
- `offset`: 시작 위치

**Response Headers:**
```
X-Total-Count: 1000
Link: </api/v1/artists?limit=20&offset=20>; rel="next"
```
