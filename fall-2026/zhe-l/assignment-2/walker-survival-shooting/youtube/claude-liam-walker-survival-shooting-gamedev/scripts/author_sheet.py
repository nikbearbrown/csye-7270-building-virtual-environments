"""Author beat_sheet.json for the walker-survival-shooting gamedev film.

Pass 1 (no args): writes narration, shots and props with placeholder durations.
Pass 2 (--sync): after Kokoro has measured audio, converts each beat's cue
fractions into seconds and sets durationSeconds from the measured duration.
All excerpt text is read from the --game copy at run time (never retyped).
Run from anywhere:  python -I scripts/author_sheet.py [--sync]
"""
import json
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
PKG = REEL.parents[1]                      # walker-survival-shooting/ (exported copy)
GAME = PKG / "godot"
PUB = "claude-liam-walker-survival-shooting-gamedev"   # folder under runtime/remotion/public
TITLE = "Walker Survival Shooting, Before the Slice"
SLUG = "claude-liam-walker-survival-shooting-gamedev"
SRC = "walker-survival-shooting @ f848d84"


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


def img(name):
    return f"{PUB}/{name}"


BEATS = []

# ── B00 walker cold open ──────────────────────────────────────────────
BEATS.append(beat("B00", "ASK",
    "Hej — this is Liam, in for Bear. On screen is a reconstructed prompt, not a saved session. "
    "It asks Walker to turn a design document about a subway extraction shooter into a Godot asset slice. "
    "The honest answer, at source revision f, eight, four, eight, d, eight, four: the design and the first assets exist. "
    "The playable slice does not, yet.",
    "ClaudeComposerAsk",
    {"greeting": "Hej, Liam", "topic": "GODOT · GAMEDEV · WALKER",
     "segment": "Reconstructed prompt (illustrative, not a saved session)",
     "command": "Please use Walker to convert my game design document about a third-person extraction "
                "shooter, where a survivor lives in a subway base and carries a rugged military tablet, "
                "into a Godot asset slice with generated art, sound and music.",
     "runningText": "reading the submitted revision f848d84…", "modelLabel": "Opus 5.5", "largeText": True,
     "output": ["Reconstruction for this film, not a historical transcript.",
                "Exists: design docs, asset log, 3 sounds, a greybox room.",
                "Not yet: character, sound events, music, mute."]},
    [("0.02", "composer fades in; greeting 'Hej, Liam'"),
     ("0.15", "reconstructed Walker prompt types into the composer"),
     ("0.6", "send arms; running line names revision f848d84"),
     ("0.75", "three answer lines land: reconstruction label, what exists, what does not")],
    role_note="COLD OPEN LAW + walker B00. Prompt labeled as an illustrative reconstruction."))

