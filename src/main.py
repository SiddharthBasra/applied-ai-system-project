"""
Command line runner for the Music Recommender Simulation.
AI110 | Foundations of AI Engineering, Week 7

Run from the project root:
    python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles (Phase 4 — Stress Test with Diverse Profiles)
# ---------------------------------------------------------------------------

PROFILES = {
    "High-Energy Pop (default)": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "likes_acoustic": False,
    },
    "Chill Study Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    },
    "Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
    },
    "Late Night Synthwave": {
        "genre": "synthwave",
        "mood": "moody",
        "energy": 0.74,
        "likes_acoustic": False,
    },
    "Acoustic Jazz Cafe": {
        "genre": "jazz",
        "mood": "relaxed",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    # Edge case: conflicting preferences (high energy but chill mood)
    "Conflicted [edge case]": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.90,
        "likes_acoustic": False,
    },
}


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------

def print_recommendations(profile_name: str, user_prefs: dict, recommendations: list) -> None:
    """Print a clean, readable ranking for one user profile."""
    width = 64
    print()
    print("=" * width)
    print(f"  PROFILE : {profile_name}")
    acoustic_flag = " | likes acoustic" if user_prefs.get("likes_acoustic") else ""
    print(
        f"  Prefs   : genre={user_prefs['genre']} | "
        f"mood={user_prefs['mood']} | "
        f"energy={user_prefs['energy']}{acoustic_flag}"
    )
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score  : {score:.4f}")
        print(f"       Because: {explanation}")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "songs.csv"
    )

    songs = load_songs(data_path)

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
