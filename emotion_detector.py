import requests
from deep_translator import GoogleTranslator
from config import config

huggingface_auth_success = False

def test_huggingface_auth():
    global huggingface_auth_success
    
    if not config.HUGGINGFACE_API_KEY:
        return False

    headers = {"Authorization": f"Bearer {config.HUGGINGFACE_API_KEY}"}
    try:
        response = requests.post(
            config.HUGGINGFACE_EMOTION_API_URL, 
            headers=headers, 
            json={"inputs": "Hello world"})
        
        if response.status_code == 200:
            huggingface_auth_success = True
            return True
        return False
    except Exception:
        return False

def translate_to_english(text):
    try:
        translator = GoogleTranslator(source='auto', target='en')
        return translator.translate(text)
    except Exception:
        return text

def detect_emotion_from_keywords(text):
    emotion_keywords = {
        "love": [
            "love", "adore", "affection", "fond", "romance",
            "romantic", "crush", "infatuated", "sweet", "darling", "honey",
            "beloved", "cherish", "devotion", "intimate", "soulmate", "sweetheart",
            "cinta", "sayang", "kasih","mesra",
            "romantis", "pacaran", "kasmaran", "suka", "gebetan", "pacar", "kekasih", "jatuh hati"
        ],
        "joy": [
            "glad", "elated", "passionate", "excited", "thrilled", "pleased", "blissful", "ecstatic", "euphoric",
            "senang", "gembira", "bahagia", "ceria", "riang", "girang", "semangat", "antusias", 
            "berseri", "berbinar", "asik", "seru", "tertawa"
        ],
        "anger": [
            "mad", "annoyed", "irritated", "frustrated", "resentful",
            "kesal", "marah", "geram", "jengkel", "sebal", "benci", "murka", "sewot", "emosi", 
            "naik pitam", "naik darah", "bete", "badmood", "kurang ajar", "sialan", "murka"
        ],
        "fear": [
            "worried", "concerned", "alarmed", "frightened", "worried",
            "takut", "cemas", "khawatir", "gelisah", "deg-degan", "panik", "was-was", "paranoid",
            "parno", "seram",  "ngeri"
        ],
        "sadness": [
            "gloomy", "melancholy", "miserable", "cry", "disappointed", "hurt", "hopeless",
            "sedih", "murung", "pilu", "duka", "galau", "patah hati", "terpuruk", "larut", "berduka", "nangis",
            "air mata", "hancur", "kecewa", "sakit hati", "luka", "kosong", "hampa", "sepi", "berpisah",
            "kesepian", "putus asa", "down", "baper", "mellow", "putus asa", "pergi","putus", "kehilangan"
        ],
        "surprise": [
            "speechless","startled", "stunned",
            "terkejut", "kaget", "takjub", "wah", "tercengang", "syok", "nggak nyangka"
        ],
    }
    
    text_lower = text.lower()
    
    for keyword in emotion_keywords["love"]:
        if keyword in text_lower:
            return "love"
    
    emotion_scores = {}
    
    for emotion, keywords in emotion_keywords.items():
        if emotion == "love":
            continue
            
        score = 0
        
        for keyword in keywords:
            if keyword in text_lower:
                score += len(keyword.split())
        
        if score > 0:
            emotion_scores[emotion] = score
    
    if emotion_scores:
        return max(emotion_scores, key=emotion_scores.get)
    
    return "neutral"

def map_emotion_to_supported(emotion):
    mapping = {
        "joy": "joy",
        "happiness": "joy", 
        "sadness": "sadness",
        "anger": "anger",
        "fear": "fear",
        "surprise": "surprise",
        "love": "love",
    }
    return mapping.get(emotion, "neutral")

def detect_emotion_from_text(text):
    global huggingface_auth_success
    
    if not hasattr(detect_emotion_from_text, '_auth_tested'):
        huggingface_auth_success = test_huggingface_auth()
        detect_emotion_from_text._auth_tested = True

    keyword_emotion = detect_emotion_from_keywords(text)
    if keyword_emotion != "neutral":
        return keyword_emotion

    if not config.HUGGINGFACE_API_KEY or not huggingface_auth_success:
        return keyword_emotion

    english_text = translate_to_english(text)
    headers = {"Authorization": f"Bearer {config.HUGGINGFACE_API_KEY}"}
    payload = {"inputs": english_text}

    try:
        response = requests.post(config.HUGGINGFACE_EMOTION_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict) and 'label' in result[0] and 'score' in result[0]:
                top_emotion = result[0]
                if top_emotion['score'] >= 0.6:
                    return map_emotion_to_supported(top_emotion['label'].lower())
                
            elif isinstance(result[0], list):
                emotions = result[0]
                top_emotion = max(emotions, key=lambda x: x['score'])
                if top_emotion['score'] >= 0.6:
                    return map_emotion_to_supported(top_emotion['label'].lower())
        
        return keyword_emotion
        
    except:
        return keyword_emotion