# Walker publisher: what one real install puts in a game folder

**What this is.** Evidence for film 3, "What is Walker, and why". On 2026-10-09 the publisher was run for real into new, empty scratch folders: once for Claude, once for Codex, and once more from the committed (public) version of the repo. Everything below comes from those runs. The publisher's output is copied verbatim into `installed/`. (Written by the evidence subagent; saved here by the main session.)

**What it found.**
- One command installs a small instruction kit and nothing else: no game, no Godot project, no README.md, no design/ folder.
- The manifest is 12 lines long.
- The Godot guide assumes C# on Godot .NET. The /gdd skill installed beside it defaults to typed GDScript, and so does the walker-jumpman example game.
- A Claude install and a Codex install have the same content, apart from paths and command sigils.
- The run used Bear's uncommitted working tree. The committed, pushed version installs only asset-gen, with no /gdd.

## 1. The runs
All three commands were run from /Users/bear/Documents/CoWork/bear-textbooks/books/walker.

| Run | Command | Exit | Log |
|---|---|---|---|
| A, Claude, working tree | `./publish.sh --engine godot --agent claude --out /private/tmp/claude-501/walker-evidence-work/walker-demo-game` | 0 | publish.log |
| B, Codex, working tree | same with `--agent codex --out .../walker-demo-game-codex` | 0 | publish-codex.log |
| C, Claude, committed HEAD 10fedb8 (via `git archive HEAD` into scratch) | same flags as A, `--out .../walker-demo-game-HEAD` | 0 | publish-committed-HEAD.log |

Full output of run A, verbatim:
```
Publishing godot/claude to: /private/tmp/claude-501/walker-evidence-work/walker-demo-game
Installed asset-gen and gdd skills
Created CLAUDE.md
Created godot.md
Created .gitignore
Done.
```

**Dependencies.** The publisher needs only bash, rsync (macOS openrsync), python3 (3.14.6) and git. All were present, and nothing failed. It checks none of the game toolchain that setup.md lists (Godot .NET, dotnet 9, ffmpeg, API keys). So a successful publish proves nothing about whether you can build a game.

**Repo state when run.** HEAD was 10fedb8, "Publish Walker framework and preserve Unity-first source under legacy" (2026-09-11), with main...origin/main. The working tree had uncommitted changes to publish.sh and prompts/runtime.md, plus an untracked gdd/.

## 2. What was installed (run A)
Run A installed **54 files, 127,260 bytes**, plus an empty .git (`git init -q`, no commits). The full list is in installed-tree.txt.
- **CLAUDE.md:** 1,349 bytes, **12 lines**. This is the runtime manifest.
- **godot.md:** 5,479 bytes, 66 lines. A copy of engines/godot.md.
- **.gitignore:** 72 bytes, 9 lines: `.claude`, `CLAUDE.md`, `godot.md`, `assets`, `screenshots`, `.godot`, `*.import`, `bin/`, `obj/`. The AI instructions themselves are not committed by default.
- **.claude/skills/asset-gen/:** 8 files, about 55 KB. SKILL.md (124 lines), rembg.md, and tools/ (asset_gen.py, tripo3d.py, rembg_matting.py, grid_slice.py, find_loop_frame.py, requirements.txt). These are paid Gemini, xAI and Tripo3D calls.
- **.claude/skills/gdd/:** 40 files, about 49 KB. SKILL.md (85 lines), persona.md (121), commands.yaml (287), 35 command specs, and 2 templates.

What the 12-line manifest says (installed/claude/CLAUDE.md):
- Line 3: keep status in README.md.
- Line 4: make assets with /asset-gen, and confirm spend before the first paid generation.
- Line 5: write the design with /gdd in design/, and build from design/GDD.md feature IDs.
- Line 6: read godot.md.
- Line 10: "Judge progress from the running game, never from a clean build".
- Line 12: "the result is proven, not claimed … finish with a 15–20s video of the game in action, and watch it back before you call the work done."

## 3. Which language the installed Godot guide assumes
**C#.** godot.md:3 says: "Stack: **Godot 4 (.NET / Mono build)**, **C#**. All Godot C# classes must be `partial`."
- Its build gate is `dotnet build` (line 10).
- It builds scenes from "C# `SceneTree` scripts" (line 16).
- Its code sample is C# (lines 26–37).
- Line 49 notes that "training data is GDScript-biased, so guessed C# enum names are often wrong".

**The contradiction in the same install.** .claude/skills/gdd/commands/p3.md:6 says "ENGINE / TOOLCHAIN (default Godot 4, typed GDScript, 2D greybox first; …". The same text is in commands.yaml:119. Walker's own repo acknowledges the split:
- walker/README.md:44–47 says the publisher "currently emits the existing **C#/.NET** engine guide. It does not yet select a GDScript guide. The separate Walker Jumpman example uses GDScript".
- walker/prompts/zelda-gdd.md:15 says the GDScript profile is "an explicit proposal, not evidence that that guide or the publisher has been migrated."

## 4. What is NOT installed
**Missing from the game folder:**
- No game at all: no project.godot, .csproj, scenes or scripts. publish.sh:8–11 says the agent "scaffolds the game itself from the engine guide — no project scaffold is shipped".
- No README.md and no design/ folder. The manifest tells the agent to create both.

**Left behind in the Walker repo:**
- **No GDScript conventions.** godot-scripting-conventions-research-prompt.md (190 lines) is a research prompt and is not shipped. No GDScript engine guide exists.
- **None of docs/:** gdscript-vs-csharp.md, zelda-gdd-workflow.md, PROJECT.md, demo_prompts.md, repository-boundary.md, How_Godot_Wants_Assets_Organized.docx.
- **Other material:** setup.md; godot-asset-organization-report.md (381 lines); prompts/zelda-gdd.md (the long Zelda prompt); bevy.md and babylon.md (the other engine guides); games/, godot-demo-projects/ and legacy/.

## 5. Claude vs Codex install
The Codex install is **56 files, 127,823 bytes**. godot.md is byte-identical. The full diff is in claude-vs-codex.diff.
- **Manifest:** CLAUDE.md vs AGENTS.md. Same 12 lines apart from the sigils.
- **Skills folder:** .claude/skills/ vs .agents/skills/.
- **Commands:** /asset-gen and /gdd vs $asset-gen and $gdd.
- **Codex extras:** an agents/openai.yaml in each skill (2 files). asset-gen sets allow_implicit_invocation: true; gdd sets it to false.
- **.gitignore:** `.claude`, `CLAUDE.md` vs `.agents`, `AGENTS.md`, `.codex`. The 7 engine lines are the same.
- **The only prose difference:** rembg.md says "Claude cannot judge transparency…" vs "Codex cannot…" (2,628 vs 2,627 bytes).

## 6. What the public, committed version installs (run C)
Run C printed "Installed asset-gen skill" (singular). It installed 11 files: asset-gen, CLAUDE.md, godot.md and .gitignore. It has **no /gdd skill**. Its CLAUDE.md is **11 lines** with no /gdd line, and its godot.md is identical to run A's.

So a clone of github.com/nikbearbrown/walker at 10fedb8 gets the 11-file kit. The 54-file kit exists only in the uncommitted local tree as of 2026-10-09. The remote was not checked (no network allowed in the brief).
