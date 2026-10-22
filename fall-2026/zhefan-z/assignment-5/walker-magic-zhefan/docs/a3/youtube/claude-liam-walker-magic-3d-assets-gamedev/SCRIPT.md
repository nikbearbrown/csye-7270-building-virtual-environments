# SCRIPT — walker-magic Assignment 3 gamedev film (Brutalist `godot-gamedev` + `walker`)

> Approved beat sheet and script (2026-10-14). Narrator: Liam, in for Bear (local Kokoro `am_onyx`). Native 4K landscape, 30 fps. No burned captions. The final card is silent (this toolkit copy has no stock jingle, as in Assignment 2).
> Narration lines are written for the voice: numbers, file names and the commit are spelled the way they should be spoken. On-screen text keeps the exact spelling.
> Wording changes after approval, made so the narration matches the screen: B10 "The last lines ask" → "Line 134 then asks" (the card shows lines 107–113 and line 134 as a note); B21's prompt says "my headless asset check" instead of the file name, so it reads aloud verbatim; B20 reads the commit as characters; B01's correction became one word ("look" → "size"), because `BrutalistHesitantWriter` matches single words only and the two-word phrase was never corrected in the first render. After the author's review (2026-10-14): B01 set in four lines at a larger size (Gate V underfill); B03 "Before any build prompt"; B19 "Each was caught by checking, not by trust."; B20 adds "drafted the build prompts"; the B16 label names the capture copy's 3840×2160 viewport.

Title: **Cold Stone, Warm Gold: Three 3D Props for a Cave Mage**

