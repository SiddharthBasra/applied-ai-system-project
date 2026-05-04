# Applied AI System: Smart Music Recommender
**Base Project:** Module 3 Music Recommender Simulation

**Summary:** This project extends the original Module 3 simulation into a more robust system by introducing an automated Reliability and Testing Harness. It evaluates the AI recommendation engine's accuracy and guardrails across standard and conflicting user profiles.

## Advanced AI Feature: Reliability System & Test Harness
I implemented an automated test harness (`evaluate_system.py`) that feeds predefined user profiles (including edge cases with conflicting parameters) into the recommendation logic. It scores the system based on its ability to handle bad inputs and return valid, formatted explanations.

## Testing Summary
- **Tests Run:** 3 (Standard, Edge Case, Vague/Missing Data)
- **Result:** 3/3 Passed
- **Overall System Reliability:** 100.0%
The system successfully handled vague requests by defaulting to energy-proximity scoring rather than crashing.

## Demo Video
(https://drive.google.com/file/d/1sxyf2E28Y3Jid36jV-MeJlAM6c3zsdz8/view?usp=sharing)

---

## How The System Works

Each `Song` stores ten attributes loaded from `data/songs.csv`: `id`, `title`, `artist`, `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`, `valence` (0.0–1.0), `danceability` (0.0–1.0), and `acousticness` (0.0–1.0).

A `UserProfile` stores four preference fields: `favorite_genre`, `favorite_mood`, `target_energy` (a float 0.0–1.0), and `likes_acoustic` (a boolean for listeners who prefer guitar-forward, natural-sounding tracks).

The `Recommender` scores each song using this recipe:

| Signal | Points | Logic |
|---|---|---|
| Genre match | +2.0 | Exact string match — strongest signal |
| Mood match | +1.0 | Exact string match — emotional alignment |
| Energy proximity | +0.0 to +1.0 | `1.0 - abs(song.energy - target_energy)` |
| Acoustic bonus | +0.5 | Applied if `likes_acoustic=True` and `song.acousticness > 0.6` |

The maximum possible score is **4.5** (all four signals matched perfectly).

After every song has a score, the catalog is sorted from highest to lowest and the top k results are returned. This is called the **Ranking Rule** — recommendation is just sorting with a custom formula.

Data flow: **Input (User Profile)** → **Process (Score every song in the CSV)** → **Output (Ranked Top 5)**

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows