"""Author beat_sheet.json for the walker-survival-shooting Assignment 6 gamedev film (particle effects).

Pass 1 (no args): narration, shots and props with placeholder durations.
Pass 2 (--sync): after Kokoro has measured audio, converts cue fractions into seconds.
--rebuild: re-author but keep measured audio/render fields of beats whose narration is unchanged.
--tbd: list every value still marked [TBD ...] (the film must not be voiced while any remain).
All code excerpt text is read at run time from GAME, a `git archive` of the submitted course-repository
revision (never retyped).
Run:  python -I scripts/author_sheet.py [--sync | --rebuild | --tbd]
"""
import json
import re
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
A6 = REEL.parents[1]
GAME = A6 / "game" / "godot"          # git archive of the course repo at 1828bb6b, read only
PUB = "claude-liam-walker-survival-shooting-a6-gamedev"
SLUG = PUB
PROJECT = "project_survival_shooting"

# ---- values decided by the user (A5 choices reused; see FACTCHECK.md) ----------------------------
TITLE = "claude-liam-walker-survival-shooting-a6-gamedev"
GREETING = "Hola"
REV = "1828bb6b"
REV_SPOKEN = "one, eight, two, eight, b, b, six, b"
SRC = f"walker-survival-shooting @ {REV} (course repository, assignment-6)"
PLAY_A_FRAMES = 702          # media/B08.mp4: 351 frames, then the same 351 as a 2x crop
PLAY_B_FRAMES = 391          # media/B16.mp4


def lines(path, a, b):
    return "\n".join((GAME / path).read_text(encoding="utf-8").splitlines()[a - 1:b])


def beat(bid, act, narration, pattern, props, show, cues=None, **extra):
    b = {"beat_id": bid, "act": act, "narration_text": narration, "voice": "am_onyx",
         "engine": "kokoro", "estimated_duration_s": max(6, round(len(narration.split()) / 2.6, 1)),
         "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion",
                  "show": [{"at": a, "event": e} for a, e in show],
                  "remotion": {"pattern": pattern, "props": props}}}
    if cues:
        b["shot"]["cue_fracs"] = cues
    for k, v in extra.items():
        if k == "shot_extra":
            b["shot"].update(v)
        else:
            b[k] = v
    return b


def figure(bid, narration, title, status, image, source, cards, show, cues, evidence=True, act="RESULT", **extra):
    props = {"title": title, "status": status, "image": f"{PUB}/{image}", "imageLabel": f"figures/{image}",
             "excerpt": "", "source": source, "cards": cards}
    if evidence:
        extra.setdefault("shot_extra", {})["evidence_media"] = f"figures/{image}"
    return beat(bid, act, narration, "GodotDesignFigure", props, show, cues, **extra)


def workbench(bid, narration, title, path, start, end, notes, output, show, cues, **extra):
    props = {"mode": "code", "title": title, "project": PROJECT,
             "path": f"{path}  ·  lines {start}–{end}", "code": lines(path, start, end),
             "startLine": start, "codeFontSize": 26 if end - start < 9 else (22 if end - start < 13 else 17),
             "source": f"{SRC} · godot/{path} lines {start}–{end}",
             "inspectorLabel": "Source notes — derived from these lines", "notes": notes, "output": output}
    return beat(bid, "CODE", narration, "GodotDevWorkbench", props, show, cues, **extra)


def footage(bid, narration, media, show, label_note):
    b = beat(bid, "RESULT", narration, None, None, show,
             role_note=f"Real native-4K engine footage. {label_note} Labels burned in by scripts/prepare_media.py. "
                       "No retiming; a labelled final-frame hold only if narration is longer.",
             qc={"full_bleed": True, "contrast_regions": [{"label": "burned-in disclosure label",
                                                           "box": [0.02, 0.935, 0.98, 0.995]}],
                 "contrast_reason": "Edge-to-edge native Godot render; the essential text is the label strip."})
    b["shot"] = {"type": "SCREEN", "class": "SHOW", "source": "own", "evidence_media": media,
                 "show": b["shot"]["show"]}
    return b


BEATS = []

# -- B00 walker cold open -----------------------------------------------------------------------
PROMPT = ("Please use Walker to convert my game design document about a third-person extraction shooter, where a "
          "survivor lives in a subway base, into its first particle effects: dust at the player's feet on every "
          "landing, and dust hanging in the air of the base only while the ceiling lights are on, with a brief, "
          "read-back tests, frame strips and a price for each.")
