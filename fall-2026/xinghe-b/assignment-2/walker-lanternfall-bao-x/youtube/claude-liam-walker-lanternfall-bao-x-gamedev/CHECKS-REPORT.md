# CHECKS-REPORT

## Beat classification (SHOW / HOLD / CARD)

34 beats: **31 SHOW · 0 justified HOLD · 3 CARD · 0 PUNT**

| Beats | Class | Why |
|---|---|---|
| B00, B32 | SHOW | the Claude composer types the ask / the Your Turn prompt (bookends) |
| B01 | SHOW | the hesitant writer types the arriving framing and corrects "game" → "assets" on the spoken word |
| B02 | SHOW | verbatim CONCEPT excerpt; each pillar card lights as it is named |
| B03, B15, B20, B25, B26 | SHOW | real engine footage with its own game sound; the event log fills in as each sound plays |
| B04–B06 | SHOW | the asset trace: blockout and rules, rejected raw output and rewritten prompt, then the edit chain stage by stage — each element appears on its phrase |
| B07, B09, B11, B13, B16, B18, B21, B23, B27 | SHOW | verbatim code; the line being spoken is highlighted |
| B08, B10, B12, B14, B17, B19, B22, B24, B28 | SHOW | the visible result of the code beat before it: real footage (B28: recorded test output) |
| B29, B30 | CARD | the assignment asks for who did what, which model made each asset, and tests/uncertainties/next steps; each column appears as it is spoken; the two boards are not adjacent |
| B31 | CARD | the verdict artifact (bookend) |
| B33 | — | the locked outro card |

## Teaching arc

FRAMEWORK ✓ (B02 concept and pillars, B04 the rules every frame must meet) · WORKED EXAMPLE ✓ (B04–B08: one asset from design to Godot) · FALSIFIABILITY ✓ (B17 before/after; B27–B28 the independence check would fail if sound changed the game) · SCAFFOLDED TASK ✓ (B32: one change, a prediction first, a test that answers it; answer key checked) · BOOKENDS ✓ (B00 ask, B01 BLUF, B31 verdict, B32 Your Turn, B33 outro) · NO-SOURCE-NO-VERDICT ✓ (every judgment in RIFF.md points at evidence on screen)

## Assignment film items

| # | Item | Where |
|---|---|---|
| 1 | concept and pillars | B02 |
| 2 | one asset: design → prompt → raw → edits → Godot | B04, B05, B06, B07–B08 (ART-PC-01, walk_contact) |
| 3 | at least two character states | B09–B10 (seven poses), also B08 |
| 4 | four SFX on real game events | B03 (kill, pickup, level-up), B20 (hurt, level-up, evolve), B26 (hurt, lose), B15 (level-up), all labelled from the take's play log |
| 5 | a game-sound-only segment, no narration | B03, B15, B20, B25, B26 |
| 6 | a source change → what the player sees or hears | B16–B17 (hit test, before/after from builds 40102ab and 8a6f988) |
| 7 | tests, uncertainties, next steps | B27–B28, B30 |
| 8 | who did what (Bao, Claude, models) | B29 |
| 9 | which model made each asset | B29 |
| 10 | source revision shown | every code panel's footer, B00 output line, B31 heading |

## Checker and gates (2026-10-01, final master)

| Check | Result |
|---|---|
| `./art godot-gamedev --check REEL --game godot` | **PASS** — 72 source files hashed + 3 exclusions = all 75 authored files; 11 components; 9 exact excerpts; teaching contract `code-then-result-v1` with 9 code/result pairs, each result clip hashed |
| `qc/beat_lint.py` | clean |
| `qc/gate_shape.py` | not applicable (finance-only gate) |
| `./art final --height 2160 --fps 30` | **ready** — `exports/landscape/claude-liam-walker-lanternfall-bao-x-gamedev.mp4`, 583.9 s, H.264 3840 × 2160 30 fps + AAC, 34/34 slots filled, no slates; no clip was retimed, slowed or centre-cut (compile log) |
| Gate V (`qc/final_frame_check.py`, beats at 50 % and 85 %) | **0 BLOCKER · 0 MAJOR** in 68 frames (`_qc/REPORT.md`); game-sound beats decoded and covered |
| Audio sync (`tools/check_sync.py`) | every game-sound beat matches its take at **0 ms** offset (±0.04 ms), correlation ≥ 0.999 — the frame-based SFX labels sit on the sounds |
| Film SHA-256 | `585a89d4a1818588e659e20b69f835176d490790bf03f49efec30b5538ddc779` |

Defects found by the pre-checks and fixed before the final: B01 text crossing the left title-safe edge (font 200 → 180), B06 low contrast (light checkerboard → the game's ground colour), B22 image crossing the right edge (narrowed), B13 third note clipped, B16/B18/B27 excerpts too long for the panel, four composed clips (B06, B14, B22, B29) one frame short of the compiler's frame count (now `ceil`), and the outro's audio (its render carries no sound; the stock jingle is now its audio).

## Visual QC (frames read by Claude; Bao still needs to watch the film)

Read: every beat at its midpoint from the final master (three contact sheets), every composed beat at several points during the build, and the code panels at full size. Checked: code readable at the panel size; highlighted line matches the narration; editor-reconstruction label and source path/lines on every code beat; held frames, frame-by-frame steps and diagnostic overlays labelled (B10 defeat, B17); one @NikBearBrown per beat (no channel-title overlay on B00); the outro restates the exact title. Loudness levelled (SOURCES.md): narration −17 to −19 LUFS, game-sound beats −16 to −21 LUFS, outro jingle −15.5 LUFS.

Known, accepted: the levelup-pose crop in B10 includes the capture's own "Real engine capture · scripted input" label; B25's event log lists kill sounds while the master bus is muted (they still fire; the mixer silences them — that is the point of the beat).
