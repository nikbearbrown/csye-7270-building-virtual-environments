#!/usr/bin/env python3
"""series_table.py: writes SERIES-TABLE.md from the actual layouts (beats, words, estimated minutes, lanes, OPEN fact-check rows,
cut line). Run after the films are laid out:  python3 series_table.py
Everything in the table is read from the films' own files, so the plan can never drift from them."""
import importlib.util
import json
import re
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent
sys.path.insert(0, str(SERIES))
import series_config as S  # noqa: E402
import lint_series as L    # noqa: E402


def load(slug):
    f = S.folder(slug) / "narration.py"
    spec = importlib.util.spec_from_file_location("n_" + slug.replace("-", "_"), f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    patterns, planned = L.registered_patterns()
    rows, group, totals = [], None, {"films": 0, "beats": 0, "words": 0, "min": 0.0, "open": 0}
    out = ["# Series table (generated)\n",
           "**What this is.** One row per film, read from the films' own files by `series_table.py`: beats, words, estimated minutes at Liam's measured pace, lanes, open fact-check rows, and the first line of each film's cut line.",
           "**Why.** So the plan's numbers are the layouts' numbers.",
           "**Found.** See the totals line at the bottom. Minutes are an estimate from word count (0.34 s per word plus the fixed opening and closing); the real length is known after the voice is generated.\n",
           "| Film | Beats | Words | Est. min | Lanes (manim / capture / remotion / editor) | OPEN rows | Lint |",
           "|---|---|---|---|---|---|---|"]
    detail = []
    for slug, title, grp in S.FILMS:
        folder = S.folder(slug)
        if grp != group:
            group = grp
            out.append(f"| **{grp}** | | | | | | |")
        if not (folder / "narration.py").exists():
            out.append(f"| {title} | not laid out | | | | | |")
            continue
        r = L.lint_film(slug, patterns, planned)
        i = r["info"]
        lanes = i.get("lanes", {})
        lane_s = " / ".join(str(lanes.get(k, 0)) for k in ("manim", "capture", "remotion", "editor"))
        fc = (folder / "FACTCHECK.md").read_text() if (folder / "FACTCHECK.md").exists() else ""
        opens = len(re.findall(r"^\|\s*[\w\-]+\s*\|[^|]*\|[^|]*\|\s*OPEN\s*\|", fc, re.M))
        status = "clean" if not r["errors"] else f"{len(r['errors'])} errors"
        out.append(f"| {title} | {i.get('beats', '-')} | {i.get('words', '-')} | {i.get('minutes', '-')} | {lane_s} | {opens} | {status} |")
        totals["films"] += 1
        totals["beats"] += i.get("beats", 0)
        totals["words"] += i.get("words", 0)
        totals["min"] += i.get("minutes", 0.0)
        totals["open"] += opens
        try:
            N = load(slug)
            detail.append((title, getattr(N, "CUT_LINE", "")))
        except Exception:
            pass
    out.append(f"\n**Totals.** {totals['films']} films, {totals['beats']} beats, {totals['words']:,} words, about {totals['min']:.0f} minutes "
               f"({totals['min'] / 60:.1f} hours) of film; {totals['open']} OPEN fact-check rows in all.\n")
    out.append("## Cut lines (what moves out if a film runs long)\n")
    for title, cut in detail:
        out.append(f"- **{title}.** {cut}")
    (SERIES / "SERIES-TABLE.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[:40]))


if __name__ == "__main__":
    main()
