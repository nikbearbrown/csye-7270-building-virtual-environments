# FACTCHECK - Key Terms: Blender to Godot

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 2 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Video only, Computed, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `30` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; Driving Blender | PASS | Second-pass check against slide 2 step 1 and 03-blender-mcp-to-godot.md | none |
| 5 | B0102 | Explanation of: Units, axes and transforms; Why a model arrives lying down, or the wrong size | PASS | Second-pass check against slide 2 step 2 and 03-blender-mcp-to-godot.md | none |
| 6 | B0103 | Explanation of: Export, import and collision; How a model and its collider reach Godot | PASS | Second-pass check against slide 2 step 3 and 03-blender-mcp-to-godot.md | none |
| 7 | B0104 | Explanation of: Measuring and budget; How you prove the result, keep it cheap and repeat it | PASS | Second-pass check against slide 2 step 4 and 03-blender-mcp-to-godot.md | none |
| 8 | B0201 | Explanation of: MCP; in the book text; TELL THESE APART; MCP route | PASS | Second-pass check against slide 3 step 1 and 03-blender-mcp-to-godot.md | none |
| 9 | B0202 | Explanation of: MCP tool; in the book text; A named action the agent may call, with typed arguments.; TOOLS THE SERVER OFFERS | PASS | Second-pass check against slide 3 step 2 and 03-blender-mcp-to-godot.md | none |
| 10 | B0203 | Explanation of: MCP server and add-on; in the book text; The server relays calls to the add-on over a local socket. | PASS | Second-pass check against slide 3 step 3 and 03-blender-mcp-to-godot.md | none |
| 11 | B0301 | Explanation of: bpy; in the book text; TELL THESE APART; --python-exit-code 1 | PASS | Second-pass check against slide 4 step 1 and 03-blender-mcp-to-godot.md | none |
| 12 | B0302 | Explanation of: Headless Blender; in the book text; also: background mode (-b); Running Blender with no window, from the command line. | PASS | Second-pass check against slide 4 step 2 and 03-blender-mcp-to-godot.md | none |
| 13 | B0303 | Figures spoken: `exit code 0`, `exit code 1` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 14 | B0303 | Explanation of: --python-exit-code; in the book text; SAME SCRIPT, WHICH RAISES ValueError; Blender -b --python bad.py | PASS | Second-pass check against slide 4 step 3 and 03-blender-mcp-to-godot.md | none |
| 15 | B0401 | Figures spoken: `2.1 m`, `1.8 m` | PASS | Each figure is printed on slide 5 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 16 | B0401 | Explanation of: Unit; in the book text; The length one coordinate step stands for, usually a metre.; TELL THESE APART | PASS | Second-pass check against slide 5 step 1 and 03-blender-mcp-to-godot.md | none |
| 17 | B0402 | Figures spoken: `1.0`, `1.8 m`, `1.8 cm`, `unit scale 0.01` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 18 | B0402 | Explanation of: in the book text; Unit scale; A MESH 1.8 UNITS TALL, TWO UNIT SCALES; 1.8 m | PASS | Second-pass check against slide 5 step 2 and 03-blender-mcp-to-godot.md | none |
| 19 | B0403 | Explanation of: Up axis; in the book text; Godot's forward is −Z; Which axis points up: Z in Blender, Y in glTF and Godot. | PASS | Second-pass check against slide 5 step 3 and 03-blender-mcp-to-godot.md | none |
| 20 | B0404 | Figures spoken: `(0.20, 0.20, 1.80)`, `1.80` | PASS | Each figure is printed on slide 5 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 21 | B0404 | Explanation of: Axis conversion; in the book text; ROTATE Z-UP TO Y-UP; Godot box: (0.20, 1.80, 0.20) | PASS | Second-pass check against slide 5 step 4 and 03-blender-mcp-to-godot.md | none |
| 22 | B0501 | Figures spoken: `2 m cube`, `0.20 × 1.80 × 0.20`, `1.00 × 1.00 × 1.00` | PASS | Each figure is printed on slide 6 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 23 | B0501 | Explanation of: Apply transforms; in the book text; TELL THESE APART; Scale | PASS | Second-pass check against slide 6 step 1 and 03-blender-mcp-to-godot.md | none |
| 24 | B0502 | Figures spoken: `node scale (1.0, 0.4)`, `0.6 m` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 25 | B0502 | Explanation of: Node scale; in the book text; A scale left on the node instead of baked into the mesh.; SCALE LEFT ON THE NODE | CORRECTED | Second-pass check against the slide and the chapter: A scale left on the node does not by itself make a collider stick out: Chapter 3 says anything generated from the mesh inherits the scale, so the bump into air needs a shape that cannot follow the stretch, the slide's sphere collider ('A sphere has one radius. It cannot follow a stretched mesh'). | Reworded. Was: "Node scale is a scale left on the node, instead of baked into the mesh. Here a ball is squashed by a node scale of one by zero point four, but its sphere collid" |
| 26 | B0503 | Figures spoken: `0.9 m` | PASS | Each figure is printed on slide 6 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 27 | B0503 | Explanation of: Origin and pivot; in the glossary; WHERE THE ORIGIN SITS; origin at the base | PASS | Second-pass check against slide 6 step 3 and 03-blender-mcp-to-godot.md | none |
| 28 | B0601 | Figures spoken: `(2.0, 2.0, 2.0) stale`, `(0.2, 0.2, 1.8) fresh` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 29 | B0601 | Explanation of: Dimensions; in the book text; TELL THESE APART; Claimed | PASS | Second-pass check against slide 7 step 1 and 03-blender-mcp-to-godot.md | none |
| 30 | B0602 | Figures spoken: `12 vertices`, `0.78`, `1.80` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 31 | B0602 | Explanation of: Bounding box; in the glossary; its half-sizes are the extents; The smallest axis-aligned box that holds an object. | PASS | Second-pass check against slide 7 step 2 and 03-blender-mcp-to-godot.md | none |
| 32 | B0603 | Figures spoken: `0.2 × 1.8 × 0.2` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 33 | B0603 | Explanation of: Claim versus measurement; in the book text; CLAIMED 0.2 × 1.8 × 0.2 M, 1 CM TOLERANCE; MEASURED SIZE | PASS | Second-pass check against slide 7 step 3 and 03-blender-mcp-to-godot.md | none |
| 34 | B0701 | Explanation of: glTF; in the book text; TELL THESE APART; glTF | PASS | Second-pass check against slide 8 step 1 and 03-blender-mcp-to-godot.md | none |
| 35 | B0702 | Explanation of: in the book text; glTF packed into a single binary file.; GLB; PACKED INTO ONE FILE | PASS | Second-pass check against slide 8 step 2 and 03-blender-mcp-to-godot.md | none |
| 36 | B0703 | Explanation of: Material through export; in the book text; NAMES CARRY THROUGH; BLENDER | PASS | Second-pass check against slide 8 step 3 and 03-blender-mcp-to-godot.md | none |
| 37 | B0704 | Explanation of: Import file (.import); in the book text; THE .IMPORT FILE, [PARAMS]; nodes/root_type="" | PASS | Second-pass check against slide 8 step 4 and 03-blender-mcp-to-godot.md | none |
| 38 | B0801 | Explanation of: Name suffix; in the book text; TELL THESE APART; Visual mesh | PASS | Second-pass check against slide 9 step 1 and 03-blender-mcp-to-godot.md | none |
| 39 | B0802 | Figures spoken: `52 of 1,066`, `572`, `55`, `0` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 40 | B0802 | Explanation of: in the book text; Collision shape; BOX COLLIDER BECOMES A HULL; 52 of 1,066 | PASS | Second-pass check against slide 9 step 2 and 03-blender-mcp-to-godot.md | none |
| 41 | B0803 | Figures spoken: `60% of the line is outside`, `0% of the line is outside` | PASS | Each figure is printed on slide 9 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 42 | B0803 | Explanation of: Convex and concave; in the glossary; CAN A LINE LEAVE THE SHAPE?; concave | PASS | Second-pass check against slide 9 step 3 and 03-blender-mcp-to-godot.md | none |
| 43 | B0901 | Figures spoken: `8`, `6`, `12`, `24`, `42 triangles` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 44 | B0901 | Explanation of: Triangle count; in the glossary; not face count or vertex count; TELL THESE APART | PASS | Second-pass check against slide 10 step 1 and 03-blender-mcp-to-godot.md | none |
| 45 | B0902 | Figures spoken: `2,000,000`, `42`, `47,619` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 46 | B0902 | Explanation of: High-poly and low-poly; video only; TRIANGLES, LOG SCALE; high-poly sculpt | PASS | Second-pass check against slide 10 step 2 and 03-blender-mcp-to-godot.md | none |
| 47 | B0903 | Figures spoken: `80 points`, `2 points`, `20 values` | PASS | Each figure is printed on slide 10 at step 3 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 48 | B0903 | Explanation of: Texture baking; video only; DETAIL MOVES INTO AN IMAGE; high-poly: 80 points | PASS | Second-pass check against slide 10 step 3 and 03-blender-mcp-to-godot.md | none |
| 49 | B0904 | Figures spoken: `LOD 0: 42`, `LOD 1: 21`, `LOD 2: 11`, `10 m`, `25 m`, `40 m` | PASS | Each figure is printed on slide 10 at step 4 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 50 | B0904 | Explanation of: LOD; in the glossary; ONE POST, MOVING AWAY (ILLUSTRATIVE LEVELS); LOD 0: 42 | PASS | Second-pass check against slide 10 step 4 and 03-blender-mcp-to-godot.md | none |
| 51 | B1001 | Explanation of: Script as source; in the book text; TELL THESE APART; Source | PASS | Second-pass check against slide 11 step 1 and 03-blender-mcp-to-godot.md | none |
| 52 | B1002 | Figures spoken: `top = 1.7`, `top = 1.8` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 53 | B1002 | Explanation of: Version control; video only; SAME EDIT, TWO FILE TYPES; .blend (binary) | PASS | Second-pass check against slide 11 step 2 and 03-blender-mcp-to-godot.md | none |
| 54 | B1003 | Figures spoken: `(2)`, `Cube.003` | PASS | Each figure is printed on slide 11 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 55 | B1003 | Explanation of: Naming conventions; video only; Agreed rules for how files and objects are named.; RULE: prop_ + lowercase words + .glb | PASS | Second-pass check against slide 11 step 3 and 03-blender-mcp-to-godot.md | none |
| 56 | B1101 | Figures spoken: `mesh 2.0 m`, `× 0.9`, `1.8 m` | PASS | Each figure is printed on slide 12 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 57 | B1101 | Explanation of: PAIR 1 · LEFT; Scale; A multiplier on the object.; × 0.9 | PASS | Second-pass check against slide 12 step 1 and 03-blender-mcp-to-godot.md | none |
| 58 | B1102 | Explanation of: PAIR 2 · LEFT; MCP route; A transcript of tool calls.; → get_scene_info | PASS | Second-pass check against slide 12 step 2 and 03-blender-mcp-to-godot.md | none |
| 59 | B1103 | Figures spoken: `42 triangles`, `12 triangles` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 60 | B1103 | Explanation of: PAIR 3 · LEFT; Visual mesh; The detailed shape you see.; 42 triangles | PASS | Second-pass check against slide 12 step 3 and 03-blender-mcp-to-godot.md | none |
| 61 | B1104 | Figures spoken: `60% of the line is outside`, `0% of the line is outside` | PASS | Each figure is printed on slide 12 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 62 | B1104 | Explanation of: PAIR 4 · LEFT; Concave; Has a hollow; a line can leave it.; 60% of the line is outside | PASS | Second-pass check against slide 12 step 4 and 03-blender-mcp-to-godot.md | none |
| 63 | B1201 | Figures spoken: `1.0`, `0.2 × 1.8 × 0.2 m`, `1 cm`, `only one of three` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 64 | B1201 | Explanation of: “make the prop the right size”; WHAT THE INSTRUCTION CHECKS; height in Godot's Y, claim 1.8 m; good | PASS | Second-pass check against slide 13 step 1 and 03-blender-mcp-to-godot.md | none |
| 65 | B1202 | Figures spoken: `the 1.8 moves` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 66 | B1202 | Explanation of: “it's lying on its side”; x; y; z | PASS | Second-pass check against slide 13 step 2 and 03-blender-mcp-to-godot.md | none |
| 67 | B1203 | Figures spoken: `1 collider` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 68 | B1203 | Explanation of: “make the collision work”; suffix setting true; 1 collider: StaticBody3D, convex shape; suffix setting false | PASS | Second-pass check against slide 13 step 3 and 03-blender-mcp-to-godot.md | none |
| 69 | B1204 | Figures spoken: `100 triangles`, `42`, `12` | PASS | Each figure is printed on slide 13 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 70 | B1204 | Explanation of: “keep it cheap”; visual mesh; 42; collider | PASS | Second-pass check against slide 13 step 4 and 03-blender-mcp-to-godot.md | none |
| 71 | B1205 | Figures spoken: `1 cm grid`, `572 of 1,066`, `52 of 1,066`, `0 of 1,066` | PASS | Each figure is printed on slide 13 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 72 | B1205 | Explanation of: “keep the flag out of the collider”; box; 572 of 1,066; hull | CORRECTED | Second-pass check against the slide and the chapter: The hull's 52 is the deck's own grid model, not the physics sampling (slide 8 note: 'The model gives 572 for the box ... and 52 for the hull; the chapter's physics sampling found 55'), so it must not be set beside the box's 572 as the same kind of result; the box's 572 agrees in both methods. | Reworded. Was: "Keep the flag out of the collider becomes sample the pennant on a one centimetre grid and require zero points inside. The box had five hundred seventy-two of on" |
| 73 | B1301 | Figures spoken: `Six checks`, `1.0` | PASS | Each figure is printed on slide 14 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 74 | B1301 | Explanation of: Is unit scale 1.0, so one unit is one metre?; Did I apply rotation and scale, so every node's scale is 1?; Is the model Y-up in Godot, with Blender's Z on Godot's Y?; Do the measured dimensions match the claim, within 1 cm? | PASS | Second-pass check against slide 14 step 1 and 03-blender-mcp-to-godot.md | none |
| 75 | B1302 | Figures spoken: `scale is 1` | PASS | Each figure is printed on slide 14 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 76 | B1302 | Explanation of: Before you trust an imported model | PASS | Second-pass check against slide 14 step 2 and 03-blender-mcp-to-godot.md | none |
| 77 | B1303 | Explanation of: Before you trust an imported model | PASS | Second-pass check against slide 14 step 3 and 03-blender-mcp-to-godot.md | none |
| 78 | B1304 | Figures spoken: `1 cm` | PASS | Each figure is printed on slide 14 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 79 | B1304 | Explanation of: Before you trust an imported model | PASS | Second-pass check against slide 14 step 4 and 03-blender-mcp-to-godot.md | none |
| 80 | B1305 | Explanation of: Before you trust an imported model | PASS | Second-pass check against slide 14 step 5 and 03-blender-mcp-to-godot.md | none |
| 81 | B1306 | Figures spoken: `0.2 × 1.8 × 0.2 m, scale 1` | PASS | Each figure is printed on slide 14 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 82 | B1306 | Explanation of: Before you trust an imported model | PASS | Second-pass check against slide 14 step 6 and 03-blender-mcp-to-godot.md | none |
| 83 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 84 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 6 step 3: the no_apply row prints MEASURED SIZE (2.0, 2.0, 2.0) in red as a failure, while the caption below says 'no_apply is drawn at the right size, so only the scale check catches it.' (2.0, 2.0, 2.0) is the mesh AABB; Chapter 3 gives no_apply's in-scene AABB as (0.2, 1.8, 0.2). The column mixes the two, so the size column and the caption contradict each other. Slide 12 step 1 repeats it ('no_apply 2.0 fail' for height in Godot's Y). The narration avoids saying which check catches no_apply.
- Slide 1 says '30 terms from Chapter 3 and the glossary', but four of the 30 (high-poly and low-poly, texture baking, version control, naming conventions) are tagged 'video only' and come from the Riot series, as the slide's own source line says.
- Slide 12 step 5 sets the box's 572 (Chapter 3's physics sampling) beside the hull's 52 (the deck's own 1 cm grid model; the chapter's sampling found 55, as slide 8 step 2 notes) under a 'Computed' badge, with no note that the two numbers come from different methods.
- Slide 3 step 2 shows the headless command 'Blender -b --factory-startup --python build_post.py' without --python-exit-code 1, the flag the next step of the same slide says to always add.
- Group names on the map do not match the slide eyebrows: the map's 'Export, import and collision' is 'Export and import' on slides 7 and 8, and the map's 'Measuring and budget' is split across 'Proving it', 'Budget' and 'Keeping it repeatable'.
- Slide 11 step 3 draws the collision shape as a plain box around base and pole, while slide 8 step 2 shows that box replaced by a tapered hull; the 12-triangle label fits either, but the picture is the superseded collider.

## Open after the second pass

- slide 6 step 3: the deck prints no_apply's MEASURED SIZE as a red (2.0, 2.0, 2.0) fail beside the caption 'only the scale check catches it'; Chapter 3 gives (2.0, 2.0, 2.0) as the mesh AABB and (0.2, 1.8, 0.2) as the AABB in the running scene. Narration says only that no_apply carries a scale and that only the good build passes, which Chapter 3 supports; the deck itself needs fixing (deck problem, not narration).
- slide 12 step 1: chart shows no_apply '2.0 fail' for height in Godot's Y; consistent with the slide's 'require the mesh to measure', since the mesh AABB is 2.0, but it can read as the drawn height. Narration speaks no no_apply figure; left as is.
