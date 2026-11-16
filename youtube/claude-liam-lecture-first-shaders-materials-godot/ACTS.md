# ACTS.md — coverage map

Source: the whole of **Assignment 5, "Shaders, Materials, and the Godot Shading Language"** (CSYE 7270, Fall 2026, 100 points): `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/assignments/05-shaders-materials-and-godot-shading-language.md` (byte-identical to `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/assignments/course-briefs/05-shaders-materials-and-godot-shading-language.md`; read in full 2026-10-16; copy in `evidence/example/sources/assignment-05.md`). Bear asked for a film that walks people through this assignment, using his project (the instructor example in `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/`) as the evidence.
Film: **Your First Shaders and Materials with Claude and Godot** — channel claude-liam (Liam, in for Bear, Kokoro `am_onyx`), skill `lecture`, @NikBearBrown. A film made FOR a course: `metadata.course` is set; the course is named in BOPEN (the playlist name) and BIDEA only. Beats BOPEN, BIDEA, BDEFS, B01–B74 (with B55B), BVDT, BHTF, BOUT = 81 beats. NO video numbers anywhere: the assignment's own number appears only as "the fifth assignment" in BIDEA, copying how the Assignment 3 film speaks (the title carries no number).
The acts follow the assignment's own order: the task and its four ideas, **1. Predict**, **2. Build It** (the wrapper and agent rules, Step 2 the shader from code, Step 3 the textured shader / hint experiment / normal-map check / audit, Step 4 the language, "what the agent gets wrong", "what must not change, done means"), **3. Use It**, **4. Ship It** + **5. Verify and submit** + the rubric + "You must be able to explain it".

| Act | Title | Beats | Source sections covered |
|---|---|---|---|
| I | Two Shaders and Their Materials | B01–B08 | Executive summary · Your task: items 2–4 (what a shader is, what a material is, what a texture is, what the Godot shading language is) and the four ideas · Who writes what · Rights and provenance · the honest disclosure about the instructor example (CHANGE-BRIEF of the example: "the film must explain that distinction") |
| II | Predict Before You Write | B09–B18 | 1. Predict: commit CHANGE-BRIEF.md first · the state · the effect specification (path, type, uniforms, the colour line) · observable rules (values, timing at 30/60/144, retrigger) · boundaries and the evidence split · controlled inputs and predicted values (by hand) · the hint experiment's predictions (encode function; Forward+/Mobile vs Compatibility) · the material plan · at least three predicted failure cases · the five short questions |
| III | Give the Agent Rules | B19–B24 | 2. Build It: the test wrapper (timeout, --fixed-fps, log, fail on SHADER ERROR / SCRIPT ERROR; exit 124) · the baseline · after every agent session (final result event; `git diff --stat godot/shaders/`) · Step 1 CLAUDE.md (draft, imports @CHANGE-BRIEF.md, under 120 lines; commit unedited, review separately; the scoped `claude -p` command and why git is read-only) |
| IV | The Shader From Code | B25–B34 | Step 2: hand-write the shader from the spec (colour line exact; revise the spec first; reimport; commit alone; TIME is global) · direct the driver and its test, plan first (the prompt) · the driver line · the test · 30/60/144 · what headless cannot show · mutate twice (semicolon, rename) |
| V | A Shader That Reads Textures | B35–B39 | Step 3: textures and import settings set explicitly · colour vs data textures (`source_color`) · the textured `spatial` shader (≥ 2 samplers, ≥ 4 uniforms with hints/defaults, ≥ 2 `group_uniforms` groups) · two `ShaderMaterial` resources from one shader · Use External for an imported scene |
| VI | Textures Are Information | B40–B48 | Step 3: the hint experiment (built, Compatibility result, Forward+ result) · a texture is information · the normal-map check (curl ratio; calibrate on a Poly Haven `_nor_gl`/`_nor_dx` pair; what it cannot tell you) · the audit (MATERIALS.md + test_materials) · fresh `.godot` cache and the `source_color` mutation |
| VII | Read the Language | B49–B55, B55B | Step 4: convert a `StandardMaterial3D`, save the generated shader, give line numbers · the eight language questions (shader_type; processor functions; built-ins; hints; hint_range clamp; the colour/data line; neighbour fragments and uniforms; what Godot adds over GLSL) · "What must not change, and what counts as done" |
| VIII | What the Agent Gets Wrong | B56–B58 | The "what the agent is likely to get wrong" table (five recorded mistakes) + the example's own recorded mistakes |
| IX | Check What You See | B59–B68 | 3. Use It: every row of the report table (baseline, shaders parse, driver, controlled values, in play, hint experiment, interface sweep, one shader two materials, material wiring, texture data, import settings) · in-engine capture, not OS screenshots · a difference of more than a step or two is a finding · one inspect-and-revise cycle · your own playtest is required · what the example did not do |
| X | Ship It, and How It's Graded | B69–B74 | 4. Ship It: the one required film (seven things), labelling reconstructions · the GitHub contents · commit order and the `a5` tag · 5. Verify (clean clone) and submit (source ZIP + SUBMISSION.md) · Rubric (100 = 60 + 10 + 10 + 20; the 60-point split 8/12/14/10/8/8) · late penalty · "You must be able to explain it" · the integrity paragraph · the required AI-policy viewing |

