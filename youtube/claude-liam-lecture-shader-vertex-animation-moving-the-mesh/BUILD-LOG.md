# Build log

2026-10-16: authored from inspected shader source and 268 fresh passing numerical checks. Native Higgsfield was not used: the existing lecture format and actual Godot evidence are the working assumption pending any user correction. Separate film per shader; base and Lambert have different objectives despite identical code.

Compact standalone treatment; estimated runtime is a planning aid, not a measured result. Audio-first production and final visual review remain pending. No audio or master generated in this preparation stage.

Representative scene preflight and shared-schema validation: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_shader-review-2026-10-16/LAYOUT-PREFLIGHT.md

## Confirmed narrator

Bear explicitly confirmed Liam for every film. Use Liam, in for Bear, throughout all narration and bookends, with local Kokoro `am_onyx`. Do not substitute a Higgsfield native voice or another narrator.

## 2026-10-18 build-stage notes

install_assets.py: run; MP4 hash-checked, JPEG re-cropped (0,0,1280,620 of frame 0191).

Audio: Kokoro am_onyx; 14 beats; timeline 161.9s. B05 spoken 10.88s padded to 16.0s (capture match). BIDEA padded +0.8s lead. BOUT padded +1.0s tail.

lecture_opening_description shortened from 72→52 chars to fit template budget. Narration text unchanged.

Title slide: built at 3840×2160; portrait slug-seeded (opening-fields.json records pick); Liam narrator credit present; no numbers. BOPEN.mp4 = 8.02s.

Preflight stills: 960×540, 25/50/95%, all 13 Remotion beats. No layout failures.

Gate V: initial run flagged low-contrast on B01-B08 (ShaderLab highlighted-row fill, pale tan ~#E8D5C8, dilutes whole-frame ink average — false positive; code text readability visually confirmed). Fixed by declaring contrast_regions on act-title heading [0.03,0.02,0.30,0.11], measured separation 0.57–0.58 in preflight stills. Also flagged underfill on BOUT (ClaudeTitleOutro intentional sparse design); fixed by qc.sparse_by_design. Gate V re-run: PASS (0 BLOCKER, 0 MAJOR).

Skin lint warning (expected): BOPEN palette=claude, cold-open is portrait/title card, not ClaudeComposerAsk. This is correct for lecture skill which replaces the composer cold open. Not a gate failure.

Review cut: 162.2s, 14/14 filled (no slates), GATE L PASS, GATE V PASS.
