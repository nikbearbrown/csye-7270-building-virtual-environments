# ACTS.md — coverage map

Source: `assignments/03-first-3d-assets-with-blender-mcp.md` (the whole assignment, read in full 2026-10-06; Bear pasted the same text with the request "Use the lecture [skill], Liam persona, to make a film on this").
Film: **Your First 3D Game Assets with Claude and Blender** — channel claude-liam (Liam, in for Bear, Kokoro `am_onyx`), skill `lecture`. A film made FOR a course: `metadata.course` is set and the course is named once, in BIDEA. Beats BIDEA, BDEFS, B01–B69 (with splits), BVDT, BHTF, BOUT.

The acts follow the assignment's own order, including its instruction to learn Blender's window BEFORE writing the brief.

| Act | Title | Beats | Source sections covered |
|---|---|---|---|
| I | Three Simple Assets | B01–B14 | Executive summary · Your task: the three assets, "what simple means" (shapes, no sculpting/textures/rigging/animation), the budget (six shapes, 500 triangles), the cumulative game and tag `a3`, "your game does not have to be 3D" + the small 3D scene, tools and cost, rights and provenance, required viewing (AI policy video) |
| II | Learn the Window First | B15–B20 | 2. Build It → "Learn the window": orbit/pan/zoom, the six interface parts, the sidebar (N), the mode selector, the one screenshot |
| III | Write the Brief Before You Build | B21–B28 (B26 split A/B) | 1. Predict: `CHANGE-BRIEF.md` — the three assets, size in metres, origin, look, budget, at least three predicted failures |
| IV | Connect Claude to Blender | B29–B40 | 2. Build It → "Connect Claude to Blender": how the MCP works, "the course has not run this route", the 2.1.1 → 2.1.9 drift, the manual steps (uv, `claude mcp add`, add-on), the checks, the safety note, the two-hour time box, the script-route fallback and its command, the 6-of-8 credit rule |
| V | Build the Assets | B41–B49 | 2. Build It → "Build the assets, one at a time": the plan-first prompt, the tool calls, forbidden services, tool-name drift, look yourself, one hand edit, save the code, save the `.blend` |
| VI | Export, Import, Check | B50–B60 | 2. Build It → "Export and place them in Godot" · 3. Use It: the checks table (size, upright and scale, origin, triangle count, imports, HUMAN CHECK, what Claude got wrong), the revision cycle |
| VII | Ship It, and How It's Graded | B61–B69 | 4. Ship It (the film, GitHub, tag) · 5. Verify and submit (clean clone, `SUBMISSION.md`) · Rubric (60/10/10/20 and the 60-point split) · You must be able to explain it · the closing caution (a passing check is not a judgment of the look) |

## LEFT OUT (with reasons)

| Source text | Reason |
|---|---|
| Header: "Suggested Canvas due date: Day 30"; "Covers: Module 3 …"; "Module 4 runs alongside it" | Course scheduling and module numbering: not self-contained, and Canvas holds the dates. The late penalty IS spoken (B68). |
| "Read first: the Module 3 lesson … Chapter 3" | A pointer to course reading the viewer is assumed not to have. Everything that reading teaches that the assignment relies on (metres, +Y up, applied transforms) is taught on screen where first needed. |
| The three grading paragraphs in full (Frictional 3/3/2/2 bullets; GitHub posting 4/3/3; Relative Quartile wording) | Administrative detail repeated in every assignment. Their totals are spoken (B66, B67). Left to the written assignment. |
| The `SUBMISSION.md` template line by line | Spoken in outline (B65); the full field list is a form, not an idea. |
| The macOS-only note and Homebrew `coreutils` for `timeout` | Platform detail for the headless check; the check itself is taught (B54–B56). |
| The `git clone … ../a3-check` / `git checkout a3` commands | Spoken as the verification step (B64); the two commands are standard git. |
| §4 item 4 in full ("one next step", "the source revision shown") and "why your game needs each" asset | Administrative detail of what the film must contain; B61A/B62 speak the four headline items. Left to the written assignment. |

## BIDEA correction and BDEFS

- BIDEA types "The AI makes the models, so I just accept whatever it makes." and corrects `so I just accept whatever it makes` → `and I direct it, measure it, and judge it`.
- BDEFS (6 terms, prerequisites only): asset · MCP · .glb · origin · triangle budget · bounding box. Concepts the film earns in their act (units, +Y up, applied transforms, headless) arrive in the act, spoken.

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I | The three real assets (crate, lantern, coin), shown as real Blender renders. |
| II | The real Blender window (one session: lantern selected, sidebar open). |
| III | The crate with its dimension arrows; its origin as a terracotta dot. |
| IV | Three blocks: Claude Code, the server, Blender with its add-on; the socket as the line between them. |
| V | The lantern as it is built, shape by shape; the loop of plan, approve, build, look, hand edit, save. |
| VI | The three assets together, in Blender, in the Godot scene; the numbers the check prints. |
| VII | The repository, the `a3` tag, the film file; the 60 / 10 / 10 / 20 split. |
