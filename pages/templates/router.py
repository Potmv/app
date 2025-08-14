from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from beat.router import get_beats_with_filter

template_router = APIRouter(
    prefix="/pages",
    tags=["frontend"],
)

templates = Jinja2Templates(directory="pages/templates")


@template_router.get("/beats_page")
async def get_beats_pages(request: Request, beats=Depends(get_beats_with_filter)):
    return templates.TemplateResponse(
        "beats.html",
        {
            "request": request,
            "beats": beats,
        },
    )
