# SOURCES — pitch film

## Made by the author (with Claude Code, see below)
- The game *Rhodes Daily* / Downfall and all its gameplay. Asset provenance for the game itself is in the repository's own `SOURCES.md`.
- The project direction and every content decision in the pitch: scope, risk framing, comparables, target role, and what is shown.

## Used
| What | Where from | Licence / terms |
|---|---|---|
| Gameplay footage | Godot Movie Maker captures of commit `1fbc309a` (`capture/`) | The author's own game |
| A6 particle frames | A6 film capture `a_play`, tag `a6` | Own work (Assignment 6) |
| A7 sword-wave frames | A7 film capture `wave_dodges`, tag `a7` | Own work (Assignment 7) |
| Narration voice | Kokoro-82M `am_onyx` via kokoro-onnx, run locally | Apache-2.0 model; the voice speaks as the author |
| Assembly and gates | Brutalist toolkit (`brutalist.art`): `generate_audio_kokoro.py`, `compile.py`, `final_frame_check.py` | Course toolkit |
| Fonts on the boards | Segoe UI and Consolas (Windows system fonts) | Used for rendering only |

- No generated images or video.
- No music in the film.
- No footage, logos or art from the two comparison games (Escape from Duckov, Greedy Cave). They are named in text only.

## What Claude (Claude Code, Opus 5.5) contributed, 2026-11-23
- **Writing:** the outline, PROJECT-BRIEF, the narration text and the beat sheet. Each was revised on the author's instructions (risk wording, scope, what to leave out).
- **Capture:** wrote `capture_pitch_film.gd`, ran the captures, reviewed them frame by frame, and re-recorded the bridge and route shots after the first takes failed.
- **Film:** wrote `make_media.py`, drew the diagram boards, ran the Brutalist pipeline, and fixed what Gate V flagged.
- **Fact check:** checked each claim against the repo and tags (FACTCHECK.md). Claude found that the 9→150 fps profiling figure has no committed log, so the film says so.
