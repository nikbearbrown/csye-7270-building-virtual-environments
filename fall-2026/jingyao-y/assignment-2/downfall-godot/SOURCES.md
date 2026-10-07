# SOURCES.md — Downfall (Assignment 2 summary)

## Starting point

This is the author's own project, `downfall-godot`. It began as a Godot port of the
author's earlier Unity prototype (README in
`../evidence/downfall-before-v1-20260924-235931.zip`).

- **Not** started from walker-jumpman or Assignment 1.
- The project name does not start with `walker-`.
- Git remote: `https://github.com/coldfish432/GodotGame.git`.

## Rights

The game uses the Arknights IP (Hypergryph): Lappland, Rhodes Island, PRTS, Closure,
Chernobog, Lungmen, Sami, Integrated Strategies relic names and effects, and PRTS
material names.

**Official images were fed to the image model as references or direct inputs:**

| Reference set | Used for |
|---|---|
| `../evidence/prts-references/` (enemy avatars, map previews) | field enemies v1, props v1, ground v1 |
| `../evidence/rhodes-references/` (story backgrounds, base and furniture art) | Rhodes base prompts |
| `art/relics/refs/prts_icons/` | every relic icon ("Redraw each PRTS icon as pixel art") |
| `art/items/batch_E4_v3`, `E4_v4/references/` | two originium sprites |
| `art/items/refs_M`, `art/portraits/refs/prts` | briefed batches, not delivered |

**This directly conflicts with the assignment rule:** "Do not prompt with, or feed in
as reference, … a copyrighted character, a brand". The author decided on 2026-10-07 to
submit the game as it is. This file states that plainly rather than hiding it.

No voice cloning is involved. No API keys are committed.

## Generative models

| Model | Where run | Terms | Used for |
|---|---|---|---|
| OpenAI **gpt-image**, identified as ChatGPT / gpt-image, issuer "OpenAI Media Service API", from the C2PA manifests embedded in every raw source PNG. | Called through the built-in `image_gen` tool of the author's Codex agent, which the docs call "Sol". Outputs went to `C:\Users\yuan\.codex\generated_images\`. | OpenAI Terms of Use / Services Agreement. Outputs are assigned to the user, subject to the policies. **Author to confirm whether this was a paid subscription.** | All generated images: Lappland walk and combat sheets, VFX, enemies, field surfaces and props, equipment and relic icons, Rhodes base. |
| Google **Gemini**, music generation ("Music" mode in the Gemini app; model shown as *Flash*) | Gemini app, author's account, downloaded as MP3 | Google Generative AI terms | 2 warehouse sounds, 2 music loops, 2 stings (see *Generated audio* below). The 13 older sounds are still sine/FM synthesis in `game/field_audio.gd`. |

**Not recorded:** seeds, quality settings and exact output sizes. Only the canvas sizes
written inside the prompts survive, so **exact reproduction is not possible**.

## Generated audio

Generated 2026-10-07 with Gemini (row above). Reproduce a runtime file from its raw
download with `python audio/tools/cut_audio.py` (needs ffmpeg, numpy, soundfile);
the same MP3s give byte-identical outputs (checked by rerunning: the hashes did not
change). Full hashes and every parameter: `audio/asset_log.json`. Loop points were
found with `audio/tools/find_loop.py` (spectral self-similarity around the seam)
and checked on the decoded OGG: the jump at the seam is smaller than the 99th
percentile of ordinary sample-to-sample steps.

| Runtime file | Raw download (SHA-256) | Prompt | Cut | Gain | Output SHA-256 |
|---|---|---|---|---|---|
| `audio/sfx/lights_on.wav` | `music/开灯.mp3` `7e2118f88215…` | [P-LIGHTS-ON](audio/PROMPTS.md) | 0.0685 s + 0.7 s; fade squared from 0.35 s | peak -3 dBFS | `9a39bead468d…` |
| `audio/sfx/lights_off.wav` | `music/关灯.mp3` `1fa94afebdd6…` | [P-LIGHTS-OFF](audio/PROMPTS.md) | 49.2556 s + 1.1 s; fade squared from 0.50 s | peak -3 dBFS | `f1094c89c705…` |
| `audio/music/base_loop.ogg` | `music/基地背景音乐.mp3` `a6191f1a3170…` | [P-BASE](audio/PROMPTS.md) | 0 – 115.4652 s; loop back to 40.171 s (75.2942 s loop); 40 ms raised-cosine into the audio before loop_offset | RMS -18 dBFS, peak <= -1 dBFS | `fc7c50488a74…` |
| `audio/music/mine_loop.ogg` | `music/矿洞外勤音乐.mp3` `88cd71e2a79e…` | [P-MINE](audio/PROMPTS.md) | 0 – 45.3041 s; loop back to 13.3034 s (32.0007 s loop); 40 ms raised-cosine into the audio before loop_offset | RMS -18 dBFS, peak <= -1 dBFS | `6420e551a3f4…` |
| `audio/music/sting_extract.ogg` | `music/撤离.mp3` `1d8b9dac62e9…` | [P-EXTRACT](audio/PROMPTS.md) | 0.6080 – 6.2788 s (first take; next take starts 6.2988 s); fade 2 ms in, squared 0.5 s out | RMS -18 dBFS, peak <= -1 dBFS | `3748b354a223…` |
| `audio/music/sting_fail.ogg` | `music/失败.mp3` `dd77388eed1f…` | [P-FAIL](audio/PROMPTS.md) | 0.0493 – 12.0308 s (first take; next take starts 12.0508 s); fade 2 ms in, squared 0.5 s out | RMS -18 dBFS, peak <= -1 dBFS | `60c09f412ba2…` |