# ── B01 hesitant writer BLUF ──────────────────────────────────────────
BEATS.append(beat("B01", "BLUF",
    "Walker Survival Shooting is not a finished asset slice. Right now it is a design record and a greybox: "
    "written design, a full asset log, three generated sounds, and one empty subway room. "
    "Here is how each piece got made, and what is missing.",
    "BrutalistHesitantWriter",
    {"text": "This game is\na finished asset slice.", "triggerWords": "a finished asset slice",
     "replacementWords": "a design record and a greybox", "fontSize": 104, "lineSpacing": 1.4,
     "align": "center", "seed": "walker-survival-shooting-f848d84", "mistakeRate": 2,
     "hesitateWithin": 0, "hesitateBetween": 1, "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
    [("0.0", "typing starts during the lead silence"),
     ("0.3", "'a finished asset slice' typed, marked in terracotta"),
     ("0.45", "phrase deleted; 'a design record and a greybox' typed in"),
     ("0.8", "corrected sentence settles")],
    lead_silence_s=0.8,
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer typing bookend: two centred lines typed token by token; mid-beat frames are mostly page by design."},
    role_note="EXECUTIVE-SUMMARY LAW. Correction = the film's actual misconception (finished slice)."))

# ── B02 concept & pillars ─────────────────────────────────────────────
BEATS.append(beat("B02", "CONCEPT",
    "The idea, in plain terms. You live in a subway under a ruined city, and you carry a rugged military tablet. "
    "Each run you go up, fight monsters, loot, and extract. Die, and you lose what you carried. "
    "Three pillars. The tablet is gameplay, and the world never pauses while it is open. "
    "Maps are small but dense. And the best loot is guarded, so extraction is high risk, high reward.",
    "GodotDesignBoard",
    {"title": "The concept and its pillars", "section": "CONCEPT · DESIGN PILLARS",
     "excerpt": "The tablet is gameplay. The tablet's software is gameplay in itself, not just an "
                "information display, and the world keeps going while it is open.",
     "source": f"{SRC} · CONCEPT.md, Design pillars (pillar 1 quoted)",
     "status": "DESIGNED · CONCEPT.md version 1, written 2026-10-03, before any generation",
     "visualLabel": "The three pillars and this assignment's scope, as written in the concept",
     "layout": "cards",
     "cards": [{"label": "1 · The tablet is gameplay", "text": "Its software is play; the world keeps going while it is open."},
               {"label": "2 · Small but complex maps", "text": "Few buildings, each as complex as a factory or a university."},
               {"label": "3 · High-risk, high-reward extraction", "text": "The best loot is guarded; dying loses what you carry."},
               {"label": "This assignment's slice", "text": "Takes place entirely inside the subway base."}]},
    [("0.0", "concept excerpt and pillar cards on screen"), ("0.42", "pillar 1 lights"),
     ("0.62", "pillar 2 lights"), ("0.78", "pillar 3 lights"), ("0.93", "slice scope card lights")],
    cues=[[0.42, 0], [0.62, 1], [0.76, 2], [0.93, 3]]))

# ── B03 storyboard panel 3 ────────────────────────────────────────────
BEATS.append(beat("B03", "STORYBOARD",
    "This is the designer's hand sketch for storyboard panel three, the core action. "
    "A short press of Tab takes the tablet out in one hand, and a small window opens in the corner of the screen "
    "while you keep walking. A long press switches to two hands. "
    "And the panel's sound line asks for one thing: a short startup beep. That beep is the asset I will trace.",
    "GodotDesignFigure",
    {"title": "Storyboard panel 3: the core action",
     "status": "Designer's hand sketch · not playable yet",
     "image": img("03-tablet-onehand.png"), "imageLabel": "design/storyboard/03-tablet-onehand.png",
     "excerpt": "Hear: a startup sound when the tablet is picked up, a short \"beep\" (sound effects focus on the tablet)",
     "source": f"{SRC} · STORYBOARD.md panel 3 · design/storyboard/03-tablet-onehand.png",
     "cards": [{"label": "Short Tab", "text": "Not looking → one hand"},
               {"label": "Small window", "text": "Bottom right, 20–40%"},
               {"label": "Long Tab", "text": "Two hands, lean in"},
               {"label": "Hear", "text": "A short startup beep"}]},
    [("0.0", "sketch of panel 3 fills the frame"), ("0.22", "Short Tab card"), ("0.42", "small window card"),
     ("0.58", "long Tab card"), ("0.75", "Hear card: the startup beep")],
    cues=[[0.2, 0], [0.4, 1], [0.58, 2], [0.74, 3]]))

# ── B04 character sheet ───────────────────────────────────────────────
BEATS.append(beat("B04", "CHARACTER",
    "The character sheet was built the same way. The designer directed ChatGPT image drafts and rejected the wrong ones: "
    "glossy materials, a coat tucked into the skirt, a thigh holster, armor built into the body. "
    "The accepted turnaround keeps a matte coat outside the skirt, a holster hidden at the right waist, and armor as separate gear. "
    "Still missing: the ten pose images, the silhouette test, and the collision overlay.",
    "GodotDesignFigure",
    {"title": "The character reference (CHAR-TURN)",
     "status": "ChatGPT image generation · accepted reference · no 3D model or pose images yet",
     "image": img("turnaround.png"), "imageLabel": "design/character/turnaround.png",
     "excerpt": "The oversized coat hangs outside the skirt and covers most of it; only the lower skirt hem is visible.",
     "source": f"{SRC} · CHANGE-BRIEF.md design change 2 · design/character/turnaround.png · SOURCES.md CHAR-TURN",
     "cards": [{"label": "Rejected", "text": "Gloss, tucked coat, armor"},
               {"label": "Holster", "text": "Right waist, under coat"},
               {"label": "Armor", "text": "Separate modular gear"},
               {"label": "Missing", "text": "10 poses, silhouette"}]},
    [("0.0", "accepted turnaround on screen"), ("0.2", "Rejected card"), ("0.55", "Holster card"),
     ("0.68", "Armor card"), ("0.82", "Missing card")],
    cues=[[0.2, 0], [0.55, 1], [0.68, 2], [0.82, 3]]))

# ── B05 what can / cannot be shown ────────────────────────────────────
BEATS.append(beat("B05", "LIMITS",
    "Now the requirement this film cannot meet. The assignment asks to see the character in two states, "
    "and four sound events firing in real play. None of that exists. There is no character, no sound wired to an event, "
    "no music, and no mute. So you will not see gameplay here. What you will see is real engine output of the greybox, "
    "and the real generated files.",
    "GodotDesignFigure",
    {"title": "What this build can and cannot show", "status": "Status at f848d84 · copied from TEST-REPORT and README",
     "image": img("status_table.png"), "imageLabel": "figures/status_table.png",
     "excerpt": "",
     "source": f"{SRC} · TEST-REPORT.md and README.md (drafts) · table built for this film from their text",
     "cards": [{"label": "Built", "text": "Docs, asset log, greybox"},
               {"label": "Accepted", "text": "3 of 4 terminal sounds"},
               {"label": "Missing", "text": "Character, events, music"},
               {"label": "Shown", "text": "Real renders, files"}]},
    [("0.0", "requirement/status table"), ("0.2", "two-states + four-events rows read as Not built"),
     ("0.45", "Missing card"), ("0.75", "Shown here card")],
    cues=[[0.1, 0], [0.3, 1], [0.48, 2], [0.75, 3]]))

# ── B06 trace: design ─────────────────────────────────────────────────
BEATS.append(beat("B06", "TRACE",
    "The trace starts in the design docs. The concept's audio direction, added on October ninth, says the tablet sounds "
    "are short, dry electronic tones with light radio static and squelch, like rugged field electronics. "
    "The change brief then names the asset, terminal power on, and its exact event: picking up the tablet, "
    "from not looking to one or two hands.",
    "GodotDesignBoard",
    {"title": "Trace 1 · the power-on beep, from design", "section": "SFX-TERMINAL-POWER-ON",
     "excerpt": "Picking up the tablet at any time (from \"not looking\" to one-handed or two-handed)",
     "source": f"{SRC} · CHANGE-BRIEF.md revision 2026-10-09 · CONCEPT.md revision 2026-10-09 · STORYBOARD.md panel 3",
     "status": "DESIGNED before generation · committed in the design docs",
     "visualLabel": "Where the asset is specified, in order", "layout": "flow",
     "cards": [{"label": "Storyboard panel 3", "text": "a short startup \"beep\""},
               {"label": "CONCEPT · audio direction (2026-10-09)", "text": "short, dry electronic tones + light radio static, squelch"},
               {"label": "CHANGE-BRIEF · event map", "text": "Trigger: picking up the tablet"},
               {"label": "SOURCES · asset log", "text": "Prompt A4 · seed 1145141919810 · output 00042"}]},
    [("0.0", "event-map excerpt"), ("0.05", "storyboard card"), ("0.2", "concept audio card"),
     ("0.62", "change-brief event card"), ("0.9", "asset log card")],
    cues=[[0.04, 0], [0.18, 1], [0.6, 2], [0.88, 3]]))

# ── B07 trace: rejected ───────────────────────────────────────────────
BEATS.append(beat("B07", "TRACE",
    "The first attempts failed. Version one asked for two confirmation beeps and a rising activation tone. "
    "The designer heard something too sharp and explosive, like an electronic transient. "
    "Version two rerolled seeds and lengths; none of those satisfied either. So the design changed: one clear beep, "
    "layered with short radio static. One more finding: every run used C F G one, so the negative prompts did nothing.",
    "GodotDesignBoard",
    {"title": "Trace 2 · what was rejected", "section": "Rejected: V01 and V02",
     "excerpt": "two brief digital confirmation beeps followed by a rising electronic activation tone",
     "source": f"{SRC} · SOURCES.md asset log rows SFX-TERMINAL-POWER-ON-V01, -V02 · prompt appendix A1",
     "status": "REJECTED · listened to by the designer · audio has no thumbnails",
     "visualLabel": "Rows from the asset log", "layout": "cards",
     "cards": [{"label": "V01 · outputs 00001–00015", "text": "Rejected: too sharp and explosive, like an electronic transient"},
               {"label": "V02 · outputs 00016–00033", "text": "Rejected: rerolls; none of them satisfied the designer"},
               {"label": "Design change", "text": "One clear single beep, layered with short radio static"},
               {"label": "CFG 1.0 finding", "text": "At CFG 1.0 the negative prompt is not used: it had no effect"}]},
    [("0.0", "prompt A1 line quoted"), ("0.14", "V01 card"), ("0.42", "V02 card"), ("0.6", "design change card"),
     ("0.82", "CFG finding card")],
    cues=[[0.14, 0], [0.42, 1], [0.6, 2], [0.8, 3]]))

# ── B08 trace: accepted raw output ────────────────────────────────────
BEATS.append(beat("B08", "TRACE",
    "Version three is the one that was accepted. The prompt asks for one clear confirmation beep, layered with a brief "
    "filtered radio static burst. With the seed on screen, twelve steps, C F G one, and a two point three second length, "
    "output zero zero zero four two was accepted with no edits. The repository file is a byte-identical copy. "
    "These settings were read back from the metadata Comfy U I embeds in the file itself.",
    "GodotDesignBoard",
    {"title": "Trace 3 · the accepted raw output", "section": "PROMPT A4 · OPENING LINES",
     "excerpt": "short rugged military handheld terminal power-on sound effect,\none clear electronic confirmation beep,\n"
                "distinct single mid-pitched beep around 900 Hz,\nthe beep is layered with a brief filtered radio static burst,",
     "source": f"{SRC} · SOURCES.md SFX-TERMINAL-POWER-ON-V03 · design/sfx_sound/sfx_power_on.flac (embedded ComfyUI workflow)",
     "status": "ACCEPTED · Stable Audio 3 Small SFX (local ComfyUI) · settings read from the FLAC metadata",
     "visualLabel": "Waveform and spectrogram drawn by FFmpeg from design/sfx_sound/sfx_power_on.flac",
     "layout": "image", "image": img("power_on_audio.png"),
     "cards": [{"label": "Settings", "text": "seed 1145141919810 · 12 steps · CFG 1.0 · lcm · 2.3 s"},
               {"label": "Edits", "text": "None · 00042 copied, byte-identical (MD5)"}]},
    [("0.0", "prompt A4 excerpt beside the waveform + spectrogram"), ("0.12", "Model card"),
     ("0.35", "Settings card"), ("0.62", "Edits card")],
    cues=[[0.33, 0], [0.6, 1]]))

# ── B09 listening segment (no narration) ──────────────────────────────
BEATS.append({"beat_id": "B09", "act": "LISTEN", "narration_text": "",
    "role_note": "Clearly labeled listening segment: the three accepted generated sound files, unaltered, "
                 "no narration. NOT in-engine (the sounds are not in the Godot project). audio_file is the "
                 "concatenated sequence; see SOURCES.md.",
    "audio_file": "listen/terminal-sfx-sequence.flac", "audio_policy": "generated-file-listen",
    "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion",
             "show": [{"at": "0.0", "event": "label: generated sound file, not in-engine, no narration"},
                      {"at": "0.08", "event": "card 1 lights as power-on plays (0.8 s)"},
                      {"at": "0.43", "event": "card 2 lights as power-off plays (4.2 s)"},
                      {"at": "0.78", "event": "card 3 lights as button press plays (7.6 s)"}],
             "remotion": {"pattern": "GodotDesignFigure", "props": {
                 "title": "Listen: the accepted terminal sounds",
                 "status": "GENERATED SOUND FILES · NOT IN-ENGINE · NO NARRATION",
                 "image": img("sequence.png"), "imageLabel": "listen/terminal-sfx-sequence.flac",
                 "excerpt": "Three accepted Stable Audio files, played unaltered. No game event triggers them yet.",
                 "source": f"{SRC} · design/sfx_sound/ (sfx_power_on, sfx_power_off, sfx_botton_press) · error sound not final",
                 "cards": [{"label": "1 · Power on", "text": "00042 · from 0.8 s"},
                           {"label": "2 · Power off", "text": "00044 · from 4.2 s"},
                           {"label": "3 · Button press", "text": "00070 · from 7.6 s"},
                           {"label": "Error sound", "text": "Not final · not played"}],
                 "cues": [{"at": 0.8, "card": 0}, {"at": 4.215, "card": 1}, {"at": 7.63, "card": 2}]}}}})

