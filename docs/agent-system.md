# Agent System 설계

## 개요

ArtistWiki의 Agent System은 오케스트레이터 패턴을 사용하여 여러 에이전트를 조율하고 자동화된 워크플로우를 실행합니다.

## 아키텍처

```
┌─────────────────────────────────────┐
│       Agent Orchestrator            │
│  - 워크플로우 조율                    │
│  - 에이전트 등록 관리                 │
│  - 작업 큐 관리                      │
│  - 에러 핸들링                       │
└────────┬────────────────────────────┘
         │
         ├──────────┬──────────┬────────────┐
         ▼          ▼          ▼            ▼
    ┌────────┐ ┌────────┐ ┌──────────┐ ┌────────┐
    │Crawler │ │Writer  │ │MediaWiki │ │Future  │
    │Agent   │ │Agent   │ │Agent     │ │Agents  │
    └────────┘ └────────┘ └──────────┘ └────────┘
```

## Base Agent Class

모든 에이전트는 `BaseAgent` 클래스를 상속받습니다.

### 인터페이스

```python
class BaseAgent(ABC):
    @abstractmethod
    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """에이전트 실행"""
        pass

    async def on_success(self, result: Dict[str, Any]) -> None:
        """성공 시 훅"""
        pass

    async def on_failure(self, error: Exception) -> None:
        """실패 시 훅"""
        pass

    async def validate_input(self, task_data: Dict[str, Any]) -> bool:
        """입력 검증"""
        pass
```

## Phase 1 Agents

### 1. Crawler Agent

**목적:** 외부 소스에서 작가 정보 수집

**입력:**
```python
{
    "url": "https://example.com/artist/name",
    "artist_name": "Pablo Picasso"
}
```

**출력:**
```python
{
    "name": "Pablo Picasso",
    "source_url": "https://example.com/artist/name",
    "raw_html": "...",
    "title": "Pablo Picasso - Biography",
    "extracted_data": {
        "birth_date": "1881-10-25",
        "death_date": "1973-04-08",
        "nationality": "Spanish"
    }
}
```

**구현:**
- httpx로 HTTP 요청
- BeautifulSoup로 HTML 파싱
- 구조화된 데이터 추출

### 2. Writer Agent

**목적:** AI로 위키 페이지 초안 생성

**입력:**
```python
{
    "artist_name": "Pablo Picasso",
    "artist_type": "painter",
    "source_data": {
        # Crawler Agent의 출력
    }
}
```

**출력:**
```python
{
    "artist_name": "Pablo Picasso",
    "wiki_content": "== Biography ==\n...",
    "format": "wikitext",
    "model": "gpt-4"
}
```

**구현:**
- OpenAI GPT-4 API 호출
- 위키텍스트 포맷팅
- 섹션 구조화 (Biography, Career, Works, Legacy)

### 3. MediaWiki Agent

**목적:** MediaWiki API를 통한 페이지 관리

**입력:**
```python
{
    "action": "create",  # or "edit", "delete"
    "page_title": "Pablo Picasso",
    "content": "== Biography ==\n..."
}
```

**출력:**
```python
{
    "page_title": "Pablo Picasso",
    "page_id": 12345,
    "status": "success"
}
```

**구현:**
- MediaWiki Bot 인증
- CSRF 토큰 관리
- API 호출 (action=edit, action=delete)
- 에러 핸들링

## Orchestrator

### 워크플로우 실행

```python
workflow = [
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

result = await orchestrator.execute_workflow(workflow, db)
```

### Context Passing

각 에이전트의 출력은 다음 에이전트의 입력으로 자동 전달됩니다.

```python
# Step 1: Crawler
context = {}
crawler_result = await crawler.execute({"url": "...", "artist_name": "..."})
context.update(crawler_result)  # source_data 추가

# Step 2: Writer
writer_task = {"artist_name": "...", "artist_type": "..."}
writer_task.update(context)  # source_data 포함
writer_result = await writer.execute(writer_task)
context.update(writer_result)  # wiki_content 추가

# Step 3: MediaWiki
mediawiki_task = {"action": "create", "page_title": "..."}
mediawiki_task.update(context)  # wiki_content 포함
mediawiki_result = await mediawiki.execute(mediawiki_task)
```

