# BUILD-LOG: Shaders in 3D (overnight rough-cut run 2026-10-14)

**What this is.** Running log of the overnight build toward a 1080p slate cut.
**Why.** Resumable; mistakes recorded.
**Found.** (see PHASE lines)

PHASE audio DONE 2026-10-14 (50 beats, 9.24 min; longest non-bookend beat 14.5 s (BDEFS); BOUT padded +1.0 s)

## Built and deviations
- Harness extended for this film: `--kind quad3d`, `own_world_3d`, scene hook `harness_frame(t)`; six scene scripts in `capture-scenes/` (S1 pad, S2 three meshes, S3 lamp, S4 turnaround, S5 face-on square, S6 wrong type) copied from the verify scripts; variants through the environment variables S_VARIANT and CLIP_L.
- D1 and D2 (docs screenshots for B15, B42): docs.godotengine.org showed a bot-check page to the headless browser; not bypassed. B15 and B42 lanes switched from `BrowserCapture` to `ClaudeCodeBeat` quote cards (the two lines the plan recorded on 2026-10-13), labelled "Quoted text, not a screenshot". Originals in `evidence/build-orig-lanes/`. Retake with Playwright later and restore.
- B43's editor clip built by `make_editor_clips.py` from the four script-recorded frames (scripted editor session).
PHASE captures DONE 2026-10-14 (19 captures; every probe agrees with the plan's verified values: pad rust then flat green, lamp off 0.337/0.435/0.412, UV corners 0.149, stripes 0.584/0.953, mix 0.298/0.537/0.380, grey 0.7373 vs 0.502, wrong type left unchanged right red)
PHASE scenes DONE 2026-10-14 (14 Manim classes, two agents)
PHASE slate DONE 2026-10-14 (slate 555.1 s; Gate V BLOCKER 2 (B06 terminal card window edge: registered CCPlainShell component, not changed), MAJOR 41 (16 underfill 54 percent, 25 low-contrast); bookend PASS; GATE T, PROOF, final not run; dark/rust pad frames and the dark terminal card are the known GATE T risks)

## 4K master + publish run (2026-10-14; normal TOPOST path, no exceptions)
- shared ShaderLab fixes (cue tag once, wider side layout, stack window up to 660 px and a caption of 34 px, code over 18 rows set at 27 px) and every ShaderLab beat re-rendered; qc.typography_regions plus qc.contrast_regions via _godot-shaders-series/gate_t_regions.py; B05 and B18 rings replaced by underline bars; B06 terminal windowMargin 100 (edge-bleed); B15 and B42 quote-card titles are file names, B15 first line is the render_mode syntax line (sweep: prose in a code card), B26 note shortened; BOPEN title card rebuilt at 3840
- PHASE final+publish DONE 2026-10-14: https://youtu.be/m63zZdLMx_Y
