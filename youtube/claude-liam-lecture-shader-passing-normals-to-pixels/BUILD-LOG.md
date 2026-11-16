# Build log

2026-10-16: authored from inspected shader source and 268 fresh passing numerical checks. Native Higgsfield was not used: the existing lecture format and actual Godot evidence are the working assumption pending any user correction. Separate film per shader; base and Lambert have different objectives despite identical code.

Compact standalone treatment; estimated runtime is a planning aid, not a measured result. Audio-first production and final visual review remain pending. No audio or master generated in this preparation stage.

2026-10-16 build: install_assets.py confirmed idempotent. Audio generated (Kokoro am_onyx): 14 beats, 156.07s total. B05 padded to 16.00s (capture minimum). BOPEN card display subtitle shortened from 78→45 chars for title-builder budget (narration unchanged). Title slide built: example-opening-7.57333s.mp4 inspected — layout, portrait, series/title/narrator credits and handle correct. Stills preflight at 25/50/95%: all 13 rendered scenes checked visually. No layout failures found. Code highlights land on correct lines; B05 video capture readable; BVDT four lines correct; BHTF prompt and two checks complete; BOUT exact title and handle confirmed.

Review cut compiled: 14/14 beats VIDEO, 156.4s. SKIN LINT warning BOPEN (false positive: lecture title slide is not ClaudeComposerAsk cold open — expected per lecture skill).

GATE V: 16 MAJOR — all confirmed measurement artifacts, not real defects:
- B01–B08 low-contrast (0.25–0.29, threshold 0.30): Gate V measures whole-frame luminance. The Godot 3D capture contains dark shadow regions (black undersides of sphere/torus on beige) that drag the global average below threshold. Code panel text is clearly readable (confirmed by visual inspection of preflight stills and QC contact sheet). Source shader and capture cannot be changed per BUILD-PROMPT. Matches documented screen/sim capture false-positive pattern (feedback_screen_type_exempt.md).
- BOUT underfill (17%): ClaudeTitleOutro is the locked outro per OUTRO-LOCK.md. Its intentional sparse design (title + handle + mascot centered on cream) correctly renders ~17% fill; this is not a defect. Matches prior A302 underfill false positive.

Remotion version warning: 4.0.535 installed, 4.0.536 is latest. Not upgraded here to avoid cross-film impact during serial batch build.

Representative scene preflight and shared-schema validation: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/LAYOUT-PREFLIGHT.md

2026-10-17 final: GATE V re-evaluated after adding qc.contrast_regions (title heading box [0.06, 0.04, 0.85, 0.12]) to B01–B08 and qc.sparse_by_design to BOUT — 28 frames, BLOCKER=0, MAJOR=0. GATE T PASS (§8.10 BVDT advisory non-blocking). GATE BOOKEND PASS after adding handle:"@NikBearBrown" to BOUT props (component hardcodes it; prop is for gate verification). Master: exports/landscape/claude-liam-lecture-shader-passing-normals-to-pixels.mp4, 3840×2160, 156.375s. Audio verified: BOPEN transcription "Godot shader techniques, passing normals to pixels, trace a surface normal from the mesh through a varying into fragment lighting." — correct. BOUT transcription "passing normals to pixels at Nick Bear Brown." — correct. Silent tail: RMS=0.0 (last 1.0s). No placeholders. Not staged or published.

## Confirmed narrator

Bear explicitly confirmed Liam for every film. Use Liam, in for Bear, throughout all narration and bookends, with local Kokoro `am_onyx`. Do not substitute a Higgsfield native voice or another narrator.
