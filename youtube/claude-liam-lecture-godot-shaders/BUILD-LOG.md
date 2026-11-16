# BUILD-LOG: Godot Shaders (pilot, overnight rough-cut run 2026-10-14)

**What this is.** The running log of the overnight build of this film toward a 1080p slate/review cut (not a 4K master).
**Why.** Resumable: each phase appends `PHASE <name> DONE <date>`; mistakes are logged for the next film.
**Found.** Phase 0 built (ShaderLab, shader_kit.py, capture harness), audio, 17 captures, 18 Manim scenes (three parallel scene-writing agents, one per act group), slate cut rendered at 1080p. Gate V: BLOCKER 0 after fixes; MAJORs left are `low-contrast` on real grey-stage captures and borderline `underfill`. No 4K master, nothing staged or published.

PHASE audio DONE 2026-10-14 (generate_audio_kokoro.py, 49 beats, 559.6 s = 9.33 min total, longest beat 21.0 s (BHTF), no body beat over 15 s; took 9 min wall because other sessions were rendering)

## Lane edits made by the builder (build-time facts only; narration, beat order and scene design untouched)
Originals kept in `evidence/build-orig-lanes/act1..5.json`. Edited in `lanes/act2.json`, `act3.json`, `act4.json`, `act5.json`, then `make_sheet.py` re-run:
- B11 BrowserCapture: second move aimed at the real sentence's measured position on the captured page (x 0.59, y 0.29, scale 1.6) with the ring [0.34, 0.255, 0.51, 0.07].
- B10: four ring boxes added (Material slot, ShaderMaterial in slot, Shader slot, shader editor) read off the real editor frames.
- `videoLabel` of B16, B31, B32, B43: the plan's wording named exact seconds ("at 1 s", "2.2 s") but the events were retimed to land on the narration (lane `show` cues), so the labels no longer name seconds (a label that states a time that is not true would be false).
- B39 ramp: added `sine: {omega: 3, t0: 0}` (new optional ShaderLab field) so the marker follows 0.5 + 0.5 sin(3 t), exactly the shader's pulse.
- B16 ring/readout repositioned onto the real sheared bottom edge (the plan's boxes were drawn before the sprite size at scale 1.0 was known). ShaderLab: margins 112 px (Gate V edge-bleed), long code lines wrap instead of clipping.

## Phase 0: what was built and where (the toolkit was edited in ONE place only)
- `ShaderLab` (Remotion): `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/runtime/remotion/src/scenes/ShaderLab.tsx`, registered in `src/Root.tsx` (import + one `<Composition id="ShaderLab">`), `./art scene-index` run, `art scenes --check ShaderLab` says RENDERABLE. Layouts side, stack, video, code; cues with labels; readouts; rings; ramp (linear, period, or `sine`); wraps long code lines; 112 px safe margins. Layouts `stack` and `code` and cue `label` were NOT exercised by this film (written to the spec, untested).
- `shader_kit.py`: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/shader_kit.py` (plus `assemble_scenes.py`, `preflight.sh`, `MANIM-BUILD-BRIEF.md`, `vcontact.py`, `voice_check.py` in the same folder).
- Capture harness: `_godot-shaders-series/lab/capture.gd`, `capture_stage.gd`, `capture_shader.sh`, scene scripts in `lab/scenes/` (light_count, dial_rect, time_bars, iris_key). Options beyond the spec: `--hold-clock`, `--tail`, `--probe-at`, `--key-at`. Route: SubViewport 3840x2160 over a 1280x720 logical canvas, `--fixed-fps 30`, render loop off, `force_draw(false, 1/30)`.
- Probes agree with the plan's verified results: gradient 0.0196/0.498/0.9804, red 1,0,0, discard (0.498,0.498,0.2) and stage (0.851,0.835,0.792), dial 0.502,0.451,0.451, UV corners, set-parameter 0.502 then 0.898, typo 0.2 stays 0.2 then 0.898, tween 0.0 then 1.0, light count 0, 0.2, 0.4, 0.6, iris centre stage colour before the key and 0.98,0.976,0.961 after (the plan's scratch run read the sprite teal; this run's sprite is the checker so the centre cell is cream), pulse varies. Evidence logs: `evidence/build-captures/`.
PHASE phase0 DONE 2026-10-14
PHASE captures DONE 2026-10-14
PHASE scenes DONE 2026-10-14

## Mistakes worth not repeating
- `art run` ignores `--height 1080` for Manim (run.sh hardcodes `-qk` 4K) and Remotion (`--scale=2`): only the compile step downsizes; Manim+Remotion still render at 4K intermediates (disk watched: 62 GB free before and after).
- First ShaderLab used 80 px side margins: Gate V edge-bleed BLOCKERs on every side-layout beat. Margins are 112 px now.
- A dark light-count canvas needs the background rect `light_mask = 0`, else the lights turn it white.
- EB Garamond digits are old-style (0 looks like o): `fontVariantNumeric: lining-nums` on the ShaderLab root.
- macOS `sed -i` needs `''`; use python for edits.
PHASE slate DONE 2026-10-14 (slate cut 561.6 s, 1920x1080 24 fps; Gate V BLOCKER 0, MAJOR 32 = 18 underfill at 54 percent (min 55) + 14 low-contrast on grey-stage Godot captures; stopped after 3 fix rounds on this gate; bookend_check PASS; GATE T, PROOF, final master NOT run (slate only))

## 4K master + publish run (2026-10-14; normal TOPOST path, no exceptions)
- shared ShaderLab fixes (see the light-shaders entry) and every ShaderLab beat re-rendered; qc.typography_regions plus qc.contrast_regions via _godot-shaders-series/gate_t_regions.py; B04 and B08 declared contrast regions (late-sample ink averaging); B19, B22, B25 label boxes now grey-bordered cards, B22 ring replaced by an underline bar; BOPEN title card rebuilt at 3840
- PHASE final+publish DONE 2026-10-14: https://youtu.be/kSq45Gsqo8I
