from datetime import datetime
from sqlalchemy import insert, select, and_, func
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from models.models import Beat
from dao.base import BaseDAO
from database import async_session_maker


class BeatDAO(BaseDAO):
    __model__ = "Beats"

    @staticmethod
    async def add_in_beats(
        title,
        description,
        price,
        bpm,
        genre,
        musical_key,
        file_url,
        cover_url,
    ):
        try:
            async with async_session_maker() as session:
                query = insert(Beat).values(
                    title=title,
                    description=description,
                    price=price,
                    bpm=bpm,
                    genre=genre,
                    musical_key=musical_key,
                    file_url=file_url,
                    cover_url=cover_url,
                    created_at=datetime.now(),
                )
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_beats(
        title=None,
        min_price=None,
        max_price=None,
        bpm=None,
        genre=None,
        musical_key=None,
    ):
        query = select(Beat)
        conditions = []

        if title:
            conditions.append(func.lower(Beat.title).contains(func.lower(title)))
        if min_price is not None:
            conditions.append(Beat.price >= min_price)
        if max_price is not None:
            conditions.append(Beat.price <= max_price)
        if bpm is not None:
            conditions.append(Beat.bpm == bpm)
        if genre:
            conditions.append(Beat.genre == genre)
        if musical_key:
            conditions.append(Beat.musical_key == musical_key)

        if conditions:
            query = query.where(and_(*conditions))
        try:
            async with async_session_maker() as session:
                result = await session.execute(query)
                return result.scalars().unique().all()
        except SQLAlchemyError as e:
            async with async_session_maker() as session:
                await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
