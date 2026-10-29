# SCRIPT — walker-magic Assignment 5 gamedev film (Brutalist `godot-gamedev` + `walker`)

> Narrator: Liam, in for Bear (local Kokoro `am_onyx`). Native 4K landscape, 30 fps. No burned captions. The final card is silent (this toolkit copy has no stock jingle, as in Assignments 2 and 3).
> Narration lines are written for the voice: numbers, file names and the commit are spelled the way they should be spoken. On-screen text keeps the exact spelling and the exact figures of the source named on each card.
> Sources of truth, in order: CHANGE-BRIEF.md (with its revisions), TEST-REPORT.md, LANGUAGE-NOTES.md, walker-magic-zhefan/MATERIALS.md, FRICTIONAL.md, SOURCES.md, the three shaders, features/player/hurt_tint_driver.gd, and the PNGs and JSON in captures/. FACTCHECK.md maps every sentence.

Title: **A Red Flash, a Frosted Rock: Two Shaders for a Cave Mage**

Labels used on screen: **Reconstructed prompt** · **Suggested prompt** · **In-engine capture · scripted** (an F9–F12 capture scene set the values; the author pressed the key) · **Enlarged ×N, nearest neighbour, from the same capture** · **Document view — reconstruction of the text, not a screenshot** · **Godot editor reconstruction** (with path and lines) · **Source view — reconstruction, not a screenshot** · **Headless test results, as recorded in TEST-REPORT.md — not a render**.

## B00 — Walker opening (Claude composer)
*On screen:* `ClaudeComposerAsk`, greeting "Hello, Liam". Prompt: "Please use Walker to convert my game design document about a fire mage in a cold cave into two shaders: a red hurt tint while she is invulnerable after a hit, and a frosted rock whose textures decide where the frost goes — each predicted first, then tested headlessly and captured in the engine." — **Reconstructed prompt**. Output lines: `hurt_tint.gdshader · canvas_item · driven by Player.invulnerable`; `rock_frost.gdshader · spatial · two materials, one shader`; `test_hurt_tint.gd · 17 checks / 0 failures at 30, 60 and 144 fps`; `test_materials.gd · 32 checks / 0 failures`.
*Narration:* "Hello — this is Liam, in for Bear. The ask: two shaders for a cave game. A red flash on the mage after a hit, and a frosted rock whose textures decide where the frost goes — each one predicted first, then tested and captured in Godot."

## B01 — Hesitant-writer summary (window ≥ 9 s)
*On screen:* typed in four lines, "One shader turns / the mage red; / one frosts a rock. / Textures are pictures." Correction (one word): "pictures" → "information".
*Narration:* "One shader turns the mage red; one frosts a rock. And the textures behind them are information, not pictures. Every claim in this film was predicted on paper first, then measured in the engine."

## B02 — The game, the state, the object
*On screen:* card: two in-engine captures (the mage at the start of the level; the two rocks in material_compare.tscn), with the state (`Player.invulnerable`) and the object (the rock, `Rock_Main` surface override) from CHANGE-BRIEF.md and its 2026-10-27 revision; game source revision 40c42f5.
*Narration:* "The game is walker magic: a pixel-art fire mage crossing a cold cave. When a wolf's lunge lands, she's invulnerable for one second — Player dot invulnerable, counting down from one. The textured shader goes on the rock from Assignment 3, in a new scene called material compare, where two copies stand side by side. Four questions follow, each answered at a line of the author's code."

## B03 — The colour line, specified first
*On screen:* **Document view** · `CHANGE-BRIEF.md` lines 38–52: the two declarations, the colour line (line 47, highlighted) and the driver mapping (line 52).
*Narration:* "Question one: what does a shader do? The author answered in the brief before writing any code: one colour line. Mix the sprite's colour toward the tint by intensity, and leave alpha alone, so transparent pixels stay transparent."

## B04 — The shader (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `shaders/hurt_tint.gdshader` lines 1–7; cues on line 6 (`fragment()`) and line 7 (the colour line).
*Narration:* "In the shader it's line seven, inside fragment. A shader is a small program the GPU runs for every pixel the sprite covers. COLOR arrives holding the texture's colour; this line mixes it toward red by intensity, and writes it back."

