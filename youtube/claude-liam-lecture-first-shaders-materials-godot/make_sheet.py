#!/usr/bin/env python3
"""make_sheet.py — builds beat_sheet.json for the lecture. Safe to re-run BEFORE `art run` / `art final`: it carries audio_file / actual_duration_s forward
and fills every Remotion beat's durationSeconds from the measured audio (or, before audio exists, from the estimate).

  narration.py        every spoken line (the clock)
  lanes/*.json        per-beat lane decisions written by the act builders:
                      { "B05": {"lane": "manim", "class": "B05_Language", "visual_intent": "...", "motion_claim": "...",
                                "show": [{"at": 0.2, "event": "..."}], "runner_up": "...", "why": "...", "sparse": true},
                        "B20": {"lane": "remotion", "pattern": "CCPlainShell", "props": {...}, ...} }
                      A Remotion props value of "__AUDIO__" under durationSeconds is replaced by the measured audio (estimate until audio exists).
A body beat with no lane entry is written as a pending Manim beat (compiles as a slate until a scene exists).

NEVER re-run this after `art final` (it rewrites the sheet and clears the build stamps). After audio generation, re-run it once to refill the Remotion durations.
"""
import json, glob
from pathlib import Path
import narration as N

HERE = Path(__file__).resolve().parent
OUT = HERE / "beat_sheet.json"
WPS = 3.2          # measured pace of Liam (Kokoro am_onyx) in the sibling films: 3.2 words/second (2.6-3.4 across films). Pacing estimate only; audio is the clock.
prev = {}
if OUT.exists():
    for b in json.loads(OUT.read_text())["beats"]:
        prev[b["beat_id"]] = b

lanes = {}
for f in sorted(glob.glob(str(HERE / "lanes" / "*.json"))):
    lanes.update(json.loads(Path(f).read_text()))


def est(n):
    return round(len(n.split()) / WPS, 2)


def carry(b):
    p = prev.get(b["beat_id"])
    if p:
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


def clock(b):
    return b.get("actual_duration_s") or b["estimated_duration_s"]


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate, "narration_text": narration,
         "estimated_duration_s": est(narration), "voice": "am_onyx", "engine": "kokoro", "persona": "liam",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    carry(b)
    b["shot"]["remotion"]["props"] = fill_audio(b["shot"]["remotion"]["props"], clock(b))
    return b


beats = []

# ── BOPEN ─ narrated portrait/title slide (lecture-title-slide-16x9; BOPEN contract: playlist -> film name -> brief summary) ─────────────────────────────────
bopen = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD", "narration_text": N.BOPEN,
         "estimated_duration_s": est(N.BOPEN), "voice": "am_onyx", "engine": "kokoro", "persona": "liam",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Professor Bear portrait, course playlist and exact film title visible immediately",
                  "show": [{"at": 0, "event": "Complete portrait/title card holds for the measured narration"}]}}
beats.append(carry(bopen))

