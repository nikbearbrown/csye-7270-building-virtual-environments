# FACTCHECK — walker-magic gamedev film

> Draft. Each spoken or on-screen claim is checked against a file, a recorded test output or a capture before rendering.

## Process decisions on record

- **SLICE AUDIO method (B18, B20).** The skill's compiler strips footage audio (`runtime/scripts/compile.py`, per-clip encode with `-an`), and `docs/PIPELINE-SAFETY.md` keeps ordinary b-roll silent under narration. Per the assignment, the course was asked for its approved method: each SLICE AUDIO beat's `audio_file` is the audio track of the same Movie Maker take, cut to exactly the same interval as its video, with no narration. **Approval (verbal):** verbal approval from the instructor the method is acceptable. Recorded 2026-10-07, as reported by the author; there is no written message.

## Claims to verify before render (filled in during the build)

| Beat | Claim | Source / evidence | Status |
|---|---|---|---|
| B03 | Build shown is `74c0443`; capture copy `5266946` has identical runtime files | `git diff --name-only 74c0443 5266946` (only `assets/audio/MUSIC-EDIT-LOG.md`) | checked |
| B05 | 64 px with hat, 1:3.5, 14x44 hit box | `CHARACTER-SHEET.md` | to check against the final excerpt |
| B06 | CHAR-REF v1, setup message and CHAR-IDLE v1 prompts verbatim | `SOURCES.md` → Image prompts (copied verbatim from `design/IMAGE-PROMPTS-from-chat.md`) | text checked; the author's "sent unchanged" confirmation is still open (file header) |
| B07 | Raw output 1920x2184 on green | `design/character/generated/CHAR-IDLE-v1.jpg` | checked (image header) |
| B08 | Face height drifted ~20%, width within 1% | `tools/clean_sprites.py` comment; session measurements | to check against the excerpt |
| B09 | 62x69, 0 off-palette pixels | `assets/sprites/edit-log.json` | to check |
| B13 | Darks from L* ~7 to 20–40; cave darkest ~5 | `assets/sprites/EDIT-LOG.md` (L* of dark steps, cave L* p5 4.7) | to check |
| B14 | 0.35 s cooldown; held button does not repeat | `features/player/tuning.gd`; `test_cast.gd` (held 2 s: 1 cast) | to check |
| B15 | 0.5 s growl; 2 HP | `features/wolf/wolf.gd` constants | to check |
| B22 | `WALKER TESTS: 11 checks / 0 failures`; route counts | `TEST-REPORT.md` recorded output | to check against a re-run |
| B23 | Models per asset; Stability AI notice | `SOURCES.md`, `README.md` Attribution | to check |
