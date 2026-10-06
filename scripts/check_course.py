#!/usr/bin/env python3
"""Check CSYE 7270 course files against pantry/course-build-spec.md.

Usage:
  python3 scripts/check_course.py                 # every module and assignment file
  python3 scripts/check_course.py modules/04-*    # one module folder (glob ok)
  python3 scripts/check_course.py assignments/05-shader-and-material.md

Exit code 1 if any FAIL. WARN lines are judgment calls for a human.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

LESSON_H2 = [
    "Executive summary",
    "The question",
    "The ideas",
    "The Walker example",          # prefix match
    "Predict → Build It → Use It → Ship It → Verify",
    "What the agents got wrong",
    "If you know Unity or Unreal",
    "Practice assessment (ungraded)",
    "The next step",
]
STEP_H3 = ["1. Predict", "2. Build It", "3. Use It", "4. Ship It", "5. Verify"]
LINKS_H2 = ["Executive summary", "Read first", "Godot documentation", "Walker projects", "Tools", "Going deeper"]
ASSIGN_H2 = [
    "Executive summary",
    "Your task",
    "1. Predict",
    "2. Build It",
    "3. Use It",
    "4. Ship It",
    "5. Verify and submit to Canvas",
    "Rubric — 100 points",
    "You must be able to explain it",
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅❌]")
FILLER = re.compile(r"\b(In this (module|assignment|lesson) we will|let's explore|delve)\b", re.I)

# Written before the spec; checked leniently (their text was approved as drafted).
LEGACY = {
    "assignments/01-extend-walker-jumpman.md",
    "assignments/02-generate-art-sound-music-for-your-game.md",
}

fails, warns = [], []


def fail(path, msg):
    rel = os.path.relpath(path, ROOT)
    if rel in LEGACY:
        warns.append(f"WARN(legacy) {rel}: {msg}")
        return
    fails.append(f"FAIL {rel}: {msg}")


def warn(path, msg):
    warns.append(f"WARN {os.path.relpath(path, ROOT)}: {msg}")


def strip_code(text):
    """Return (prose_without_fences_and_inline_code, list_of_fences)."""
    fences = []

    def grab(m):
        fences.append((m.group(1).strip(), m.group(2)))
        return "\n"

    prose = re.sub(r"^```([^\n]*)\n(.*?)^```[ \t]*$", grab, text, flags=re.S | re.M)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    return prose, fences


def headings(text, level):
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("#" * level + " "):
            out.append(line[level + 1:].strip())
    return out


def words(prose):
    return len(re.findall(r"\S+", prose))


def common_checks(path, text):
    prose, fences = strip_code(text)
    for lang, body in fences:
        if not lang:
            fail(path, "fenced code block without a language tag")
    if re.search(r"<\/?[a-zA-Z][^>]*>", prose):
        fail(path, "raw HTML in prose: " + re.search(r"<\/?[a-zA-Z][^>]*>", prose).group(0))
    if EMOJI.search(text):
        fail(path, "emoji")
    if FILLER.search(prose):
        warn(path, "filler phrase: " + FILLER.search(prose).group(0))
    if re.search(r"!\[[^\]]*\]\(", prose):
        fail(path, "image embed (no images allowed)")
    base = os.path.dirname(path)
    for m in re.finditer(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", prose):
        url = m.group(1)
        if url.startswith("#"):
            continue
        if url.startswith("https://"):
            continue
        if url.startswith("http://") or url.startswith("mailto:") or "://" in url:
            fail(path, "non-https link: " + url)
            continue
        target = os.path.normpath(os.path.join(base, url.split("#")[0]))
        if not os.path.exists(target):
            fail(path, "relative link does not resolve: " + url)
    for lang, body in fences:
        if lang == "bash":
            logical, cur = [], ""
            for line in body.splitlines():
                s = line.rstrip()
                if not s.strip() or s.strip().startswith("#"):
                    continue
                if s.endswith("\\"):
                    cur += s[:-1] + " "
                    continue
                logical.append((cur + s).strip())
                cur = ""
            if cur:
                logical.append(cur.strip())
            if len(logical) > 1:
                warn(path, f"bash block with {len(logical)} commands (spec: one per block): {logical[0][:50]}…")
    return prose


def check_exec_summary_first(path, text):
    h1 = headings(text, 1)
    h2 = headings(text, 2)
    if not h1:
        fail(path, "no H1 title")
    if not h2 or h2[0] != "Executive summary":
        fail(path, "first H2 must be 'Executive summary', got: " + (h2[0] if h2 else "none"))


def check_lesson(path, full=True):
    text = open(path, encoding="utf-8").read()
    prose = common_checks(path, text)
    h1 = headings(text, 1)
    if h1 and not re.match(r"Module \d+ — ", h1[0]):
        fail(path, f"H1 should start 'Module N — ', got: {h1[0]}")
    check_exec_summary_first(path, text)
    n = words(prose)
    if full:
        h2 = headings(text, 2)
        # required headings must appear, in order
        pos = -1
        for req in LESSON_H2:
            idx = next((i for i, h in enumerate(h2) if h == req or (req == "The Walker example" and h.startswith(req))), None)
            if idx is None:
                fail(path, "missing H2: " + req)
            elif idx < pos:
                fail(path, "H2 out of order: " + req)
            else:
                pos = idx
        h3 = headings(text, 3)
        for s in STEP_H3:
            if s not in h3:
                fail(path, "missing H3: " + s)
        if n < 2000:
            fail(path, f"too short: {n} words (spec 2,200–3,400)")
        elif n < 2200:
            warn(path, f"slightly short: {n} words (spec 2,200–3,400)")
        if n > 3800:
            fail(path, f"too long: {n} words (spec 2,200–3,400)")
        elif n > 3400:
            warn(path, f"slightly long: {n} words (spec 2,200–3,400)")
    else:
        if n < 800:
            fail(path, f"too short: {n} words")
    return n


def check_links(path):
    text = open(path, encoding="utf-8").read()
    common_checks(path, text)
    h1 = headings(text, 1)
    if h1 and not re.match(r"Module \d+ — Helpful links", h1[0]):
        fail(path, f"H1 should be 'Module N — Helpful links', got: {h1[0]}")
    check_exec_summary_first(path, text)
    h2 = headings(text, 2)
    for req in LINKS_H2:
        if req not in h2:
            fail(path, "missing H2: " + req)
    entries = re.findall(r"^- \[[^\]]+\]\((?:https://|\.\./)[^)]+\) — .+$", text, flags=re.M)
    bullets = re.findall(r"^- ", text, flags=re.M)
    if len(entries) != len(bullets):
        fail(path, f"{len(bullets) - len(entries)} bullet(s) not in the form '- [Title](https://…) — why'")
    if not 10 <= len(entries) <= 18:
        fail(path, f"{len(entries)} link entries (spec 10–18)")
    urls = re.findall(r"\]\((https://[^)\s]+)\)", text)
    if len(urls) != len(set(urls)):
        warn(path, "duplicate URL in the page")
    return len(entries)


def check_assessment(path):
    try:
        data = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        fail(path, "invalid JSON: " + str(e))
        return
    raw = open(path, encoding="utf-8").read()
    if "\n  " not in raw:
        fail(path, "JSON must be indented (2 spaces)")
    for k in ("title", "description", "questions"):
        if k not in data:
            fail(path, "missing key: " + k)
            return
    qs = data["questions"]
    if len(qs) != 6:
        fail(path, f"{len(qs)} questions (spec: exactly 6)")
    answers = []
    for i, q in enumerate(qs, 1):
        for k in ("prompt", "choices", "answer", "feedback"):
            if k not in q:
                fail(path, f"Q{i} missing {k}")
        ch = q.get("choices", [])
        if len(ch) != 4:
            fail(path, f"Q{i} has {len(ch)} choices (spec: 4)")
        a = q.get("answer")
        if not isinstance(a, int) or not 0 <= a < len(ch):
            fail(path, f"Q{i} answer index invalid: {a!r}")
        answers.append(a)
        if len(set(c.strip().lower() for c in ch)) != len(ch):
            fail(path, f"Q{i} has duplicate choices")
        for c in ch:
            if re.search(r"\b(all|none) of the above\b", c, re.I):
                fail(path, f"Q{i} uses 'all/none of the above'")
        if EMOJI.search(json.dumps(q, ensure_ascii=False)):
            fail(path, f"Q{i} contains emoji")
        if not 20 <= len(q.get("feedback", "")) <= 700:
            warn(path, f"Q{i} feedback length {len(q.get('feedback', ''))} (aim for 1–3 sentences)")
        longest = max(range(len(ch)), key=lambda j: len(ch[j])) if ch else -1
        if longest == a and len(ch) == 4 and len(ch[a]) > 1.6 * sorted(len(c) for c in ch)[-2]:
            warn(path, f"Q{i}: the correct answer is much longer than the others (a tell)")
    # The length tell: a test-wise student picks the longest, most hedged choice without reading.
    longest, ratios = 0, []
    for q in qs:
        ch = q.get("choices", [])
        a = q.get("answer")
        if len(ch) == 4 and isinstance(a, int) and 0 <= a < 4:
            if len(ch[a]) >= max(len(c) for c in ch):
                longest += 1
            others = [len(c) for i, c in enumerate(ch) if i != a]
            ratios.append(len(ch[a]) / (sum(others) / 3))
    if longest > 3:
        fail(path, f"the correct choice is the longest in {longest} of 6 questions (max 3): rebalance the distractors")
    if ratios and sum(ratios) / len(ratios) > 1.25:
        fail(path, f"the correct choice averages {sum(ratios)/len(ratios):.2f}x the length of the distractors (max 1.25)")
    if answers:
        from collections import Counter
        if max(Counter(answers).values()) > 2:
            fail(path, f"correct-answer position repeats more than twice: {answers}")


def table_points(section_text, header_hint):
    """Sum the Points column of the first table in section_text."""
    total, found = 0, False
    for line in section_text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and re.search(r"subtotal|total", cells[0], re.I):
                continue
            if cells and re.fullmatch(r"\*{0,2}\d+(\.\d+)?\*{0,2}", cells[-1]):
                found = True
                total += float(cells[-1].strip("*"))
    return total if found else None


def check_assignment(path):
    text = open(path, encoding="utf-8").read()
    prose = common_checks(path, text)
    check_exec_summary_first(path, text)
    h1 = headings(text, 1)
    if h1 and not re.match(r"Assignment \d+ - ", h1[0]):
        fail(path, f"H1 should start 'Assignment N - ', got: {h1[0]}")
    if "**100 points**" not in text:
        fail(path, "missing '**100 points**'")
    h2 = headings(text, 2)
    pos = -1
    for req in ASSIGN_H2:
        idx = next((i for i, h in enumerate(h2) if h == req or h.startswith(req)), None)
        if idx is None:
            fail(path, "missing H2: " + req)
        elif idx < pos:
            fail(path, "H2 out of order: " + req)
        else:
            pos = idx
    for need in ("Implementation and explanation", "Frictional", "GitHub version posting matching Canvas", "Relative Quartile"):
        if need not in text:
            fail(path, "rubric missing: " + need)
    # rubric arithmetic: the subdivision table under "### Implementation and explanation — 60 points"
    m = re.search(r"### Implementation and explanation — 60 points\n(.*?)(?=\n### )", text, flags=re.S)
    if not m:
        fail(path, "missing '### Implementation and explanation — 60 points' subsection")
    else:
        s = table_points(m.group(1), "Points")
        if s is None:
            fail(path, "no Points table in the 60-point subsection")
        elif abs(s - 60) > 1e-9:
            fail(path, f"60-point subdivision sums to {s:g}, not 60")
    m2 = re.search(r"## Rubric — 100 points\n(.*?)(?=\n### )", text, flags=re.S)
    if m2:
        s2 = table_points(m2.group(1), "Points")
        if s2 is None or abs(s2 - 100) > 1e-9:
            # Total rows are skipped, so the 60 + 10 + 10 + 20 rows must sum to 100
            warn(path, f"top rubric table did not parse as 60/10/10/20 + Total 100 (sum read {s2})")
    for must in ("SHA-256", "FRICTIONAL.md", "SOURCES.md", "TEST-REPORT.md", "CHANGE-BRIEF.md", "SUBMISSION"):
        if must not in text:
            fail(path, "missing required mention: " + must)
    if not re.search(r"\ba\d+\b", text) and "tag" not in text.lower():
        warn(path, "no mention of the git tag for this assignment")
    n = words(prose)
    if n < 1900:
        fail(path, f"too short: {n} words (spec 2,000–3,500)")
    if n > 5200:
        fail(path, f"too long: {n} words (spec 2,000–3,500)")
    elif n > 3800:
        warn(path, f"long: {n} words (spec 2,000–3,500)")
    return n


def targets(args):
    if not args:
        args = ["modules/*", "assignments/*.md"]
    out = []
    for a in args:
        out += glob.glob(os.path.join(ROOT, a))
    return sorted(set(out))


def main():
    args = sys.argv[1:]
    seen = 0
    for t in targets(args):
        if os.path.isdir(t):
            name = os.path.basename(t)
            if not re.match(r"\d\d-", name):
                continue
            for f in sorted(glob.glob(os.path.join(t, "*"))):
                b = os.path.basename(f)
                if b == "lesson.md":
                    n = check_lesson(f)
                    print(f"{os.path.relpath(f, ROOT)}: {n} words")
                elif re.match(r"(lesson-\d+|labs)\.md$", b):
                    n = check_lesson(f, full=False)
                    print(f"{os.path.relpath(f, ROOT)}: {n} words (extra page)")
                elif b == "links.md":
                    n = check_links(f)
                    print(f"{os.path.relpath(f, ROOT)}: {n} links")
                elif b == "assessment.json":
                    check_assessment(f)
                    print(f"{os.path.relpath(f, ROOT)}: checked")
                seen += 1
            if name != "01-walker-and-godot" or True:
                for req in ("lesson.md", "links.md", "assessment.json"):
                    if not os.path.exists(os.path.join(t, req)):
                        fail(os.path.join(t, req), "missing")
        elif t.endswith(".md") and re.match(r"\d\d-", os.path.basename(t)) and os.path.basename(os.path.dirname(t)) == "assignments":
            n = check_assignment(t)
            print(f"{os.path.relpath(t, ROOT)}: {n} words")
            seen += 1
    for w in warns:
        print(w)
    for f in fails:
        print(f)
    print(f"\n{seen} files checked, {len(fails)} FAIL, {len(warns)} WARN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
