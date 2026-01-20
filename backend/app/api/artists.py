"""
Artists API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.models.artist import Artist
from app.schemas.artist import ArtistCreate, ArtistUpdate, ArtistResponse

router = APIRouter()


@router.get("/", response_model=dict)
async def get_artists(
    type: Optional[str] = Query(None, pattern="^(painter|writer|musician)$"),
    search: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """작가 목록 조회"""
    query = select(Artist)

    # 필터링
    if type:
        query = query.filter(Artist.type == type)
    if search:
        query = query.filter(Artist.name.ilike(f"%{search}%"))

    # 총 개수
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # 페이지네이션
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    artists = result.scalars().all()

    return {
        "items": artists,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(
    artist_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """작가 상세 조회"""
    result = await db.execute(
        select(Artist).filter(Artist.id == artist_id)
    )
    artist = result.scalar_one_or_none()

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    return artist


@router.post("/", response_model=ArtistResponse, status_code=201)
async def create_artist(
    artist_in: ArtistCreate,
    db: AsyncSession = Depends(get_db)
):
    """작가 생성"""
    artist = Artist(**artist_in.model_dump())
    db.add(artist)
    await db.commit()
    await db.refresh(artist)
    return artist


@router.put("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: UUID,
    artist_in: ArtistUpdate,
    db: AsyncSession = Depends(get_db)
):
    """작가 정보 수정"""
    result = await db.execute(
        select(Artist).filter(Artist.id == artist_id)
    )
    artist = result.scalar_one_or_none()

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    # 업데이트
    update_data = artist_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(artist, field, value)

    await db.commit()
    await db.refresh(artist)
    return artist


@router.delete("/{artist_id}")
async def delete_artist(
    artist_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """작가 삭제"""
    result = await db.execute(
        select(Artist).filter(Artist.id == artist_id)
    )
    artist = result.scalar_one_or_none()

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    await db.delete(artist)
    await db.commit()

    return {"message": "Artist deleted successfully"}
