from typing import Literal

from pydantic import BaseModel

MusicalKeyType = Literal[
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]

PriceType = Literal[30, 50, 60, None]


class UpBeatQueryParams(BaseModel):
    title: str
    description: str
    price: int
    bpm: int
    genre: str
    musical_key: MusicalKeyType
