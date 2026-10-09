"""Reference gate: a windowed (4K) take is valid only if its input/event log matches a headless
run of the same driver, action for action and position for position.

    python gate.py <headless.jsonl> <take.jsonl>

Compared: every press, release, click and game event, with tick, attempt, player x/y/state and
the cast direction. Not compared (diagnostics that legitimately differ between a real window and
headless): window pixel coordinates, focus_lost, reassert, start (window size). Exit 0 = valid.
"""
import json
import sys

IGNORED_EVENTS = {"focus_lost", "reassert", "start", "finish"}
IGNORED_KEYS = {"window", "root_viewport"}
# A real OS cursor sits on whole window pixels (0.25 game-world px at a 2564-px-wide window),
# so the aim read back by the game and the cast direction get a small, explicit tolerance.
# Any change in outcome (a hit or a miss) still fails through the game-event rows.
TOLERANCE = {"game_mouse_world": 0.5, "dir": 0.005}


def same(a, b):
    if a.keys() != b.keys():
        return False
    for k in a:
        if k in TOLERANCE and isinstance(a[k], list):
            if len(a[k]) != len(b[k]) or any(abs(x - y) > TOLERANCE[k] for x, y in zip(a[k], b[k])):
                return False
        elif a[k] != b[k]:
            return False
    return True


def rows(path):
    out = []
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("event") in IGNORED_EVENTS:
            continue
        out.append({k: v for k, v in r.items() if k not in IGNORED_KEYS})
    return out


def main():
    ref, take = rows(sys.argv[1]), rows(sys.argv[2])
    raw = [json.loads(l) for l in open(sys.argv[2], encoding="utf-8")]
    focus = sum(1 for r in raw if r.get("event") == "focus_lost")
    reassert = sum(1 for r in raw if r.get("event") == "reassert")
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(ref, take)) if not same(a, b)]
    ok = not diffs and len(ref) == len(take)
    print(f"gate: {'PASS' if ok else 'FAIL'}  compared rows ref/take: {len(ref)}/{len(take)}  "
          f"differing: {len(diffs)}  focus losses: {focus}  re-asserted presses: {reassert}")
    for i, a, b in diffs[:5]:
        print(f"  row {i}\n    ref : {a}\n    take: {b}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
