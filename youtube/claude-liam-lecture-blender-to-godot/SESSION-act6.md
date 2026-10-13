# SESSION-act6 — what Codex's screen shows in B64, B65, B66, and where every line comes from

**What this is.** The record behind the three beats that show Codex (the second agent, which revised the checkpoint post). Every line shown on a Codex surface, and every line of its run drawn beside it, is listed here with the place in the real run it was taken from.

**Why it exists.** The lecture shows a tool as itself and nothing on a tool's screen may be invented. A reviewer can open each source below and find the line.

**What was found.** Everything shown traces to the record. Three things a reviewer should know: (1) the Codex templates carry a green check on every line, so only lines that really completed are put on them; the failed runs are drawn as an ink ledger instead; (2) the narration's 'fixed it' for Codex is imprecise (the setting was already on; Codex removed the extra physics block): factcheck row 623; (3) the run was `codex exec --json`, a command-line run: the library's Codex templates are the Codex app's look, used here as the library's faithful skin, which the lecture skill names as the second rung.

Sources (all under `examples/03-blender-mcp-to-godot/`): `PROMPTS.md`; `transcripts/run2-codex.jsonl` (47 lines, indexed from 0 below; item ids are Codex's own, e.g. item_23); `transcripts/run2-claude-refused.jsonl`; `logs/run-times.txt`; `logs/blender-crash-in-codex-sandbox.txt`; `diffs/run2-codex-plus-operator.diff`.

Rebuild the stills and recheck every string: `python3 evidence/act6/make_codex_stills.py`, `python3 evidence/act6/check_embedded.py`.

## B64 · the composer (pantry/a6_codex_ask.png, library component CodexComposerAsk)

| Shown | Source |
|---|---|
| The whole prompt, from 'The previous agent run (Claude Code) stopped at the turn limit' to 'Report the real output and git diff --stat. Do not commit.' | PROMPTS.md, section 'Run 2 — Codex CLI 0.153.4', the text block, verbatim (copied to evidence/act6/prompt2_codex.txt by the script) |
| 'CODEX CLI 0.153.4' (label above the prompt) | PROMPTS.md heading: 'Codex CLI 0.153.4' |
| 'gpt-5.6-sol' (model label) | PROMPTS.md: 'gpt-5.6-sol, reasoning low' |
| 'workspace-write' (mode label) | PROMPTS.md: `codex exec --sandbox workspace-write` |
| 'walker-3d-platformer-asset' (workspace) | the folder name in the transcript's paths (`<scratch>/walker-3d-platformer-asset/...`) |
| Under the window: 'Claude Code, asked first:' and 'You've hit your session limit · resets 6:40pm (America/New_York)' | transcripts/run2-claude-refused.jsonl, line 2, the assistant text, and line 3, the result; the label is ours |
| Template chrome, not from the run | 'Codex' and the C mark, 'WORKSPACE', 'TASKS', the empty task card (the heading is left empty), the status 'Running' and the arrow button. One stray status dot the template draws above the prompt (its empty 'running' line) was painted out |

## B65 · Codex's thread (pantry/a6_codex_found.png, library component CodexWindow) and the four runs

| Shown | Source |
|---|---|
| 'web_search: site:docs.godotengine.org Node type customization use node type suffixes name suffixes glTF -convcolonly' | run2-codex.jsonl line 11 (item.completed, type web_search): the query, verbatim; 'web_search:' is the event type |
| 'The documentation identifies `nodes/use_node_type_suffixes`: disabling it opts out of collision-producing node suffixes, including `-convcolonly`.' | line 20 (agent_message item_10), its first sentence, verbatim |
| 'update godot/props/checkpoint_post.glb.import' | line 24 (file_change item_12, completed): changes[0], kind update; the `<scratch>/walker-3d-platformer-asset/` prefix in the transcript is a redaction placeholder and is dropped |
| 'update tools/blender/build_checkpoint_post.py' | same event, changes[5], kind update |
| 'I've also changed the collider to a tapered convex hull: full base footprint below, pole-width above, ending exactly at the pennant root.' | line 29 (agent_message item_15), its last sentence, verbatim |
| Heading 'item.completed', status 'item.completed', thread 'codex exec' | event type names and the command name: our labels, chosen so no wording of ours is presented as Codex's |
| The collider outline turning from a box into the hull | diffs/run2-codex-plus-operator.diff and scripts/agent/build_checkpoint_post.py (hull of base +-0.30 and pole +-0.08); vertices read from checkpoint_post.glb |
| Four rows 'as written', 'private temp folder', 'separate config folder', '--gpu-backend flag', each with a cross and 'exit 139' | lines 30-31 (item_16: Blender -b --factory-startup --python tools/blender/build_checkpoint_post.py, exit_code 139), 35-36 (item_19: the same with `TMPDIR=/private/tmp`, 139), 37-38 (item_20: `BLENDER_USER_CONFIG=/tmp/blender-config BLENDER_USER_SCRIPTS=/tmp/blender-scripts`, `--disable-autoexec`, 139), 41-42 (item_22: `--gpu-backend vulkan`, 139); row labels are our descriptions of the four variants |
| 'GPU_backend_type_selection_detect' and 'metal_is_supported' under 'crash site, from Blender's own crash log' | logs/blender-crash-in-codex-sandbox.txt, backtrace frames 4-6 (`_ZN7blender3gpu10MTLBackend18metal_is_supportedEv`, `_ZN7blender33GPU_backend_type_selection_detectEv`): readable substrings of the real symbol names |

Not shown, on purpose: Codex's own sentence after the first crash says Blender 'exited 0 but crashed'; the recorded exit code is 139 (line 31), which is what the film shows.

## B66 · the tool call (pantry/a6_codex_tool_a.png and _b.png, library component CodexCodeBeat)

| Shown | Source |
|---|---|
| 'Initialize Blender so its headless build can access the graphics backend' | line 43 (item.started, mcp_tool_call item_23), arguments.title |
| 'let app = await cua.getApp("Blender");' | same event, arguments.code |
| 'cua_repl · js' | same event: server cua_repl, tool js |
| 'Computer Use was not approved to use Blender' | line 44 (item.completed, item_23), result.content[0].text, verbatim |
| 'stopped by the operator, 5 min 31 s in' | logs/run-times.txt: Codex start 2026-09-27T18:54:24Z, 'stopped by the operator at 2026-09-27T18:59:55Z after the Computer Use attempt on Blender'; the difference is 5 min 31 s; the wording is ours |
| 'first prompt' card: 'Never open its window.' (shown on two lines) | PROMPTS.md, Run 1 (Claude Code) prompt: 'Run it only in background mode (-b --factory-startup --python <script>). Never open its window.' |
| 'revision prompt' card: the same sentence as a ghost in a dashed box | the revision prompt (Run 2, Codex) contains no sentence about the window (checked by script: the word 'window' does not occur in it) |
| 'Blender -b' with 'exit 139', then 'cua_repl js' | the four Blender runs above, then item_23 |
| Template chrome, not from the run | the dark code card, the line number, the `$` bar (left empty) and its green status dot; the dot sits beside the refusal text although the call was refused, a limit of the template |

Cropping: the template's tall empty dark card is cut to header, code line and status bar (evidence/act6/make_codex_stills.py); no text was changed.