**Gemini settings per download (to be confirmed by the author):** Music mode,
*Flash*, Instrumental; Genre Custom for the two sounds, Ambient/Electronic for the
music; which take of how many was kept. Gemini exposes no seed, so regenerating
from the prompt gives a different file; reproduction starts from the archived raw
MP3s in `music/`.

**The model did not follow the musical numbers in the prompts.** Asked for 100 BPM ×
16 bars, the base track came back as a 75.3 s cycle; asked for 96 BPM in D minor,
the mine track is about 75 BPM (3.2 s bars) in E minor. The cuts follow the measured
structure, not the prompt.

## Tools (non-generative)

- **Godot** 4.7.2-stable.
- **ffmpeg** 9.0.1 and **Python with numpy + soundfile** for the audio cuts (`audio/tools/`).
- **Python with Pillow** for nearest-neighbour reduction, quantization and alignment:

| Script | Applied to |
|---|---|
| `godot_assets/prepare_combat_atlas.py`, `prepare_lappland_vfx.py` | Lappland combat atlas and VFX |
| `art/prepare_enemy_atlas.py`, `prepare_enemy_directional.py` | enemy atlases |
| `art/relics/reduce_generated.py` | relic icons |
| `art/items/*/process_sources.py`, `remap_v5.py` | equipment icons |
| `art/rhodes/*/h3_source_pipeline.py`, `h4_kit.py`, `export_runtime.py` | Rhodes base |

- **Claude Code** wrote the briefs and review notes, the processing and assembly scripts, game code, and tests.
- **Hand-made or code-drawn, not generated:**
  - Rhodes walls/doors batch1 v4 (drawn on the native grid after the model failed the geometry);
  - Rhodes logo L v2;
  - placeholder shelf hatch.

## Asset log

Rows cover the assets used at runtime plus the main rejected rounds. The full
prompts are in the files linked in the **Prompt** column.

