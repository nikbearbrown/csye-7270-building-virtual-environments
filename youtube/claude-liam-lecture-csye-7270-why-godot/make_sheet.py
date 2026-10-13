#!/usr/bin/env python3
"""make_sheet.py — builds beat_sheet.json for the lecture. Safe to re-run: it carries audio_file / actual_duration_s forward
(only while the beat's narration text is unchanged) and fills every Remotion beat's durationSeconds from the measured audio.
Identical in all three "CSYE 7270: Start Here" films; everything film-specific is in narration.py.

  narration.py        every spoken line (the clock)
  lanes/*.json        per-beat lane decisions written by the act builders:
                      { "B03": {"lane": "manim", "class": "B03_GoodColumn", "visual_intent": "...", "motion_claim": "...",
                                "show": [{"at": 0.2, "event": "..."}], "runner_up": "...", "why": "...", "sparse": true},
                        "B14": {"lane": "remotion", "pattern": "CCPlainShell", "props": {...}, ...} }
                      A Remotion props value of "__AUDIO__" under durationSeconds is replaced by the measured audio.
A body beat with no lane entry is written as a pending Manim beat (compiles as a slate until a scene exists).
"""
import json, glob
from pathlib import Path
import narration as N

HERE = Path(__file__).resolve().parent
OUT = HERE / "beat_sheet.json"
prev = {}
if OUT.exists():
    for b in json.loads(OUT.read_text())["beats"]:
        prev[b["beat_id"]] = b

lanes = {}
for f in sorted(glob.glob(str(HERE / "lanes" / "*.json"))):
    lanes.update(json.loads(Path(f).read_text()))


def est(n):  # words / 2.5 per second
    return round(len(n.split()) / 2.5, 1)


def carry(b):
    p = prev.get(b["beat_id"])
    if p and p.get("narration_text") == b.get("narration_text"):
        for k in ("actual_duration_s", "audio_file"):
            if k in p:
                b[k] = p[k]
    return b


def fill_audio(props, dur):
    if isinstance(props, dict):
        return {k: (round(dur, 2) if v == "__AUDIO__" else fill_audio(v, dur)) for k, v in props.items()}
    if isinstance(props, list):
        return [fill_audio(v, dur) for v in props]
    return props


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate, "narration_text": narration,
         "estimated_duration_s": est(narration), "voice": "am_onyx", "engine": "kokoro", "persona": "liam",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    carry(b)
    dur = b.get("actual_duration_s")
    if dur:
        b["shot"]["remotion"]["props"] = fill_audio(b["shot"]["remotion"]["props"], dur)
    return b


beats = []

# ── BOPEN ─ the approved lecture first beat: portrait, title, series position; narrated playlist → title → summary ──────
bopen = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD", "narration_text": N.BOPEN,
         "estimated_duration_s": est(N.BOPEN), "voice": "am_onyx", "engine": "kokoro", "persona": "liam",
         "routing": {"about": "Film identity and payoff", "runner_up": "Minimal title card",
                     "reason": "The lecture skill's approved first beat: portrait, series position, entry pointer, honest narrator credit."},
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Professor Bear portrait, exact film title, short payoff, series and position visible immediately.",
                  "show": [{"at": 0, "event": "Complete populated lecture opener visible for the whole narration"}]},
         "qc": {"sparse_by_design": True, "sparse_reason": "Identity card: portrait, title, series; teaching motion resumes in BIDEA."}}
beats.append(carry(bopen))

