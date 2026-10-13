# BUILD-LOG.md — claude-liam-lecture-blender-to-godot

First film built with the `lecture` skill (skill written 2026-10-02, no earlier film). Built 2026-10-06.

## Request and interpretation
Bear: "use the lecture skill to start doing initial cuts of all of the missing videos that we laid out" (the production list in
`books/youtube/nbb/playlist-course-map/`, CSYE 7270 file: 11 of 16 chapters have no film; 31 films listed to make), then "use the Liam persona, this is for the
Nik Bear Brown" (channel claude-liam, @NikBearBrown, Liam in for Bear). Interpretation used: ONE lecture per chapter that has no film (a lecture is one whole chapter as one
film), whose acts cover the chapter's listed "still needed" premises. Pilot = Chapter 3 (Blender → Godot), first in map order with zero coverage. NOT confirmed by Bear
(open question in the hand-over): per-chapter lectures vs the 31 premise-level films; CSYE only vs all seven courses.
No `metadata.course` is set: the CSYE 7270 films carry no course credit (bookloop law applies; only INFO 7375 films are exempt).

## Decisions
- Greeting Bonjour (Kokoro-clean). Channel claude-liam; BOUT = ClaudeTitleOutro (OUTRO-LOCK). Title "Proving a 3D Model Arrived in Godot".
- Beat IDs must be UPPER-CASE (`build_safety.validate_project`: `[A-Z][A-Z0-9_]*`); splits are B33A/B33B, B47A/B47B, B67A/B67B, B71A/B71B.
- 75 body beats; 80 beats total; measured narration ≈ 14.9 min. Four beats split because they ran past 15 s.
- Unity/Unreal comparisons, MCP install steps, Walker framework text, exercises: LEFT OUT with reasons in ACTS.md.
- Real evidence re-run 2026-10-06 (Blender 5.1.2, Godot 4.7.2): three-column probe, stale-dimensions, exit-code; Blender Workbench renders of the post; a REAL Blender window screenshot
  (scratch `BLENDER_USER_CONFIG` so Bear's Blender prefs were not touched); real Blender and Godot app icons.

## Toolchain facts learned (for the next lecture)
- Remotion compositions run at **30 fps** (Manim at 24). Stills: frame = seconds × 30 × pct.
- `FlowDiagram` is NOT renderable (older docs name it). `./art scenes --check <Name>` first.
- `generate_audio_kokoro.py --only` drops BOUT's 1.0 s pad: re-pad (apad 1.0) and write `actual_duration_s` back after any full run. Kokoro reads "glTF/GLB/MCP/FBX/OBJ/UV" badly: spelled out in narration only.
- `art` Gate F reads FACTCHECK/SHOTLIST/PROMPTS; `build_docs.py` writes SHOTLIST/FACTCHECK/CHECKS-REPORT from `lanes/*.json` and `factcheck/*.md`.
- Gate A static check must run from a folder holding ONLY scenes.py; `preflight.sh <act> <classes…>` does that in a private scratch and also runs the layout audit and a last-frame still.
- Manim `ImageMobject("pantry/…")` resolves from the reel folder (scratch folders need a `pantry` symlink).
- Another session was rendering Remotion for a different lecture (anthropics/muse/film-01) at the same time: Remotion renders contend; run 4K renders strictly one at a time.

## Whisper check of the audio (base.en)
Greeting/outro clean. Worth a listen: B21 ("ticks" heard as "takes"), B37 ("Godot" once heard as "God out"), BDEFS ("Six terms. A mesh" runs together). Digit-vs-word differences are normalisation only.

## Narration corrections made after the builders checked every claim (2026-10-06; all re-voiced, factcheck rows updated)
- B56 "Sixteen of sixteen" → **Fifteen of fifteen**; B67A "Seventeen of seventeen" → **Sixteen of sixteen**: the recorded test logs have 15 and 16 PASS lines (the chapter's counts came from `grep -c "_check("`, which also counts the `func _check(` definition).
- B09 now "In the community version, an add-on…" (the socket is stated only on the community project's page); B11 "By default, both run agent-written code with no guard" (the community project has an opt-in safe mode); B12 "The Blender Lab page warns of the same risk: no guards" (it says nothing about authentication or a port).
- B25 "post" → "column"; B28 "Separately, its export guidance…" (Godot's stated reason for applying the transform is editor selection, not physics).
- B38 "ignores the collision hints in your model's names" (was "every naming hint"); B41 "Through Blender's glTF export, a collider has to be a mesh" (Godot 4.7.2 has glTF physics-shape classes); B42 "primitive shapes often perform best, convex shapes are a compromise, and concave shapes are the slowest" (the page states no strict ranking).
- B65 "saw it was already on, removed the extra physics block" (the starting import already had use_node_type_suffixes=true); B70 "about eleven centimetres on each side, halfway up the taper" (0.110 m at the middle of the taper; the maximum near the base is ≈ 0.22 m).

## Gates (run 2026-10-06)
Gate F (242 claims, 3 CORRECTED, 0 unresolved) · Gate A static · Gate W · layout audit · Gate L · bookend PASS · Gate V first run BLOCKER 3 / MAJOR 9 → fixed (darkened pale marks in B01/B61/B62/B69; pre-cropped the two Codex windows so nothing crosses the title-safe edge; documented underfill waivers for B14 and B28) → **0 / 0** · GATE T first run FAIL (B11, B42: the terracotta ring on the two real-page captures read as accent text) → BrowserCapture `ringColor "#A64A24"` → **PASS** (80 beats).
Master: `exports/landscape/claude-liam-lecture-blender-to-godot.mp4` · 3840×2160 · 24 fps · 902.0 s · AAC 48 kHz stereo · clean (no beat labels; the `-slate.mp4` review cut keeps the burn-in labels) · narration ends 900.35 s, 1.65 s silent tail.
Lane histogram: 66 Manim, 5 CCSession, 2 BrowserCapture, 1 CCPlainShell, 1 LibraryIconRow, 5 bookends. Runtime 15.0 min.

## Mistakes worth not repeating
- Two `art run`s on one reel at once race on `media/videos/…` (`mv: No such file`). A command started with `nohup … &` inside a short background command is NOT killed when that command ends; check `ps` before starting another run, and run `art run` itself as the background task.
- Remotion stills are 30 fps (I first sampled at 24).
- `art run` compiles per-beat clips even when the final concat is interrupted; re-running finishes it from cache.

## Open items for Bear (nothing is staged or published)
1. Listen to it. Never heard by a human: B21 ("ticks" heard as "takes"), B37 ("Godot" once heard as "God out"), BDEFS ("Six terms. A mesh" runs together).
2. The recorded working-folder name `walker-3d-platformer-asset` is visible in the title bar of the five Claude Code session beats (B48–B51, B54) and in the Codex window stills (B64–B66). It is a real captured value (left unaltered); keep it, or relabel it.
3. The Codex window templates have no failure state (they put a green tick on every line); B65 draws crashes as an ink ledger beside them. B66 uses a real dark Codex tool card (passed Gate T at 4K).
4. B21 adds one directional light to Godot's night-scene demo so it is visible (disclosed in the lane and factcheck). B20 tested only the unit-scale-1 case. B24 uses a three-size "test box" for the axis swap, labelled on screen.
5. B11/B12 show real captures of public pages (GitHub README, blender.org Lab page) taken 2026-10-06; B28/B42 show Godot's docs (CC BY 3.0, domain and title on screen).
6. The source chapter and its record still carry the wrong numbers/claims (this film does not): chapters/03 L13, L292, L332 (counts 16/17 → 15/16), L124 (speed ranking of shape types), L334 (11 cm "at mid-height"), L38-ish and L124 "In glTF, a collider has to be a mesh"; examples/03/README.md L7, L18, L20 (counts), L68 ("up to 11 cm each side at mid-height"; the real maximum is ≈ 22 cm just above the base).
7. Scope: this is the only chapter built so far. Whether to make a lecture for each remaining chapter (4, 6–11, 13–15) or the map's 31 premise films, and whether the other six courses follow, is Bear's call.