BEATS.append(beat("B00", "ASK",
    f"{GREETING}, this is Liam, narrating for Jonathan. The prompt on screen is a reconstruction for this film, not a "
    "saved session. It asks Walker to give a subway extraction shooter its first particle effects: dust when the "
    "player lands, and dust in the air that lives only while the lights are on. "
    f"At source revision {REV_SPOKEN}, the answer is two effects, four tests, a cost script, and eighteen fixture strips.",
    "ClaudeComposerAsk",
    {"greeting": GREETING, "topic": "GODOT · GAMEDEV · WALKER",
     "segment": "Reconstructed prompt (illustrative, not a saved session)", "command": PROMPT,
     "runningText": f"reading the submitted revision {REV}…", "modelLabel": "Opus 5.5", "largeText": True,
     "output": ["Reconstruction for this film, not a historical transcript.",
                "Built: Effect A landing dust (2 emitters); Effect B light dust (1300 specks).",
                "Checked: 157 / 27 / 110 / 41 PASS; GPU +0.001 ms and +0.017 ms."]},
    [("0.02", f"composer fades in; greeting '{GREETING}'"), ("0.15", "reconstructed prompt types in"),
     ("0.6", "running line names the revision"), ("0.75", "three answer lines land")]))

# -- B01 hesitant writer -----------------------------------------------------------------------
BEATS.append(beat("B01", "BLUF",
    "Claude built the particles from my brief; I judged every strip and every change. The tests prove the "
    "settings and the timing; only the pictures show the look.",
    "BrutalistHesitantWriter",
    {"text": "Claude made my\nparticle effects.", "triggerWords": "Claude made",
     "replacementWords": "I directed and Claude built", "fontSize": 104, "lineSpacing": 1.4, "align": "center",
     "seed": "walker-survival-shooting-a6", "mistakeRate": 2, "hesitateWithin": 0, "hesitateBetween": 1,
     "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
    [("0.0", "typing starts"), ("0.3", "'Claude made' typed, marked"), ("0.45", "corrected to 'I directed and "
     "Claude built'"), ("0.8", "sentence settles")],
    lead_silence_s=0.8,
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer typing bookend; mostly page by design."},
    role_note="EXECUTIVE-SUMMARY LAW. Correction = the likely misconception (the AI made the effects unsupervised)."))

# -- B02 the game and both effects ----------------------------------------------------------------
BEATS.append(figure("B02",
    "The game: a survivor in a subway base. Effect A is landing dust. Its job is to say you touched the ground, "
    "and its event is a new signal, landed, on the character's body. Effect B is dust hanging in the air, for "
    "atmosphere. Its condition is the ceiling lights: on, the dust is there; off, it is gone.",
    "The game and its two effects", "Native Godot renders, 3840x2160, scripted input · left: Effect A, player camera · right: Effect B, film camera",
    "fig_game.png", f"{SRC} · this film's captures landing-run-02 f62, lights-film-01 f290",
    [{"label": "Effect A", "text": "event: Humanoid.landed (Space)"},
     {"label": "Effect B", "text": "condition: CeilingLights on (F)"},
     {"label": "Both", "text": "GPUParticles3D, effects/*.tscn"}],
    [("0.0", "both captures"), ("0.3", "Effect A card"), ("0.65", "Effect B card")],
    [(0.15, 0), (0.55, 1), (0.85, 2)], evidence=False, act="SETUP"))

# -- Effect A ----------------------------------------------------------------------------------------
BEATS.append(figure("B03",
    "Before anything was built, I wrote the intent. Timing: strongest at a tenth and a half of a second, gone at "
    "one point six. Scale: about one and a half capsules wide. Two layers: dust, and a faint ring on the floor. "
    "And the retrigger rule: a second landing restarts it, so at most one burst is alive.",
    "Effect A · the intent block", "CHANGE-BRIEF.md, committed before the first agent prompt",
    "fig_a_intent.png", f"{SRC} · CHANGE-BRIEF.md, Effect A",
    [{"label": "Timing", "text": "peak 0.15 s, gone 1.6 s"},
     {"label": "Layers", "text": "Dust 24 + GroundRing 1"},
     {"label": "Retrigger", "text": "restart(); peak 25"}],
    [("0.0", "intent page"), ("0.3", "timing"), ("0.6", "layers"), ("0.85", "retrigger")],
    [(0.2, 0), (0.6, 1), (0.85, 2)], evidence=False, act="INTENT"))

BEATS.append(workbench("B04",
    "A particle system has three parts, and this one node shows all three. Emission: how many and when. Line "
    "one seventeen, twenty-four particles; one-shot, all at once on line one twenty-one. Process: what each "
    "particle does over its life, here a ParticleProcessMaterial on line one twenty-four. Draw: what each "
    "particle looks like, a quad mesh on line one twenty-five.",
    "Three parts · landing_dust.tscn", "effects/landing_dust.tscn", 113, 125,
    [{"label": "Emission", "value": "lines 117–121"},
     {"label": "Process", "value": "line 124"},
     {"label": "Draw", "value": "line 125: 0.32 m quad"}],
    ["Scene written by the agent from my brief (prompt-2)"],
    [("0.0", "reconstruction of the Dust node"), ("0.2", "emission lines"), ("0.6", "process line"),
     ("0.85", "draw line")],
    [(0.2, 117, "emission: 24 particles"), (0.35, 121, "all at once"), (0.6, 124, "process: what each does"),
     (0.85, 125, "draw: what each looks like")]))
BEATS.append(figure("B05",
    "The first strip, r zero, from the preview scene, a fixture. Triggered on frame ten; the picture first "
    "changes on frame eleven. The ring is clear. The dust is a few warm dots, gone by frame thirty. My verdict "
    "before Claude read anything: I want grey cloud-like puffs, not dots.",
    "Effect A · first strip r0", "FIXTURE capture: preview scene, Movie Maker, 30 fps, 2048x1152, cropped; top bright, bottom dark",
    "fig_a_r0.png", f"{SRC} · captures/landing_dust/r0/bright-fade, dark-fade · TUNING.md r0",
    [{"label": "Frames", "text": "12 · 15 · 30 · 50"},
     {"label": "Reads as", "text": "dots, gone by frame 30"},
     {"label": "My verdict", "text": "grey puffs, not dots"}],
    [("0.0", "bright row then dark row"), ("0.4", "ring at 15 and 20"), ("0.8", "verdict")],
    [(0.2, 0), (0.55, 1), (0.85, 2)]))
BEATS.append(figure("B06",
    "That wish broke the brief's ankle-height rule, so I revised the intent first, then tuned. Revision r one "
    "changed one setting: the dust quad from eight to thirty-two centimetres. The agent edited before my "
    "approval, and sent its prediction afterwards; I approved after the fact and kept it. Its prediction held at "
    "most frames, including thirty: bigger, still visible at point seven seconds. At frame fifty it missed. I stopped "
    "tuning here, on my in-game judgement.",
    "Effect A · revision r1: the Dust quad grows fourfold", "FIXTURE captures: top row r0, bottom row r1, same frames",
    "fig_a_r1.png", f"{SRC} · captures/landing_dust/r0, r1 · TUNING.md r1 · CHANGE-BRIEF revisions",
    [{"label": "Change", "text": "Dust quad 0.08 → 0.32 m"},
     {"label": "Order", "text": "edited before my approval"},
     {"label": "Prediction", "text": "most held; f50 missed"},
     {"label": "Verdict", "text": "kept; tuning stops at r1"}],
    [("0.0", "r0 over r1"), ("0.3", "change"), ("0.5", "edit before approval"), ("0.7", "prediction"),
     ("0.9", "verdict")],
    [(0.2, 0), (0.42, 1), (0.68, 2), (0.9, 3)], act="TUNING"))

BEATS.append(workbench("B07",
    "Now the event. After every move, the body asks: am I on the floor now, and was I in the air last frame? Then "
    "this frame is a landing, and line one thirteen emits landed, once. Line one fifteen is a fix: on load, "
    "the physics engine pushed the player up out of the floor, which counted as a landing. The test caught it.",
    "The event · humanoid.gd", "characters/human/humanoid/humanoid.gd", 109, 115,
    [{"label": "Called", "value": "every physics frame"},
     {"label": "Emits", "value": "landed, notify-only"},
     {"label": "Fix", "value": "_has_touched_floor (my choice)"}],
    ["Written by the agent (prompt-3), fix chosen by me"],
    [("0.0", "reconstruction of _notify_landing()"), ("0.35", "the landing test"), ("0.55", "emit once"),
     ("0.85", "the scene-load fix")],
    [(0.3, 112, "air last frame, floor now"), (0.55, 113, "announce once"), (0.85, 115, "no landing on load")]))
BEATS.append(footage("B08",
    "In the running game, with scripted key presses. Two single jumps: dust and a ring at the feet. Then four "
    "rapid jumps, mostly while moving left, each landing inside the last burst's lifetime. Each time, the old dust is "
    "cleared and plays again where the feet are. Replayed at twice the size: no pile-up.",
    "media/B08.mp4",
    [("0.0", "full frame, landings 1-2"), ("0.25", "rapid jumps 3-6"), ("0.5", "replay as a 2x crop")],
    "Scripted Space/A input (captures/landing-run-02); second half is the same frames as a labelled 2x crop."))

BEATS.append(workbench("B09",
    "The trigger listens to landed. It moves to the feet, then calls restart on both emitters, not emitting "
    "equals true. Restart clears a burst that is still alive and starts a new one here. Setting emitting would "
    "do nothing to a live one-shot burst.",
    "The retrigger · landing_dust_trigger.gd", "effects/landing_dust_trigger.gd", 38, 41,
    [{"label": "Called", "value": "by Humanoid.landed, once per landing"},
     {"label": "Rule", "value": "restart(): at most one burst alive"},
     {"label": "Writes", "value": "only its own position (presentation)"}],
    ["Written by the agent (prompt-3)"],
    [("0.0", "reconstruction"), ("0.3", "move to the feet"), ("0.65", "restart both")],
    [(0.3, 39, "stand on the landing point"), (0.6, 40, "clear and replay the dust"),
     (0.85, 41, "and the ring")]))
BEATS.append(figure("B10",
    "The retrigger strip: a second landing on frame twenty-five, half a metre away. On twenty-five the old dust "
    "is gone; on twenty-seven the new ring starts at the new spot; the old cloud never comes back. The state "
    "test checks the same rule by real key presses: with emitting equals true instead, it fails.",
    "Effect A · retrigger strip", "FIXTURE capture, r1: frames 24 · 25 · 26 (top), 27 · 30 · 35 (bottom); second landing at frame 25",
    "fig_a_retrigger.png", f"{SRC} · captures/landing_dust/r1/bright-retrigger · TEST-REPORT Step 3",
    [{"label": "f25", "text": "old burst cleared"},
     {"label": "f27", "text": "new ring at the new spot"},
     {"label": "Test", "text": "emitting = true → 22 PASS, 5 FAIL"}],
    [("0.0", "six frames"), ("0.3", "f25"), ("0.55", "f27"), ("0.8", "test")],
    [(0.25, 0), (0.5, 1), (0.85, 2)]))

# -- Effect B ----------------------------------------------------------------------------------------
BEATS.append(figure("B11",
    "Effect B has a different job: atmosphere, not feedback. Its first intent was a small box of dust under one "
    "light. It must already be settled on its first frame, frozen when paused, gone when hidden or when the "
    "lights go off. Later I revised it to fill the whole room, lit by the lights.",
    "Effect B · the intent block", "CHANGE-BRIEF.md, Effect B and its 2026-11-12 revision",
    "fig_b_intent.png", f"{SRC} · CHANGE-BRIEF.md, Effect B",
    [{"label": "Job", "text": "ambience, while lights are on"},
     {"label": "States", "text": "settled · frozen · gone"},
     {"label": "Revised", "text": "whole room, lit"}],
    [("0.0", "intent page"), ("0.3", "job"), ("0.6", "states"), ("0.85", "revision")],
    [(0.2, 0), (0.55, 1), (0.85, 2)], evidence=False, act="INTENT"))
BEATS.append(workbench("B12",
    "Its process material uses what Effect A does not. A box emission shape, moved to the room's centre by an "
    "offset. Turbulence, so specks drift on noise instead of straight lines. And an opacity ramp with several "
    "peaks, so each speck twinkles in and out. The draw material adds light rather than covering, and preprocess "
    "runs six seconds before the first frame.",
    "Features A lacks · light_dust.tscn", "effects/light_dust.tscn", 12, 26,
    [{"label": "Box", "value": "lines 12–14"},
     {"label": "Turbulence", "value": "line 25 (to 29)"},
     {"label": "Elsewhere", "value": "ADD + lit 45–46"}],
    ["Built by the agent; redesigned by Claude Code at my request"],
    [("0.0", "reconstruction of the process material"), ("0.2", "box and offset"), ("0.5", "turbulence"),
     ("0.8", "ramp")],
    [(0.2, 12, "box emission"), (0.32, 13, "moved to the room centre"), (0.55, 25, "turbulence"),
     (0.8, 24, "the twinkling ramp")]))
BEATS.append(figure("B13",
    "The specks are one or two pixels, so each raw crop sits beside a computed difference against a frame with "
    "the dust hidden. First strip, r zero: a hundred and fifty specks under one light. I said the size should "
    "vary, and it was too dense. Revision r one changed one setting, amount, from a hundred and fifty to ninety. "
    "The agent proposed first this time; its prediction, about seventy changed pixels, measured seventy-four. Kept.",
    "Effect B · r0 → r1: amount 150 → 90", "FIXTURE captures, cropped; difference tiles are computed analysis",
    "fig_b_r0r1.png", f"{SRC} · captures/light_dust/r0, r1 (dark) · TUNING.md Effect B",
    [{"label": "r0", "text": "150 specks, about 115 px"},
     {"label": "r1", "text": "90: predicted ~70, got 74"},
     {"label": "Verdict", "text": "kept: \"Much better\""}],
    [("0.0", "raw and difference, r0 then r1"), ("0.4", "r0"), ("0.7", "r1"), ("0.9", "verdict")],
    [(0.3, 0), (0.7, 1), (0.92, 2)], act="TUNING"))
BEATS.append(figure("B14",
    "Then, in the game, I had to walk up to a light to see anything. So I asked for the whole room, lit by the "
    "lights, sizes from three millimetres to three centimetres, all at once. That is a redesign recorded in the "
    "brief, not a tuning round. Three thousand specks was too dense and too bright; I chose nine hundred at half "
    "brightness, then thirteen hundred.",
    "Effect B · redesign (not a tuning round)", "FIXTURE captures, whole frame; computed differences",
    "fig_b_redesign.png", f"{SRC} · captures/light_dust/redesign, redesign-2 · CHANGE-BRIEF revisions",
    [{"label": "Box", "text": "14 x 2.6 x 9 m, lit per pixel"},
     {"label": "Pass 1", "text": "3000: too dense, too bright"},
     {"label": "Final", "text": "1300, half brightness"}],
    [("0.0", "3000 left, 1300 right"), ("0.4", "pass 1"), ("0.8", "final")],
    [(0.25, 0), (0.6, 1), (0.88, 2)], act="TUNING"))

BEATS.append(workbench("B15",
    "The condition lives in a listener on the dust. Lights on: show it and restart once, which reruns "
    "preprocess. Lights off: hidden that frame, and no new births. It never touches the lights; it only reads "
    "them.",
    "The condition · light_dust_listener.gd", "effects/light_dust_listener.gd", 43, 51,
    [{"label": "Called", "value": "lights_changed, and once at start"},
     {"label": "On", "value": "visible + exactly one restart()"},
     {"label": "Off", "value": "visible = false, emitting = false"}],
    ["Written by the agent (prompt-5-wire), changes asked by Claude"],
    [("0.0", "reconstruction"), ("0.3", "lights on"), ("0.75", "lights off")],
    [(0.3, 46, "on: restart once"), (0.55, 48, "or show, and restart there"), (0.85, 50, "off: hidden at once")]))
BEATS.append(footage("B16",
    "In the game, through a film camera near the first light, with scripted F presses at the switch. The inset is "
    "computed: it shows where the dust is. Lights off, the dust is gone that frame. Lights on, it is back already "
    "spread out. Paused from code, it freezes. Hidden, gone; shown again, full at once.",
    "media/B16.mp4",
    [("0.0", "lights on"), ("0.3", "F: off"), ("0.45", "F: on, spread at once"), ("0.6", "paused"),
     ("0.75", "hidden, then shown")],
    "Film camera added by the capture script; scripted S/F input; pause and hide set from code "
    "(captures/lights-film-01). Inset is a computed difference."))
BEATS[-1]["hold_s"] = 3.0      # measured narration 15.66 s > clip 13.03 s: labelled held final frame (prepare_media --hold-b 3)

# -- the generated process shader ------------------------------------------------------------------
BEATS.append(workbench("B17",
    "I converted Effect B's process material into a shader in the editor. Line two sixty-one is my brief's box: "
    "a random point in a cube, times emission box extents, seven, one point three, four point five. Line two "
    "sixty-three adds the offset, zero, point one five, three point two. That is why the box is fourteen by nine "
    "metres and centred on the room.",
    "Generated process shader · emission box", "shaders/particles_generated.gdshader", 257, 264,
    [{"label": "Line 261", "value": "brief extents (7, 1.3, 4.5)"},
     {"label": "Line 263", "value": "brief offset (0, 0.15, 3.2)"},
     {"label": "Runs", "value": "once per particle, at birth"}],
    ["Generated by Godot 4.7.2 from my conversion; unedited"],
    [("0.0", "reconstruction of the generated lines"), ("0.35", "line 261"), ("0.75", "line 263")],
    [(0.35, 261, "random point in the box"), (0.75, 263, "plus the offset")]))
BEATS.append(figure("B18",
    "And here is that box on screen: the computed difference of the final strip spans the whole frame, not one "
    "light. The settings decide where specks are born; the shader is the code that does it, on the GPU.",
    "Result · the box, filled", "FIXTURE capture redesign-2 (right): computed difference, whole frame",
    "fig_b_redesign.png", f"{SRC} · captures/light_dust/redesign-2 · shaders/particles_generated.gdshader 261–263",
    [{"label": "Brief", "text": "extents (7, 1.3, 4.5)"},
     {"label": "Brief", "text": "offset (0, 0.15, 3.2)"},
     {"label": "Screen", "text": "specks across the room"}],
    [("0.0", "whole-room difference"), ("0.5", "brief rows"), ("0.85", "screen")],
    [(0.2, 0), (0.45, 1), (0.8, 2)]))
BEATS.append(workbench("B19",
    "Line two fifty-three runs every frame: the colour is multiplied by the colour ramp at the particle's age. "
    "That is my opacity ramp, zero, point six, point one five, point nine, and so on, so each speck brightens and "
    "dims several times. Gravity is lines three ninety-seven and four ten, but both effects set gravity to zero.",
    "Generated process shader · colour over life", "shaders/particles_generated.gdshader", 251, 255,
    [{"label": "Line 253", "value": "= brief opacity ramp, 8 stops"},
     {"label": "Lines 397, 410", "value": "gravity → velocity (0 here)"},
     {"label": "Not here", "value": "amount, lifetime: on the node"}],
    ["Generated by Godot 4.7.2; unedited"],
    [("0.0", "reconstruction"), ("0.4", "line 253"), ("0.85", "gravity note")],
    [(0.4, 253, "colour times the ramp at this age")]))
BEATS.append(figure("B20",
    "The ramp on screen, in the final fixture strip. Frames eleven and forty have the same density but "
    "different specks lit. Paused, frames forty-six and fifty-four are identical. Hidden, nothing. Shown on "
    "sixty-six, full at once. Lights off on seventy-one, nothing left glowing.",
    "Result · twinkle, pause, hide, off", "FIXTURE capture redesign-2: computed differences against the dust hidden",
    "fig_b_timeline.png", f"{SRC} · captures/light_dust/redesign-2/dark · TUNING.md",
    [{"label": "f11 / f40", "text": "same density, specks differ"},
     {"label": "f46 = f54", "text": "paused: identical"},
     {"label": "f61 / f71", "text": "hidden · lights off: none"}],
    [("0.0", "ten frames"), ("0.3", "11, 40"), ("0.55", "46 = 54"), ("0.8", "61, 66, 71")],
    [(0.2, 0), (0.5, 1), (0.85, 2)]))

# -- verification and price -------------------------------------------------------------------------
BEATS.append(workbench("B21",
    "The tests read settings back from the loaded scene. First they ask ClassDB whether each property name "
    "exists in this engine, so a stale name fails loudly. Then every value is compared with the brief.",
    "Read-back · test_landing_dust_config.gd", "tests/test_landing_dust_config.gd", 100, 106,
    [{"label": "Names", "value": "44 names checked in ClassDB"},
     {"label": "Values", "value": "every brief setting read back"},
     {"label": "Mode", "value": "headless, --fixed-fps 60, run by me"}],
    ["Written by the agent (prompt-2)"],
    [("0.0", "reconstruction"), ("0.4", "ClassDB"), ("0.8", "the check")],
    [(0.4, 103, "every property this engine has"), (0.8, 106, "missing name = FAIL")]))
BEATS.append(figure("B22",
    "All four pass, headless at sixty frames per second: a hundred fifty-seven, twenty-seven, a hundred ten and "
    "forty-one. The state tests press real keys: Space and D for landings, S and F for the lights, and check "
    "restart counts, pause and hide.",
    "Result · what the tests proved", "Recorded test output, copied verbatim",
    "fig_log_tests.png", f"{SRC} · logs/test_*_60fps.log · TEST-REPORT",
    [{"label": "Config", "text": "157 · 110 PASS"},
     {"label": "State", "text": "27 · 41 PASS, real keys"},
     {"label": "Retrigger", "text": "old burst never finishes"}],
    [("0.0", "four logs"), ("0.35", "config"), ("0.65", "state"), ("0.85", "retrigger")],
    [(0.25, 0), (0.55, 1), (0.85, 2)]))
BEATS.append(figure("B23",
    "Then I broke it. Mutation one: the Godot three name, initial velocity. The engine loaded it silently; in "
    "four point seven that name is an editor-only pair, so the float is dropped and the minimum speed becomes "
    "zero. Only the read-back caught it. Mutation two: amount thirty, brief unchanged. Both exit one.",
    "Result · the mutations fail", "Recorded test output, copied verbatim",
    "fig_log_mutations.png", f"{SRC} · logs/mutation_1_godot3_name_60fps.log, mutation_2_value_drift_60fps.log",
    [{"label": "Godot 3 name", "text": "no error; min 0.6 → 0.0"},
     {"label": "Value drift", "text": "amount 24 → 30"},
     {"label": "Both", "text": "156 PASS, 1 FAIL, exit 1"}],
    [("0.0", "failing lines"), ("0.35", "mutation 1"), ("0.7", "mutation 2")], [(0.3, 0), (0.7, 1), (0.9, 2)]))

BEATS.append(workbench("B24",
    "The headless price, the chapter's way: time each frame as the gap between two process frames, three hundred "
    "frames, three repeats, round-robin, with an empty-scene control and a ten thousand CPU-particle control.",
    "Headless CPU price · cost_effects.gd", "tests/cost_effects.gd", 102, 111,
    [{"label": "Cases", "value": "empty · off · A · B · CPU control"},
     {"label": "Frames", "value": "60 warm-up, 300 timed, 3 repeats"},
     {"label": "Mode", "value": "headless, --fixed-fps 60"}],
    ["Written by the agent (prompt-7)"],
    [("0.0", "reconstruction"), ("0.4", "timing loop"), ("0.8", "per-frame times")],
    [(0.4, 106, "one frame"), (0.65, 107, "read the clock"), (0.85, 109, "add to the total")]))
BEATS.append(figure("B25",
    "Empty scene: point zero zero four milliseconds. Ten thousand CPU particles: one point eight eight. So the "
    "script sees CPU work. Effect A adds point zero zero six, Effect B point zero two five, both inside the "
    "noise. That is expected: headless Godot uses a dummy renderer, so GPU simulation and drawing never run. "
    "Near zero says nothing about the GPU.",
    "Result · headless price near zero", "Recorded output of cost_effects.gd, copied verbatim",
    "fig_log_cost.png", f"{SRC} · logs/cost_effects_60fps.log",
    [{"label": "Control", "text": "empty 0.004 · CPU 1.88 ms"},
     {"label": "Effects", "text": "+0.006 · +0.025 ms, in noise"},
     {"label": "Why", "text": "dummy renderer: no GPU work"}],
    [("0.0", "cost log"), ("0.3", "controls"), ("0.6", "effects"), ("0.85", "why")],
    [(0.2, 0), (0.55, 1), (0.85, 2)]))
BEATS.append(figure("B26",
    "The GPU price, on an R T X fifty-seventy Ti laptop GPU, windowed, vsync off, lights kept on, reading the "
    "engine's measured GPU time. Effect B adds point zero one seven milliseconds against a point three budget; "
    "Effect A about point zero zero one against point two. With vsync on, F P S reads one forty-four; my debug "
    "key V turns it off, and F P S rises to about thirteen fifty, so the comparison is not capped.",
    "Result · GPU price against the budget", "Recorded output of gpu_price.gd (two runs) · TEST-REPORT Use It",
    "fig_log_gpu.png", f"{SRC} · logs/gpu_price.log · TEST-REPORT GPU price and FPS",
    [{"label": "Effect B", "text": "+0.017 ms ≤ 0.3 ms"},
     {"label": "Effect A", "text": "+0.001 ms ≤ 0.2 ms"},
     {"label": "Vsync key V", "text": "144 → about 1350 FPS"}],
    [("0.0", "gpu log"), ("0.35", "B"), ("0.6", "A"), ("0.85", "vsync")],
    [(0.3, 0), (0.6, 1), (0.85, 2)]))

# -- limits, judgement -------------------------------------------------------------------------------
BEATS.append(figure("B27",
    "What no headless run can show: whether anything is visible, reads well, or is too bright. That is the "
    "strips and my own play. One thing I am not sure of: Effect A's visibility box. Since r one, the puffs reach "
    "point two three metres up and point six eight out, beyond the box's point two and point six, so they may "
    "vanish early at the screen edge. Enlarging it is my next step.",
    "Limits and what remains uncertain", "TEST-REPORT Use It · README Known limitations",
    "fig_a_r1.png", f"{SRC} · README.md, TEST-REPORT.md",
    [{"label": "Headless", "text": "settings + timing, no pixels"},
     {"label": "Uncertain", "text": "A visibility_aabb too small"},
     {"label": "Next step", "text": "enlarge it, one revision"}],
    [("0.0", "r0/r1 strips again"), ("0.3", "headless"), ("0.6", "aabb"), ("0.85", "next step")],
    [(0.2, 0), (0.55, 1), (0.85, 2)], evidence=False, act="LIMITS"))
BEATS.append(figure("B28",
    "Agent mistakes I caught: it forgot the fixed seed on the preview; its first wiring fired the dust on scene "
    "load; and in tuning it edited before I approved. Claude's strip readings I overruled: it said the dust was "
    "too warm, cut flat by the floor, hidden by the capsule, and not six to eight separate puffs. In the game I "
    "do not see those as problems. A human lands, not a mech.",
    "Claude against me", "TUNING.md Effect A r1 · FRICTIONAL.md Steps 2–4",
    "fig_a_retrigger.png", f"{SRC} · TUNING.md, FRICTIONAL.md",
    [{"label": "Caught", "text": "seed · load trigger · early edit"},
     {"label": "Overruled", "text": "warm · flat · hidden · merged"},
     {"label": "Why", "text": "my in-game judgement"}],
    [("0.0", "strip"), ("0.3", "caught"), ("0.65", "overruled"), ("0.9", "why")],
    [(0.25, 0), (0.6, 1), (0.9, 2)], evidence=False, act="JUDGEMENT"))

# -- verdict, your turn, outro -----------------------------------------------------------------------
BEATS.append(beat("B29", "VERDICT",
    "Verdict. Built: two effects, their triggers, four tests, a cost script and a GPU helper. Human: the brief, "
    "every verdict, the redesign values, the shader conversion and the play test. AI: the scenes, tests, "
    "previews and strip readings, by Claude Code with Opus five point five; and this narration, by local Kokoro. "
    "Textures: none from outside; both effects draw with gradient textures defined in their scene files. "
    f"Shown: revision {REV_SPOKEN}. Next: enlarge Effect A's visibility box.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Verdict", "artifactHeading": f"Walker Survival Shooting at {REV}.",
     "brandLabel": "@NikBearBrown",
     "artifactLines": ["Built: landing dust + light dust, triggers, 4 tests, cost script, GPU helper.",
                       "Human: brief, verdicts, redesign values, shader conversion, play test.",
                       "AI: scenes, tests, previews, strip readings (Claude Code, Opus 5.5); narration (Kokoro).",
                       "Textures: none from outside; GradientTexture2D in the scene files.",
                       "Uncertain: Effect A visibility_aabb  ·  Next: enlarge it as its own revision"]},
    [("0.0", "verdict page"), ("0.2", "built"), ("0.4", "human / AI"), ("0.7", "textures"), ("0.85", "next")]))
