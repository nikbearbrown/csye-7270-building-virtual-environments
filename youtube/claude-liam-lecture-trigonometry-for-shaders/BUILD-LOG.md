# BUILD-LOG: Trigonometry for Shaders (overnight rough-cut run 2026-10-14)

**What this is.** Running log of the overnight build toward a 1080p slate cut.
**Why.** Resumable; mistakes recorded.
**Found.** (see PHASE lines)

PHASE audio DONE 2026-10-14 (46 beats, 8.73 min; longest non-bookend beat 15.6 s (BDEFS); BOUT padded +1.0 s)

## Built and deviations
- Harness extended: `--sprite-res N` and `--linear` (a 512 px linearly filtered blob for the sweep clips, as the plan asks).
- Square captures are 1920 x 1920 and their ShaderLab windows are square: `videoAspect: 1` added to those lanes (the plan says a square capture gets a square window) and ShaderLab's side layout now caps the window height (640 px) for squarer captures. Originals in `evidence/build-orig-lanes/`.
- D1 and D2 (B08 and B33 docs screenshots): docs.godotengine.org showed a bot-check page to the headless browser; not bypassed. B08 and B33 lanes switched from `BrowserCapture` to `ClaudeCodeBeat` quote cards of the sentences the plan recorded on 2026-10-13, labelled "Quoted text, not a screenshot". Retake with Playwright later and restore.
PHASE captures DONE 2026-10-14 (13 captures; probes match the plan: planet teal, moon 0.502/0.600/0.749 at (0.7598,0.65), atan colours, sweep wedges)
PHASE scenes DONE 2026-10-14 (23 Manim classes, three agents)
PHASE slate DONE 2026-10-14 (slate 524.666667 s; Gate V BLOCKER 0, MAJOR 26; bookend PASS; GATE T, PROOF, final not run)

## 4K master + publish run (2026-10-14; normal TOPOST path, no exceptions)
- shared ShaderLab fixes (cue tag once, wider side layout, stack excerpt whole rows and a wide label, 32 px label, code over 18 rows set at 27 px so no line clips) and every ShaderLab beat re-rendered; qc.typography_regions plus qc.contrast_regions via _godot-shaders-series/gate_t_regions.py; B25 rings replaced by underline bars; B17 grid darkened (Gate V); B28 given a title (square capture underfill); B08 and B33 quote-card titles are file names, B22 caption reworded; BOPEN title card rebuilt at 3840
- PHASE final+publish DONE 2026-10-14: https://youtu.be/JioKVZbdzxQ
