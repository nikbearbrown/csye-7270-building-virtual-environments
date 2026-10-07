# Sources

> Draft — 2026-10-01. Every tool and model used to make assets for this project. Rows marked TODO are filled in before the commit that first uses them.

## Generation tools

| Tool | Version | Source | License | Used for |
|---|---|---|---|---|
| Google Gemini (Gemini web app, image generation) | Model: TODO · Version: TODO | https://gemini.google.com | Google Terms of Service and Generative AI Additional Terms | Every generated image: mage, wolf, FX, cave tiles and background. See **Generated images** below. |
| ComfyUI | v0.38.1 (commit `20ca544ee0436721d8eb5f544665e490609f72c8`) | https://github.com/comfyanonymous/ComfyUI | GPL-3.0 | Running Stable Audio Open locally |
| Stable Audio Open 1.0 | `model.safetensors` at commit `f21265c1e2710b3bd2386596943f0007f55f802e` (sha256 `7b20458a…66b57e`) | https://huggingface.co/stabilityai/stable-audio-open-1.0 | Stability AI Community License (last updated July 5, 2024) — gated; accepted by the author on Hugging Face | Sound effects |
| T5-base text encoder (for Stable Audio Open) | `model.safetensors` at commit `a9723ea7f1b39c1eae772870f3b547bf6ef7e6c1` (sha256 `a9090354…c8f5b4`) | https://huggingface.co/google-t5/t5-base | Apache-2.0 | Text conditioning for Stable Audio Open, as in ComfyUI's official audio example (https://comfyanonymous.github.io/ComfyUI_examples/audio/) |
| Google Gemini (Gemini web app, music generation: Lyria) | Model: Lyria · Version: TODO (as shown in the Gemini app) | https://gemini.google.com | Google Terms of Service and Generative AI Additional Terms | MUS-LOOP source track `Beneath_the_Unlit_Stone.mp3`. See **Music** below. |
| Suno (free plan) | v4.5-all and V6 Preview | https://suno.com | Suno Terms of Service (free plan: non-commercial) | **Rejected** for MUS-LOOP; nothing used. See **Music** below. |

## Generated images (Google Gemini)

Accepted images stay full size; rejected ones are kept only as 256 px-wide thumbnails in the group's `rejected/` folder.

- **`*-thumb.png`:** thumbnail from a screenshot of the Gemini output; original download not kept. The author made these from screenshots shared in a chat with Claude. This covers all 13 `.png` thumbnails: CHAR-CAST v1, v2, v4 · CHAR-RUN v1, v2 · ENEMY-WOLF-DOWN v2 · WOLF-R1 run v0, run v1, lunge v1, down v1, derived · ENV-TILES v1 · ENV-BG v2.
- **`*-thumb.jpg`:** made from the original downloaded file (CHAR-REF v1, v3 · CHAR-RUN-PASSING v0).

