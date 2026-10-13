#!/usr/bin/env python3
"""lint_series.py — machine checks on the LAYOUT of the Godot shader films. Run from anywhere.

  python3 lint_series.py                      # every film in series_config.FILMS that has a folder
  python3 lint_series.py godot-shaders uv-space
  python3 lint_series.py --report             # also writes LINT-REPORT.md next to this file

It checks the rules a human would otherwise have to check by eye: length band, beat sizes, forbidden words (numbering, "the book",
"the course"), bookend contracts (terms, writer, recap, your turn), lane entries (runner-up, motion, cues, real component names),
the file set, and that every shader file a beat points at exists. It cannot judge teaching quality or truth: that is FACTCHECK.md
and a human read of SCRIPT.md.
"""
import glob
import importlib.util
import json
import re
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent
sys.path.insert(0, str(SERIES))
import series_config as S  # noqa: E402

REQUIRED_FILES = ["narration.py", "make_sheet.py", "beat_sheet.json", "SCRIPT.md", "ACTS.md", "SHOTLIST.md", "FACTCHECK.md",
                  "CHECKS-REPORT.md", "SOURCES.md", "PROMPTS.md", "CAPTURE-PLAN.md", "BUILD-PROMPT.md"]
FORBIDDEN = [
    (r"\bthis chapter\b", "says 'this chapter'"), (r"\bthe book\b", "says 'the book'"), (r"\bthe course\b", "says 'the course'"),
    (r"\b(in the )?(last|previous|next|earlier|first|second|third|other) (video|film|lecture|episode)\b", "refers to another video"),
    (r"\bvideo (one|two|three|four|five|\d+)\b", "numbers a video"), (r"\bpart (one|two|three|four|five|\d+)\b", "numbers a part"),
    (r"\bepisode\b", "says 'episode'"), (r"\bas we (saw|learned|covered|did) (earlier|before|previously)\b", "leans on an earlier film"),
    (r"\bCSYE\b|\bINFO ?7375\b|\bNortheastern\b", "names a course or school (these films are standalone)"),
    (r"\b(textbook|syllabus|assignment|module|homework)\b", "course language"),
    (r"\bplaylist\b", "mentions the playlist"), (r"\bseries\b", "says 'series' (viewer-facing numbering risk)"),
    (r"\b\d+ of \d+\b", "N of X numbering"),
]
# GLOSSARY "Never say" and spoken-form rules, checked on narration text (error = the voice would get it wrong; warn = register).
WORD_ERRORS = [
    (r"\bPI\b|\bTAU\b", "uppercase PI/TAU in narration (the voice reads PI as the letters P, I; write lowercase pi / tau)"),
    (r"\b[A-Za-z_]+\(\)", "a code call with parentheses in narration (say the name: fragment, not fragment())"),
    (r"\b[A-Z]{3,}\b", "an all-caps word in narration (the voice may spell it out; write built-ins as lowercase words: vertex, color, time)"),
    (r"\bGPU\b|\bCPU\b|\bUV\b|\bRGBA?\b|\bHSV\b", "unspaced acronym in narration (write G P U, U V, R G B)"),
]
WORD_WARNINGS = [
    (r"\bpixel shader\b", "says 'pixel shader' (allowed only in the one beat that explains the two names)"),
    (r"\b(draw call|rasteri[sz]\w*|invocations?|kernel)\b", "jargon from the GLOSSARY never-say list"),
    (r"\b(just|simply|easy|easily|obviously)\b", "register: the GLOSSARY says cut just / simply / easy / obviously"),
    (r"\b(\w+) times (faster|slower)\b|\b\w+ cores\b|\bthousands of (cores|threads)\b", "a speed multiplier or core count (claims must be measured)"),
    (r"\b(starts|begins) when the node (appears|is added)\b|\bsince the shader was created\b", "TIME is one clock for the whole game"),
]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def _norm_term(t):
    return re.sub(r"[*`\s]+", "", t).lower()


def _norm_def(d):
    d = d.replace("\u25c6", " ")
    return re.sub(r"\s+", " ", d).strip().rstrip(".").lower()