# ── B10 trace: in-engine result = none ────────────────────────────────
BEATS.append(beat("B10", "TRACE",
    "And the last step of the trace: the in-engine result. There is not one yet. This is the saved scene tree of base dot "
    "T S C N. There is no audio player node. The Godot project contains no sound files at all, and project dot godot "
    "defines no input actions, so nothing could trigger the beep. The sounds still sit in the design folder as FLAC files, "
    "not yet converted to Ogg.",
    "GodotDevWorkbench",
    {"mode": "tree", "title": "Trace 4 · in-engine result: not yet", "project": "project_survival_shooting",
     "path": "base.tscn", "source": f"{SRC} · godot/base.tscn (saved scene; node names verbatim, siblings grouped on one line) · godot/project.godot",
     "treeLabel": "Saved scene · base.tscn",
     "tree": ["Base (Node3D)", "  WorldEnvironment", "  room (CSGCombiner3D): floor, 4 walls, ceiling",
              "  stairs (CSGCombiner3D)", "    step_1 … step_6, landing", "    stairs_ramp > CollisionShape3D",
              "  test_chair (test_chair.glb)", "  ceiling_light_1, ceiling_light_2 (OmniLight3D)",
              "  preview_camera (Camera3D)"],
     "inspectorLabel": "Source inspection — not Inspector values",
     "notes": [{"label": "Audio nodes in base.tscn", "value": "0 (no AudioStreamPlayer)"},
               {"label": "Audio files under godot/", "value": "0"},
               {"label": "project.godot", "value": "No input map · no main scene"},
               {"label": "Where the sounds are", "value": "design/sfx_sound/*.flac, outside the project"}],
     "output": ["No scripts, so nothing is created at runtime"]},
    [("0.0", "Godot editor reconstruction: saved scene tree + source notes"), ("0.3", "tree walks root to camera"),
     ("0.45", "note: zero audio nodes"), ("0.6", "note: no input map"), ("0.85", "note: sounds outside the project")],
    cues=[[0.0, 1, "Saved scene root: Base (Node3D)"], [0.3, 6, "stairs_ramp: collision only"], [0.42, 9, "Last node: preview_camera. No AudioStreamPlayer anywhere"], [0.56, 1, "project.godot: no [input] section, no main scene"], [0.72, 7, "test_chair: the only imported asset besides icon.svg"]]))

