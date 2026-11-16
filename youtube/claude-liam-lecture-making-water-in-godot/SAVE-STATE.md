# SAVE-STATE — 2026-10-16

1. Primary Request and Intent:
   The user (Bear) invoked Claude Code from `books/` to execute a complete lecture film build for "Making Water in Godot" (`claude-liam-lecture-making-water-in-godot`), following `BUILD-PROMPT.md` exactly. Specifically:
   - Generate Kokoro audio for all 55 beats
   - Check label stills (Phase 0), run captures, Manim preflight, and all Phase 3 stills
   - Run review cut (`art run`) and final 4K master (`art final`) via `./brutalist.art/art`
   - Run every required gate to PASS (F, A, B, V, T, bookend, PROOF)
   - Fix the smallest unit and re-run only that on failure; log in `BUILD-LOG.md`
   - **Do NOT publish, stage, or upload anything**
   - **Do NOT change narration, scene design, or beat sheet**
   - Report master's absolute path, runtime, and any gate that did not pass

2. Key Technical Concepts:
   - **Kokoro TTS** (`am_onyx` voice, free, $0.00) for audio generation
   - **ShaderLab** (Remotion component): layouts `side`, `stack`, `video`; `label` cue feature on ~30 beats
   - **Gate system**: F (factcheck), A (Manim static), B (layout audit), V (frame check), T (typography), bookend, PROOF
   - **captures.py**: Godot offline harness with Lab lock (`/private/tmp/claude-501/shaderlab.lock`); C22/C29 pinned at 1280×720
   - **Manim preflight** (`preflight.sh`): content time must be under target for each scene
   - **`gate_t_regions.py`**: declares `qc.typography_regions` and `qc.contrast_regions` on all ShaderLab beats
   - **`edge_spread.py`**: measures near-edge row spread on low-flat.mp4 and low-waves.mp4
   - **B45 lineCues scaling**: terminal card cues must keep all 7 lines before 45% and ring after 55% of beat duration
   - **`_gen_lanes.py` + `make_sheet.py`**: lane generation pipeline; never re-run `make_sheet.py` after `art final`
   - **Lab lock**: shared `/private/tmp/claude-501/shaderlab.lock`; never bypass, never `pkill -f`
   - **`art run --height 2160`**: review cut; **`art final --height 2160 --out $R/exports/landscape`**: 4K master
   - **Godot 4.7.2** Forward+ (default) and Compatibility renderers

3. Files and Code Sections:
   - **`BUILD-PROMPT.md`** (`R/`): governing handoff document; defines phases, gates, traps, hard stops, final report format
   - **`BUILD-LOG.md`** (`R/`): running build log; layout stage phases already done; build stage appended with completed phases
     - Added: PHASE copies-to-remotion, phase0-stills, audio, pad-bout, title-card, voice-check, b45-cue-fix, manim-preflight, gate-t-regions, phase3-stills DONE (all 2026-10-16)
     - Added: Voice check findings (BHTF "go-dose" mispronunciation) and Mistakes section
   - **`_gen_lanes.py`** (`R/`): lane generator; **edited line 591** to fix B45 lineCues:
     - New cues [10, 57, 73, 90, 103, 117, 130] (verified at stills 25%/95%)
   - **`beat_sheet.json`** (`R/`): 55 beats; all 55 have `actual_duration_s` set; total 654.9s = 10.91 min
   - **`scenes.py`** (`R/`): assembled from scenes_act1..5.py + shader_kit.py
   - **`evidence/planning-checks/logs/edge-spread.txt`**: low-waves max 100 rows (inside 85–105 acceptable range)
   - **`media/BOPEN.mp4`**: title card 3840px wide, 11.18s
   - **`brutalist.art/runtime/remotion/public/making-water/`**: all 36 capture files + editor-inspector-dock.png present

4. Errors and Fixes:
   - **B45 lineCues past 45% threshold**: Fixed by proportional compression → [10, 57, 73, 90, 103, 117, 130]; ring 265 unchanged
   - **BHTF voice mispronunciation**: Kokoro says "go-dose" for "Godot"; logged, reported to Bear; cannot edit liam.json

5. Completed Phases:
   - copies-to-remotion ✓, phase0-stills ✓, audio ✓, pad-bout ✓, title-card ✓, voice-check ✓, b45-cue-fix ✓, manim-preflight ✓, gate-t-regions ✓, phase3-stills ✓
   - **`art run` just completed (exit code 0)** — awaiting output inspection

6. Pending:
   - Read art run output / qc-sheet.png
   - `art final $R --height 2160 --out $R/exports/landscape`
   - `python3 brutalist.art/runtime/scripts/bookend_check.py $R`
   - Fix any gate failures; write final report to Bear
