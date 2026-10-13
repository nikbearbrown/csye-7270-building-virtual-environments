#!/usr/bin/env python3
"""make_sheet.py — builds beat_sheet.json for the lecture. Safe to re-run: it carries audio_file / actual_duration_s forward
and fills every Remotion beat's durationSeconds from the measured audio.

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

def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
    b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate, "narration_text": narration,
         "estimated_duration_s": est(narration), "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    carry(b)
    dur = b.get("actual_duration_s")
    if dur:
        b["shot"]["remotion"]["props"] = fill_audio(b["shot"]["remotion"]["props"], dur)
    return b

beats = []

# ── BIDEA ─ hesitant writer: greeting + what the topic is about ───────────────────────────────────────
beats.append(remotion("BIDEA", "the question", N.BIDEA, "BrutalistHesitantWriter",
    {"text": "My model looks right in Blender,\nso it must be right in the game?",
     "triggerWords": "so it must be right in the game", "replacementWords": "but what did the game receive",
     "fontSize": 66, "charMs": 24, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 4, "jitter": 20,
     "seed": N.SLUG, "banner": ""},
    [{"at": 0.0, "event": "types 'My model looks right in Blender,'"},
     {"at": 0.62, "event": "backspaces 'so it must be right in the game' and types 'but what did the game receive'"}],
    lead_silence_s=0.8,
    motion_claim="The writer types the naive assumption and corrects it into the real question.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}))

# ── BDEFS ─ key terms ───────────────────────────────────────────────────────────────────────────────────
beats.append(remotion("BDEFS", "terms", N.BDEFS, "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "mesh", "meaning": "the points and faces that make a shape"},
               {"term": "collider", "meaning": "an invisible shape the physics engine tests against"},
               {"term": "bounding box", "meaning": "the smallest upright box around a shape"},
               {"term": "glTF", "meaning": "a file format for 3D models; distances in metres, Y is up"},
               {"term": "headless", "meaning": "running a program with no window"},
               {"term": "MCP", "meaning": "Model Context Protocol: lets an agent call another program's tools"}],
     "durationSeconds": "__AUDIO__", "folderLabel": "@NikBearBrown"},
    [{"at": 0.1, "event": "'mesh' lands"}, {"at": 0.25, "event": "'collider' lands"}, {"at": 0.42, "event": "'bounding box' lands"},
     {"at": 0.6, "event": "'glTF' lands"}, {"at": 0.75, "event": "'headless' lands"}, {"at": 0.88, "event": "'MCP' lands"}],
    gate="CARD", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one plain line each."}))

# ── BODY ─ one best visual per beat (lanes/*.json) ──────────────────────────────────────────────────────
for bid, ai, text in N.BODY:
    act = f"{N.ACTS[ai][0]} · {N.ACTS[ai][1]}"
    L = lanes.get(bid)
    if L is None:
        b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW", "narration_text": text,
             "estimated_duration_s": est(text), "voice": "am_onyx", "engine": "kokoro",
             "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": "PENDING — no lane entry yet", "show": [],
                      "manim": {"class": f"{bid}_Pending"}, "motion_claim": "pending"},
             "pending": True}
        beats.append(carry(b))
        continue
    lane = L["lane"]
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": L.get("proof_gate", "SHOW"), "narration_text": text,
         "estimated_duration_s": est(text), "voice": "am_onyx", "engine": "kokoro"}
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

# ── BVDT ─ recap (one bare sentence per act-ish, 6 lines: the card paginates in twos) ───────────────────────
beats.append(remotion("BVDT", "verdict", N.BVDT_NARRATION, "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap", "artifactHeading": "Prove It Arrived", "artifactLines": N.BVDT_LINES},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.2, "event": "six recap lines land in narration order"}],
    lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."}))

# ── BHTF ─ your turn ───────────────────────────────────────────────────────────────────────────────────────
beats.append(remotion("BHTF", "your turn", N.BHTF_NARRATION, "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Test What Arrived", "command": N.BHTF_PROMPT,
     "runningText": "paste this into Claude…", "output": N.BHTF_CHECKS,
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens — 'Your turn.'"}, {"at": 0.12, "event": "the prompt types in full"},
     {"at": 0.85, "event": "two check lines land"}]))

# ── BOUT ─ channel outro (claude-liam → ClaudeTitleOutro, OUTRO-LOCK) ───────────────────────────────────────────
bout = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
        "narration_text": f"{N.TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
        "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                 "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": N.TITLE, "slug": N.SLUG, "handle": "@NikBearBrown", "subline": ""}}},
        "kind": "outro_voice", "tail_silence_s": 1.0}
beats.append(carry(bout))

sheet = {"metadata": {
    "slug": N.SLUG, "title": N.TITLE, "topic": "3D · BLENDER TO GODOT", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "French (Bonjour)",
    "audience": "game developers and students who let an AI agent make 3D assets",
    "source_doc": "csye-7270-building-virtual-environments/chapters/03-blender-mcp-to-godot.md (read in full 2026-10-06); examples/03-blender-mcp-to-godot",
    "playlist": "Virtual Environments and Real-Time 3D", "chapter_number": 3,
    "tags": ["Blender", "Godot", "glTF", "3D models", "game development", "Claude Code", "Codex", "AI agents", "Nik Bear Brown"]},
    "beats": beats}
OUT.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
pend = sum(1 for b in beats if b.get("pending"))
print(len(beats), "beats;", pend, "pending; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in beats)), "s")