# ── B11 code: stairs + ramp ───────────────────────────────────────────
STAIR = lines("base.tscn", 69, 81)
BEATS.append(beat("B11", "CODE",
    "The second trace has real engine output: the greybox. The designer built the floor and side walls, then asked Claude "
    "to finish it from basic shapes. Read the last step and the ramp. Each step rises zero point two metres and runs zero "
    "point three. Then a collision box with no mesh, tilted by the matrix entries zero point five five four seven and zero "
    "point eight three two one. That is a thirty-three point seven degree slope: exactly rise over run.",
    "GodotDevWorkbench",
    {"mode": "code", "title": "Trace ENV-BASE-01 · the invisible stair ramp", "project": "project_survival_shooting",
     "path": "base.tscn  ·  lines 69–81", "code": STAIR, "startLine": 69, "codeFontSize": 23,
     "source": f"{SRC} · godot/base.tscn lines 69–81 (and line 13, BoxShape3D size) · built by Claude Code (Claude Opus 5.5)",
     "inspectorLabel": "Source notes — derived from these lines",
     "notes": [{"label": "Step rise / run", "value": "0.2 m / 0.3 m · 6 steps → 1.2 m platform"},
               {"label": "Ramp tilt (line 80)", "value": "atan(0.5547 / 0.8321) = 33.7° = atan(0.2 / 0.3)"},
               {"label": "Ramp length (line 13)", "value": "2.163 = √(1.8² + 1.2²)"},
               {"label": "Why a ramp", "value": "a character body does not step up stairs by default"}],
     "output": ["StaticBody3D + CollisionShape3D, no MeshInstance3D → collides but is never drawn"]},
    [("0.0", "Godot editor reconstruction of base.tscn lines 69–81"), ("0.38", "step_6 transform + size lines highlight"),
     ("0.58", "stairs_ramp StaticBody3D line highlights"), ("0.7", "CollisionShape3D transform line highlights"),
     ("0.88", "shape line highlights; notes show the 33.7° derivation")],
    cues=[[0.36, 70, "step_6 centre y 0.85, height 1.2 → top at 1.45 m"], [0.46, 71, "each step 0.3 m deep; heights grow by 0.2 m"], [0.58, 77, "stairs_ramp: a StaticBody3D with no mesh"], [0.68, 80, "rotation entries 0.8321 / 0.5547 → 33.7°"], [0.9, 81, "shape: BoxShape3D_ramp, 1.5 × 0.1 × 2.163 m (line 13)"]]))

