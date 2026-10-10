# RIFF — observations, interpretation, narration, next experiment

Only the engine artifacts are riffed here; the document beats explain written design, not observed play.
There is no gameplay in this build, so no riff claims fun, feel, fairness or readability for a player.

| Artifact + time | Visible observation | Interpretation (source) | Narration (B-id) | Next experiment |
|---|---|---|---|---|
| `capture/stairs_side.png` (static) | six steps in profile, landing on the left; nothing else | the ramp has no mesh, so a normal render cannot show it (`base.tscn` lines 77–81) | "On the left, a normal render: you only see steps." (B12) | — |
| `capture/stairs_side_collision.png` (static) | an orange box lies along the front edges of all six steps, from floor to landing | the CollisionShape3D's top surface passes through each step nose; slope = rise/run (source math, B11) | "the invisible ramp lies across every step edge" (B12) | change only the step heights, predict the mismatch, re-run `ramp_check.gd` |
| `evidence/ramp-check.log` | noses 1–5: first hit `stairs/stairs_ramp` at +0.0007 m; nose 6: `Base/stairs` at 0.0000 m; PASS | the ramp ends exactly at the sixth step edge, where the landing begins | "meets the first five step edges within a millimetre, and ends at the sixth" (B12) | add a check that a CharacterBody3D capsule actually climbs it, once a character exists |
| `media/B14.mp4` 0–20.5 s | slow pan from the back-wall chair across the room toward the stairs; two bright spots on the ceiling; walls and floor blue-grey; nothing in the scene moves | lights at x = ±3.5 under a 3.235 m ceiling (lines 86–98); near-black environment (lines 5–10) | "two cool pools of light … dark and blue-grey, as the concept asked" (B14) | put a near-black capsule at character height in the darkest corner and grayscale-check it (CHANGE-BRIEF failure 2) |
| `listen/terminal-sfx-sequence.flac` 0.8 / 4.2 / 7.6 s | three short sounds separated by silence. From the waveform plots only (Claude cannot listen): power-on has a brief spike then a short burst; power-off has a larger, longer burst; button press is one short transient (`figures/sequence.png`). The listening judgments are the designer's, in the game's SOURCES.md | accepted generated files, unedited; no game event plays them | none (B09 is a no-narration listening segment) | wire power-on to the tablet state change and count triggers per press |

Hypotheses kept separate from observations: whether the ramp works for a real character, whether the dark
character reads in this room, and whether one input plays one sound are **untested** and are said so on screen.
