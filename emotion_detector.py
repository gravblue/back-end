from transformers import pipeline
from deep_translator import GoogleTranslator

# Inisialisasi pipeline Hugging Face (tanpa token)
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def translate_to_english(text):
    try:
        translator = GoogleTranslator(source='auto', target='en')
        return translator.translate(text)
    except Exception:
        return text

def map_emotion_to_supported(emotion):
    mapping = {
        "joy": "joy",
        "happiness": "joy",
        "sadness": "sadness",
        "anger": "anger",
        "fear": "fear",
        "surprise": "surprise",
        "love": "love",
        "neutral": "neutral"
    }
    return mapping.get(emotion.lower(), "neutral")

def detect_emotion_from_keywords(text):
    emotion_keywords = {
        "love": [
            "love", "adore", "affection", "fond", "romance",
            "romantic", "crush", "infatuated", "sweet", "darling", "honey",
            "beloved", "cherish", "devotion", "intimate", "soulmate", "sweetheart",
            "cinta", "sayang", "kasih", "mesra",
            "romantis", "pacaran", "kasmaran", "suka", "gebetan", "pacar", "kekasih", "jatuh hati"
        ],
        "joy": [
            "glad", "elated", "passionate", "excited", "thrilled", "pleased", "blissful", "ecstatic", "euphoric",
            "senang", "ceria", "riang", "girang", "semangat", "antusias", "tertawa"
        ],
        "anger": [
            "mad", "annoyed", "irritated", "frustrated", "resentful",
            "kesal", "geram", "jengkel", "sebal", "benci", "murka", "sewot", "emosi", 
            "naik pitam", "bete", "badmood", "kurang ajar", "sialan"
        ],
        "fear": [
            "worried", "concerned", "alarmed", "frightened",
            "cemas", "deg-degan", "was-was", "paranoid", "parno"
        ],
        "sadness": [
            "gloomy", "melancholy", "miserable", "cry", "disappointed", "hurt", "hopeless",
            "murung", "pilu", "duka", "galau", "terpuruk", "larut", "nangis",
            "air mata", "hancur", "sakit hati", "luka", "kosong", "hampa", "sepi", "berpisah",
            "putus asa", "down", "baper", "mellow", "pergi", "putus", "kehilangan"
        ],
        "surprise": [
            "speechless", "startled", "stunned",
            "kaget", "takjub", "wah"
        ]
    }

    text_lower = text.lower()
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return emotion
    return "neutral"

def detect_emotion_from_text(text):
    if not text or not text.strip():
        return "neutral"

    # Cek dulu pakai keyword
    keyword_emotion = detect_emotion_from_keywords(text)
    if keyword_emotion != "neutral":
        return keyword_emotion

    # Kalau tidak terdeteksi keyword, pakai model Hugging Face
    try:
        english_text = translate_to_english(text)
        predictions = emotion_pipeline(english_text)[0]
        top = max(predictions, key=lambda x: x['score'])

        if top['score'] >= 0.6:
            return map_emotion_to_supported(top['label'])
        else:
            return "neutral"
    except Exception as e:
        print(f"Model error: {str(e)}")
        return "neutral"

# Tes
if __name__ == "__main__":
    test_texts = [
        "Aku cinta kamu",         # love (keyword)
        "Aku sangat bahagia",     # joy (keyword)
        "Saya kecewa banget",     # sadness (keyword)
        "Saya takut gelap",       # fear (keyword)
        "Gila ini seru banget!",  # joy (model)
        "asdfghjkl",              # neutral (fallback)
        "Aku kehilangan dia"      # sadness (keyword)
    ]
    for text in test_texts:
        result = detect_emotion_from_text(text)
        print(f"'{text}' ➜ {result}")
