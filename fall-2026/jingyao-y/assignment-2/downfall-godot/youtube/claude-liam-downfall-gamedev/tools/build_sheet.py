"""Write beat_sheet.json for the Downfall Assignment 2 gamedev film.

Run from the reel folder:  python tools/build_sheet.py <snapshot-of-111bf6e>
Code excerpts are read verbatim from the snapshot clone, so displayed code
always equals the hashed source the evidence ledger records.
"""
import json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
SNAP = Path(sys.argv[1])
REV = "111bf6e"
TITLE = "Downfall: Generated Art, Sound and Music"
SLUG = "claude-liam-downfall-gamedev"
TOPIC = "GODOT GAMEDEV · DOWNFALL"


def lines(path, a, b):
    text = (SNAP / path).read_text(encoding="utf-8").splitlines()
    return "\n".join(text[a - 1:b])


EXCERPTS = {
    "B03": ("godot_assets/lappland_animator_3d.gd", 38, 42),
    "B05": ("game/game_manager.gd", 157, 160),
    "B08": ("game/game_music.gd", 70, 82),
    "B11": ("art/relics/reduce_generated.py", 60, 70),
    "B15": ("tests/test_audio.gd", 70, 78),
}


def say(bid, act, text, shot, **extra):
    beat = {"beat_id": bid, "act": act, "narration_text": text, "voice": "am_onyx", "engine": "kokoro",
            "estimated_duration_s": max(6, round(len(text.split()) / 2.5)), "shot": shot}
    beat.update(extra)
    return beat


def workbench(bid, title, notes, cues, note_label="Source notes — not Inspector values"):
    path, a, b = EXCERPTS[bid]
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "code-highlight",
            "label": "Godot editor reconstruction",
            "show": [{"at": "0.0", "event": f"Godot editor reconstruction: {path} lines {a}-{b}, revision {REV}"}],
            "remotion": {"pattern": "GodotDevWorkbench", "props": {
                "mode": "code", "title": title, "project": "downfall-godot",
                "path": f"res://{path}", "source": f"Godot editor reconstruction · {path}:{a}-{b} · commit {REV}",
                "code": lines(path, a, b), "startLine": a, "codeFontSize": 27 if b - a < 8 else 24,
                "inspectorLabel": note_label, "notes": notes, "cues": cues}}}


def capture(bid, clip, label, events, evidence=True):
    shot = {"type": "GAMEPLAY", "class": "SHOW", "source": "capture",
            "capture_ref": {"id": clip, "label": label}, "label": label,
            "show": [{"at": str(t), "event": e} for t, e in events]}
    if evidence:
        shot["evidence_media"] = f"media/{bid}.mp4"
    return shot


def graphic(pattern, props, events, motion="type-on"):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": motion,
            "show": [{"at": str(t), "event": e} for t, e in events],
            "remotion": {"pattern": pattern, "props": props}}


QC_GAME = {"full_bleed": true, "full_bleed_reason": "Real Godot capture: the game's own HUD is drawn edge to edge by design.", "contrast_regions": [{"label": "capture-label", "box": [0.02, 0.932, 0.6, 0.973]}], "contrast_reason": "Real Godot capture: the game's ground is deliberately dark and low-contrast (pillar: attacks and red warnings must stand out), so whole-frame ink contrast is not a text measure. This region samples the burned capture label, the only overlay text on the shot."}