YT = ("Please use Walker on my Godot project. Read my CHANGE-BRIEF and effects/landing_dust.tscn. Enlarge the Dust "
      "emitter's visibility_aabb so it contains the r1 puffs. Before you change anything, predict what my "
      "edge-of-screen check will show, then capture again and compare.")
BEATS.append(beat("B30", "HANDOFF",
    "Your turn. Paste this into Claude. " + YT.replace("effects/landing_dust.tscn", "my landing dust scene")
    .replace("CHANGE-BRIEF", "change brief").replace("visibility_aabb", "visibility box") +
    " The prediction is the point: write down what should change before you look. This was Liam, narrating for "
    "Jonathan.",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "GODOT · GAMEDEV · WALKER", "segment": "Walker Survival Shooting",
     "command": YT, "runningText": "paste this into Claude…", "output": [], "modelLabel": "Opus 5.5",
     "largeText": True},
    [("0.02", "composer 'Your turn.'"), ("0.1", "prompt types in"), ("0.7", "send arms"), ("0.9", "sign-off")],
    role_note="HANDOFF LAW: prompt read aloud verbatim (two names spoken in words), then discussed; Liam signs off."))
BEATS.append({"beat_id": "B31", "act": "OUTRO", "kind": "outro_voice",
    "narration_text": "claude liam, walker survival shooting, a six, gamedev. At Nik Bear Brown.",
    "title_spoken_note": "TTS-friendly reading of the exact title " + TITLE, "voice": "am_onyx", "engine": "kokoro",
    "estimated_duration_s": 5, "tail_hold_s": 1.0,
    "role_note": "OUTRO-LOCK: exact title, hardcoded @NikBearBrown, slug-seeded mascot, no subline, spoken, no jingle.",
    "shot": {"type": "GRAPHIC", "class": "CARD", "source": "remotion",
             "show": [{"at": "0.0", "event": "title card, handle, mascot"}],
             "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG}}}})

METADATA = {
    "title": TITLE, "slug": SLUG, "topic": "GODOT · GAMEDEV · WALKER", "kind": "gamedev",
    "skill": "godot-gamedev", "mode": "walker", "brand": "claude-liam", "register": "Teardown",
    "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx", "palette": "claude",
    "aspect_ratio": "16:9", "fps": 30, "fit": "contain", "captions": False,
    "channel": "@NikBearBrown", "folderLabel": "@NikBearBrown", "persona": "Liam (narrating for Jonathan)",
    "in_for_bear": False, "greeting": GREETING,
    "greeting_note": "A5 choices reused: greeting Hola, narrator line 'Liam, narrating for Jonathan'.",
    "game": {"name": "walker-survival-shooting", "source_revision": REV,
             "engine": "Godot 4.7.2.stable.official.ed1daf0bf", "game_path": f"walker-survival-shooting/godot ({REV})"},
    "note": "godot-gamedev walker film for Assignment 6 (particle effects). Engine images: the submitted fixture "
            "frame strips (preview scenes, labelled FIXTURE) and this film's native-4K captures of the unmodified "
            "project with scripted input (one with a film camera added by the capture script; pause and hide set "
            "from code; all labelled). Difference images are computed analysis and labelled. No game change, no "
            "commit, no push, no publication.",
}


def write(sheet):
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=True) + "\n", encoding="ascii")


CLIPS = {"B08": PLAY_A_FRAMES, "B16": PLAY_B_FRAMES}


def sync():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    for b in sheet["beats"]:
        if b["beat_id"] in CLIPS:                      # real footage: the clip's own length (plus any labelled hold)
            hold = b.get("hold_s", 0.0)
            b["render_duration_s"] = CLIPS[b["beat_id"]] / 30 + hold
        d = b.get("actual_duration_s")
        rem = (b.get("shot") or {}).get("remotion")
        if not d or not rem:
            continue
        props = rem["props"]
        props["durationSeconds"] = round(d, 6)
        fr = b["shot"].get("cue_fracs")
        if fr:
            if rem["pattern"] == "GodotDevWorkbench":
                props["cues"] = [{"at": round(f[0] * d, 3), "line": f[1], "label": f[2]} for f in fr]
            else:
                props["cues"] = [{"at": round(f * d, 3), "card": c} for f, c in fr]
    write(sheet)


def rebuild():
    old = {b["beat_id"]: b for b in json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))["beats"]}
    for b in BEATS:
        o = old.get(b["beat_id"], {})
        if o.get("narration_text") != b.get("narration_text"):
            continue
        for k in ("actual_duration_s", "audio_file", "render_duration_s", "build", "hold_s"):
            if k in o:
                b[k] = o[k]
        r = ((o.get("shot") or {}).get("remotion") or {}).get("rendered")
        if r and b.get("shot", {}).get("remotion"):
            b["shot"]["remotion"]["rendered"] = r
    write({"metadata": METADATA, "beats": BEATS})
    sync()


def tbd():
    text = json.dumps({"metadata": METADATA, "beats": BEATS}, ensure_ascii=False)
    found = sorted(set(re.findall(r"\[TB[DC][^\]]*\]", text)))
    print("TBD values:", found or "none")
    return 1 if found else 0


if __name__ == "__main__":
    if "--tbd" in sys.argv:
        sys.exit(tbd())
    if "--rebuild" in sys.argv:
        rebuild()
    elif "--sync" in sys.argv:
        sync()
    else:
        write({"metadata": METADATA, "beats": BEATS})
    print("beat_sheet.json written:", len(BEATS), "beats")
