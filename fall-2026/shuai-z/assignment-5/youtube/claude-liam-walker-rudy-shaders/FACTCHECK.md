# FACTCHECK — Two Shaders for Walker Rudy.

Every number and factual claim spoken or shown in the film, with its source. Claude drafted this file while building the film. Paths are relative to `fall-2026/shuai-z/assignment-5/` unless they start with `capture/`, `stills/` or `tools/` (this reel).

| Beat | Claim | Source |
| --- | --- | --- |
| B00 | revision `a2a3a77`; Godot 4.7.2; `game/` GL Compatibility, `godot/` Forward+ | `git rev-parse HEAD`; `logs/game_checks_60fps.log` line 1; `game/project.godot` lines 95–96; `godot/project.godot` line 16 (CLAUDE.md) |
| B00 | every shader line by shuai-z; brief, driver, tests and captures by Claude Code, reviewed by shuai-z | SOURCES.md, Human / AI contributions; CLAUDE.md, Ownership; commits `ae0a3757`, `a87a18be`, `9481663a` |
| B01 | Claude drafted the brief, the driver and the tests; shuai-z typed every shader line | SOURCES.md table rows "CHANGE-BRIEF.md", "The driver and its test", "The materials audit", and the three shader rows. The driver and its test were written by the scoped `claude -p` sessions that Claude ran |
| B02 | Godot 4.7, Compatibility; invulnerable for 1.2 s after a hit or a respawn; hits ignored | `game/content/rudy/rudy.gd` lines 75, 112–113, 129–130, 144, 188 (CLAUDE.md) |
| B02 | the tint colour is the waystone's glow | `game/content/level_1/waystone.gd` line 19 `GLOW := Color(0.6, 0.88, 1.0)`; `invulnerable_tint.gdshader` line 4 |
| B02 | the textured shader is on the waystone's Stone and the circle's DarkStone, Forward Plus | `godot/scenes/props_room.tscn` surface overrides (CLAUDE.md); `godot/project.godot` line 16 |
| B03 | the four lines named | `invulnerable_tint.gdshader:8`, `circle_darkstone.tres:9`, `weathered_stone.gdshader:4` and `:7`, read by `tools/make_stills.py` |
| B04 | the brief came before either shader | brief `fc9cd523` (2026-10-24 22:11 EDT); first shader `ae0a3757` (2026-10-27 16:18 EDT) |
| B04 | the colour line and the uniform table | CHANGE-BRIEF.md §2, read and asserted by `tools/make_stills.py` |
| B04 | strength 0.4: at 0.6 the outline falls to 2.1:1; at 0.4 it is 3.5:1; rule 9 asks for 3:1 | CHANGE-BRIEF.md §2 uniform table (`tint_strength` row) and §3 contrast (3.51:1) |
| B04 | 1.183 s ± one frame at 30, 60 and 144 fps | CHANGE-BRIEF.md §2 rule 4 |
| B04 | Claude drafted it; shuai-z reviewed it | CHANGE-BRIEF.md header |
| B05 | nine lines; `canvas_item`; three uniforms; line 8; `.rgb` only | `game/shaders/invulnerable_tint.gdshader`, excerpted verbatim (lines 1–9) |
| B05 | `COLOR` arrives as the texel times the vertex colour, which carries `modulate` | CHANGE-BRIEF.md §7 short answer 2, quoting Godot's canvas_item reference; LANGUAGE-NOTES.md question 2 |
| B05 | the shader runs per fragment, not exactly per screen pixel | LANGUAGE-NOTES.md question 2. The narration's "once for each fragment of the hearts" follows it |
| B06 | the capture stopped the driver and set `tint_amount` from code to 0, 0.5, 1 and 2 | `game/tests/capture_tint.gd` lines 55–62; TEST-REPORT.md §4 |
| B06 | P1 (200, 64, 53) at 0.0 and (181, 128, 134) at 1.0, as predicted; 0.5 matches | `logs/capture_tint.log`: `#C84035`, `#B58086`, `#BF605D`, each "off by 0"; CHANGE-BRIEF.md §3 |
| B06 | P3, inside the empty heart, stays the sky at every value | `logs/capture_tint.log`: `#C8C6CB` at every value |
| B06 | at 2.0 P1 is one step from the unclamped prediction, 81 from the clamped one; `hint_range` does not clamp | `logs/capture_tint.log` line for tint 2.0 P1; TEST-REPORT.md §4 |
| B07 | one line, every frame; reads `_invulnerable_left / invulnerable_time`; never writes Rudy's state | `game/ui/hud.gd` lines 89–92 and 108–111 (excerpt 108–111); TEST-REPORT.md §3 (the test assigns none of Rudy's state); CHANGE-BRIEF.md Boundaries |
| B07 | the shader holds the default 0; the material holds the current value and is local to the scene | `invulnerable_tint.gdshader` line 3; `game/ui/hearts_tint.tres` line 6 `resource_local_to_scene = true`; CHANGE-BRIEF.md short answer 6 |
| B07 | written by the scoped `claude -p` session, `bd797945` | SOURCES.md; `sessions/README.md` |
| B08 | the real game at 4K by Movie Maker, scripted input from a film-only driver on a copy | CAPTURE.md §1 |
| B08 | a heart empties, the full hearts pale toward blue and fade back; back onto the spikes, nothing; two more hits; the respawn restarts the tint | `capture/play-01-run.log` (hearts 3 → 2 at 131; no rise on the spikes; 0.0 from 167; hearts 1 at 223; 0 at 308; 3 and 0.972222 at 343); the inset frames |
| B08 | after Enter the hearts still fade in | the capture's frames 45–90 (the hearts' `modulate.a` tween, `hud.gd` line 62); shuai-z's own check, TEST-REPORT.md §4 |
| B09 | the window opens at 0.986 and falls with game time; no heart lost and no jump on the spikes | `capture/play-01-run.log` frames 131–167; the test's A6, A7 and A10 at 30 fps (`logs/game_invulnerable_tint_checks_30fps.log`) |
| B09 | the last heart's window is still running when he gets back up; the value jumps from 0.04 to 0.97 | `capture/play-01-run.log` frames 342–343 (0.041667 → 0.972222); CHANGE-BRIEF.md rule 5 |
| B10 | Rock 01, Poly Haven, Rob Tuytel, CC0 | `godot/assets/textures/rock_01/ATTRIBUTION.md`; SOURCES.md, Textures |
| B10 | normal map: directions in red and green; roughness: how sharp a reflection is | CHANGE-BRIEF.md §5 texture table |
| B10 | every import setting set explicitly | CHANGE-BRIEF.md §5 "Why the last column"; TEST-REPORT.md §11 (no `.import` rewritten after five editor sessions) |
| B10 | curl ratios 0.1444 and 1.8556 | `logs/godot_calibrate_normal_map_check_60fps.log`; TEST-REPORT.md §10 |
| B11 | samplers' hints at lines 3–5; `group_uniforms` at 7 and 11; `hint_range` with a step at line 9 | `godot/shaders/weathered_stone.gdshader`, excerpted verbatim (lines 3–13) |
| B11 | plain GLSL has neither the groups nor the slider metadata | LANGUAGE-NOTES.md question 8 |
| B12 | Claude did the sweep at shuai-z's request; shuai-z reviewed it | TEST-REPORT.md §7 |
| B12 | albedo_tint black removes the colour; uv_scale breaks at both ends; normal_strength and roughness_offset under three steps on average | `logs/capture_sweep.log` close-up means: 73.51; 12.51 and 9.20; 2.62, 2.93, 2.64, 0.90; TEST-REPORT.md §7 judgement |
| B12 | the normal map is gentle, the roughness map nearly flat, the Sun's highlight cannot land on the sides | TEST-REPORT.md §7, "Why normal_strength and roughness_offset barely show" (7.7° mean tilt; roughness mean 0.516; Sun 50.2° up) |
| B13 | four outputs; `clamp(…, 0.0, 1.0)`; one scaled UV | `weathered_stone.gdshader` lines 16–22, excerpted verbatim |
| B13 | the upper-case outputs are Godot's, wired into its lighting | LANGUAGE-NOTES.md question 8 |
| B14 | the real props scene, Forward Plus, 4K; only the camera moves; props, light and materials as saved | CAPTURE.md §2 |
| B14 | rune, moss, spikes and gold keep their flat imported colours | CLAUDE.md (overrides on Stone and DarkStone only; the other surfaces keep imported materials, `logs/probe_overrides.log`) |
| B14 | the disc's material: darker, flatter in relief, glossier, three values | `circle_darkstone.tres` lines 13, 15, 16 against `waystone_stone.tres`; CHANGE-BRIEF.md §5 "Why they differ". "Glossier" is the material's intent (roughness_offset −0.25); B12 says why it barely shows under this light |
| B15 | the strip is 64, 128, 192; two samplers on one file; only one `source_color`; `unshaded`; a bool picks | `godot/shaders/hint_experiment.gdshader` lines 2–13 (verbatim); CHANGE-BRIEF.md §4 |
| B15 | predicted 137, 188, 225 without the hint | CHANGE-BRIEF.md §4 table |
| B15 | Claude's script computed the predictions; shuai-z rechecked the left band by hand | CHANGE-BRIEF.md header; TEST-REPORT.md §4, "By hand, after the captures" |
| B16 | six bands exactly as predicted, each flat over 9 × 9 | `logs/capture_hint.log` lines 7–12 |
| B17 | the circle's material names the same shader and textures; `#A4A7B4`, 0.35, −0.25 | `godot/materials/circle_darkstone.tres` lines 8–16 (verbatim); `Color(0.6431373, 0.654902, 0.7058824, 1)` is `#A4A7B4`; CHANGE-BRIEF.md revision 2 |
| B18 | one shader object; line 18 halved darkens both by 22.54 and 10.52 steps; tint to white moves the circle 19.97 and the waystone 0.00; normal_strength 2.0 moved it 0.76, so the check was revised | `logs/capture_sweep.log` (`SHARED … true`, the three `CHANGE` lines); TEST-REPORT.md §§8, 13 |
| B18 | in memory, never saved | TEST-REPORT.md §8 (`git status` clean; the shader file never edited) |
| B19 | shuai-z converted a StandardMaterial3D with the same textures in the editor and annotated it | LANGUAGE-NOTES.md §A; SOURCES.md generated-shader row; commit `fe795908` |
| B19 | the two pairs of lines; `hint_roughness_normal` against `hint_normal` | `standard_generated.gdshader` 10–11, 69–72 and `weathered_stone.gdshader` 3–4, 19–20, read by `tools/make_stills.py`; LANGUAGE-NOTES.md question 6 |
| B19 | 16 uniforms against 7 | `logs/probe_standard_generated.log` line 6; `weathered_stone.gdshader` declares 3 samplers and 4 values |
| B20 | real input; one sample a frame; 71/60 s ± one frame and 144/60 = 2.4 s at half speed; the test never calls `take_hit()` or sets the parameter | `game/tests/invulnerable_tint_checks.gd` lines 347–354 (verbatim) and its header; TEST-REPORT.md §3 |
| B21 | 1.2000, 1.1833, 1.1806 s; 15 of 15 at each rate | `logs/game_invulnerable_tint_checks_{30,60,144}fps.log` (A9 lines; 15 `PASS`) |
| B21 | a frame-counting HUD failed A9 at 30 and 144 | TEST-REPORT.md §3, "The frame rate matters to this test" |
| B22 | the three mutations, made by shuai-z, each exit 1; which checks failed | `logs/game_invulnerable_tint_checks_60fps_no_semicolon.log`, `_renamed.log`, `logs/godot_test_materials_60fps_no_source_color.log`; TEST-REPORT.md §2 table (exit codes are the wrapper's) |
| B22 | 125 of 125 after a fresh import | TEST-REPORT.md §9; `logs/godot_test_materials_60fps.log` |
| B23 | headless draws nothing | `logs/probe_headless.log`; CLAUDE.md, Headless facts |
| B23 | the OS screenshot is 4 to 11 steps darker; converted to sRGB it matches | `logs/capture_hint_vs_os.log` (64→56 … 225→221); TEST-REPORT.md §12 |
| B23 | shuai-z played the game, watched the fade-in and checked the materials in the editor | TEST-REPORT.md §§4–6; SOURCES.md, People |
| BVD1 | 141/141, 44/44; 15/15 at three rates; 125/125 after a fresh import; three mutations exit 1 | TEST-REPORT.md Summary and §§1–3, 9 |
| BVD1 | windowed captures exact at 0.0, 0.5, 1.0 and all six bands; the playtest and its three edge cases | TEST-REPORT.md §§4–6 |
| BVD1 | uncertain: the sRGB step unconfirmed; one edge pixel one step off, unexplained; two controls below sight; macOS M3 only; nobody else played | CLAUDE.md, Unconfirmed; TEST-REPORT.md §4 (pixel (51, 67)), §7, §14; SOURCES.md, People |
| BVD1 | mistakes caught: the probe's own marker; relative permission rules re-anchored by a `cd`; Rock 01 copied to the wrong folder; "about 3 MB", really 1,908,496 bytes | FRICTIONAL.md entries of 2026-10-27: "The shader from code", "the first implementation run was refused", "Rock 01's textures", "The materials audit and its review" |
| BVD2 | who made what | SOURCES.md, People and Human / AI contributions |
| BVD2 | the circle's tint `#A4A7B4` and the curl threshold 0.5 were shuai-z's choices | CHANGE-BRIEF.md revision 2; TEST-REPORT.md §10 |
| BVD2 | Rock 01 by Rob Tuytel, CC0; the grey strip written by code | SOURCES.md, Textures |
| BVD2 | the next step, a grazing-light test scene | Claude's suggestion, from TEST-REPORT.md §7's finding that the scene's Sun cannot put a highlight on the sides; not yet discussed with shuai-z |
| BHTF | rule 9's 3:1; `hearts_tint.tres` stores no `tint_strength`, so setting it there overrides the shader's default for the hearts only | CHANGE-BRIEF.md §2; `game/ui/hearts_tint.tres`; the brief says 0.6 gives about 2.1:1 |
