from pydantic import BaseModel
from typing import List, Optional

class EmotionRequest(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    emotion: str
    keyword: str

class Track(BaseModel):
    title: str
    artist: str
    url: str
    preview_url: Optional[str] = None
    album_art: Optional[str] = None

class RecommendationResponse(BaseModel):
    tracks: List[Track]
    message: Optional[str] = None

class AnalyzeAndRecommendResponse(BaseModel):
    emotion: str
    keyword: str
    tracks: List[Track]
    message: Optional[str] = None