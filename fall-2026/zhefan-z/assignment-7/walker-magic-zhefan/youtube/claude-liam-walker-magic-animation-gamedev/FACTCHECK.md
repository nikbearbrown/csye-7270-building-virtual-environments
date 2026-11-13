# FACTCHECK — every spoken claim and its source

Documents and game source at f860fed. "Capture" = `capture/run-01-inputs.jsonl` and `capture/run-01-frames.jsonl` (CAPTURE.md); frame numbers are PNG frames of run-01 (60 fps, one per physics tick). Logs are in `logs/` at f860fed.

| Beat | Claim (spoken) | Source |
|---|---|---|
| B00 | two clips: a run that loops, a lunge that commits; keyed as data; checked tick by tick | CHANGE-BRIEF.md Clip 1 (LOOP_LINEAR), Clip 2 (LOOP_NONE, committing action); CLAUDE.md "Ownership" (keys in .tscn); `tests/test_pin_behaviour.gd` |
| B00 output | run 4 cells, 10 fps, LOOP_LINEAR, discrete; lunge 89 ticks, LOOP_NONE; pin 8 scenarios 16 / 0 and edges 13 / 0 at 30, 60, 144 | `player.tscn` 62–101; `wolf.tscn` 60–146; `logs/test_pin_behaviour_{30,60,144}fps.log`, `logs/test_anim_edges_{30,60,144}fps.log` |
| B01 | keys on the physics tick the game reads; gameplay pinned before the first key | `player.tscn` 417, `wolf.tscn` 249 (`callback_mode_process = 0`); git log: pin `a9b4bc1` before clips `72e8d21` |
| B02 | take_lunge at tick 40, before A7 and now; one picture before; keyed rig, afterimage, torch-lit cave now; gameplay identical | `captures/look/take_lunge_t40_{before,now}.png` (`tests/capture_look.gd`, fixture); README.md image caption; pin `take_lunge` unchanged (`logs/pin/take_lunge.json` byte-identical in `ff71bbb`) |
| B03 | scripted input, real engine output; four cells at ten a second; run, stop, run, jump, land; run restarts at cell 0 on the landing tick | Capture frames 20, 118, 153, 301, 323, 346 (cell 0); `player.tscn` 64, 97 |
| B04 | stops where the wolf first sees her; growls 31 ticks; steps back, lunge misses; recovers; runs past; growls again, turns, lunges right; hits | Capture: GROWL 880–910 (31 frames), A held 24 frames, LUNGE 911–932 facing −1 with no HURT, RECOVER 933–968, PATROL 969, GROWL 970, LUNGE 1001–1022 facing +1, HURT at 1009 (HP 5 → 4) |
| B04 | code flips the Facing node; the clip keys the rig inside it | `wolf.gd` 136–140 (`facing_node.scale.x = facing`); `wolf.tscn` 90, 102, 114, 126 (tracks on `Facing/Rig…`) |
| B05 | the one behaviour change; click as the growl starts; cast on growl tick 2; lands on tick 21; no lunge, straight to recovery, hitbox never arms | CHANGE-BRIEF.md "Behaviour change"; capture: GROWL 1528, cast_fired 1530, RECOVER 1549 (clip frame 53, HP 2 → 1), no LUNGE, `monitoring` false on every frame of the segment |
| B06 | cutout rig from the A2 wolf; two regions overlapping at the waist; hip and shoulder pivots; Muybridge's galloping dog | `wolf.tscn` 216–245; `logs/test_clip_lunge_60fps.log` (parts-are-regions overlap 4 px; pivots at image px (29, 16), (55, 16)); SOURCES.md; `design/a7/reference/SOURCES.md` (plate 707) |
| B07 | phase table from the pin: 31, 22, 36 ticks; keys at frames over 60; scale track crouch, stretch, overshoot | CHANGE-BRIEF.md revision 2026-11-10; `wolf.tscn` 106, 109 |
| B08 | every track resolves; key times = frame / 60; 17 checks, 0 failures; logged rig matched every key | `logs/test_clip_lunge_60fps.log`; TEST-REPORT.md strips row "logged rig values equal the phase table at growl + 0, 25, 31, 37, 53, 65; PATROL at +89"; `captures/figures/lunge_onion.png` |
| B09 | Sprite2D and a frame track over four cells; Gemini from the author's own sprite; cleaned onto the author's palette; Muybridge's runner | CHANGE-BRIEF.md revision 2026-11-12 (run cycle replaced); SOURCES.md; `design/a7/reference/SOURCES.md` (plate 60) |
| B10 | discrete frame track; cells 0–3 at 0, 0.1, 0.2, 0.3 s; looping clip 0.4 s; seam rule | `player.tscn` 64–65, 97–100; CHANGE-BRIEF.md Clip 1 seam rule and revision 2026-11-12 |
| B11 | 6, 6, 6, 7 ticks per cell on entry, then 5, 6, 6, 7 per loop; wraps on the tick it reaches 0.4; 16 / 16 | Capture frames 20–116 (sheet cell per frame); `captures/run/game-r2-ticks/ticks.jsonl`; TUNING.md r2; `logs/test_clip_run_60fps.log` |
| B12 | the state machine only calls play; starts the clip on a state change, from zero; flip_h in code; the structure test scans every script | `player.gd` 143–154; `logs/test_anim_structure_60fps.log` (no-game-script-writes-a-keyed-property: PASS) |
| B13 | falling, then on the landing tick run from cell 0; 11 structure checks | Capture frames 340–351 (FALL → RUN at 346, cell 0); `logs/test_anim_structure_60fps.log` 11 / 0 |
| B14 | pin before any clip; 8 scenarios, every physics tick, real input, 3 frame rates; clips added and wired: unchanged; one change in its own commit | TEST-REPORT.md "Pin first"; git log (`a9b4bc1`, `72e8d21`, `33d78ae` "pin unchanged", `72f37b8`); `tests/test_pin_behaviour.gd` |
| B15 | a growl hit that leaves HP sends the wolf to RECOVER and seeks the recovery section; other phases only lose HP | `wolf.gd` 152–163 |
| B16 | hit_growl differs from tick 24, GROWL → RECOVER, no lunge; kill changed too (first hit in a growl); not predicted; played, accepted, re-pinned: two files; 16 / 16 at all three rates | `captures/figures/pin_timeline.png`; TEST-REPORT.md "Pin first"; FRICTIONAL.md "Predictions"; `git show --stat ff71bbb` (hit_growl.json, kill.json); `logs/test_pin_behaviour_*fps.log` at ff71bbb |
| B17 | clicks timed to land on a boundary; first/last growl tick cancel; first/last lunge tick don't; kill wins everywhere; 13 / 13 at three rates | `logs/test_anim_edges_{30,60,144}fps.log`; TEST-REPORT.md "Edges" |
| B18 | a cancel drew frame 54, now seeks 52; a growl after a one-tick patrol started at frame 1, so both players run first; this capture shows both fixes holding | CHANGE-BRIEF.md revision 2026-11-12; `wolf.gd` 162; `wolf.tscn` 248; `player.tscn` 416; capture frame 1549 (clip frame 53), frames 969–970 (PATROL one tick, GROWL at clip frame 0) |
| B19 | Godot 3 `loop = true` not caught, loads as looping; continuous frame track, cell past the sheet, missing node, no cancel: all caught | `logs/mutation-a7-1…5-*_60fps.log` (16 / 0; 1, 2, 2, 2 failures); TEST-REPORT.md "Mutations"; CHANGE-BRIEF.md revision 2026-11-12 (F1 does not occur) |
| B20 | from sight distance only casts in the first 12 growl ticks (0.2 s) cancel; removal after death on frame time: tick 79 at 60, 80 at 30 and 144 | `captures/figures/growl_window.png`; TUNING.md (growl cancel entry); CHANGE-BRIEF.md revisions 2026-11-10 and 2026-11-12; `captures/figures/two_clocks.png`; `wolf.gd` 170 |
| B21 | r0 two frames; 1 px hat hop; planted foot slides 13–15 px, snaps back; three fixes for the other foot failed | TUNING.md run r0 and "Attempts that failed"; FRICTIONAL.md "Struggle and revision" 2–3; `captures/run/analysis/` |
| B22 | r1 bobbed the body; hat rows exactly as predicted; rejected in play (feet still twitch); r2 four-frame cycle kept | TUNING.md r1 (268 / 270 / 267 / 265), r2; git log `fc096c9`, `338c8bf`, `32eed66` |
| B23 | third clip, continuous tracks on energy and size, 2.4 s, looping; seam: value at 0 = value at the end, 1.6 and 1.6 | `cave_lights.tscn` 19–30, 34, 58; `logs/test_clip_flicker_60fps.log` (seam-rule PASS) |
| B24 | the left torch's pool follows the energy keys, correlation 0.95; 11 of 11 | `evidence/torch-flicker-measurement.json` (measured by `scripts/media.py` on capture frames 0–440: 0.949, offset −1 frame); `logs/test_clip_flicker_60fps.log` |
| B25 | 144 embers; a ghost every 3 lunge ticks, fading in a quarter second; r0 not noticeable, r1 clearly visible; contrast measured up to 3.07; pin 8 / 8 | `embers.tscn` 39; `wolf.tscn` 256–258; TUNING.md visual r0 → r1 (2.57 → 3.07, 2.74 before); TEST-REPORT.md "Every later visual change"; `logs/test_afterimage_*` |
| B26 | foot still slides; growl window 0.2 s by choice; removal on frame time; scripted input, feel is the author's call | README.md "Known limitations"; TEST-REPORT.md "Human checks" |
| B27 | who did what; revision f860fed | FRICTIONAL.md "Human and AI contributions"; git log |
| B28 | built, measured, judged, open | the beats above; FRICTIONAL.md "Still open" |
| B29 | suggested prompt; 110 px/s and 10 fps | `tuning.gd` RUN_SPEED 110.0; `player.tscn` run clip (10 cells per second) |

