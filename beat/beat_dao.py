from datetime import datetime
from sqlalchemy import insert
import aiohttp
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from beat.beat_model import Beat
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
                query = insert(Beat).values(title=title, description=description, price=price, bpm=bpm, genre=genre, musical_key=musical_key, file_url=file_url, cover_url=cover_url, created_at=datetime.now())
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            raise HTTPException(status_code=500, detail=str(e))