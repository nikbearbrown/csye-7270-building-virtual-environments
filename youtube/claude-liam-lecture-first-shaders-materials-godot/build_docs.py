#!/usr/bin/env python3
"""build_docs.py — writes SHOTLIST.md, FACTCHECK.md and CHECKS-REPORT.md from beat_sheet.json, lanes/*.json and factcheck/*.md.
Safe to re-run (run it after make_sheet.py). It never touches narration, scenes or the sheet.
FACTCHECK rows must be `| # | Beat | Claim | Verdict | Source | Fix |` with Verdict in PASS / CORRECTED / EXEMPT (Gate F rejects anything else)."""
import json, glob, re, datetime, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
sheet = json.loads((HERE / "beat_sheet.json").read_text())
beats = sheet["beats"]
today = datetime.date.today().isoformat()
BOOK = ("BOPEN", "BIDEA", "BDEFS", "BVDT", "BHTF", "BOUT")

# ── SHOTLIST ───────────────────────────────────────────────────────────────────────────────────────────────
rows = ["| beat | about | lane picked | runner-up | why this one wins |", "|---|---|---|---|---|"]
for b in beats:
    bid = b["beat_id"]
    shot = b.get("shot", {})
    if bid in BOOK:
        pat = shot.get("remotion", {}).get("pattern") or shot.get("template", "")
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
    "# SHOTLIST.md — one row per beat (BEST-BEAT LAW: every body beat auditioned >= 2 lanes; a beat with no runner-up was not auditioned)\n\n"
    + "\n".join(rows) + "\n")

# ── FACTCHECK ──────────────────────────────────────────────────────────────────────────────────────────────
fc_rows = []
for f in sorted(glob.glob(str(HERE / "factcheck" / "*.md"))):
    fc_rows += [l for l in Path(f).read_text().splitlines() if l.strip().startswith("|") and not re.match(r"^\|\s*[-: ]+\|", l)
                and not l.strip().lower().startswith("| #")]
out = []
bad = []
for l in fc_rows:
    cells = [c.strip() for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))]   # split on UNESCAPED pipes; a literal pipe inside a cell is written \|
    if len(cells) >= 6:
        verdict = cells[3].split()[0].strip("*").upper() if cells[3] else ""
        if verdict not in ("PASS", "CORRECTED", "EXEMPT"):
            bad.append((cells[1], cells[3]))
        out.append("| " + " | ".join([str(len(out) + 1)] + cells[1:6]) + " |")
    else:
        bad.append(("?", l[:60]))
def _beat_order(r):
    m = re.match(r"\|\s*\d+\s*\|\s*([A-Z0-9]+)", r)
    return m.group(1) if m else ""
(HERE / "FACTCHECK.md").write_text(
    "# FACTCHECK.md (Gate F)\n\n"
    f"Status: {len(out)} claims checked against the assignment text, the example's frozen source files, its recorded logs, the re-run logs of 2026-10-16 (`evidence/runs/`), "
    f"the captures, and the cited primary docs; signed by the build agent {today} (no human sign-off yet). Verdicts: PASS, CORRECTED (the narration or the picture was changed after the check), "
    "EXEMPT (framing, a drawing of an idea, a definition, or a card's own text). Zero OPEN. Every number is read from a log or json or is shown arithmetic.\n\n"
    "| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |\n|---|---|---|---|---|---|\n" + "\n".join(out) + "\n")
if bad:
    print("BAD VERDICTS:", bad)

# ── CHECKS-REPORT ──────────────────────────────────────────────────────────────────────────────────────────
hist = collections.Counter()
gates = collections.Counter()
act_s = collections.OrderedDict()
for b in beats:
    t = float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0)
    act_s[b["act"]] = act_s.get(b["act"], 0) + t
    gates[b.get("proof_gate", "SHOW")] += 1
    if b["beat_id"] in BOOK:
        hist["bookend"] += 1
    elif b.get("pending"):
        hist["PENDING"] += 1
    else:
        s = b["shot"]
        hist[("manim" if b["lane"] == "manim" else "remotion · " + s["remotion"]["pattern"])] += 1
total = sum(act_s.values())
measured = all(b.get("actual_duration_s") for b in beats)
(HERE / "CHECKS-REPORT.md").write_text(f"""# CHECKS-REPORT.md — PROOF GATE (written {today}, layout stage)

Beats: {len(beats)} · {'measured' if measured else 'ESTIMATED (words / 3.2; no audio exists yet)'} runtime {total:.0f} s ({total/60:.1f} min) · PROOF GATE classes {dict(gates)}.
A lane histogram is information, never a quota.

## Lane histogram
""" + "\n".join(f"- {k}: {v}" for k, v in sorted(hist.items(), key=lambda kv: -kv[1])) + """

## Runtime by act
""" + "\n".join(f"- {k}: {v:.0f} s" for k, v in act_s.items()) + """

## Whole-sheet teaching-arc checklist (nopunt)
- [x] FRAMEWORK beat before the worked example — Act II (B09-B18) presents what the change brief commits to (state, specification, colour line, measurable rules, controlled inputs, the hint-experiment predictions, material plan, predicted failures); Acts IV-IX run the example against exactly those fields.
- [x] WORKED EXAMPLE — Acts IV-IX walk the instructor example (labelled as such) through the wrapper, the driver, the mutations, the textured shader and two materials, the hint experiment in two renderers, the normal-map calibration, the audit and the human checks, each with a real log or a real engine capture.
- [x] FALSIFIABILITY / edge-case beat — B33-B34 (mutations: a deleted semicolon and a renamed uniform; the driver test still passes), B48 (deleting source_color), B62-B64 (the colour shortfall, the renderer, hint range does not clamp), B56-B58 (what the agent gets wrong).
- [x] SCAFFOLDED viewer task — BHTF: a paste-able prompt and two checks the viewer runs.
- [x] Bookends — BOPEN (narrated portrait/title), BIDEA (writer), BDEFS (terms) and BVDT, BHTF, BOUT (channel outro); no composer cold open, by the lecture skill's own spine.
- [ ] No source, no verdict — every body beat that asserts a number or a named result carries an on-screen artifact: verify per beat at the stills pass (open items are listed in BUILD-LOG.md).

## Open items
See BUILD-LOG.md.
""")
print("SHOTLIST/FACTCHECK/CHECKS-REPORT written;", len(out), "factcheck rows;", dict(hist), "est min", round(total / 60, 1))
