# LANE-PLAN.md — suggested pictures, per beat

SUGGESTIONS, not orders. The BEST-BEAT LAW decides: audition at least two lanes per beat, pick the one whose MOTION is the beat's claim, write the pick and the
runner-up in your lanes file. Where a real capture or a real log exists, it wins over a drawing of the same thing (SHOW-THE-THING LAW). Evidence file names are
in `EVIDENCE-INDEX.md`. Numbers on screen come from the evidence logs, never from memory.

Real numbers already confirmed (Blender 5.1.2, `evidence/primitives/tris.log`): cube 12 · plane 2 · default cylinder 124 · default cone 62 · default UV sphere 960 ·
sphere 12 segments x 6 rings 120 · cylinder with 12 vertices 44 triangles.

Builder assignment: one builder per act, 7 in all (I, II, III, IV, V, VI, VII).

## ACT I — Three Simple Assets (B01–B14)
| Beat | About | Suggested lane (runner-up) |
|---|---|---|
| B01 | the job; the three assets; (carries the ACT title) | Manim: the three REAL renders (crate, lantern, coin) arrive on cream, one label each (iso props as runner-up) |
| B02 | Claude drives Blender via MCP; you stay in the loop, one hand edit | Manim diagram: Claude → MCP → Blender (real Blender icon), a terracotta hand-edit mark loops back (iso blocks) |
| B03 | prop, environment, collectible | iso drawings of a crate, a tree/rock, a coin (LibraryIconRow) |
| B04 | simple = basic shapes; no sculpting/textures/rigging/animation | Manim: cube, cylinder, cone, sphere, plane assemble into the real lantern; four struck-out labels |
| B05 | budget: six shapes, 500 triangles | Manim: a cube's real 12 triangles outlined, two hero numbers |
| B06 | the trap: 12 / 124 / 960 vs 500 | Manim bar chart, real numbers, the 500 line ringed |
| B07 | lower segments: 960 → 120 | the real image `ev_sphere_default_vs_low.png` with camera moves (Manim ImageMobject) |
| B08 | one game, layers, tag a3 | Manim: layers stacking, the third tagged; no dates |
| B09A | 2D game still makes three assets; a small 3D scene | iso: a flat 2D game card next to a small 3D stage |
| B09B | floor, one light, camera, three assets | iso stage drawing with the three props (runner-up: the real Godot screenshot) |
| B10 | later assignments reuse the scene | Manim: arrow from the scene to later layers; the real Godot showcase screenshot |
| B11 | the tools (Claude Code, Blender, the add-on), free | each tool as itself: Claude Code skin (CC kit, nothing typed), the real Blender window crop, the add-on shown by its README line |
| B12 | you build it; downloaded / AI-generated mesh doesn't count | Manim two-up: the crate built from shapes (kept) vs two struck model sources |
| B13 | services off | Manim: six switches, all off, named from the README (`evidence/mcp/`) |
| B14 | watch the AI policy video | the real video page (BrowserCapture) or a card with the real title (runner-up) |

## ACT II — Learn the Window First (B15–B20): real captures
| Beat | About | Suggested lane |
|---|---|---|
| B15 | orbit, pan, zoom (carries the ACT title) | cross-fade `ev_bl_orbit_1..3.png` with three gesture marks |
| B16 | the 3D viewport | `ev_bl_object_mode.png`, push in to the viewport, one terracotta ring (boxes in `evidence/gui/NOTES.md`) |
| B17 | toolbar, Outliner | the same window, rings on each as spoken |
| B18 | Properties editor, the sidebar (N): location, rotation, scale, dimensions | rings, then a hard zoom on the sidebar's Item panel |
| B19 | the mode selector, Object vs Edit | `ev_bl_object_mode.png` → `ev_bl_edit_mode.png`, ring on the header selector |
| B20 | one screenshot in a notes file | a document skin of `BLENDER-NOTES.md` with the six part names as headings (a template, labelled) |

