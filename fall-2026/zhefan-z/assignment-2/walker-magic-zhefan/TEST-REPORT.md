# TEST-REPORT — walker-magic

> Engine: Godot 4.7.2-stable (win64). Slice source revision tested: `74c0443` (branch `zhefan-z/assignment-2`); documentation and evidence images were added afterwards (see `git log`). The playtests are the author's, recorded as stated; automated results are copied from the command output.

## Results against the assignment's checks

| Check | Result | Evidence |
|---|---|---|
| **Startup and controls** | Pass. A fresh copy of `74c0443` (`git archive` into an empty folder: 183 files, no `.godot` cache) imports in 6 s, and every automated suite passes there (73 checks); the main scene runs headless with no script errors. Movement, jump, cast, pause, mute and restart work with the intended input (playtests 1–6). | Commands below; playtests 1–6 |
| **Character against the sheet** | Pass, with differences listed below. Every state and both facings, in engine beside the accepted pose. | `design/checks/engine/states-vs-sheet.png`; `design/character/collision.png` |
| **Storyboard against the slice** | P1, P2, P3, P4, P5 and P7 covered; **P6 (boss) not covered** (cut in CHANGE-BRIEF Revision 2). Differences listed below. | `design/checks/engine/P*.png` beside `design/storyboard/*.svg` |
| **Sound events** | Pass. Five events, each exactly one sound per occurrence, including rapid repeats and a held input: automated (`test_sound_triggers.gd`) and heard in playtest 5. | Automated checks; playtest 5 |
| **Music** | Pass. The loop repeats without a click or gap (3x preview and playtest 5); pause resumes from the same point, fail stops it, the exit stops it and leaves silence, as predicted. At -8 dB on the Music bus the music sits well under the effects (playtest 5). | `assets/audio/MUSIC-EDIT-LOG.md`; playtest 5 |
| **Muted play** | Pass. Every event reads with both buses muted (playtest 6; also playtest 4 before audio existed). | Playtests 4 and 6 |
| **Automated check** | Pass. `test_sound_triggers.gd` counts sound triggers per event during a scripted route through the slice and in edge cases: `WALKER TESTS: 11 checks / 0 failures`. | Automated checks |

### Character against the sheet — differences
In-engine frames: `design/checks/engine/states-vs-sheet.png` (row 1: accepted Gemini pose; row 2: facing right; row 3: facing left).
- All 8 slice states swap correctly (idle, run, rise, fall, cast, hurt, fail, win) and mirror cleanly with `flip_h`. run_passing is on the sheet but not used by the slice (run shows run_contact; CHARACTER-SHEET Revision 2).
- The tunic is olive green in the Gemini art but gray-brown in engine: the cleanup maps it to the sheet's tunic colour #6B5A4E (palette revision 1).
- The eyes are a forced 2x2 red block in open-eye poses, larger than in the art (CHARACTER-SHEET Revision 3).
- The cast pose's yellow-green crystal glow is removed; the crystal is solid red.
- Fine detail (bows, belt pouches, ember charm) merges at 64 px, as expected at that size.
- Collision: the 14x44 rectangle matches the sheet in every pose; in RISE and FAIL it covers part of the head (known limitation; `design/character/collision.png`).

### Storyboard against the slice
| Panel | Storyboard | In engine | Differences |
|---|---|---|---|
| P1 first view | `design/storyboard/01-title.svg` | `design/checks/engine/P1-first-view.png` | No title screen or push-in: the slice starts directly in play. The mage at the bottom of the dark cave matches. |
| P2 core action | `design/storyboard/02-core-action.svg` | `design/checks/engine/P2-core-action.png` | Fireball from the crystal to the crosshair at the growling wolf (lunge image), as drawn. No stalactite or SFX-ROCK (cut). |
| P3 success | `design/storyboard/03-success.svg` | `design/checks/engine/P3-success-flash.png`, `P3-success-down.png` | White flash, then the down image; the wolf then disappears (no collapse frames, no particles; CHANGE-BRIEF Revision 2). Held close-up is not used: the game camera stays medium. |
| P4 failure | `design/storyboard/04-failure.svg` | `design/checks/engine/P4-failure.png` | Matches: the dark pit between marked edge caps, "Fell into the dark", camera frozen. A pit fall shows the fall image (the kneeling fail image is for HP 0). |
| P5 retry | `design/storyboard/05-recovery.svg` | `design/checks/engine/P5-retry.png` | Jump over the same pit with full hearts after the reload. No heal icon (heal cut). |
| P6 boss | `design/storyboard/06-boss.svg` | — | **Not covered** (boss cut, CHANGE-BRIEF Revision 2). |
| P7 end | `design/storyboard/07-end.svg` | `design/checks/engine/P7-end.png` | Win image at the code-drawn exit of pale light, "CLEARED / R to play again", silence after SFX-CLEAR. The exit is open from the start (no boss to defeat). |

