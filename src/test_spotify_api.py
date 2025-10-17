import os 
from dotenv import load_dotenv
import spotipy 
from spotipy.oauth2 import SpotifyOAuth

# Load the environment variables from .env
load_dotenv()

# Grt credentials from environment
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Authenticate with Spotify
scope = "user-top-read" # permission to read top tracks/artists
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_path="token_cache/.cache"
))

# Get Top 5 Artists
res = sp.current_user_top_artists(limit=5, time_range='medium_term')

print("\n🎧 Your Top 5 Artists (Medium Term):\n")
for idx, artist in enumerate(res['items']):
    print(f"{idx+1}. {artist['name']}")