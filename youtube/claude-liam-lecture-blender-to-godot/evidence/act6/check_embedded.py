#!/usr/bin/env python3
"""check_embedded.py — every real-text string that scenes_act6.py puts on screen is found in the real record.
Run from the REEL folder:  python3 evidence/act6/check_embedded.py > evidence/act6/check_embedded.out.txt
Each row: (string shown, the real source it must occur in).  A string must occur BOTH in scenes_act6.py (it is what we show) and in the source.
"""
import json, re, sys
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]
EX = REEL.parent.parent / "examples" / "03-blender-mcp-to-godot"
scenes = (REEL / "scenes_act6.py").read_text()
def text(p): return (EX / p).read_text()
def tool_inputs(jsonl, tool_name, key):
    out = []
    for l in text(jsonl).splitlines():
        d = json.loads(l); c = d.get("message", {}).get("content")
        if isinstance(c, list):
            for x in c:
                if x.get("type") == "tool_use" and x.get("name") == tool_name and key in x.get("input", {}): out.append(x["input"][key])
    return out
def tool_results(jsonl):
    out = []
    for l in text(jsonl).splitlines():
        d = json.loads(l); c = d.get("message", {}).get("content")
        if isinstance(c, list):
            for x in c:
                if x.get("type") == "tool_result": out.append(x["content"] if isinstance(x["content"], str) else json.dumps(x["content"]))
    return out
run1 = "transcripts/run1-claude.jsonl"
writes = tool_inputs(run1, "Write", "content")            # every file the first agent wrote, in order
first_test = next(w for w in writes if "test_checkpoint_post" in w or "_check(" in w)   # first version of the test
results = "\n".join(tool_results(run1))
codex = [json.loads(l) for l in text("transcripts/run2-codex.jsonl").splitlines()]
codex_blob = json.dumps(codex, ensure_ascii=False)
refused = text("transcripts/run2-claude-refused.jsonl")
v1, v2 = text("logs/verify1-test_checkpoint_post.log"), text("logs/verify2-test_checkpoint_post.log")
crash = text("logs/blender-crash-in-codex-sandbox.txt")
prompts = text("PROMPTS.md"); runtimes = text("logs/run-times.txt")
run1_test = text("scripts/agent/test_checkpoint_post.run1.gd")
rows = [
    # B60
    ("FAIL  no unexpected materials", results, "run-1 transcript: first test run output"),
    ('[found ["PostMetal", "FlagCloth", ""]]', results, "run-1 transcript: first test run output"),
    ("if mat:", first_test, "run-1 transcript: FIRST version of the materials loop (Write)"),
    ('if mat and mat.resource_name != "":', run1_test, "scripts/agent/test_checkpoint_post.run1.gd (the agent's later version)"),
    ("PASS  no unexpected named materials", v2, "logs/verify2-test_checkpoint_post.log"),
    ('["PostMetal", "FlagCloth"]', v2, "logs/verify2-test_checkpoint_post.log"),
    # B62
    ("PASS  collision X_max ≤ 0.35", v1, "logs/verify1-test_checkpoint_post.log (the part before the ellipsis)"),
    ("[got 0.300]", v1, "logs/verify1-test_checkpoint_post.log (the part after the ellipsis)"),
    # B63
    ("PLAYER_CAP_H  := 2.10", run1_test, "run-1 test, line 23"),
    ("POST_WORLD    := Vector3(-6.5, -4.0, 3.9334)", run1_test, "run-1 test, line 26"),
    ("player.tscn", prompts, "PROMPTS.md (ask 3 names player/player.tscn)"),
    ("game.tscn", prompts, "PROMPTS.md (ask 2 names game.tscn)"),
    ("test_checkpoint_post.gd", prompts, "PROMPTS.md"),
    # B64
    ("You've hit your session limit · resets 6:40pm (America/New_York)", refused, "transcripts/run2-claude-refused.jsonl"),
    # B65 / B66
    ("GPU_backend_type_selection_detect", crash, "logs/blender-crash-in-codex-sandbox.txt"),
    ("metal_is_supported", crash, "logs/blender-crash-in-codex-sandbox.txt"),
    ("Never open", prompts, "PROMPTS.md run 1 (Claude Code) prompt: the sentence 'Never open its window.' (shown on two lines)"),
    ("its window.", prompts, "PROMPTS.md run 1 (Claude Code) prompt"),
    ("cua_repl", codex_blob, "run2-codex.jsonl item_23 server"),
    # B68
    ("no pennant length lies inside collider", v2, "logs/verify2-test_checkpoint_post.log"),
    ("[overlap 0.0000 m]", v2, "logs/verify2-test_checkpoint_post.log"),
]
bad = 0
for s, src, label in rows:
    a, b = s in scenes, s in src
    print(("OK  " if a and b else "BAD ") + f"{s!r}  in scenes_act6.py: {a}  in {label}: {b}")
    bad += (not (a and b))
