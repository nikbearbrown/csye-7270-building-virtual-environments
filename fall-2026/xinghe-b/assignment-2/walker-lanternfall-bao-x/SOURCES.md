# SOURCES

`walker-lanternfall-bao-x` · Bao Xing · CSYE 7270 Assignment 2

Everything in this repository is original to this project or was generated for it by the local models below. The per-run record — prompt, settings, seed, decision, reason, every edit, file path, storyboard panel — is [ASSET-LOG.md](ASSET-LOG.md) (rendered from the JSON sidecars in `gen/log/`). Rejected results are kept as thumbnails and contact sheets in `gen/thumbs/` and `gen/rejected/`.

## Starting point

- A **blank Godot 4.7.2 project**; no code or assets were copied from a starter.
- The protagonist concept (the Lamp-Head Courier) comes from my Assignment 1, [yanxlh/walker-jumpman-bao-x](https://github.com/yanxlh/walker-jumpman-bao-x), which extended [nikbearbrown/walker-jumpman](https://github.com/nikbearbrown/walker-jumpman). No file from either repository is included here.

## Generative models (all run locally on a MacBook, Apple M4 Pro, 16 GB, macOS 26)

| Model | Exact revision | Runtime | Licence / terms | Used for |
|---|---|---|---|---|
| [black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) | `741f7c3` | mflux 0.20.0 (MLX 0.32.2) Python API; 4-bit copy saved locally with `mflux-save` | Apache-2.0 | ART-PC-01, ART-EN-01, ART-EN-02, ART-ENV-01 … ART-ENV-07, ART-FX-01, ART-FX-02, ART-FX-03, ART-PK-01 (all 14 art assets) |
| [stabilityai/stable-audio-open-1.0](https://huggingface.co/stabilityai/stable-audio-open-1.0) | `f21265c` | diffusers 0.40.0, torch 2.14.0 (MPS), fp32; sampler fix in `gen/sfx_sampler_fix.py` | Stability AI Community License (free for non-commercial use and for organisations under USD 1 M revenue; outputs owned by the user) — accepted on Hugging Face by Bao | SFX-01 … SFX-06b |
| [facebook/musicgen-medium](https://huggingface.co/facebook/musicgen-medium) | `d3bd7b0` | transformers 5.17.0, torch 2.14.0 (MPS), fp16 | weights CC-BY-NC-4.0 (non-commercial; this is non-commercial coursework); AudioCraft code MIT | MUS-01, MUS-02 |
| [facebook/musicgen-melody](https://huggingface.co/facebook/musicgen-melody) | `68d653a` | same as above | weights CC-BY-NC-4.0 | first MUS-02 batch only — all four rejected, none shipped |
| [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | v1.0, as the ONNX files `kokoro-v1.0.onnx` and `voices-v1.0.bin` (kokoro-onnx release `model-files-v1.0`) | kokoro-onnx 0.4.7 (ONNX Runtime), called by the course's Brutalist toolkit | Apache-2.0 (weights); kokoro-onnx code MIT | the film's narration only, in the preset voice `am_onyx` ("Liam, in for Bear") — a stock synthetic voice, not a copy of a real person's voice. The game has no voice. |

No paid service, API key or school-hosted generator was used. FLUX.1-schnell is guidance-distilled and takes no negative prompt; exclusions are written into its positive prompts, as each log entry notes.

## What the prompts never contain

No living artist's name or style, no copyrighted character, no brand, no existing song or recording (no stem splitting, no audio-to-audio from a real track), no real person's voice. MUS-02 was generated from text only; the melody-conditioned attempt used this project's own MUS-01 as its condition.

## Processing tools (all local, all edits logged)

| Tool | Version | Role |
|---|---|---|
| Godot | 4.7.2.stable.official.ed1daf0bf | the game; also rasterises the storyboard SVGs for comparison |
| Python (via uv 0.12.19) | 3.12 | pipeline scripts in `gen/`, `design/`, `scripts/` |
| Pillow · numpy · scipy | 12.3.0 · 2.5.3 · 1.18.1 | figure detection, background keying, Lab palette lock, seamless tiling |
| librosa · soundfile | 1.0.0 · 0.14.0 | beat tracking, bar-aligned loops, crossfades, SFX trimming, OGG Vorbis encoding (libsndfile) |
| matplotlib | 3.11.2 | waveform/spectrogram thumbnails for audio log entries |
| torchsde | 0.2.6 | Brownian noise for Stable Audio Open's sampler |

## Collaborators and assistants

- **Claude Code** (Anthropic), running Claude Opus 5.5 in the Claude desktop app: my coding assistant for the whole project; what it did is in the table below. The read-only whole-branch code review on 2026-10-01 was a second, fresh Claude context. Claude generated no art or audio: every image and sound file in the game comes from the models above (the design images in `design/` are drawn by its scripts from simple shapes, see below).
- **The course's Brutalist toolkit** (a local clone of brutalist.art): the godot-gamedev skill with the walker modifier, its Remotion scenes, checks and outro jingle — used for the film only. The film's own [SOURCES.md](youtube/claude-liam-walker-lanternfall-bao-x-gamedev/SOURCES.md) lists its parts.
- **Walker's asset helpers** (`rembg_matting.py`, `grid_slice.py`) were not used: `gen/art_process.py` keys out the background and `gen/figures.py` finds the figures to cut.
- **People:** nobody else worked on this. Every playtest and every listening session was mine; no one else played the slice or listened to the candidates.

## Who contributed what

| | Claude (Claude Code) | Generative models | Me |
|---|---|---|---|
| **Design documents and plan** | drafted CONCEPT, STORYBOARD, CHARACTER-SHEET and CHANGE-BRIEF from my choices; drew the storyboard panels, character blockout and palettes with scripts; wrote the build plan | — | chose the game, theme, scope and the local models; read the four documents and approved them before tag `design-v1`, without hand-drawn panels; chose or asked for every later revision (nearest-enemy aim after the bot results; 2D pixel art and 10 poses; after my first play, rising XP cost, tougher monsters, new cards, solid props, a broken-up map) |
| **Prompts** | wrote every prompt and setting in `gen/prompts/` from the character sheet and storyboard, and rewrote them after rejected batches (the courier, the puddle, the Sunflare layer) | — | set the direction they follow — "不用3d就是2d像素游戏，然后不用太多动作" — and my reasons for rejecting candidates (MUS-01: "后面的杂音太多") fed the rewrites |
| **Code** | wrote all the Godot code, the automated checks, the generation and processing scripts and the repository audit, test-first; fixed what the code review found | — | asked for each gameplay change after playing it, e.g. "子弹打到怪物之后要求消失" (bullets vanish on a hit) and "路灯这些有阻挡效果" (solid props) |
| **Art, sound and music** | ran the models; measured every candidate (contrast, tile seams, tempo, energy above 6 kHz); built contact sheets, mock game screens and listening files and suggested a pick; applied the logged edits (background keying, cutting, palette lock, trimming, loop cuts) | produced every raw image (FLUX.1-schnell), sound effect (Stable Audio Open) and music loop (MusicGen-medium) — table above | looked at or listened to every candidate and chose every asset that shipped, with my reason in ASSET-LOG (e.g. SFX-01 "3 不刺耳", MUS-02 "有种远古的感觉"); chose to draw puddles and leaves half-transparent. Exception: five MUS-02 candidates were rejected by Claude's automated check without my listening, and the log says so |
| **Testing** | wrote and ran the automated checks; captured the in-engine screenshots for the comparisons | — | played the slice twice, with sound on and then muted ([TEST-REPORT §4](TEST-REPORT.md)) |
| **Film script** | wrote the narration and built the film with the course's godot-gamedev workflow (walker modifier): scripted gameplay capture, code panels, edit; checked every claim against the repository and corrected seven lines before the final render ([FACTCHECK.md](youtube/claude-liam-walker-lanternfall-bao-x-gamedev/FACTCHECK.md)) | — | chose to make it from build `8a6f988` with no further game changes ("不用，直接开始做视频"); watched and listened to the whole final export before submitting ("看过了 没问题") |
| **Narration** | — | Kokoro-82M read the script in the stock voice `am_onyx` | — |

## Reproduce an asset from the log

Every run in [ASSET-LOG.md](ASSET-LOG.md) keeps its exact prompt, seed and settings in `gen/log/<ID>/<run>.json`. One-time setup (Python 3.12 via uv; the downloads need the Hugging Face licences for FLUX.1-schnell and Stable Audio Open accepted first):

```bash
uv venv --python 3.12 gen/.venv-art && uv pip install --python gen/.venv-art -r gen/requirements-art.txt
uv venv --python 3.12 gen/.venv-audio && uv pip install --python gen/.venv-audio -r gen/requirements-audio.txt
gen/.venv-art/bin/mflux-save --model schnell --quantize 4 --path gen/cache/flux-schnell-4bit
gen/.venv-audio/bin/python -c "from huggingface_hub import snapshot_download as d; [d(r) for r in ['stabilityai/stable-audio-open-1.0', 'facebook/musicgen-medium', 'facebook/musicgen-melody']]"
```

Then re-run any logged generation by its run id (the `###` headings in ASSET-LOG):

```bash
gen/.venv-audio/bin/python gen/reproduce.py ART-PC-01-20260929T210117Z-s11-walk_contact
```

`gen/reproduce.py` writes the logged prompt, seed and settings into a one-run spec, runs it through the same generator script that made the original, inside a temporary copy of `gen/` (the repository and its log are not touched), and compares the new file with the logged one: the full-size raw if it is on disk (`gen/raw/`, kept locally, not committed), else the accepted copy (`gen/accepted/`), else the thumbnail. The hand edits are re-run from the steps listed under each run; the film's asset trace did this for the walking pose and landed on the shipped frame pixel for pixel.

Checked on 2026-10-04 on the machine that made the assets ([evidence/reproduce-2026-10-04.txt](evidence/reproduce-2026-10-04.txt)):

| Run | What it is | Result |
|---|---|---|
| `ART-PC-01-20260929T210117Z-s11-walk_contact` | the walking pose traced in the film (accepted) | identical — 0 of 262,144 pixels differ |
| `ART-ENV-06-20260930T161937Z-s3` | the first puddle batch (rejected) | identical — 0 of 393,216 pixels differ |
| `MUS-01-20260930T013739Z-s5` | the night-market loop (accepted) | identical — all 958,080 samples |
| `SFX-01-20260930T030318Z-s3` | the kill sound (accepted) | identical — all 22,050 samples |

The walking pose was first made with FLUX quantized to 4-bit at load; the re-run used the saved 4-bit copy that every later run used and still matched exactly. On other hardware the arithmetic of MLX and the Apple GPU may differ, so a re-run elsewhere can come out close rather than identical.

## Other material

- **Font:** Godot's built-in default font (bundled with the engine), used by the HUD.
- **Storyboard, character blockout and palettes:** drawn by scripts in `design/` from simple shapes; no generated or external art.
- **Code and documents:** written for this project with Claude Code as described above; Claude is not an asset generator here. The day-by-day record of who decided what is [FRICTIONAL.md](FRICTIONAL.md).
