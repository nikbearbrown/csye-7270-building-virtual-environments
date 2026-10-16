# FACTCHECK

Every factual claim in the narration and on screen, with where it was checked. Source revision of the game: **8a6f988** (`FILM-SOURCE-REVISION.txt`). "Take" means a real 4K engine capture in `capture/` (CAPTURE.md).

## Corrections made while building the film

| Beat | First draft said | Why it was wrong | Now says |
|---|---|---|---|
| B01, B29, B31 | "Bao made every accept and reject call" | 5 of the 99 runs (MUS-02 rejects) were rejected by an automated layer check that Bao did not listen to; the logs say so | "every one that shipped was Bao's pick"; B29 shows "94 of 99 runs" and the automated-check note |
| B29 | "listened to every sound candidate" | true for the 21 sound-effect candidates, not for the 5 automated MUS-02 rejects | "listened to every sound-effect candidate" |
| B08 | "the hurtbox sat low" | the generated torso sat **below** the hurtbox centre (coat centre y ≈ 22–24 vs 20) | "his torso sat below the hurtbox" |
| B16 | "bullets flew straight through monsters" (as Bao's note) | Bao's words were "子弹 打到怪物之后 要求消失" (bullets should vanish when they hit a monster); TEST-REPORT L1 records what he saw | "Bao saw bullets fly on through monsters, and asked for them to vanish on a hit"; his words are on screen |
| B17 | "this bolt crosses the moth's wing" | the diagnostic shows the bolt touching the wing's sprite box at the tip | "clips the moth's wing" |
| B27 | "the audio suite's full seeded run" | the autoplay bot loses at tick 3817 (1:04), well before 3:00 | "seeded autoplay run" |
| B14, B24 | narration timed to each key press | the real pause lasts 3 s and the mute keys are 2 s apart; narration cannot follow that rhythm without retiming footage | narration describes the sequence; exact key presses are labelled on screen at their real frames |

## Claims by beat

| Beat | Claim | Checked against |
|---|---|---|
| B00 | design first, then art, 4 SFX and a loop with free/local models, in a playable Godot scene | Assignment 2 brief |
| B00 | 23 assets from local models, 99 runs logged | `gen/log/` (23 asset folders, 99 sidecars) |
| B00 | 122 automated checks, two playtests by Bao | `capture/test-run-film-build-raw.txt`; TEST-REPORT §4 |
| B01 | 14 sprites and props, 7 SFX, 2 loops | `godot/assets/manifest.json`; 14 PNG, 7 WAV, 2 OGG under `godot/assets/` |
| B01 | every shipped asset was Bao's pick | `gen/log/*/*.json`: every `modify` decision has `decided_by: Bao Xing` |
| B02 | committed and tagged before any image existed | tag `design-v1` = 46d2fe2 (2026-09-28 15:21 EDT); first generation commit e384933 (2026-09-29 16:57 EDT); `scripts/audit_repo.py --stage final` order check |
| B02 | excerpt and pillar text | CONCEPT.md, "In two sentences" and "Design pillars" (verbatim; pillar cards give the heading and its first sentence) |
| B04 | 32 × 32, lamp 11–13 px, feet on row 31, faces right with a code flip, 5 colours, 1-px outline | CHARACTER-SHEET.md §3, §6, §7 |
| B05 | first prompt: flat-vector sheet, twelve poses; result shaded/3D, grid ignored; rejected by Bao | `gen/log/ART-PC-01/ART-PC-01-20260929T202956Z-s11.json` (prompt, decision, reason, Bao's words) |
| B05 | rewritten per pose; no negative prompt | `…-s11-walk_contact.json` (prompt verbatim on screen; `negative_prompt` field) |
| B05 | FLUX.1-schnell @ 741f7c3, mflux 0.20.0, 4-bit, seed 11, 512², 4 steps, 104 s | same sidecar `settings`; SOURCES.md (revision) |
| B06 | keyed, mirrored, lamp 12 px, palette-locked 32 × 32; re-run equals the shipped frame | `tools/asset_trace_stages.py` → `images/trace/walk_contact-stages.json`: `equals_shipped_frame: true`, lamp 12.0 px |
| B07 | lines 107, 109, 110 do what is said | `godot/features/player/player.gd` lines 106–113 (shown verbatim) |
| B08 | origin (16, 20) → (16, 23); torso 1.7–3.6 px low; test RED → GREEN | CHARACTER-SHEET R3; TEST-REPORT L8 |
| B09 | priority: override, 12 ticks hurt, 8 ticks cast, walk every 8 ticks, idle | `player.gd` 78–87; `tuning.gd` (IFRAME_TICKS 48, HURT_POSE_TICKS 12, CAST_POSE_TICKS 8); `WALK_FRAME_TICKS` 8 |
| B10 | the seven poses on screen are the ones chosen | main take (walk, hurt at run 0:53.9, levelup portrait, sunflare after 0:58.5, victory at 3:00), props take (cast/idle), lose take (defeat) |
| B11 | kill 60 ms / 3 voices; pickup 1 voice; hurt 800 ms; evolve once; simulation clock | `audio_bus.gd` 19–28 and 81–82; `sfx_gate.gd`. Note: kill sounds get a random ±5 % pitch (line 101, global RNG); which sounds play and when is deterministic |
| B12 | kills outnumber kill sounds in a dense wave | counters from the main take: SFX plays from its own `AudioBus.play_log`, kills from the identical dry run's `enemy_killed` signal (main take frames 5670–6128, run 2:34–2:49) |
| B12 | Bao's note "不会连起来" | `evidence/playtest/2026-10-01-runs-A-B.md`, TEST-REPORT §8 |
| B13 | PAUSED low-pass + −10 dB; LEVELUP chime + −6 dB; PLAYING restores; LOST/WON fade + stinger | `audio_bus.gd` 126–148, constants 29–32 |
| B14 | Esc at run 0:40, 3 s pause, timer 0:40 on both sides | main take log: pause at tick 2400, resume at tick 2401, 3 s (90 frames) apart |
| B16 | old test: centre distance < radius + 4 (10 px for a moth); new: 14 px segment vs the visible box; pierce | `git show a51af69`; `session.gd` 273–284; `enemy.gd` 27–38; `tuning.gd` BEAM_HALF_LENGTH 7, hit_half |
| B17 | before: bolt touches the moth's sprite box outside the old circle, no hit, flies on | build 40102ab take, frames 2006–2008; driver diagnostic `pass_through` (first 4015, last 4016, d_min 13.4) with the engine's canvas transform |
| B17 | after: wing-tip hit outside the old circle; next frame the moth is a gem | main take frames 215–216; diagnostic `edge_hit` (first 433, d_min 19.0, i.e. outside 10 px at every sampled tick) |
| B17 | two tests RED → GREEN; "子弹对的" | TEST-REPORT L1, §4 (session 2) |
| B18 | seeded shuffle; Sunflare first when beam 3 and moths 3 | `progression.gd` 76–77, 93–102 |
| B19 | at run 0:58 the Sunflare card leads; banner, zoom-out 0.72, pose, brighter coat, layer | main take log (card offered ['sunflare', …] at tick 3512); `camera_fx.gd`; `audio_bus.gd` 150–155 |
| B21 | movement line; push_out on line 61 before the clamp; enemies not blocked | `player.gd` 56–63; CONCEPT R5 |
| B22 | stopped at the edge, then slides; box = opaque area inset 2 px | props take frames 179–619; `ground.gd` SOLID_BOX comment; overlay drawn from the SOLID_BOX numbers |
| B23 | M / 9 / 0 flip bus mutes only; HUD reads the flags | `session.gd` 362–374; `audio_bus.gd` 198–200; `hud.gd` 49, 79–81 |
| B24 | the HUD line flips; the run continues | props take frames 246–747 |
| B27, B28 | one stinger; seed replayed silent; identical summary | `test_audio.gd` 69–74; recorded run: lost at tick 3817, kills 80, level 7, x −220.11, y 202.53 in both runs |
| B28 | logic 32, gameplay 65, audio 25, all pass | `capture/test-run-film-build-raw.txt` (fresh `git archive 8a6f988`, imported, no script errors) |
| B28 | Run A / Run B quotes, build 1b24721 | `evidence/playtest/2026-10-01-runs-A-B.md`; TEST-REPORT §4 |
| B29 | roles | FRICTIONAL.md header line (Bao's own summary of who did what) |
| B29 | model per asset, revisions | SOURCES.md table; `gen/log/*/*.json` `model` fields |
| B30 | wraith contrast 0.03; hurtbox reaches the lamp; gamepad untested; bot balance; playtests before review fixes | TEST-REPORT §12, §16, §6; README limitations; git history (Runs A/B at 1b24721, review fixes 491892a–8a6f988) |
| B30 | next steps | CONCEPT.md "Semester goal" |
| B31 | source revision 8a6f988 | `FILM-SOURCE-REVISION.txt` |

## Your Turn — answer key (checked, not shown in the film)

Changing `"kill": {"cooldown_ms": 60, …}` to `0` in an isolated copy and running `test_audio.gd`: 20 kills in one tick play **3** kill sounds (the 3-voice cap still holds), and **2** checks fail — `burst-20-kills-one-sfx` (plays 3) and `kill-throttled` (min gap 50 ms < 60). All other checks pass.

## Fixed outside the film

TEST-REPORT §8, §11 and §14 quoted numbers from a build before the code-review fixes (independence at tick 3850, 88 kills, level 8). The committed `evidence/audio.json` at 8a6f988 and the film's fresh run agree (tick 3817, 80 kills, level 7); TEST-REPORT now quotes those, with a note on where the older numbers came from. The repository's SOURCES.md listed FLUX.1-schnell's assets without the five map props (ART-ENV-03 … 07); added.
