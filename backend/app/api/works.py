"""
Works API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.models.work import Work
from app.schemas.work import WorkCreate, WorkUpdate, WorkResponse

router = APIRouter()


@router.get("/", response_model=dict)
async def get_works(
    artist_id: Optional[UUID] = None,
    year: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """작품 목록 조회"""
    query = select(Work)

    # 필터링
    if artist_id:
        query = query.filter(Work.artist_id == artist_id)
    if year:
        query = query.filter(Work.year == year)

    # 총 개수
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # 페이지네이션
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    works = result.scalars().all()

    return {
        "items": works,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/{work_id}", response_model=WorkResponse)
async def get_work(
    work_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """작품 상세 조회"""
    result = await db.execute(
        select(Work).filter(Work.id == work_id)
    )
    work = result.scalar_one_or_none()

    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    return work


@router.post("/", response_model=WorkResponse, status_code=201)
async def create_work(
    work_in: WorkCreate,
    db: AsyncSession = Depends(get_db)
):
    """작품 생성"""
    work = Work(**work_in.model_dump())
    db.add(work)
    await db.commit()
    await db.refresh(work)
    return work


@router.put("/{work_id}", response_model=WorkResponse)
async def update_work(
    work_id: UUID,
    work_in: WorkUpdate,
    db: AsyncSession = Depends(get_db)
):
    """작품 정보 수정"""
    result = await db.execute(
        select(Work).filter(Work.id == work_id)
    )
    work = result.scalar_one_or_none()

    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    # 업데이트
    update_data = work_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(work, field, value)

    await db.commit()
    await db.refresh(work)
    return work


@router.delete("/{work_id}")
async def delete_work(
    work_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """작품 삭제"""
    result = await db.execute(
        select(Work).filter(Work.id == work_id)
    )
    work = result.scalar_one_or_none()

    if not work:
        raise HTTPException(status_code=404, detail="Work not found")

    await db.delete(work)
    await db.commit()

    return {"message": "Work deleted successfully"}
