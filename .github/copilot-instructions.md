Project: SpotifyWrappedDashboard — AI agent quick guide

Purpose
- Small Python project that collects & analyzes a user's Spotify "top" tracks/artists and stores CSV snapshots in data/ for downstream EDA notebooks.

Key files & flow
- src/data_collection.py — primary programmatic entry. Important functions: create_spotify_client(), get_top_artists(), get_top_tracks(), save_to_csv().
- src/test_spotify_api.py — a lightweight, runnable smoke test that illustrates how OAuth is configured and how to call current_user_top_artists.
- notebooks/eda_analysis.ipynb — exploratory notebook that reads CSV outputs and performs analysis/plots.
- data/ — output CSVs (e.g. top_tracks_YYYY-MM-DD.csv, top_artistsYYYY-MM-DD.csv).
 - src/run_all.py — convenience script that runs data collection + saves dated CSV snapshots and generates EDA plots into `plots/`.
 - data/ — output CSVs (e.g. top_tracks_YYYY-MM-DD.csv, top_artists_YYYY-MM-DD.csv).

Authentication & runtime conventions
- Credentials are provided via environment variables loaded by python-dotenv (.env): SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI.
- OAuth caching: cache_path="token_cache/.cache" is used in both scripts — do not remove or rename the token_cache/ folder unless you also update the cache path strings.
- Scope used: user-top-read (read-only access to top artists/tracks). The repo intentionally avoids some Spotify endpoints (see README note about audio features).

Data collection specifics & gotchas
- save_to_csv() writes into ../data relative to src/, so running scripts from repo root or from src/ works but be mindful of current working directory when testing.
- src/data_collection.py contains a commented (but robust) get_audio_features() implementation — the project currently skips audio features due to API constraints; if you re-enable it, handle 403 responses and missing items as the commented code shows.
- Track IDs are expected to be 22-character Spotify IDs when enriching audio features — the sample audio-features logic filters on this.

Quick smoke-test order (Windows cmd.exe):
1) Install deps: pip install -r requirements.txt
2) Provide env vars (or create a .env) with the 3 SPOTIFY_* values
3) Run python src/test_spotify_api.py to confirm OAuth and that your account returns top artists
4) Run python src/data_collection.py OR python src/run_all.py to generate CSV snapshots in `data/` and plots in `plots/`

Filename convention
- CSV snapshots use an underscore before the date: `top_artists_YYYY-MM-DD.csv` and `top_tracks_YYYY-MM-DD.csv`. `src/run_all.py` also creates plot images named like `popularity_distribution_YYYY-MM-DD.png` in `plots/`.

Testing & CI notes
- There's no automated test suite; src/test_spotify_api.py is a manual smoke test. When adding tests, follow the existing pattern: small scripts that exercise OAuth flows and CSV outputs.

Coding patterns & style specific to this repo
- Minimal dependency surface: spotipy, python-dotenv, pandas. See requirements.txt.
- Prefer explicit, small functions (see get_top_artists() / get_top_tracks()), return pandas DataFrames.
- I/O is CSV-centric for reproducibility with notebooks — prefer writing small, well-named CSV snapshots (the current date-based filenames are the convention).

What an AI agent should do first
- Read src/data_collection.py and src/test_spotify_api.py to understand auth and I/O contracts.
- Confirm environment variables and token_cache usage before making network calls.
- If augmenting with audio features or additional endpoints, copy-and-use the existing commented get_audio_features() logic as a safe pattern (it contains fallbacks for empty/403 responses).

Where to look next
- notebooks/eda_analysis.ipynb for how downstream analysis expects CSV columns and additional fields (month/date fields mentioned in README).
- data/ for existing snapshot examples (top_artists.csv, top_tracks.csv, recent dated CSVs).

If something is unclear
- Ask which run environment you want (local vs CI). Some assumptions (Windows/cmd) are in the repo; CI may need different auth handling (use service accounts or stored tokens).

Next steps I can help with
- Add a tiny GH Actions workflow to run src/test_spotify_api.py as a smoke check (requires valid secrets), or
- Convert src/test_spotify_api.py into a proper unit test that mocks Spotify responses.
