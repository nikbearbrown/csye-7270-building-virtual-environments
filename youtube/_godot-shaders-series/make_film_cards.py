#!/usr/bin/env python3
"""make_film_cards.py: writes FILM-CARDS.md, one card per laid-out film (idea, the wrong assumption it opens on, length, what it
corrected, where to read it), read from the films' own files. Run after the films are laid out:  python3 make_film_cards.py"""
import importlib.util
import re
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent
sys.path.insert(0, str(SERIES))
import series_config as S  # noqa: E402
import lint_series as L    # noqa: E402

ROW = re.compile(r"^\|\s*[\w\-]+\s*\|[^|]*\|(?P<claim>[^|]*)\|\s*(?P<verdict>CORRECTED|OPEN|PASS|EXEMPT)\s*\|(?P<evidence>[^|]*)\|")


def load(slug):
    f = S.folder(slug) / "narration.py"
    spec = importlib.util.spec_from_file_location("n_" + slug.replace("-", "_"), f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def first_sentence(s):
    s = " ".join(str(s).split())
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return m.group(1) if m else s


def main():
    patterns, planned = L.registered_patterns()
    out = ["# Film cards (generated)\n",
           "**What this is.** One card per film in the series: the idea, the wrong assumption the film opens on, its estimated length, what running Godot corrected, and where to read it.",
           "**Why.** So the whole series can be judged on one page before anyone opens twenty scripts.",
           "**Found.** Read from each film's `narration.py` and `FACTCHECK.md` by `make_film_cards.py`; lengths are estimates from word count (0.34 s per word plus 4 s), not from audio.\n"]
    group = None
    n_cards = 0
    for slug, title, grp in S.FILMS:
        folder = S.folder(slug)
        if grp != group:
            group = grp
            out.append(f"## {grp}\n")
        if not (folder / "narration.py").exists() or not (folder / "beat_sheet.json").exists():
            out.append(f"### {title}\n\nNot laid out yet.\n")
            continue
        try:
            N = load(slug)
        except Exception as e:  # noqa: BLE001
            out.append(f"### {title}\n\nnarration.py does not import: {e}\n")
            continue
        r = L.lint_film(slug, patterns, planned)
        info = r["info"]
        fc = (folder / "FACTCHECK.md")
        corrected, opened = [], 0
        if fc.exists():
            for line in fc.read_text().splitlines():
                m = ROW.match(line)
                if not m:
                    continue
                if m.group("verdict") == "CORRECTED":
                    corrected.append(" ".join(m.group("claim").split()))
                elif m.group("verdict") == "OPEN":
                    opened += 1
        bidea = getattr(N, "BIDEA_TEXT", ("", "", ""))
        wrong = " ".join(str(bidea[0]).split())
        right = bidea[2] if len(bidea) > 2 else ""
        lanes = info.get("lanes", {})
        lane_s = ", ".join(f"{k} {v}" for k, v in lanes.items() if v)
        status = "lint clean" if not r["errors"] else f"{len(r['errors'])} lint errors"
        out.append(f"### {title}\n")
        out.append(f"- **The idea.** {getattr(N, 'SUMMARY', '')}")
        out.append(f"- **Opens on the assumption.** \"{wrong}\" (the hesitant writer corrects it to \"{right}\").")
        out.append(f"- **Length.** {info.get('beats', '?')} beats, {info.get('words', '?')} words, about {info.get('minutes', '?')} minutes. Lanes: {lane_s}. {status}.")
        if corrected:
            out.append(f"- **Corrected by running Godot ({len(corrected)}).** " + " | ".join(c[:150] for c in corrected[:4]) + (" …" if len(corrected) > 4 else ""))
        else:
            out.append("- **Corrected by running Godot.** nothing in the fact-check was marked CORRECTED.")
        if opened:
            out.append(f"- **Open fact-check rows.** {opened} (see the film's FACTCHECK.md).")
        cut = first_sentence(getattr(N, "CUT_LINE", ""))
        if cut:
            out.append(f"- **If it runs long.** {cut}")
        out.append(f"- **Read.** `{folder}/SCRIPT.md`\n")
        n_cards += 1
    out.insert(4, f"**Cards.** {n_cards} films laid out of {len(S.FILMS)}.\n")
    (SERIES / "FILM-CARDS.md").write_text("\n".join(out) + "\n")
    print(f"{n_cards} cards -> FILM-CARDS.md")


if __name__ == "__main__":
    main()