beats = [
    say("B00", "ASK",
        "Hola. Liam, in for Bear. This is a reconstructed ask, not a transcript. A student wanted Walker to take the design "
        "for Downfall, a top-down extraction action game where Lappland fights down floors that only go one way, and fill it "
        "with generated art, sound and music, wired into a Godot slice that actually plays.",
        graphic("ClaudeComposerAsk", {
            "greeting": "Hola, Liam", "topic": TOPIC, "segment": "Please Use Walker",
            "command": "Please use Walker to convert my game design document about Downfall, a top-down extraction ARPG "
                       "where Lappland fights down one-way floors, into generated art, sound effects and music in a playable Godot slice.",
            "runningText": "reading the design documents…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
            "effortLabel": "High",
            "output": ["Reconstructed prompt - illustrative, not a transcript.",
                       "Art: gpt-image. Music and event sounds: Gemini.",
                       "Design documents labelled retrospective."]},
            [(0.02, "composer card fades in"), (0.28, "the Walker ask types"), (0.78, "result lines land")])),
    say("B01", "BLUF",
        "Here's the honest version. Most of this art was generated first and written up afterwards, and the design "
        "documents say they are retrospective. The images came from OpenAI's gpt-image, through the student's Codex agent, "
        "which the docs call Sol. The music, the two stings and two event sounds came from Gemini. Claude wrote the briefs, "
        "the processing scripts, the game code and the tests. The student made the calls.",
        graphic("BrutalistHesitantWriter", {
            "text": "Design first, then generate.\nArt: gpt-image, through Sol.\nMusic and cues: Gemini.\nEvery asset logged.",
            "triggerWords": "first", "replacementWords": "after",
            "fontSize": 128, "lineSpacing": 2.1, "align": "center", "seed": "1729", "charMs": 8, "mistakeRate": 2,
            "hesitateWithin": 0, "hesitateBetween": 1, "durationSeconds": 22},
            [(0.15, "'Design first, then generate' types and pauses"), (0.4, "struck through, corrected to 'Generated first, documented after'")],
            motion="type-on-correct"), lead_silence_s=0.8),
    say("B02", "GAMEPLAY",
        "Downfall in two sentences. Lappland, a Rhodes Island operative, takes a contract, fights and loots down floors that "
        "only go one way, and keeps deciding whether to push deeper or get out with what she has. Four pillars shaped every "
        "asset: positioning and timing, a trade-off at every descent, regions you can tell apart, and attacks you can read. "
        "One caveat up front: it is built on Arknights' characters and world, which the assignment's rights rule forbids. "
        "The student kept it, and the documents say so plainly.",
        capture("B02", "warehouse", "Real Godot capture · scripted input · isolated copy", [(0.0, "Rhodes base hall, base music playing")], evidence=False),
        qc=QC_GAME),
    say("B03", "MECHANISM",
        "Lappland's states are cells in two generated atlases. The walk sheet gives eight directions. The combat sheet has "
        "five rows, and the other three directions are mirrored at runtime. This table names each state's first column and "
        "its frame count: three combo attacks, the sword wave, and one hurt frame. The note on the right is a correction: the "
        "generated south-east row faced the wrong way, so it is drawn as south-west, flipped.",
        workbench("B03", "Lappland's states are atlas cells",
                  [{"label": "Atlases (gpt-image)", "value": "walk 32 px × 8 dirs · combat 64 px × 5 rows"},
                   {"label": "Line 26", "value": "MIRRORED: SE drawn as SW, flipped"}],
                  [{"at": 0.5, "line": 38, "label": "5 drawn rows; 3 mirrored"}, {"at": 9.0, "line": 42, "label": "state → first column, frames"}])),
    say("B04", "RESULT",
        "Here is what those lines do in the running game, driven by scripted input on an isolated copy. Real W, A, S and D "
        "key events turn her east, south, west and north. Then the left-click attack path runs the combo. The swords come "
        "from the combat cells, and her facing follows the target. Each state is a straight swap to a different cell, with "
        "no blending.",
        capture("B04", "combat", "Real Godot capture · scripted input (real key events) · isolated copy",
                [(0.0, "WASD turns: east, south, west, north"), (0.5, "combo attacks and hurt against city enemies")]),
        qc=QC_GAME),
    say("B05", "MECHANISM",
        "Sound never decides anything here. The warehouse has four real events: a bank of lights coming on, a floor hatch "
        "opening, a shelf rising, and the lights going out. Each one is a signal the room already emits once, on an edge, "
        "not every frame. These four lines connect them to cues. Two cues have Gemini-generated files. The hatch and shelf "
        "files were never generated, so those two are counted, but silent.",
        workbench("B05", "Four warehouse events, four cues",
                  [{"label": "Gemini files", "value": "lights_on, lights_off"},
                   {"label": "Not generated", "value": "hatch, shelf: counted, silent"}],
                  [{"at": 0.5, "line": 157, "label": "bank lit"}, {"at": 6.0, "line": 158, "label": "hatch"},
                   {"at": 9.0, "line": 159, "label": "shelf"}, {"at": 12.0, "line": 160, "label": "lights out"}])),
    say("B06", "RESULT",
        "Walking in for real: four banks of lights clunk on, one after another, and the racks rise out of the floor as they "
        "come on screen. The test counts exactly four light cues, one per bank, and one hatch and one shelf cue per built "
        "rack. Standing in the doorway adds nothing. Next, the same walk with no narration at all.",
        capture("B06", "warehouse", "Real Godot capture · scripted input (move targets) · isolated copy",
                [(0.0, "walk through the west door"), (0.4, "light banks come on one by one; racks rise")]),
        qc=QC_GAME),
    {"beat_id": "B07", "act": "SLICE AUDIO", "narration_text": "", "voice": "am_onyx", "engine": "kokoro",
     "clock": "source", "audio_policy": "preserve", "kind": "source_report",
     "role_note": "Labelled segment: the slice's own audio (base music, lights on, lights off), no narration over it.",
     "shot": capture("B07", "warehouse", "SLICE AUDIO · no narration · real capture",
                     [(0.0, "burned label: slice audio, no narration"), (0.5, "lights on, racks, walk out, lights off")], evidence=False),
     "qc": QC_GAME},
    say("B08", "MECHANISM",
        "Music follows the run. Starting a contract fades the calm base loop out and starts the field loop. Each loop file "
        "carries its own intro, and Godot jumps back to a logged loop point, so the seam needs no second file. Pausing in "
        "the field freezes the loop on the same sample. When a run ends, this function fades the field track and plays "
        "exactly one sting, fail or extract, while the base music waits for it to finish.",
        workbench("B08", "One sting per run end",
                  [{"label": "Loop points (asset_log.json)", "value": "base 40.171 s · mine 13.3034 s"},
                   {"label": "Pause", "value": "field: frozen · base: −10 dB"}],
                  [{"at": 0.5, "line": 74, "label": "only after field music"}, {"at": 10.0, "line": 75, "label": "fade field track"},
                   {"at": 14.0, "line": 80, "label": "one sting"}])),
    say("B09", "RESULT",
        "In play: Escape opens the pause menu, and the field freezes, music included. Escape again, and it resumes from the "
        "same point. Then a real loss. She starts from the floor thirty camp, unlocked in memory to skip thirty floors of "
        "walking, steps onto floor thirty-one, and fights without dodging or healing until she is killed. The run "
        "ends, and the fail sting plays once.",
        capture("B09", "combat+death", "Real Godot capture · scripted input · camp unlocked in memory (disclosed)",
                [(0.0, "Esc: pause menu, field frozen"), (0.35, "floor 31: fighting without dodging"), (0.8, "行动失败 settlement")]),
        qc=QC_GAME),
    {"beat_id": "B10", "act": "SLICE AUDIO", "narration_text": "", "voice": "am_onyx", "engine": "kokoro",
     "clock": "source", "audio_policy": "preserve", "kind": "source_report",
     "role_note": "Labelled segment: the slice's own audio at death: field track stops, STING-FAIL plays once.",
     "shot": capture("B10", "death", "SLICE AUDIO · no narration · real capture",
                     [(0.0, "burned label: slice audio, no narration"), (0.3, "killed; fail sting over the settlement")], evidence=False),
     "qc": QC_GAME},
    say("B11", "MECHANISM",
        "One asset, all the way through: the relic Emperor's Favour. The brief told Sol to draw a letter opener across a "
        "sealed envelope. gpt-image painted it at twelve hundred and fifty-four pixels. This script crops it, shrinks it "
        "nearest-neighbour to sixty-four pixels inside a seventy-two pixel canvas, and quantizes it to twenty-three colours "
        "plus an outline. Claude's review flagged forty-three percent isolated pixels. The student looked, and accepted it.",
        workbench("B11", "Brief → prompt → raw → 72 px",
                  [{"label": "Brief → prompt", "value": "R_brief_v1.md row 1 → batch_R1_v1/README.md"},
                   {"label": "Review", "value": "43% isolated pixels; author accepted"}],
                  [{"at": 0.5, "line": 60, "label": "fit 64 px"}, {"at": 10.0, "line": 62, "label": "nearest-neighbour shrink"},
                   {"at": 16.0, "line": 70, "label": "23 colours"}])),
    say("B12", "RESULT",
        "The result, step by step: the raw painting, the seventy-two pixel icon shown eight times larger, and the same icon "
        "in the engine's relic window, drawn at exactly one times. Icons are only ever drawn at whole multiples of seventy-two, "
        "so every pixel stays square.",
        {"type": "GRAPHIC", "class": "SHOW", "source": "image", "label": "Real files + engine screenshot (tests/capture_gui.gd)",
         "evidence_media": "media/B12.mp4",
         "show": [{"at": "0.0", "event": "raw source → 72 px ×8 → in-engine R window"}]}),
    say("B13", "MECHANISM",
        "A cause and effect nobody planned. Recording this film from a fresh clone, the camp came out silent: no field "
        "music, no extraction sting. The cause was one ignore rule. 'Music, slash' was meant for the raw MP3 downloads, but "
        "it also matched 'audio, slash, music', so every loop and sting was missing from git. Anchoring it with a leading "
        "slash put five music files back.",
        graphic("GitHubCodeDiff", {
            "file": ".gitignore", "badge": "+1 −1",
            "lines": [{"gutter": "9", "text": "# Seam listening copies (regenerated by audio/tools/cut_audio.py)", "kind": "context"}, {"gutter": "10", "text": "audio/_check/", "kind": "context"}, {"gutter": "11", "text": "", "kind": "context"}, {"gutter": "12", "text": "# Course rule: no MP3/MP4 in GitHub. Raw Gemini downloads stay local (…)", "kind": "context"}, {"gutter": "-", "text": "music/", "kind": "del"}, {"gutter": "+", "text": "/music/", "kind": "add"}, {"gutter": "14", "text": "*.mp3", "kind": "context"}, {"gutter": "15", "text": "*.mp4", "kind": "context"}, {"gutter": "16", "text": "", "kind": "context"}, {"gutter": "17", "text": "# Official PRTS/Arknights images used as references: copyrighted, not redistributed.", "kind": "context"}, {"gutter": "18", "text": "art/relics/refs/prts_icons/", "kind": "context"}],
            "caption": "commit 111bf6e · found when a fresh-clone capture came out silent"},
            [(0.0, "diff panel: .gitignore"), (0.4, "music/ removed"), (0.6, "/music/ added")], motion="diff-reveal"),
        qc={"contrast_regions": [{"label": "file-header", "box": [0.12, 0.16, 0.3, 0.21]}, {"label": "context-row", "box": [0.12, 0.25, 0.72, 0.29]}], "contrast_reason": "GitHubCodeDiff is a dark panel whose add/del rows carry an intentional red/green tint; the whole-frame average mixes that tint and the empty page into the metric. These regions sample the file header and a context row of real text."}),
    say("B14", "RESULT",
        "The same clone after the fix. The camp has its music, a real mouse click on the green Extract button ends the run, "
        "and the extraction sting plays once over Mission Accomplished.",
        capture("B14", "extract", "Real Godot capture · real mouse click · camp unlocked in memory (disclosed)",
                [(0.0, "camp screen"), (0.3, "click 撤离"), (0.5, "行动结束 settlement")]),
        qc=QC_GAME),
    say("B15", "MECHANISM",
        "The automated check behind the sound claims. The test walks the warehouse and counts every call to the sound "
        "player, counting even when it runs headless, before playback is skipped. One light cue per bank, one hatch and "
        "one shelf per built rack, and nothing extra while standing still. The honest limit: the test teleports between "
        "rooms, so it proves the counting, not how the room feels.",
        workbench("B15", "Counting one sound per event",
                  [{"label": "Suite", "value": "test_audio.gd · 26 checks"},
                   {"label": "Shortcut", "value": "teleports: proves counts, not feel"}],
                  [{"at": 0.5, "line": 70, "label": "4 light cues"}, {"at": 8.0, "line": 76, "label": "one shelf per rack"},
                   {"at": 14.0, "line": 78, "label": "no repeats"}])),
    say("B16", "RESULT",
        "On a fresh clone of commit one-one-one-b-f-six-e, every test suite passes, headless and windowed. One screenshot "
        "script failed once on a random map and passed both times it was rerun, so that one is flaky, not fixed. One commit "
        "earlier, the audio test failed at the missing music. That failure is how the gap was found.",
        {"type": "GRAPHIC", "class": "SHOW", "source": "image", "label": "Recorded run_all.ps1 output on a fresh clone",
         "evidence_media": "media/B16.mp4",
         "show": [{"at": "0.0", "event": "recorded test output lines from the fresh-clone runs"}]}),
    say("B17", "VERDICT",
        "Verdict. Working: seven Lappland states, three generated regions, a base loop and a field loop, two stings, two "
        "generated event sounds and a mute switch, with one sound per event under test. Found and fixed: a fresh clone was "
        "missing every music file. Still open: the Arknights material, design written after generation, seven poses of "
        "ten, the hatch and shelf sounds, and the human playtest with sound on and muted, which the author still has to "
        "record. Next step: generate those two sounds and three poses.",
        graphic("ClaudeVerdictArtifact", {
            "artifactTitle": "Verdict", "artifactHeading": f"downfall-godot · {REV}", "brandLabel": "@NikBearBrown",
            "artifactLines": [
                "Working: 7 Lappland states · 3 regions · 2 loops · 2 stings · 2 event sounds · mute; one sound per event (test_audio).",
                "Found and fixed: a fresh clone had no music files (ignore rule, 111bf6e).",
                "Open: Arknights IP · design after generation · 7 of 10 poses · hatch and shelf sounds · no separate music/SFX mute.",
                "Human playtest, sound on and muted: still to be recorded by the author."]},
            [(0.2, "line 1"), (0.4, "line 2"), (0.6, "line 3"), (0.8, "line 4")], motion="artifact-reveal")),
    say("B18", "HANDOFF",
        "Your turn. Paste this into Claude: 'Clone my Godot repo into an empty folder, list every res path my code loads, "
        "tell me which of those files git is not tracking, then run my tests in that clone.' That is the check that caught "
        "the missing music here. Write down how many you expect it to find before you run it. Liam, in for Bear.",
        graphic("ClaudeComposerAsk", {
            "greeting": "Your turn.", "topic": TOPIC, "segment": "Check A Fresh Clone",
            "command": "Clone my Godot repo into an empty folder, list every res:// path my code loads, tell me which of "
                       "those files git is not tracking, then run my tests in that clone.",
            "runningText": "cloning into an empty folder…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
            "effortLabel": "High", "output": ["Predict the count first.", "Then compare."], "animateTyping": True},
            [(0.02, "composer fades in"), (0.12, "prompt types"), (0.78, "running text")])),
    {"beat_id": "B19", "act": "OUTRO", "narration_text": "Liam, in for Bear.", "voice": "am_onyx", "engine": "kokoro",
     "estimated_duration_s": 7, "audio_policy": "silence",
     "shot": graphic("ClaudeTitleOutro", {"title": TITLE, "slug": SLUG}, [(0.0, "title card"), (0.45, "mascot"), (0.7, "jingle")], motion="mascot-title")},
]

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "kind": "godot-gamedev", "mode": "walker",
    "playlist": "NikBearBrown", "brand": "claude-liam", "audience": "CSYE 7270 reviewers and Godot students",
    "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
    "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "crop",
    "captions": False, "channel_title": "@NikBearBrown", "channel": "@NikBearBrown", "folderLabel": "@NikBearBrown",
    "greeting": "Hola, Liam", "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
    "game": {"name": "downfall-godot", "engine_version": "Godot 4.7.2.stable.official.ed1daf0bf",
             "revision": REV, "repo": "https://github.com/coldfish432/GodotGame"},
    "note": "godot-gamedev, walker mode. Gameplay beats are real native 3840x2160 Godot captures from an isolated clone "
            "of 111bf6e (window override + MJPEG quality only), scripted input, not a human playtest. See CAPTURE.md.",
    "tags": ["Godot 4", "godot-gamedev", "generated assets", "game audio", "Kokoro", "Remotion", "Claude", "course assignment"]},
    "beats": beats}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, ensure_ascii=False, indent=1), encoding="utf-8")
print("beats", len(beats))
