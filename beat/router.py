import mimetypes
import uuid
import logging
from io import BytesIO
from PIL import Image
from fastapi_cache.decorator import cache

from beat.validating import UpBeatQueryParams

from aiohttp import ClientError
from fastapi.params import Depends

from beat.beat_dao import BeatDAO

from s3client import s3_client
from fastapi import APIRouter, UploadFile, File, HTTPException

beats_router = APIRouter(prefix="/beats")

logger = logging.getLogger(__name__)


@beats_router.get("/")
async def get_beats_with_filter(
    title: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    bpm: int | None = None,
    genre: str | None = None,
    musical_key: str | None = None,
):
    return await BeatDAO.get_beats(
        title=title,
        min_price=min_price,
        max_price=max_price,
        bpm=bpm,
        genre=genre,
        musical_key=musical_key,
    )


@beats_router.post("/upload_beat")
async def load_beat(
    query_params: UpBeatQueryParams = Depends(),
    beat_file: UploadFile = File(...),
    image_file: UploadFile = File(...),
):
    try:
        beat_bytes = await beat_file.read()
        image_bytes = await image_file.read()

        beat_key = f"{uuid.uuid4()}_{beat_file.filename}"
        image_key = f"{uuid.uuid4()}_{image_file.filename}"

        beat_mime = (
            mimetypes.guess_type(beat_file.filename)[0] or "application/octet-stream"
        )

        try:
            img = Image.open(BytesIO(image_bytes))

            if img.width != img.height:
                size = min(img.width, img.height)
                left = (img.width - size) // 2
                top = (img.height - size) // 2
                right = left + size
                bottom = top + size

                img = img.crop((left, top, right, bottom))

            output_buffer = BytesIO()
            img.save(output_buffer, format="webp", quality=90)
            processed_image_bytes = output_buffer.getvalue()
            image_mime = "image/jpeg"
        except Exception as img_error:
            logger.warning(f"Image processing failed, using original: {img_error}")
            processed_image_bytes = image_bytes
            image_mime = (
                mimetypes.guess_type(image_file.filename)[0]
                or "application/octet-stream"
            )

        beat_url = await s3_client.upload_bytes(beat_bytes, beat_key, beat_mime)
        cover_url = await s3_client.upload_bytes(
            processed_image_bytes, image_key, image_mime
        )

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

        return {"result": "uploaded"}

    except ClientError as e:
        logger.error(f"S3 upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=422, detail="File upload failed")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