# ── BIDEA ─ hesitant writer: greeting + what the topic is about ───────────────────────────────────────
txt, trig, repl = N.BIDEA_TEXT
beats.append(remotion("BIDEA", "the question", N.BIDEA, "BrutalistHesitantWriter",
    {"text": txt, "triggerWords": trig, "replacementWords": repl,
     "fontSize": 66, "charMs": 24, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 4, "jitter": 20,
     "seed": N.SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the shortcut assumption"},
     {"at": 0.62, "event": f"backspaces '{trig}' and types '{repl}'"}],
    lead_silence_s=0.8,
    motion_claim="The writer types the shortcut assumption and corrects it into the film's real stance.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}))

# ── BDEFS ─ key terms ───────────────────────────────────────────────────────────────────────────────────
beats.append(remotion("BDEFS", "terms", N.BDEFS, "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": t, "meaning": m} for t, m in N.BDEFS_TERMS],
     "durationSeconds": "__AUDIO__", "folderLabel": "@NikBearBrown"},
    [{"at": 0.1 + 0.18 * i, "event": f"'{t}' lands"} for i, (t, _) in enumerate(N.BDEFS_TERMS)],
    gate="CARD", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: five prerequisites, one plain line each."}))

# ── BODY ─ one best visual per beat (lanes/*.json) ──────────────────────────────────────────────────────
for bid, ai, text in N.BODY:
    act = f"{N.ACTS[ai][0]} · {N.ACTS[ai][1]}"
    L = lanes.get(bid)
    if L is None:
        b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW", "narration_text": text,
             "estimated_duration_s": est(text), "voice": "am_onyx", "engine": "kokoro", "persona": "liam",
             "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": "PENDING — no lane entry yet", "show": [],
                      "manim": {"class": f"{bid}_Pending"}, "motion_claim": "pending"},
             "pending": True}
        beats.append(carry(b))
        continue
    lane = L["lane"]
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": L.get("proof_gate", "SHOW"), "narration_text": text,
         "estimated_duration_s": est(text), "voice": "am_onyx", "engine": "kokoro", "persona": "liam"}
    if lane == "manim":
        b["shot"] = {"type": "GRAPHIC", "source": "own", "visual_intent": L["visual_intent"], "show": L.get("show", []),
                     "manim": {"class": L["class"]}, "motion_claim": L["motion_claim"]}
    else:  # remotion / capture / card
        b["shot"] = {"type": "REMOTION", "source": "own", "visual_intent": L["visual_intent"], "show": L.get("show", []),
                     "remotion": {"pattern": L["pattern"], "props": L.get("props", {})}, "motion_claim": L["motion_claim"]}
    if L.get("sparse", True):
        b["qc"] = {"sparse_by_design": True, "sparse_reason": L.get("sparse_reason",
                   "Lecture body beat: one object or scene on a cream stage with the voice carrying the explanation; only underfill/clustered are waived.")}
    for k in ("lead_silence_s", "tail_silence_s", "kind"):
        if k in L:
            b[k] = L[k]
    b["lecture"] = {"runner_up": L.get("runner_up", ""), "why": L.get("why", "")}
    carry(b)
    dur = b.get("actual_duration_s")
    if dur and lane != "manim":
        b["shot"]["remotion"]["props"] = fill_audio(b["shot"]["remotion"]["props"], dur)
    beats.append(b)

# ── BVDT ─ recap (six lines: the card paginates in twos) ────────────────────────────────────────────────
beats.append(remotion("BVDT", "verdict", N.BVDT_NARRATION, "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": N.BVDT_HEADING, "artifactLines": N.BVDT_LINES},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.2, "event": "six recap lines land in narration order"}],
    lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."}))

# ── BHTF ─ your turn ───────────────────────────────────────────────────────────────────────────────────────
beats.append(remotion("BHTF", "your turn", N.BHTF_NARRATION, "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": N.BHTF_SEGMENT, "command": N.BHTF_PROMPT,
     "runningText": "paste this into Claude…", "output": N.BHTF_CHECKS,
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.12, "event": "the prompt types in full"},
     {"at": 0.85, "event": "two check lines land"}]))

# ── BOUT ─ channel outro (claude-liam → ClaudeTitleOutro, OUTRO-LOCK) ───────────────────────────────────────
bout = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
        "narration_text": f"{N.TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro", "persona": "liam",
        "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                 "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": N.TITLE, "slug": N.SLUG, "handle": "@NikBearBrown", "subline": ""}}},
        "kind": "outro_voice", "tail_silence_s": 1.0}
beats.append(carry(bout))

sheet = {"metadata": {
    "slug": N.SLUG, "title": N.TITLE, "topic": N.TOPIC, "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "sidecar", "greeting_language": N.GREETING,
    "course": N.COURSE, "audience": "students starting CSYE 7270, and anyone directing an AI agent to build a game",
    "series_title": N.SERIES, "series_video_number": N.VIDEO_NUMBER, "series_video_count": N.VIDEO_COUNT,
    "series_entry_video": "Video 1 · Conducting AI for Games",
    "lecture_opening_description": N.OPENING_DESCRIPTION,
    "lecture_opening_template": "lecture-title-slide-16x9",
    "lecture_opening_title_lines": N.TITLE_LINES,
    "bookend_exempt": ["cold-open", "bvdt"],
    "bookend_exempt_reason": "lecture skill: opens on the narrated identity card then the hesitant writer; no composer cold open.",
    "source_doc": "csye-7270-building-virtual-environments/youtube/_conducting-series-evidence/ (real Walker records, a real publisher run, a real no-bridge Godot demo, live captures); request was Bear's, 2026-10-09",
    "tags": N.TAGS},
    "beats": beats}
OUT.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
pend = sum(1 for b in beats if b.get("pending"))
print(len(beats), "beats;", pend, "pending; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in beats)), "s")