## B05 — Controlled values (result)
*On screen:* **In-engine capture · scripted** — `captures/hurt_tint_i0.0.png`, `hurt_tint_i0.5.png`, `hurt_tint_i1.0.png`, the mage enlarged, the two sampled pixels marked; beside them the predicted and measured table from TEST-REPORT.md.
*Narration:* "Here's that line on screen, with the driver switched off and intensity set from code. At zero, hair and hat keep their stored colours. At one, both are pure red. At one half, four of the six channels match the prediction exactly; the two that land on point five came out one step lower — inside the plus-or-minus one the brief allowed."

## B06 — The driver (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/player/hurt_tint_driver.gd` lines 6–15; cues on line 13 (failing or cleared) and line 15 (`set_shader_parameter`). Notes: CHANGE-BRIEF.md line 207 (which resource holds the default and the current value).
*Narration:* "Question two: how is a material different from a shader? Line fifteen of the driver answers it. Every frame, it hands one number to the sprite's material — not to the shader. The shader holds the code and the default, zero. The material holds the current value."

## B07 — The driver in the game loop (result)
*On screen:* **Headless test results, as recorded in TEST-REPORT.md — not a render**: 17 checks / 0 failures at 30, 60 and 144 fps; R1 0.9833; R4 durations; R7 ticks; R8 a fail at HP 0.
*Narration:* "The driver ran in the real game loop, with real wolf lunges, at thirty, sixty and one hundred forty-four frames a second: seventeen checks, zero failures, at each rate. The first tinted value was zero point nine eight three three. A fail at zero HP forces it to zero, even with invulnerable frozen at one. Headless, this proves the number, not the colour."

## B08 — A value from code, past the slider
*On screen:* **In-engine capture · scripted** — `captures/hurt_tint_grey_i2.0.png`, the mage enlarged; the prediction table from TEST-REPORT.md (not clamped / clamped / measured).
*Narration:* "A value set from code skips the Inspector. Pure red couldn't show whether hint range clamps, so the tint was set to grey and intensity to two. Hair: twenty-three, twenty-five, fifteen. Hat: one ninety-seven, one ninety-one, ninety-five — exactly the unclamped prediction. Clamped, both would have been one twenty-eight grey. The range only shapes the Inspector's slider."

## B09 — Two materials, one shader (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `assets/materials/mat_rock_frosted.tres` lines 8–17; cues on lines 9, 10 and 14. Notes: the dry material's lines 10 and 14.
*Narration:* "The same split, in 3D. This is the frosted material: one shader reference, five values, three textures. The dry material is the same file with two values changed — base tint white instead of a cold blue-white, and frost amount zero instead of zero point six five."

## B10 — The two rocks (result)
*On screen:* **In-engine capture · scripted** — `captures/rock_compare_default.png`, enlarged, labelled by material.
*Narration:* "One shader, two materials, two rocks. On the left, the dry rock, as the textures describe it. On the right, the same shader with frost amount at zero point six five: a pale frost where the roughness map is low. The small top stones keep their imported Assignment 3 material on both."

## B11 — Change a material, then the shader
*On screen:* **In-engine capture · scripted** — `captures/rock_one_material_changed.png` and `captures/rock_compare_after_shader_edit.png` beside `rock_compare_default.png`, with the measurements from TEST-REPORT.md.
*Narration:* "Change one value in one material — normal scale zero, on the dry one only — and only the left rock changes: six thousand thirty-one pixels, none on the right. Edit one line of the shader — line twenty-eight, times one half — and both rocks change. Values live in the material; the code lives in the shader."

## B12 — The hint experiment (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `shaders/hint_experiment.gdshader` lines 1–14; cues on lines 4, 5 and 7. Notes: `greys_3x1.png` texels; the scene's environment (MATERIALS.md).
*Narration:* "Question three: why is a texture information rather than a picture? The hint experiment isolates it. One PNG, three greys: sixty-four, one twenty-eight, one ninety-two. Two samplers read the same file — one marked source color, one not — on unshaded quads, under a linear tonemap."