# ── BIDEA ─ hesitant writer: greeting + the misconception the film corrects ───────────────────────────────────────────────────────────────────────────
beats.append(remotion("BIDEA", "Opening", N.BIDEA, "BrutalistHesitantWriter",
    {"text": "The tests pass,\nso the shader looks right.",
     "triggerWords": "so the shader looks right", "replacementWords": "so the shader is wired, and my eyes judge the look",
     "fontSize": 66, "charMs": 24, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 4, "jitter": 20,
     "seed": N.SLUG, "banner": "", "durationSeconds": "__AUDIO__"},
    [{"at": 0.0, "event": "types 'The tests pass,'"},
     {"at": 0.62, "event": "backspaces 'so the shader looks right' and types 'so the shader is wired, and my eyes judge the look'"}],
    lead_silence_s=0.8,
    motion_claim="The writer types the belief a newcomer arrives with and corrects it into the assignment's real stance.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}))

# ── BDEFS ─ key terms (prerequisites only, <= 17 characters each) ─────────────────────────────────────────────────────────────────────────────────────
beats.append(remotion("BDEFS", "Opening", N.BDEFS, "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "GPU", "meaning": "the chip that draws graphics"},
               {"term": "pixel", "meaning": "one dot of the image"},
               {"term": "uniform", "meaning": "a value game code hands a shader"},
               {"term": "renderer", "meaning": "the part of Godot that draws"},
               {"term": "headless", "meaning": "running Godot with no window"},
               {"term": "mutation", "meaning": "a deliberate break, to test a test"}],
     "folderLabel": "@NikBearBrown", "durationSeconds": "__AUDIO__"},
    [{"at": 0.1, "event": "'GPU' lands"}, {"at": 0.25, "event": "'pixel' lands"}, {"at": 0.42, "event": "'uniform' lands"},
     {"at": 0.58, "event": "'renderer' lands"}, {"at": 0.74, "event": "'headless' lands"}, {"at": 0.88, "event": "'mutation' lands"}],
    gate="CARD", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one plain line each."}))

# ── BODY ─ one best visual per beat (lanes/*.json) ────────────────────────────────────────────────────────────────────────────────────────────────────
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
    if lane != "manim":
        b["shot"]["remotion"]["props"] = fill_audio(b["shot"]["remotion"]["props"], clock(b))
    beats.append(b)

# ── BVDT ─ recap: "Let's recap with Claude." then one bare sentence per act-ish, 6 lines (the card paginates in twos) ─────────────────────────────────
beats.append(remotion("BVDT", "Closing", N.BVDT_NARRATION, "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": "Your First Shaders and Materials", "artifactLines": N.BVDT_LINES,
     "lectureLayout": True, "brandLabel": "@NikBearBrown", "durationSeconds": "__AUDIO__"},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.2, "event": "six recap lines land in narration order"}],
    lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."}))

# ── BHTF ─ your turn: props.command == narration_text (lecture skill); the two output lines are the viewer's own checks ─────────────────────────────
beats.append(remotion("BHTF", "Closing", N.BHTF_NARRATION, "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Predict, Then Test", "command": N.BHTF_PROMPT,
     "runningText": "paste this into Claude…", "output": N.BHTF_CHECKS, "folderLabel": "@NikBearBrown", "durationSeconds": "__AUDIO__"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.12, "event": "the prompt types in full"},
     {"at": 0.85, "event": "two check lines land"}]))

# ── BOUT ─ channel outro (claude-liam -> ClaudeTitleOutro, locked by OUTRO-LOCK.md) ─────────────────────────────────────────────────────────────────
bout = {"beat_id": "BOUT", "act": "Closing", "lane": "bookend", "proof_gate": "SHOW",
        "narration_text": f"{N.TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro", "persona": "liam",
        "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                 "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": N.TITLE, "slug": N.SLUG, "lectureLayout": True, "durationSeconds": "__AUDIO__"}}},
        "kind": "outro_voice", "tail_silence_s": 1.0,
        "qc": {"sparse_by_design": True, "sparse_reason": "ClaudeTitleOutro: title + handle + mascot on a dark field; sparse layout is the brand design."}}
carry(bout)
bout["shot"]["remotion"]["props"] = fill_audio(bout["shot"]["remotion"]["props"], clock(bout))
beats.append(bout)

sheet = {"metadata": {
    "slug": N.SLUG, "title": N.TITLE, "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "channel_title": "@NikBearBrown", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "register": "Teardown", "clock": "narration", "palette": "claude", "fps": 24, "width": 3840, "height": 2160, "aspect_ratio": "16:9",
    "caption_policy": "sidecar", "greeting_language": "German (Hallo)",
    "course": "CSYE 7270 Virtual Environments and Real-Time 3D · Nik Bear Brown · Northeastern University",
    "playlist": N.PLAYLIST, "series_title": N.PLAYLIST,
    "lecture_opening_description": "Write two shaders and test what a pass proves",
    "lecture_opening_title_lines": ["Your First Shaders", "and Materials with", "Claude and Godot"],
    "lecture_opening_template": "lecture-title-slide-16x9",
    "topic": "CSYE 7270 · SHADERS AND MATERIALS",
    "audience": "CSYE 7270 students (Fall 2026) doing the shaders and materials assignment, and anyone directing an AI agent around Godot shaders",
    "source_doc": "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/assignments/05-shaders-materials-and-godot-shading-language.md (the whole assignment, read in full 2026-10-16; the worked example is the instructor example in /Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/)",
    "tags": ["Godot", "shaders", "materials", "Godot shading language", "uniforms", "textures", "Claude Code", "AI agents", "CSYE 7270", "Nik Bear Brown"],
    "bookend_exempt": ["cold-open"],
    "bookend_exempt_reason": "Lecture opens with a narrated portrait/title, writer, and terms; recap is present.",
}, "beats": beats}
OUT.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
pend = sum(1 for b in beats if b.get("pending"))
print(len(beats), "beats;", pend, "pending; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in beats)), "s")
