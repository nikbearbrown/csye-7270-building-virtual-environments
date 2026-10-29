# FACTCHECK — walker-magic Assignment 5 gamedev film

Every spoken claim and every on-screen figure, with its source. "A5" = `fall-2026/zhefan-z/assignment-5/`. Game files are read from a `git archive` of `40c42f5` (identical to the working tree for every excerpt shown; `media.py` asserts it). Checked by Claude Code against the files and the captures; the author has not yet reviewed the film.

## Discrepancies found while checking, and what the film does

| Where | Discrepancy | Film |
|---|---|---|
| FRICTIONAL.md line 33 | "every decision in CHANGE-BRIEF and its **four** revisions"; CHANGE-BRIEF.md has **three** dated revisions (2026-10-23 ×2, 2026-10-27) | says "its revisions", no count (B27) |
| captures/hurt_tint_pixels.json, grey 2.0 rows | the capture script's `mix_on_stored_values_if_not_clamped` uses 128 for grey 0.5 (8-bit rounding): (24, 26, 16), (198, 192, 96). TEST-REPORT.md predicts with 127.5: (23, 25, 15), (197, 191, 95) | shows TEST-REPORT.md's prediction and the JSON's measured `rgb8` (B08) |
| captures/hurt_tint_pixels.json `saved_tint_color` | "Color(1, 0, 0, 1)" (the material held red before F9), not unset | not shown; the captures' tint is red either way |

## Claims