def canon_defs():
    """term -> on-screen definition, read from GLOSSARY.md (rows whose term cell is a single bold name)."""
    out = {}
    g = SERIES / "GLOSSARY.md"
    if not g.exists():
        return out
    for line in g.read_text().splitlines():
        m = re.match(r"^\|\s*\*\*(?P<t>[^|]+?)\*\*\s*\|\s*(?P<d>[^|]+?)\s*\|", line)
        if not m or "/" in m.group("t"):
            continue
        out.setdefault(_norm_term(m.group("t")), m.group("d").replace("\u25c6", "").strip())
    return out


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def registered_patterns():
    p = S.TK / "runtime/remotion/src/scenes.json"
    names = set()
    try:
        for s in json.loads(p.read_text())["scenes"]:
            names.add(s["id"])
    except Exception:
        pass
    planned = set()
    cs = SERIES / "COMPONENT-SPECS.md"
    if cs.exists():
        planned = set(re.findall(r"^### (\w+) \(NEW\)", cs.read_text(), re.M))
    return names, planned


def lint_film(slug, patterns, planned):
    film = S.folder(slug)
    errs, warns, info = [], [], {}
    if not film.exists():
        return {"slug": slug, "exists": False, "errors": ["folder missing"], "warnings": [], "info": {}}
    for f in REQUIRED_FILES:
        if not (film / f).exists():
            errs.append(f"missing file: {f}")
    if not (film / "lanes").exists() or not list((film / "lanes").glob("*.json")):
        errs.append("missing lanes/*.json")
    if errs and not (film / "narration.py").exists():
        return {"slug": slug, "exists": True, "errors": errs, "warnings": warns, "info": info}
    try:
        N = load_module(film / "narration.py", f"narration_{slug.replace('-', '_')}")
    except Exception as e:  # noqa: BLE001
        return {"slug": slug, "exists": True, "errors": errs + [f"narration.py does not import: {e}"], "warnings": warns, "info": info}

    if N.SLUG != S.full_slug(slug):
        errs.append(f"SLUG {N.SLUG!r} != folder {S.full_slug(slug)!r}")
    lines = getattr(N, "TITLE_LINES", [N.TITLE])
    if len(lines) > 3 or any(len(x) > 28 for x in lines):
        errs.append(f"TITLE_LINES must be <=3 lines of <=28 chars: {lines}")
    if "".join(lines).replace(" ", "") != N.TITLE.replace(" ", ""):
        warns.append("TITLE_LINES do not spell TITLE")
    if len(N.OPENING_DESCRIPTION) > 52:
        errs.append(f"OPENING_DESCRIPTION is {len(N.OPENING_DESCRIPTION)} chars (max 52)")
    # "3D" in a title is fine for the voice (Kokoro reads it as "three D", checked by the Shaders in 3D layout); other digits are not.
    if re.search(r"\d", re.sub(r"\b[23]D\b", "", N.TITLE) + N.OPENING_DESCRIPTION):
        errs.append("digit in title/opening description")
    spoken = getattr(N, "SPOKEN_TITLE", N.TITLE)
    if re.search(r"\b[A-Z]{2,}\b", spoken) and spoken == N.TITLE:
        warns.append(f"TITLE has an acronym ({N.TITLE!r}): set SPOKEN_TITLE in narration.py with spaced letters (BOPEN and BOUT narration use it)")

    # narration text
    all_text = {"BOPEN": N.BOPEN, "BIDEA": N.BIDEA, "BDEFS": N.BDEFS, "BVDT": N.BVDT_NARRATION, "BHTF": N.BHTF_NARRATION}
    ids = []
    for bid, ai, text in N.BODY:
        ids.append(bid)
        all_text[bid] = text
        n = len(text.split())
        if n > 60:
            errs.append(f"{bid}: {n} words (max 60): split it")
        elif n > 48:
            warns.append(f"{bid}: {n} words (over 48)")
        elif n < 10:
            warns.append(f"{bid}: only {n} words")
        longest = max((len(s.split()) for s in re.split(r"(?<=[.!?])\s+", text)), default=0)
        if longest > 30:
            warns.append(f"{bid}: a {longest}-word sentence (hard to say aloud)")
    expect = [f"B{i:02d}" for i in range(1, len(N.BODY) + 1)]
    if ids != expect:
        errs.append("body beat ids must run B01, B02, ... with no gaps")
    for bid, text in all_text.items():
        for pat, why in FORBIDDEN:
            if bid == "BOPEN" and "playlist" in why:
                continue
            m = re.search(pat, text, re.I)
            if m:
                errs.append(f"{bid}: {why} ('{m.group(0)}')")
        digits = re.findall(r"\d+(?:\.\d+)*", re.sub(r"\b[23]D\b", "", text) if bid == "BOPEN" else text)
        if digits:
            warns.append(f"{bid}: digits in narration {digits[:4]} (write numbers as words for the voice)")
        for pat, why in WORD_ERRORS:
            m = re.search(pat, text)
            if m:
                errs.append(f"{bid}: {why} ('{m.group(0)}')")
        for pat, why in WORD_WARNINGS:
            m = re.search(pat, text, re.I)
            if m and not ("pixel shader" in why and "fragment" in text.lower()):   # the beat that explains the two names is allowed
                warns.append(f"{bid}: {why} ('{m.group(0)}')")
    glsl_beats = [b for b, t in all_text.items() if re.search(r"\bG L S L\b|\bGLSL\b", t)]
    if len(glsl_beats) > 1:
        warns.append(f"GLSL is mentioned in {len(glsl_beats)} beats {glsl_beats} (at most once per film, as 'close to G L S L')")
    if not N.BIDEA.startswith(f"{getattr(N, 'GREETING', 'Hallo')}. This is Liam, in for Bear."):
        errs.append("BIDEA must open 'Hallo. This is Liam, in for Bear.' (GREETING constant)")
    if not N.BVDT_NARRATION.startswith("Let's recap with Claude."):
        errs.append("BVDT_NARRATION must open \"Let's recap with Claude.\"")
    if len(N.BVDT_LINES) not in (4, 6):
        errs.append(f"BVDT_LINES must be 4 or 6 lines, got {len(N.BVDT_LINES)}")
    if not N.BHTF_NARRATION.startswith("Your turn."):
        errs.append("BHTF_NARRATION must open 'Your turn.'")
    if N.BHTF_PROMPT not in N.BHTF_NARRATION:
        errs.append("BHTF_PROMPT must appear word for word inside BHTF_NARRATION (the prompt is read in full)")
    if len(N.BHTF_CHECKS) != 2:
        errs.append("BHTF_CHECKS must be exactly two lines")
    if not (3 <= len(N.BDEFS_TERMS) <= 6):
        errs.append(f"BDEFS_TERMS must be 3 to 6, got {len(N.BDEFS_TERMS)}")
    for t, m in N.BDEFS_TERMS:
        if len(t) > 17:
            errs.append(f"term {t!r} is {len(t)} chars (max 17: longer ones truncate and no gate catches it)")
        if len(m) > 72:
            warns.append(f"term {t!r}: meaning is {len(m)} chars (keep it to one short line)")
    canon = canon_defs()
    for t, m in N.BDEFS_TERMS:
        c = canon.get(_norm_term(t))
        if c and _norm_def(m) != _norm_def(c):
            warns.append(f"term {t!r}: card wording differs from GLOSSARY ({m!r} vs {c!r})")
    txt, trig, repl = N.BIDEA_TEXT
    if trig not in txt:
        errs.append("BIDEA_TEXT trigger is not verbatim in the text")
    if trig[-1:] in ".,;:!?" or repl[-1:] in ".,;:!?":
        errs.append("BIDEA_TEXT trigger/replacement must not end in punctuation (the correction would never fire)")

    # acts and size
    if not (3 <= len(N.ACTS) <= 5):
        warns.append(f"{len(N.ACTS)} acts (3 to 5 expected for a ten-minute film)")
    for ai, (num, title) in enumerate(N.ACTS):
        c = sum(1 for _, a, _ in N.BODY if a == ai)
        if c < 4 or c > 12:
            warns.append(f"act {num} has {c} beats (4 to 12 expected)")
        if num != ROMAN[ai]:
            errs.append(f"act {ai} numeral is {num!r}, expected {ROMAN[ai]!r}")
    words = sum(len(t.split()) for t in all_text.values()) + 3 * len(N.BDEFS_TERMS)
    minutes = (words * S.SEC_PER_WORD + 4.0) / 60.0
    info.update({"beats": len(N.BODY) + 6, "body": len(N.BODY), "words": words, "minutes": round(minutes, 1)})
    if minutes > S.HARD_MAX:
        errs.append(f"estimated {minutes:.1f} min exceeds the {S.HARD_MAX:g}-minute ceiling: cut")
    elif minutes > S.TARGET_MAX + 1.0:
        warns.append(f"estimated {minutes:.1f} min is over the preferred band ({S.TARGET_MIN:g} to {S.TARGET_MAX:g}); name the cut line")
    elif minutes < S.TARGET_MIN - 2.0:
        warns.append(f"estimated {minutes:.1f} min is short of the preferred band")
    if not (34 <= len(N.BODY) <= 52):
        warns.append(f"{len(N.BODY)} body beats (34 to 52 expected)")

    # lanes
    lanes = {}
    for f in sorted(glob.glob(str(film / "lanes" / "*.json"))):
        try:
            lanes.update(json.loads(Path(f).read_text()))
        except Exception as e:  # noqa: BLE001
            errs.append(f"{Path(f).name} is not valid JSON: {e}")
    classes = set()
    lane_hist = {}
    for bid in ids:
        L = lanes.get(bid)
        if not L:
            errs.append(f"{bid}: no lane entry")
            continue
        lane = L.get("lane")
        lane_hist[lane] = lane_hist.get(lane, 0) + 1
        for k, minlen in (("visual_intent", 40), ("motion_claim", 20), ("runner_up", 5), ("why", 12)):
            if len(str(L.get(k, ""))) < minlen:
                errs.append(f"{bid}: lane entry needs a real '{k}'")
        sh = L.get("show")
        if not sh or not all(isinstance(x, dict) and "at" in x and "event" in x for x in sh):
            errs.append(f"{bid}: 'show' must list {{at, event}} cues")
        if lane == "manim":
            c = L.get("class", "")
            if not c.startswith(bid + "_"):
                errs.append(f"{bid}: manim class must start with '{bid}_', got {c!r}")
            if c in classes:
                errs.append(f"{bid}: duplicate manim class {c}")
            classes.add(c)
        elif lane in ("remotion", "capture", "card", "terminal", "show-tell", "editor"):
            p = L.get("pattern")
            if not p:
                errs.append(f"{bid}: remotion lane needs 'pattern'")
            elif p not in patterns and p not in planned:
                errs.append(f"{bid}: pattern {p!r} is not a registered scene or a '### {p} (NEW)' in COMPONENT-SPECS.md")
            if not isinstance(L.get("props", {}), dict):
                errs.append(f"{bid}: props must be an object")
            if lane == "capture" and not L.get("capture_spec"):
                errs.append(f"{bid}: capture lane needs a capture_spec")
            props = L.get("props", {}) if isinstance(L.get("props", {}), dict) else {}
            if p == "LectureCodeTrace" and len(str(props.get("code", "")).split("\n")) > 10:
                errs.append(f"{bid}: LectureCodeTrace holds about 10 lines at 4K, this has {len(str(props.get('code', '')).split(chr(10)))}")
            if p == "ShaderLab" and len(str(props.get("code", "")).split("\n")) > 14:
                errs.append(f"{bid}: ShaderLab code is limited to 14 lines")
            if p == "LectureEvidenceTable":
                if not (1 <= len(props.get("rows", [])) <= 4) or not (2 <= len(props.get("headers", [])) <= 4):
                    errs.append(f"{bid}: LectureEvidenceTable takes 1 to 4 rows and 2 to 4 headers")
        else:
            errs.append(f"{bid}: unknown lane {lane!r}")
    info["lanes"] = lane_hist
    blob = json.dumps(lanes)
    for ref in sorted(set(re.findall(r"lab-shaders/[\w\-./]+\.gdshader", blob))):
        if not (film / ref).exists():
            errs.append(f"lane points at {ref} but the file does not exist")
    if not (film / "lab-shaders").exists():
        warns.append("no lab-shaders/ folder (every shader shown on screen should be a tested file there)")
    if not (film / "evidence/planning-checks").exists():
        warns.append("no evidence/planning-checks/ (claims should be backed by runs or cited docs)")

    # paperwork
    sl = (film / "SHOTLIST.md").read_text() if (film / "SHOTLIST.md").exists() else ""
    for bid in ids:
        if not re.search(rf"^\|\s*{bid}\s*\|", sl, re.M):
            errs.append(f"SHOTLIST.md has no row for {bid}")
    fc = (film / "FACTCHECK.md").read_text() if (film / "FACTCHECK.md").exists() else ""
    rows = re.findall(r"^\|\s*[\w\-]+\s*\|[^|]*\|[^|]*\|\s*(PASS|CORRECTED|EXEMPT|OPEN)\s*\|", fc, re.M)
    info["factcheck_rows"] = len(rows)
    if len(rows) < 12:
        errs.append(f"FACTCHECK.md has {len(rows)} verdict rows (expected at least 12)")
    if rows.count("OPEN"):
        warns.append(f"FACTCHECK.md has {rows.count('OPEN')} OPEN rows (unverified claims)")
    for f in ("ACTS.md", "SHOTLIST.md", "FACTCHECK.md", "CHECKS-REPORT.md", "SOURCES.md", "CAPTURE-PLAN.md", "BUILD-PROMPT.md"):
        pth = film / f
        if pth.exists():
            head = "\n".join(pth.read_text().splitlines()[:14])
            if not (re.search(r"\*\*What", head) and re.search(r"\*\*Found", head)):
                warns.append(f"{f} does not open with a What / Why / Found summary")
    bp = (film / "BUILD-PROMPT.md").read_text() if (film / "BUILD-PROMPT.md").exists() else ""
    if bp and not re.search(r"(?i)do not publish|never publish|no publishing", bp):
        errs.append("BUILD-PROMPT.md must say not to publish")
    return {"slug": slug, "exists": True, "errors": errs, "warnings": warns, "info": info}