Labels used on screen: **Reconstructed prompt** · **My screenshot** (the author's own screenshots) · **Excerpt from the Claude Code session** · **Blender MCP look render — captured by Claude Code** · **Source view · Blender Python, run through the MCP — not Godot** · **Godot editor reconstruction** (with path and lines) · **Godot Movie Maker capture · scripted camera** · **Headless check output — not a render** · **Recorded command output**.

## B00 — Walker opening (Claude composer)
*On screen:* `ClaudeComposerAsk`, greeting "Hello, Liam". Prompt: "Please use Walker to convert my game design document about a fire mage in a cold cave into three simple 3D props — a rock, a crystal and a treasure chest — built in Blender through the MCP and checked in Godot." — **Reconstructed prompt**. Output lines: the three sizes and triangle counts; `22 checks / 0 failures`.
*Narration:* "Hello — this is Liam, in for Bear. The ask: three simple 3D props for a 2D cave game, built by Claude inside a running Blender, then checked in Godot."

## B01 — Hesitant-writer summary (window ≥ 9 s)
*On screen:* typed in four lines, "Three 3D props / for a 2D cave game. / The check passed: / the look is right." Correction (one word, as the walker summary requires): "look" → "size".
*Narration:* "Three 3D props for a 2D cave game. The check passed: the size is right. Whether they also look right is a different question — and only a person can answer it."

## B02 — The assignment, and this game
*On screen:* card: the requirements, and the three assets with their roles (CHANGE-BRIEF.md).
*Narration:* "The game is walker magic: a pixel-art fire mage in a cold cave, so far all 2D. Assignment three asks for three props from basic shapes — at most six shapes and five hundred triangles each — through the Blender MCP, with one edit by hand, a small Godot scene, and a headless check. The rock is a roadblock she jumps. The crystal is cold-blue decoration. The chest is the reward at the exit, warm on purpose: in this cave, warmth means fire made it safe."

## B03 — Learning the window
*On screen:* **My screenshot** ×3 (UV sphere 960, ico sphere at subdivision 1: 20, 6-vertex cone: 10), status bars enlarged.
*Narration:* "Before any build prompt, the author measured Blender's shapes in Scene Statistics. A default UV sphere: 960 triangles, nearly twice the limit. An ico sphere at one subdivision: 20. A six-sided cone: 10. Those readings became the predictions: sixty triangles for the rock, thirty for the crystal, seventy-six for the chest."

## B04 — The prompt and the approval
*On screen:* two lines of the Rock prompt, verbatim — **Excerpt from the Claude Code session** — and **My screenshot** `claude-code-rock-plan-approval.png`.
*Narration:* "Each asset began with a written prompt and a plan. This is the rock's: build only this asset, exactly as the brief specifies, and don't export yet. Claude Code proposed six steps, and nothing ran until the author pressed Yes, build it."

## B05 — Rock, Revision 1 (code)
*On screen:* **Source view · Blender Python, run through the MCP — not Godot** · `tools/blender/build_rock.py` lines 309–319 (call R2).
*Narration:* "This is the revised rock, call R2. Each stone's turns are baked into its mesh, so its rotation stays zero; then its scale is the target size divided by what its vertices actually measure."

## B06 — Rock (result)
*On screen:* **Blender MCP look render — captured by Claude Code**: the first build beside Revision 1.
*Narration:* "The first build sized the stones from a looser box. The final fit had to stretch the rock 1.19 times wide, and it read as three dice. Sized from the vertices, Revision 1 fits with factors of exactly one. One flaw stays: a 6.6-centimetre gap at the floor between the base stones, accepted as a known limitation."

## B07 — The hand edit
*On screen:* **My screenshot** `hand-edit-crystal-short-b-rotz20.png`, with the title bar `*` and the rotation panel enlarged.
*Narration:* "The crystal carries the hand edit. The first three attempts never reached the scene; Claude Code re-measured and saw no change. The fourth stuck: Crystal Short B, rotation Z typed as twenty degrees, Enter, and an asterisk in the title bar."

## B08 — Crystal (code)
*On screen:* **Source view · Blender Python, run through the MCP — not Godot** · `tools/blender/build_crystal.py` lines 472–478 (call J1).
*Narration:* "That turn narrowed the crystal to 32 centimetres, under the brief. Call J1 doesn't stretch it: it lengthens only that cone along its own axis, so the rotation stays exactly as typed."

## B09 — Crystal (result)
*On screen:* **Blender MCP look render — captured by Claude Code**; 0.3228 → 0.350 m.
*Narration:* "A factor of 1.21. The crystal is back to 35 by 35 by 60 centimetres and thirty triangles, with the hand-turned cone still leaning where it was put."

## B10 — Chest lid (code)
*On screen:* **Source view · Blender Python, run through the MCP — not Godot** · `tools/blender/build_chest.py` lines 107–113 (call 4), with line 134 as a note.
*Narration:* "The chest lid is an eight-sided cylinder on its side, turned until one face points straight up. Line 134 then asks one question: does the true top reach 0.6 metres?"

## B11 — Chest (result)
*On screen:* **Blender MCP look render — captured by Claude Code**.
*Narration:* "It does: 0.600, flat. An eight-sided lid as deep as the body rises half its depth, so the split came out 37.6 plus 22.4 centimetres instead of 35 plus 25. The total held, and the brief records the change."

## B12 — Export (code)
*On screen:* **Source view · Blender Python, run through the MCP — not Godot** · `tools/blender/build_chest.py` lines 377–390 (call E1).
*Narration:* "Export uses Blender's own G-L-T-F exporter: binary, plus-Y up, the default in 5.2.2, with materials."

## B13 — Export (result)
*On screen:* **Recorded command output** — the three `.glb` files read outside Blender, from the reference copy of 8d8895c.
*Narration:* "Read back outside Blender, each file has one node with no transform, height on Y starting at zero, and exactly the predicted triangles. The chest's lock reaches plus-Z: its front faces the camera, as the brief predicted."

## B14 — The author's look in Godot
*On screen:* **My screenshot** ×3 `prop-room-*-before-fixes.png`.
*Narration:* "Then the author's own look in Godot: from the game camera, from above, from below through the floor. All three stand upright with closed undersides, and the chest's gold, lowered to metallic 0.3, reads yellow-gold. But the background was Godot's default grey, the floor's edges showed, and from the side the mage became a thin line."

## B15 — The scene fixes (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `showcase3d/prop_room.tscn` lines 37–44 (the Mage), with lines 16–18 (Environment) as a note.
*Narration:* "Two fixes in the scene file: a WorldEnvironment with the cave's background colour, and billboard mode on the mage, so she turns to face the camera. Her pixel size, 0.0227 metres, makes sixty-four pixels exactly 1.45 metres."

## B16 — The running scene (result)
*On screen:* **Godot Movie Maker capture · scripted camera** · run-01 · capture copy · viewport set to 3840×2160.
*Narration:* "Here it is running, at native 4K, with a scripted camera. The props stand on the floor beside a 1.45-metre mage. As the camera swings behind them, she keeps facing us — a flat sprite always shows her front — and with one light from the front, the rock and the chest go almost black, while the crystal keeps its blue."

## B17 — The headless check (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `tests/test_a3_assets.gd` lines 78–90.
*Narration:* "The headless check loads each file, measures its true vertex bounds, and compares them with numbers copied from the brief, within two centimetres."

## B18 — The headless check (result)
*On screen:* **Headless check output — not a render**, re-run on the reference copy of 8d8895c, beside the brief.
*Narration:* "Twenty-two checks, zero failures. It can fail, too: with the rock's width changed to 1.1 in a scratch copy, it reported one failure and exit code one. What it can't tell you is whether these read as a rock, a crystal and a chest, or how the glow looks in a real cave."

## B19 — What Claude got wrong
*On screen:* card (TEST-REPORT.md → What Claude got wrong; Known limitations).
*Narration:* "Claude got things wrong. It sized the first rock from an overstated box. When the hand edit didn't appear, it blamed a different Blender; it was the same one, and the rotation was probably cancelled. It once said FRICTIONAL dot M D didn't exist. Each was caught by checking, not by trust."

## B20 — Verdict
*On screen:* `ClaudeVerdictArtifact`.
*Narration:* "The verdict. Built: three props through the MCP, their files, a prop room and a check. Measured: size, origin, transforms, triangles and colours. Judged by the author: that they read as what they are. Still unknown: how the floor gap and the glow look in real play. Claude Code wrote the Blender code, the scene and the check; Claude in chat proposed sizes and colours, drafted the build prompts, and drafted documents; the author chose, approved, edited by hand, and looked. Source shown: commit 8 d 8 8 9 5 c."

## B21 — Your Turn
*On screen:* `ClaudeComposerAsk`, greeting "Your turn.", runningText "paste this into Claude…". Prompt: "Please use Walker to add a torch beside my treasure chest: one prop from basic shapes, under 150 triangles, warm emission, origin at its base. Before building, predict its bounding box in metres, then add a line to my headless asset check that fails if the prediction is wrong."
*Narration:* "Your turn. Please use Walker to add a torch beside my treasure chest: one prop from basic shapes, under 150 triangles, warm emission, origin at its base. Before building, predict its bounding box in metres, then add a line to my headless asset check that fails if the prediction is wrong. The torch is the brief's next step: warmth beside the chest. The prediction comes first, so the check can prove you wrong. Take this prompt, run it on your own game, and change one thing."

## B22 — Regular outro
*On screen:* `ClaudeTitleOutro` (locked): exact title, @NikBearBrown, one slug-seeded mascot, no subline. Silent.
