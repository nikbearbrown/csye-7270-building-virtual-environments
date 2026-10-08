# Prompts and command lines — Chapter 15

## Executive summary

Two prompts, both to Claude Code in the same session, on 27 September 2026, run from the scratch project root. The first states FEAT-10's save rules, written from WJ-D02's instruction to "write migration/corruption/reset rules before implementation". The second, sent after the reviewer's own checks, states two observed failures and the rule each broke, then asks for the smallest fix. Codex was not run for this chapter.

## Prompt 1 — implement FEAT-10 (saved as `prompt-best-time.txt`)

```text
This is walker-jumpman-clawd (Godot 4.7.2, GDScript), Professor Bear's Walker
example. Read README.md, GDD.md (FEAT-10), PRODUCTION-PLAN.md (WJ-D02),
godot/project.godot, godot/game/session.gd, godot/ui/hud.gd and every script
in godot/tests/ before editing anything.

Implement FEAT-10, a persistent personal best, as ONE bounded change.
Save rules (these are the WJ-D02 rules; follow them exactly):
- One JSON file, default path user://best_time.json, holding
  {"format": "walker-jumpman-clawd.best", "version": 1,
   "level": "first-steps", "best_seconds": <float>}.
- Load it once when the session starts. Missing file: no best, no error.
- Ignore, with push_warning and without crashing, a file that is not valid
  JSON, is not a dictionary, has the wrong format or level, or whose
  best_seconds is not a finite number greater than 0.
- A file whose version is greater than 1 was written by a newer build: ignore
  it and never overwrite it.
- On COMPLETE, if there is no best or last_finish_time is lower, update the
  best and save it: write a temporary file, then rename it over the old one.
  A failed write is reported with push_warning and changes no game state.
- The HUD's complete panel shows the best time. Nothing else in the HUD moves.
- The save path must be settable before the session enters the tree, so a
  test never reads or writes the player's real user:// file.

Do not change movement, tuning, the level JSON, collision, the camera or any
existing test. The 25 mechanics checks, 9 keyboard checks and test_clawd.gd
must still pass.

Write godot/tests/test_best_time.gd (extends SceneTree, same report style as
test_game.gd). Give every case its own fresh directory under
res://../evidence/. Complete the real route with tests/route_driver.gd and
prove: the file is written with the schema above; a NEW session instance
loads the same best; a slower completion does not replace it; each rejected
file leaves the game playable and is replaced only when a valid best is
saved; a version-2 file survives a completion byte for byte.

Then add godot/export_presets.cfg with one preset named "Web" (platform
"Web", export path ../build/web/index.html, tests/* excluded from the
export). Do not install or download export templates.

Run all four test scripts with
`godot --headless --path godot --script <res:// path> --fixed-fps 60`
and report the real output. Do not commit. End with a short list of what
these tests cannot tell us.
```

As run. Started 2026-09-27T18:03:32Z, ended 18:12:53Z, exit 0, 31 turns, CLI-reported cost $1.23:

```bash
claude -p "$(cat ../prompt-best-time.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > ../session.jsonl 2> ../session.stderr
```

## Prompt 2 — the correction (saved as `prompt-best-time-fix.txt`)

```text
I verified your change with my own commands. Two save rules are broken and
one claim in your summary is false.

1. You wrote that no test writes the player's real user:// file. With HOME
   pointed at a scratch folder, the unchanged tests/test_game.gd saved
   best_seconds 5.4667 to user://best_time.json, and tests/test_keyboard.gd
   saved 0.0667 (its resolve_contacts fixture "finishes" after 4 ticks).
   Those tests create the session with the default path.
2. My check wrote {"format":"walker-jumpman-clawd.best","version":2,
   "level":"first-steps-remix","best_seconds":4.0}, completed the route, and
   the file was overwritten. The same happens when a version-2 file renames
   "format". The rule is: a version greater than 1 is never overwritten,
   whatever else in the file changed.

Fix both in godot/game/session.gd only:
- A session with test_mode = true persists nothing unless the test set
  best_time_path explicitly. Normal play keeps user://best_time.json.
- Read "version" before any other field. If it is a number greater than 1,
  never write that path in this session.
Do not edit test_game.gd, test_keyboard.gd or test_clawd.gd.

In tests/test_best_time.gd: give each run its own new directory (for example
a timestamped folder), so a file left by an earlier run cannot make case 01
pass; add the two version-2 cases above; delete the "hud-best-field-set"
check, because it does not test the HUD.

Run all four test scripts the same way as before and report the real output.
Do not commit.
```

As run. Resumed the same session. Started 18:19:13Z, ended 18:22:41Z, exit 0, 8 turns, $0.76:

```bash
claude -p "$(cat ../prompt-best-time-fix.txt)" --resume ae769ccf-812c-460e-896e-fd82e64b77c2 --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > ../session-fix.jsonl 2> ../session-fix.stderr
```

## Reviewer commands (not the agent)

All test runs after the leak was found used a scratch `HOME` (macOS; `OS.get_user_data_dir()` follows it):

```bash
HOME="$PWD/../scratch-home" godot --headless --path godot --script res://tests/verify_best_time_rules.gd --fixed-fps 60
```

Clean-clone reproduction (scratch commit `35f1ec4`):

```bash
git clone <scratch-repo> ../clean-clone
```

```bash
HOME="$PWD/../scratch-home" godot --headless --path godot --import
```

```bash
git status --short
```

Invariant script, in a clone of the published repository with the change applied:

```bash
node scripts/clawd-build.cjs
```

Export attempts (real `HOME`; no game code runs):

```bash
godot --headless --path godot --export-release "Web" ../build/web/index.html
```

```bash
godot --headless --path godot --export-pack "Web" ../build/pack/walker-jumpman-clawd.zip
```

```bash
godot --headless --main-pack walker-jumpman-clawd.pck --quit-after 120
```