## B13 — Same bytes, two meanings (result)
*On screen:* **In-engine capture · scripted** — `captures/hint_quads.png`, enlarged, the six sampled band centres marked; predicted and measured table from TEST-REPORT.md.
*Narration:* "With source color, the screen shows the file's own numbers: the decode on sampling and the encode on output cancel. Without it, the numbers are taken as already linear, and the encode brightens them: one thirty-seven, one eighty-eight, two twenty-five. All six exactly as predicted. Same bytes; the hint decides what they mean."

## B14 — Three samplers (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `shaders/rock_frost.gdshader` lines 15–19; cues on lines 16, 17 and 18. Notes: each texture's import settings and imported format (MATERIALS.md).
*Narration:* "The rock makes the same choice three times. Line sixteen: the albedo is colour, marked source color. Line seventeen: the normal map is data — directions, with no colour conversion. Line eighteen: roughness is data too, read as stored."

## B15 — Data, checked as data (result)
*On screen:* **Headless test results, as recorded in TEST-REPORT.md — not a render**: the curl-ratio table for both normal maps, and the `source_color` mutation.
*Narration:* "A normal map is a field of slopes, and the curl check can tell which way it was written. The bound map scores zero point one four four four read the OpenGL way, and one point eight five five six the DirectX way — so it's OpenGL, which Godot expects. And delete source color from line sixteen: the material test fails, exit code one."

## B16 — Where the frost goes (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `shaders/rock_frost.gdshader` lines 30–35; cues on lines 33 and 35.
*Narration:* "Line thirty-five is where data becomes a decision. The roughness value at each pixel is compared with a threshold that frost amount slides from minus zero point one to one point one. Below it, the surface frosts, with a soft band either side. Nobody sees the roughness map; it decides where the frost goes."

## B17 — Frost amount, swept (result)
*On screen:* **In-engine capture · scripted** — `captures/rock_sweep_frost_amount_min.png`, `_default.png`, `_max.png`, with the author's observations from TEST-REPORT.md.
*Narration:* "Frost amount at zero: the frosted rock matches the bare one. At zero point six five, the frost layer — and despite the audit's worry about the compressed roughness map, the author saw no blocks at this size. At one, a white crust buries the rock's detail, which the author judged bad for readability."

## B18 — The interface (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `shaders/rock_frost.gdshader` lines 3–12; cues on lines 5, 6, 7 and 11.
*Narration:* "Lines four to twelve are the material's interface: five values in two groups — two colours, and three numbers, each with a range. The capture scene swept every one on the frosted material — minimum, its own value, maximum — and restored it after each."

## B19 — The interface, swept (result)
*On screen:* **In-engine capture · scripted** — twelve `captures/rock_sweep_<uniform>_<min|default|max>.png` for `base_tint`, `normal_scale`, `roughness_scale` and `frost_color`, with the author's observations from TEST-REPORT.md.
*Narration:* "Base tint at black leaves white frost floating on a dark rock. Normal scale at zero flattens the relief; at two, it digs in. Roughness scale at zero gives a sharp highlight; at two, fully matte. Frost colour at black reads like soot. And nothing broke the render: no missing-material pink, no black holes."

## B20 — The language (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `shaders/hurt_tint.gdshader` lines 1–4; cues on lines 1, 3 and 4. Notes: `rock_frost.gdshader:1`; LANGUAGE-NOTES.md answers 1 and 8.
*Narration:* "Question four: what is the Godot shading language? Line one says it: shader type, canvas item. One word picks the pipeline — 2D here, spatial for the rock — and with it, which built-ins exist. Lines three and four use what plain GLSL doesn't have: hints like source color and hint range."

## B21 — Two pipelines (result)
*On screen:* **In-engine capture · scripted** — `captures/hurt_tint_i1.0.png` (canvas_item) beside `captures/rock_compare_default.png` (spatial), each enlarged.
*Narration:* "The same language, two pipelines. Canvas item: the 2D sprite, where the shader mixes colour directly. Spatial: the rock under one directional light, where the shader writes albedo, roughness and a normal map, and the 3D pipeline lights them."