## LEFT OUT (with reasons) — nothing is dropped silently
| Source text | Reason |
|---|---|
| Header: "10-day cadence", "10% daily late penalty" wording, "Covers: Module 6 … Module 7 and their chapters" | Course scheduling and module numbering: not self-contained. The late penalty IS spoken (B73). |
| "Required viewing: [AI Policy …](link)" as a separate item | A pointer to a video; its point (say what the AI did, be able to explain) is spoken in B06 and closes the film (B74: "watch that video"). |
| "Your game, one more layer": repository named `walker-…`, individual work, "one change of game … before Assignment 4", "if your game is 2D do parts 3 and 4 in the 3D scene" | Course administration that applies to enrolled students only; the tag `a5` is spoken in B70. Left to the written assignment. |
| "What counts" table, row by row (the `canvas_item` option; "at least two uniforms each with a type, a hint and a default"; AGENTS.md first-line rule; "two materials differ in at least two values or one texture") | The minimums are shown in the example's own files (B11, B23, B26, B37, B39) and spoken where they teach; the table is a checklist for the written assignment. |
| Rights: "generated textures follow Assignment 2's rules"; "walker-jumpman-clawd's SOURCES.md … public availability is not a licence grant" | Course rules for other assignments; B08 teaches the general rule (credit every texture, show the code). |
| Predict: HDR 2D / contrast ratio; "what the renderer rules out" (decals, VoxelGI, SDFGI, SSIL); "what the effect does while paused / if the state ends early / several instances" | Conditional or detail items; spoken in outline (B13, B18); the example's test checks pause, reset and early interruption (B31). |
| Build It: the four public Walker projects; `brew install coreutils` for `timeout`; "Codex reads AGENTS.md, not CLAUDE.md" | Pointers and platform/tool asides. |
| The `curl_ratio` GDScript listing; "use a stride of 8 on 4K textures" | The idea and the real numbers are taught (B44–B46); the listing is the assignment's own code. The example ran stride 2 on a 1k pair (caption). |
| Step 3: "Make two ShaderMaterial resources as .tres … place them in your 3D scene" beyond B39; "A WorldEnvironment sets a Linear tonemap…" | Shown on screen in B40–B42 (the re-run's fixture sets it; the example's own fixture has none and says so). |
| Ship It: "Use the Walker opening/summary and Verdict → Your Turn → regular outro"; "no minimum runtime; no Short; no paid media"; the full GitHub inventory incl. the film's own beat sheet and evidence records; reviewer-access test | The film's own spine and workflow rules; B70 lists the inventory in outline. |
| 5. Submit: the `SUBMISSION.md` template, field by field; "put the final SHA in the Canvas note; both revisions" | Spoken in outline (B71); the field list is a form. |
| Rubric prose: Frictional 3/3/2/2 bullets, GitHub 4/3/3, Relative Quartile wording ("meeting the criteria can earn the other 80") | Administrative detail repeated in every assignment; the totals and the 60-point split are spoken (B72). |
| "Use SOURCES.md to credit …" and the three-sentence "describe what AI contributed" paragraph | Documentation duties; the authorship rule is spoken (B06, B74). |

## BIDEA correction and BDEFS
- BIDEA types "The tests pass, so the shader looks right." and corrects `so the shader looks right` → `so the shader is wired, and my eyes judge the look` (the assignment's own thesis: "A passing headless run proves … It proves nothing about what the screen shows").
- BDEFS (6 terms, prerequisites only): GPU · pixel · uniform · renderer · headless · mutation. Shader, material, texture and the Godot shading language are the four ideas the film earns in Act I, spoken in their act.

## Cast per act (the same object is the same picture within an act)
| Act | Recurring objects |
|---|---|
| I | The real pad frames (terracotta striped pad turning green; Claude on it) and the two real spheres (matte, coated); a pixel grid for the shader idea. |
| II | The 11-line `signal.gdshader` with its colour line ringed; the pad crop; one dark-stripe pixel carried through the hand arithmetic. |
| III | The wrapper script; the example's real terminal logs (one terminal window skin); the commit chain. |
| IV | The same 11 lines, lit a few at a time; the pad; the E key; three frame-rate rulers. |
| V | `surface.gdshader` (14 lines); the two textures (colour stripes, roughness greys); matte and coated spheres. |
| VI | The 3 x 1 grey file read two ways (the real bands); the Poly Haven pair; a number line 0 / 1 / 2. |
| VII | `standard_generated.gdshader` (48 lines) beside the example's three shaders; the corner/pixel diagram. |
| VIII | The assignment's table rows; one drawn test-vs-summary pair. |
| IX | The real pad captures at 0 / 0.5 / 1 / 2 in both renderers; the real lab frames; the spheres. |
| X | The repository, the commit chain, the `a5` tag on a string; the 100-point bar. |
