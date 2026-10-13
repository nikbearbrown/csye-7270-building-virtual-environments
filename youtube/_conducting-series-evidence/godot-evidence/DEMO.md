# Godot no-bridge demo: evidence for film 2 ("Why Godot")

**What this is.** On 2026-10-09, on Bear's Mac, a Claude agent added a Label node to a real Godot 4.7.2 scene. It did this by editing the scene's text file, then proved the change with a headless Godot command. It made four tool calls: Read, Edit, Write, and Bash running `godot`. It used no MCP server, no editor plugin and no bridge. The run took 23.4 s from prompt to final report. The change was verified 13.3 s after the prompt.

**What was found.**
- **The edit worked first time.** The agent's own check printed `PASS`. My separate check, written by me and kept outside the project, also passed:
  - all 21 original nodes are still present
  - the scripts and signal connection I checked are still attached
  - there is exactly one new Label, under the root, with the right text
- **Controls.** The same check run on the unedited scene fails, as it should. The edited game runs headless for 60 frames with exit 0, and an editor import pass also exits 0. No errors or warnings appeared.
- **One deviation from what Godot writes itself.** The agent left out the `unique_id=` attribute that every other node in this 4.7 scene carries. Godot loads the file fine without it. When I had Godot re-serialise the scene, it assigned one (`unique_id=1828201969`). So the text is valid, but it is not byte-for-byte what the editor would save.
- **Deviation from the brief: no `claude -p` run.** The brief asked for a headless `claude -p` session. Every Claude Code binary on this machine refused to authenticate, so that could not happen; the details are in [What could not be done as briefed](#what-could-not-be-done-as-briefed). Instead the demo ran as a **fresh Claude Code subagent** with the same prompt, on the same model (`claude-opus-5-5`). Its tool limits were written into the prompt but **not enforced by the harness**. Its transcript shows it kept to them.

---

## What could not be done as briefed

The brief asked for `claude -p ... --output-format stream-json --verbose`, with tools enforced through `--allowedTools`, `--disallowedTools` and `--strict-mcp-config`. Every attempt failed at authentication before any model call, at $0 cost. Full log: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-evidence/part2/01-claude-p-auth-failures.txt`.

| Binary | Result |
|---|---|
| `/opt/homebrew/bin/claude` 2.1.150 | "Not logged in · Please run /login". An earlier attempt with `--setting-sources ""` returned "API Error: 401 OAuth access token has been revoked." |
| Desktop-bundled `claude` 2.1.293 (`~/Library/Application Support/Claude/claude-code/2.1.293/...`) | "Failed to authenticate: OAuth session expired and could not be refreshed" |
| `~/.local/bin/claude` 2.1.139 | "Not logged in · Please run /login" |

Both the inherited environment and a clean `env -i` environment were tried. Logging in needs Bear's hand (`claude` then `/login` in a terminal). I did not attempt it.

**Substitute run.** I started a fresh general-purpose Claude Code subagent. It began with no context from me and had not seen the scene. It received the exact prompt below. Its transcript was saved by the harness, and a filtered copy is in this folder.

Limitation: that subagent technically had other tools available, including MCP tools. The rules lived only in the prompt. The transcript shows it called nothing but Read, Edit, Write, one `godot` Bash command, and the handback. This shows the job *can be done* with those tools. It does not show the harness *forbade* anything else. To get the enforced, stream-json version, re-run with the command in [To reproduce](#to-reproduce-the-enforced-claude--p-version-once-logged-in) once `claude` is logged in.

---

## Part 1: facts from this machine

Files: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-evidence/part1/`

- **`godot --version`**: `4.7.2.stable.official.ed1daf0bf`, exit 0. `/opt/homebrew/bin/godot` is a symlink to `/Applications/Godot.app/Contents/MacOS/Godot`.
- **Size**:
  - `du -sh /Applications/Godot.app` is **337M**.
  - The single binary is **335M** (351,312,912 bytes). Essentially the whole editor is one executable.
  - No Godot download (zip or dmg) was found in `~/Downloads`.
- **CLI help**:
  - `godot --headless --help` is 129 lines, with 98 option lines.
  - Relevant options include `--headless`, `--import`, `--quit`, `--quit-after`, `-s/--script`, `--check-only`, `--export-release/--export-debug/--export-pack`, and `--doctool`.
  - Full text: `part1/godot-help-full.txt`.
- **A small real project** (`/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot`):
  - 27 files, 93,085 bytes, `du -sh` 172K.
  - The 14 `.tscn`/`.gd`/`project.godot` files total **34,203 bytes**. There are no `.tres` files.
  - `file` reports every one of them as `ASCII text`, including the `.gd.uid` sidecars, e.g. `uid://ctlvx6ghbupgu`.
  - Its two scenes are tiny. `game/main.tscn` is 168 bytes and 6 lines, because the game builds its nodes in code.
  - Excerpts of `main.tscn`, the first 40 lines of `features/player/player.gd`, and `project.godot` are in `part1/walker-claude-inventory-and-excerpts.txt`.
- **Headless import and quit on a COPY** (`part1/walker-claude-copy-import-quit.txt`):
  - `godot --headless --path <copy> --import`: exit 0, 3.03 s.
  - `godot --headless --path <copy> --quit`: exit 0, 0.25 s.
  - Side effect: the import pass **created one new file**, `tests/test_clawd.gd.uid`, because the original repo is missing that sidecar. No other source file changed.

---

## Part 2: the no-bridge demo

**Project.** `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-pong/godot` was copied to `/private/tmp/claude-501/godot-evidence-work/pong-demo`, minus its `.godot/` cache. The original was not touched.
- Its `pong.tscn` is 103 lines and 3,974 bytes. It has 7 `ext_resource` lines with `uid://` values, 4 sub_resources, and 21 nodes, each carrying `unique_id=`.
- Baseline before the demo: `--import` exit 0 in 6.47 s, then `--quit-after 30` exit 0. See `part2/00-baseline-import-and-run.txt`.

**Exact prompt**: `part2/02-prompt.txt`. Summary: use only Read, Edit, Write and `godot` Bash commands; add a Label named `HelloLabel` under the root with text "Hello from a text file" by editing the `.tscn` text; write `res://check_label.gd` that loads, finds, prints and quits 0 or 1; run it headless; report.

### What the agent did, step by step (from its transcript, UTC)

The prompt arrived at 17:42:02.783.

1. **17:42:04.475, Read** `pong.tscn`. It got back the whole 103-line scene.
2. **17:42:07.196, Edit** `pong.tscn`. It anchored on the Camera2D's last property and the first connection line:
   - `old_string`: `offset = Vector2(320, 200)\n\n[connection`
   - `new_string`: the same lines, with the new node block inserted between them.
3. **17:42:09.845, Write** `check_label.gd`. The script extends `SceneTree`, loads the scene in `_initialize()`, and uses `get_node_or_null("HelloLabel") as Label`. It prints the text, then `PASS` or `FAIL`, and quits 0 or 1. It also fails on load or instantiate errors. Full file: `part2/check_label.gd`.
4. **17:42:13.272, Bash** `godot --headless --path /private/tmp/claude-501/godot-evidence-work/pong-demo --script res://check_label.gd`. Output, returned at 17:42:16.052, with no error flag:
   ```
   Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

   HelloLabel text: Hello from a text file
   PASS
   ```
5. **17:42:25.771, handback.** In its own words: "I left out a `unique_id` on purpose so it couldn't clash with an existing ID."

It made no other tool calls. Every call and result is in `part2/04-tool-calls-and-results.txt`, and the filtered transcript is in `part2/03-transcript.jsonl`. The agent's thinking blocks are stored empty in the transcript, so its reasoning is not recorded.

**Timings**:
- Prompt to verified PASS: **13.3 s**.
- Prompt to final report: **23.4 s** (the harness reported `duration_ms: 23439`).
- The `godot --script` check inside the agent's run: about 2.8 s of wall time between the tool call and its result. My later re-run took 0.16 s.
- Wall clock on my side, including spawn overhead: 34.6 s.

### The diff (`part2/pong.tscn.diff`)

```diff
--- a/pong.tscn
+++ b/pong.tscn
@@ -95,6 +95,9 @@
 [node name="Camera2D" type="Camera2D" parent="." unique_id=957432765]
 offset = Vector2(320, 200)
 
+[node name="HelloLabel" type="Label" parent="."]
+text = "Hello from a text file"
+
 [connection signal="area_entered" from="Left" to="Left" method="_on_area_entered"]
 [connection signal="area_entered" from="Right" to="Right" method="_on_area_entered"]
 [connection signal="area_entered" from="LeftWall" to="LeftWall" method="_on_wall_area_entered"]
```

The change is three added lines and nothing removed. No `ext_resource`, `uid://` or id was touched, because a Label needs none. Files changed relative to the original: `pong.tscn`, plus the new `check_label.gd`. The later editor import also generated `check_label.gd.uid`.

### Independent checks (mine, not the agent's)

Full output: `part2/independent-checks.txt`. My script is `part2/independent_check.gd`. It ran from **outside** the project folder (`/private/tmp/claude-501/godot-evidence-work/independent-check/independent_check.gd`).

| Check | Result |
|---|---|
| Re-run the agent's `check_label.gd` | `PASS`, exit 0, 0.16 s |
| My script on the **edited** scene | PackedScene node_count 22. Instantiated 22. Original nodes present 21/21. One Label at `HelloLabel`, parent `Pong`, text "Hello from a text file". Scripts still on Left/Right/Ball/walls/ceiling/floor. `INDEPENDENT RESULT: PASS`, exit 0 |
| **Control**: my script on the **unedited** scene | node_count 21, "Expected exactly 1 Label, found 0", `FAIL (1)`, exit 1 |
| `godot --headless --path pong-demo --quit-after 60` (runs the game) | exit 0, 0.56 s, no errors |
| `godot --headless --path pong-demo --import` (editor pass) | exit 0, 1.96 s, no errors or warnings. Afterwards `pong.tscn` is byte-identical to before plus the diff, so the editor did not rewrite it |
| How Godot itself serialises the new node (`part2/resave.gd`, which packs and saves to a scratch file, `part2/pong.resaved-by-godot.tscn`) | `[node name="HelloLabel" type="Label" parent="." unique_id=1828201969]`. Godot adds a `unique_id`; the agent's text omits it |

### What the agent got wrong or did differently

- **It omitted `unique_id`.** Every other node in this Godot 4.7 scene has one. Godot accepted the file without it: no warning on load, run or import. Godot's own serialiser adds one, so the editor will likely add one the next time the scene is saved. I did not verify that, because I did not open the windowed editor. Calling the omission "on purpose" is the agent's own claim. Whether it is the right choice is a judgement call. It is not an error.
- **Exit-code claim.** The agent said the check exited 0 because the Bash tool flagged no error; its rules stopped it from echoing `$?`. My re-run confirmed exit 0 directly.
- Nothing broke, and no second attempt was needed.

### What this does and does not prove

**It does show**, on this machine with Godot 4.7.2:
- A Godot scene is a plain-text file that an AI agent can read and change with an ordinary string edit.
- Godot's own CLI (`--headless --script`, `--import`, `--quit-after`) is enough to verify that change, with no MCP server, editor plugin or bridge.
- A check I wrote separately agrees, and a control run on the unedited scene fails as it should.

**It does not show**:
- That this generalises. It was **one run**, of a **tiny, additive task** (one node, no resources, no ids, no signals), on a small 2D scene.
- Anything about complex scenes: instanced sub-scenes, ext_resource id renumbering, `uid://` creation for new resources, animation or tileset data, or merge conflicts.
- That tool restrictions were enforced. They were stated in the prompt and kept, but not imposed by the harness, because `claude -p` could not authenticate.
- That the result looks right on screen. Nothing was rendered, and the Label sits at position (0,0) with default theme.
- That headless `claude -p` behaves the same as this subagent. It was the same model and prompt, but a different harness.

---

## To reproduce the enforced `claude -p` version (once logged in)

From a fresh copy of `walker-pong/godot`:

```
cd <copy>
claude -p "$(cat /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-evidence/part2/02-prompt.txt)" \
  --output-format stream-json --verbose \
  --tools Read,Edit,Write,Bash \
  --allowedTools 'Read' 'Edit' 'Write' 'Bash(godot:*)' \
  --disallowedTools 'WebFetch' 'WebSearch' 'Agent' 'NotebookEdit' \
  --permission-mode dontAsk \
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
  --setting-sources "" --no-session-persistence > transcript.jsonl
```

Change the prompt's absolute paths to match the copy's location.

## File index

Folder: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/godot-evidence/`

- `part1/`
  - `godot-version-size-help.txt`
  - `godot-help-full.txt`
  - `walker-claude-inventory-and-excerpts.txt`
  - `walker-claude-copy-import-quit.txt`
- `part2/`
  - `00-baseline-import-and-run.txt`
  - `01-claude-p-auth-failures.txt`
  - `02-prompt.txt`
  - `03-transcript.jsonl` (filtered; harness reminders omitted)
  - `04-tool-calls-and-results.txt`
  - `pong.tscn.before`
  - `pong.tscn.after`
  - `pong.tscn.diff`
  - `check_label.gd`
  - `independent_check.gd`
  - `independent-checks.txt`
  - `resave.gd`
  - `pong.resaved-by-godot.tscn`

The raw, unfiltered transcript of the demo agent is still in the harness store: `/Users/bear/.claude/projects/-Users-bear-Documents-CoWork/b4e22290-c2cb-4e1f-afcc-e7ec4a58f487/subagents/agent-a6762635c63d1761b.jsonl`.