## ACT III — Write the Brief Before You Build (B21–B28)
| Beat | About | Suggested lane |
|---|---|---|
| B21 | commit the brief first; keep the original | Manim: a file `CHANGE-BRIEF.md` committed, then a revision added beside it, the original kept |
| B22 | name / what it is / where it appears | Manim table row for the crate (example values, labelled) |
| B23 | size in metres, justified | Manim: the real crate dimensions with dimension arrows beside a labelled example player |
| B24 | one unit is one metre in both | Manim: a ruler, Blender "1 unit" = Godot "1 unit" = 1 m |
| B25A | origin: centre of the underside | Manim side view of the crate, a terracotta DOT at the base centre |
| B25B | build around the world origin | the world origin axes at the floor, the crate on it |
| B26A | origin in the middle: at floor level it sinks half its height (real gap -0.4 m); lifted by a guess it floats (real +0.1 m) | Manim: three crates in side view (centre origin sinks; lifted by a guess floats; base origin sits), the real gaps from `evidence/godot/demo_iii_*.log` |
| B26B | lifted exactly by half its height it sits, but only because you moved it; check the origin itself | Manim: the lifted crate passing the gap check, then the origin check failing it ("the origin is 0.4 m above the base"), real lines from `evidence/godot/demo_iii_crate_origin_centre_lifted_origin_check.log` |
| B27 | look and budget | the real lantern render with its real triangle count and colour chips |
| B28 | three predicted failures and their checks | four small failure panels (lying on its side, 10x wrong, server won't connect, colour lost), each with a check mark |

## ACT IV — Connect Claude to Blender (B29–B40)
| Beat | About | Suggested lane |
|---|---|---|
| B29 | the MCP route: add-on, socket, server | iso drawing: Claude Code block, server block, Blender block, a socket line between (the kit's `mcp`/`server` props) |
| B30 | the course hasn't run it; README as recorded 27 Sep | the README as the project's own words (document skin) or BrowserCapture of the public repo page; on-screen "documented, not run" |
| B31 | 6 Oct README leads with a one-line installer; use the manual steps | the real README text from `evidence/mcp/readme-219.md` (quote ≤ 15 words), the manual steps ringed |
| B32 | step one: uv via Homebrew | `CCPlainShell`: `brew install uv`, no output, "documented, not run" |
| B33 | step two: register the server | `CCPlainShell`: the `claude mcp add ...` line from the assignment, no output |
| B34 | step three: the add-on; Edit > Preferences > Add-ons | `CCPlainShell` for `uvx mcp-for-blender install-addon`, then the real Preferences capture (`ev_bl_prefs_addons.png`) |
| B35 | the add-on starts its server; check the tab; services off; fresh session | the README's own words (document skin); never a drawn add-on panel |
| B36 | safety: no authentication or encryption | a Manim open port/door, plus the README sentence quoted (≤ 15 words) |
| B37A | localhost, save first, turn the add-on off | three marks (LibraryIconRow) or a Manim checklist |
| B37B | don't open files from people you don't trust | one Manim picture: a file approaching a port that is open |
| B38 | two-hour time box; the script route | Manim: a clock ring for two hours, each attempt logged, a fork to the script route |
| B39A | the three flags of the command | `CCPlainShell` with the REAL command and REAL output from `evidence/assets/build_*.log`; each flag ringed as spoken |
| B39B | python-exit-code one: 0 vs 1 | the REAL exit-code logs from `evidence/exitcode/`: two shell lines, `0` then `1` |
| B40 | an honest failed attempt earns up to 6 of 8 | Manim: a bar of 8 points, the bracket at 6 |

## ACT V — Build the Assets (B41–B49)
| Beat | About | Suggested lane |
|---|---|---|
| B41 | plan first; the prompt | `ClaudeCodeBeat` listing of the assignment's prompt (a document, labelled "adapted prompt, not run") |
| B42 | get scene info; propose; don't build yet | the same listing with the lines ringed, then a Manim step chip |
| B43 | one execute-code call per object; report; apply; show | Manim: the loop's steps as chips, one object at a time (lantern shapes appear one by one from the REAL build log) |
| B44 | forbidden downloads and generation tools; "say what you could not verify" | the listing's forbidden-tools lines, ringed |
| B45 | tool names drift: 2.1.1 vs 2.1.9 | Manim two-column table from `evidence/mcp/README-FACTS.md`, three struck, one added |
| B46 | look yourself | a real render of the lantern, an eye mark, the voice's "Claude can't tell you" |
| B47 | one hand edit | `ev_bl_hand_edit_before.png` → `ev_bl_hand_edit_after.png`, labelled illustrative |
| B48 | save the code, one script per asset | the REAL start of `evidence/assets/build_lantern.py` on `ClaudeCodeBeat`, the folder `tools/blender/` |
| B49 | save the .blend; .blend1 backups; don't commit those | the REAL `ls -la` from `evidence/assets/ls_blend.log`, `.blend1` ringed, then `.gitignore` |

## ACT VI — Export, Import, Check (B50–B60)
| Beat | About | Suggested lane |
|---|---|---|
| B50 | export as GLB; +Y Up on by default | the REAL `ev_bl_export_gltf.png`, ring on +Y Up |
| B51 | Blender Z up, glTF/Godot Y up | Manim: axes turning; the REAL numbers for the lantern with +Y Up on and off from `evidence/godot/` |
| B52 | the newer add-on has no export tool; two routes | the real File > Export menu crop and the one-line alternative |
| B53 | files into Godot; import; the little scene | the REAL import log and the REAL Godot showcase screenshot |
| B54 | the headless script prints size, scale, axis | `CCPlainShell`: the REAL command and the REAL printed table from `evidence/godot/` |
| B55 | compare with brief and with Blender's sidebar | Manim table: asset / Blender dims / Godot box / node scale, the matching row ringed (real numbers) |
| B56 | sit, sink or float: the origin check; moving the node hides the problem | Manim: the three gap values from the real runs (0.0 / -0.4 / +0.1) and the origin check's real verdict line |
| B57 | triangle count; Scene Statistics | the REAL `ev_bl_status_stats.png`, ring on the count; the three assets' counts vs 500 |
| B58 | a check can prove less than it claims (a recorded case) | Manim: a ray that stops on the object's own collider (the recorded case, labelled; numbers from `examples/03.../README.md`) |
| B59 | the human check: behind, below, size, missing faces | the REAL renders `ev_lantern_back.png`, `ev_lantern_below.png`, camera moves |
| B60 | one revision from something you saw; commit message example | Manim: before/after numbers from the real wrong-size demonstration; the assignment's own example commit message |

## ACT VII — Ship It, and How It's Graded (B61A–B69)
| Beat | About | Suggested lane |
|---|---|---|
| B61A | the film: game, assets, real Blender session, prompt, hand edit | Manim: four tiles built from real evidence images |
| B61B | the assets in the Godot scene with headless numbers beside the brief | the REAL Godot screenshot beside the REAL printed numbers |
| B62 | what you checked / uncertain / Claude got wrong / human vs AI | Manim ledger of four columns |
| B63 | GitHub, the tree, tag a3, don't move it | `CCPlainShell` with the REAL `git` output from `evidence/git/` (`git ls-files`, `git tag a3`, `git log --oneline --decorate`) |
| B64 | verify from a clean clone | `CCPlainShell`: the REAL `git clone` / `git checkout a3` output |
| B65 | the submission note | document skin of the SUBMISSION.md fields (the assignment's own template, labelled) |
| B66 | 60 / 10 / 10 / 20 | Manim stacked bar, an 80 bracket, the 20 ringed |
| B67 | the split of the 60: 10 / 14 / 18 / 10 / 8 | Manim: the 60 bar split in five |
| B68 | late work; be able to explain | Manim: -10% per day; the real Blender sidebar crop with rings on size, origin, scale |
| B69 | a passing check is not a judgment of the look | Manim: two columns, "a check shows" vs "only you judge"; the real Godot screenshot |

Bookends (BIDEA, BDEFS, BVDT, BHTF, BOUT) are built by `make_sheet.py`, not by you.