## Agent Job Tracking

모든 에이전트 실행은 `agent_jobs` 테이블에 기록됩니다.

```python
job = AgentJob(
    job_type="crawler",
    status="running",
    input_data={"url": "...", "artist_name": "..."},
    started_at=datetime.utcnow()
)
db.add(job)

# 에이전트 실행
result = await agent.execute(task_data)

# 성공 시
job.status = "success"
job.output_data = result
job.completed_at = datetime.utcnow()

# 실패 시
job.status = "failed"
job.error_message = str(error)
job.completed_at = datetime.utcnow()
```

## Error Handling

### Retry Logic

```python
async def execute_with_retry(
    agent: BaseAgent,
    task_data: Dict[str, Any],
    max_retries: int = 3
) -> Dict[str, Any]:
    for attempt in range(max_retries):
        try:
            return await agent.execute(task_data)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Failure Handling

워크플로우 중 하나의 에이전트가 실패하면:
1. 에러 로그 기록
2. 워크플로우 중단
3. 사용자에게 에러 메시지 반환
4. Rollback 가능한 경우 이전 상태로 복구

## Phase 2 Agents (예정)

### 4. Validator Agent

**목적:** 정보 정확성 검증

```python
{
    "artist_name": "Pablo Picasso",
    "wiki_content": "...",
    "checks": ["dates", "facts", "sources"]
}
```

### 5. Category Agent

**목적:** 자동 카테고리 분류

```python
{
    "artist_name": "Pablo Picasso",
    "artist_type": "painter",
    "content": "..."
}
→
{
    "categories": ["Spanish painters", "Cubism", "20th century artists"]
}
```

### 6. Image Agent

**목적:** 이미지 수집 및 최적화

```python
{
    "artist_name": "Pablo Picasso",
    "image_urls": ["..."]
}
→
{
    "processed_images": [
        {"url": "...", "thumbnail": "...", "license": "..."}
    ]
}
```

## Phase 3 Agents (예정)

### 7. Relationship Agent

**목적:** 작가 간 관계 분석

```python
{
    "artist_name": "Pablo Picasso",
    "content": "..."
}
→
{
    "relationships": [
        {"target": "Georges Braque", "type": "collaborator"},
        {"target": "Henri Matisse", "type": "rival"}
    ]
}
```

### 8. Recommendation Agent

**목적:** 유사 작가 추천

```python
{
    "artist_id": "uuid",
    "artist_type": "painter"
}
→
{
    "recommendations": [
        {"artist_id": "uuid", "similarity": 0.85, "reason": "..."}
    ]
}
```

## 성능 최적화

### Parallel Execution

독립적인 에이전트는 병렬 실행 가능:

```python
# 순차 실행 (기본)
await orchestrator.execute_workflow([agent1, agent2, agent3], db)

# 병렬 실행
results = await asyncio.gather(
    agent1.execute(task1),
    agent2.execute(task2),
    agent3.execute(task3)
)
```

### Caching

- Crawler 결과: 24시간 캐시
- Writer 결과: 재사용 불가 (항상 새로 생성)
- MediaWiki 조회: 1시간 캐시

## 모니터링

### Metrics

- 에이전트별 실행 횟수
- 평균 실행 시간
- 성공률/실패율
- 에러 타입별 통계

### Logging

```python
logger.info(f"Agent {self.name} started", extra={
    "agent_type": self.name,
    "task_data": task_data
})

logger.info(f"Agent {self.name} completed", extra={
    "agent_type": self.name,
    "duration": elapsed_time,
    "result": result
})
```

## 테스트

### Unit Tests

```python
@pytest.mark.asyncio
async def test_crawler_agent():
    agent = CrawlerAgent()
    result = await agent.execute({
        "url": "https://example.com/test",
        "artist_name": "Test Artist"
    })
    assert "name" in result
    assert result["name"] == "Test Artist"
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_workflow():
    workflow = [
        {"agent_type": "crawler", ...},
        {"agent_type": "writer", ...},
        {"agent_type": "mediawiki", ...}
    ]
    result = await orchestrator.execute_workflow(workflow, mock_db)
    assert result["status"] == "completed"
```
