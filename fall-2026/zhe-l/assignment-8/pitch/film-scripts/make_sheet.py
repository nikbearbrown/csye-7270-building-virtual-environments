#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for the walker-survival-shooting final-project pitch (A8).

Narration and visual plan come from the approved draft (submission-a8/beat_sheet.json, field
narration_en). Show-tell drawings (Manim) for the idea beats; SCRIPTED-INPUT game captures and
document frames (media/<BID>.mp4, made by prepare_media.py) for what exists; a ShowTellCard name
card as the outro.

Bookends: the narration speaks as the author (Zhe Liu). The assignment forbids the instructor's
name, persona and credit line, so the show-tell hesitant writer ("in for Bear"), the Your Turn
composer and the @NikBearBrown outro are not used. BOUT is a ShowTellCard with the author's name;
metadata.channel_title is set to the author so bookend_check compares against it.
Run: python -I scripts/make_sheet.py   (keeps measured audio fields when the narration is unchanged)
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
DRAFT = Path(r"<working-folder>\submission-a8\beat_sheet.json")
SLUG = "walker-survival-shooting-pitch"
TITLE = "walker-survival-shooting"
AUTHOR = "Zhe Liu"
SPARSE = {"sparse_by_design": True, "sparse_reason": "Show-tell: one drawn object and a few labels on the stage. Only underfill and clustering waived."}

draft = {b["id"]: b for b in json.load(open(DRAFT, encoding="utf-8"))["beats"]}


def text(bid):
    return draft[bid]["narration_en"]


def manim(bid, cls, intent, show):
    return {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
            "narration_text": text(bid), "voice": "am_onyx", "engine": "kokoro", "qc": SPARSE,
            "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": intent, "motion_claim": intent,
                     "show": show, "manim": {"class": cls}},
            "label": "CONSTRUCTED" if "PLANNED" not in intent and "WILL" not in intent else "CONSTRUCTED · planned"}


def screen(bid, intent, label):
    return {"beat_id": bid, "act": "exists", "lane": "media", "proof_gate": "SHOW",
            "narration_text": text(bid), "voice": "am_onyx", "engine": "kokoro",
            "shot": {"type": "SCREEN", "class": "SHOW", "source": "own", "evidence_media": f"media/{bid}.mp4",
                     "show": [{"at": "0.0", "event": intent}]},
            "role_note": label,
            "qc": {"full_bleed": True,
                   "contrast_regions": [{"label": "burned-in disclosure label", "box": [0.02, 0.9, 0.98, 0.995]}],
                   "contrast_reason": "Edge-to-edge engine render or document frame; the essential text is the label strip."}}


B = [
    screen("B00", "Scripted input: one-hand raise, then two hands (tablet-scripted.mp4 frames 0-165)",
           "SCRIPTED INPUT · f13431bf; small caption: AI voice, script by Zhe Liu"),
    manim("B01", "B01_OneSentence", "A tablet shows a memo; beside it a small clock keeps ticking",
          [{"at": 0.1, "event": "tablet lands"}, {"at": 0.3, "event": "memo lines write onto the screen"}, {"at": 0.6, "event": "clock hand keeps turning"}]),
    manim("B02", "B02_TheBuild", "WILL: a build box opens; inside is one room",
          [{"at": 0.1, "event": "box drops in"}, {"at": 0.35, "event": "lid opens"}, {"at": 0.6, "event": "one room rises inside"}]),
    manim("B03", "B03_Difference", "A row of identical boxes; one opens and the tablet rises out of it",
          [{"at": 0.1, "event": "boxes slide in"}, {"at": 0.6, "event": "one box opens, tablet rises"}]),
    manim("B04", "B04_Checklist", "A quest checklist ticks itself line by line",
          [{"at": 0.15, "event": "checklist page"}, {"at": 0.35, "event": "ticks land one by one"}]),
    manim("B05", "B05_ClueLoop", "PLANNED: a goal card, two testimony pages, lines fly into a third memo, a red circle marks a contradiction",
          [{"at": 0.1, "event": "goal card"}, {"at": 0.3, "event": "two testimonies"}, {"at": 0.55, "event": "lines fly into your memo"}, {"at": 0.8, "event": "red circle"}]),
    manim("B06", "B06_Menus", "Three menu tablets with a few tabs each, one per game; none of them reaches out to the world",
          [{"at": 0.1, "event": "three menu tablets"}, {"at": 0.6, "event": "tabs light, nothing leaves the screen"}]),
    screen("B07", "Scripted input: This PC, open a folder, Up, minimize, taskbar, show desktop (tablet-scripted.mp4 frames 150-500)",
           "SCRIPTED INPUT · f13431bf"),
    screen("B08", "Scripted input in the ThoughtPad debug scene: read-only text stays unchanged; the editable memo takes typing",
           "STANDALONE DEBUG SCENE · SCRIPTED INPUT · f13431bf"),
    screen("B09", "Document frame: the Keys section of pitch/README.md", "DOCUMENT · pitch/README.md"),
    screen("B10", "Scripted input: raise lights the screen; an interrupted raise never lights (b10-scripted.mp4)",
           "SCRIPTED INPUT · f13431bf"),
    screen("B11", "Scripted input: screen glow, then two jumps with landing dust (b10 / b11 clips)",
           "SCRIPTED INPUT · f13431bf; GPU note: NVIDIA GeForce RTX 5070 Ti Laptop GPU, landing dust +0.001 ms"),
    screen("B12", "Document frame: last lines of the six test logs at f13431bf", "REAL OUTPUT · f13431bf"),
    screen("B13", "Scripted input: W with two hands does not move the body; with one hand it walks (tablet-scripted.mp4 frames 480-673)",
           "SCRIPTED INPUT · f13431bf"),
    manim("B14", "B14_FirstLoop", "WILL: a gun and an exit door stamped NOT NOW; then five pages pass along the first clue loop",
          [{"at": 0.1, "event": "gun and exit door"}, {"at": 0.3, "event": "NOT NOW stamp"}, {"at": 0.55, "event": "the loop runs page by page"}]),
    manim("B15", "B15_Shrink", "A big crate shrinks to a small core; six replaceable blocks click onto it",
          [{"at": 0.1, "event": "big crate"}, {"at": 0.3, "event": "shrinks to a core"}, {"at": 0.55, "event": "blocks click on"}]),
    manim("B16", "B16_Learning", "Left: five new tools land in a 'new' tray; right: one code block sits in a 'had' tray",
          [{"at": 0.15, "event": "new tray fills"}, {"at": 0.6, "event": "had tray"}]),
    manim("B17", "B17_ExistsWill", "Two trays: EXISTS (solid blocks) and WILL (dashed outlines); one dashed block has a question mark",
          [{"at": 0.15, "event": "EXISTS tray"}, {"at": 0.45, "event": "WILL tray"}, {"at": 0.7, "event": "question mark"}]),
]

