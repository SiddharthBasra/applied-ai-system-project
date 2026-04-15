"""
Music Recommender Simulation — Core Logic
AI110 | Foundations of AI Engineering, Week 7

Implements both:
  - An OOP API (Song, UserProfile, Recommender) used by the test suite
  - A functional API (load_songs, score_song, recommend_songs) used by main.py
"""

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its audio/metadata attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a listener's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------------
# OOP Recommender (used by tests/test_recommender.py)
# ---------------------------------------------------------------------------

class Recommender:
    """
    Scores and ranks Song objects against a UserProfile.

    Scoring recipe:
      +2.0  genre match
      +1.0  mood match
      +1.0  energy similarity  (1 - |song.energy - target|)
      +0.5  acousticness bonus if user likes_acoustic and song.acousticness > 0.6
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Return a numeric score for one song given a user profile."""
        score = 0.0

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0

        # Reward songs whose energy is *close* to the user's target,
        # rather than blindly preferring high or low energy.
        score += 1.0 - abs(song.energy - user.target_energy)

        # Acoustic bonus: reward mellow, guitar-forward tracks for listeners
        # who explicitly prefer that texture.
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5

        return round(score, 4)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score, highest first."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why this song was scored."""
        parts = []

        if song.genre.lower() == user.favorite_genre.lower():
            parts.append(f"genre match — {song.genre} (+2.0)")

        if song.mood.lower() == user.favorite_mood.lower():
            parts.append(f"mood match — {song.mood} (+1.0)")

        energy_sim = round(1.0 - abs(song.energy - user.target_energy), 4)
        parts.append(f"energy similarity (+{energy_sim:.2f})")

        if user.likes_acoustic and song.acousticness > 0.6:
            parts.append(f"acoustic bonus (+0.5)")

        return "; ".join(parts) if parts else "no strong match found"


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file and return a list of dictionaries.
    Numeric columns (energy, tempo_bpm, valence, danceability, acousticness)
    are cast to float so arithmetic works correctly downstream.
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song dict against a user preference dict.

    user_prefs keys expected: "genre", "mood", "energy"
    Optional key:             "likes_acoustic" (bool)

    Returns (score: float, reasons: List[str]).
    The reasons list makes each recommendation self-explaining.
    """
    score = 0.0
    reasons = []

    # Genre match: strongest signal (+2.0)
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: emotional alignment (+1.0)
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy proximity: rewards closeness, not just high/low (+0.0 to +1.0)
    target_energy = user_prefs.get("energy", 0.5)
    energy_sim = round(1.0 - abs(song["energy"] - target_energy), 4)
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim:.2f})")

    # Acoustic texture bonus (+0.5)
    if user_prefs.get("likes_acoustic", False) and song.get("acousticness", 0) > 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Rank all songs by score and return the top-k results.

    Uses sorted() (not .sort()) so the original catalog list is never mutated —
    important when running several profiles in sequence.

    Returns a list of (song_dict, score, explanation_string) tuples.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
