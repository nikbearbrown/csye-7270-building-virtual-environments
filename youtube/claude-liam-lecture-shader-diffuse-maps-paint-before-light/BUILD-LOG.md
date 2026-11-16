# Build log

2026-10-16: authored from inspected shader source and 268 fresh passing numerical checks. Native Higgsfield was not used: the existing lecture format and actual Godot evidence are the working assumption pending any user correction. Separate film per shader; base and Lambert have different objectives despite identical code.

Compact standalone treatment; estimated runtime is a planning aid, not a measured result. Audio-first production and final visual review remain pending. No audio or master generated in this preparation stage.

Representative scene preflight and shared-schema validation: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/LAYOUT-PREFLIGHT.md

2026-10-17 build: install_assets.py confirmed idempotent. Audio generated (Kokoro am_onyx): 14 beats, 156.86s total. B05 padded to 16.00s (capture minimum). BOPEN card display subtitle shortened from 69→42 chars for title-builder budget (narration unchanged: "Godot Shader Techniques. Diffuse Maps: Paint Before Light. Trace a color texture through UV sampling and diffuse multiplication."). Title slide built: example-opening-7.72267s.mp4 inspected — layout, portrait, series/title/subtitle/narrator credits and handle correct. Stills preflight at 25/50/95%: all 13 rendered scenes checked visually. No layout failures found. Code highlights land on correct lines; B05 video capture readable; Godot caption "Tint the diffuse texture; highlight added separately" clear at final size; BVDT four items correct; BHTF prompt with two checks correct; BOUT exact title and handle confirmed.

qc.contrast_regions (title heading box [0.06, 0.04, 0.85, 0.12]) added to B01–B08 before art run; qc.sparse_by_design added to BOUT; handle:"@NikBearBrown" added to BOUT props. These are the same documented exemptions used for the normals film — ShaderLab HILITE tan (#E6D3C2) and Godot 3D capture mid-tones dilute whole-frame luminance; regional title-heading sep ~0.72; BOUT locked outro 17% fill is by design.

Review cut compiled: 14/14 beats VIDEO, 157.2s. SKIN LINT warning BOPEN (false positive: lecture title slide is not ClaudeComposerAsk cold open — expected per lecture skill). GATE V: BLOCKER=0, MAJOR=0 (first pass). GATE T: PASS (§8.10 BVDT advisory non-blocking). GATE BOOKEND: PASS. Master: exports/landscape/claude-liam-lecture-shader-diffuse-maps-paint-before-light.mp4, 3840×2160, 157.167s. Audio verified: BOPEN "Godot shader techniques, diffuse maps, paint before light, trace a color texture through UV sampling and diffuse multiplication." — correct. BOUT "Diffuse maps paint before light at Nick Bear Brown." — correct. Tail silence RMS=0.0 (last 1.0s). Not staged or published.

## Confirmed narrator

Bear explicitly confirmed Liam for every film. Use Liam, in for Bear, throughout all narration and bookends, with local Kokoro `am_onyx`. Do not substitute a Higgsfield native voice or another narrator.
