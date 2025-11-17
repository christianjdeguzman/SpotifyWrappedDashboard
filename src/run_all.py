# src/run_all.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date

from data_collection import create_spotify_client, get_top_artists, get_top_tracks, save_to_csv

def run_pipeline_and_plots():
    # Create Spotify client
    sp = create_spotify_client()

    # Fetch data
    top_artists_df = get_top_artists(sp)
    top_tracks_df  = get_top_tracks(sp)

    # Prepare directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    # Snapshot date string
    today_str = date.today().strftime("%Y-%m-%d")

    # Save CSVs with date
    artists_filename = f"top_artists_{today_str}.csv"
    tracks_filename  = f"top_tracks_{today_str}.csv"
    save_to_csv(top_artists_df, artists_filename)
    save_to_csv(top_tracks_df,  tracks_filename)

    # ---- EDA & plots ----

    # 1. Popularity distribution histogram
    plt.figure(figsize=(8,5))
    sns.histplot(top_tracks_df['popularity'], bins=30, kde=True)
    plt.title("Track Popularity Distribution")
    plt.xlabel("Popularity Score")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join("plots", f"popularity_distribution_{today_str}.png"))
    plt.close()

    # 1a. Duration in Minutes
    top_tracks_df['duration_ms'] = top_tracks_df['duration_ms'] / 60000
    plt.figure(figsize=(8,5))
    sns.histplot(top_tracks_df['duration_ms'], bins=30)
    plt.title("Track Duration (mins)")
    plt.xlabel("Duration (mins)")
    plt.ylabel("Count")  # optional: because histogram shows counts
    plt.tight_layout()
    plt.savefig(os.path.join("plots", f"track_duration_distribution_{today_str}.png"))
    plt.close()

    # 2. Duration vs Popularity scatter plot
    top_tracks_df['duration_min'] = top_tracks_df['duration_ms'] / 60000
    plt.figure(figsize=(8,5))
    sns.scatterplot(x='duration_min', y='popularity', data=top_tracks_df)
    plt.title("Track Duration vs Popularity")
    plt.xlabel("Duration (min)")
    plt.ylabel("Popularity Score")
    plt.tight_layout()
    plt.savefig(os.path.join("plots", f"duration_vs_popularity_{today_str}.png"))
    plt.close()

    # 3. Genre frequency bar chart
    genres_series = (
        top_artists_df['genres']
        .str.split(r',\s*')
        .explode()
        .str.strip()
        .value_counts()
    )
    top_genres = genres_series.head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(
        x=top_genres.values,
        y=top_genres.index,
        hue=top_genres.index,
        palette='viridis',
        legend=False
    )
    plt.title("Top 10 Genres by Count")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.savefig(os.path.join("plots", f"top_genres_{today_str}.png"))
    plt.close()

    # 4. Artist track count bar chart
    artist_counts = top_tracks_df['artist'].value_counts().head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(
        x=artist_counts.values,
        y=artist_counts.index,
        hue=artist_counts.index,
        palette='magma',
        legend=False
    )
    plt.title("Top 10 Artists by Number of Top Tracks")
    plt.xlabel("Number of Top Tracks")
    plt.ylabel("Artist")
    plt.tight_layout()
    plt.savefig(os.path.join("plots", f"top_artists_count_{today_str}.png"))
    plt.close()

    print(f"✅ Pipeline complete. Data saved in `data/{artists_filename}` & `data/{tracks_filename}`;")
    print(f"   Plots saved in `plots/` with date suffix {today_str}.")

if __name__ == "__main__":
    run_pipeline_and_plots()