### Inspect-and-revise cycles (driven by observation)
1. **Palette revision 1** (CHARACTER-SHEET Revision 3): on the cave-tone contact-sheet row the stockings, boots and hat brim disappeared (predicted failure 3); skin mapped to gold and the staff head dithered. Measured the cave (L* p5 4.7, p50 8.7), lifted the dark steps, fixed skin, crystal and eyes; before/after: `design/checks/mage-palette-revision1-before-after.png`.
2. **SFX clipping**: the first Stable Audio run clipped in 10 of 18 files; regenerated with the same seeds at -6 dB (`design/audio/sfx-gen-log.md`).
3. **Head-size measure**: the first sprite scaling used face height, which varied about 20% with hair and hat; switched to face width, which is stable within 1% (`tools/clean_sprites.py`).
4. **Thin outlines**: the staff turned entirely into outline colour and vanished on the cave tone; outlines are now only drawn where the shape keeps a fill pixel behind them.
5. **Music source**: Suno could not be used without paying (0 downloads on the free account); switched to Google Gemini (Lyria) (CHANGE-BRIEF, SOURCES.md).
6. **Cast pose design**: CHAR-CAST v1 thrust the staff forward across her body, and the author realised a forward-pointing pose does not fit mouse aiming in any direction; the cast was redesigned as a raised staff. v2 did not raise it and had a yellow-green glow too close to the green screen; v3 was accepted, and v4 came back unchanged (SOURCES.md).

## Playtest notes (human)

### Playtest 1 — 2026-10-06, after S2 (source revision `2667fc9`)
- **Who / how:** the author, playing with the keyboard in the 1280x720 window (640x360 viewport, 2x).
- **Covered:** running and turning, full and short jumps, clearing the pit at a run, walking into the pit, the 1.2 s reload, camera follow, readability against the cave.
- **Result:** movement, jump height, the pit and the 1.2 s reload all feel fine; the camera follows smoothly; the mage stays readable against the cave. No changes needed.
- **Not covered yet:** cast, wolf, exit, HUD and fail text, pause, mute, sound (later steps).

### Playtest 2 — 2026-10-06, after S3 (source revision `5156280`)
- **Who / how:** the author, keyboard and mouse in the 1280x720 window.
- **Covered:** casting in every direction (up, behind her, down into the ground), turning to cast behind her while running, rapid clicking, casting mid-jump, finding the crosshair.
- **Result:** fireballs go where the crosshair is in all directions; turning to cast behind her feels natural; the 0.35 s cooldown and the 260 px/s fireball speed feel right; the crosshair is easy to see; the cast pose looks fine mid-jump. No changes needed.
- **Not covered yet:** wolf, exit, HUD and fail text, pause, mute, sound.

### Playtest 3 — 2026-10-07, after S4 (source revision `40595ce`)
- **Who / how:** the author, keyboard and mouse in the 1280x720 window.
- **Covered:** approaching the wolf, reacting to the growl, taking lunge hits, knockback, defeating it with two fireballs, losing all 5 HP.
- **Result:** the 0.5 s growl gives enough time to react; the lunge feels fair and only hits on visible contact; the knockback reads clearly; the white flash and the down image read as defeated; the 36 px wolf reads as a threat next to the 64 px mage.
- **Issue observed:** HP 0 feels abrupt, because there is no HP display yet. Addressed in S5 (HUD hearts and the "Out of HP" text).
- **Not covered yet:** exit, HUD and fail text, pause, mute, sound.

### Playtest 4 — 2026-10-07, after S5 (source revision `61e0189`) — preliminary muted run
- **Who / how:** the author, keyboard and mouse in the 1280x720 window. The slice had no sound yet, so this was effectively a muted run; the formal muted and sound-on runs follow after S6.
- **Covered:** losing all HP, reading the hearts, finding and entering the exit, the Cleared screen, pausing and resuming, reading every event without sound.
- **Result:** HP 0 no longer feels abrupt with the hearts and "Out of HP"; the hearts are readable; the exit reads as the way out and her hair still feels like the brightest shape; pause stops and resumes cleanly. Every event reads without sound: cast, wolf hit flash and defeat, hurt (image, knockback, blink, lost heart), fail text, Cleared screen.
- **Issue observed:** the HUD's smooth built-in font clashes a little with the pixel art. Logged as a known limitation; no change now.

### Playtest 5 — 2026-10-07, sound on, final audio (source revision `74c0443`)
- **Who / how:** the author, keyboard and mouse in the 1280x720 window, with the final SFX OGGs and MUS-LOOP.ogg.
- **Covered:** every sound event in play, fast clicks and holding cast, the music loop over repeats, Esc pause, a fail, the exit, M and N.
- **Result:** every event made exactly one sound, including fast clicks and holding cast; the music looped with no click; pause, fail and clear behaved as predicted (CHANGE-BRIEF music behaviour); M and N each muted only their own bus.
- **Music level (Music bus at -8 dB):** sits well under the effects; kept at -8 dB.

