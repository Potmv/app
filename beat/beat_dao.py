from datetime import datetime

import aiohttp

from beat.beat_model import Beat
from dao.base import BaseDAO
from database import async_session_maker


class BeatDAO(BaseDAO):
    __model__ = "Beats"
