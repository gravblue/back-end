import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    
    HUGGINGFACE_EMOTION_API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    
    APP_TITLE = "AI Mood-Based Music Recommender"
    APP_VERSION = "2.0.0"
    
    CORS_ORIGINS = ["*"]
    
    MAX_RECOMMENDATIONS = 10
    MIN_RECOMMENDATIONS = 1
    
    SUPPORTED_EMOTIONS = [
        "sadness", "joy", "anger", "fear", "love", "surprise", "neutral"
    ]

config = Config()