# ── B12 result: stairs render ─────────────────────────────────────────
BEATS.append(beat("B12", "RESULT",
    "Here is what those lines do. On the left, a normal render: you only see steps. On the right, the same frame with "
    "Godot's collision drawing turned on: the invisible ramp lies across every step edge. A raycast check I ran for this "
    "film agrees: the ramp surface meets the first five step edges within a millimetre, and ends at the sixth. "
    "A prediction I have not tested: change the step height alone, and the ramp stops matching.",
    "GodotDesignFigure",
    {"title": "Result · the ramp you cannot see",
     "status": "Native Godot 4.7.2 renders, 3840×2160 · film camera added by capture script · scene unchanged",
     "image": img("stairs_compare.png"), "imageLabel": "figures/stairs_compare.png",
     "excerpt": "Left: normal render. Right: --debug-collisions, debug shape colour set to orange for readability.",
     "source": f"{SRC} · capture/stairs_side.png, capture/stairs_side_collision.png · evidence/ramp-check.log",
     "cards": [{"label": "Normal render", "text": "Steps only; ramp invisible"},
               {"label": "Debug collisions", "text": "Ramp across every edge"},
               {"label": "Raycast (new check)", "text": "Edges 1–5: 0.7 mm · PASS"},
               {"label": "Prediction (untested)", "text": "Step height alone breaks it"}]},
    [("0.0", "normal vs debug-collision renders side by side"), ("0.12", "Normal card"), ("0.3", "Debug card"),
     ("0.55", "Raycast card"), ("0.83", "Prediction card")],
    cues=[[0.1, 0], [0.28, 1], [0.52, 2], [0.82, 3]],
    shot_extra={"evidence_media": "figures/stairs_compare.png"}))

