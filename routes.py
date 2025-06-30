from fastapi import APIRouter, HTTPException, Query
from models import (
    EmotionRequest, 
    EmotionResponse, 
    RecommendationResponse, 
    AnalyzeAndRecommendResponse
)
from emotion_detector import detect_emotion_from_text
from spotify_service import search_songs_by_playlist_ids
from config import config

router = APIRouter()

@router.post("/detect-emotion", response_model=EmotionResponse)
def detect_emotion(data: EmotionRequest):
    try:
        emotion = detect_emotion_from_text(data.text)
        return EmotionResponse(emotion=emotion, keyword=emotion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting emotion: {str(e)}")

@router.get("/recommend-from-playlists", response_model=RecommendationResponse)
def recommend_from_playlists(
    emotion: str = Query(...),
    limit: int = Query(5, ge=config.MIN_RECOMMENDATIONS, le=config.MAX_RECOMMENDATIONS),
):
    try:
        tracks = search_songs_by_playlist_ids(emotion, limit)
        message = f"Found {len(tracks)} songs from predefined playlists" if tracks else f"No tracks found from playlists for emotion: {emotion}"
        return RecommendationResponse(tracks=tracks, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting playlist recommendations: {str(e)}")

@router.post("/analyze-and-recommend", response_model=AnalyzeAndRecommendResponse)
def analyze_and_recommend(
    data: EmotionRequest,
    limit: int = Query(5, ge=config.MIN_RECOMMENDATIONS, le=config.MAX_RECOMMENDATIONS)
):
    try:
        emotion = detect_emotion_from_text(data.text)
        tracks = search_songs_by_playlist_ids(emotion, limit)
        message = f"Found {len(tracks)} songs" if tracks else f"No tracks found for emotion: {emotion}"
        return AnalyzeAndRecommendResponse(emotion=emotion, keyword=emotion, tracks=tracks, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")