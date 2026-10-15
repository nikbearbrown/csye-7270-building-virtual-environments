# FACTCHECK — Three Props for Walker Rudy.

Every number and factual claim spoken or shown in the film, with its source. Paths are relative to `fall-2026/shuai-z/assignment-3/` unless they start with `youtube/…` (this reel) or `assignment-2/`.

| Beat | Claim | Source |
| --- | --- | --- |
| B00 | Blender 5.2.2, MCP for Blender 2.1.9, Godot 4.7.2; source `f6f8acf` | README.md; TEST-REPORT.md header; `git rev-parse HEAD` = `f6f8acf09b1c…` at render, and the last commit touching `godot/` |
| B00 | 82 to 280 triangles each | TEST-REPORT.md *Triangle count*; `capture/checks-pass.log` (118, 280, 82) |
| B00 | brief/approvals/hand edit: shuai-z; Blender calls and Godot scripts: Claude Code | SOURCES.md human/AI table; FRICTIONAL.md |
| B01 | no model generated a mesh; basic shapes only | SOURCES.md (no downloaded models, no AI-generated meshes); tools/blender/*.py use only `primitive_cube/cone/cylinder_add` |
| B02 | spikes cost a heart; the waystone is where he gets back up; the circle ends Level 1 | CHANGE-BRIEF.md rev. 1 "In the game" lines |
| B02 | Rudy 160 px = 1.2 m; every size from the 2D pixels | CHANGE-BRIEF.md *Scale*; `assignment-2/game/content/rudy/frames/frames.json` `anchor_height_game_px: 160` |
| B02 | the figure draws each file at 1/density | `assignment-2/game/content/level_1/art/props.json` and `frames.json`: density 2 for all four; `tools/make_stills.py` `game_props()` |
| B03 | brief committed before building; six predicted failures | CHANGE-BRIEF.md rev. 1 header and table; commit `be59ab7` precedes the first build commit `a5f3c45` |
| B03 | sizes, origin, budgets on the card | CHANGE-BRIEF.md rev. 1–2 |
| B04 | shuai-z's own screenshots; Blender 5.2; port 9876; libraries and generators off | BLENDER-NOTES.md; evidence/mcp-setup-log.md ("Connected on port 9876", add-on 1.8); the screenshot itself shows the checkboxes off |
| B05 | the prompt text and time (20:14 EDT) | Claude Code session transcript, 2026-10-14T00:14:58Z |
| B05 | 8-sided cylinder, 22 cm across (radius 0.11), 2 cm deep, at the hand-chosen height | tools/blender/build_waystone.py lines 301–311 (`vertices=8, radius=0.11, depth=0.02`, `Z_CENTRE = 0.4537`) |
| B05 | every call kept in order in tools/ | tools/blender/build_waystone.py header |
| B06 | image is the MCP look tool's, captured by Claude at 20:15 EDT | `blender-looks/4-trial-ring-8.png`, extracted from the session transcript by `tools/extract_looks.py` (tool result at 2026-10-14T00:15:32Z) |
| B06 | a torus is not a basic shape, so two cylinders | CHANGE-BRIEF.md rev. 2 |
| B07 | moved 3.4 cm up, Z 0.42 → 0.4537; X, Y, size unchanged | FRICTIONAL.md (Claude's read-back); re-read for this film from a copy of evidence/waystone-after-hand-edit.blend: `Waystone_Rune (0.0, -0.185, 0.4537)` size 0.2 × 0.02 × 0.3 |
| B07 | G then Z then drag; keys are a sequence, not a chord | FRICTIONAL.md "What it taught me about the interface" |
| B07 | no recording of the edit; comparison stills | FRICTIONAL.md; the user chose option (b) on 2026-10-13. Before: `blender-looks/1-built-rectangle.png` (look result at 2026-10-13T23:58:02Z = 19:58 EDT). After: `blender-looks/2-after-hand-edit.png`, captured by Claude at 22:26:56 EDT on 2026-10-13 through the same look call (angles, front/right/top/three_quarter, material, 768 px) after opening a byte-identical copy (SHA-256 `68079e9d…`) of the saved file; the user's open `spikes.blend` was reopened afterwards and not saved |
| B08 | 42 → 82 (R) → 86 (8-sided ring) → 118 triangles; budget 60 → 130 in revision 2 | TEST-REPORT.md *Inspect and revise*; CHANGE-BRIEF.md rev. 2 |
| B09 | Claude found the shared undersides while planning; revision 3 lifted two discs | TEST-REPORT.md *What Claude got wrong* 1; CHANGE-BRIEF.md rev. 3 |
| B09 | 280 / 300; five 8-sided cones; 82 / 100 | CHANGE-BRIEF.md; `capture/checks-pass.log` |
| B10 | exported as glb with +Y Up | tools/blender/export_glb.py; TEST-REPORT.md *Upright and scale* |
| B10 | the table has a name, file, X and no height; Y = 0 | godot/tools/build_props_room.gd lines 10–18 and 58 |
| B10 | a 1.2 m post | build_props_room.gd line 18 and 61–75 |
| B11 | rendered at 4K; one orbit; post, spikes below its middle, circle almost twice as wide as he is tall; plain back; shadows from bases | `capture/orbit-01.mp4` (691 frames, 3840×2160) and `capture/orbit-01-run.log`; the circle is 2.25 m against the 1.2 m post; the spikes 0.47 m |
| B12 | within five millimetres | check_props.gd line 16, `TOL := 0.005` |
| B13 | 0.70 × 0.40 × 0.84 to four decimals; heights on Y; origins at zero; budgets | `capture/checks-pass.log`, identical apart from the header line to evidence/check_props-2026-10-13.txt |
| B13 | forty-four checks, zero failed | `capture/checks-pass.log`: 44 lines beginning `ok`, `PASS: 0 failed check(s)`, exit 0. **Correction:** TEST-REPORT.md and FRICTIONAL.md said "46 checks"; the log has 44, and both now say 44 |
| B13 | a parse error still exited 0 | TEST-REPORT.md *How to run the checks*; *What Claude got wrong* 2 |
| B14 | floor's top from the floor mesh; Module 3's agent check measured its own collider | check_props.gd lines 95–97; the assignment text ("an agent's floor check stopped on the object's own collider") |
| B15 | raised 30 cm on an isolated copy; FAIL; exit 1; project scene untouched | `capture/fail-diagnostic.diff`, `capture/checks-fail-diagnostic.log`; `git status` clean for `godot/` after the run |
| BVD1 | human check: sizes suit the post; spikes closest, circle furthest (no rune pattern, light or glow); behind and below fine; gold brighter in Godot | TEST-REPORT.md *Human check: look* (shuai-z's words, translated) |
| BVD1 | no second viewer; macOS only; scene separate from the game | TEST-REPORT.md *Known limitations* and "No other person has looked at the scene" |
| BVD1 | the three things Claude got wrong | TEST-REPORT.md *What Claude got wrong* |
| BVD2 | who made what | SOURCES.md human/AI table; FRICTIONAL.md "Human / AI" lines |
| BVD2 | next step: the circle's rune pattern, light and glow | TEST-REPORT.md and README.md *Known limitations* (shuai-z's judgement) |
| BHTF | the suggested prompt | PROMPTS.md (a suggestion for the viewer; not run for this film) |

## Corrections found while making the film

- **TEST-REPORT.md and FRICTIONAL.md said the check run had 46 checks; the log has 44** (12 + 12 + 11 for the three props, 9 for the scene). The film says forty-four. At shuai-z's request, TEST-REPORT.md and FRICTIONAL.md were corrected to 44 in the commit that adds this film.
