from typing import Optional
from pydantic import BaseModel


class ConstructQueryInput(BaseModel):
    track: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None


class SpotifySearchResult(BaseModel):
    track_name: str
    artist: str
    album_image: str
    id: str
