# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** — a content-based music recommendation simulator built for AI110, Week 7.

---

## 2. Intended Use

This system suggests the top 5 songs from a small catalog based on a listener's preferred genre, mood, and energy level. It is designed for classroom exploration of how content-based recommenders work — not for deployment to real users. The goal is to make the pipeline from user data → score → ranking fully transparent and inspectable.

Assumptions: the user can describe their taste in advance using the fields `genre`, `mood`, and `energy`. The system does not learn from listening history or adapt over time.

---

## 3. How the Model Works

Every song in the catalog has a set of attributes: genre, mood, energy, tempo, danceability, acousticness, and valence. A listener's taste is captured in a profile with four fields: their favorite genre, preferred mood, target energy level, and whether they enjoy acoustic-sounding music.

To recommend songs, the system asks four questions about each track and awards points for each match:

- Does the song's genre match the listener's favorite? If yes: 2 points. This is weighted highest because genre defines the fundamental sound.
- Does the song's mood match the listener's preferred mood? If yes: 1 point. Mood captures emotional tone — happy, intense, chill, moody, relaxed.
- How close is the song's energy to the listener's target? The closer, the more points — up to 1 full point for an exact match, and 0 points if the song is at the opposite extreme.
- Does the listener like acoustic-sounding music, and does the song have a high acousticness score? If both are true: a 0.5 bonus.

After every song in the catalog has a score, the system sorts them from highest to lowest and returns the top 5. That's the entire algorithm — recommendation is just sorting with a custom formula.

---

## 4. Data

The catalog contains **22 songs** stored in `data/songs.csv`. The starter file included 10 songs; 12 additional tracks were added to ensure better coverage across genres and to reduce the risk of profiles returning near-identical results every time.

Genres represented: pop, lofi, rock, synthwave, jazz, ambient, indie pop. Moods represented: happy, chill, intense, focused, moody, relaxed.

The dataset skews toward Western, English-language popular music and electronic genres common in study/productivity playlists. Genres like K-pop, reggaeton, classical, country, or R&B are entirely absent. This means the recommender will underserve any listener whose taste falls outside these categories, not because the algorithm is wrong but because the data doesn't cover them.

All genre and mood labels were assigned manually and reflect one person's interpretation. A different labeler might call "Night Drive Loop" atmospheric rather than moody, or "Gym Hero" dance-pop rather than pop/intense.

---

## 5. Strengths

The system works best when the catalog has good coverage of the user's genre and the user's preferences are internally consistent (no contradictions between mood and energy).

The "Chill Study Lofi" profile produced the most accurate-feeling results: Late Night Drift scored a perfect 4.5 because it matched genre, mood, had identical energy to the target, and triggered the acoustic bonus. The top 3 results all felt intuitively correct as study music.

The "Intense Rock" profile also performed well because the catalog contains four rock/intense songs at different energy levels, giving the ranking room to meaningfully differentiate results.

The system's biggest strength is transparency. Every recommendation comes with a plain-language explanation ("genre match (+2.0), mood match (+1.0), energy similarity (+0.97)") that tells the user exactly why each song ranked where it did. Most real recommenders are black boxes — this one is fully inspectable.

---

## 6. Limitations and Bias

**Genre dominance creates a filter bubble.** Genre accounts for 2 of a possible 4.5 points. In practice, this means the top 3–4 results for any profile are almost always the same genre the user asked for, even when a cross-genre song would feel like a perfect match. A jazz listener who would actually love a chill lofi track will never see it because "lofi ≠ jazz."

**Binary matching ignores genre similarity.** "Indie pop" and "pop" are scored as completely different genres. In reality they share many sonic qualities. A similarity matrix (e.g., pop and indie pop share 70% overlap) would produce more intuitive cross-genre suggestions.

**Small catalog amplifies every bias.** With 22 songs and 7 genres, some genres have only 2–3 tracks. A synthwave listener will always see the same 2 songs at the top regardless of their specific energy target, because there's nothing else to differentiate. The system would need at least 200–500 songs per genre to produce genuinely varied recommendations.

**Conflicting preferences return silently wrong results.** The edge-case profile (lofi/chill genre and mood, energy=0.90) returned low-energy lofi tracks because the genre and mood signals outweighed the energy mismatch. The system had no way to flag that the request was contradictory — it confidently returned results that were wrong in a specific dimension without explanation.

**The data reflects a narrow slice of musical taste.** No representation of classical, country, R&B, K-pop, or reggaeton means anyone whose primary genre falls outside the catalog will see irrelevant results regardless of how well the algorithm is tuned.

---

## 7. Evaluation

Six distinct user profiles were tested:

- **High-Energy Pop** — top 3 all scored 3.93–3.97 and were correctly pop/happy/high-energy. Results felt accurate.
- **Chill Study Lofi** — top 3 scored 4.46–4.50, all lofi/chill. The acoustic bonus correctly reinforced these results. Perfect match.
- **Intense Rock** — top 4 were all rock/intense. The #5 result was Gym Hero (pop/intense) with no genre match, showing that mood+energy can place a non-genre-match in the top 5 if the genre-matched catalog is small.
- **Late Night Synthwave** — only 2 synthwave songs exist in the catalog; #3–5 were mood matches from other genres, revealing the small-catalog problem clearly.
- **Acoustic Jazz Cafe** — top 2 were perfect jazz/relaxed/acoustic matches. #3–5 were lofi tracks that won on energy proximity + acoustic bonus, a cross-genre serendipity that felt plausible.
- **Conflicted edge case (lofi/chill, energy=0.90)** — all 5 results were lofi with low energy. Genre+mood dominated, the energy mismatch was ignored. This was the clearest failure mode.

Tests in `tests/test_recommender.py` verified that `recommend()` returns songs sorted correctly (pop/happy ranked #1 over lofi/chill for a pop/happy profile) and that `explain_recommendation()` returns a non-empty string.

---

## 8. Future Work

- **Connect to the Spotify Web API** to use real audio features (acousticness, valence, danceability) measured from actual audio rather than hand-labeled estimates, and to access a catalog of millions of songs.
- **Replace binary genre/mood matching with embedding similarity** so that "indie pop" and "pop" share partial credit, and "chill" and "relaxed" moods are treated as close but not identical.
- **Add implicit feedback:** track which songs the user skips versus replays and adjust weights accordingly. A user who always skips songs with energy > 0.7 should have their target energy updated downward automatically.
- **Improve result diversity:** the current system always returns the closest matches, which means the top 5 can feel nearly identical. A diversity penalty (penalizing songs that are too similar to an already-selected result) would make the list feel more like a playlist and less like a sorted table.

---

## 9. Personal Reflection

The most surprising thing I discovered was how little math a recommendation system actually needs to produce results that feel right. A handful of weights, a loop over a CSV, and a sort — and the output feels like something a streaming platform might genuinely surface. That simplicity is both the system's strength and its weakness: it is fully understandable, but it also cannot handle any nuance that wasn't explicitly programmed in.

Building this changed the way I think about platforms like Spotify or TikTok. When a recommendation feels uncannily accurate, it is probably not because the algorithm is "smart" — it is because the platform has enormous amounts of behavioral data (skips, replays, playlist additions) that let it infer preferences far more accurately than any stated profile could. Our system only knows what the user tells it; a real system knows what the user *does*.

Human judgment still matters most in two places: deciding what features to measure in the first place (why energy and not tempo? why genre and not lyric themes?) and evaluating whether the results *feel* right to a real person. No metric can fully capture whether a playlist feels good. That final quality check — "does this actually sound like what I'd want to hear?" — still requires a human ear.
