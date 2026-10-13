#!/usr/bin/env python3
"""make_sheet_shared.py — the ONE beat-sheet builder for the Godot shader lecture series.

Each film's make_sheet.py is a four-line shim:

    import sys; from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
    import make_sheet_shared; make_sheet_shared.main(Path(__file__).resolve().parent)

Inputs per film (all in the film folder):
  narration.py     every spoken line + the bookend content (the clock)
  lanes/*.json     per-body-beat lane decisions: { "B01": {"lane": "manim", "class": "B01_Name", "visual_intent": "...",
                     "motion_claim": "...", "show": [{"at": 0.2, "event": "..."}], "runner_up": "...", "why": "...", "sparse": true},
                     "B07": {"lane": "remotion", "pattern": "LectureCodeTrace", "props": {...}, ...} }
                   Optional per entry: "capture_spec" (what the build session must record in the Shader Lab), "lead_silence_s".
                   A Remotion props value of "__AUDIO__" under durationSeconds is replaced by the measured audio.
Outputs: beat_sheet.json (estimates only until Kokoro runs; measured audio is carried forward while narration is unchanged)
         SCRIPT.md (the human review script)
Safe to re-run at the layout stage. NEVER re-run after `art final` in the build stage: it clears the build stamps.
"""
import glob
import importlib.util
import json
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent
sys.path.insert(0, str(SERIES))
import series_config as S            # noqa: E402
import build_script_md               # noqa: E402

BOOKENDS = ("BOPEN", "BIDEA", "BDEFS", "BVDT", "BHTF", "BOUT")
REMOTION_LANES = ("remotion", "capture", "card", "terminal", "show-tell", "editor")


