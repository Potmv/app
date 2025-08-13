import mimetypes
import uuid
from datetime import datetime
from typing import Literal

from aiohttp import ClientError
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from beat.beat_dao import BeatDAO
from config import settings
from database import async_session_maker
from s3.s3client import S3Client
from fastapi import APIRouter, UploadFile, File, HTTPException

beats_router = APIRouter(prefix="/beats")
import logging
s3_client = S3Client(
        access_key=settings.ACCESS_KEY,
        secret_key=settings.SECRET_KEY,
        endpoint_url=settings.ENDPOINT_URL,
        bucket_name=settings.BUCKET_NAME,
    )

PriceType = Literal[30, 50, 60]
logger = logging.getLogger(__name__)
MusicalKeyType = Literal[
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]
class BeatQueryParams(BaseModel):
    title: str
    description: str
    price: int
    bpm: int
    genre: str
    musical_key: MusicalKeyType

@beats_router.post("/upload_beat")
async def load_beat(
    query_params: BeatQueryParams = Depends(),  # FastAPI сам распарсит query-строку
    beat_file: UploadFile = File(...),
    image_file: UploadFile = File(...),
    ):
    beat_bytes = await beat_file.read()
    image_bytes = await image_file.read()

    beat_key = f"{uuid.uuid4()}_{beat_file.filename}"
    image_key = f"{uuid.uuid4()}_{image_file.filename}"
    try:
        beat_url = await s3_client.upload_bytes(beat_bytes, beat_key, "audio/mpeg")
        image_url = await s3_client.upload_bytes(image_bytes, image_key, "image/jpeg")
        try:
            query = insert("Beats").values(title=query_params.title, description=query_params.description, price=query_params.price, bpm=query_params.bpm, genre=query_params.genre,
                              musical_key=query_params.musical_key, file_url=beat_url, cover_url=image_url, created_at=datetime.now())
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"
            raise HTTPException(status_code=500, detail=msg)
    except ClientError as e:
        logger.error(f"Failed to upload beat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(e))