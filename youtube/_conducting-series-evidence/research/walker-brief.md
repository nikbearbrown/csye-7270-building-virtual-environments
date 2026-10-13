# Research brief: Walker (Film 3, "What is Walker, and why")

Read-only research. Everything quoted is exact from the files. "INFERRED" marks my reading, not the files' words.
Short names used below:
- W = /Users/bear/Documents/CoWork/bear-textbooks/books/walker
- C = /Users/bear/Documents/CoWork/bear-textbooks/books/walker-jumpman-clawd

`./publish.sh --help` was run (the only command run). It only prints the script's own header comment (publish.sh:1-10). It writes nothing.

---

## 0. The one fact that decides how Film 3 can be told (INFERRED, but checkable)

The installed rules are few. `publish.sh` installs only these into a game:
- a 12-line runtime manifest (W/prompts/runtime.md)
- one engine guide (W/engines/<engine>.md)
- the `asset-gen` skill (W/asset-gen/)
- the `gdd` (Zelda) skill (W/gdd/)
- a `.gitignore` (W/publish.sh:99-158)

Most of the rest of "Walker" is prose in docs, prompts and research files. It is NOT copied into a game:
- W/docs/*
- W/prompts/zelda-gdd.md (marked superseded, W/prompts/zelda-gdd.md:1)
- the two Godot research prompts and the asset report

The sharpest "must not" rules are therefore split across three places:
1. the framework docs (read by humans),
2. the installed `gdd` skill and engine guide,
3. a hand-written AGENTS.md inside each game. C/AGENTS.md is hand-written. C has no `.claude/` directory and no publisher-made CLAUDE.md. Check: `ls -a C | grep -i claude` returned nothing but AGENTS.md.

So for Film 3 the true statement is: Walker is the rules plus the habit of a loop. Walker is not a program that enforces the rules.

---

## 1. What Walker is and is not (the files' own words)

IS:
- W/README.md:3-6: "Framework instructions and tools for building games with AI agents. Walker's working loop is **Game brief → Build → Playtest → Inspect → Revise → Export**. The agent helps execute and check changes; the human decides what the game should be and whether it feels right."
- The working loop appears again as a table, W/docs/zelda-gdd-workflow.md:37-44. Each stage has an output and a boundary. Example: Build → "Runnable project plus implementation map, not a completion claim". Export → "Versioned package and evidence; publication remains separate".
- W/AGENTS.md:8: "This repository is not a published game repo. It is the source that `publish.sh` renders into a runtime game repo for a chosen engine and host agent."
- W/README.md:32-35: "`publish.sh` installs an agent manifest, an engine guide, and the `asset-gen` skill. It does not create a playable game or implement the entire development loop automatically."
- Who decides what (W/docs/zelda-gdd-workflow.md ties it to Zelda; W/prompts/zelda-gdd.md:54): "Human designers own player intent, scope, tradeoffs, and approval. AI can draft, compare, implement authorized changes, and run tests."
- The same line continues: "Humans determine whether the game communicates, feels fair, and is enjoyable."
- Game side, C/CHANGE-BRIEF.md:42-43: "AI: code, inspection, test execution, documentation, narrated film production. Human: intent, scope, art judgment, play-feel review, and the next decision."
- Naming: W/prompts/zelda-gdd.md:9: "Every new game project must use a `walker-`-prefixed kebab-case name". W/docs/zelda-gdd-workflow.md:48 attributes this to "Bear's naming requirement".
- Zelda is the design-review persona (W/gdd/persona.md:3-6 and W/prompts/zelda-gdd.md:11): "direct, specific, and willing to challenge a feature that does not serve the player." Note W/prompts/zelda-gdd.md:11 also forbids her from claiming shipping experience or studio employment. The installed persona.md:3-4 still says "20+ years shipping titles". That is a conflict between the old prose and the installed skill (INFERRED).

IS NOT:
- W/README.md:8-10: "This repository contains the framework, not example games, recovered student assets, downloaded Godot demos, or video production workspaces."
- W/docs/PROJECT.md:5 (Godogen-era text): "It is not a game engine, a code generator, or an asset marketplace."
- Not a CLI. W/docs/zelda-gdd-workflow.md:3: "No `walker gdd` shell binary exists; that remains a future adapter."
- Not an enforcer. W/docs/zelda-gdd-workflow.md:64: "Gate validation is a convention the skill follows, not code that enforces it."

Why it exists, and the history (legacy):
- W/legacy/README.md:5-6: "AI made *execution* cheap. It did not make *judgment* cheap."
- The old Walker was Unity-first. W/legacy/README.md:3: "Doctrine and tooling for AI-assisted Unity work ... with a hard line protecting the parts an AI can't safely touch."
- Its two ideas (W/legacy/README.md:9-10):
  - The membrane: the agent works the text layer (C#, config); the human works the asset layer (`.meta` GUIDs, prefabs, scenes).
  - Conformance vs adequacy: "Code that compiles and runs is *conformance* ... Whether the game *feels* right is *adequacy* — only a human playing it can clear that gate."
- Governing principle, W/legacy/AGENTS.md:13: "P1 — machines verify conformance, humans verify adequacy ... The CLI cannot play the game."
- Status in the legacy tree itself (W/legacy/AGENTS.md:7): "Today the repo is **documents**; the `unity/` tooling does not exist yet."
- It was "preserved unchanged" in `legacy/` from commit `3b394be95d49537cb806317f6f617c4ba20e8bf8` (W/README.md:102-105, W/docs/repository-boundary.md:41-49). The framework's own git log: `10fedb8 Publish Walker framework and preserve Unity-first source under legacy`.
- INFERRED, but strong: the current Walker keeps the legacy idea. "A successful build is not evidence of a successful human playtest" (W/README.md:28) is P1 reworded for Godot. The Godot version drops the Unity "membrane" as such.

---

## 2. THE RULES (verbatim, each under 25 words)

Legend: [I] = installed into every published game by publish.sh. [D] = lives in framework docs or prompts only, not installed. [G] = lives in the game's own hand-written AGENTS.md.

### 2a. Scope limits
1. [D] "Every new game project must use a `walker-`-prefixed kebab-case name, such as `walker-jumpman`." — W/prompts/zelda-gdd.md:9
2. [D] "Do not silently use Unity, Bevy, Babylon.js, or a hosted game generator." — W/prompts/zelda-gdd.md:13
3. [D] "Python may orchestrate local tooling, but gameplay belongs in Godot." — W/prompts/zelda-gdd.md:13
4. [D] "Respect an existing project's pinned engine and language." — W/prompts/zelda-gdd.md:13
5. [D] "Games are separate repositories; a framework checkout must not require a game checkout." — W/docs/repository-boundary.md:3-4
6. [D] "Keep framework source and game work in separate repositories." — W/README.md:65-66
7. [D] "Do not use the current publisher on an existing game directory." — W/prompts/zelda-gdd.md:32
8. [I] "Build from `design/GDD.md` feature IDs, not from memory of the chat." — W/prompts/runtime.md:5
9. [I] "Never write design files anywhere else, and never overwrite a human-edited section without saying which paragraphs changed." — W/gdd/SKILL.md:84-85
10. [I] "Unknown command: print the nearest ids and stop; never guess." — W/gdd/SKILL.md:25-26
11. [D] "Do not cut requirements, extend schedules, spend, publish, erase working projects, or change approved targets just to keep a loop running." — W/prompts/zelda-gdd.md:40
12. [D] "Drafting tasks is not authorization to execute them." — W/prompts/zelda-gdd.md:44
13. [I] "Producing a GDD is not producing a game, and a newer GDD does not validate an older build." — W/gdd/persona.md:115-116
14. [G] "Task mini-goals ... are future work. Do not implement them without a new scoped request." — C/AGENTS.md:8-10 (ellipsis mine; the original lists the items)
15. [G] "Make one reviewable change. Predict a failure, preserve unrelated behavior, test, inspect real output, and record actual effort" — C/AGENTS.md:11-12
16. [G] "Change drawing and presentation selection only." — C/CHANGE-BRIEF.md:25
17. [G] "Do not edit or push the sibling walker-jumpman starter." — C/AGENTS.md:3-4
18. [D] The 40% rule: if CORE features exceed 40%, report the numbers and ask. "Never decide unilaterally." — W/gdd/persona.md:70-75 and W/gdd/commands/p1.md:13

### 2b. Code-writing rules

What is installed is a C# guide. The GDScript rules are a proposal plus a copyable prompt.

Installed Godot guide, C# (W/engines/godot.md):
19. [I] "Stack: **Godot 4 (.NET / Mono build)**, **C#**. All Godot C# classes must be `partial`." — W/engines/godot.md:3
20. [I] "`assets/` **only** files the running game loads (keep generation inputs/refs outside it)." — W/engines/godot.md:9
21. [I] "Match version-sensitive fields to the installed toolchain ... don't hardcode values from memory" — W/engines/godot.md:7
22. [I] Scenes are generated, not hand-written. A builder script "contains **no** runtime logic (no `_Ready`/`_Process`, signals, or game state). Build **leaf scenes first**, parents after." — W/engines/godot.md:16
23. [I] "every node must have `Owner` set to the scene root or it won't serialize." — W/engines/godot.md:20
24. [I] "**`SetScript()` disposes the C# wrapper** — set scripts *last*, after the hierarchy is built." — W/engines/godot.md:22
25. [I] "never `CreateTrimeshShape()`/`CreateConvexShape()` on imported meshes (drops to <1 FPS)." — W/engines/godot.md:39
26. [I] "Verify against the installed Godot — read the C# API in the Godot docs/assemblies rather than guessing." — W/engines/godot.md:49
27. [I] "Frame-rate-independent damping: `speed *= Mathf.Exp(-rate * delta)`, not `speed *= (1 - drag)` per tick." — W/engines/godot.md:50
28. [I] "`.gdignore` ... only `screenshots/` should have one, never `assets/`." — W/engines/godot.md:48 (ellipsis mine)

Zelda design profile, typed GDScript (prose, NOT installed):
29. [D] "For a new project, propose Godot 4, typed GDScript, and a 2D greybox first unless the user specifies otherwise" — W/prompts/zelda-gdd.md:13
30. [D] "This GDScript design profile is an explicit proposal, not evidence that that guide or the publisher has been migrated." — W/prompts/zelda-gdd.md:15
31. [D] "Pin version-sensitive APIs against the installed Godot and official documentation before implementation." — W/prompts/zelda-gdd.md:32

GDScript conventions (a copyable prompt; NOT installed; NOT run on any game that I could find):
32. [D] "Use full static typing on all variables, parameters, and return values" — W/godot-scripting-conventions-research-prompt.md:136-137
33. [D] "Never write a script that reaches upward or sideways in the tree with a hardcoded relative path" — W/godot-scripting-conventions-research-prompt.md:151-152
34. [D] "Child-to-parent or outward communication: always a signal ... Never call a method on `get_parent()`." — W/godot-scripting-conventions-research-prompt.md:157-160 (ellipsis mine)
35. [D] "Default to composing small, single-purpose scenes/components ... over deep class inheritance chains." — W/godot-scripting-conventions-research-prompt.md:167-168 (ellipsis mine)
36. [D] Style: snake_case files/functions/variables/signals, PascalCase classes, CONSTANT_CASE constants. — W/godot-scripting-conventions-research-prompt.md:134-135. Wiring: `@onready` for node refs (:147), `@export` for Inspector values (:149).

Scene and asset organisation (W/godot-asset-organization-report.md; a research report, NOT installed). The report itself says (:20-21) "This is a convention, not an engine mandate." It also says (:201) "There is no single community consensus".
37. [D] "Organize around ownership and dependency locality, then preserve the metadata that keeps those dependencies intact." — W/godot-asset-organization-report.md:8
38. [D] "If only one scene or feature uses it, place it with that feature." — W/godot-asset-organization-report.md:274
39. [D] Commit every `.import` and `.uid` sidecar. "Ignore `.import` and `.uid`; Godot will regenerate them" is called "Wrong for teams." — W/godot-asset-organization-report.md:291-292 (the "Commit" list starts at :286) and :325; the "Ignore" list starts at :296 with `.godot/`
40. [D] "Start from a clean commit and make the move its own reviewable change." — W/godot-asset-organization-report.md:306
41. [D] Move a file together with its `.import` or `.uid` companion. Do not copy the sidecar when creating a different resource. — W/godot-asset-organization-report.md:309 and :328 (paraphrase; quote from :328 is "Wrong. Move the sidecar for the same resource; do not copy it...")

Code conflict to name honestly in the film: W/docs/gdscript-vs-csharp.md (written for the 2026-04-06 Godogen migration, W/CHANGELOG.md:34-35) argues for C#: "C# is not easier or harder to write *conceptually* — it's easier to write *correctly*." (:51). The Walker examples and the Zelda profile use GDScript. W/README.md:44-46 says the publisher "does not yet select a GDScript guide." W/setup.md:94 still says "The **.NET edition** is required for Godot projects." The working Walker example needs neither: C/godot/project.godot has no csproj, and C/README.md:73 says "No .NET runtime or external assets are required."

### 2c. Verification rules
42. [I] "Judge progress from the running game, never from a clean build" — W/prompts/runtime.md:10
43. [I] "if the user hasn't seen it running, finish with a 15–20s video of the game in action, and watch it back before you call the work done." — W/prompts/runtime.md:12
44. [I] Build gate: `dotnet build`, then `godot --headless --import` after asset changes, then `godot --headless --quit`. — W/engines/godot.md:10 (paraphrased; exact: "Build gate: `dotnet build`, then `godot --headless --import` after asset changes, then `godot --headless --quit`")
45. [I] "Validate the pack: count nodes before packing, `Instantiate()` the `PackedScene` after, and compare counts" — W/engines/godot.md:21
46. [I] "The clip must show the behavior progressing across the whole window — no dead time, no single looped frame." — W/engines/godot.md:66
47. [D] "A successful build is not evidence of a successful human playtest." — W/README.md:28
48. [D] "Do not mistake a scene tree, compilation success, screenshots, or a recording for a completed human playtest." — W/prompts/zelda-gdd.md:34
49. [D] "Never prefill a result as PASS." — W/prompts/zelda-gdd.md:50
50. [D] Fixing a failed test: propose a design revision "instead of weakening the test to make it pass." — W/prompts/zelda-gdd.md:52 (partial quote)
51. [I] The reverse command tags every claim `[OBSERVED path:line]`, `[INFERRED]` or `[MISSING]`. "Sprites do not prove a mechanic; a script without a scene does not prove a working feature" — W/gdd/commands/reverse.md:24-30
52. [D] "Existing sprites do not prove a mechanic exists; source code without scenes does not prove a working game." — W/prompts/zelda-gdd.md:22
53. [I] Every PX goal, mechanic, system, feature, risk and test gets a stable ID (PX-01, M-01, S-01, F-01, R-01, T-01). — W/gdd/persona.md:48-50
54. [G] "Never invent human playtests, multiple days of work, approvals or test passes." — C/AGENTS.md:13-14
55. [G] "Numeric fixtures and scripted inputs are not human playtesting. Preserve failed receipts." — C/AGENTS.md:15-16
56. [G] "Videos belong in youtube/. Their gameplay must be actual engine output; gallery previews must be labelled." — C/AGENTS.md:21-22

### 2d. Spend and safety rules
57. [I] "Confirm the spend with the user before the first paid generation." — W/prompts/runtime.md:4
58. [I] "These are paid APIs — every call costs real money." — W/asset-gen/SKILL.md:13
59. [I] "Each generation costs real money, so confirm with the user before generating." — W/asset-gen/SKILL.md:92
60. [D] "Asset-generation tools can call paid services. They are optional, require your own credentials, and must not be run without approval for the associated spend." — W/README.md:69-71 (the sentence is ~25 words; shorten to the second half for the screen: "must not be run without approval for the associated spend")
61. [D] "Never commit credentials." — W/README.md:71
62. [I] Do not double-charge: "A timeout ... does **not** mean server failure ... **Do not resubmit — that double-charges.**" — W/asset-gen/SKILL.md:84 (resume with `asset_gen.py resume`, :86)
63. [I] "Review every PNG before any GLB conversion — a bad image wastes 30¢+ downstream." — W/asset-gen/SKILL.md:37
64. [I] The generated `.gitignore` excludes CLAUDE.md/AGENTS.md (the generated instructions), assets, screenshots, `.godot`. — W/publish.sh:136-157. The README tells you to review it first: "Review the generated game's `.gitignore` before publishing it" — W/README.md:66-67
65. [D] "Here, “publish” means **write runtime files locally**, not upload to GitHub." — W/README.md:63. And: "`--force` deletes the entire destination." — W/README.md:65-66. The script does `rm -rf "${TARGET:?}"` at W/publish.sh:88-92.
66. [D] "Uploading to GitHub, itch.io, a website, or an app store is a separate action requiring authorization." — W/prompts/zelda-gdd.md:56
67. [D] "Do not force-push or rewrite history to apply these rules." — W/docs/repository-boundary.md:26-27
68. [D] "reject files over 25 MB." (pre-publication audit; gitignore cannot do size) — W/docs/repository-boundary.md:34-37
69. [G] "Only publish a video when Bear explicitly asks for that publication." — C/AGENTS.md:22-23
70. [G] "inspect staged files for >25 MB." — C/AGENTS.md:19
71. [D] Secrets via environment only: `GOOGLE_API_KEY`, `XAI_API_KEY`, `TRIPO3D_API_KEY`. — W/setup.md:133-137

### 2e. Human-only decisions
72. [D] "the human decides what the game should be and whether it feels right." — W/README.md:5-6
73. [I] Four human gates: vision, systems, world, scope. "Zelda never signs a gate herself." — W/gdd/persona.md:94-96. In the status file, "Gates are signed by humans only." — W/gdd/templates/DESIGN-STATUS.json:13
74. [D] "Agent drafting never signs a human gate." — W/prompts/zelda-gdd.md:38
75. [D] "A direct request for a complete draft authorizes drafting with named assumptions; it does not authorize inventing approvals" — W/prompts/zelda-gdd.md:21
76. [D] "Human designers own player intent, scope, tradeoffs, and approval." — W/prompts/zelda-gdd.md:54
77. [D] "Humans determine whether the game communicates, feels fair, and is enjoyable." — W/prompts/zelda-gdd.md:54
78. [I] Scope warning: offer a smaller game or a revised timeline. "Never silently extend timeline. Never silently cut features." — W/gdd/persona.md:73-74 (the registry prose; the prompt version is W/prompts/zelda-gdd.md:42)
79. [I] Task tickets: "Generate only if confirmed." — W/gdd/persona.md:81
80. [I] `edu` mode is opt-in: "Do NOT infer from the concept description." — W/gdd/persona.md:87
81. [G] "Human play-feel review ... Bear plays and chooses one improvement or test." — C/CHANGE-BRIEF.md:37-38 and C/SOURCES.md:16-17 ("Human play-feel review remains open.")
82. [G] "Bear owns scope, visual direction, release decisions, and approval." — C/GAME-BRIEF.md:56-57
83. [D] "CASE-020–021 are human sessions, never filled by simulated agents." — C/PLAYTEST-PLAN.md:22

The rules about how Walker itself is edited are separate (W/AGENTS.md:19-23). They are not rules for a game. Two quotable ones:
- "Don't give obvious guidance. The agent is a highly capable LLM" (:22)
- "When you change or remove a feature, describe the new state on its own terms." (:23)

CONTRIBUTING.md is Godogen's own and is still in the tree:
- "Godogen is an autonomous pipeline. The goal is to generate the best possible games with as little human guidance as possible." — W/CONTRIBUTING.md:5
- That is the opposite stance to Walker's loop. INFERRED: a good contrast beat. Flag it as an inconsistency in the repo, not as a design statement of Walker.

---

## 3. Godogen attribution and licence (facts only)

- W/AGENTS.md:3: "This is the active Walker framework, incorporating the Godogen source publisher."
- W/README.md:32: "Walker carries the **Godogen** source publisher and asset-generation tools."
- W/README.md:107-109: "The active publisher, engine guides, and asset-generation tooling retain their Godogen attribution." It points to LICENSE.md, CHANGELOG.md, CONTRIBUTING.md and AGENTS.md.
- W/LICENSE.md:1-3: "The MIT License / Copyright 2026 Alex Ermolov". Alex Ermolov is the copyright holder named in the file. The file does not call him the Godogen author. That link is INFERRED from the Godogen text throughout the tree (W/CHANGELOG.md:47: "Initial Godogen release", 2026-03-09).
- MIT terms: use, copy, modify, merge, publish, distribute, sublicense and sell are allowed. The copyright notice must be included. The software is provided "AS IS". (W/LICENSE.md:5-11)
- Carried-over Godogen text is visible: publish.sh:2 "Publish Godogen runtime files"; W/docs/PROJECT.md:1 "Godogen — From Prompt to Playable Game"; W/setup.md:3 "consolidated Godogen source repo"; W/CHANGELOG.md:19 `godogen:scene-change`; and the whole history from 2026-03-09 to 2026-07-02 in the CHANGELOG.
- What Walker added (W/CHANGELOG.md:2-6, dated 2026-09-18): the `gdd/` Zelda skill. Zelda is called the "upstream Zelda persona": 30 design commands from upstream, plus Walker additions `reverse`, `draft`, `deck`, `film`, `status`. The `prompts/zelda-gdd.md` prose is superseded by the skill.
- Other facts:
  - The repo also holds the file "hushangqing_27407_31505521_The MIT License", a student submission's MIT notice ("Copyright <2024> <Shangqing Hu>"). W/.gitignore:12-13 ignores it as "Local submission provenance". W/docs/repository-boundary.md:22-23 says it does not belong in the framework's licence declaration. Do not show it in the film, and do not show the name.
  - Example game licence status: C/SOURCES.md:21-22: "This repository does not add a blanket license to inherited work whose license has not been established. Public availability is not itself a license grant."
  - The Clawd character: C/SOURCES.md:9-11 says it is "an independent educational project, not an Anthropic product or endorsement."
  - Whether the upstream Godogen repo is still maintained, or where it lives, is not stated in these files. Do not claim either.

---

## 4. Worked example: the rules shaping one real change (walker-jumpman-clawd, Iteration 1, 2026-09-11)

What was asked (the human):
- C/CHANGE-BRIEF.md:9-12: "Bear wants the player to be a coding agent, represented by Clawd. Eventually, mini-goals will represent completed tasks and the final goal a full agentic loop. **Those task goals, new hazards, and the level extension are not implemented now.**"
- Scope, C/CHANGE-BRIEF.md:25-27: "Change drawing and presentation selection only. Preserve the player physics function, tuning, collision shape, level JSON, hazards, camera, input bindings, and recovery."
- It was handed to the agent as one change, not the whole game. FRICTIONAL.md:9-11: Bear "asked for one change at a time".

What the rules forced (a prediction first, in writing). C/CHANGE-BRIEF.md:14-21 lists three predicted failures BEFORE building:
1. "The wide Clawd silhouette may overhang the unchanged collision box. An arm can overlap a hazard without contact; inspect rather than silently retune."
2. "Playing a decorative jump loop on a physically jumping body could create two apparent jump arcs." So the decision (FRICTIONAL.md:17-18) was "physics supplies the airborne trajectory. Hold the mascot's apex pose instead of adding the gallery animation's second jump arc."
3. "A library of 18 animations might be mistaken for 18 implemented abilities." The fix: a separate gallery, labelled "a separate visual gallery, not 18 new gameplay abilities" (C/README.md:20).
- Scope guard: the 18 × 28 collider was kept (C/godot/features/player/player.gd:27, `shape.size = Vector2(18, 28)`). The FRICTIONAL entry says "Preserve the 18 × 28 collider first, expose the difference, and ask the human to judge it in play." (FRICTIONAL.md:15-16)
- Code is typed GDScript in the regular engine: `config/features=PackedStringArray("4.7", "GL Compatibility")`, 640x360 (C/godot/project.godot:7-12), and `func _physics_process(delta: float) -> void` (player.gd:44). INFERRED: it is mostly typed but not fully. For example `var tuning = Tuning.new()` (player.gd:7) is untyped. Do not say "every line is typed".
- Layout: feature-first, as the asset report prefers. The folders are `features/player/`, `game/`, `levels/`, `ui/`, `gallery/`, `tests/`, and every `.gd` has a `.gd.uid` sidecar committed (C/godot listing).

What was checked:
- C/README.md:35-37, and FRICTIONAL.md:22-26: "The 25 original mechanics checks and 9 synthetic-keyboard checks passed." The unchanged files were compared byte-for-byte with the starter commit: "The original physics function, tuning resource, level JSON, and HUD ... are byte-identical."
- A separate, independent TypeScript reference supplied 162 animation samples (FRICTIONAL.md:27-29). The GDScript test passed 1,944 scalar comparisons plus 6 staged presentation checks (C/godot/tests/test_clawd.gd:13-19 and :28-42). Frictional says "This establishes sampled parity, not that every possible frame is right."
- The test report labels its own limits: `"scope": "Numeric animation parity and staged presentation checks, not human playtesting"` (C/godot/tests/test_clawd.gd:43).
- Commands (C/README.md:39-43): `godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60`, then `test_keyboard.gd`, `test_clawd.gd`, then `node scripts/clawd-build.cjs`.
- Real engine output was captured at native 4K, "Clawd is recognizable in the existing level" (FRICTIONAL.md:30-31).
- Status file keeps the gaps explicit (C/CLAWD-STATUS.json:12-16): `"human_playtest": "pending"`, `"level_extension": "not implemented"`, `"task_mini_goals": "not implemented"`, `"agentic_loop_finish": "not implemented"`, `"assignment_1_complete": false`.

What went wrong, and what was kept (C/FRICTIONAL.md; this is the best "rules in action" material):
- An AI authoring-script error: two malformed dictionary entries. "Python's syntax check rejected it before execution." (FRICTIONAL.md:33-36)
- A capture that looked done and wasn't. One 18-second take saved 343 frames instead of 540: "The early receipt's PASS is insufficient; the take is rejected for the film and retained." (:39-43). The fix required 600 saved frames for 20 seconds; re-recordings got `-v2` names "preserving original takes".
- A second capture failure: "Exit code zero did not establish success. Rejected that take and retained its partial frames/logs." (:48-51)
- A visual failure: a multi-word trigger the component didn't match, so "The first render left the wrong sentence on screen." (:54-58) It was found by inspecting the render, not the log.
- The tradeoff left in the open instead of hidden (:59-63): "the broad arms can extend beyond the left world boundary, and the character can pass in front of world labels ... questions for Bear's next play session."
- This matches the rule "Preserve failed receipts" (C/AGENTS.md:16).

What a human found: the honest answer is that the files do not record a human finding for the Clawd iteration. Do not invent one.
- What IS recorded is a human decision about direction. Bear supplied intent and constraints: "Bear supplied the intent and constraints. AI implemented, captured, tested, wrote and rendered this iteration. Human play-feel judgments, film approval and the next design decision remain pending." (FRICTIONAL.md:71-74)
- Later, Bear authorised publication: "That authorizes publication; it does not invent a human playtest or a claim that Bear watched and approved every frame." (:79-81)
- If the film needs a moment where a human found something, the better-documented one is the parent starter, below. That one is a bug found by the machine checks, not by a human either.
- Companion example from the starter, C/BUILD-REPORT.md:19: "The first 25-check run found four failures, retained in [the original report] ... The jump tuning and acceptance tolerances were not weakened." One failure: "stale Area2D contacts after teleporting to spawn created a second death". This shows "do not weaken the test" in action.
- Starter, C/BUILD-REPORT.md:35: "AI checks mechanics; you judge the game." This is the best one-line summary of the human/AI split in the whole tree.
- Starter review (C/DESIGN-REVIEW.md:3): "**Document checks passed; gameplay untested.**" The CORE share was 66.7% against the 40% warning, "arithmetically correct" (:7). The scope warning was reported, not silently fixed.

---

## 5. What is only a specification (honest limits of Walker today)

From the files:
- W/README.md:38-40: "The `walker gdd` shell surface is still a specification, not an installed CLI or slash-command adapter."
- W/docs/zelda-gdd-workflow.md:64: "Still unbuilt: a `walker gdd` shell adapter, Godot discovery and test/capture orchestration tied to T-xx ids, and export checks."
- Same file, :3: "No `walker gdd` shell binary exists; that remains a future adapter."
- Same file, :50: "No generated consolidator is installed, so do not label hand-authored content as compiler output."
- Same file, :52: "A future implementation map should connect each feature ID to actual scene/script paths." (`reverse` does write an IMPLEMENTATION-MAP.md; the manual one in C/design/IMPLEMENTATION-MAP.md exists.)
- W/README.md:33-35: it "does not create a playable game or implement the entire development loop automatically."
- W/README.md:44-46: the publisher emits only the C#/.NET guide: "It does not yet select a GDScript guide."
- W/docs/PROJECT.md:54: "The runtime does not ship a dedicated audio pipeline or mobile/native packaging."
- W/docs/repository-boundary.md:51-53: "the Zelda/GDD documents describe authoring instructions, not an installed Walker CLI."
- W/docs/zelda-gdd-workflow.md:3 says `/gdd` IS implemented as an installed skill (2026-09-18).

Inferred from my reading (INFERRED):
- Enforcement is by convention. The gates live in `design/DESIGN-STATUS.json` (W/gdd/templates/DESIGN-STATUS.json:6-11), a file the agent could edit. Nothing stops it. "Gates are signed by humans only" is an instruction, not a lock.
- The GDScript rules in 2b (items 32-36) are in a prompt you could paste. They are not part of anything publish.sh installs. The installed guide is C#. In the working example (walker-jumpman-clawd), the GDScript rules live in the game's own hand-written files (C/AGENTS.md).
- The "tests" the rules call for are written by the agent for each game. The Clawd tests are plain `extends SceneTree` scripts the agent wrote (C/godot/tests/test_clawd.gd:1). Walker ships no test framework and no `T-xx` runner.
- The Walker publisher has not been shown to have been used to create walker-jumpman-clawd. That repo carries no publisher-made CLAUDE.md or `.claude/skills/`. It was cloned from the starter (C/SOURCES.md:3-5; FRICTIONAL.md:13-14). So "the rules in action" in section 4 are Walker-style rules written by hand into that game. They are not the output of `./publish.sh`.
- The tree has stale or contradictory spots to avoid reciting:
  - W/CONTRIBUTING.md is the Godogen contributor guide, "autonomous pipeline ... as little human guidance as possible".
  - W/docs/gdscript-vs-csharp.md argues for C#.
  - W/setup.md says Godot .NET is required.
  - W/prompts/zelda-gdd.md:11 forbids claims of shipping experience, but W/gdd/persona.md:3-4 gives Zelda "20+ years shipping titles".
- The `film` command (W/gdd/commands/film.md:21-22): "It never publishes, never captures gameplay by itself, and never changes the design." The brutalist.art `godot-gdd` skill is what makes films. That is outside Walker.
- Walker itself: is Walker yet proven beyond one small game? The only worked examples named are walker-jumpman and walker-jumpman-clawd (W/README.md:93-94). W/games/RECOVERY-README.md exists and the memory notes say 59 walker-* repos exist. I did not verify that. Say "two worked examples named in the README".
- Not all of W/games/ and W/youtube/ were read. They are excluded from the framework by design (W/README.md:96-98).

---

## 6. Five quotable lines (each from the files)

1. "The agent helps execute and check changes; the human decides what the game should be and whether it feels right." — W/README.md:5-6
2. "A successful build is not evidence of a successful human playtest." — W/README.md:28
3. "AI checks mechanics; you judge the game." — C/BUILD-REPORT.md:35
4. "Never invent human playtests, multiple days of work, approvals or test passes." — C/AGENTS.md:13-14
5. "Judge progress from the running game, never from a clean build" — W/prompts/runtime.md:10

Spares:
- "Zelda never signs a gate herself." — W/gdd/persona.md:95-96
- "Make one reviewable change." — C/AGENTS.md:11
- "Exit code zero did not establish success." — C/FRICTIONAL.md:49-50
- "Gate validation is a convention the skill follows, not code that enforces it." — W/docs/zelda-gdd-workflow.md:64
- "AI made *execution* cheap. It did not make *judgment* cheap." — W/legacy/README.md:5-6 (the idea behind the whole project)

---

## Suggested spine for Film 3 (INFERRED, optional)

1. The problem: AI makes building cheap, and it does not make judgment cheap (legacy README).
2. The loop: Game brief, Build, Playtest, Inspect, Revise, Export. Who decides what.
3. What it must NOT do: the rules in groups (scope, spend, humans-only), then how code must be written.
4. The rules in action: Clawd, one change, three predictions, a rejected capture, and a status file that says "pending".
5. Honest limits: the rules are mostly instructions the agent follows, not enforcement. The CLI is a specification.

Files read: all of W/{README,AGENTS,CLAUDE(symlink to AGENTS),setup,publish.sh,CHANGELOG,CONTRIBUTING,LICENSE}.md; W/prompts/*; W/engines/godot.md (bevy/babylon headers only); W/gdd/{SKILL,persona}.md, commands.yaml head, commands/{reverse,p1,film,status}.md and a grep across all commands; W/docs/*.md except the .docx; both Godot research files (read to the end of the copyable prompt, and the report to the end of the "Source Control" section); W/asset-gen/SKILL.md; W/legacy/{README,AGENTS,walker-cli-critique}.md; W/scripts/render_dir.py head; C/{AGENTS,CHANGE-BRIEF,GAME-BRIEF,FRICTIONAL,SOURCES,README (first 80 lines),BUILD-REPORT,DESIGN-REVIEW}.md, CLAWD-STATUS.json, godot/project.godot, godot/tests/test_clawd.gd, head of test_game.gd and test_keyboard.gd, head of player.gd.
