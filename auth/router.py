import aiohttp
from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
from typing import Annotated

from auth.oauth_google import generate_google_oauth_redirect_uri
from config import settings

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/google/url")
def get_google_oauth_redirect_url():
    uri = generate_google_oauth_redirect_uri()
    return RedirectResponse(url=uri, status_code=302)

@auth_router.post("/google/callback")
async def handle_code(
        code: Annotated[str, Body(embed=True)],
):
    google_token_url = "https://oauth2.googleapis.com/token"

    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=google_token_url,
                data={
                    "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
                    "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "code": code,
                },
            ssl=False,
        ) as response:
            res = await response.json()
            print(f"{res=}")