# FACTCHECK.md

Each factual claim in the narration, with where it was checked. Source revision: `111bf6e`.

| Beat | Claim | Checked against | Status |
|---|---|---|---|
| B00 | The prompt is reconstructed, not a transcript. | It is labelled on screen. | OK (disclosed) |
| B01 | Most art was generated first; the design docs say they are retrospective. | The banners in `CONCEPT.md`, `STORYBOARD.md`, `CHARACTER-SHEET.md`; the dating in `FRICTIONAL.md` (walk sheet 2026-09-22, GDD about 2026-09-24). | OK |
| B01 | Images came from gpt-image via Codex "Sol"; music, two stings and two event sounds came from Gemini. | `SOURCES.md`, Generative models (C2PA manifests; `audio/PROMPTS.md`). | OK. Gemini made 2 loops, 2 stings and 2 SFX (the narration says "the music"). |
| B02 | The pillars and the one-way floors. | `CONCEPT.md` (from `策划案_v1_0.md` §三, §九). | OK |
| B02 | Arknights IP is used against the rights rule. | `SOURCES.md` §Rights. | OK |
| B03 | Eight walk directions; five combat rows, three mirrored; three combo attacks, wave, one hurt frame; SE drawn as SW, flipped. | `lappland_animator_3d.gd:26,38,42`; atlas 896×320 = 14×5 cells. | OK |
| B04 | Real WASD key events; left-click path. | `capture/combat-inputs.jsonl` (`hold_key` D/S/A/W); `Player.attack` in `capture_a2_film.gd`. | OK |
| B05 | Four signals on an edge; two cues have Gemini files; hatch and shelf are counted but silent. | `game_manager.gd:157-160`; `field_audio.gd:7-12`; `audio/sfx/` holds only `lights_on.wav` and `lights_off.wav`. | OK |
| B06 | Four light cues, one hatch and one shelf per built rack, nothing extra in the doorway. | `test_audio.gd:70-78`, which passed on the fresh clone (`evidence/fresh-clone-111bf6e.log`). | OK |
| B08 | Each loop has its own intro and a logged loop point; pause freezes the field loop; one sting per run end. | `game_music.gd:10-13, 70-82, 107-113`; `audio/asset_log.json`. | OK |
| B09 | The floor-30 camp is unlocked in memory; she fights without dodging or healing until killed; one fail sting. | `capture/death-inputs.jsonl` (`setup_unlock_camp`; settled by frame 349); `capture_a2_film.gd` `fight(150, false)`. | OK |
| B11 | Painted at 1254 px; nearest-neighbour to 64 inside 72; 23 colours plus an outline; 43% isolated pixels flagged; author accepted. | The source PNG is 1254×1254; `reduce_generated.py:10-12, 60-70`; the measurement and the author's "挺好的" are recorded in `FRICTIONAL.md`. | OK |
| B12 | Drawn at exactly 1× in the R window; only whole multiples of 72. | `ui/ak.gd` `relic_icon` (`floori(side / 72)`); `test_relic_icons.gd` checks 72 and 144. | OK |
| B13 | `music/` also matched `audio/music/`; five music files restored. | `git show --stat 111bf6e` (five `.ogg` files plus their `.import` files); the silent 720p trial (−91 dB) is in `CAPTURE.md`. | OK |
| B14 | The camp has music; a real click on 撤离; one extract sting. | `capture/extract-inputs.jsonl` (click at frame 110, on the button's centre); volumedetect gives −23.8 dB mean (4–10 s). | OK |
| B15 | Counts are taken before the headless early return; the test teleports. | `field_audio.gd` (`counts` incremented before the `headless` return); `test_audio.gd:72,74`. | OK |
| B16 | Every test suite passes on a fresh `111bf6e` clone; `capture_v1` failed once and passed on reruns; `f770e26` failed at the missing music. | `evidence/fresh-clone-111bf6e.log`, `evidence/fresh-clone-f770e26.log`. | OK (`capture_v1` rerun twice, both clean) |
| B17 | 7 states, 3 regions, 2 loops, 2 stings, 2 event sounds, a mute switch; open items. | `CHARACTER-SHEET.md`, `SOURCES.md`, `TEST-REPORT.md`. | OK |
| B17 | The human playtest is not recorded. | `TEST-REPORT.md` §Human playtest. | OK |

## Corrections made during the build

- **B09** first said "killed in about ten seconds". The final take's timing was checked against its input log, and the line now says "until she is killed".
- **B12** first claimed a 2× pick card that the beat does not show. That line was removed.
- **B16** first said "the whole suite passes", and then "three reruns". It now names the flaky `capture_v1` and says it passed both times it was rerun.
- **B01:** the hesitant-writer correction did not fire, because a trigger containing a comma is split into two triggers. It was reworded to a single-word trigger, "first" → "after".

## Visual and audio QC

Recorded after the final render in the section below.

### Final export, checked 2026-10-07

`exports/landscape/claude-liam-downfall-gamedev.mp4`:

| Property | Value |
|---|---|
| Resolution | 3840×2160 |
| Frame rate | 30 fps |
| Duration | 383.3 s |
| SHA-256 | `144dbfe4412d5c2ed2e18e42c9d881dc126e31d2b264f101d7d502a1c59cc943` |

- **Gate V:** 40 frames sampled, 0 BLOCKER, 0 MAJOR. Declared contrast regions are listed in `_qc/REPORT.md`.
- **First render refused:** 4 BLOCKER and 13 MAJOR. The fixes were:
  - B12/B16 labels moved into title-safe;
  - capture-label contrast regions declared on the gameplay beats;
  - B01 font enlarged;
  - B13 given more real `.gitignore` context lines and contrast regions.
- **Audio, per beat:**
  - every narrated beat has a mean of about −27 dB;
  - B07 and B10 (slice audio) carry the game mix: B07's loudness envelope correlates 0.91 with `media/B07.mp4`'s capture audio;
  - B19 is silent (−91 dB).
- **Outro jingle: limitation.** OUTRO-LOCK asks for a stock jingle under the card. This checkout's `ClaudeTitleOutro` renders no audio element, so the card is silent. The Assignment 1 film from the same pipeline is silent there too. The shared tool was not changed.
- **Frames inspected:** one per beat (`_qc/final_sheet.png`, kept locally). They show:
  - the code at reading size, with no cut-off lines;
  - labels on every capture beat;
  - "Design came first." correcting to "after";
  - the asset trace;
  - the test-output panel;
  - the verdict;
  - the outro title and handle.
- **Not done:** no human has watched the whole film with sound.
