import random
from spotify_auth import get_spotify_client

EMOTION_PLAYLIST_IDS = {
    "sadness": ["3nxTE0NRhVO45hJRndxrL9"],
    "joy": ["5LMTBceKfqJwawvGhzszhk"],
    "anger": ["3dAC5HEkLwcAZHOJ1fMP9w"],
    "fear": ["0d29Z9cKf28BPxCgsbmAI5"],
    "love": ["4ARq8N7J63MdGqaB8QSyJH"],
    "surprise": ["5JTerVQbZEZJJwmF8zTRcd"],
    "neutral": ["0L3k87l5zuVLRSXjpDC6UF"]
}

def process_track(track):
    if not track or track.get('is_local') or not all([track.get('name'), track.get('artists')]):
        return None

    images = track.get('album', {}).get('images', [])
    return {
        "title": track['name'],
        "artist": track['artists'][0]['name'],
        "url": track['external_urls'].get('spotify', '#'),
        "preview_url": track.get('preview_url'),
        "album_art": images[1]['url'] if len(images) > 1 else (images[0]['url'] if images else None)
    }

def get_tracks_from_playlist(playlist_id):
    try:
        sp = get_spotify_client()
        results = sp.playlist_tracks(playlist_id, limit=50)
        return [
            processed for item in results.get('items', [])
            if (processed := process_track(item.get('track')))
        ]
    except Exception as e:
        print(f"Error fetching tracks from playlist {playlist_id}: {e}")
        return []

def search_songs_by_playlist_ids(emotion, limit=5):
    try:
        playlist_ids = EMOTION_PLAYLIST_IDS.get(emotion.lower(), EMOTION_PLAYLIST_IDS["neutral"])
        all_tracks = []

        for pid in playlist_ids:
            all_tracks.extend(get_tracks_from_playlist(pid))

        # Remove duplicates
        seen = set()
        unique_tracks = []
        for track in all_tracks:
            key = f"{track['title'].lower()}_{track['artist'].lower()}"
            if key not in seen:
                seen.add(key)
                unique_tracks.append(track)

        random.shuffle(unique_tracks)
        return unique_tracks[:limit]
    except Exception as e:
        print(f"Error fetching songs for emotion '{emotion}': {e}")
        return []