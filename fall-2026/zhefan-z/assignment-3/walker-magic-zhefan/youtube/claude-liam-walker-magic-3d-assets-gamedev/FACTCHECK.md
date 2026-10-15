# FACTCHECK — walker-magic Assignment 3 gamedev film

Every spoken claim, with its source at commit `8d8895c` unless stated. "A3 docs" = `fall-2026/zhefan-z/assignment-3/` (CHANGE-BRIEF.md, TEST-REPORT.md, FRICTIONAL.md). Checked by Claude Code against the files, the recorded logs and the frames; the author approves the script.

| Beat | Claim | Source | Status |
|---|---|---|---|
| B00 | Three simple 3D props for a 2D cave game, built by Claude in a running Blender, checked in Godot | README.md (A3); TEST-REPORT.md | ✓ |
| B00 | On screen: 1.0 × 0.8 × 0.7 m / 60; 0.35 × 0.35 × 0.6 m / 30; 0.8 × 0.5 × 0.6 m / 76; 22 checks / 0 failures | evidence/glb-read-8d8895c.log; evidence/test_a3_assets-8d8895c.log | ✓ |
| B01 | The check passed: the size is right; whether they look right is for a person | Assignment 3 text ("A passing check shows your assets arrived at the size you intended…"); TEST-REPORT.md "What the headless check does not show" | ✓ |
| B02 | walker-magic: a pixel-art fire mage in a cold cave, so far all 2D | README.md (A3) "The game itself is still 2D"; CONCEPT.md | ✓ |
| B02 | At most six shapes and 500 triangles each, through the Blender MCP, one hand edit, a small Godot scene, a headless check | Assignment 3 text (ASSIGNMENT-3.txt, not committed) | ✓ |
| B02 | Rock a roadblock she jumps; crystal cold-blue decoration; chest the reward at the exit, warm on purpose; warmth = what fire made safe | CHANGE-BRIEF.md Assets 1–3 and Palette rule | ✓ |
| B03 | Before any build prompt, the author measured the shapes in Scene Statistics | CHANGE-BRIEF.md "Measured in my Blender session"; FRICTIONAL.md "Learning the window"; the three screenshots | ✓ |
| B03 | Default UV sphere 960 triangles, nearly twice the limit; ico sphere subdivision 1: 20; six-sided cone: 10 | screenshots' status bars (三角面:960, 20, 10); CHANGE-BRIEF.md table | ✓ |
| B03 | Predictions 60 / 30 / 76 | CHANGE-BRIEF.md "measured basis" lines | ✓ |
| B04 | The rock's prompt: build only this asset, exactly as the brief specifies, don't export yet | the author's Rock prompt (session transcript, 2026-10-14; PROMPTS.md) | ✓ |
| B04 | Claude Code proposed six steps; nothing ran until "Yes, build it" | the approval screenshot ("proposed the Rock build in six steps … Nothing is built"); build_rock.py starts after it | ✓ |
| B05 | Call R2 bakes each stone's turns into its mesh (rotation stays 0) and sets scale = target / measured vertex size | tools/blender/build_rock.py lines 309–319 | ✓ |
| B06 | The first build sized stones from a looser box; the fit stretched it 1.19 wide; it read as three dice | FRICTIONAL.md "Building the Rock"; TEST-REPORT.md cycle 1 ("look like dice"); build_rock.py call 7 output | ✓ |
| B06 | Revision 1 fits with factors of exactly one; a 6.6 cm floor gap stays, accepted as a known limitation | TEST-REPORT.md cycle 1 and Known limitations; build_rock.py R5, R6 and the dated note | ✓ |
| B07 | The first three attempts never reached the scene; Claude Code re-measured each time; the fourth: Crystal_Short_B, Z typed as 20°, Enter, `*` in the title bar | FRICTIONAL.md "Building the Crystal"; build_crystal.py calls 8, 9, 11, 12 and the note; the screenshot | ✓ |
| B08 | The turn narrowed the crystal to 32 cm, under the brief | build_crystal.py call 12 output (0.3228 m) | ✓ (0.3228 m, spoken "32 centimetres") |
| B08 | J1 lengthens only that cone along its own axis; the rotation stays as typed | build_crystal.py lines 472–478; J1 printed "rotation unchanged: True" | ✓ |
| B09 | Factor 1.21; back to 35 × 35 × 60 cm and 30 triangles | J1 output (1.2125); J2 output; FRICTIONAL.md | ✓ |
| B10 | The lid is an 8-sided cylinder on its side, turned until a face points straight up; line 134 checks the true top against 0.6 m | build_chest.py lines 107–113 and 134 | ✓ |
| B11 | It does: 0.600, flat | build_chest.py call 4 output ("true top z: 0.6 … top face normal (0,0,1)") | ✓ |
| B11 | An 8-sided lid as deep as the body rises half its depth; split 37.6 + 22.4 cm instead of 35 + 25; total held; the brief records the change | CHANGE-BRIEF.md "Revision 2026-10-14" | ✓ |
| B12 | Blender's own glTF exporter, binary, +Y up (the default in 5.2.2), with materials | build_chest.py lines 377–390; SOURCES.md (A3) | ✓ |
| B13 | One node with no transform; height on Y from 0; the predicted triangles; the chest's lock reaches +Z: front faces the camera, as predicted | evidence/glb-read-8d8895c.log; CHANGE-BRIEF.md axes prediction | ✓ |
| B14 | The author looked from the game camera, from above, from below through the floor; upright, closed undersides | TEST-REPORT.md HUMAN CHECK; the three screenshots | ✓ |
| B14 | The gold, lowered to metallic 0.3, reads yellow-gold | TEST-REPORT.md cycle 2 (the F6 screenshot) | ✓ |
| B14 | Grey default background, floor edges visible, the mage a thin line from the side | TEST-REPORT.md HUMAN CHECK; screenshots | ✓ |
| B15 | WorldEnvironment with the cave's background colour; billboard mode on the mage | prop_room.tscn lines 16–18, 25–26, 40 | ✓ |
| B15 | Pixel size 0.0227 m makes 64 pixels exactly 1.45 m | prop_room.tscn line 39 (0.0226563 × 64 = 1.4500); mage_idle.png 64 opaque rows | ✓ |
| B16 | Native 4K, scripted camera (label: capture copy · viewport set to 3840×2160); props on the floor beside the mage; she keeps facing the camera; from behind the rock and chest go almost black; the crystal keeps its blue | CAPTURE.md (probe, run-01, frames checked); RIFF.md | ✓ (observed in the frames) |
| B17 | The check loads each file, measures true vertex bounds, compares with numbers copied from the brief, within 2 cm | tests/test_a3_assets.gd lines 8–16, 46–60, 78–90 | ✓ |
| B18 | 22 checks, 0 failures | evidence/test_a3_assets-8d8895c.log | ✓ |
| B18 | With the rock's width changed to 1.1 in a scratch copy: one failure, exit 1 | TEST-REPORT.md Extra checks (Claude Code's session report, 2026-10-14) | ✓ |
| B18 | It can't tell whether they read as what they are, or how the glow looks in a real cave | TEST-REPORT.md "What the headless check does not show" | ✓ |
| B19 | Sized the first rock from an overstated box; blamed a different Blender (same one; the rotation was probably cancelled); said FRICTIONAL.md didn't exist; each caught by checking | TEST-REPORT.md "What Claude got wrong" | ✓ |
| B20 | Built / measured / judged / unknown; contributions; source 8d8895c | TEST-REPORT.md; FRICTIONAL.md "Human and AI contributions"; SOURCES.md (A3) | ✓ |
| B20 | Claude in chat drafted the build prompts | the author's statement in the film review, 2026-10-14 (not stated in FRICTIONAL.md, which lists sizes, the connection test, the order of work, colours, the metallic fix and documents) | ✓ author |
| B21 | The torch is the brief's next step: warmth beside the chest | CHANGE-BRIEF.md Asset 3 ("later a torch or campfire will stand beside it") and Out of scope | ✓ |

**Wording changes after approval** (SCRIPT.md header): B10 "Line 134 then asks"; B21's prompt says "my headless asset check"; spoken spellings (G-L-T-F, "8 d 8 8 9 5 c", "FRICTIONAL dot M D", "Crystal Short B").

**Not checked by this table:** the pronunciation of the narration (Kokoro output must be listened to), and anything the screen shows that the narration does not claim.