## B22 — The shader Godot writes
*On screen:* **Source view — reconstruction, not a screenshot**: `shaders/standard_generated.gdshader` line 7 beside `rock_frost.gdshader` line 16, and line 19 beside line 17, annotated from LANGUAGE-NOTES.md.
*Narration:* "Godot can write this language for you. Converting a standard material gives this generated shader. Its line seven matches the author's line sixteen: albedo as source color, plus repeat enable. Its line nineteen matches line seventeen: the normal map read as data — but with hint roughness normal, which links it to the roughness texture."

## B23 — What the tests proved
*On screen:* **Headless test results, as recorded in TEST-REPORT.md — not a render**: the machine-checks table, shortened.
*Narration:* "What the tests proved. The seven earlier suites: ninety-five checks, zero failures, before and after, every line identical. The hurt tint: seventeen checks at three frame rates. The materials: thirty-two checks — again after deleting the import cache. Every run went through one wrapper that fails on any shader or script error."

## B24 — Broken on purpose, and the limit
*On screen:* card: the three mutations and their results; "What no headless run shows" (TEST-REPORT.md).
*Narration:* "Then the tests were broken on purpose. Delete a semicolon: a shader error, exit one. Rename intensity in the shader only: no error at all — fifteen checks still passed, and only two caught it. Remove source color from the albedo: the material test fails. And no headless run shows the look; the dummy renderer draws nothing."

## B25 — What the agent got wrong
*On screen:* card: FRICTIONAL.md entries 4, 6 and 8.
*Narration:* "What the agent got wrong. Its CLAUDE dot M D draft cited a log that wasn't committed, and said the blink toggles every tick; it's every tenth of a second. When R7 failed at one forty-four, it offered to widen the tolerance or drop the clause; the author refused both, and measured in physics ticks instead. And it recommended letting an Assignment 3 test fail; the author moved the material into scene overrides."

## B26 — Still uncertain, and one next step
*On screen:* card: still open (FRICTIONAL.md), known limitations (README.md), one next step.
*Narration:* "Still uncertain: why the GPU wrote the two point-five channels one step lower, and why a pause shifts frame time by more than one physics step. Both explanations are untested. The ice roughness is a constant, not a uniform. One next step: test the rounding, with more controlled values that land on point five."

## B27 — Who did what
*On screen:* card: human and AI contributions (FRICTIONAL.md), the texture source (SOURCES.md), the revision shown.
*Narration:* "Who did what. The author: every decision in the brief, the colour line and every declaration, the hand computations, the three shaders typed by hand, the language answers, and every human check. Claude Code: the driver, the tests, the materials and scenes, the audit and the capture tools. Claude in chat: planning, checking arithmetic, and drafting documents. The rock textures are Poly Haven's Rock 01, by Rob Tuytel, CC0."

## B28 — Verdict
*On screen:* `ClaudeVerdictArtifact`.
*Narration:* "The verdict. Built: a hurt tint driven by game state, a frosted rock from one shader and two materials, a hint experiment, and the tests around them. Measured: every controlled pixel, six hint values, and the material wiring. Judged by the author: that the tint and the frost look right. Unknown: two untested explanations. Source shown: commit 4 0 c 4 2 f 5."

## B29 — Your Turn
*On screen:* `ClaudeComposerAsk`, greeting "Your turn.", runningText "paste this into Claude…". Prompt: "Please use Walker to turn the ice roughness in my frosted rock shader into a uniform with a range, set in both materials. Before changing anything, predict which of my captures will change and which will not, then add a check to my material test that fails if either material leaves it unset." — **Suggested prompt**.
*Narration:* "Your turn. Please use Walker to turn the ice roughness in my frosted rock shader into a uniform with a range, set in both materials. Before changing anything, predict which of my captures will change and which will not, then add a check to my material test that fails if either material leaves it unset. It's one bounded change, and the prediction comes first, so a capture can prove you wrong. Take this prompt, run it on your own shader, and change one thing."

## B30 — Regular outro
*On screen:* `ClaudeTitleOutro` (locked): exact title, @NikBearBrown, one slug-seeded mascot, no subline. Silent.
