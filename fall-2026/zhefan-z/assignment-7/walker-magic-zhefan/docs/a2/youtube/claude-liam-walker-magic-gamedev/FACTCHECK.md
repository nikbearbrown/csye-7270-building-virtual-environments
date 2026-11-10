# FACTCHECK — walker-magic gamedev film

> Every spoken or on-screen claim, checked against a file at the build shown (`74c0443`, read from a `git archive` snapshot), a recorded test output or a gated capture. Checked 2026-10-07 by Claude Code. Listening to the narration (pronunciation, levels) is the author's check on the master.

## Process decisions on record

- **SLICE AUDIO method (B18, B20).** The skill's compiler strips footage audio (`runtime/scripts/compile.py`, per-clip encode with `-an`), and `docs/PIPELINE-SAFETY.md` keeps ordinary b-roll silent under narration. Per the assignment, the course was asked for its approved method: each SLICE AUDIO beat's `audio_file` is the audio track of the same Movie Maker take, cut to exactly the same interval as its video, with no narration. **Approval (verbal):** verbal approval from the instructor the method is acceptable. Recorded 2026-10-07, as reported by the author; there is no written message.
- **Image prompts (B06).** The author confirmed on 2026-10-07 that all image prompts in `design/IMAGE-PROMPTS-from-chat.md` were sent unchanged.
- **Narration addition.** B25 ends with "Liam, in for Bear." (the skill: "Liam signs off in Your Turn"); every other line is verbatim from the approved `SCRIPT.md`.

## Claims

| Beat | Claim | Evidence | Status |
|---|---|---|---|
| B02 | Two-screen slice; one mage, one wolf, one pit, one exit | `game/main.gd` LEVEL_WIDTH 1280 = 2 × 640; `game/main.tscn`: one Wolf, one PitKillZone/PitDark, one Exit | checked |
| B03 | Build shown `74c0443`; capture copy `5266946` has identical runtime files | `git diff --name-only 74c0443 5266946` → only `assets/audio/MUSIC-EDIT-LOG.md` | checked |
| B03 | The six requirements | The author's film brief to Claude Code (2026-10-07), summarised on the card | checked |
| B04 | Pitch and four pillars | `CONCEPT.md` line 7 (excerpt verbatim), lines 26–29 (pillar names verbatim; card lines are interpretations, labelled) | checked |
| B05 | 64 px with the hat; not chibi; 1:3.5; six colours + outline; 14×44 feet to chin | `CHARACTER-SHEET.md` lines 9, 10, 46, 50–60 | checked |
| B06 | Three prompts word for word; setup message uploaded the reference + 9 sketches | `SOURCES.md` → Image prompts (verbatim from `design/IMAGE-PROMPTS-from-chat.md`); author: sent unchanged | checked |
| B06/B23 | Model shown in the app: Gemini 3.8 Flash | `SOURCES.md` → Image prompts header | checked |
| B07 | Raw output 1920 × 2184 on green, not the game | `design/character/generated/CHAR-IDLE-v1.jpg` (image header; EDIT-LOG bg #21E403); card labelled RAW GEMINI OUTPUT — not in engine | checked |
| B08 | Keys green; idle scaled to 64 px; other poses sized by face width; face height ~20% drift, width within 1% | `tools/clean_sprites.py` line 427 (key_green), 442–443 (comment), 456–459; `tools/sprites.json` idle_height_px 64 | checked |
| B09 | 62 × 69 px; every pixel on the palette; logged with hashes | `assets/sprites/EDIT-LOG.md` idle row: size [62, 69], out_height 64, colours 14, off_palette_px 0, binary alpha; `edit-log.json` sha256 entries | checked |
| B10 | No animation; one image per state; texture swaps on state change | `features/player/player.gd` 17–26 (TEXTURES), 130–133 (`_set_state`); no AnimationPlayer/AnimatedSprite in any `.gd`/`.tscn` | checked |
| B11 | Idle, run, up, down, over the pit, landing; scripted input | run-01 frames 0–555; jump pressed tick 294; CAPTURE.md gate PASS | checked |
| B12 | Stockings, boots, brim mapped to the outline colour and vanished; rule lifts them one step | `assets/sprites/EDIT-LOG.md` observed_issue + palette_revision; `tools/clean_sprites.py` 130–151 | checked |
| B13 | Darks from L* ~7 to 20–40; cave darkest ~5 | EDIT-LOG: outline 7.4 → indigo-shade 20.7, tunic-shade 25.9, tunic-base 39.6; cave L* p5 4.7 | checked |
| B14 | Faces the cursor, one fireball at the crystal, 0.35 s cooldown, a held button doesn't repeat | `player.gd` 101–112, 212–218 (`is_action_just_pressed`); `tuning.gd` 13; test re-run `cast-held-2s-plays-once` PASS | checked |
| B15 | Half a second of growl; first hit flashes, second puts it down, then gone | `wolf.gd` GROWL_TIME 0.5, MAX_HP 2, FLASH_TIME, DOWN_TIME 0.6; run-01 log: casts 8.817/9.183 s, wolf_down 9.317 s | checked (growl start derived ±1 tick, SHOTLIST) |
| B16 | Game announces events, one node plays; muted game behaves the same, tests check it | `audio/audio_director.gd` 40–50; test re-run `muted-route-identical` PASS | checked |
| B17/B18 | Five events, five sounds, heard in the take | run-01/run-02 logs; CAPTURE.md audio levels per event window | checked |
| B19/B20 | M = Music bus, N = SFX bus; with N her cast is silent | `game/main.gd` 64–69, `session_input.gd` 11–14, `controls.gd` 9–10; run-03 RMS silent 2.92–3.4 s (CAPTURE.md) | checked |
| B21 | A scripted route counts sound requests per event against the game events | `tests/test_sound_triggers.gd` 103–113, 118–123 | checked |
| B22 | 11 checks / 0 failures; 5 casts → 5 sounds; held → 1; two same-frame fireballs → 1 defeat; headless dummy driver | `evidence/test_sound_triggers-74c0443.log` (re-run 2026-10-07 on a fresh import of the 74c0443 archive) | checked |
| B23 | Which model made which asset; code-drawn exit, hearts, crosshair, pit fill; Stability notice | `README.md` lines 58, 76; `SOURCES.md`; `features/exit/exit.gd`, `ui/crosshair.gd`, `ui/hud.gd` `_draw()` | checked |
| B24 | Limits: no boss, smooth HUD font, hit box over the head when crouched, defeat legs | `TEST-REPORT.md` known limitations (playtest 4 font); `CHARACTER-SHEET.md` Revision 3; `SOURCES.md` ENEMY-WOLF-DOWN v3 | checked |
| B24 | Next: boss arena, 2× wolf, 10 HP, 2-damage lunge | `CONCEPT.md` line 19; `CHANGE-BRIEF.md` line 79 | checked |
| B25 | A real-lunge test exists to predict against | test re-run `hurt-real-lunges-one-sound-per-landed-hit` PASS (hp_lost 3) | checked |
