# LANE-PLAN — Film 3: "What Is Walker, and Why"
Read `../_conducting-series-evidence/BUILDER-BRIEF-COMMON.md` first. One builder per act (acts 1–6). Beat ids and narration: `narration.py`. Rules with exact quotes: EVID/research/walker-brief.md section 2 (verbatim, path:line) and EVID/walker-evidence/ANALYSIS.md.

## Honesty rules for THIS film
- Walker is rules and a habit, NOT enforcement. Gates are conventions (W/docs/zelda-gdd-workflow.md:64). No `walker gdd` CLI exists; no test framework ships.
- The installed Godot guide is C# (godot.md:3); the example games and the installed /gdd skill default to typed GDScript (gdd/commands/p3.md:6). The GDScript conventions are a copyable research prompt, NOT installed. Show both sides of the disagreement.
- Run A (working tree) installs 54 files incl. /gdd; the COMMITTED public HEAD 10fedb8 installs 11 files and no /gdd (ANALYSIS.md section 6). Say "as of 9 October 2026".
- No human finding exists in the Clawd records; the play-test is "pending"; gates are null/unsigned. Do not invent one.
- Godogen: MIT, copyright holder Alex Ermolov per W/LICENSE.md; do not call him "the author" on screen beyond what the file says; never show the student-submission licence file or its name.
- Show quotes <= 15 words, attributed to the file and line.

## Act 1 — The Problem Walker Answers (B01–B04)
- B01 github-walker.png (real repo page) + three nouns: instructions, tools, a way of working. B02 the sentence from W/legacy/README.md:5-6 as a large quote card. B03 the legacy Unity idea: agent works the text, human works what only a human can safely touch (a two-column drawn membrane) + "the tooling does not exist yet" (W/legacy/AGENTS.md:7). B04 Godogen attribution: LICENSE head (MIT, 2026) + CHANGELOG line, and the added /gdd skill (2026-09-18).
## Act 2 — The Loop and Who Decides (B05–B07)
- B05 the six-step loop as a moving circle (Game brief → Build → Play-test → Inspect → Revise → Export) with real captures per step from walker-claude. B06 the table output/boundary per step (W/docs/zelda-gdd-workflow.md:37-44). B07 the two-line split with the real quote (W/README.md:5-6).
## Act 3 — What the AI Must Not Do (B08–B13)
- One rule-group per beat, each rule quoted verbatim <=15 words with its file:line: scope (rules 2,3,11,12), drafting vs approval (12,75), the four gates vision/systems/world/scope (73–74; show the real DESIGN-STATUS.json gate_approvals nulls from C/design/DESIGN-STATUS.json), proof (42,47,49,50), money and safety (57–66), size (15). Mark each rule with where it lives: installed [I] / framework doc [D] / game's own file [G] (legend in walker-brief.md).
## Act 4 — How the AI Writes Code (B14–B17)
- B14 the installed godot.md (EVID/walker-evidence/installed/claude/godot.md) as real text: the build gate, verify rule, running-game rule. B15 the GDScript conventions (godot-scripting-conventions-research-prompt.md lines 134-168) as four icons + real lines. B16 the split screen: godot.md:3 (C#) vs gdd p3.md:6 (typed GDScript) vs the real project.godot of walker-claude (no .NET) — the contradiction, side by side. B17 "a prompt you can copy" vs "installed": the installed-tree listing with no GDScript file.
## Act 5 — Walker in Action (B18–B23)
- B18 the REAL publish run: publish.log (5 lines) + installed-tree.txt counts (54 files, 127,260 bytes), recorded 2026-10-09, terminal skin labelled "recorded run". B19 the 12-line manifest (installed/claude/CLAUDE.md) as Menlo text, with lines highlighted in turn. B20 walker-claude with the three predictions on cards and scope "drawing only" (C/CHANGE-BRIEF.md). B21 the arms-past-edge frame: use the real walker-claude capture (state which frame) and the FRICTIONAL.md:59-63 line. B22 the 343/540 receipt and the exit-0/no-receipt take (real receipt JSON excerpts) with "preserve failed receipts" (C/AGENTS.md:16). B23 the pending list: CLAWD-STATUS.json lines 12-16 + signed_by null.
## Act 6 — What Walker Is Not (B24–B26)
- B24 DESIGN-STATUS.json as an editable file (an agent could edit it): draw the file with the gate fields and the quote from zelda-gdd-workflow.md:64. B25 two lists: "specification, not built" (walker gdd CLI, test framework) and "committed vs working tree" (11 vs 54 files, dated 2026-10-09). B26 the habit as five verbs: predict, change one thing, run the real game, keep failed receipts, leave judgment to the human — each a real exhibit from Act 5.
