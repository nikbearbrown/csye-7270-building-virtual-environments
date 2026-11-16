#!/usr/bin/env python3
"""verify_embedded.py — fail if a line embedded in scenes_act5.py (A5_REAL) or scenes_act7.py (A7_REAL) differs from the frozen source.
Run from the reel folder:  python3 evidence/act5/verify_embedded.py"""
import ast, sys
SRC = "evidence/example/sources/"
bad = 0
for act in ("5", "7"):
    try:
        tree = ast.parse(open(f"scenes_act{act}.py").read())
    except FileNotFoundError:
        continue
    d = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == f"A{act}_REAL" for t in node.targets):
            d = ast.literal_eval(node.value)
    if d is None:
        print(f"act {act}: no A{act}_REAL"); continue
    n = 0
    for f, rows in d.items():
        L = open(SRC + f).read().split("\n")
        for ln, t in rows.items():
            n += 1
            if L[ln - 1] != t:
                bad += 1; print("MISMATCH", act, f, ln, repr(t), repr(L[ln - 1]))
    print(f"act {act}: {n} embedded lines checked")
# the verbatim log lines B52 shows
try:
    tree = ast.parse(open("scenes_act7.py").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "A7_LOG" for t in node.targets):
            lg = ast.literal_eval(node.value)
            L = open("evidence/act7/vertex_albedo_check.log").read().split("\n")
            for t in lg:
                if t not in L:
                    bad += 1; print("LOG MISMATCH", repr(t))
            print(f"act 7: {len(lg)} log lines checked")
except FileNotFoundError:
    pass
print("VERIFY", "FAIL" if bad else "PASS")
sys.exit(1 if bad else 0)