# ── B13 code: lights ──────────────────────────────────────────────────
LIGHTS = lines("base.tscn", 86, 98)
BEATS.append(beat("B13", "CODE",
    "One more cause and effect: the lighting. The concept asks for dark, cool tones. In the scene file, two omni lights hang "
    "at x minus three point five and plus three point five, just under the ceiling, with a pale blue colour, energy one point "
    "five, and an eight metre range. The environment behind them is nearly black, with a weak blue-grey ambient light.",
    "GodotDevWorkbench",
    {"mode": "code", "title": "Lighting the greybox", "project": "project_survival_shooting",
     "path": "base.tscn  ·  lines 86–98", "code": LIGHTS, "startLine": 86, "codeFontSize": 23,
     "source": f"{SRC} · godot/base.tscn lines 86–98 (environment: lines 5–10)",
     "inspectorLabel": "Source notes — derived from these lines",
     "notes": [{"label": "Positions", "value": "x = ±3.5, y = 2.9"},
               {"label": "Colour · energy · range", "value": "pale blue · 1.5 · 8 m"},
               {"label": "Environment (lines 5–10)", "value": "near-black; ambient 0.35"},
               {"label": "CONCEPT", "value": "dark, cool-toned"}],
     "output": ["Two OmniLight3D nodes; no other light sources in the scene"]},
    [("0.0", "Godot editor reconstruction of lines 86–98"), ("0.35", "light_1 transform highlights"),
     ("0.45", "light_2 transform highlights"), ("0.55", "color / energy / range lines highlight"),
     ("0.85", "environment note")],
    cues=[[0.3, 87, "ceiling_light_1 at x = −3.5, y = 2.9"], [0.42, 94, "ceiling_light_2 at x = +3.5, y = 2.9"], [0.55, 88, "pale blue: (0.78, 0.86, 1.0)"], [0.62, 89, "energy 1.5"], [0.7, 91, "range 8 m"]]))

# ── B14 result: room pan (real footage) ───────────────────────────────
BEATS.append({"beat_id": "B14", "act": "RESULT",
    "narration_text": "And the result, rendered by Godot at native four K. A film camera added by my capture script pans "
        "across the room. Nothing in the scene moves, because nothing in it can. You can see the two cool pools of light on "
        "the ceiling, the test chair against the back wall, and the stairs. It is dark and blue-grey, as the concept asked. "
        "Whether a near-black character would read against these walls is still untested.",
    "voice": "am_onyx", "engine": "kokoro", "estimated_duration_s": 24,
    "role_note": "Real native-4K engine footage (capture/room_pan). Label burned in by scripts/prepare_media.py.",
    "qc": {"full_bleed": True,
           "contrast_regions": [{"label": "burned-in disclosure label", "box": [0.02, 0.935, 0.98, 0.995]}],
           "contrast_reason": "Edge-to-edge native Godot render of a dark room; the only essential text is the disclosure label strip, checked locally."},
    "shot": {"type": "SCREEN", "class": "SHOW", "source": "own",
             "evidence_media": "media/B14.mp4",
             "show": [{"at": "0.0", "event": "labeled native 4K Godot render; pan starts at the back-wall chair"},
                      {"at": "0.45", "event": "ceiling light pools pass through frame"},
                      {"at": "0.8", "event": "pan ends on the stairs"}]}})

