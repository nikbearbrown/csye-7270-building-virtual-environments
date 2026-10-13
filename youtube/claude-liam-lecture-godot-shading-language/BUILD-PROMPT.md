# Build the Godot Shading Language lecture

You are running from `/Users/bear/Documents/CoWork/bear-textbooks/books`.
Read this file completely and follow it. Finish the one landscape 4K film, then STOP.

## Identity and boundaries
- Reel: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language`
- Toolkit: `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art`
- Course/playlist: CSYE 7270 Building Virtual Environments.
- Exact title: Godot Shading Language.
- Persona: Liam, in for Bear; local Kokoro am_onyx; @NikBearBrown.
- 58 beats, 46 body beats in six acts. Estimated 12:16 before real speech measurement; no runtime target or cap.
- Read `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/skills/make/lecture/SKILL.md` and the toolkit's applicable instructions.
- Preserve authored narration and scene design. Fix the smallest concrete failure and log it; do not silently rewrite the film, change voice, invent evidence, or skip gates.
- No paid media generation, staging, publication, Git commit or push. No additional film or Short.

## What is already done
Complete source coverage in ACTS.md; per-beat visual audition in SHOTLIST.md; FACTCHECK.md and SOURCES.md; all narration in content.json / NARRATION.md; make_sheet.py and beat_sheet.json; eleven literal Manim Scene classes in scenes.py; registered Remotion components for all other beats; actual Godot and browser captures; reproducible Godot source.

Twenty positive shader files rendered in Godot 4.7.2 Compatibility on Apple M4 Pro without shader errors. Twenty-four actual pixel assertions passed. A deliberate type error produced a real diagnostic. Eleven static animation checks passed with zero errors and warnings; beat lint and runtime project validation passed. These are **preparation checks**, not final audiovisual QA.

Audio, scene stills, movie clips and master are not yet built. No measured speech durations are claimed. Open HOLDs: zero. No user decision is pending for the free build.

## Commands in order, from books/

1. Validate, generate audio, apply explicit silences, then rebuild props from measured timing:

```bash
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/validate_package.py
python3 ./brutalist.art/runtime/scripts/generate_audio_kokoro.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/prepare_audio.py
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/make_sheet.py
python3 ./brutalist.art/runtime/scripts/align.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/prepare_opening.py
```

The art entry point dispatches `run` and `final`; audio and stills use its documented runtime scripts. There is no invented `art audio` command. Do not use direct `npx remotion render`.

Kokoro currently ignores the declared pause fields, so prepare_audio.py adds BIDEA's 0.8-second lead, BVDT's 0.5-second lead, and BOUT's 1-second tail idempotently and remeasures with ffprobe. If revoicing a beat, use `--only BID`, rerun prepare_audio.py and make_sheet.py, and re-align only changed beats. Do not carry measured audio after changing narration. `make_sheet.py` preserves audio only when the text is identical.

BOPEN must be narrated. prepare_opening.py uses the approved title template after measuring BOPEN, copies the resulting video-only hold to media/BOPEN.mp4, and lets the standard compiler mux narration. Professor Bear is labeled as himself; Liam is the narrator. Slug-seeded portrait selection is professor-bear-1x1-93.png. No silent opener, jingle, film number, video count or placeholder.

2. Preview all scenes at low resolution before the 4K review:

```bash
python3 /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/preflight.py
```

This renders Manim end-frame stills and Remotion 25/50/95-percent stills. Actually inspect every image; make a contact sheet if useful. Inspect the writer's final corrected text, all code lines, matrix column layout, screenshot zooms, six-line recap pagination, full learner prompt, opening portrait/title and outro. Document defects and fixes in CHECKS-REPORT.md. Passing a subprocess does not imply visual approval.

The Manim cue helper reads mp3/words.json and maps authored phrases to actual speech when available. Check the cue timings by ear and eye. Remotion code lineCues are initially distributed across the measured narration; align important declarations and error lines to their spoken phrases before final rendering. BrowserCapture moves avoid the midpoint window. This synchronization is mechanical finishing of the authored scene design.

3. Render the review cut through the canonical entry point:

```bash
./brutalist.art/art run /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language --height 2160
```

Run foreground. Remotion goes through runtime/scripts/remotion_scenes.py with concurrency one. Do not render multiple shared-media jobs concurrently. Do not edit the sheet while a compiler is running. Read and fix Gate F, A, B, V and T results. No PUNT or missing clip can ship. If a scene changes, move only its stale per-beat clip and corresponding cache into `_superseded/` before rerendering; do not remove unrelated assets.

4. Inspect the review cut, then create and verify the master:

```bash
python3 ./brutalist.art/runtime/scripts/type_check.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language
./brutalist.art/art final /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language --height 2160 --fps 24 --out /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language/exports/landscape
python3 ./brutalist.art/runtime/scripts/bookend_check.py /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shading-language
```

The final filename is reported by the compiler. Probe that exact file: 3840×2160, 24 fps, readable video and audible narration. Compare runtime with the sum of measured audio durations within one frame per beat of rounding. Inspect 15/50/85-percent samples of each beat and the continuous final film, including at least 2 fps frame coverage per the toolkit's visual-QC rule. Listen to pronunciation of Godot, GLSL, UV, ALBEDO, CSYE 7270, numbers and the greeting. Verify the last second is silent and the final title does not cut on a syllable. Preserve sidecar captions, no burned captions.

## Known traps and evidence limits
- The legacy JSON schema excludes shot.type CARD, but the current lecture opener contract explicitly requires BOPEN CARD. The active runtime project validator and beat lint accept the mandated template. Do not change the opener to dodge that obsolete enum or edit a shared checker.
- The static checker initially misread Matrix numeric entries as screen coordinates; B19 now uses proper MathTex matrices and explicit geometric column highlights, and passes. Inspect the actual math frame for bounds and typography.
- Captures show actual engine output, not hypothetical mock results. Keep their color information; it is the evidence. Diagrams are labeled conceptual. Native editor capture is 3456×2070 and uses imageAspect from its real dimensions, not a fake 16:9 claim.
- Code cards are executed source excerpts, never fabricated Claude output. Shell cards contain retained local diagnostics/reports. No historical Claude Code session is asserted, so SESSION.md is unnecessary.
- Incoming COLOR preserves the CanvasItem texture/vertex contribution; arbitrary texture(TEXTURE, UV) substitution would change the lesson. Do not rewrite flash.gdshader to lose base alpha.
- The community homepage was visibly captured with HTTP 454; do not claim 200. Its content was inspected. Source transcript author/title/URL are unspecified; do not invent them.
- The negative test intentionally logs SHADER ERROR. It is separate from the clean positive run. Never count the negative test as a clean shader, and never ignore positive-run diagnostics.
- Actual rendering evidence is on one local GPU and one renderer. Compute is explained from official documentation and is not executed in this Compatibility lab. Collider behavior is a conceptual distinction, not a claimed physics integration test.
- B07 compares real opaque and transparent cube captures; alpha alone is not called glass. B33 compares real switch/fallthrough outputs. Never replace these with stock pictures.
- Stills and current static checks do not certify final readability, audio, alpha behavior on other artwork, game meaning or performance.

## Required completion report
Write actual gate results and fixes to BUILD-LOG.md and `_qc/REPORT.md`. Do not fabricate human signatures. Keep any unresolved gate plainly marked failed or unrun.

Report the master's absolute path, measured runtime, final lane histogram, zero/unresolved HOLD count, and any gate that did not pass. Do not claim completion if any required gate fails. STOP at the local master. Never stage or publish.