**Workflow change:** the mage and the first wolf round shared one long Gemini chat, and earlier images started leaking into new ones (the mage's head in a wolf frame, cave paintings in the tiles). From the wolf onward, each asset group got its own Gemini chat to stop this context bleed.

### Mage — `design/character/generated/` (chat 1, shared)

| Asset | Status | File | Notes |
|---|---|---|---|
| CHAR-REF v1 | rejected | `rejected/CHAR-REF-v1-thumb.jpg` | Staff broke into loose pixels at 64 px (see CHARACTER-SHEET Revision 1). |
| CHAR-REF v2 | **accepted** | `CHAR-REF-v2.jpg` | Mid-thigh tunic and thicker staff accepted in Revision 1. |
| CHAR-REF v3 | rejected | `rejected/CHAR-REF-v3-thumb.jpg` | Unchanged from v2. |
| CHAR-IDLE v1 | **accepted** | `CHAR-IDLE-v1.jpg` | |
| CHAR-RUN-CONTACT attempt 1 | rejected | `rejected/CHAR-RUN-v1-thumb.png` | Two frames side by side, staff cut off, floating foot, ground line. |
| CHAR-RUN-CONTACT attempt 2 | rejected | `rejected/CHAR-RUN-v2-thumb.png` | Model edited the reference sheet instead of drawing a new pose. |
| CHAR-RUN-CONTACT v3 | **accepted** | `CHAR-RUN-CONTACT-v3.jpg` | |
| CHAR-RUN-PASSING v0 | rejected | `rejected/CHAR-RUN-PASSING-v0-thumb.jpg` | See notes. |
| CHAR-RUN-PASSING v1 | **accepted** | `CHAR-RUN-PASSING-v1.png` | Screenshot; see notes. |
| CHAR-RISE v1 | **accepted** | `CHAR-RISE-v1.jpg` | Staff not raised as the prompt asked, but consistent with IDLE. |
| CHAR-FALL v1 | **accepted** | `CHAR-FALL-v1.jpg` | |
| CHAR-CAST attempts 1–2 | rejected | `rejected/CHAR-CAST-v1-thumb.png`, `rejected/CHAR-CAST-v2-thumb.png` | Reason: TODO. |
| CHAR-CAST v3 | **accepted** | `CHAR-CAST-v3.jpg` | File originally named CAST-v1. Yellow-green crystal glow removed in cleanup; glow added in Godot. |
| CHAR-CAST v4 | rejected | `rejected/CHAR-CAST-v4-thumb.png` | Reason: TODO. |
| CHAR-HURT v1 | **accepted** | `CHAR-HURT-v1.jpg` | |
| CHAR-FAIL v1 | **accepted** | `CHAR-FAIL-v1.jpg` | |
| CHAR-WIN v1 | **accepted** | `CHAR-WIN-v1.jpg` | |

### Wolf — `design/character/generated/`

Round 1 (chat 1, shared with the mage) was abandoned because the long chat mixed earlier images into new ones. The wolf was restarted in a new, text-only chat (chat 2), and every accepted wolf frame comes from that chat.

| Asset | Status | File | Notes |
|---|---|---|---|
| Round 1 run v0 | rejected | `rejected/WOLF-R1-RUN-v0-bleed-thumb.png` | The mage's head leaked into the wolf. |
| Round 1 run v1 | rejected | `rejected/WOLF-R1-RUN-v1-thumb.png` | Screenshot. Abandoned with round 1. |
| Round 1 lunge v1 | rejected | `rejected/WOLF-R1-LUNGE-v1-thumb.png` | Abandoned with round 1. |
| Round 1 down v1 | rejected | `rejected/WOLF-R1-DOWN-v1-thumb.png` | Abandoned with round 1. |
| Round 1 frame derived from down v1 | rejected | `rejected/WOLF-R1-DERIVED-thumb.png` | Legs still in the running pose. |
| ENEMY-WOLF-RUN v2 | **accepted** | `ENEMY-WOLF-RUN-v2.jpg` | Chat 2. |
| ENEMY-WOLF-LUNGE v2 | **accepted** | `ENEMY-WOLF-LUNGE-v2.jpg` | Chat 2. |
| ENEMY-WOLF-DOWN v2 | rejected | `rejected/ENEMY-WOLF-DOWN-v2-thumb.png` | Chat 2. Legs still in the running pose. |
| ENEMY-WOLF-DOWN v3 | **accepted** (partially achieved) | `ENEMY-WOLF-DOWN-v3.jpg` | Chat 2. Eyes closed, head and ears down; legs unchanged. The defeat motion is handled in the engine: white flash, tilt, cool blue-gray particles. |

### FX — `design/character/generated/`

| Asset | Status | File | Notes |
|---|---|---|---|
| FX-FIREBALL-BURST v1 | **accepted** (first try) | `FX-FIREBALL-BURST-v1.jpg` | The downloaded original has semi-transparent ghost blobs and dark fragments along the top; only the fireball and the burst are cropped out in cleanup. |

### Environment — `design/environment/generated/`

| Asset | Status | File | Notes |
|---|---|---|---|
| ENV-TILES v1 | rejected | `rejected/ENV-TILES-v1-thumb.png` | Visible seams when tiled; cave paintings leaked in from the background chat. |
| ENV-TILES v2 | **accepted** | `ENV-TILES-v2.jpg` | Only the uniform dark rock is used as the repeating tile, plus the two end pieces; the brighter wall on the left is discarded. |
| ENV-BG v1 | **accepted** | `ENV-BG-v1.jpg` | Framed composition, fixed to the camera. |
| ENV-BG v2 | rejected | `rejected/ENV-BG-v2-thumb.png` | Cave paintings add warm colors, against pillar 2 ("your fire is the only warmth"). |

## Sound effects (Stable Audio Open 1.0)

Generation: ComfyUI, 3 variants per sound with fixed seeds 1, 2, 3; prompts, settings and hashes in `design/audio/sfx-gen-log.md`. The first run clipped in 10 of 18 files and was regenerated at -6 dB with the same seeds (content unchanged). Raw WAVs stay outside the repo in `E:\7270\tools\sfx_raw\`.

Picks are the author's, after listening. Reason for every pick: it matches the on-screen action better and reads more clearly; the other seeds fit the action less well or were less clear.

| Sound | Picked | Rejected | Edits (`tools/trim_sfx.py`) | In the slice |
|---|---|---|---|---|
| SFX-CAST | seed 3 | seeds 1, 2 | trim leading silence, cut to 0.4 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-CAST.ogg` |
| SFX-WOLF-DOWN | seed 1 | seeds 2, 3 | trim, cut to 0.6 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-WOLF-DOWN.ogg` |
| SFX-HURT | seed 3 | seeds 1, 2 | trim, cut to 0.3 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-HURT.ogg` |
| SFX-FAIL | seed 2 | seeds 1, 3 | trim, cut to 1.0 s, 250 ms fade-out (sustained tone; stays shorter than the 1.2 s reload), level match | `assets/audio/sfx/SFX-FAIL.ogg` |
| SFX-CLEAR | seed 3 | seeds 1, 2 | trim, cut to 1.2 s, 10 ms fade-out, level match | `assets/audio/sfx/SFX-CLEAR.ogg` |
| SFX-HEAL | seed 3 (pre-pick) | — | not exported: heal is out of the slice (CHANGE-BRIEF Revision 2); pre-picked for the full game | — |

Common edits for every exported sound: onset = first 2 ms window above -45 dBFS with 5 ms kept before it, 2 ms fade-in so the cut cannot click, raised-cosine fade-out, levels matched on the loudest 50 ms window (short-window RMS) to one shared target of -15.75 dBFS with peaks at most -1 dBFS, OGG Vorbis q6 (FFmpeg libvorbis). Per-file numbers (onset, cut points, gain, peak, hashes): `assets/audio/EDIT-LOG.md`.

## Music (Google Gemini, Lyria)

- **Rejected first attempt: Suno.** 4 tracks were generated on the free plan. The two V6 Preview tracks were paid previews, and the free account had 0 downloads available, so no Suno track could be used without paying; the author switched to Google Gemini instead. Nothing from Suno is in the project. (CHANGE-BRIEF's "Generation tools" planned Suno; this is the change.)
- **Accepted: Google Gemini, Lyria.** Track `Beneath_the_Unlit_Stone.mp3` (MP3, 44.1 kHz stereo, 181.37 s, sha256 `6401e27055558127282bf15341158276146278e15ad0d0e9c0ee36a7d2248430`), kept outside the repo in `E:\7270\tools\music_raw\` and never committed. Model version: TODO (as shown in the Gemini app). Prompt: TODO (the author's prompt text).
- **SynthID:** audio generated by Lyria in the Gemini app carries Google's inaudible SynthID watermark; MUS-LOOP, cut from it, should be treated as carrying it too.
- **Loop:** 60.886 s to 115.510 s (12 bars at about 52.7 bpm), points suggested by Claude's waveform analysis in chat. Both points snapped to the nearest zero crossing, with a 50 ms crossfade of the loop's end into the audio just before the loop start (`tools/make_music_loop.py`). **Status: preview rendered, waiting for the author's listening check of the seams**; exported to `assets/audio/music/MUS-LOOP.ogg` only after that.

## Runtime

| Tool | Version | Source | License |
|---|---|---|---|
| PyTorch | 2.11.0+cu128 | https://pytorch.org · https://download.pytorch.org/whl/cu128 | BSD-3-Clause |
| torchvision | 0.26.0+cu128 | https://github.com/pytorch/vision | BSD-3-Clause |
| torchaudio | 2.11.0+cu128 | https://github.com/pytorch/audio | BSD-2-Clause |
| Python | 3.12.7 | https://www.python.org | PSF-2.0 |
| uv | 0.11.19 | https://github.com/astral-sh/uv | MIT or Apache-2.0 |
| Godot Engine | 4.7.2-stable | https://godotengine.org | MIT |
| Pillow | 12.3.0 | https://python-pillow.org | MIT-CMU |
| NumPy | 2.5.2 | https://numpy.org | BSD-3-Clause (with bundled 0BSD/MIT/Zlib parts) |
| SciPy | 1.18.1 | https://scipy.org | BSD-3-Clause |
| PyAV | 19.0.0 | https://github.com/PyAV-Org/PyAV | BSD-3-Clause |
| FFmpeg | 9.0.2 (gyan.dev full build, via WinGet) | https://ffmpeg.org | GPL-3.0 build (includes libvorbis, BSD-3-Clause) |

Project scripts: `tools/clean_sprites.py` (sprite cleanup, settings in `tools/sprites.json`, log in `assets/sprites/EDIT-LOG.md`), `tools/sheet_images.py` (silhouette and collision check images), `tools/gen_sfx.py` (sound generation, prompts in `tools/sfx_prompts.json`, log in `design/audio/sfx-gen-log.md`), `tools/trim_sfx.py` (SFX trim and export, log in `assets/audio/EDIT-LOG.md`) and `tools/make_music_loop.py` (music loop). All run with the ComfyUI venv; the two audio scripts also use FFmpeg.

Hardware: NVIDIA GeForce RTX 5060 Laptop GPU (8 GB), Windows 11.

## Notes

- **SynthID:** images made with Google Gemini carry an invisible SynthID watermark embedded in the pixels. Google designs it to survive common edits such as resizing and cropping, so the CHAR-REF images and their thumbnails should be treated as carrying it.
- **Stable Audio Open attribution:** the Community License (§IV.a) requires that anything distributed with or made from the model keeps the notice "This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI Ltd. All Rights Reserved" and shows "Powered by Stability AI". You own the generated outputs (§IV.c.iii). Commercial use is allowed only for revenue under US $1M and requires registering at https://stability.ai/community-license. This project is coursework (non-commercial).
- **CHAR-RUN-PASSING v1 is a screenshot:** `CHAR-RUN-PASSING-v1.png` (900×1024) is a screenshot of the accepted Gemini output; the original download was lost. Screenshot pixels, not the original file, so it may differ slightly in resolution and color from the other frames.
- **CHAR-RUN-PASSING v0 (rejected):** wide stride, gray ground band, and too similar to RUN-CONTACT for a 2-frame loop. Commit `2a90b0b` mistakenly added this image at full size as `CHAR-RUN-PASSING-v1.jpg`; it was removed in the next commit and replaced by the v0 thumbnail.
- **Run loop:** RUN-CONTACT v3 + RUN-PASSING v1, chosen after comparing loop previews.
- **CHAR-RUN-PASSING v1:** hat about 5% smaller than in the other frames, and less forward lean than RUN-CONTACT v3. During cleanup, scale by head height and re-check the run loop in the engine.
- Model weights and the ComfyUI install live in `E:\7270\tools\`, outside this repo, and are not committed.

## Original commit SHAs

Author and committer of the imported commits were rewritten to `zhefan-z <noreply>` for the course repo, to follow the fall-2026 rule "no IDs and no full names"; author and commit dates and file contents are unchanged. The originals are the permanent record in zhef-z/walker-magic-zhefan, frozen at `920d969`.

| Course-repo SHA | Original SHA (zhef-z/walker-magic-zhefan) | Author date | Commit |
|---|---|---|---|
| `7371b257cbca6b7e6b049153d7f3f00d1866153d` | `6697b805420ac46b925d17fd4dbc00330fae239f` | 2026-10-01T17:00:58-04:00 | Add concept, storyboard, character sheet and change brief before any generation |
| `26668d6661269f00a2297c2bf60b4b0e6a1c8b17` | `c4fabafbb31f2e1b475b77b84912d5aad0e6274b` | 2026-10-01T18:07:05-04:00 | Add CHAR-REF v1-v3, idle and run contact from Gemini, Revision 1, SOURCES draft |
| `24e8c629ceaeb35c539673c2f05741c2514025f6` | `2a90b0bafe44c3fd41c684d3845936dcea670278` | 2026-10-01T18:16:12-04:00 | Add CHAR-RUN-PASSING v1 from Gemini |
| `a40b5346b8441d436a1d530121ecd429fce51d7c` | `95b9bb85b7412649d8fb18f87a902c7aa5f3e42c` | 2026-10-01T18:33:03-04:00 | Add remaining accepted Gemini poses, fix passing frame (v1 screenshot, v0 rejected) |
| `7f195585fca2767d5362c1c3b9a0f9b6ef35d2df` | `a67239c4c44aadf1a008cc18af99f37058abe596` | 2026-10-03T03:14:11-04:00 | WIP checkpoint: sprite cleanup, SFX generation scripts, SOURCES and rejected thumbnails |
| `511fcbf19080690aed407b888e266ff047f38aec` | `920d96914fa34e3682cafa236fdaf5a04cb6c662` | 2026-10-06T15:43:40-04:00 | Add FRICTIONAL pointer to the course-repo log |