### Playtest 6 — 2026-10-07, muted, final audio (source revision `74c0443`)
- **Who / how:** the author, with both buses muted (M and N).
- **Result:** every event still reads without sound (CHANGE-BRIEF failure case 7, assignment check "Muted play").

## Known limitations
- HUD text uses Godot's smooth built-in font, which clashes a little with the pixel art (playtest 4). A pixel font is a later change.
- The fixed 14x44 collision rectangle covers part of the head in RISE and FAIL (CHARACTER-SHEET Revision 3).
- Code-drawn, not generated: the exit (ENV-EXIT), HP hearts (UI-HEART), crosshair (UI-CROSSHAIR) and the dark fill in the pit.
- Storyboard P6 (boss) is not covered by the slice (CHANGE-BRIEF Revision 2); neither are the heal spell, spikes and stalactites.
- No title screen (storyboard P1 shows one); the slice starts in play.
- Final audio is in: the five SFX OGGs (Stable Audio Open) and MUS-LOOP.ogg (Google Gemini, Lyria). The code-made placeholder tones (`audio/placeholder_tones.gd`) remain only as a fallback if an OGG is missing; none is used in the current slice.
- The Music bus is at -8 dB, confirmed in playtest 5 (the music sits well under the effects).
- When the game window is closed, Godot prints "2 resources still in use at exit" for `MUS-LOOP.ogg` (see below).

## Automated checks

All commands run from the project folder (`fall-2026/zhefan-z/assignment-2/walker-magic-zhefan`). The Revision column is where the result was first recorded; **every suite was re-run on a fresh copy of `74c0443` and passed (73 checks)**.

| Check | Command (from the project folder) | Result | Revision |
|---|---|---|---|
| Player states, facing, jump, pit, collision vs sheet | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_player.gd` | `WALKER TESTS: 11 checks / 0 failures` | `2667fc9` |
| Cast: spawn at the crystal, aim, facing, walls, held and rapid input (real `Input`) | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_cast.gd` | `WALKER TESTS: 11 checks / 0 failures` (held 2 s: 1 cast; tapping 2 s: 6 casts, cooldown 0.35 s) | `5156280` |
| Wolf: patrol, 0.5 s growl telegraph, lunge, hurt + knockback + blink, HP 0, flash, down image, removal, one defeat for two same-frame fireballs | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_wolf.gd` | `WALKER TESTS: 13 checks / 0 failures` | `40595ce` |
| Flow: HUD hearts, fail texts, exit and Cleared once, input stops after clear, R restart only after clear, Esc pause/resume, no pause after fail or clear | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_flow.gd` | `WALKER TESTS: 14 checks / 0 failures` | `61e0189` |
| Audio: buses and routing, OGG or placeholder per sound, each event sound once, music on load / pause / fail / clear, M and N mute, identical game state muted vs unmuted (dummy audio driver: counts play requests, not what is heard) | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_audio.gd` | `WALKER TESTS: 13 checks / 0 failures` | `e53a601` |
| **Sound triggers per event (the slice's required automated check)**: a scripted route through the whole slice with the real wolf AI (run, jump the pit, shoot the wolf until defeated, reach the exit), repeated muted; plus held cast, rapid taps, two fireballs into a 1 HP wolf in one frame, same-frame and invulnerable hits, real lunges for 4 s, pit twice + HP 0 in one frame, exit twice | `Godot_v4.7.2-stable_win64_console.exe --path . --headless -s res://tests/test_sound_triggers.gd` | `WALKER TESTS: 11 checks / 0 failures`. Route: 5 casts → 5 SFX-CAST, 1 SFX-WOLF-DOWN, 0 SFX-HURT, 0 SFX-FAIL, 1 SFX-CLEAR, music started once and stopped at the exit; muted route identical. Held 2 s: 1 cast; tapping 2 s: 6; two same-frame fireballs: 1 wolf-down; 3 landed lunges: 3 hurt; double fail: 1; double exit: 1 | `74c0443` |

All suites run with the final SFX OGGs and MUS-LOOP.ogg in place (all 73 checks pass). Headless uses a dummy audio driver, so these checks prove the triggers and the music state, not what a listener hears; that is the sound-on playtest.

Observed, not fixed: when the game window is closed, Godot prints "2 resources still in use at exit" for `MUS-LOOP.ogg`. It appears only at shutdown, does not affect play or the tests, and stopping and releasing the music player on exit did not remove it; root cause not found.

Measured during S5: the code-drawn exit's brightest pixel is L* 89.0, below the hair base (L* 91.7) and highlight (L* 97.3), so the hair stays the brightest shape on screen (pillar 3, CHANGE-BRIEF failure case 3); the margin is small and is a human check in playtest 4.

In-engine evidence images were captured with `tests/capture_scene.gd` (real renderer, 1x frames) and composed into `design/checks/engine/`.
