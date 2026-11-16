# BUILD-LOG: The Shader Math Toolkit (overnight rough-cut run 2026-10-14)

**What this is.** Running log of the overnight build toward a 1080p slate cut.
**Why.** Resumable; mistakes recorded.
**Found.** (see PHASE lines)

PHASE audio DONE 2026-10-14 (47 beats, 8.80 min; longest non-bookend beat 17.2 s (BDEFS); BOUT padded +1.0 s)

## Deviations
- D1 (B12 docs screenshot): docs.godotengine.org answered the headless browser with a bot-check page; not bypassed. `lanes/act2.json` B12 switched from `BrowserCapture` to a `ClaudeCodeBeat` quote card with the three lines the plan recorded on 2026-10-13 (original lane kept in `evidence/build-orig-lanes/act2.json`), labelled "Quoted text, not a screenshot". Retake D1 with Playwright when the page allows a browser in; then restore the original lane (`python3 _gen_lanes.py && python3 make_sheet.py` before any final).
- Helpers `plot_with_strip`, `number_line`, `vec_arrow`, `chip` written in `_kit_extra.py` (the assembler now pastes `_kit_extra.py` / `_kit_cast.py` when a film has them); to be folded into the shared kit.
PHASE captures DONE 2026-10-14 (16 clips/stills; probes agree with the plan within 8-bit probe-position rounding)
PHASE scenes DONE 2026-10-14 (23 Manim classes by four parallel scene agents; they found _kit_extra.plot_with_strip drew the strip from the input not the curve's output: each act file carries a fixed variant a<N>_plot; _kit_extra.py itself left as written, fold the fix in)
PHASE slate DONE 2026-10-14 (slate 529.0 s; Gate V BLOCKER 0, MAJOR 26 = 18 underfill at 54 percent + 8 low-contrast; stopped; bookend PASS; GATE T, PROOF, final not run; the true-gray strips and black fields in the real captures are the known GATE T risk)

## 4K master + publish run (2026-10-14; normal TOPOST path, no exceptions)
- shared ShaderLab fixes (see the light-shaders entry) and every ShaderLab beat re-rendered; qc.typography_regions plus qc.contrast_regions via _godot-shaders-series/gate_t_regions.py; B24 card now a grey-bordered white card (label-in-box overlap), B30 rings replaced by underline bars; B12 quote-card title is a file name, B25 note shortened; BOPEN title card rebuilt at 3840
- PHASE final+publish DONE 2026-10-14: https://youtu.be/JK8xivmoa3g
