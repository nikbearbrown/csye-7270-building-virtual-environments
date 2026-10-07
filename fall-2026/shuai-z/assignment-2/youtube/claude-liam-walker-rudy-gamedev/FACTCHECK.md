# FACTCHECK — every spoken number and checkable claim

Source paths are relative to `walker-rudy/`; `game/` is at `3b7aa1c`.

| Beat | Claim | Value | Source |
| --- | --- | --- | --- |
| B00 | Course | CSYE 7270 | README.md |
| B00 card | 16 Rudy frames · 6 sound effects · 1 loop · 141 checks | 16 / 6 / 1 / 141 | `rudy_look.gd` FRAMES (16 entries); `sfx.gd` STREAMS (6); `music.gd` LOOP; `capture/checks-run.log` (141 PASS) |
| B00 card | Started from an empty repository | — | project SOURCES.md "Starting point" |
| B01 | Models made pictures, sounds, music; code makes one game | — | project SOURCES.md, ASSET-LOG.md |
| B02 | Design committed before generation | tag `design-v1` | README.md; CHANGE-BRIEF.md header |
| B02 | Two sentences and four pillars | verbatim | CONCEPT.md |
| B05 | Two gaps, 210 px and 200 px | 4510 − 4300; 6600 − 6400 | `level_1.tscn` Segment positions and sizes |
| B05 | Two rows of spikes, three goblins, one pickup, waystone, circle | — | `level_1.tscn` |
| B05 | 7,700 px end to end | Bounds/Right x 7700 | `level_1.tscn:94` |
| B05 | Sky at two percent, fields at forty | 0.0218, 0.4 | `backdrop.gd:20–21` |
| B06 | No music call in `_start_play`; music started in `_ready` | — | `main.gd:79, 105–111` |
| B08 | Hold timer 120 ms | `turn_hold_time := 0.12` | `rudy.gd:57` |
| B10 | 1,500 px/s up; heavier gravity down | 1500; 4000 / 6400 px/s² | `rudy.gd:58–60` |
| B10 | Apex 294 px, rise 0.38 s, fall 0.32 s | as stated in the source comment | `rudy.gd:60` (not re-measured) |
| B11 | Key held for a second and a half: one takeoff, one sound | 90 ticks held | `capture/run-03-inputs.jsonl` mark "jump held for 1.5 s", check "a held key jumps once, one sound" |
| B12 | Run frames alternate every eighth of a second | `run_frame_time := 0.125` | `rudy.gd:61, 308` |
| B12 | Sixteen frames, fifteen lines | 16; lines 295–309 | `rudy_look.gd:15–32`; the excerpt |

Note (2026-10-07): B12's narration says the frames are "chosen by a dozen lines"; the excerpt is fifteen lines (`rudy.gd:295–309`). "A dozen" is a round figure in the rendered film and is left as spoken.
| B13 | Rise, then fall at the top because he was moving | debug line CHAR-RISE → CHAR-FALL | run-03 frames 272–293 |
| B14 | Pose seven; drawn by Claude in code | — | CHARACTER-SHEET.md table; poses.png footer "code-drawn by Claude · not a generative-model output" |
| B15 | First output leaned toward the hit; rejected; one-sentence edit; second accepted, nearly flat, gold motifs | — | ASSET-LOG.md rows CHAR-HURT-01, CHAR-HURT-02 |
| B16 | Scale 0.1816; background colour sampled; 2 texture px per game px | `scale`, `background_rgb`, `density` | `frames.json:111–117, 341`; ASSET-LOG.md |
| B16R | Frame on its 410×386 canvas, origin 205, 370, no outline in the file | — | `frames.json:342–349`; `rudy_look.gd` header (outline is the material) |
| B17 | Hearts 3 → 2, hurt cry, music dip | dip −6 dB | run-02 log frames 79–80 (`hearts`, `sounds: hurt`, `music_db`) ; `music.gd:23` |
| B18 | Hair vs wheat contrast 1.71 | 1.71 | TEST-REPORT.md predicted failure 2 |
| B18 | Three rings, eight texture px | `ring <= 3`; width 8 | `outline.gdshader:29–30`; `outline.tres:7` |
| B19 | With the outline: contrast 11.13 (on screen in B18's notes) | 11.13 | TEST-REPORT.md |
| B20 | Overlap list reports two ticks late | — | `goblin.gd:8–10` comment |
| B20 | Soles at most 14 px below the top | `STOMP_MARGIN := 14.0` | `goblin.gd:23, 105` |
| B22 | Hitbox 50 px in front; live 0.03–0.18 s of a 0.3 s swing | 50; 0.03; 0.18; 0.3 | `rudy.gd:66–69` |
| B24 | 1.2 s invulnerable | `invulnerable_time := 1.2` | `rudy.gd:75` |
| B25 | Gear flies, hearts stay at two | — | run-02 frame 243 check "the hit takes the gear, not a heart" |
| B26 | Music dips 9 dB through fade and respawn | `DEATH_DIP := -9.0` | `music.gd:25`; `main.gd:122, 139` |
| B27 | Two hearts → one, back at the waystone | x 4120 | run-02 checks at frames 393 and 432 |
| B29 | Back at the opening, three hearts, waystone dark | x 300 | run-02 check at frame 546 |
| B30 | Hit on the last heart dips 9 dB, not 15 | — | `music.gd:11–12` comment; `target_db` |
| B30 | Ramps over 0.15 s | `RAMP_TIME := 0.15` | `music.gd:26` |
| B31 | Music twelve decibels down while paused | −12.0 dB | `music.gd:22`; run-03 log `music_db` while `paused` |
| B33 | Muted jump still counted | — | run-03 check "muted, the jump still calls Sfx.play once" |
| B34 | Music fades over 1.5 s; end card after 2 s | 1.5; 2.0 | `music.gd:27`; `main.gd:43` |
| B36 | 141 headless checks; same route twice, buses muted | — | `capture/checks-run.log`; `checks.gd:1328–1343` |
| B36 | Checks may teleport Rudy | `_teleport` | `checks.gd:1696` |
| B37 | All checks passed, 141 PASS, exit 0, 733 ticks either way | — | `capture/checks-run.log` (exit code recorded when run) |
| BVD1 | Four native 4K takes; all six sounds on real events | run-01…04 | CAPTURE.md; logs' `sounds` fields (jump, stomp, pickup, slash, portal in run-01; hurt in run-02) |
| BVD1 | shuai-z's playtest, sound on and muted; only player | 2026-10-04 | TEST-REPORT.md "My playtests" |
| BVD1 | Not built: mushroom, spores, blocking; four planned sounds | — | TEST-REPORT.md "Known limitations"; CHANGE-BRIEF.md revisions |
| BVD2 | Which model made which asset | — | project SOURCES.md "Generative models"; ASSET-LOG.md |
| BHTF | STOMP_MARGIN 14 → 4 px | 14 | `goblin.gd:23` (the 4 is the viewer's experiment) |
| BOUT | Title | Walker Rudy, Wired In. | beat sheet metadata |
