"""
ArtistWiki Backend - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="ArtistWiki API",
    description="작가/예술가 위키 시스템 - AI 에이전트 오케스트레이션",
    version="0.1.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "ArtistWiki API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


# API 라우터 등록
from app.api import artists, works, agents

app.include_router(artists.router, prefix="/api/v1/artists", tags=["artists"])
app.include_router(works.router, prefix="/api/v1/works", tags=["works"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
