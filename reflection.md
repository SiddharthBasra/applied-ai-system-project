# Reflection — Profile Comparisons and System Observations

**AI110 | Foundations of AI Engineering — Week 7 Project**
**Author:** Sidd Basra

---

## Profile Pair 1: High-Energy Pop vs. Intense Rock

Both profiles want high-energy music (0.85 and 0.92 respectively), but they diverge in genre and mood. The Pop profile wants `happy` songs; the Rock profile wants `intense` ones.

**What changed:** The Pop profile returned a tight cluster of pop/happy songs (Sunrise City, City Pulse, Golden Hour) all scoring 3.93–3.97. The Rock profile's top 4 were all rock/intense, scoring 3.96–3.99 — even tighter. But both profiles had a dramatic drop at #5: for Pop, the #5 result (Rooftop Lights, indie pop) scored only 1.91 because it couldn't earn the genre match bonus. For Rock, Gym Hero (pop/intense) snuck into #5 at 1.99 purely on mood + energy, with no genre match.

**Why does this make sense?** When the catalog has enough songs in your genre with the right mood, the top 4 results are nearly identical in score — the differences come down to a few hundredths of a point from energy proximity. The dramatic drop at #5 happens because there simply aren't more genre-matched songs, so the algorithm falls back to the next best signal. The system is working correctly; the catalog coverage is just limited.

---

## Profile Pair 2: Chill Study Lofi vs. Acoustic Jazz Cafe

Both profiles want low-energy, mellow music with `likes_acoustic=True`. The Lofi profile targets `chill` mood and 0.38 energy; the Jazz profile targets `relaxed` mood and 0.35 energy.

**What changed:** The Lofi profile produced the highest possible score in the system: Late Night Drift scored a perfect 4.50 because it matched genre, mood, had identical energy (0.38), and triggered the acoustic bonus. The Jazz profile's top 2 both scored 4.48 — Coffee Shop Stories and Velvet Underground are both jazz/relaxed with acousticness > 0.6 and very close energy to the target. Interestingly, both profiles' #3–5 results crossed genre: the Jazz profile's #3, #4, #5 were all lofi tracks that scored ~1.47–1.50 on energy proximity + acoustic bonus alone, without any genre or mood match.

**Why does this make sense?** When the catalog has only 2 jazz songs, the algorithm is forced to reach outside the genre for results 3–5. The lofi tracks earned those spots because their energy and acousticness closely matched the jazz profile's preferences. This is actually the most "serendipitous" behavior in the system — a jazz listener seeing lofi tracks might genuinely enjoy them, since both are low-energy and acoustic. Whether this is a feature or a bug depends on the user.

---

## Profile Pair 3: Late Night Synthwave vs. Conflicted Listener (edge case)

The Synthwave profile is a strong match: genre=synthwave, mood=moody, energy=0.74. The Conflicted Listener is the adversarial case: genre=lofi, mood=chill, but energy=0.90 — a high-energy preference combined with a genre and mood that are almost always low-energy.

**What changed:** The Synthwave profile's top 2 (Night Drive Loop, Neon Grid) scored 3.98–3.99 — near-perfect. But only 2 synthwave songs exist in the catalog, so results #3–5 dropped sharply to 0.92–1.92, filled by mood and energy matches from other genres. The Conflicted Listener returned all lofi songs, but every one of them was low-energy (0.35–0.44), scoring 3.45–3.52 because genre + mood dominated the energy mismatch.

**Why does this make sense?** The Synthwave case exposes the small-catalog problem directly: when a genre only has 2 songs, the recommender runs out of meaningful options after #2. The Conflicted case shows the algorithm's inability to detect contradictory preferences — lofi and chill guarantee low-energy songs, but the user requested high energy. The system returned results that were "correct" by genre and mood while silently getting the energy wrong. A real production system would flag this inconsistency rather than returning a confidently wrong answer.

---

## General Observations

**The genre weight is the most powerful lever in the system.** In every single profile, the top results are dominated by the user's stated genre. No cross-genre song broke into the top 2 for any profile. This confirms that a genre weight of +2.0 (out of a possible 4.5) creates an effective genre filter bubble — useful for precision, but limiting for discovery.

**The acoustic bonus interacts cleanly with the catalog.** For profiles with `likes_acoustic=True`, the bonus consistently reinforced intuitively correct recommendations (lofi and jazz tracks both score high on acousticness). For profiles without it, the bonus had zero effect. This is a well-designed feature because it only activates when both the user and the song satisfy the condition — it never distorts results for users who don't care about acoustic texture.

**Small datasets amplify every bias.** With 2 synthwave songs, 2 jazz songs, and 4 lofi songs, results for some profiles are nearly deterministic. There is no randomness, no discovery, and almost no variation in what any given profile sees. The system would feel more like a real recommender with a catalog of 500+ songs, where energy and valence differences between songs create meaningful spread in the scores.
