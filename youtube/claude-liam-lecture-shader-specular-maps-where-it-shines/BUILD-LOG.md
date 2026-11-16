# Build log

2026-10-16: authored from inspected shader source and 268 fresh passing numerical checks. Native Higgsfield was not used: the existing lecture format and actual Godot evidence are the working assumption pending any user correction. Separate film per shader; base and Lambert have different objectives despite identical code.

Compact standalone treatment; estimated runtime is a planning aid, not a measured result. Audio-first production and final visual review remain pending. No audio or master generated in this preparation stage.

Representative scene preflight and shared-schema validation: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/LAYOUT-PREFLIGHT.md

2026-10-18 build: install_assets.py confirmed idempotent. Audio generated (Kokoro am_onyx): 14 beats, 151.97s total. B05 padded to 16.00s (capture minimum). BOPEN card display subtitle shortened from 66→48 chars ("Packed masks control rim and highlight strength.") for title-builder budget; narration unchanged. Title slide built: example-opening-7.63733s.mp4 inspected — layout, portrait, series/title/subtitle/narrator credits and handle correct. Stills preflight at 25/50/95%: all 13 rendered scenes checked visually. No layout failures found. Code highlights land on correct lines; B05 video capture readable; Godot captions "Spec masks: all one" and "Spec masks: R rim / G highlight" clear at final size; BVDT items correct; BHTF prompt with two checks correct; BOUT exact title and handle confirmed.

qc.contrast_regions (title heading box [0.06, 0.04, 0.85, 0.12]) added to B01–B08 before art run; qc.sparse_by_design added to BOUT; handle:"@NikBearBrown" added to BOUT props (same documented pattern as prior shader films). GATE V: BLOCKER=0, MAJOR=0 (first pass). GATE T: PASS (§8.10 BVDT advisory non-blocking). GATE BOOKEND: PASS. Master: exports/landscape/claude-liam-lecture-shader-specular-maps-where-it-shines.mp4, 3840×2160, 152.333s. Audio verified: BOPEN "Godot shader techniques, specular maps where it shines, explain independently packed masks for rim and highlight strength." — correct. BOUT "Specular maps where it shines at Nick Bear Brown." — correct. Tail silence RMS=0.0. Not staged or published.

## Confirmed narrator

Bear explicitly confirmed Liam for every film. Use Liam, in for Bear, throughout all narration and bookends, with local Kokoro `am_onyx`. Do not substitute a Higgsfield native voice or another narrator.
