#!/usr/bin/env bash
# Every number Act V part 1 puts on screen or says about the first agent's session, recomputed from the record.
# Run:  bash transcript_facts.sh        (writes transcript-facts.log beside it)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
EX="$HERE/../../../../examples/03-blender-mcp-to-godot"
T="$EX/transcripts/run1-claude.jsonl"
{
echo "== result events (transcript lines 187 and 263)"
jq -c 'select(.type=="result") | {subtype, num_turns, duration_ms, minutes: ((.duration_ms/60000*10|round)/10)}' "$T"
echo
echo "== permission_denials per result, split by the refusal text the session saw"
for L in 187 263; do
  sed -n "${L}p" "$T" | jq -r --arg L "$L" '"line \($L): \(.permission_denials|length) denials"'
done
echo "refusals by kind (an error result whose text says the command needs approval, or was blocked outside the working directory):"
python3 - "$T" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
def errs(lo, hi):
    out = []
    for i, r in enumerate(rows, 1):
        if lo <= i < hi and r["type"] == "user":
            c = r["message"]["content"]
            if isinstance(c, list):
                for b in c:
                    if b.get("type") == "tool_result" and b.get("is_error"):
                        t = b["content"] if isinstance(b["content"], str) else " ".join(x.get("text", "") for x in b["content"])
                        out.append((i, t))
    return out
for name, lo, hi in (("phase 1 (lines 1-186)", 1, 187), ("phase 2 (lines 190-262)", 190, 263)):
    e = errs(lo, hi)
    appr = [x for x in e if "approval" in x[1]]
    blocked = [x for x in e if "was blocked" in x[1]]
    print(f"{name}: {len(appr)} needed approval (the allow list) + {len(blocked)} blocked (outside the working directory) = {len(appr)+len(blocked)} denials; lines {[x[0] for x in appr]} + {[x[0] for x in blocked]}")
# the full-path Godot attempts
n = 0
for i, r in enumerate(rows, 1):
    if r["type"] == "assistant":
        for b in r["message"]["content"]:
            if b["type"] == "tool_use" and b["name"] == "Bash" and "/Applications/Godot.app" in b["input"].get("command", ""):
                n += 1
print(f"Bash calls using /Applications/Godot.app/...: {n}")
# the compaction event
for i, r in enumerate(rows, 1):
    if r.get("subtype") == "compact_boundary":
        m = r["compact_metadata"]; print(f"line {i}: compact_boundary trigger={m['trigger']} pre_tokens={m['pre_tokens']} post_tokens={m['post_tokens']}")
PY
echo
echo "== timeline (run-times.txt gives the start and the final stop; durations from the two result events)"
python3 - <<'PY'
from datetime import datetime, timedelta
start = datetime.fromisoformat("2026-09-27T18:07:54"); end2 = datetime.fromisoformat("2026-09-27T18:48:53")
p1 = timedelta(milliseconds=1271707); p2 = timedelta(milliseconds=717737)
end1 = start + p1; start2 = end2 - p2
print(f"phase 1: {start.time()} -> {end1.time()}  ({p1.total_seconds()/60:.1f} min)")
print(f"gap (debug process hung until stopped): {end1.time()} -> {start2.time()}  ({(start2-end1).total_seconds()/60:.1f} min)")
print(f"phase 2: {start2.time()} -> {end2.time()}  ({p2.total_seconds()/60:.1f} min)")
PY
echo
echo "== the finished run-1 test's own log (logs/verify1-test_checkpoint_post.log)"
echo "PASS lines: $(grep -c '^PASS' "$EX/logs/verify1-test_checkpoint_post.log")   FAIL lines: $(grep -c '^FAIL' "$EX/logs/verify1-test_checkpoint_post.log")"
grep -E "^Failures" "$EX/logs/verify1-test_checkpoint_post.log"
echo "check() call sites in the run-1 test: $(grep -cE '^\s*_check\(' "$EX/scripts/agent/test_checkpoint_post.run1.gd")   ('grep -c _check(' also counts the 'func _check(' definition: $(grep -c '_check(' "$EX/scripts/agent/test_checkpoint_post.run1.gd"))"
echo "run-2 test: PASS lines $(grep -c '^PASS' "$EX/logs/verify2-test_checkpoint_post.log"), check() call sites $(grep -cE '^\s*_check\(' "$EX/scripts/agent/test_checkpoint_post.gd"), 'grep -c _check(' = $(grep -c '_check(' "$EX/scripts/agent/test_checkpoint_post.gd")"
echo
echo "== the first test run (transcript line 139): the ray and the post"
sed -n 139p "$T" | jq -r '.message.content[0].content' | grep -E "ray from|ray hit|FAIL|merged AABB" 
echo
echo "== game.tscn placement edits (transcript lines 132 and 210)"
for L in 132 210; do sed -n "${L}p" "$T" | jq -r '.message.content[0].input | (.new_string // .old_string)' | grep -o 'Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, [^)]*)' | head -n1 | sed "s/^/line $L: /"; done
python3 -c "print('gap between the two placements: %.5f m' % (4.0 - 3.84189))"
} > "$HERE/transcript-facts.log" 2>&1
cat "$HERE/transcript-facts.log"