| Asset ID | Prompt / settings | Outcome and reason | Edits | Where used |
|---|---|---|---|---|
| CHAR-WALK | **No prompt survives.** gpt-image, C2PA timestamp 2026-09-22T20:14Z (`lappland_8_direction_walk_sheet.png`). | Accepted. **Rejected/unused concepts:** `lappland_chibi_pixel*.png` (5 files, same day). | Re-laid out as `lappland_8dir_walk_4frames.png` (4×8 cells of 222 px). BOX-downsampled to 32 px with alpha thresholding; the script is not kept. SE row mirrored at runtime. | `godot_assets/lappland_8dir_walk_32.png` · P1, P4, P5 |
| CHAR-COMBAT | `godot_assets/拉普兰德战斗素材.md`: "transparent pixel art GAME SPRITE ATLAS… original Lappland (Arknights) chibi wolf girl combat frames…", with the walk sheet as reference image. 2026-09-30. | Accepted. The **first slicing was rejected** (80% shrink, clipped swords). Backup in `../evidence/lappland-backup-20260929-203119/`. **Open:** SW≈S, N frames too similar. | `prepare_combat_atlas.py`: per-cell alignment to the foot line, 64 px cells. | `lappland_combat_64.png` · P4, P6, P8 |
| VFX-SLASH/WAVE | **No prompt recorded.** Originals in `godot_assets/lappland_vfx_originals/`. | Accepted. `剑气_概念原画.png` was kept as concept only. | `prepare_lappland_vfx.py` bake. | `lappland_vfx_*.png` · P4, P6 |
| ENEMY-V1 / ENV-PROPS-V1 / ENV-GROUND-V1 | `art/field/prompts.md` (3×3 grid of 512 px cells, 1536×1536), PRTS refs plus Lappland style ref. 2026-09-25. | Enemies superseded by the 8-direction boards. props_v1 kept as the style reference. ground_v1 replaced. | Sliced by `art/field_art.gd`. | `art/field/props_v1.png` |
| ENV-BG-V1 | `art/field/background_prompts_v1.md`. 2026-09-29. | **Rejected/superseded** by v2 (no longer referenced). Before/after: `design/evidence/background-*-{mine,city,snow}.png`. | — | — |
| ENV-SURF-* / ENV-PROPS-V2 | `art/field/scene_v2_prompts.md`, `scene_groups_v2_prompt.md`. Low-contrast surface "so characters and red warning areas stand out". | Accepted. Rationale in `场景美术重构_v2.md`. | Shader tiling (`terrain_background.gdshader`). | `surface_*_v2.png`, `scene_groups_v2.png` · P3–P5 |
| ENEMY-ATK | `art/field/enemy_attacks_prompt.md` (5 columns × 7 rows, identity-preserve). | Accepted. A floating-weapon variant was **rejected** at the user's request because it looked like a charge bar. **File deleted, no thumbnail.** | `prepare_enemy_atlas.py` | `enemy_attacks_64.png` · P5 |
| ENEMY-DIR / ENEMY-WALK | `art/enemy_multidirection_originals_v1/方向分列提示词.md`, `art/enemy_movement_originals_v1/生成提示词.md`. | Accepted. The first-draft layout prompt was **rejected** (duplicate directions). No image kept. | `prepare_enemy_directional.py` | `enemy_dir_*_64.png`, `enemy_walk_*_64.png` |
| ITEM-E1..E4 | `art/items/batch_E*_v*/generation_prompts.md`, `generation_metadata.json` (inputs plus SHA-256). | v1 **rejected:** code-drawn, not painted (`E_revision_brief_v2.md`). v2–v5 accepted in stages; reasons per icon in `E*_revision_v*.md` (speckle, camouflage blotches, orange-ramp misuse, glyph-like shapes). Contact sheets per round. | `process_sources.py` resize and quantize; `remap_v5.py` palette remap. | `art/items/runtime/` · P8, P10 |
| RELIC-R1..R4 | `art/relics/batch_R1_v1/README.md` ("redraw the reference's subject… ≤24 colours"), with PRTS icon as input. | All accepted. R1 was accepted despite Claude flagging 43% isolated pixels (user: "挺好的", "it's fine"). Earlier drafts in `previous_v1/`. | `reduce_generated.py`: 72×72, binary alpha, 23 colours. | `art/relics/runtime/` · P6 |
| ENV-RHODES | `art/rhodes/batch*/prompts.md`, `batch_H*/sources/prompts.json`. Acceptance log in `罗德岛基地美术策划案_v2_0.md` §4.5. | Batch1 source v1 **rejected**. H3 v1 **rejected** (code-drawn icons). Other rounds pass in 1–4 iterations. | Integer reduction plus CIELAB quantization; assembled by `assemble_*.py`. | `art/rhodes_runtime/` · P1, P9 |

## Rejected-output evidence that survives

- Equipment:
  - `art/items/contact_sheet.png`;
  - `batch_E*_v*/contact_sheet*.png`, `silhouette_check.png`;
  - `batch_E4_v*/reviews/`;
  - `raw_originium_downscale_tests.png`.
- Relics: `art/relics/batch_R*/contact_sheet.png`, `previous_v1/`.
- Rhodes: `art/rhodes/source_batch1_20260930/`, `batch2_v2/diagnostics/`.
- Lappland and backgrounds:
  - `godot_assets/lappland_chibi_*.png`;
  - `../evidence/lappland-backup-20260929-203119/`;
  - `design/evidence/background-before-*.png`.

## What is in GitHub and what stays local (2026-10-07)

The repository is public, so these are kept out of it on purpose (`.gitignore`):

| Kept out | Why | What stands in for it |
|---|---|---|
| Official PRTS reference images (`art/relics/refs/prts_icons/`, `art/items/refs_M/prts_icons/`, `art/portraits/refs/`, `art/items/batch_E4_v*/references/`, `art/_to_sol/*.zip`) | They are Hypergryph's copyrighted art and are not redistributed. | Each brief lists the PRTS URL of every reference (`art/relics/refs/relics_table.json` has all 96 relic icon URLs). |
| Raw Gemini MP3 downloads (`music/`) | The course rule keeps MP3 out of GitHub. | `audio/asset_log.json` has their SHA-256; `cut_audio.py` rebuilds the runtime files from them. |
| Full-size image generations (`art/*/batch_*/sources/`) | The course asks for thumbnails of raw and rejected outputs, not full-size files. | `design/evidence/raw-sources/*.jpg`: one thumbnail sheet per batch (14 sheets). Each batch folder keeps its contact sheet, 8× previews and manifest. |
| `../evidence/` | It sits outside the project folder. | Everything the A2 docs show is copied into `design/` (storyboard frames, character captures, background before/after). |