# ── B15 tests ─────────────────────────────────────────────────────────
BEATS.append(beat("B15", "TESTS",
    "What was tested. A fresh export of the submitted revision imports cleanly, and base dot T S C N runs a hundred and "
    "twenty frames with no errors or warnings. The ramp raycast passes. Re-running a sound with the same prompt and seed "
    "gave identical decoded audio. These are headless machine checks. No human has played anything, because there is "
    "nothing to play, and none of this shows that a sound fires once per event.",
    "GodotDesignFigure",
    {"title": "What was tested",
     "status": "Headless checks · re-run while making this film · not a playtest",
     "image": img("test_log.png"), "imageLabel": "evidence/fresh-run-120.log · evidence/ramp-check.log",
     "excerpt": "Result: both commands exited with code 0. (TEST-REPORT.md, automated check 1)",
     "source": f"{SRC} · TEST-REPORT.md · evidence/*.log recorded 2026-10-09 · SOURCES.md reproducibility check",
     "cards": [{"label": "Fresh copy", "text": "exit 0"},
               {"label": "Warnings", "text": "0"},
               {"label": "Ramp raycast", "text": "PASS"},
               {"label": "Sound repro", "text": "same MD5"}]},
    [("0.0", "recorded command output"), ("0.1", "fresh-copy card"), ("0.25", "errors card"),
     ("0.36", "ramp card"), ("0.48", "sound repro card")],
    cues=[[0.08, 0], [0.24, 1], [0.36, 2], [0.47, 3]]))

# ── B16 models & contributions ────────────────────────────────────────
BEATS.append(beat("B16", "CREDITS",
    "Who made what. ChatGPT image generation made the character turnaround, the extra views and the tablet references. "
    "A local model, ChenkinNoob X L, made early drafts, all rejected. Stable Audio 3 Small made all the sound. "
    "Claude Code built the greybox and the test chair in code. The assignment text says code-drawn art does not meet the "
    "generative model requirement; the professor confirmed to the designer that these basic-shape 3D builds count. "
    "Both are true, so both are on screen.",
    "GodotDesignFigure",
    {"dense": True, "title": "Who made which asset",
     "status": "From SOURCES.md at f848d84 · every accept / reject was the designer's",
     "image": img("models_table.png"), "imageLabel": "figures/models_table.png",
     "excerpt": "Assignment text: code-drawn art does not satisfy the generative-model requirement. "
                "Professor, to the designer: Claude's basic-shape 3D builds count.",
     "source": f"{SRC} · SOURCES.md (Generative models, Human / AI contributions) · README.md",
     "cards": [{"label": "Designer", "text": "all verdicts"},
               {"label": "ChatGPT", "text": "prompt wording"},
               {"label": "Claude", "text": "greybox, log, film"},
               {"label": "Stated", "text": "rule vs ruling"}]},
    [("0.0", "model → asset table"), ("0.1", "designer card"), ("0.35", "ChatGPT card"),
     ("0.55", "Claude Code card"), ("0.75", "rule vs ruling card")],
    cues=[[0.05, 0], [0.12, 1], [0.5, 2], [0.72, 3]]))

# ── B17 uncertain + next ──────────────────────────────────────────────
BEATS.append(beat("B17", "NEXT",
    "What is still uncertain. The error sound keeps coming out with tremolo and repeated tones, and the designer does not yet "
    "know how to get one clean tone. Nobody knows whether the dark outfit reads against this room. And the once-per-event "
    "logic is not written. The next concrete step: convert the three sounds to Ogg, add an audio player, and fire power on "
    "when the tablet's state changes, with a log that proves one trigger per press.",
    "GodotDesignBoard",
    {"title": "Uncertain, and the next step", "section": "KNOWN LIMITATION",
     "excerpt": "The error sound still has repeated or tremolo-like tones; I do not yet know how to get one clean tone from the model.",
     "source": f"{SRC} · TEST-REPORT.md · CHANGE-BRIEF.md predicted failures 2 and 3 · FRICTIONAL.md 2026-10-09 next step",
     "status": "Source revision shown in this film: f848d84",
     "visualLabel": "Open questions, then one bounded next step", "layout": "cards",
     "cards": [{"label": "Uncertain", "text": "Error sound: tremolo and repeated tones"},
               {"label": "Untested (prediction 2)", "text": "Does the near-black character read against the base?"},
               {"label": "Not written", "text": "One input → exactly one sound (prediction 3)"},
               {"label": "Next step", "text": "OGG → AudioStreamPlayer → fire on tablet state change; log the count"}]},
    [("0.0", "TEST-REPORT limitation quoted"), ("0.05", "Uncertain card"), ("0.33", "prediction 2 card"),
     ("0.45", "not-written card"), ("0.62", "Next step card")],
    cues=[[0.04, 0], [0.32, 1], [0.44, 2], [0.6, 3]]))

