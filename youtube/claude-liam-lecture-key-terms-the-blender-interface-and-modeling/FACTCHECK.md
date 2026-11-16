# FACTCHECK - Key Terms: The Blender Interface and Modeling

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 3 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Editor or docs, Computed, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `30` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; The Blender window | PASS | Second-pass check against slide 2 step 1 and 03-blender-mcp-to-godot.md | none |
| 5 | B0102 | Explanation of: Mesh anatomy; What a model is made of, and how it is counted | PASS | Second-pass check against slide 2 step 2 and 03-blender-mcp-to-godot.md | none |
| 6 | B0103 | Explanation of: Placing and measuring; Where it sits, how big it is, which way is up | PASS | Second-pass check against slide 2 step 3 and 03-blender-mcp-to-godot.md | none |
| 7 | B0104 | Explanation of: Shaping and surfacing; How it is built faster, and how it gets its look | PASS | Second-pass check against slide 2 step 4 and 03-blender-mcp-to-godot.md | none |
| 8 | B0201 | Explanation of: 3D viewport; editor or docs; The area where you see and edit the scene in 3D.; TELL THESE APART | PASS | Second-pass check against slide 3 step 1 and 03-blender-mcp-to-godot.md | none |
| 9 | B0202 | Figures spoken: `3 objects`, `1 collection` | PASS | Each figure is printed on slide 3 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 10 | B0202 | Explanation of: editor or docs; A tree listing every object and collection in the scene.; Outliner; Collection | PASS | Second-pass check against slide 3 step 2 and 03-blender-mcp-to-godot.md | none |
| 11 | B0203 | Figures spoken: `(0, 0, 1) m` | PASS | Each figure is printed on slide 3 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 12 | B0203 | Explanation of: editor or docs; Properties editor; Cube: Location; X 0.0 m | PASS | Second-pass check against slide 3 step 3 and 03-blender-mcp-to-godot.md | none |
| 13 | B0301 | Figures spoken: `3 editors` | PASS | Each figure is printed on slide 4 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 14 | B0301 | Explanation of: Workspace; editor or docs; TELL THESE APART; Workspace | CORRECTED | Second-pass check against the slide and the chapter: The slide's note says the layouts drawn are simplified; Blender's default window has more workspace tabs than the five drawn, so the sentence must describe the drawing, not Blender. | Reworded. Was: "Five tabs sit across the top of a Blender window. A Workspace is a saved arrangement of editors for one job, picked from those tabs. The tabs change which edito" |
| 15 | B0302 | Figures spoken: `FRAMES 1 TO 60`, `1, 30, 60`, `x = 0 m`, `x = 4 m` | PASS | Each figure is printed on slide 4 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 16 | B0302 | Explanation of: editor or docs; Playback controls and a frame scale with keyframes marked.; FRAMES 1 TO 60, THREE KEYFRAMES; 1 | PASS | Second-pass check against slide 4 step 2 and 03-blender-mcp-to-godot.md | none |
| 17 | B0401 | Figures spoken: `All 8 vertices`, `5.9 units` | PASS | Each figure is printed on slide 5 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 18 | B0401 | Explanation of: Object Mode; editor or docs; Work on whole objects: move, rotate, scale.; TELL THESE APART | PASS | Second-pass check against slide 5 step 1 and 03-blender-mcp-to-godot.md | none |
| 19 | B0402 | Figures spoken: `1 of 8`, `the other 7`, `8 points` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 20 | B0402 | Explanation of: editor or docs; Work on the mesh itself: its vertices, edges and faces.; Edit Mode; EDIT MODE: SELECT AND MOVE ONE VERTEX | PASS | Second-pass check against slide 5 step 2 and 03-blender-mcp-to-godot.md | none |
| 21 | B0403 | Figures spoken: `2 of 5` | PASS | Each figure is printed on slide 5 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 22 | B0403 | Explanation of: Collection; editor or docs; COLLECTIONS; Props | PASS | Second-pass check against slide 5 step 3 and 03-blender-mcp-to-godot.md | none |
| 23 | B0501 | Explanation of: Mesh; in the book text; TELL THESE APART; Vertex | PASS | Second-pass check against slide 6 step 1 and 03-blender-mcp-to-godot.md | none |
| 24 | B0502 | Figures spoken: `V = 8` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 25 | B0502 | Explanation of: in the glossary; A corner point of a mesh.; Vertex; VERTICES: THE CORNER POINTS | PASS | Second-pass check against slide 6 step 2 and 03-blender-mcp-to-godot.md | none |
| 26 | B0503 | Figures spoken: `E = 12`, `shared by 2 faces` | PASS | Each figure is printed on slide 6 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 27 | B0503 | Explanation of: in the glossary; A line joining two vertices.; Edge; EDGES: THE LINES BETWEEN THEM | PASS | Second-pass check against slide 6 step 3 and 03-blender-mcp-to-godot.md | none |
| 28 | B0504 | Figures spoken: `F = 6`, `8 − 12 + 6 = 2`, `6 − 9 + 5 = 2` | PASS | Each figure is printed on slide 6 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 29 | B0504 | Explanation of: Face; in the glossary; A flat surface bounded by edges.; FACES: THE FLAT SURFACES | PASS | Second-pass check against slide 6 step 4 and 03-blender-mcp-to-godot.md | none |
| 30 | B0601 | Figures spoken: `four vertices`, `1 quad = 2 triangles`, `6 quads = 12 triangles` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 31 | B0601 | Explanation of: Quad; in the glossary; A face with four vertices.; TELL THESE APART | PASS | Second-pass check against slide 7 step 1 and 03-blender-mcp-to-godot.md | none |
| 32 | B0602 | Figures spoken: `6`, `12`, `8`, `24` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 33 | B0602 | Explanation of: Polygon count; in the glossary; FOUR TALLIES OF THE SAME CUBE; Faces (Blender) | PASS | Second-pass check against slide 7 step 2 and 03-blender-mcp-to-godot.md | none |
| 34 | B0701 | Figures spoken: `6 of 12` | PASS | Each figure is printed on slide 8 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 35 | B0701 | Explanation of: Normal; in the glossary; The direction a surface faces.; TELL THESE APART | PASS | Second-pass check against slide 8 step 1 and 03-blender-mcp-to-godot.md | none |
| 36 | B0702 | Figures spoken: `3 of 12`, `3 flipped` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 37 | B0702 | Explanation of: Flipped normals; in the glossary; Faces pointing inward, so they look dark or vanish.; THREE NORMALS FLIPPED | PASS | Second-pass check against slide 8 step 2 and 03-blender-mcp-to-godot.md | none |
| 38 | B0801 | Figures spoken: `(3.0, 1.5)`, `45°`, `Scale 1.6` | PASS | Each figure is printed on slide 9 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 39 | B0801 | Explanation of: Transform; in the book text; TELL THESE APART; Origin | PASS | Second-pass check against slide 9 step 1 and 03-blender-mcp-to-godot.md | none |
| 40 | B0802 | Figures spoken: `1.8 M`, `HEIGHT 0`, `−0.9 m` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 41 | B0802 | Explanation of: in the glossary; Origin; PLACE A 1.8 M POST AT HEIGHT 0; lowest point −0.9 m | PASS | Second-pass check against slide 9 step 2 and 03-blender-mcp-to-godot.md | none |
| 42 | B0803 | Figures spoken: `2 UNIT`, `60°`, `(1.0, 1.7)` | PASS | Each figure is printed on slide 9 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 43 | B0803 | Explanation of: in the glossary; The point an object rotates and scales around.; Pivot; SAME 60° TURN OF A 2 UNIT BAR | PASS | Second-pass check against slide 9 step 3 and 03-blender-mcp-to-godot.md | none |
| 44 | B0901 | Figures spoken: `2 m`, `(0.1, 0.1, 0.9)`, `1.00`, `1.80` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 45 | B0901 | Explanation of: Apply transforms; in the book text; Also: scale versus size; TELL THESE APART | CORRECTED | Second-pass check against the slide and the chapter: Chapter 3 applies Rotation and Scale only (Object > Apply > Rotation & Scale; transform_apply with location=False), as slide 14 step 4 also says; the slide entry's 'position, rotation and scale' is not repeated as fact. | Reworded. Was: "A table of a pole's numbers. Apply transforms bakes position, rotation and scale into the mesh and resets them to neutral. This pole is a two metre cube scaled " |
| 46 | B0902 | Figures spoken: `(1.0, 0.5)`, `(4.12, 3.43)` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 47 | B0902 | Explanation of: Local and global space; editor or docs; PARENT TURNS; LOCAL POINT STAYS PUT; Local (1.0, 0.5) → global (4.12, 3.43) | PASS | Second-pass check against slide 10 step 2 and 03-blender-mcp-to-godot.md | none |
| 48 | B1001 | Figures spoken: `1.8 UNIT`, `2.1 M`, `1 unit = 1 m` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 49 | B1001 | Explanation of: Unit; in the book text; TELL THESE APART; Right-handed | PASS | Second-pass check against slide 11 step 1 and 03-blender-mcp-to-godot.md | none |
| 50 | B1002 | Figures spoken: `+Y Up`, `1.8` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 51 | B1002 | Explanation of: Right-handed, +Z up; in the book text; extents 0.2, 1.8, 0.2; extents 0.2, 0.2, 1.8 | CORRECTED | Second-pass check against the slide and the chapter: As spoken, 'Z points up' read as part of what right-handed means; handedness and the up axis are separate (Chapter 3: Godot is right-handed and Y-up), so Z up is tied to Blender. | Reworded. Was: "Blender's axes beside Godot's. Right-handed, plus Z up, is how Blender sets its axes. Right-handed means X cross Y gives Z, and Z points up. Godot is right-hand" |
| 52 | B1101 | Figures spoken: `level 1`, `8 vertices`, `6 faces`, `26 vertices`, `24 faces` | PASS | Each figure is printed on slide 12 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 53 | B1101 | Explanation of: Modifier; editor or docs; A live step that changes a mesh without editing it.; TELL THESE APART | PASS | Second-pass check against slide 12 step 1 and 03-blender-mcp-to-godot.md | none |
| 54 | B1102 | Figures spoken: `5 vertices`, `has 8`, `x = 0` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 55 | B1102 | Explanation of: Mirror modifier; editor or docs; Copies the mesh across an axis, so you model one half.; MODEL THE RIGHT HALF; MIRROR ON X | PASS | Second-pass check against slide 12 step 2 and 03-blender-mcp-to-godot.md | none |
| 56 | B1103 | Figures spoken: `4 times`, `6 faces`, `24 faces`, `96 faces` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 57 | B1103 | Explanation of: Subdivision Surface; editor or docs; Splits and smooths faces; each level makes 4 times as many.; ONE FACE'S OUTLINE, THEN 2× THE CORNERS PER LEVEL | PASS | Second-pass check against slide 12 step 3 and 03-blender-mcp-to-godot.md | none |
| 58 | B1104 | Figures spoken: `4 vertices`, `8 vertices`, `12 vertices`, `16 vertices`, `1 segment`, `3 segments` | PASS | Each figure is printed on slide 12 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 59 | B1104 | Explanation of: Bevel; editor or docs; A SQUARE CORNER, CUT IN 0 TO 3 SEGMENTS; sharp | PASS | Second-pass check against slide 12 step 4 and 03-blender-mcp-to-godot.md | none |
| 60 | B1201 | Figures spoken: `6 faces, 6 cells` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 61 | B1201 | Explanation of: UV map; in the glossary; The flattened 2D layout of a mesh used to place a texture.; TELL THESE APART | PASS | Second-pass check against slide 13 step 1 and 03-blender-mcp-to-godot.md | none |
| 62 | B1202 | Figures spoken: `12 edges`, `5 kept joined`, `7 seams` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 63 | B1202 | Explanation of: Unwrapping; in the glossary; Cutting a mesh and flattening it into a UV map.; UNWRAP: CUT THE SEAMS, FLATTEN | PASS | Second-pass check against slide 13 step 2 and 03-blender-mcp-to-godot.md | none |
| 64 | B1203 | Explanation of: Material versus texture; in the glossary; MATERIAL (THE RECIPE); TEXTURE (ONE IMAGE) | PASS | Second-pass check against slide 13 step 3 and 03-blender-mcp-to-godot.md | none |
| 65 | B1301 | Explanation of: PAIR 1 · LEFT; Origin; The point position and rotation are measured from.; ● origin: the object's own point | PASS | Second-pass check against slide 14 step 1 and 03-blender-mcp-to-godot.md | none |
| 66 | B1302 | Figures spoken: `scale 0.50`, `2 m`, `size 1.00 m` | PASS | Each figure is printed on slide 14 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 67 | B1302 | Explanation of: PAIR 2 · LEFT; Scale; A multiplier left on the object.; scale 0.50 | PASS | Second-pass check against slide 14 step 2 and 03-blender-mcp-to-godot.md | none |
| 68 | B1303 | Figures spoken: `6 faces`, `12 triangles` | PASS | Each figure is printed on slide 14 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 69 | B1303 | Explanation of: PAIR 3 · LEFT; Face count; What Blender shows.; 6 faces | PASS | Second-pass check against slide 14 step 3 and 03-blender-mcp-to-godot.md | none |
| 70 | B1304 | Explanation of: PAIR 4 · LEFT; Material; The whole surface recipe.; colour, roughness, metal… | PASS | Second-pass check against slide 14 step 4 and 03-blender-mcp-to-godot.md | none |
| 71 | B1401 | Figures spoken: `level 2`, `6 faces`, `24 faces`, `96` | PASS | Each figure is printed on slide 15 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 72 | B1401 | Explanation of: “make it smoother”; WHAT THE INSTRUCTION DOES; level 0: 6 faces; level 1: 24 faces | PASS | Second-pass check against slide 15 step 1 and 03-blender-mcp-to-godot.md | none |
| 73 | B1402 | Figures spoken: `5 vertices`, `8`, `38%` | PASS | Each figure is printed on slide 15 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 74 | B1402 | Explanation of: “I only want to model half”; you model: 5 vertices; the shape has: 8 vertices; you place 38% fewer vertices | PASS | Second-pass check against slide 15 step 2 and 03-blender-mcp-to-godot.md | none |
| 75 | B1403 | Figures spoken: `+Y Up`, `1.8 m`, `0.2 m` | PASS | Each figure is printed on slide 15 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 76 | B1403 | Explanation of: “it lies on its side in Godot”; Godot height without +Y Up: 0.2 m; Godot height with +Y Up: 1.8 m; the post stands, 1.8 m tall | PASS | Second-pass check against slide 15 step 3 and 03-blender-mcp-to-godot.md | none |
| 77 | B1404 | Figures spoken: `(0.1, 0.1, 0.9)`, `(1, 1, 1)`, `2.0 m`, `1.8 m` | PASS | Each figure is printed on slide 15 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 78 | B1404 | Explanation of: “the scale is wrong”; scale Z before: 0.9; scale Z after: 1.0; mesh height before: 2.0 m | PASS | Second-pass check against slide 15 step 4 and 03-blender-mcp-to-godot.md | none |
| 79 | B1405 | Figures spoken: `level 3 is 768 triangles`, `level 1 is 48`, `quadruples` | PASS | Each figure is printed on slide 15 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 80 | B1405 | Explanation of: “the model is too heavy”; level 0: 12 triangles; level 1: 48 triangles; level 2: 192 triangles | PASS | Second-pass check against slide 15 step 5 and 03-blender-mcp-to-godot.md | none |
| 81 | B1501 | Explanation of: Is the scene in metres, with unit scale 1.0?; Is the transform applied, so scale reads (1, 1, 1)?; Do all normals point out, so no face is dark or missing? | PASS | Second-pass check against slide 16 step 1 and 03-blender-mcp-to-godot.md | none |
| 82 | B1502 | Figures spoken: `1.0` | PASS | Each figure is printed on slide 16 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 83 | B1502 | Explanation of: Before you hand a model to the game | PASS | Second-pass check against slide 16 step 2 and 03-blender-mcp-to-godot.md | none |
| 84 | B1503 | Figures spoken: `(1, 1, 1)` | PASS | Each figure is printed on slide 16 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 85 | B1503 | Explanation of: Before you hand a model to the game | PASS | Second-pass check against slide 16 step 3 and 03-blender-mcp-to-godot.md | none |
| 86 | B1504 | Explanation of: Before you hand a model to the game | PASS | Second-pass check against slide 16 step 4 and 03-blender-mcp-to-godot.md | none |
| 87 | B1505 | Explanation of: Before you hand a model to the game | PASS | Second-pass check against slide 16 step 5 and 03-blender-mcp-to-godot.md | none |
| 88 | B1506 | Figures spoken: `(1, 1, 1)` | PASS | Each figure is printed on slide 16 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 89 | B1506 | Explanation of: Before you hand a model to the game | PASS | Second-pass check against slide 16 step 6 and 03-blender-mcp-to-godot.md | none |
| 90 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 91 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 6 (Quads, triangles and the polygon count), step 2: the Polygon count entry says 'Three tallies of one mesh', but the chart beside it is titled 'FOUR TALLIES OF THE SAME CUBE' and the note says 'One mesh, four numbers'.
- Slide 10 (Units and the right-handed +Z up axes): the TELL THESE APART box sets 'Right-handed' against 'Y up (Godot)' as if they were opposites. Handedness and the up axis are separate properties, and Chapter 3 says Godot is right-handed too ('Godot is right-handed and Y-up'). The narration says Godot is right-handed as well.
- Slide 10 step 2 prints 'extents 0.2, 1.8, 0.2' and 'extents 0.2, 0.2, 1.8' for full sizes. The course glossary defines Extents as 'The half-sizes of a bounding box', so by that definition these are sizes, and the extents would be 0.1, 0.9, 0.1. The narration says 'Z extent' only as the slide's note and slide 14 do.
- Slide 13 step 2 (pair 2): Size is defined as 'The real dimensions in the mesh', but the picture shows 'size 1.00 m' worked out as 'scale × mesh = what you see' while 'the mesh is still 2 m'. By the printed definition the size in the mesh would be 2 m. The narration says 'the real dimensions you end up with' and leaves out 'in the mesh'.
- Slide 9 step 1: the grey divider line in the table runs through the red 'Size you see (m)' row, so that row looks struck through.
- Slide 9 step 1: the Apply transforms entry says 'Bake position, rotation and scale', but Chapter 3 and slide 14 step 4 apply Rotation & Scale only (the chapter's script passes location=False).
- Slide 12 step 3: the red curve from the checker texture runs across the label '← filled by the texture', striking it through. The image slot it points to stays an empty box.
- Slide 13 step 1 (pair 1): at the end of the step both turned squares overlap their own captions ('origin: the object's own point', 'pivot: set to a corner here'), so the captions are hard to read. Slide 13 step 4: the three unlabelled bars under 'colour, roughness, metal…' end with metal at about 0.8, while slide 12 step 3 shows Metallic 0.0.
- Slide 4 step 2 and slide 5 steps 2 to 4: the hidden back corner of the cube is drawn as a dot on top of the front face, so a vertex seems to float in the middle of a face (most visible at slide 5 step 4).
- Slide 4 step 1: the caption 'All 8 vertices moved together, 5.9 units' sits next to the note 'the mesh is untouched'. In Object Mode only the object's location changes, so 'vertices moved' can read as an edit to the mesh. The 5.9 is a screen distance (410 px over a 70 px drawing scale), not a value Blender would report.
- Slide 11 step 3: the picture is one face's outline whose corners double each level (4, 8, 16), but the labels under it give the whole cube's face counts (6, 24, 96). A viewer can take '24 faces' as the count for the one drawn outline.
- Slide 5 step 1: the Mesh entry and its note say 'the chapter calls it mesh data' and 'what the chapter means by mesh data'. In a standalone film there is no chapter on screen.

## Open after the second pass

- slide 10 step 2 and slide 14 step 3: the slide prints full sizes (0.2, 1.8, 0.2) as 'extents' and the course glossary defines Extents as half-sizes of a bounding box; the narration says 'Z extent' of one point eight only in Chapter 3's own sense ('puts Blender's Z extent on Godot's Y') and never speaks the slide's 'extents' line, so it is left as is, but the deck label should be checked.
- slide 9 step 1: the on-screen Apply transforms entry (and the course glossary) still read 'Bake position, rotation and scale', while the narration now follows Chapter 3's rotation and scale; the deck entry and glossary row may need aligning with Chapter 3.
