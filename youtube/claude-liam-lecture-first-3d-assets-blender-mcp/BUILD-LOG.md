# BUILD-LOG.md — claude-liam-lecture-first-3d-assets-blender-mcp

## What this is, what was found
A 13.4-minute film of Assignment 3 ("Your First 3D Game Assets with Claude, the Blender MCP, and Blender") for CSYE 7270, narrated by Liam in for Bear, built with the `lecture` skill on 2026-10-06. It follows the assignment in seven acts and ends with the recap, the Your Turn prompt and the channel outro. **The master is built and every machine gate passes. Nothing is staged or published.**

What matters before you watch it:
- **The MCP route is not shown running, because nobody has run it.** Its three commands appear without output, labelled "documented, not run". The three assets in the film were built by a Blender script (the assignment's fallback route), and the film says so. Someone still has to run the MCP route once before the assignment is released.
- **The real tools were run to get the pictures.** Every number and every window on screen comes from a recorded run: Blender 5.1.2 built the crate, lantern and coin (60, 202 and 180 triangles) and took the window screenshots; Godot 4.7.2 imported them and ran the headless check. Those runs found four mistakes in the assignment and my first narration; all are fixed (see Corrections).
- **The Blender screenshots were taken by a script, not by a person at the keyboard**, with scratch preferences (your Blender settings were never touched). The hand-edit before/after is scripted too, and is labelled "illustrative" on screen.

Master: `exports/landscape/claude-liam-lecture-first-3d-assets-blender-mcp.mp4` · 3840×2160 · 24 fps · 806.13 s · AAC 48 kHz stereo · clean (no beat labels) · narration ends 804.5 s, 1.6 s silent tail. Review cut with burn-in labels: `claude-liam-lecture-first-3d-assets-blender-mcp-slate.mp4`.
Lane histogram: 68 Manim, 5 bookends, 7 Remotion (2 BrowserCapture, 4 CCPlainShell, 1 ClaudeCodeBeat). 80 beats, 79 SHOW / 1 CARD.

## Request and interpretation
Bear: "Use the lecture skill, Liam persona, to make a film on this." followed by the full text of Assignment 3 (dictation: "lecture scale"). Interpreted as the `lecture` skill (whole document as ONE act-structured film), channel claude-liam (Kokoro `am_onyx`), no approval gates on free steps, stop at the master, never publish.
The film is made FOR the course, so `metadata.course` is set and the course is named once, in BIDEA. The acts follow the assignment's own order, including its instruction to learn Blender's window before writing the brief: I Three Simple Assets · II Learn the Window First · III Write the Brief Before You Build · IV Connect Claude to Blender · V Build the Assets · VI Export, Import, Check · VII Ship It, and How It's Graded. `ACTS.md` is the coverage map and lists what was left out and why.

## How it was built
- Narration and sheet by me (`narration.py`, `make_sheet.py`, 80 beats); one evidence agent produced the real runs (`evidence/`, `EVIDENCE-INDEX.md`); seven act-builders (one per act) wrote `scenes_actN.py`, `lanes/actN.json`, `factcheck/actN.md`; `assemble_scenes.py` pastes them with `kit.py` into `scenes.py`; `build_docs.py` writes SHOTLIST / FACTCHECK / CHECKS-REPORT.
- Every body beat auditioned two lanes; the pick and runner-up are in `SHOTLIST.md`. Tools are shown as themselves: the real Blender window (cropped, never shrunk), the real Godot output, the real Claude Code and terminal skins, the public GitHub README and the course's policy video page (captured without sign-in).

## Corrections made because the real runs disagreed with the text (all re-voiced, fact-check rows updated)
- **Origin in the middle:** the assignment and my first draft said it "floats". Real run: placed at floor level it sinks half its height (gap −0.4 m); lifted by a wrong guess it floats (+0.1 m); lifted by exactly half it sits, the floor-gap check passes it, and only an origin check catches it ("the origin is 0.4 m above the base"). B26A/B26B say this.
- **Installer:** the 2.1.9 README "finds the MCP clients on your machine … lets you pick which to set up"; it does not set up every client (B31; the assignment's wording is fixed too).
- **Version drift:** the next release after 2.1.1 came 3 days later, not 9; 2.1.9 is the seventh release after it, on 6 Oct (B30, B45).
- **Backups:** a factory Blender keeps one backup, `.blend1`, not "and so on" (B49).
- **"model" (Bear, after watching the first cut):** every spoken "model" meant a 3D model, so Liam now says "three-D model" throughout (8 beats re-voiced and retimed: BIDEA, BDEFS, B12, B13, B16, B25A, B26A, B44; on-screen "3D models" to match). Nothing refers to an AI model except the proper name "Model Context Protocol", which stays. The master was re-cut after this change; gates all PASS again.
- Wording that claimed the unrun route's behaviour as fact now says what the prompt asks Claude to do (B42, B43); "the newer add-on has no export tool" is now "the newer MCP version" (B52); B66 "earns the other eighty" is now "can earn" (the rubric's own word); B63 now says to push the tag; B14 and B62 no longer open a sentence with "Use" (Kokoro read it as the noun).

## Gates (2026-10-06)
Gate L · Gate A static · Gate W · layout audit · Gate F (276 claims, FACTCHECK.md) · Gate V first run MAJOR 4 (B25A low contrast; B38 and B39A underfill) → fixed → **0 / 0** · GATE T first run FAIL 6 (B12, B22, B25B, B61A, B61B, B62: image content read as low-contrast text; B25B's real Blender capture could not pass at any crop and became the isometric drawing) → fixed → **PASS** · bookend_check **PASS**. Master checks: 3840×2160, runtime = sum of audio + frame rounding, silent tail present. A SKIN LINT line says the BIDEA cold open is a hesitant writer, not a composer: advisory, and the `lecture` skill accepts that open.
Whisper pass over all 80 beats found no misreads that remain (digit/word and British/American spelling differences are normalisation only; small.en hears "Claude" as "cloud/clawed", which Kokoro does not say).

## Mistakes worth not repeating
- `art run` skips a beat as "already filled" if `manim/<BID>.mp4` exists: moving only `clips/` re-renders nothing. Move `manim/<BID>.mp4`, `clips/<BID>.mp4` and `media/videos/scenes/2160p24/partial_movie_files/<class>` into `_superseded/`, then re-run (the old files are in `_superseded/rerun1` and `rerun2`).
- GATE T reads any pixel within 48 RGB of ink as text: dark crate outlines, Blender's dark interface and Godot's floor shadow become "text blobs". Approximations at 1080p/2× upscale pass what the real 4K gate fails; render the class at 4K and run `type_check.py`'s functions on the 50% and 85% frames.
- Ink-coloured rings around text fail §8.6b (overlap); the builders used grey rings. A real capture with a dark interface landing at the 50% mark fails §8.3b/§8.6b: land it after the midpoint.
- Manim cache: a warm cache can add frames and push a clip past its audio; clear the stale partials before the final render.
- Preflight renders with `-s`, which under-reports pace on beats with many short plays; check with a real `-ql --fps 24` render and ffprobe.
- Kokoro: "A. I." not "AI"; sentence-initial "Use" is read as a noun; "bounding box" after "And" fuses.

## Open items for Bear (nothing is staged or published)
1. **Watch it.** Nobody has watched the master. Worth a listen: B60 (Whisper heard no opening "And").
2. **Run the MCP route once** (install, `claude mcp add`, the add-on, one prompt) before the assignment goes out; then the "documented, not run" labels can become real captures.
3. **B14** shows the policy video's own poster frame: a slide of a grading rubric ("Top 25% (20 points)") with the title ringed, captured 6 Oct. It is real, but it is a rubric slide from that video, not this assignment's.
4. **B41–B44 show the assignment's prompt verbatim**, including "Walker's Game brief → Build → Playtest → Revise → Export workflow", a course workflow the film never explains.
5. **Departures from plan:** B63 shows the tag but not the push (the example repo has no remote, so a push line would invent output); `git log --oneline --decorate` did not fit the terminal; B64 shows a `cd` step the recorded run did too; B68 holds its finished picture for the last ~2.9 s; B49 shows `ls -1` (the `ls -la` lines were too wide for the type floor); B25B is the drawn version, not the real capture.
6. **Left to the written assignment:** §4 item 4's "one next step" and "the source revision shown", "why your game needs each asset", the SUBMISSION.md fields line by line, the macOS `timeout` note (see `ACTS.md`).
7. **Publishing:** `art post` and the upload wait for your word; channel claude-liam (@NikBearBrown), playlist "Virtual Environments and Real-Time 3D". The film folder is untracked in the course repository and has not been committed or pushed.