| Beat | Claim | Source | Status |
|---|---|---|---|
| B00 | Two shaders for a cave game: a red flash on the mage after a hit, a frosted rock whose textures decide where frost goes | A5 README.md "What this assignment added"; CHANGE-BRIEF.md §2, §4 | ✓ |
| B00 | Each predicted first, then tested and captured in Godot | CHANGE-BRIEF.md (original 2026-10-22, before the shaders); TEST-REPORT.md | ✓ |
| B00 | On screen: canvas_item, driven by Player.invulnerable; spatial, two materials one shader; 17 / 0 at 30, 60, 144; 32 / 0 | hurt_tint.gdshader:1; hurt_tint_driver.gd; rock_frost.gdshader:1; TEST-REPORT.md lines 19, 27 | ✓ |
| B01 | Textures are information, not pictures; predicted first, then measured | the film's argument (prompt question 3); CHANGE-BRIEF.md §3–4; TEST-REPORT.md | ✓ (framing) |
| B02 | A pixel-art fire mage crossing a cold cave | A5 README.md line 3 | ✓ |
| B02 | Invulnerable for one second after a lunge lands; Player.invulnerable counting down from 1.0 | CHANGE-BRIEF.md §1 table (player.gd:155, :80, :152) | ✓ |
| B02 | The textured shader on the A3 rock, in material_compare.tscn, two copies side by side; Rock_Main surface 0 override, Rock_Top imported | CHANGE-BRIEF.md revision 2026-10-27 | ✓ |
| B03 | The answer specified before code: one colour line; mixes toward the tint by intensity, leaves alpha, transparent pixels stay transparent | CHANGE-BRIEF.md lines 44–50; original version 2026-10-22 (line 3) | ✓ |
| B04 | Line 7 inside fragment | hurt_tint.gdshader:6–7 | ✓ |
| B04 | A shader runs for every pixel the sprite covers | LANGUAGE-NOTES.md answer 2 | ✓ |
| B04 | COLOR arrives holding the texture's colour | CHANGE-BRIEF.md §6 (texture × vertex colour; shown in the notes) | ✓ |
| B05 | Driver off, intensity set from code | TEST-REPORT.md "Controlled values"; capture_hurt_tint.gd | ✓ |
| B05 | At 0 stored colours; at 1 pure red; at 0.5 four of six channels exact, two x.5 channels one lower, inside ±1 | TEST-REPORT.md table lines 43–50; CHANGE-BRIEF.md line 100 (±1); hurt_tint_pixels.json | ✓ |
| B06 | Line 15 hands one number to the material every frame | hurt_tint_driver.gd:10, :15 | ✓ |
| B06 | The shader holds the code and the default (0); the material the current value | CHANGE-BRIEF.md line 207; hurt_tint.gdshader:4 | ✓ |
| B07 | Real game loop, real wolf lunges, 30 / 60 / 144: 17 / 0 at each rate | TEST-REPORT.md line 19 | ✓ |
| B07 | First tinted value 0.9833 | TEST-REPORT.md line 20 | ✓ |
| B07 | Fail at HP 0 forces 0, invulnerable frozen at 1.0 | TEST-REPORT.md line 25 | ✓ |
| B07 | Headless proves the number, not the colour | TEST-REPORT.md line 8; test_hurt_tint.gd header | ✓ |
| B08 | Pure red couldn't show clamping; tint grey, intensity 2 | TEST-REPORT.md line 52; FRICTIONAL.md 9 | ✓ |
| B08 | Hair (23, 25, 15), hat (197, 191, 95) = unclamped prediction; clamped (128, 128, 128) | TEST-REPORT.md line 52; hurt_tint_pixels.json rgb8 | ✓ |
| B08 | The range only shapes the Inspector slider | LANGUAGE-NOTES.md answers 4, 5; CHANGE-BRIEF.md line 209 | ✓ |
| B09 | Frosted material: one shader reference, five values, three textures | mat_rock_frosted.tres:9–17 | ✓ |
| B09 | Dry differs in two values: base tint white vs (0.92, 0.95, 1), frost amount 0 vs 0.65 | CHANGE-BRIEF.md §4 "The two materials"; mat_rock_dry.tres:10, :14 | ✓ ("cold blue-white" describes (0.92, 0.95, 1); the brief: "a colder part of the cave") |
| B10 | Dry rock as the textures describe it; frosted at 0.65; frost where roughness is low | CHANGE-BRIEF.md §4 tables ("areas with low roughness frost first") | ✓ |
| B10 | Top stones keep their imported A3 material on both | CHANGE-BRIEF.md revision 2026-10-27; MATERIALS.md | ✓ |
| B11 | normal_scale 0 on dry only: only the left changes, 6031 pixels, none on the right | TEST-REPORT.md lines 94–95 | ✓ |
| B11 | Line 28 × 0.5: both rocks change (on screen 8225 / 8103) | TEST-REPORT.md line 96 | ✓ |
| B11 | On screen: means 67.9 / 84.0, 66.1 / 84.0, 54.7 / 73.7; edit reverted | TEST-REPORT.md lines 94–98 | ✓ |
| B12 | One PNG, three greys 64, 128, 192; two samplers, one source_color, one not; unshaded quads, Linear tonemap | CHANGE-BRIEF.md §3; hint_experiment.gdshader:2, 4–5; hint_experiment.tscn:10–14 | ✓ |
| B13 | With source_color the file's numbers (decode and encode cancel); without, brightened to 137, 188, 225; all six as predicted | TEST-REPORT.md lines 64–70; CHANGE-BRIEF.md §3; hint_pixels.json | ✓ |
| B14 | Line 16 albedo colour with source_color; 17 normal map data, no conversion; 18 roughness data, read as stored | rock_frost.gdshader:16–18; LANGUAGE-NOTES.md answers 4, 6; CHANGE-BRIEF.md §4 textures table | ✓ |
| B14 | On screen: import modes and formats | MATERIALS.md Samplers table; TEST-REPORT.md line 31 | ✓ |
| B15 | Curl check tells which way a normal map was written; bound map 0.1444 OpenGL, 1.8556 DirectX; OpenGL, which Godot expects | TEST-REPORT.md line 30; normal_map_check.gd:1–3; CHANGE-BRIEF.md §4 | ✓ |
| B15 | Delete source_color from line 16: material test fails, exit 1 | TEST-REPORT.md line 29 | ✓ |
| B16 | Line 35 compares roughness with a threshold that frost_amount slides from −0.1 to 1.1; below it frosts with a soft band | rock_frost.gdshader:31–35 (comments translated on screen) | ✓ |
| B17 | 0: matches the bare rock; 0.65: frost layer, no blocks at this size despite the DXT1 worry; 1: white crust, bad for readability | TEST-REPORT.md lines 82, 84, 86 | ✓ |
| B18 | Lines 4–12: five values in two groups — two colours, and three numbers each with a range | rock_frost.gdshader:4–12 (colours: source_color; numbers: hint_range) | ✓ (first draft said all five had a range; corrected before release) |
| B18 | Capture scene swept each on the frosted material: min, own value, max, restored after each | TEST-REPORT.md line 74; capture_rock_sweep.gd | ✓ |
| B19 | Observations for base_tint, normal_scale, roughness_scale, frost_color; no pink, no black holes | TEST-REPORT.md lines 78–84 | ✓ |
| B20 | Line 1 shader_type canvas_item; one word picks the pipeline (2D here, spatial for the rock) and which built-ins exist | hurt_tint.gdshader:1; rock_frost.gdshader:1; LANGUAGE-NOTES.md answer 1 | ✓ |
| B20 | Lines 3–4 use hints plain GLSL doesn't have | LANGUAGE-NOTES.md answer 8 | ✓ |
| B21 | canvas_item mixes colour directly; spatial writes albedo, roughness and a normal map, lit by one directional light | hurt_tint.gdshader:7; rock_frost.gdshader:38, 43, 46–47; LANGUAGE-NOTES.md answers 1, 3; MATERIALS.md Lights | ✓ |
| B22 | Converting a standard material gives the generated shader; line 7 ≈ line 16 plus repeat_enable; line 19 ≈ line 17 but hint_roughness_normal linking to the roughness texture | LANGUAGE-NOTES.md "The generated shader" | ✓ |
| B23 | Seven earlier suites 95 / 0 before and after, lines identical; hurt tint 17 at three rates; materials 32, again after deleting the cache; one wrapper failing on shader or script errors | TEST-REPORT.md lines 6, 14–15, 19, 27–28 | ✓ |
| B24 | Semicolon: shader error, exit 1; rename: no error, 15 passed, two caught it; source_color: material test fails; no headless run shows the look | TEST-REPORT.md lines 8, 17–18, 29, 111 ("only the uniform-list and source-default checks failed" = two) | ✓ |
| B25 | CLAUDE.md draft cited an uncommitted log, blink "every tick" (really 0.1 s) | FRICTIONAL.md 4 | ✓ |
| B25 | R7 at 144: offered to widen or drop; author refused, physics ticks | FRICTIONAL.md 6 | ✓ |
| B25 | Recommended letting an A3 test fail; author moved the material into scene overrides | FRICTIONAL.md 8 | ✓ |
| B26 | Two untested explanations; ice roughness a constant | FRICTIONAL.md "Still open"; README.md Known limitations | ✓ |
| B26 | One next step: test the rounding with more x.5 controlled values | proposed by this film (labelled so on screen) | judgment |
| B27 | Contributions of the author, Claude Code, claude.ai | FRICTIONAL.md "Human and AI contributions" | ✓ |
| B27 | Rock 01, Poly Haven, Rob Tuytel, CC0 | SOURCES.md line 13 | ✓ |
| B28 | Built / measured / judged / unknown; source 40c42f5 | TEST-REPORT.md; FRICTIONAL.md; TEST-REPORT.md line 3 | ✓ |
| B29 | ice_roughness as a uniform: one bounded change with a prediction and a check | README.md Known limitations (the constant) | suggestion |
