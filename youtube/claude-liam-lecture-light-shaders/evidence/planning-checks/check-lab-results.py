#!/usr/bin/env python3
"""check-lab-results.py: is lab-results.jsonl a complete, valid record of run-lab-checks.sh?

Why this exists: on 2026-10-13 about 14:49 another session ran `pkill -f run-lab-checks.sh`, which can kill any film's batch of that name.
This reads (it does not run Godot) and checks, for this film:
  1. one row for every shader x renderer that run-lab-checks.sh loops over (lab-shaders/*.gdshader x forward_plus, gl_compatibility);
  2. every row exit 0 and a parseable RESULT line with "ok": true;
  3. the uniforms the Lab lists equal the uniforms declared in the shader file;
  4. the results file is newer than every shader file (nothing was edited after the batch);
  5. no row is duplicated or out of order (a killed batch re-run over a live one would interleave).
Exit 0 only if all five hold. Run from anywhere: python3 check-lab-results.py
"""
import glob
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.abspath(os.path.join(HERE, "..", ".."))
RES = os.path.join(HERE, "lab-results.jsonl")
SHADERS = sorted(glob.glob(os.path.join(FILM, "lab-shaders", "*.gdshader")))
RENDERERS = ["forward_plus", "gl_compatibility"]

problems = []
rows = [json.loads(line) for line in open(RES) if line.strip()]
expected = [(os.path.basename(s), r) for s in SHADERS for r in RENDERERS]
got = [(r["shader"], r["renderer"]) for r in rows]
print(f"shaders in lab-shaders/: {len(SHADERS)}; expected rows: {len(expected)}; rows in file: {len(rows)}")
if got != expected:
    missing = [e for e in expected if e not in got]
    extra = [g for g in got if g not in expected]
    dup = sorted({g for g in got if got.count(g) > 1})
    problems.append(f"rows differ from the batch loop: missing {missing}, extra {extra}, duplicated {dup}, in order: {got == sorted(got)}")

for r in rows:
    tag = f'{r["shader"]} {r["renderer"]}'
    if r["exit"] != 0:
        problems.append(f"{tag}: exit {r['exit']}")
        continue
    out = r["output"]
    if not out.startswith("RESULT "):
        problems.append(f"{tag}: no RESULT line: {out[:80]!r}")
        continue
    try:
        j = json.loads(out[len("RESULT "):])
    except Exception as e:  # noqa: BLE001
        problems.append(f"{tag}: RESULT is not JSON ({e})")
        continue
    if j.get("ok") is not True:
        problems.append(f"{tag}: ok is not true")
    declared = re.findall(r"^\s*uniform\s+\w+\s+(\w+)", open(os.path.join(FILM, "lab-shaders", r["shader"])).read(), re.M)
    listed = sorted(u.split(":")[0] for u in j.get("uniforms", []))
    if sorted(declared) != listed:
        problems.append(f"{tag}: Lab lists uniforms {listed}, file declares {sorted(declared)}")
    if r["renderer"] == "forward_plus" and "forward" not in str(j.get("renderer", "")).lower():
        problems.append(f"{tag}: the Lab reports renderer {j.get('renderer')!r}")
    if r["renderer"] == "gl_compatibility" and "compat" not in str(j.get("renderer", "")).lower():
        problems.append(f"{tag}: the Lab reports renderer {j.get('renderer')!r}")

res_t = os.path.getmtime(RES)
newer = [os.path.basename(s) for s in SHADERS if os.path.getmtime(s) > res_t]
print("results file written:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res_t)))
print("newest shader edit:  ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(max(os.path.getmtime(s) for s in SHADERS))))
if newer:
    problems.append(f"shaders edited after the batch: {newer}")

if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print(f"OK: {len(rows)} of {len(expected)} rows present, in loop order, all exit 0 with ok true, uniforms match the files, no shader newer than the results.")
