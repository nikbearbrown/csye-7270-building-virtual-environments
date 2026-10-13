#!/usr/bin/env bash
# verify_scope.sh — re-runs the checks behind B17/B21/B22's numbers (read-only).  Output: evidence/act3/verify_scope.log
BOOKS=/Users/bear/Documents/CoWork/bear-textbooks/books
C=$BOOKS/walker-jumpman-clawd
S=$BOOKS/walker/games/walker-jumpman
echo "== B17: the two receipts (S = starter)"
python3 - <<PY
import json
for f in ("mechanics-1789078423.29998.json", "mechanics-1789078494.18347.json"):
    d = json.load(open("$S/evidence/" + f)); r = d["results"]
    print(f, d["created_at"], "checks", len(r), "PASS", sum(x["status"] == "PASS" for x in r), "failures field", d["failures"])
    for i, x in enumerate(r, 1):
        if x["status"] != "PASS": print("   #%d %s FAIL observed %s" % (i, x["id"], x["observed"]))
from datetime import datetime as D
a = D.fromisoformat(json.load(open("$S/evidence/mechanics-1789078423.29998.json"))["created_at"]); b = D.fromisoformat(json.load(open("$S/evidence/mechanics-1789078494.18347.json"))["created_at"])
print("gap seconds:", (b - a).total_seconds())
a = [x["id"] for x in json.load(open("$S/evidence/mechanics-1789078423.29998.json"))["results"]]; b = [x["id"] for x in json.load(open("$S/evidence/mechanics-1789078494.18347.json"))["results"]]
print("same 25 check ids in the same order:", a == b)
PY
echo; echo "== B21: what changed from the starter commit 9387542 to the Clawd commit f1cc442 (godot/ only)"
git -C $C diff --numstat 9387542 f1cc442 -- godot
echo "-- files in godot/ named levels/ or tuning.gd or hud.gd or main.tscn in that diff:"
git -C $C diff --name-only 9387542 f1cc442 -- godot | grep -E "levels/|tuning.gd|hud.gd|main.tscn" || echo "(none: unchanged)"
echo "-- _physics_process() slice (func _physics_process( up to the next func) identical?"
python3 - <<PY
import subprocess
def sl(t):
    i = t.index("func _physics_process("); j = t.index("\nfunc ", i + 5); return t[i:j]
a = subprocess.run(["git", "-C", "$C", "show", "9387542:godot/features/player/player.gd"], capture_output=True, text=True).stdout
b = subprocess.run(["git", "-C", "$C", "show", "f1cc442:godot/features/player/player.gd"], capture_output=True, text=True).stdout
print("physics slice identical:", sl(a) == sl(b), "| whole player.gd identical:", a == b)
PY
echo "-- hazards live in first_steps.json:"; grep -n '"hazards"' $C/godot/levels/first_steps.json
echo "-- animation receipt:"; cat $C/evidence/clawd/animation-1789103540.86128.json | tr -d '\n '; echo
echo "-- 162 samples x 12 scalars = $((162*12))"
echo; echo "== B22: the take (controls.mp4, walker-jumpman-clawd walkthrough capture): where Clawd stops, and the camera"
python3 - <<PY
import json
rows = [json.loads(l) for l in open("$C/youtube/claude-liam-walker-jumpman-clawd-walkthrough/capture/controls-states.jsonl")]
m = min(rows, key=lambda r: r["x"]); print("min x", m["x"], "at frame60", m["frame60"], "camera_x", m["camera_x"], "(640-wide view centred on 320 => left screen edge = world x 0)")
print("art half-width = 136 units * 0.32 / 2 = %.2f px; body centre stops at x = 10 => art reaches x = %.2f" % (136 * 0.32 / 2, 10 - 136 * 0.32 / 2))
PY
grep -n "maxf(position.x, 10.0)" $C/godot/features/player/player.gd
