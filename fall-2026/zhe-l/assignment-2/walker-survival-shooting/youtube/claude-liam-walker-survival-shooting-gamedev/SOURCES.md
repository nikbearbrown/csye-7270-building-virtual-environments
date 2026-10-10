# Sources — film *Walker Survival Shooting, Before the Slice*

## Source revision
- Game and documents: course repository commit **f848d84**, folder `fall-2026/zhe-l/assignment-2/`
  (`walker-survival-shooting/` and `FRICTIONAL.md`), exported with `git archive` into an isolated working copy.
  The `godot/` folder is unchanged since `69b0608` (TEST-REPORT).
- Uncommitted drafts read for status and test facts: the designer's `README.md` and `TEST-REPORT.md`.
- Nothing in the game, the course repository or the designer's working folder was changed for the film.

## Toolkit
- Brutalist (`brutalist.art`), `godot-gamedev` skill in walker mode, updated to upstream commit `22264a3` before
  the build. The checkout also carries six pre-existing local Windows-compatibility edits (npx lookup, drawtext
  font path, QC timecode exclusion); they were not made for this film.
- `./art doctor` exits 1 on an upstream guard that finds documentation mentioning a paid TTS vendor inside the
  toolkit's own example reels. Every dependency it would check was verified individually (ffmpeg 9.0.2,
  Python 3.12.10, Node 24.19.0, MiKTeX, Pillow, manim, faster-whisper, kokoro-onnx + model files, Kokoro synth
  smoke test, Remotion deps, EB Garamond, Oswald).
- Remotion scenes used: `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDesignBoard`, `GodotDesignFigure`,
  `GodotDevWorkbench`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro`. No new component was written.
- One root-cause fix to the shared toolkit, made for this build (uncommitted in the toolkit checkout):
  `GodotDesignFigure.tsx` and `GodotDesignBoard.tsx` drew the `@NikBearBrown` handle at `bottom: height*.04`,
  so its descender crossed the title-safe line and the toolkit's own Gate V refused every such beat. Both now use
  `height*.048`, the value `GodotDevWorkbench` already uses. Nothing else in the components changed.
- Beat-level QC declarations (reviewable in `beat_sheet.json`): B01 `sparse_by_design` (hesitant-writer typing);
  B14 `full_bleed` + one `contrast_regions` box on the burned-in label (edge-to-edge engine footage).
- GATE T fixes: section headings on `GodotDesignBoard` beats are upper case, because the checker split lowercase
  serif fragments ("rom", "nown", ".md)") into sub-floor text runs; B05 / B15 left dense mode (title-safe top).
- Figure images are passed to Remotion through `runtime/remotion/public/claude-liam-walker-survival-shooting-gamedev/`;
  the copies are byte-identical to `figures/` and the design files (`evidence/public-copies.sha256`).

## Narration
- Kokoro-82M (open weights, Apache-2.0) through `kokoro-onnx`, voice `am_onyx` ("Liam, in for Bear"), run
  locally; no paid TTS, no voice cloning. Script written by Claude Code (Claude Opus 5.5) from the documents
  above. B01 has 0.8 s of silence prepended and B20 a 1.0 s silent tail (FFmpeg), per the skill's timing rules.

## Engine evidence
- Godot v4.7.2.stable.official.ed1daf0bf, Windows 11, D3D12. Capture method in `CAPTURE.md`; per-file SHA-256
  in `evidence/MANIFEST.sha256`.
- Runtime tree probe: not needed. The project has no scripts, so the running tree is the saved `base.tscn` plus,
  in the capture harness only, a SubViewport and one added camera.

## Sound shown in B08 / played in B09
- `design/sfx_sound/sfx_power_on.flac` (ComfyUI output 00042), `sfx_power_off.flac` (00044),
  `sfx_botton_press.flac` (00070): Stable Audio 3 Small SFX, Stability AI, Stability AI Community License; run
  locally by the designer in ComfyUI 0.38.0 (SOURCES.md of the game).
- The B08 settings were re-read from the ComfyUI workflow embedded in `sfx_power_on.flac` (FFprobe format tag
  `prompt`): checkpoint `stable_audio_3_small_sfx.safetensors`, text encoder `t5gemma_b_b_ul2.safetensors`,
  KSampler seed 1145141919810, 12 steps, CFG 1.0, `lcm`, `simple`, denoise 1.0; EmptyLatentAudio 2.3 s, batch 2.
- `listen/terminal-sfx-sequence.flac` = 0.8 s silence + power on + 1 s + power off + 1 s + button press + 1 s,
  concatenated with FFmpeg's `concat` filter at 44.1 kHz stereo; no gain, filtering or trimming. Duration 9.744 s.
  The film's master audio is 48 kHz, so the compositor resamples it. This is a playback of the generated files,
  labelled **not in-engine**: the sounds are not in the Godot project and no game event triggers them.
- Waveforms / spectrogram: FFmpeg `showwavespic` and `showspectrumpic` drawn directly from those files.

## Images shown
- `design/storyboard/03-tablet-onehand.png`: the designer's hand sketch (storyboard panel 3).
- `design/character/turnaround.png`: ChatGPT image generation, accepted reference CHAR-TURN (prompt not saved; see
  the game's SOURCES.md).
- `figures/*.png`: built by `scripts/make_figures.py` from native captures, FFmpeg plots, and table text copied
  from TEST-REPORT, README and SOURCES. Fonts: Lato, PT Mono (SIL OFL, bundled with the toolkit).

## Contributions to the film
- **Designer (Zhe Liu):** every design decision, accept/reject judgment and asset shown; the direction for this
  film (what to show, what to leave out, how to label it).
- **Claude Code (Claude Opus 5.5):** read the documents, wrote the capture harness, ran the checks, wrote the
  beat sheet, narration script and these records, and drove the Brutalist pipeline.
- **Kokoro:** narration audio. **Godot:** engine renders. **FFmpeg:** encoding, plots, label overlay.
