from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache


from redis import asyncio as aioredis

app = FastAPI()

from pages.templates.router import template_router
from auth.router import auth_router
from beat.router import beats_router

app.include_router(template_router)
app.include_router(auth_router)
app.include_router(beats_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost:6379",
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