## Corrections: where a document and the logs disagree, and what the film shows

| Document says | The tree / logs show | On screen |
|---|---|---|
| README: "5 new suites (pin, edges, three clip read-backs, structure, afterimage)" | that list is 7 suites | the film names the suites individually and never says "5 new suites" |
| README: strips are "frame n = tick n" | the capture harnesses add the scene one frame late: Movie Maker frame n shows tick n − 1 (`tests/capture_*.gd` headers; TUNING.md r0) | fixture strips are shown with their own labels only; this film's own capture is one frame per tick from the start of each segment (CAPTURE.md) |
| README: run frames "6 ticks each at 60 Hz" | 6/6/6/7 on entry, 5/6/6/7 per loop (`captures/run/game-r2-ticks/ticks.jsonl`; this capture) | B11 shows the measured counts |
| README / TEST-REPORT: "clip frame = phase tick on all 119 growl ticks" | 119 ticks of the lunge clip across two growl cycles: 89 of one growl–lunge–recover and 30 of the next growl (`test_anim_edges` `ticks_checked: 119`, second growl at tick 170) | B17: "all 119 ticks checked: 89 of one growl-lunge-recover, 30 of the next growl" |
| TEST-REPORT: "It found two alignment bugs" (the edges test) | the first (frame 54) was found by the edges test; the second (frame 1 after a one-tick patrol) in the windowed lunge capture's tick log, then the edges check was extended and verified by removing the fix | B18 labels each bug with how it was found |
| TEST-REPORT cites `wolf.gd:59` and `wolf.gd:150` | at f860fed: `wolf.gd:71` (`_timer = maxf(...)`) and `wolf.gd:170` (removal `create_timer`) | B20 cites `wolf.gd:170` |
| TEST-REPORT: `32eed66` among commits with "pin 16/16 at 30, 60, 144" | at `32eed66` the pin was run at 60 only and was 14/16 (the two known differences, before the re-pin in `ff71bbb`; commit message) | B14 lists `a1b6f44 · 7a9a65e · 272fb39` for "16 / 0 after each" and notes "32eed66 (run r2) shows 14 / 16" |
| TEST-REPORT: "no gap … at 8× in the game strip" (waist seam) | the agent's seam check zoom was 4× of the game pixels | the film makes no seam-zoom claim |

## Corrections made while building

- The first narration measured 7.4 min against the brief's 5–6; it was cut twice (1586 → 1175 words), leaving 6 min 15 s.
- B18's second heading ran past the right margin at the largest type; the layout now checks heading width, and the heading was shortened, with "spotted in the windowed lunge capture's tick log" kept in the text under it.
- B07's third source note was clipped by the workbench's notes column in the pilot; every workbench now has two short notes.
- The capture's frames 441–442, 1089–1090 and 1620–1622 are empty (the scene was freed between segments); B03 first included frame 441 at real speed and the torch measurement included 441. Both now stop before it.
- B02 first showed both whole frames at ×2 with half the card empty; it now shows the same crop of both at ×3.
- The first `art final` was refused by Gate V (B01 under-filled at 54 % of the safe area); the hesitant writer's type was enlarged and the second export passed.
- B10, B12, B15 and B23 first cut their excerpts before the cued line (the workbench does not scroll); the excerpts were narrowed to what shows, with the dropped lines in labelled notes.
