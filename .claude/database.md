# ArtistWiki Database Configuration

## PostgreSQL Connection Info

### SSH Tunnel Setup
모든 DB 접근은 SSH 터널링을 통해 이루어집니다:

```bash
ssh -L 15432:127.0.0.1:5432 \
  -L 15433:127.0.0.1:5433 \
  -L 15434:127.0.0.1:5434 \
  -L 15435:127.0.0.1:5435 \
  -L 15436:127.0.0.1:5436 \
  dokploy.jrai.space
```

### ArtistWiki Database (예정)

**Connection via SSH Tunnel:**
- **Host**: `localhost`
- **Port**: `15436` (로컬 터널 포트)
- **Database**: `artistwiki`
- **User**: `artistwiki_user`
- **Password**: `[생성 후 업데이트]`

**Direct Connection (Dokploy):**
- **Host**: `dokploy.jrai.space`
- **Port**: `5436` (리모트 포트)
- **Database**: `artistwiki`
- **User**: `artistwiki_user`

### Connection String

```bash
# Local (via SSH tunnel)
postgresql://artistwiki_user:[password]@localhost:15436/artistwiki

# Remote (direct)
postgresql://artistwiki_user:[password]@dokploy.jrai.space:5436/artistwiki
```

### MCP PostgreSQL Tool Usage

```python
# Read-only query
mcp__postgres__query(
    sql="SELECT * FROM artists LIMIT 10"
)
```

---

## Database Schema

### Artists Table
```sql
CREATE TABLE artists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('painter', 'writer', 'musician')),
    birth_date DATE,
    death_date DATE,
    nationality VARCHAR(100),
    biography TEXT,
    mediawiki_page_id INTEGER UNIQUE,
    mediawiki_page_title VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_artists_type ON artists(type);
CREATE INDEX idx_artists_name ON artists(name);
CREATE INDEX idx_artists_mediawiki_page_id ON artists(mediawiki_page_id);
```

### Works Table
```sql
CREATE TABLE works (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    year INTEGER,
    type VARCHAR(100),
    description TEXT,
    mediawiki_page_id INTEGER UNIQUE,
    mediawiki_page_title VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_works_artist_id ON works(artist_id);
CREATE INDEX idx_works_year ON works(year);
CREATE INDEX idx_works_mediawiki_page_id ON works(mediawiki_page_id);
```

### Agent Jobs Table
```sql
CREATE TABLE agent_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'running', 'success', 'failed')),
    target_id UUID,
    target_type VARCHAR(50),
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agent_jobs_status ON agent_jobs(status);
CREATE INDEX idx_agent_jobs_job_type ON agent_jobs(job_type);
CREATE INDEX idx_agent_jobs_target_id ON agent_jobs(target_id);
```

### Relationships Table
```sql
CREATE TABLE relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
    target_artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
    relationship_type VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_artist_id, target_artist_id, relationship_type)
);

CREATE INDEX idx_relationships_source ON relationships(source_artist_id);
CREATE INDEX idx_relationships_target ON relationships(target_artist_id);
```

---

## Status

- [ ] Dokploy에서 PostgreSQL 생성
- [ ] 데이터베이스 및 유저 생성
- [ ] 스키마 초기화
- [ ] SSH 터널 포트 할당 (15436)
- [ ] 접속 정보 업데이트

---

## Notes

- PostgreSQL 버전: 17
- 타임존: UTC
- 인코딩: UTF-8
- Read-only 쿼리는 MCP 도구 사용
- Write 작업은 Backend API를 통해서만 수행
