# FACTCHECK — every claim in the narration and on screen, with its source

Written by Claude Code, 2026-11-22, before the master compile. The script is `PLAN` in `scripts/sheet.py`; the voice reads the same words with a few tokens spelled for speech (`SAY` in that file: "H-D two-D", "R-T-X fifty-sixty", "zero point zero two"). Tense rule: past tense only for what exists and is shown; everything else "will".

## Narration

| Beat | Claim | Source | Shown as |
|---|---|---|---|
| B00 | A wolf growls before it lunges; a hit during the growl cancels the lunge | `capture/run-01-inputs.jsonl`: `wolf_hit` frame 1549, `prev_state` GROWL, `state` RECOVER; expectation `cancel` (0 lunges, hitbox never armed) | real capture, 840b501 |
| B00 | "my game as it runs today, played by scripted input" | CAPTURE.md (840b501 is the A7 tip; driver = scripted input) | label on every frame |
| B01 | Name, genre, one cave level, fireballs, a great wolf; a playable Windows build of one vertical slice | PROJECT-BRIEF.md §1 | future tense; title card labelled Constructed |
| B02 | Octopath Traveler's HD-2D look, Metal Slug-style shooting, mouse-aimed fireball; Octopath turn-based, Metal Slug fixed directions, Hollow Knight large cave with progression; "I've played all three"; a short action run | PROJECT-BRIEF.md §2 | text only; no footage, art or logos of those games |
| B02 | the fireball is aimed by the mouse (present: it exists) | 840b501: `capture/run-01-inputs.jsonl` `click` rows (aim sent = aim seen) | — |
| B03 | Depth of field, bloom, cold blue cave / warm fire, light shafts through fog, fireball as moving light; visual only; the pin will still pass | PROJECT-BRIEF.md "The look (planned)" | Constructed - proposed, not built |
| B04–B06 | Four short, skippable story moments with portraits; the five lines; a campfire line after the first fight; the sad portrait for a defeat | PROJECT-BRIEF.md "The look" → Story moments; the lines and the defeat portrait from the author's film request (`prompt-1-pitch.txt`, beat 4) | Constructed dialogue scenes; portraits labelled Generated (Gemini 4) |
| B07 | Target role gameplay programmer; reader a hiring manager or lead gameplay programmer; unzip, double-click the exe, controls on the title screen, one key skips the opening line, playing within a minute | PROJECT-BRIEF.md §3 | Constructed - proposed, not built |
| B08 | "It will prove I can build and verify gameplay systems" | PROJECT-BRIEF.md §4 | — |
| B08 | The lunge and the growl cancel "already ran in Assignment 7" | A7 TEST-REPORT.md at 840b501 (Pins, Edges); this film's capture at 840b501: hurt on 1009, cancel on 1549 | real capture, 840b501 |
| B09 | Pinned every physics tick before the change; only the two scenarios with a hit during the growl changed | A7 TEST-REPORT.md at 840b501, "Pins": "only `hit_growl` and `kill` differ, both from tick 24 (GROWL → RECOVER)"; `captures/figures/pin_timeline.png` | figure from the logs, 840b501 |
| B09 | Thirty-eight headless test runs passed in a fresh clone | PROJECT-BRIEF.md "Exists today"; verified in Part 1 of this session: the Assignment 7 session's fresh clone of 840b501 (the result the A7 TEST-REPORT.md points to the Canvas note for) ran 8 suites at 30/60/144 and 14 at 60 = 38 runs, all exit 0; the 38 committed logs at 840b501 (35 `test_*`, 3 `probe_two_clocks`) all end "0 failures" (`scripts/cards.py` asserts this when it draws the table) | table from the committed logs |
| B09 | Frame time for the slice will be measured on an RTX 5060 Laptop GPU | PROJECT-BRIEF.md "The look" and §4 | future |
| B10 | In / out / first; how anyone would know the first room ran | PROJECT-BRIEF.md §5 | Constructed - proposed, not built |
| B11 | The risk, the two options, the one-room spike, the pin as the test, the fallback | PROJECT-BRIEF.md §6 | Constructed - proposed, not built |
| B12 | Half learning, half showing; new: HD-2D, a 3D cave, its lighting and camera, 2D sprites placed in 3D | PROJECT-BRIEF.md §7 | Constructed - proposed, not built |
| B13 | The hurt-tint shader from Assignment 5 | 2b68e0a: `shaders/hurt_tint.gdshader`, `features/player/hurt_tint_driver.gd`; `capture/a5-run-01-frames.jsonl` (tint 0.98 → 0 over 59 frames) | real capture, 2b68e0a |
| B14 | Fireball particles from Assignment 6, measured at about 0.02 and 0.10 ms of GPU time on an RTX 5060 Laptop GPU | A6 TEST-REPORT.md at 7672d5a lines 62–73 ("Over case 1 ≈ 0.02 ms / ≈ 0.10 ms", Visual Profiler, RTX 5060 Laptop GPU; the 0.10 case is an upper bound with 18 trails) | real capture, 3c37fe0 |
| B15 | The run cycle, state machines and tests from Assignment 7 | A7 TEST-REPORT.md at 840b501 | real capture, 840b501 |
| B16 | Exists today / will exist lists | PROJECT-BRIEF.md "Exists today" (verified against git in Part 1) and "Will exist" | Exists: in git at the revision shown · Will exist: proposed, not built |

## On screen only

| Beat | Text | Source |
|---|---|---|
| B01 | "Background: Real capture · scripted input · revision 840b501 · frame 15" | `capture/run-01-frames.jsonl` row 15: segment run, mage IDLE |
| B09 | the test table (suite, rates, checks) | `logs/*.log` at 840b501, read with `git show`; counts parsed from each log's last "checks / failures" line |
| B09 | "Measured cost (Assignment 6, RTX 5060 Laptop GPU) … about 0.02 and 0.10 ms" | as B14 |
| B16 | revisions per row: 840b501, 7672d5a, 2b68e0a, "Assignment 3", "pitch/art/" | PROJECT-BRIEF.md "Exists today"; each checked with `git branch --contains` in Part 1 |
| B00/B08 | chips: frame number, mage and wolf state, wolf HP, the hit | `capture/run-01-frames.jsonl`, `capture/run-01-inputs.jsonl` |
| B13 | chips: mage state, HP, hurt-tint intensity | `capture/a5-run-01-frames.jsonl` (intensity read from the shader uniform) |

## Not claimed

- No player, playtest, quote, wishlist, download, metric or result is invented. The only numbers are 0.02, 0.10 ms (A6 measurement, machine named), 38 runs and 30/60/144 fps (A7 logs), the frame numbers and HP values (capture logs), and the counts in the test table (committed logs).
- No frame rate of the film's captures is claimed: Movie Maker renders offline at a fixed step.
- Nothing proposed is shown as built: every drawing of a planned feature carries "Constructed - proposed, not built".

## Corrections recorded while checking

- ART-PROMPTS.md says the film labels the concept art "Generated (Gemini 4) · concept, not in the game"; the author's film request asks for "… · concept art, not in the game", which is what the film shows. ART-PROMPTS.md is left as written.
- ART-PROMPTS.md says Gemini returned the expression sheet and the two wolves "on white"; the committed files have flat green (#00FE00-ish) backgrounds. Left as written; reported to the author.
