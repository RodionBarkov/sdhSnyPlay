from pydantic import BaseModel
from typing import Optional

class STracksAdd(BaseModel):
    name: str
    description: Optional[str] = None
    cover_url: Optional[str] = None
    audio_url: str
    lyrics: Optional[str] = None

class STracks(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    cover_url: Optional[str] = None
    audio_url: str
    lyrics: Optional[str] = None


    class Config:
        from_attributes = True