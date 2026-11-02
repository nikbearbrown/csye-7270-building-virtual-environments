# Fact check — claude-liam-walker-survival-shooting-a5-gamedev

Every claim in the narration, with its source in the submitted files (course repository, `fall-2026/zhe-l/assignment-5/`, at a84cfa23) or in this film's own capture records (`CAPTURE.md`). Game source shown: 2d558bba (no game file changed after it).

| Beat | Claim | Source |
|---|---|---|
| B00 | Reconstructed prompt, not a saved session | This film (label on screen) |
| B00 | Two shaders by hand, two materials, tests | FRICTIONAL.md (A5 entries); TEST-REPORT sections 1–9 |
| B01 | The user wrote both shaders; Claude checked each step | FRICTIONAL.md, "What I did" / "What Claude contributed" |
| B02 | State = tablet in use; screen glows once the tablet reaches the hand | CHANGE-BRIEF part 1 |
| B02 | Textured shader on the two weapon crates | CHANGE-BRIEF part 3 revision |
| B03 | fragment() runs per pixel in parallel; each run has its own locals, cannot see neighbours; state arrives as a uniform set from GDScript | LANGUAGE-NOTES questions 2 and 7 |
| B03 | Line 6 is the colour line of the specification | CHANGE-BRIEF part 1 (colour line) |
| B04 | 0.39 → (151, 162, 162), hand-computed, difference 0; 2.0 → white; hint_range does not clamp code | TEST-REPORT section 4; LANGUAGE-NOTES question 5 |
| B05 | Driver written by the user; off when put away, on when arrived, otherwise keep | FRICTIONAL.md; humanoid.gd lines 137–142 |
| B06 | Dark while moving, lit on arrival, no flicker, dark on put-away, out-and-back never lit | CAPTURE.md (tablet-run-02, 10 PASS) |
| B07 | set_screen_lit() written by Claude at the user's request; 0.39 from an @export; Local To Scene | FRICTIONAL.md; tablet_device.gd lines 39–48; CHANGE-BRIEF part 1 |
| B08 | Lit after 0.3667 / 0.35 / 0.35 s; second body 0.0 on every frame; 24 PASS each | logs/screen_glow_check_{30,60,144}fps_final.log; TEST-REPORT section 3 |
| B09 | Defaults in the shader, current values in the ShaderMaterial; shared material shares values | CHANGE-BRIEF short answers (the user's own answer; LANGUAGE-NOTES has no separate question) |
| B09 | crate_long_wear.tres stores only roughness 0.95 and wear 0.2 | crate_long_wear.tres lines 12–13; MATERIALS.md section 1 |
| B10 | Long crate more worn and duller because it is dragged more; same textures and scale | CHANGE-BRIEF part 3 revision (two materials) |
| B11 | wear_mask is height data (no source_color); low places rust first; rust_albedo is the colour | LANGUAGE-NOTES question 6; CHANGE-BRIEF part 3 revision |
| B12 | 0 → no rust, 0.1 → about a tenth (9.8 % on the mask), 1 → all rust | CAPTURE.md (crate sweep); FRICTIONAL.md (9.8 %) |
| B13 | crate_long has no UVs; 336 normals on the axes; box projection proposed by Claude; object space; no normal map on the crates | FRICTIONAL.md; CHANGE-BRIEF part 3 revision |
| B14 | texture_scale = repeats per metre; default 2 ≈ 12–16 cm patches | CHANGE-BRIEF part 3 revision (uniform table) |
| B15 | group_uniforms and hints give an Inspector panel; ALBEDO/ROUGHNESS outputs finished by Godot's lighting | LANGUAGE-NOTES question 8 |
| B16 | What changed at each value (no judgement of the look) | CAPTURE.md (crate and crate-glint sweeps); TEST-REPORT section 9 |
| B17 | One 3x1 PNG, line 4 with source_color, line 5 without; predicted by hand | CHANGE-BRIEF part 2 revision; FRICTIONAL.md |
| B18 | 64/128/192 and 137/188/225 measured, difference 0 | CAPTURE.md (hint); TEST-REPORT section 9; LANGUAGE-NOTES question 4 |
| B19 | Godot generated the shader; the user annotated it; line 13 ↔ crate line 3 | LANGUAGE-NOTES question 6; commits 22dc162d, 4473d512 |
| B20 | Without source_color the rust is paler (film-only mutated copy) | CAPTURE.md (mutation); CHANGE-BRIEF failure case 8. The film does **not** claim the shader-edit check (both crates change), which was not done (TEST-REPORT, README) |
| B21 | Line 42 ↔ crate line 4; not hint_roughness_normal that keeps the data | LANGUAGE-NOTES question 6 |
| B22 | Curl ratios 0.1991 / 1.8009 both ways; no flip | TEST-REPORT section 7; logs/normal_map_check_60fps_final.log |
| B23 | Hint check reads source text; written in the audit | tests/test_materials.gd lines 206–223; TEST-REPORT section 6 |
| B24 | source_color mutation 1 FAIL exit 1; semicolon 3 FAIL with SHADER ERROR; rename 3 FAIL without error | TEST-REPORT section 2; logs/mutation_*.log |
| B25 | Headless cannot show the look; METALLIC never written | TEST-REPORT section 6; MATERIALS.md |
| B26 | Test bugs, misnamed import option, a setting cited that is not in the file, a comparison of two runs | FRICTIONAL.md; TEST-REPORT sections 4 and 6 |
| B26 | Textures: ambientCG Metal041C, CC0 | godot/assets/shader/metal041c/ATTRIBUTION.md; SOURCES.md |
| B26 | Uncertain (three items) and next step | Chosen by the user on 2026-11-01 (next step: CLAUDE.md rule 7 plan) |
| B27 | Your Turn experiment | Draft by Claude, shown to the user |
| B28 | Title | Chosen by the user: the slug, as is |
