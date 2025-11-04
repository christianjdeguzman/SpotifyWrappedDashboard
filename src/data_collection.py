import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client():
    load_dotenv()

    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        # Get credentials from environments
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-top-read",
        cache_path="token_cache/.cache"
    ))
    
    return sp

# Data Collection Functions
def get_top_artists(sp, limit=20, time_range="medium_term"):
    # medium term = 6 months
    results = sp.current_user_top_artists(limit=limit, time_range=time_range)
    # Initialize an empty array for lists of artists
    artists = []
    # Loop through each artists in top 20
    for artist in results["items"]:
        # Make a dictionary for each artists
        artist_info = {
            "name": artist["name"],
            "genres": ", ".join(artist["genres"]),
            "popularity": artist["popularity"],
            "followers": artist["followers"]["total"],
            "spotify_url": artist["external_urls"]["spotify"]
        }
        artists.append(artist_info)

    return pd.DataFrame(artists)

def get_top_tracks(sp, limit=20, time_range="medium_term"):
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    
    tracks = []
    
    for track in results["items"]:
        track_info = {
            "track_name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "duration_ms": track["duration_ms"],
            "popularity": track["popularity"],
            "spotify_url": track["external_urls"]["spotify"]
            } 
        tracks.append(track_info)
    
    return pd.DataFrame(tracks)

# Save to CSV file
def save_to_csv(df, filename):
    # gets the folder where the script lives (src/ root)
    # gets a full path to data/ which we will store csv file in
    out_dir = os.path.join(os.path.dirname(__file__), "../data")
    # Ensures code can safely write files there
    os.makedirs(out_dir, exist_ok=True)
    # Builds the full file path and writes DF to CSV file
    df.to_csv(os.path.join(out_dir, filename), index=False)
    print(f"Saved: {filename}")


# test run
# Checks if the script is being run directly (python src/data collection.py)
if __name__ == "__main__":
    sp = create_spotify_client()
    top_artists_df = get_top_artists(sp)
    top_tracks_df = get_top_tracks(sp)
    print(top_artists_df.head())
    print(top_tracks_df.head())

    save_to_csv(top_artists_df, "top_artists.csv")
    save_to_csv(top_tracks_df, "top_tracks.csv")