# BUILD-LOG: Vertex Shaders (overnight rough-cut run 2026-10-14)

**What this is.** Running log of the overnight build toward a 1080p slate cut.
**Why.** Resumable; mistakes recorded.
**Found.** (see PHASE lines)

PHASE audio DONE 2026-10-14 (46 beats, 8.80 min; longest non-bookend beat 16.7 s (BDEFS); BOUT padded +1.0 s)

## Built and deviations
- Scene library: `capture-scenes/capture_scenes.gd` and `vscene.gd` are copies of the planning files (`evidence/planning-checks/scratch-project/`), with ONE change: `preload("res://vscene.gd")` became the relative `preload("vscene.gd")` (the Lab project has no `res://vscene.gd`). `capture-scenes/vertex_scene.gd` is the adapter (scene id in V_ID, beat length in CLIP_L; it applies the scene's own canvas, 640 x 360 or 1280 x 720, to the capture viewport).
- The two loop clips (`flag-final`, `dials-rest`) are recorded at the longer of their two beats' lengths instead of 8.4 s loops, because ShaderLab does not loop video.
- B40: the planning run (verify10.gd) re-run on this machine today prints the same banner and `297` (`evidence/build-captures/B40-verify10-rerun.out`), so the lane's lines are real output.
- ShaderLab: the window label now wraps (it ran off the right edge on long labels: Gate V edge-bleed BLOCKERs on B29, B30, B32, B34, B38, B39); those six beats re-rendered.
PHASE captures DONE 2026-10-14 (25 captures through the scene library; no probes in the plan for scene captures beyond the planning frames, the C18 Lab still blends as expected; frames looked at: flags wave pinned at the pole, lit folds, polygon twisted vs clean, vertex-two bottom square changes colour)
PHASE scenes DONE 2026-10-14 (12 Manim classes, two agents)
PHASE slate DONE 2026-10-14 (slate 528.750000 s; Gate V BLOCKER 0, MAJOR 66 = 54 low-contrast on grey-stage captures + 12 underfill; bookend PASS; GATE T, PROOF, final not run)

## 4K master + publish run (2026-10-14; normal TOPOST path, no exceptions)
- ShaderLab shared fixes (cue tag drawn once, wider line-number column, wider side layout, label 32 px) and every ShaderLab beat re-rendered; qc.typography_regions plus qc.contrast_regions (title, file name, video label, caption; the code card is INK on near-white, 11.5:1) via _godot-shaders-series/gate_t_regions.py; B03 terracotta ring replaced by an underline bar over a grey backing; B39 caption reworded (sweep flagged a trailing preposition); BOPEN title card rebuilt at 3840
- PHASE final+publish DONE 2026-10-14: https://youtu.be/4CPj6-aKqgQ
