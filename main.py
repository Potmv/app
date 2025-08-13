from fastapi import FastAPI

app = FastAPI()

from auth.router import auth_router
from beat.router import beats_router

app.include_router(auth_router)
app.include_router(beats_router)