def _load_narration(film_dir):
    spec = importlib.util.spec_from_file_location("narration", film_dir / "narration.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fill_audio(props, dur):
    if isinstance(props, dict):
        return {k: (round(dur, 2) if v == "__AUDIO__" else fill_audio(v, dur)) for k, v in props.items()}
    if isinstance(props, list):
        return [fill_audio(v, dur) for v in props]
    return props


def main(film_dir):
    film_dir = Path(film_dir).resolve()
    N = _load_narration(film_dir)
    out = film_dir / "beat_sheet.json"
    prev = {}
    if out.exists():
        for b in json.loads(out.read_text())["beats"]:
            prev[b["beat_id"]] = b
    lanes = {}
    for f in sorted(glob.glob(str(film_dir / "lanes" / "*.json"))):
        lanes.update(json.loads(Path(f).read_text()))

    est = S.est_seconds

    def carry(b):
        p = prev.get(b["beat_id"])
        if p and p.get("narration_text") == b.get("narration_text"):
            for k in ("actual_duration_s", "audio_file"):
                if k in p:
                    b[k] = p[k]
        return b

    def remotion(bid, act, narration, pattern, props, show, gate="SHOW", **extra):
        b = {"beat_id": bid, "act": act, "lane": "bookend", "proof_gate": gate, "narration_text": narration,
             "estimated_duration_s": est(narration), "voice": S.VOICE, "engine": "kokoro", "persona": "liam",
             "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
        b.update(extra)
        carry(b)
        dur = b.get("actual_duration_s")
        if dur:
            b["shot"]["remotion"]["props"] = fill_audio(b["shot"]["remotion"]["props"], dur)
        return b

    beats = []

    # BOPEN: the approved lecture first beat (portrait, title; narrated playlist-if-any -> title -> summary).
    bopen = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD", "narration_text": N.BOPEN,
             "estimated_duration_s": est(N.BOPEN), "voice": S.VOICE, "engine": "kokoro", "persona": "liam",
             "routing": {"about": "Film identity and payoff", "runner_up": "Minimal title card",
                         "reason": "The lecture skill's approved first beat: portrait, title, narrated summary."},
             "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9",
                      "narration_contract": "playlist-title-summary-v1", "motion": "hold",
                      "visual_intent": "Professor Bear portrait, exact film title and short payoff visible immediately.",
                      "show": [{"at": 0, "event": "Complete populated lecture opener visible for the whole narration"}]},
             "qc": {"sparse_by_design": True, "sparse_reason": "Identity card: portrait and title; teaching motion resumes in BIDEA."}}
    beats.append(carry(bopen))

    # BIDEA: hesitant writer, greeting + the misconception corrected by one phrase.
    txt, trig, repl = N.BIDEA_TEXT
    beats.append(remotion("BIDEA", "the question", N.BIDEA, "BrutalistHesitantWriter",
        {"text": txt, "triggerWords": trig, "replacementWords": repl, "fontSize": 66, "charMs": 24, "hesitateBetween": 6,
         "hesitateWithin": 1, "mistakeRate": 4, "jitter": 20, "seed": N.SLUG, "banner": ""},
        [{"at": 0.0, "event": "types the newcomer's assumption"},
         {"at": 0.62, "event": f"backspaces '{trig}' and types '{repl}'"}],
        lead_silence_s=0.8,
        motion_claim="The writer types the assumption a newcomer arrives with and corrects it into the film's real subject.",
        qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}))

    # BDEFS: prerequisite vocabulary only.
    beats.append(remotion("BDEFS", "terms", N.BDEFS, "ClaudeDefinitions",
        {"title": "Terms In This Lecture", "terms": [{"term": t, "meaning": m} for t, m in N.BDEFS_TERMS],
         "durationSeconds": "__AUDIO__", "folderLabel": S.HANDLE},
        [{"at": 0.1 + 0.18 * i, "event": f"'{t}' lands"} for i, (t, _) in enumerate(N.BDEFS_TERMS)],
        gate="CARD", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: prerequisites, one plain line each."}))

    # BODY: one best visual per beat (lanes/*.json).
    seen_acts = set()
    for bid, ai, text in N.BODY:
        act = f"{N.ACTS[ai][0]} · {N.ACTS[ai][1]}"
        L = lanes.get(bid)
        if L is None:
            b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW", "narration_text": text,
                 "estimated_duration_s": est(text), "voice": S.VOICE, "engine": "kokoro", "persona": "liam",
                 "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": "PENDING: no lane entry yet", "show": [],
                          "manim": {"class": f"{bid}_Pending"}, "motion_claim": "pending"},
                 "pending": True}
            beats.append(carry(b))
            continue
        lane = L["lane"]
        b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": L.get("proof_gate", "SHOW"), "narration_text": text,
             "estimated_duration_s": est(text), "voice": S.VOICE, "engine": "kokoro", "persona": "liam"}
        if lane == "manim":
            b["shot"] = {"type": "GRAPHIC", "source": "own", "visual_intent": L["visual_intent"], "show": L.get("show", []),
                         "manim": {"class": L["class"]}, "motion_claim": L["motion_claim"]}
        else:
            b["shot"] = {"type": "REMOTION", "source": "own", "visual_intent": L["visual_intent"], "show": L.get("show", []),
                         "remotion": {"pattern": L["pattern"], "props": L.get("props", {})}, "motion_claim": L["motion_claim"]}
        if L.get("sparse", True):
            b["qc"] = {"sparse_by_design": True, "sparse_reason": L.get("sparse_reason",
                       "Lecture body beat: one object or scene on a cream stage, the voice carries the explanation; only underfill/clustered are waived.")}
        for k in ("lead_silence_s", "tail_silence_s", "kind"):
            if k in L:
                b[k] = L[k]
        b["lecture"] = {"runner_up": L.get("runner_up", ""), "why": L.get("why", "")}
        if L.get("capture_spec"):
            b["lecture"]["capture_spec"] = L["capture_spec"]
        if ai not in seen_acts:
            seen_acts.add(ai)
            b["lecture"]["act_title_on_screen"] = N.ACTS[ai][1]
        carry(b)
        dur = b.get("actual_duration_s")
        if dur and lane != "manim":
            b["shot"]["remotion"]["props"] = fill_audio(b["shot"]["remotion"]["props"], dur)
        beats.append(b)

    # BVDT: recap, one bare sentence per act (4 or 6 lines: the card paginates in twos).
    beats.append(remotion("BVDT", "verdict", N.BVDT_NARRATION, "ClaudeVerdictArtifact",
        {"artifactTitle": "Recap", "artifactHeading": N.BVDT_HEADING, "artifactLines": N.BVDT_LINES},
        [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.2, "event": "recap lines land in narration order"}],
        lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."}))

    # BHTF: your turn.
    beats.append(remotion("BHTF", "your turn", N.BHTF_NARRATION, "ClaudeComposerAsk",
        {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": N.BHTF_SEGMENT, "command": N.BHTF_PROMPT,
         "runningText": "paste this into Claude…", "output": N.BHTF_CHECKS, "folderLabel": S.HANDLE,
         "modelLabel": getattr(N, "BHTF_MODEL_LABEL", "Opus 5.5"), "effortLabel": getattr(N, "BHTF_EFFORT_LABEL", "High")},
        [{"at": 0.0, "event": "Composer opens: 'Your turn.'"}, {"at": 0.12, "event": "the prompt types in full"},
         {"at": 0.85, "event": "two check lines land"}]))

    # BOUT: the channel outro (claude-liam -> ClaudeTitleOutro, locked by OUTRO-LOCK.md).
    bout = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
            "narration_text": f"{getattr(N, 'SPOKEN_TITLE', N.TITLE)}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": S.VOICE, "engine": "kokoro",
            "persona": "liam",
            "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                     "remotion": {"pattern": "ClaudeTitleOutro",
                                  "props": {"title": N.TITLE, "slug": N.SLUG, "handle": S.HANDLE, "subline": ""}}},
            "kind": "outro_voice", "tail_silence_s": 1.0}
    beats.append(carry(bout))

    meta = {
        "slug": N.SLUG, "title": N.TITLE, "topic": N.TOPIC, "skill": "lecture", "style_preset": "lecture",
        "channel": S.CHANNEL, "persona": S.PERSONA, "voice": S.VOICE, "voice_kokoro": S.VOICE, "engine": "kokoro",
        "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9",
        "width": 3840, "height": 2160, "caption_policy": "sidecar", "greeting_language": getattr(N, "GREETING", "Hallo"),
        "audience": "people making games in Godot, and anyone directing an AI that writes shaders for them",
        "godot_version": S.GODOT,
        "lecture_opening_description": N.OPENING_DESCRIPTION,
        "lecture_opening_template": "lecture-title-slide-16x9",
        "lecture_opening_title_lines": getattr(N, "TITLE_LINES", [N.TITLE]),
        "bookend_exempt": ["cold-open", "bvdt"],
        "bookend_exempt_reason": "lecture skill: opens on the narrated identity card then the hesitant writer; no composer cold open.",
        "source_doc": getattr(N, "SOURCE_DOC", "see SOURCES.md"),
        "tags": N.TAGS}
    if S.PLAYLIST:
        meta["series_title"] = S.PLAYLIST
        meta["playlist"] = S.PLAYLIST
    sheet = {"metadata": meta, "beats": beats}
    out.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
    pend = sum(1 for b in beats if b.get("pending"))
    words = sum(len(b["narration_text"].split()) for b in beats)
    total = words * S.SEC_PER_WORD + 4.0
    print(f"{N.SLUG}: {len(beats)} beats; {pend} pending; {words} words; est {total/60:.1f} min")
    build_script_md.write(film_dir, N, sheet, lanes)
