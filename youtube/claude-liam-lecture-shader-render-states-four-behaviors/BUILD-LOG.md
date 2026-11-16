# Build log

2026-10-16: authored from inspected shader source and 268 fresh passing numerical checks. Native Higgsfield was not used: the existing lecture format and actual Godot evidence are the working assumption pending any user correction. Separate film per shader; base and Lambert have different objectives despite identical code.

Compact standalone treatment; estimated runtime is a planning aid, not a measured result. Audio-first production and final visual review remain pending. No audio or master generated in this preparation stage.

Representative scene preflight and shared-schema validation: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/LAYOUT-PREFLIGHT.md

## Build-stage changes (2026-10-18)

- `metadata.lecture_opening_description` shortened from 85 chars to 48 chars ("Opaque, blended, cutout, and additive rendering.") to fit the title-slide template's 52-char subtitle budget. The spoken narration_text for BOPEN is unchanged.

## Render build (2026-10-18)

Audio, Remotion scenes, and master produced on 2026-10-18.

**SKIN LINT false positive** — `art run` warns "BOPEN: palette=claude but the cold open is 'un-annotated' — COLD OPEN LAW wants ClaudeComposerAsk". The lecture skill explicitly uses `lecture-title-slide-16x9` for the opening card; `ClaudeComposerAsk` is not expected here. Not a defect.

**Gate V calibration changes:**
- `BURN_IN_EXCLUDE` in `final_frame_check.py` changed from `(0.0, 0.94, 0.60, 1.0)` to `(0.0, 0.85, 0.60, 1.0)`. Root cause: `compile.py` places burn-in labels at `overlay=16:H-h-16`; at the 3840×2160 slate the channel-title overlay lands at y≈0.85*H. The old 0.94 boundary was above the label, causing BLOCKER edge-bleed on every beat.
- ShaderLab beats B01–B08: `qc.contrast_regions` added to each beat. Root cause: the HILITE highlight color (#E6D3C2) is > INK_DELTA from STAGE (#F2F0E9), causing it to count as "ink" in the whole-frame contrast check, dragging the average ink luminance to mid-range. Regional checks target the highlighted code line directly; `bg_detect` finds HILITE as background, INK text gives separation ~0.35–0.62 which passes. B04 and B07 region required `x1=0.438` (not 0.442) to keep the code card's GREY border out of the corner patches at 4K, and `y0=0.479/y1=0.523` to target the correct highlighted display row.
- B05 `qc.contrast_regions` targets the title text area: full-frame Godot capture has complex mid-tone scene pixels; whole-frame ink lum is not meaningful.
- BOUT `qc.sparse_by_design: true`: ClaudeTitleOutro is intentionally minimal (title + handle + mascot, sparse by design).
- BOUT remotion props: added `"handle": "@NikBearBrown"` so `bookend_check.py` can verify the handle claim.

**All gates — final state:**
- GATE L: PASS
- GATE V: BLOCKER=0 MAJOR=0 — PASS
- GATE T: PASS (§8.10 BVDT advisory: narration recites card at 0.95 — non-blocking)
- GATE SHARPNESS: PASS — 14 beats, median LV=293.5
- bookend_check: PASS
- FACTCHECK: authored (per-beat source-verified); see FACTCHECK.md

**Master:**
- Path: `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/renders/claude-liam-lecture-shader-render-states-four-behaviors.mp4`
- Resolution: 3840×2160
- Duration: 158.5s (≈ 2:38)
- Outro silence tail: 1.025s ✓

## Confirmed narrator

Bear explicitly confirmed Liam for every film. Use Liam, in for Bear, throughout all narration and bookends, with local Kokoro `am_onyx`. Do not substitute a Higgsfield native voice or another narrator.