# ── B18 verdict ───────────────────────────────────────────────────────
BEATS.append(beat("B18", "VERDICT",
    "Verdict. What is real: a careful design record, a reproducible asset log, three accepted sounds, and a greybox whose "
    "stair ramp demonstrably lines up. What is missing is the slice itself: no character, no events, no music, no mute, "
    "so this film cannot show play. The judgment, every accept, reject and redesign, was the designer's. "
    "The models produced drafts; Claude built shapes and kept the records.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Verdict", "artifactHeading": "Walker Survival Shooting at f848d84.", "brandLabel": "@NikBearBrown",
     "artifactLines": ["Built: design docs, asset log, 3 accepted sounds, a greybox.",
                       "Traced: beep from design to 00042; not in the engine yet.",
                       "Missing: character, sound events, music, mute.",
                       "Human: every accept, reject and redesign."]},
    [("0.0", "verdict artifact page"), ("0.15", "Built line"), ("0.4", "Traced line"), ("0.55", "Missing line"),
     ("0.8", "Human line")]))

# ── B19 your turn ─────────────────────────────────────────────────────
YT = ("Please use Walker on my Godot project. Read my CHANGE-BRIEF event-to-sound map and base.tscn. Pick one sound "
      "event and write the smallest change that plays it on that event, plus a test that logs how many times it fired "
      "for one short press, one long press and a held key. Predict the counts before you run it.")
BEATS.append(beat("B19", "HANDOFF",
    "Your turn. Paste this into Claude. " + YT.replace("base.tscn", "base dot T S C N").replace("CHANGE-BRIEF", "change brief") +
    " The prediction is the point: write down the counts first, so the log can prove you wrong. "
    "Start with one sound, not four. Liam, in for Bear.",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "GODOT · GAMEDEV · WALKER", "segment": "Walker Survival Shooting",
     "command": YT, "runningText": "paste this into Claude…", "output": [],
     "modelLabel": "Opus 5.5", "largeText": True},
    [("0.02", "composer with greeting 'Your turn.'"), ("0.1", "prompt types in"), ("0.7", "send arms"),
     ("0.9", "Liam signs off")],
    role_note="HANDOFF LAW: prompt read aloud verbatim, then discussed; Liam signs off here."))

# ── B20 locked outro ──────────────────────────────────────────────────
BEATS.append({"beat_id": "B20", "act": "OUTRO", "kind": "outro_voice",
    "narration_text": f"{TITLE}. At Nik Bear Brown.", "voice": "am_onyx", "engine": "kokoro",
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
    "channel": "@NikBearBrown", "folderLabel": "@NikBearBrown", "persona": "Liam (in for Bear)", "in_for_bear": True,
    "greeting": "Hej, Liam", "greeting_note": "hello lexicon: Hej (Swedish); Assignment 1 used Ciao.",
    "game": {"name": "walker-survival-shooting", "source_revision": "f848d84",
             "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
             "game_path": "walker-survival-shooting/godot (exported from f848d84)"},
    "note": "godot-gamedev walker film. No playable slice exists at f848d84: no character, no sound events, no "
            "music, no mute. Engine footage is native-4K renders of the unmodified base.tscn through a capture "
            "script that only adds a film camera. The listening beat B09 plays the generated sound files, labeled "
            "not in-engine. No game change, no commit, no push, no publication.",
}


def write(sheet):
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=True) + "\n", encoding="ascii")


def sync():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    for b in sheet["beats"]:
        if b["beat_id"] == "B09":
            b["actual_duration_s"] = 9.744308   # listen/terminal-sfx-sequence.flac, measured
            b["shot"]["remotion"]["props"]["durationSeconds"] = 9.744308
            continue
        d = b.get("actual_duration_s")
        rem = (b.get("shot") or {}).get("remotion")
        if not d or not rem:
            continue
        props = rem["props"]
        props["durationSeconds"] = round(d, 6)
        fr = b["shot"].get("cue_fracs")
        if fr:
            key = "line" if rem["pattern"] == "GodotDevWorkbench" else "card"
            if key == "line":
                props["cues"] = [{"at": round(f[0] * d, 3), "line": f[1], "label": f[2]} for f in fr]
            else:
                props["cues"] = [{"at": round(f * d, 3), "card": c} for f, c in fr]
    write(sheet)


def rebuild():
    """Re-author from this script but keep measured audio/render fields from the live sheet."""
    old = {b["beat_id"]: b for b in json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))["beats"]}
    for b in BEATS:
        o = old.get(b["beat_id"], {})
        for k in ("actual_duration_s", "audio_file", "render_duration_s", "build"):
            if k in o:
                b[k] = o[k]
        r = ((o.get("shot") or {}).get("remotion") or {}).get("rendered")
        if r and b.get("shot", {}).get("remotion"):
            b["shot"]["remotion"]["rendered"] = r
    write({"metadata": METADATA, "beats": BEATS})
    sync()


if __name__ == "__main__":
    if "--rebuild" in sys.argv:
        rebuild()
    elif "--sync" in sys.argv:
        sync()
    else:
        write({"metadata": METADATA, "beats": BEATS})
    print("beat_sheet.json written")
