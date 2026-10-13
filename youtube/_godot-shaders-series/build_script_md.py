"""build_script_md.py — writes SCRIPT.md, the human review script of one film (called by make_sheet_shared.main).

Executive summary first (what / why / found), then an act map, then every beat: the exact words Liam will say, the picture,
the motion, the runner-up lane. Generated from narration.py + lanes/*.json, so it can never drift from the beat sheet.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import series_config as S  # noqa: E402


def _words(t):
    return len(t.split())


def _mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def write(film_dir, N, sheet, lanes):
    beats = sheet["beats"]
    by_id = {b["beat_id"]: b for b in beats}
    body = [b for b in beats if b["beat_id"] not in ("BOPEN", "BIDEA", "BDEFS", "BVDT", "BHTF", "BOUT")]
    total_words = sum(_words(b["narration_text"]) for b in beats)
    est_total = total_words * S.SEC_PER_WORD + 4.0
    lane_hist = {}
    for b in body:
        lane_hist[b["lane"]] = lane_hist.get(b["lane"], 0) + 1
    hist = ", ".join(f"{k} {v}" for k, v in sorted(lane_hist.items(), key=lambda kv: -kv[1]))
    L = []
    L.append(f"# Script: {N.TITLE}\n")
    L.append(f"**What this is.** The words Liam will say in *{N.TITLE}*, beat by beat, each with the picture it gets. "
             "This is the layout stage: nothing is voiced, captured or rendered yet.\n")
    L.append("**Why.** So the whole film can be read, and changed, before anyone builds it. A change to a line is cheap now and "
             "expensive after the audio and the 4K render.\n")
    L.append(f"**Found.** {len(beats)} beats, {total_words} words, about **{_mmss(est_total)}** at Liam's measured pace "
             f"({S.SEC_PER_WORD} s per word, median of 57 shipped films). Preferred band {S.TARGET_MIN:g} to {S.TARGET_MAX:g} minutes, "
             f"ceiling {S.HARD_MAX:g}. Body lanes: {hist}.")
    cut = getattr(N, "CUT_LINE", "")
    if cut:
        L.append(f"\n**If it runs long.** {cut}")
    L.append("\n**How to read it.** Blockquotes are the spoken words, exactly as they will be sent to the voice. "
             "Numbers are written as words because the voice engine reads them better that way; the screen shows the real figures. "
             "Letters in an acronym are spaced for the same reason. \"Picture\" is what is on screen; \"Motion\" is the thing "
             "the voice can point at.\n")
    L.append("## Act map\n")
    L.append("| Act | Title | Beats | Words | About |")
    L.append("|---|---|---|---|---|")
    for ai, (num, title) in enumerate(N.ACTS):
        ids = [bid for bid, a, _ in N.BODY if a == ai]
        w = sum(_words(t) for bid, a, t in N.BODY if a == ai)
        L.append(f"| {num} | {title} | {len(ids)} | {w} | ~{_mmss(w * S.SEC_PER_WORD)} |")
    L.append("")

    def block(b, label=None):
        L.append(f"### {b['beat_id']}{(' · ' + label) if label else ''} · {_words(b['narration_text'])} words · ~{b['estimated_duration_s']:.0f} s")
        L.append("")
        L.append("> " + b["narration_text"].replace("\n", "\n> "))
        L.append("")

    L.append("## Opening\n")
    block(by_id["BOPEN"], "identity card")
    L.append(f"*Picture.* Portrait of Professor Bear (random square portrait, seeded by the film slug), the title \"{N.TITLE}\", "
             f"and the line \"{N.OPENING_DESCRIPTION}\".\n")
    block(by_id["BIDEA"], "the question")
    txt, trig, repl = N.BIDEA_TEXT
    L.append(f"*Picture.* The hesitant writer types: \"{txt}\" then deletes \"{trig}\" and types \"{repl}\".\n")
    block(by_id["BDEFS"], "terms")
    L.append("*Picture.* \"Terms In This Lecture\": " + "; ".join(f"**{t}** — {m}" for t, m in N.BDEFS_TERMS) + "\n")

    cur = -1
    for bid, ai, text in N.BODY:
        if ai != cur:
            cur = ai
            L.append(f"## Act {N.ACTS[ai][0]}: {N.ACTS[ai][1]}\n")
        b = by_id[bid]
        block(b)
        lecture = b.get("lecture", {})
        shot = b["shot"]
        L.append(f"*Picture.* {shot.get('visual_intent', '')}")
        L.append("")
        L.append(f"*Motion.* {shot.get('motion_claim', '')}")
        L.append("")
        lane_line = f"*Lane.* {b['lane']}"
        if shot.get("remotion"):
            lane_line += f" · `{shot['remotion']['pattern']}`"
        if shot.get("manim"):
            lane_line += f" · `{shot['manim']['class']}`"
        if lecture.get("runner_up"):
            lane_line += f" · runner-up: {lecture['runner_up']}"
        L.append(lane_line)
        cs = lecture.get("capture_spec")
        if cs:
            L.append("")
            L.append(f"*Capture to record.* {cs if isinstance(cs, str) else cs.get('summary', cs)}")
        L.append("")

    L.append("## Closing\n")
    block(by_id["BVDT"], "recap")
    L.append("*Picture.* The recap card: " + " / ".join(N.BVDT_LINES) + "\n")
    block(by_id["BHTF"], "your turn")
    L.append(f"*Prompt shown and read in full:* {N.BHTF_PROMPT}\n")
    L.append("*Two checks:* " + " · ".join(N.BHTF_CHECKS) + "\n")
    block(by_id["BOUT"], "outro")
    L.append("*Picture.* The locked channel outro card: exact title, handle, one mascot. Followed by a one-second silent tail.\n")
    (Path(film_dir) / "SCRIPT.md").write_text("\n".join(L) + "\n")
