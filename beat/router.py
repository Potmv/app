import uuid
import logging

from typing import Literal

from aiohttp import ClientError
from fastapi.params import Depends
from pydantic import BaseModel

from beat.beat_dao import BeatDAO

from s3client import s3_client
from fastapi import APIRouter, UploadFile, File, HTTPException

beats_router = APIRouter(prefix="/beats")

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
    query_params: BeatQueryParams = Depends(),
    beat_file: UploadFile = File(...),
    image_file: UploadFile = File(...),
):
    beat_bytes = await beat_file.read()
    image_bytes = await image_file.read()

    beat_key = f"{uuid.uuid4()}_{beat_file.filename}"
    image_key = f"{uuid.uuid4()}_{image_file.filename}"
    try:
        beat_url = await s3_client.upload_bytes(beat_bytes, beat_key, "audio/mpeg")
        cover_url = await s3_client.upload_bytes(image_bytes, image_key, "image/jpeg")
        await BeatDAO.add_in_beats(
            title=query_params.title,
            description=query_params.description,
            price=query_params.price,
            bpm=query_params.bpm,
            genre=query_params.genre,
            musical_key=query_params.musical_key,
            file_url=beat_url,
            cover_url=cover_url,
        )
    except ClientError as e:
        logger.error(f"Failed to upload beat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(e))
