# BUILD-LOG: Godot Shader Language (overnight rough-cut run 2026-10-14)

**What this is.** Running log of the overnight build toward a 1080p slate cut.
**Why.** Resumable; mistakes recorded.
**Found.** (see PHASE lines)

PHASE audio DONE 2026-10-14 (47 beats, 9.42 min, longest body beat B09 15.5 s; BOUT padded +1.0 s)
PHASE captures DONE 2026-10-14 (stills via Lab at 1920x1080 match the plan's probes; two live clips; the pastel-to-bgr dissolve from two real renders)
PHASE scenes DONE 2026-10-14 (22 Manim classes by three parallel scene agents)

## Deviations and mistakes
- CAPTURE-PLAN's time-origin rule for C01a/C01b is inverted: the shader is mix(vec3(0.9), base, wave), so wave near 1 is TEAL and wave near 0 is the pale gray. The plan's rule (wave 0.4 or less) would put the pale phase on the Gate V frames. captures.py maximises the minimum wave instead (B40 clip: 0.99, red 0.37 at both sample times; B01 clip: 0.63, red about 0.54 to 0.60 because its two sample times cannot both sit on the teal peak).
- D1/D2 (docs screenshots for B26 and B31): docs.godotengine.org answered the headless browser with a bot-check page ("Just a moment..."); I did NOT try to get past it. B26 and B31 were switched in `lanes/act3.json` and `act4.json` (originals in `evidence/build-orig-lanes/`) from `BrowserCapture` to `ClaudeCodeBeat` quoting the page text recorded in CAPTURE-PLAN (read 2026-10-13), with a line saying it is quoted text and not a screenshot. Retake D1/D2 by Playwright when the page lets a browser in, then restore the original lanes.
PHASE slate DONE 2026-10-14 (slate 566.0 s 1920x1080; Gate V BLOCKER 0, MAJOR 11 = 9 low-contrast on pale pastel captures + 2 underfill 54 percent; bookend PASS; GATE T, PROOF, final master not run. B26/B31 quote-cards: the sparkLine note is clipped at the card edge in the cut: cosmetic, unfixed)

## 4K master + publish run (2026-10-14; normal TOPOST path, no exceptions)
- shared ShaderLab fixes (see the light-shaders entry) and every ShaderLab beat re-rendered; qc.typography_regions plus qc.contrast_regions via _godot-shaders-series/gate_t_regions.py; tag boxes in B35, B36 and B39 now grey-bordered (label-in-box overlap), B03 ring replaced by an underline bar; B26 and B31 quote-card titles are file names, B33 note and B24 caption reworded; BOPEN title card rebuilt at 3840
- PHASE final+publish DONE 2026-10-14: https://youtu.be/g0vgKR9Ac7Q