BOUT = {"beat_id": "BOUT", "act": "bookend", "lane": "bookend", "proof_gate": "SHOW",
        "narration_text": text("B18"), "voice": "am_onyx", "engine": "kokoro", "qc": SPARSE,
        "kind": "outro_voice", "tail_silence_s": 1.0,
        "shot": {"type": "REMOTION", "source": "own",
                 "show": [{"at": 0.1, "event": "name card fills"}],
                 "remotion": {"pattern": "ShowTellCard",
                              "props": {"kind": "masked", "word": AUTHOR, "heading": TITLE,
                                        "sub": "AI voice · script by me", "title": TITLE, "handle": AUTHOR,
                                        "subline": "", "durationSeconds": 4.0}}}}

beats = B + [BOUT]

# keep measured audio for unchanged narration
old = {}
sheet_path = REEL / "beat_sheet.json"
if sheet_path.exists():
    old = {b["beat_id"]: b for b in json.load(open(sheet_path, encoding="utf-8"))["beats"]}
for b in beats:
    b["estimated_duration_s"] = round(len(b["narration_text"].split()) / 2.6, 1)
    o = old.get(b["beat_id"])
    if o and o.get("narration_text") == b["narration_text"]:
        for k in ("audio_file", "actual_duration_s", "render_duration_s"):
            if k in o:
                b[k] = o[k]
        if b["beat_id"] == "BOUT" and "actual_duration_s" in o:
            b["shot"]["remotion"]["props"]["durationSeconds"] = o["actual_duration_s"]

meta = {"slug": SLUG, "title": TITLE, "topic": "GODOT · FINAL PROJECT PITCH", "skill": "show-tell",
        "style_preset": "show-tell", "channel": "zhe-liu", "channel_title": AUTHOR,
        "persona": "Zhe Liu (AI voice, script by the author)", "in_for_bear": False,
        "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro", "clock": "narration",
        "palette": "claude", "register": "Teardown", "fps": 30, "aspect_ratio": "16:9",
        "width": 1920, "height": 1080, "caption_policy": "none",
        "bookend_exempt": ["cold-open", "bvdt", "bhtf"],
        "bookend_exempt_reason": "Final-project pitch: the assignment requires the narration to speak as the author and forbids the instructor's name, persona and credit line, so the hesitant-writer greeting, the Your Turn composer and the @NikBearBrown outro are not used. The outro is a name card for the author.",
        "game": {"name": "walker-survival-shooting", "source_revision": "f13431bf",
                 "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
                 "game_path": "assignment-8/walker-survival-shooting/godot (f13431bf)"},
        "note": "All game footage is scripted input recorded with Godot Movie Maker from an isolated copy of f13431bf (see CAPTURE.md); drawings are constructed; designs not built are labelled PLANNED / WILL. No commit, push or publication from the film work."}
json.dump({"metadata": meta, "beats": beats}, open(sheet_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(beats)} beats -> {sheet_path}")
