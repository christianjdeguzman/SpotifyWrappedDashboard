import datetime
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
            "track_id" : track["id"],
            "track_name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "duration_ms": track["duration_ms"],
            "popularity": track["popularity"],
            "spotify_url": track["external_urls"]["spotify"]
            } 
        tracks.append(track_info)
    
    return pd.DataFrame(tracks)
'''

def get_audio_features(sp, tracks_df):
    """
    Try to augment tracks_df with Spotify audio features.
    If the audio_features endpoint returns 403 (forbidden),
    log the issue and return the original tracks_df un-enriched.
    """
    # Extract track IDs
    track_ids = [
        tid for tid in tracks_df["track_id"].tolist()
        if isinstance(tid, str) and len(tid) == 22
    ]

    if not track_ids:
        print("No valid track IDs found.")
        return tracks_df

    try:
        features = sp.audio_features(track_ids)
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error (audio_features): {e}")
        print("Fallback: Returning original tracks_df without audio features.")
        return tracks_df

    # If features returned but maybe all None
    if not features or all(f is None for f in features):
        print("audio_features returned no data (all None).")
        print("Fallback: Returning original tracks_df without audio features.")
        return tracks_df

    audio_data = []
    for f in features:
        if f:
            audio_data.append({
                "track_id": f["id"],
                "danceability": f["danceability"],
                "energy": f["energy"],
                "tempo": f["tempo"],
                "valence": f["valence"],
                "acousticness": f["acousticness"],
                "instrumentalness": f["instrumentalness"],
                "liveness": f["liveness"],
                "speechiness": f["speechiness"],
            })

    audio_df = pd.DataFrame(audio_data)

    # Merge enriched features with original tracks by track_id
    merged_df = pd.merge(
        tracks_df.reset_index(drop=True),
        audio_df.reset_index(drop=True),
        how="left",
        left_on="track_id",
        right_on="track_id"
    )
    return merged_df
'''

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

    print(top_tracks_df.head())
    print(top_artists_df.head())
    
    # tracks_with_features = get_audio_features(sp, top_tracks_df)
    #print(tracks_with_features.head())
    #save_to_csv(tracks_with_features, f"top_tracks_features_{datetime.date.today()}.csv")

    save_to_csv(top_artists_df, f"top_artists{datetime.date.today()}.csv")
    save_to_csv(top_tracks_df, f"top_tracks_{datetime.date.today()}.csv")