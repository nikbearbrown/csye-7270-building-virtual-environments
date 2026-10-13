# Preparation checks

58 beats: 46 body SHOW beats, 6 act-title CARD beats, 6 required opening/closing beats. No HOLD and no unresolved PUNT. Lane histogram: {'bookend': 6, 'card': 6, 'manim': 11, 'code': 20, 'capture': 13, 'shell': 2}.

Teaching arc: framework B01 before the first example; worked examples B04–B07 and B36–B37; falsifiability B16 and B33; scaffolded task BHTF with two independent checks; mandated lecture bookends present; source/evidence references in FACTCHECK.md.

Evidence: 20 positive shader files rendered without SHADER ERROR; 24 pixel assertions pass. The invalid type test is rejected by the compiler. Real source captures were visually inspected. Source author/URL for the pasted transcript remains unspecified and is not invented.

Structural checks: literal scene classes resolve, registered Remotion patterns resolve, narration is present, BHTF command matches narration, no numbered-video metadata. Static scene checker results are in evidence/static-scene-checks.json. Local schema validation and source checks are recorded in evidence/package-validation.json.

Not yet run: TTS, word alignment, low-resolution film-scene stills, Gate B pixel layout, Gate V frame review, Gate T typography, sharpness, audio/listening review, final bookend verification and final-master duration/dimensions. Those cannot pass before rendering. No blank gate result is called a PASS.

---

# Preflight visual inspection — 13 October 2026

Audio: 58 beats generated (Kokoro am_onyx, $0.00). prepare_audio.py applied BIDEA 0.8 s lead, BVDT 0.5 s lead, BOUT 1.0 s tail idempotently and remeasured. align.py wrote words.json (58 beats aligned, 0 fallbacks). make_sheet.py wrote measured durations into beat_sheet.json; estimated unmeasured runtime 736 s (~12:16).

BOPEN: prepare_opening.py built a 9.96 s video-only hold from the approved title template; narration muxed by the standard compiler.

Manim scenes inspected (11 end-frame stills):
- B01_Pipeline: geometry → fragments diagram — correct, labels readable
- B07_SpatialComparison: two real Godot cube captures side-by-side — evidence intact
- B09_Displacement: collision ≠ rendered rectangle — clear conceptual diagram
- B11_TimeInput: clock hand + offset square — matches sin(TIME) claim
- B14_Independent: fragment grid with one highlighted pixel — correct invocations
- B17_VectorCells: four labelled component cells (r=0.2, g=0.6, b=0.9, a=1.0) — values from swizzle.gdshader
- B19_MatrixColumns: MathTex column vectors and assembled mat2, terracotta highlight on column 0 — verified
- B30_Interpolation: black-to-white gradient bar with midpoint mark — matches UV.x claim
- B33_Fallthrough: two real Godot captures (with breaks vs fallthrough, 0.25/0.75 vs 0.10) — evidence intact
- B35_LoopTrace: three indexed value cells + "3 · stop" in terracotta — correct bounded loop
- B44_Experiment: Base/Prediction pair with Compare line — correct scaffold

Remotion beats inspected (25/50/95% stills, 47 Remotion beats sampled):
- BIDEA: writer animation mid-frame — correct
- BDEFS: 4 terms (GPU, Vertex, Fragment, Material) — correct count, no truncation
- BACT1–BACT6: single-line act titles centred — correct
- B02/B06/B08/B10/B12/B15/B18/B20/B22/B26/B29/B34: ClaudeCodeBeat — all readable, correct shader source, no overflow
- B03/B05: BrowserCapture — Godot Inspector panel with terracotta Material ring; actual Godot render
- B13: BrowserCapture — uv.gdshader render, real colour gradient
- B16: CCPlainShell — SHADER ERROR: Invalid assignment of 'int' to 'float'. diagnostic visible
- B24: BrowserCapture — shared ShaderMaterial, two squares, slight right crop within frame (acceptable at 4K)
- B40: BrowserCapture — thebookofshaders.com, page text visible
- B43: BrowserCapture — Godot compute shaders docs, fine at 4K
- BVDT: 6 lines paginate correctly (1-2 at 25%, 3-4 at 50%, 5-6 at 95%) — no 5-line defect
- BHTF: full prompt and two independent check lines — correct
- BOUT: ClaudeTitleOutro "Godot Shading Language." @NikBearBrown + mascot — correct

Defects found during visual inspection: NONE blocking. B24 right edge slightly cropped but both squares visible — acceptable. All code text readable, all labels ≤ 3 words, no narration set as type, no bullet lists.

Gates outstanding before master is complete: Gate F (FACTCHECK ✓ from stage-1), Gate A (audio alignment — align.py clean), Gate B (pixel layout from 4K render), Gate V (review cut visual), Gate T (type_check.py), bookend_check.py.