# counts
n139 = sum(1 for d in codex if d.get("type") == "item.completed" and d["item"].get("type") == "command_execution" and d["item"].get("exit_code") == 139)
print("Codex command_execution events with exit_code 139:", n139, "(narration: four times)"); bad += (n139 != 4)
rev_prompt = prompts[prompts.index("## Run 2 — Codex CLI"):]
rev_prompt = rev_prompt[:rev_prompt.index("## Steps the operator ran")]
first_prompt = prompts[prompts.index("## Run 1"):prompts.index("## Run 2, first attempt")]
print("'Never open its window.' in the first prompt:", "Never open its window." in first_prompt, "; the word 'window' in the revision (Codex) prompt:", "window" in rev_prompt.lower(), "(B66: the rule was not repeated)")
bad += ("Never open its window." not in first_prompt)
bad += ("window" in rev_prompt.lower())
print("B67A: PASS lines in verify2 log:", len(re.findall(r"^PASS", v2, re.M)), " FAIL lines:", len(re.findall(r"^FAIL", v2, re.M)), " 'Failures: 0' present:", "Failures: 0" in v2)
embedded = re.search(r"A6_PASS_LINES = \[(.*?)\]\n", scenes, re.S).group(1)
shown = re.findall(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', embedded)
shown = [a or b for a, b in shown]
pass_lines = [l[len("PASS  "):] for l in v2.splitlines() if l.startswith("PASS")]
print("B67A embedded list == the log's PASS lines (text after 'PASS  '):", shown == pass_lines, "(", len(shown), "vs", len(pass_lines), ")"); bad += (shown != pass_lines)
print("verify1 PASS lines:", len(re.findall(r"^PASS", v1, re.M)), "(chapter/README say 16 of 16)")
# run-times: stopped 5 min 31 s after start
from datetime import datetime
t0 = datetime.fromisoformat("2026-09-27T18:54:24+00:00"); t1 = datetime.fromisoformat("2026-09-27T18:59:55+00:00")
print("Codex run: start 18:54:24Z stop 18:59:55Z ->", t1 - t0, " (run-times.txt has both stamps:", "18:54:24Z" in runtimes and "18:59:55Z" in runtimes, ")")
lane = json.loads((REEL / "lanes/act6.json").read_text())
shell = lane["B67B"]["props"]["lines"]
pl = [l for l in v2.splitlines() if l.startswith("PASS")]
ok = all(l == "" or l in pl for l in shell)
print("B67B shell lines are all verbatim PASS lines of logs/verify2-test_checkpoint_post.log:", ok, "(", sum(1 for l in shell if l), "lines )"); bad += (not ok)
print("B67B shell title is the real command in PROMPTS.md:", lane["B67B"]["props"]["title"] in prompts); bad += (lane["B67B"]["props"]["title"] not in prompts)
print("ALL EMBEDDED STRINGS VERIFIED" if bad == 0 else f"{bad} PROBLEM(S)")
sys.exit(1 if bad else 0)