def main(argv):
    report = "--report" in argv
    slugs = [a for a in argv if not a.startswith("--")] or [s for s, _, _ in S.FILMS if S.folder(s).exists()]
    patterns, planned = registered_patterns()
    results = [lint_film(s, patterns, planned) for s in slugs]
    ok = 0
    print(f"{'film':34} {'beats':>5} {'words':>6} {'min':>5}  err warn")
    for r in results:
        i = r["info"]
        print(f"{r['slug']:34} {i.get('beats', '-'):>5} {i.get('words', '-'):>6} {i.get('minutes', '-'):>5}  {len(r['errors']):>3} {len(r['warnings']):>4}")
        ok += not r["errors"]
    for r in results:
        for e in r["errors"]:
            print(f"ERROR   {r['slug']}: {e}")
    for r in results:
        for w in r["warnings"]:
            print(f"warn    {r['slug']}: {w}")
    print(f"\n{ok}/{len(results)} films clean of errors")
    if report:
        L = ["# Layout lint report\n",
             "**What this is.** The machine checks of every shader film's layout (length band, beat sizes, forbidden words, bookend rules, lane entries, file set).\n",
             "**Why.** So the review does not have to count words or hunt for a stray \"the book\".\n",
             f"**Found.** {ok} of {len(results)} films have no errors. Warnings are judgment calls, listed per film.\n",
             "| Film | Beats | Words | Est. min | Errors | Warnings |", "|---|---|---|---|---|---|"]
        for r in results:
            i = r["info"]
            L.append(f"| {r['slug']} | {i.get('beats', '-')} | {i.get('words', '-')} | {i.get('minutes', '-')} | {len(r['errors'])} | {len(r['warnings'])} |")
        for r in results:
            if r["errors"] or r["warnings"]:
                L.append(f"\n## {r['slug']}\n")
                L += [f"- ERROR: {e}" for e in r["errors"]] + [f"- warn: {w}" for w in r["warnings"]]
        (SERIES / "LINT-REPORT.md").write_text("\n".join(L) + "\n")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
