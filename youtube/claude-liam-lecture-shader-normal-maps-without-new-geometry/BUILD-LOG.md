# Build log

2026-10-16: authored from inspected shader source and 268 fresh passing numerical checks. Native Higgsfield was not used: the existing lecture format and actual Godot evidence are the working assumption pending any user correction. Separate film per shader; base and Lambert have different objectives despite identical code.

Compact standalone treatment; estimated runtime is a planning aid, not a measured result. Audio-first production and final visual review remain pending. No audio or master generated in this preparation stage.

Representative scene preflight and shared-schema validation: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/LAYOUT-PREFLIGHT.md

## Build stage (Claude Code): append `PHASE <name> DONE <date>` lines below this line

PHASE audio DONE 2026-10-17 (14 beats Kokoro am_onyx; total 156.0s; B05 padded to 16.00s; $0.00)
PHASE title-card DONE 2026-10-17 (opening/example-opening-8.34s.mp4; copied to media/BOPEN.mp4; lecture_opening_description shortened to 51 chars)
PHASE stills DONE 2026-10-17 (13 Remotion beats × 3 pcts = 39 stills; all cues and layouts clean; B05 capture playing correctly to completion)
PHASE gate-t-regions DONE 2026-10-17 (8 ShaderLab beats given typography_regions + contrast_regions; BOUT sparse_by_design added; BOUT handle=@NikBearBrown added)
PHASE master DONE 2026-10-17 (exports/landscape/claude-liam-lecture-shader-normal-maps-without-new-geometry.mp4; 3840×2160; 156.0s = 2:36; 9.0 MB; Gate L clean; Gate V BLOCKER=0 MAJOR=0; GATE T PASS 0 FAILs; Gate F PASS 9 rows; bookend PASS; sharpness PASS median LV=393.8; PROOF GATE present)

## Mistakes worth not repeating (build stage)

- **gate_t_regions.py lives at `_godot-shaders-series/gate_t_regions.py`**, not in brutalist.art/runtime/qc/ — use that path for every shader-series reel.
- **lecture_opening_description must be ≤52 chars**: build.py raises ValueError above that limit; shorten proactively before running audio.
- **BHTF row must be inside the main FACTCHECK.md table**: a row after a blank line is invisible to factcheck_check.py.
- **BOUT needs `handle` prop explicitly**: ClaudeTitleOutro does not inherit handle from metadata; must set `shot.remotion.props.handle = "@NikBearBrown"` in beat_sheet.json.
- **BOUT needs `qc.sparse_by_design: true`**: ClaudeTitleOutro is intentionally sparse; without the declaration, GATE V fails with `underfill`.

## Confirmed narrator

Bear explicitly confirmed Liam for every film. Use Liam, in for Bear, throughout all narration and bookends, with local Kokoro `am_onyx`. Do not substitute a Higgsfield native voice or another narrator.
