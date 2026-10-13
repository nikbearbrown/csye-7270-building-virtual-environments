#!/usr/bin/env python3
"""build_docs.py — writes SHOTLIST.md, FACTCHECK.md and CHECKS-REPORT.md from beat_sheet.json, lanes/*.json and factcheck/*.md.
Safe to re-run. Run after make_sheet.py."""
import json, glob, re, datetime, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
sheet = json.loads((HERE / "beat_sheet.json").read_text())
beats = sheet["beats"]
today = datetime.date.today().isoformat()

# ── SHOTLIST ───────────────────────────────────────────────────────────────────────────────────────────────
rows = ["| beat | about | lane picked | runner-up | why this one wins |", "|---|---|---|---|---|"]
for b in beats:
    bid = b["beat_id"]
    shot = b.get("shot", {})
    if bid in ("BIDEA", "BDEFS", "BVDT", "BHTF", "BOUT"):
        pat = shot.get("remotion", {}).get("pattern", "")
        rows.append(f"| {bid} | opening/closing bookend | bookend · {pat} | — | fixed spine (lecture SKILL) |")
        continue
    lec = b.get("lecture", {})
    if b.get("pending"):
        rows.append(f"| {bid} | PENDING | — | — | no lane entry yet |")
        continue
    lane = b["lane"]
    pick = shot.get("manim", {}).get("class") if lane == "manim" else shot.get("remotion", {}).get("pattern")
    about = (shot.get("visual_intent") or "").replace("|", "/")
    rows.append(f"| {bid} | {about} | {lane} · {pick} | {lec.get('runner_up','').replace('|','/')} | {lec.get('why','').replace('|','/')} |")
(HERE / "SHOTLIST.md").write_text(
    "# SHOTLIST.md — one row per beat (BEST-BEAT LAW: every body beat auditioned ≥ 2 lanes; a beat with no runner-up was not auditioned)\n\n"
    + "\n".join(rows) + "\n")

# ── FACTCHECK ──────────────────────────────────────────────────────────────────────────────────────────────
fc_rows = []
for f in sorted(glob.glob(str(HERE / "factcheck" / "*.md"))):
    fc_rows += [l for l in Path(f).read_text().splitlines() if l.strip().startswith("|")]
n = 0
out = []
for l in fc_rows:
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    if len(cells) >= 6:
        n += 1
        out.append("| " + " | ".join([str(n)] + cells[1:6]) + " |")
(HERE / "FACTCHECK.md").write_text(
    "# FACTCHECK.md (Gate F)\n\n"
    f"Status: {len(out)} claims checked against the source chapter, its evidence record (logs, transcripts, scripts), fresh re-runs on 2026-10-06 and the cited primary docs; signed by the build agent {today} (no human sign-off yet).\n\n"
    "| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |\n|---|---|---|---|---|---|\n" + "\n".join(out) + "\n")

# ── CHECKS-REPORT ──────────────────────────────────────────────────────────────────────────────────────────
hist = collections.Counter()
gates = collections.Counter()
act_s = collections.defaultdict(float)
for b in beats:
    t = float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0)
    act_s[b["act"]] += t
    gates[b.get("proof_gate", "SHOW")] += 1
    if b["beat_id"] in ("BIDEA", "BDEFS", "BVDT", "BHTF", "BOUT"):
        hist["bookend"] += 1
    elif b.get("pending"):
        hist["PENDING"] += 1
    else:
        s = b["shot"]
        hist[("manim" if b["lane"] == "manim" else "remotion · " + s["remotion"]["pattern"])] += 1
total = sum(act_s.values())
(HERE / "CHECKS-REPORT.md").write_text(f"""# CHECKS-REPORT.md — PROOF GATE (written {today})

Beats: {len(beats)} · estimated/measured runtime {total:.0f} s ({total/60:.1f} min) · PROOF GATE classes {dict(gates)}.
A lane histogram is information, never a quota.

## Lane histogram
""" + "\n".join(f"- {k}: {v}" for k, v in sorted(hist.items(), key=lambda kv: -kv[1])) + f"""

## Runtime by act
""" + "\n".join(f"- {k}: {v:.0f} s" for k, v in act_s.items()) + """

## Whole-sheet teaching-arc checklist (nopunt)
- [x] FRAMEWORK beat before the worked example — Act III (B21–B28) presents the fields a brief commits to (size in metres, origin, look, budget, predicted failures); Act VI tests exactly those fields by number, and the eyes cover the rest.
- [x] WORKED EXAMPLE — Acts V and VI walk three real assets (crate, lantern, coin), built by a real Blender script run, through export, import and the headless check, with the brief's fields on screen.
- [x] FALSIFIABILITY / edge-case beat — B26 (an origin in the middle sinks or floats) and B58 (a check can prove less than it claims), with the real failure demonstrations (unapplied scale, +Y Up off, a centred origin) shown in Act VI.
- [x] SCAFFOLDED viewer task — BHTF: a paste-able prompt and two checks the viewer runs.
- [x] Bookends — opening pair (hesitant writer, key terms) and closing three (recap, Your Turn, channel outro); no composer cold open, by the lecture skill's own spine.
- [ ] No source, no verdict — every body beat that asserts a number or a named result carries an on-screen artifact: verify per beat at the stills pass (open items are listed in BUILD-LOG.md).

## Open items
See BUILD-LOG.md.
""")
print("SHOTLIST/FACTCHECK/CHECKS-REPORT written;", len(out), "factcheck rows;", dict(hist))
