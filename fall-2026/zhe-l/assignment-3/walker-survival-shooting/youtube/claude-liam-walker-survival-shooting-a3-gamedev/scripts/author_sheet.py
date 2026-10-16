"""Author beat_sheet.json for the walker-survival-shooting Assignment 3 gamedev film.

Pass 1 (no args): narration, shots and props with placeholder durations.
Pass 2 (--sync): after Kokoro has measured audio, converts each beat's cue
fractions into seconds and sets durationSeconds from the measured duration.
--rebuild: re-author from this script but keep measured audio/render fields.
All code excerpt text is read from the exported game copy at run time (never retyped).
Run:  python -I scripts/author_sheet.py [--sync | --rebuild]
"""
import json
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
PKG = REEL.parents[1]                      # walker-survival-shooting/ (exported copy of b370626)
GAME = PKG / "godot"
PUB = "claude-liam-walker-survival-shooting-a3-gamedev"   # folder under runtime/remotion/public
TITLE = "Walker Survival Shooting: First Props in Blender"
SLUG = "claude-liam-walker-survival-shooting-a3-gamedev"
REV = "b370626"
SRC = f"walker-survival-shooting @ {REV}"
REV_SPOKEN = "b, three, seven, oh, six, two, six"
PROJECT = "project_survival_shooting"
LOOK = "viewport capture by Claude through the MCP look tool"


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


def figure(bid, act, narration, title, status, image, image_label, excerpt, source, cards, show, cues, **extra):
    props = {"title": title, "status": status, "image": img(image), "imageLabel": image_label,
             "excerpt": excerpt, "source": source, "cards": cards}
    return beat(bid, act, narration, "GodotDesignFigure", props, show, cues, **extra)


def board(bid, act, narration, title, section, excerpt_label, excerpt, source, status, visual_label, cards, show,
          cues, layout="cards", **extra):
    props = {"title": title, "section": section, "excerptLabel": excerpt_label, "excerpt": excerpt,
             "source": source, "status": status, "visualLabel": visual_label, "layout": layout, "cards": cards}
    return beat(bid, act, narration, "GodotDesignBoard", props, show, cues, **extra)


def workbench(bid, narration, title, path, start, end, source, notes, output, show, cues, **extra):
    props = {"mode": "code", "title": title, "project": PROJECT,
             "path": f"{path}  ·  lines {start}–{end}", "code": lines(path, start, end),
             "startLine": start, "codeFontSize": 23, "source": source,
             "inspectorLabel": "Source notes — derived from these lines", "notes": notes, "output": output}
    return beat(bid, "CODE", narration, "GodotDevWorkbench", props, show, cues, **extra)


BEATS = []

# -- B00 walker cold open ------------------------------------------------------------------
BEATS.append(beat("B00", "ASK",
    "Hola, this is Liam, in for Bear. The prompt on screen is a reconstruction for this film, not a saved session. "
    "It asks Walker to turn the design document for a subway extraction shooter into its first 3D props. "
    f"At source revision {REV_SPOKEN}, the answer is three assets, in Blender and in a Godot scene, and a check script.",
    "ClaudeComposerAsk",
    {"greeting": "Hola, Liam", "topic": "GODOT · GAMEDEV · WALKER",
     "segment": "Reconstructed prompt (illustrative, not a saved session)",
     "command": "Please use Walker to convert my game design document about a third-person extraction shooter, "
                "where a survivor lives in a subway base and carries a rugged military tablet, into its first 3D "
                "props: a start-menu chair, the tablet and weapon crates, built in Blender through the MCP and "
                "checked in Godot.",
     "runningText": f"reading the submitted revision {REV}…", "modelLabel": "Opus 5.5", "largeText": True,
     "output": ["Reconstruction for this film, not a historical transcript.",
                "Built: chair, tablet, 2 weapon crates (+ 2 desks).",
                f"Checked: 55 headless PASS, 0 FAIL at {REV}."]},
    [("0.02", "composer fades in; greeting 'Hola, Liam'"),
     ("0.15", "reconstructed Walker prompt types into the composer"),
     ("0.6", "send arms; running line names revision b370626"),
     ("0.75", "three answer lines land: reconstruction label, what was built, the headless result")],
    role_note="COLD OPEN LAW + walker B00. Prompt labeled as an illustrative reconstruction."))

# -- B01 hesitant writer BLUF -------------------------------------------------------------
BEATS.append(beat("B01", "BLUF",
    "I directed and Claude built my game's first 3D props. Claude wrote the Blender code; I made the decisions "
    "and one edit by hand. The checks prove the sizes, not the looks.",
    "BrutalistHesitantWriter",
    {"text": "Claude made my game's\nfirst 3D props.", "triggerWords": "Claude made",
     "replacementWords": "I directed and Claude built", "fontSize": 104, "lineSpacing": 1.4,
     "align": "center", "seed": "walker-survival-shooting-b370626", "mistakeRate": 2,
     "hesitateWithin": 0, "hesitateBetween": 1, "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
    [("0.0", "typing starts during the lead silence"),
     ("0.3", "'Claude made' typed, marked in terracotta"),
     ("0.45", "phrase deleted; 'I directed and Claude built' typed in"),
     ("0.8", "corrected sentence settles")],
    lead_silence_s=0.8,
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer typing bookend: centred lines typed token by token; mid-beat frames are mostly page by design."},
    role_note="EXECUTIVE-SUMMARY LAW. Correction = the film's actual misconception (the AI made the assets alone)."))

# -- B02 the game and the three assets ----------------------------------------------------
BEATS.append(board("B02", "CONCEPT",
    "The game first. You live in a subway base, carry a rugged military tablet, go out to fight monsters, and "
    "extract. This assignment needed three props for that base. A chair for the character to sit on in the start "
    "menu. The tablet itself, the core of play. And weapon crates: furniture the player will build to store items. "
    "Every footprint sits on a grid, where one cell is ten centimetres.",
    "The game, and why it needs these three", "README · GAME PREMISE",
    "README · SUBMITTED TEXT",
    "The player lives in a subway base, carries a rugged military tablet, goes out to fight monsters, and extracts.",
    f"{SRC} · README.md · CHANGE-BRIEF.md revision 2026-10-15 (asset table)",
    "THE THREE ASSIGNMENT ASSETS · from the brief's 'What it is in the game' row",
    "Each asset and its job in the game",
    [{"label": "Chair · ENV-SEAT", "text": "Where the character sits in the start menu"},
     {"label": "Tablet · PROP-TABLET", "text": "Carried in the hands; core gameplay"},
     {"label": "Weapon crates · large + small", "text": "Buildable storage furniture; open / close animations"},
     {"label": "Furniture grid", "text": "1 cell = 0.1 m; footprints are whole cells"}],
    [("0.0", "README excerpt and four asset cards"), ("0.3", "chair card"), ("0.45", "tablet card"),
     ("0.6", "crates card"), ("0.85", "grid card")],
    [[0.3, 0], [0.45, 1], [0.58, 2], [0.84, 3]]))

# -- B03 routes and order -----------------------------------------------------------------
BEATS.append(board("B03", "ROUTE",
    "How they were made. Most of it went through the Blender MCP: Claude Code ran Python inside my open Blender, "
    "and looked at the viewport to check. Three later steps ran as headless scripts instead. And one honest detail: "
    "the brief was written after the chair and the tablet existed, so some of its numbers are measurements, "
    "not predictions.",
    "Two routes into Blender, and the real order", "CHANGE-BRIEF · order, recorded honestly",
    "CHANGE-BRIEF · 2026-10-15 REVISION",
    "This brief was written on 2026-10-15. … So this brief is not a prediction written before any modelling, "
    "and some numbers below are measured values.",
    f"{SRC} · CHANGE-BRIEF.md (2026-10-15 entry) · SOURCES.md asset log · tools/blender/build_*.py headers",
    "ROUTES PER SOURCES.md · MCP for Blender add-on 1.8 · Blender 5.2.2",
    "Which step used which route",
    [{"label": "Blender MCP (live, in my window)", "text": "Chair v1, tablet, crates v1–v2, both desks"},
     {"label": "Script route (headless Blender)", "text": "Chair v2, large crate v3, duplicate latch removed"},
     {"label": "Me", "text": "Every decision, every accept, and the hand edit"},
     {"label": "Order", "text": "Chair 10-07 → tablet 10-12 → brief + crates 10-15"}],
    [("0.0", "brief excerpt and route flow"), ("0.08", "MCP card"), ("0.42", "script-route card"),
     ("0.55", "me card"), ("0.65", "order card")],
    [[0.06, 0], [0.4, 1], [0.52, 3]], layout="flow"))

# -- B04 prompt -> what Claude built --------------------------------------------------------
BEATS.append(figure("B04", "PROMPT",
    "Here is a real prompt, translated from my Chinese. Make me a tablet from the reference images. Block it out "
    "with cubes; a greybox is enough. And here is what Claude built: twenty-one bevelled boxes, eight hundred and "
    "four triangles. That is not a greybox. It is the first thing Claude got wrong: it built more than I asked for.",
    "A prompt to Claude, and what it built",
    "MY PROMPT, TRANSLATED FROM CHINESE · Blender MCP · 2026-10-12",
    "tablet_prompt.png", "figures/tablet_prompt.png",
    "", f"{SRC} · SOURCES.md PROP-TABLET-01 · tools/blender/build_tablet.py call 1 · image: {LOOK}",
    [{"label": "Asked for", "text": "A greybox from cubes"},
     {"label": "Got", "text": "21 bevelled boxes"},
     {"label": "Triangles", "text": "804 (budget 500)"},
     {"label": "Verdict", "text": "Overbuilt"}],
    [("0.0", "my translated prompt beside the grey tablet capture"), ("0.18", "Asked-for card"),
     ("0.5", "Got card"), ("0.62", "triangle card"), ("0.82", "Overbuilt card")],
    [[0.15, 0], [0.5, 1], [0.62, 2], [0.8, 3]]))

# -- B05 tablet: colour, triangles, kept over the shape limit -------------------------------
BEATS.append(figure("B05", "REVISE",
    "I kept the shape, but front and back were hard to tell apart, so I asked for a dark green and black shell "
    "with one large black screen. Claude rebuilt it with three materials. Then the course limit bit: five hundred "
    "triangles. Keeping bevels only on the body and the four corner bumpers brought it to three hundred and "
    "eighty-eight. It is still twenty-one shapes, over the limit of six. I decided to keep it.",
    "The tablet: my colours, then the triangle cut",
    "Blender MCP · 2026-10-12 and 2026-10-15 · accepted by me",
    "tablet_versions.png", "figures/tablet_versions.png",
    "", f"{SRC} · SOURCES.md PROP-TABLET-01, PROP-TABLET-02 · TEST-REPORT.md §5, §8.1 · images: {LOOK}",
    [{"label": "My request", "text": "Green / black, black screen"},
     {"label": "Triangles", "text": "804 → 388"},
     {"label": "Shapes", "text": "21 (limit 6)"},
     {"label": "My decision", "text": "Keep it as it is"}],
    [("0.0", "my second prompt beside the green/black and 388-triangle captures"), ("0.1", "request card"),
     ("0.45", "triangle card"), ("0.75", "shape card"), ("0.9", "decision card")],
    [[0.08, 0], [0.42, 1], [0.76, 2], [0.9, 3]]))

# -- B06 chair -----------------------------------------------------------------------------
BEATS.append(figure("B06", "REVISE",
    "The chair went the other way. Version one was nine boxes, with stretchers and two backrest slats. To meet the "
    "six-shape limit, I asked Claude to change it: the stretchers went, and the slats merged into one board. Same "
    "size, seventy-two triangles. That rebuild ran as a headless script, so there is no viewport capture of it. "
    "On the right is the chair in Godot.",
    "The chair: nine boxes cut to six",
    "v1 Blender MCP · v2 script route · accepted by me as the start-menu seat",
    "chair.png", "figures/chair.png",
    "", f"{SRC} · SOURCES.md ENV-SEAT-TEST-01, ENV-SEAT-02 · build_chair.py calls 1–5 · left: {LOOK} · right: native Godot render crop",
    [{"label": "v1", "text": "9 boxes · 108 triangles"},
     {"label": "Cut", "text": "No stretchers; one backrest"},
     {"label": "v2", "text": "6 shapes · 72 triangles"},
     {"label": "Size", "text": "0.44 × 0.42 × 0.90 m"}],
    [("0.0", "v1 capture beside the v2 Godot crop"), ("0.1", "v1 card"), ("0.3", "cut card"),
     ("0.5", "v2 card"), ("0.82", "right panel: chair in Godot")],
    [[0.08, 0], [0.3, 1], [0.5, 2], [0.62, 3]]))

# -- B07 crates and the grid ---------------------------------------------------------------
BEATS.append(figure("B07", "REVISE",
    "The crates taught me the grid. I asked for one cube and one crate twice as long, in military green. The first "
    "version's handles stuck out, so the small crate covered zero point five six by zero point five one five metres, "
    "off any clean grid. I set the rule, one cell is zero point one, and Claude moved the hardware inside the "
    "footprint. Now it is exactly five by five cells.",
    "The crates: a footprint that fits the grid",
    "Blender MCP · 2026-10-15 · my grid rule: 1 cell = 0.1 m",
    "crates.png", "figures/crates.png",
    "build_crate_cube.py lines 150–151: BW = L - 2*HANDLE  # body length without handles  ·  "
    "BD = Wd - LATCH  # body width without latches",
    f"{SRC} · tools/blender/build_crate_cube.py call 2 (lines 150–151, spacing compressed) · SOURCES.md CRATE-CUBE-01/02, CRATE-LONG-02 · images: {LOOK}",
    [{"label": "v1 small crate", "text": "0.56 × 0.515 m"},
     {"label": "My rule", "text": "1 cell = 0.1 m"},
     {"label": "v2 small crate", "text": "0.5 × 0.5 m = 5 × 5"},
     {"label": "v2 large crate", "text": "1.0 × 0.5 m = 10 × 5"}],
    [("0.0", "my grid prompt beside the v1 and v2 crate captures"), ("0.3", "v1 footprint card"),
     ("0.6", "rule card"), ("0.85", "v2 cards")],
    [[0.28, 0], [0.6, 1], [0.85, 2], [0.93, 3]]))

# -- B08 my hand edit (my own screenshot) ----------------------------------------------------
BEATS.append(figure("B08", "HAND EDIT",
    "And this is my own screenshot, from my Blender in Simplified Chinese. Edit Mode, the small crate, one latch "
    "selected; the sidebar shows its median point. My edit: I raised both latches so each sits half on the lid and "
    "half on the body, so it reads as a latch that locks the lid. And I moved the handles up, so the centre of "
    "gravity is lower when it is carried.",
    "My hand edit in Blender",
    "MY OWN SCREENSHOT · Blender 5.2.2, Simplified Chinese interface · title bar cropped",
    "my_screenshot.png", "design/blender-notes/blender-session-01.png",
    "", f"{SRC} · design/blender-notes/blender-session-01.png (title bar cropped) · BLENDER-NOTES.md · SOURCES.md CRATE-CUBE-02",
    [{"label": "Mode", "text": "Edit Mode (Chinese interface)"},
     {"label": "Selected", "text": "One latch of the small crate"},
     {"label": "Median point", "text": "x −0.123 · y −0.2425 · z 0.42553"},
     {"label": "Why", "text": "Latch on the seam; handles higher"}],
    [("0.0", "my own Blender screenshot, Chinese interface"), ("0.16", "mode card"), ("0.25", "selected card"),
     ("0.36", "median point card"), ("0.5", "why card: latch on the seam, handles higher")],
    [[0.15, 0], [0.22, 1], [0.34, 2], [0.5, 3]]))

# -- B09 the latch: inspect and revise -----------------------------------------------------
BEATS.append(figure("B09", "CHECK",
    "Then the checking. Claude measured my edit: the right latch had been stretched ten centimetres deep, into the "
    "box. I fixed it and told Claude not to measure again, and Claude wrote fixed into the records. It was not: the "
    "fix never reached the saved file. My second fix, a copy of the left latch, worked, and a hidden duplicate was "
    "deleted. Six millimetres of asymmetry remain, and I kept them.",
    "Inspect, revise, and inspect again",
    "Native Godot 4.7.2 render of the current small crate · film camera added by capture script",
    "godot_latch.png", "figures/godot_latch.png",
    "I said it was fixed, but my first fix never reached the saved files.",
    f"{SRC} · TEST-REPORT.md §8.4 and §9.5 · SOURCES.md CRATE-CUBE-02 · build_crate_cube.py call 3",
    [{"label": "Measured", "text": "Right latch 0.10 m deep"},
     {"label": "Fix 1", "text": "Never saved"},
     {"label": "Fix 2", "text": "0.015 m deep, both sides"},
     {"label": "Kept", "text": "Right latch 6 mm off"}],
    [("0.0", "Godot render of the small crate front, latches on the seam"), ("0.08", "measured card"),
     ("0.4", "fix 1 card"), ("0.62", "fix 2 card"), ("0.88", "kept card")],
    [[0.06, 0], [0.38, 1], [0.6, 2], [0.86, 3]]))

# -- B10 code: base.tscn placement -> B11 result ---------------------------------------------
BEATS.append(workbench("B10",
    "Into Godot. This is my scene file, base dot T S C N. Each asset is one instance of its imported G L B, placed "
    "with a transform. The chair, the two crates, and the tablet. There is no scaling: ones on the diagonal. The y "
    "value, zero point two five, is the top of the floor slab. The tablet's row holds a tilt, because I lifted and "
    "tilted it to see it better.",
    "Placing the assets in base.tscn", "base.tscn", 137, 147,
    f"{SRC} · godot/base.tscn lines 137–147 (desks: lines 149–153)",
    [{"label": "Instances", "value": "chair.glb, crate_long.glb, crate_cube.glb, tablet.glb"},
     {"label": "Scale", "value": "1, 1, 1 on every node"},
     {"label": "y = 0.25", "value": "top of the 0.5 m floor slab"}],
    ["Saved scene; these are the file's lines, not Inspector values"],
    [("0.0", "Godot editor reconstruction of base.tscn lines 137–147"), ("0.25", "chair instance line"),
     ("0.45", "transform lines: identity basis"), ("0.6", "y = 0.25"), ("0.85", "tablet transform with tilt")],
    [[0.2, 137, "chair: an instance of chair.glb"], [0.32, 140, "crate_long and crate_cube"],
     [0.45, 138, "basis 1,0,0 / 0,1,0 / 0,0,1: no scale"], [0.58, 144, "y = 0.25: top of the floor"],
     [0.8, 147, "tablet: tilted, lifted to y 0.664"]]))

BEATS.append(figure("B11", "RESULT",
    "And here is what those lines produce, rendered by Godot at native four K through my asset camera. The chair, "
    "the tablet floating beside the large crate, and the small crate. They read as what they are at a "
    "glance, but that was my check, not the script's. The light is cool and dim; I moved one light myself so the "
    "assets could be seen.",
    "Result · the assets in the subway base",
    "Native Godot 4.7.2 render, 3840×2160 · the scene's own a3_asset_camera · scene unchanged",
    "godot_asset_cam.png", "figures/godot_asset_cam.png",
    "", f"{SRC} · capture/stills/asset_cam.png (cropped to the figure frame) · capture/capture_driver.gd",
    [{"label": "Camera", "text": "a3_asset_camera (in the scene)"},
     {"label": "In frame", "text": "Chair, tablet, 2 crates"},
     {"label": "Human check", "text": "Recognisable at a glance"},
     {"label": "Lights", "text": "One moved by me"}],
    [("0.0", "native 4K render through a3_asset_camera"), ("0.12", "camera card"), ("0.3", "in-frame card"),
     ("0.5", "human-check card"), ("0.82", "lights card")],
    [[0.1, 0], [0.25, 1], [0.48, 2], [0.8, 3]],
    shot_extra={"evidence_media": "figures/godot_asset_cam.png"}))

# -- B12 code: the brief inside the check -> B13 result ------------------------------------------
BEATS.append(workbench("B12",
    "Now the check script, which Claude wrote. It compares every imported asset with my brief. This table is the "
    "contract: a file, an expected size in metres, the expected lowest point, and a triangle budget of five hundred. "
    "Notice the tablet: its lowest point is minus zero point zero eight one, because I kept its origin in the centre "
    "on purpose, so it can be attached to a hand later.",
    "The brief, written into the check", "tests/a3_asset_check.gd", 15, 21,
    f"{SRC} · godot/tests/a3_asset_check.gd lines 15–21 (tolerance: line 12, 0.002 m; header comment: line 14)",
    [{"label": "Size", "value": "Vector3 in Godot order: x, y (height), z"},
     {"label": "Tolerance", "value": "0.002 m (line 12)"},
     {"label": "Tablet lowest y", "value": "−0.081: origin kept in the centre"}],
    ["Run: godot --headless --path godot --script res://tests/a3_asset_check.gd"],
    [("0.0", "Godot editor reconstruction of the ASSETS table"), ("0.2", "chair row"),
     ("0.45", "triangle budget"), ("0.62", "tablet row"), ("0.82", "tablet lowest y")],
    [[0.15, 15, "one row per asset: name, file, size, lowest y, budget"], [0.3, 16, "chair: 0.44 × 0.90 × 0.42"],
     [0.48, 16, "budget: 500 triangles"], [0.62, 17, "tablet: lowest y −0.081"]]))

BEATS.append(figure("B13", "RESULT",
    "Here is the headless output beside the brief. Godot is y up, so the height moves to the middle number, but "
    "every size matches within two millimetres. The small crate is off by six thousandths of a millimetre. "
    "Triangles: seventy-two, three hundred and eighty-eight, and eighty-eight each. This is recorded output from a "
    "fresh export of the submitted revision, not a number typed in by hand.",
    "Result · brief beside the headless numbers",
    "HEADLESS · Godot 4.7.2 --headless · re-run for this film on a fresh export of b370626",
    "brief_vs_headless.png", "figures/brief_vs_headless.png",
    "", f"{SRC} · evidence/a3-check.log (Part 1 summary lines) · CHANGE-BRIEF.md asset table",
    [{"label": "Sizes", "text": "All within 0.002 m"},
     {"label": "Small crate", "text": "0.500006 (6 µm)"},
     {"label": "Triangles", "text": "72 · 388 · 88 · 88"},
     {"label": "Exit code", "text": "0 (55 PASS)"}],
    [("0.0", "brief column beside the headless column"), ("0.12", "Y-up note"), ("0.35", "sizes card"),
     ("0.5", "small crate card"), ("0.68", "triangle card"), ("0.88", "exit code card")],
    [[0.3, 0], [0.48, 1], [0.66, 2], [0.86, 3]],
    shot_extra={"evidence_media": "figures/brief_vs_headless.png"}))

# -- B14 code: crate animation check -> B15 result (real clip) ----------------------------------
BEATS.append(workbench("B14",
    "The crates have to open. These lines find each crate's animation player, play open, jump to its last frame, "
    "and read the lid's rotation. It must be minus one hundred degrees. Then close, and it must be back at zero. "
    "The lid's origin sits on the back hinge, so it swings about the x axis.",
    "Checking the crate animations", "tests/a3_asset_check.gd", 89, 97,
    f"{SRC} · godot/tests/a3_asset_check.gd lines 89–97",
    [{"label": "Animations", "value": "open and close, from the .glb"},
     {"label": "Seek", "value": "to the last frame, then read the lid"},
     {"label": "Expected", "value": "open → −100°, close → 0°"}],
    ["Log: open → −100.00° · close → 0°"],
    [("0.0", "Godot editor reconstruction of lines 89–97"), ("0.25", "has_animation line"),
     ("0.45", "play open + seek"), ("0.6", "−100 check"), ("0.8", "close and 0 check")],
    [[0.18, 91, "both animations must exist"], [0.35, 94, "play open, seek to the end"],
     [0.52, 95, "the lid must read −100°"], [0.7, 97, "after close: 0°"]]))

BEATS.append({"beat_id": "B15", "act": "RESULT",
    "narration_text": "This is the same animation in the scene, rendered at four K. My capture script plays each "
        "crate's own imported open animation, then close; nothing else moves. Fifteen frames each, a little over half "
        "a second. The headless check only proves the end angles. The test report adds what it misses: the open lid "
        "swings about eight centimetres behind the footprint, so against a wall it would pass through.",
    "voice": "am_onyx", "engine": "kokoro", "estimated_duration_s": 24,
    "role_note": "Real native-4K engine footage (capture/crates_open). Label burned in by scripts/prepare_media.py.",
    "qc": {"full_bleed": True,
           "contrast_regions": [{"label": "burned-in disclosure label", "box": [0.02, 0.935, 0.98, 0.995]}],
           "contrast_reason": "Edge-to-edge native Godot render; the only essential text is the disclosure label strip, checked locally."},
    "shot": {"type": "SCREEN", "class": "SHOW", "source": "own", "evidence_media": "media/B15.mp4",
             "show": [{"at": "0.0", "event": "labeled native 4K Godot render; both crates closed"},
                      {"at": "0.3", "event": "both lids swing open about the back hinge"},
                      {"at": "0.65", "event": "both lids close again"}]}})

# -- B16 code: placement checks -> B17 result -------------------------------------------------
BEATS.append(workbench("B16",
    "Placement checks. The floor top is read from the floor node itself, not from an asset. Every floor item must "
    "rest on it, and every crate and desk needs footprint edges on the ten-centimetre grid. The chair is not "
    "grid-checked, because it is zero point four four by zero point four two. And this comment is history: the "
    "tablet used to be checked against the crate lid.",
    "Checking placement in the scene", "tests/a3_asset_check.gd", 112, 122,
    f"{SRC} · godot/tests/a3_asset_check.gd lines 112–122 (floor top: line 104; tablet check: line 123; overlaps: lines 124–129)",
    [{"label": "Floor top", "value": "from room/floor (line 104)"},
     {"label": "Grid", "value": "edges × 10 must be whole numbers"},
     {"label": "Not grid-checked", "value": "chair: 0.44 × 0.42 m"}],
    ["Part 2 of the same headless run"],
    [("0.0", "Godot editor reconstruction of lines 112–122"), ("0.25", "floor check"),
     ("0.45", "grid check"), ("0.85", "tablet comment")],
    [[0.2, 113, "rests on the floor top"], [0.38, 118, "edge × 10 must round to a whole number"],
     [0.62, 114, "GRID_ITEMS: crates and desks only"], [0.82, 120, "the tablet used to lie on the lid"]]))

BEATS.append(figure("B17", "RESULT",
    "The result: every bottom at zero point two five, every grid edge clean, no overlaps. Fifty-five passes, zero "
    "failures, exit code zero. An earlier run failed: after I lifted the tablet into the air, the lid check broke. "
    "The check changed because the placement changed, and the failing log is kept in the repository.",
    "Result · on the floor, on the grid, apart",
    "HEADLESS · Part 2 log, abridged (x, z positions omitted) · recorded output",
    "log_part2.png", "figures/log_part2.png",
    "", f"{SRC} · evidence/a3-check.log Part 2 · test-logs/a3_check_2026-10-15_v1_tablet-moved.log (exit 1)",
    [{"label": "Bottoms", "text": "All at y = 0.250"},
     {"label": "Grid", "text": "4 of 4 on 0.1 m"},
     {"label": "Total", "text": "55 PASS · 0 FAIL"},
     {"label": "Earlier run", "text": "1 FAIL, log kept"}],
    [("0.0", "Part 2 log beside a render of the same placements"), ("0.1", "bottoms card"),
     ("0.22", "grid card"), ("0.35", "total card"), ("0.6", "earlier failing run card")],
    [[0.08, 0], [0.18, 1], [0.3, 2], [0.5, 3]],
    shot_extra={"evidence_media": "figures/log_part2.png"}))

# -- B18 what the check cannot show; my human check ------------------------------------------------
BEATS.append(figure("B18", "LIMITS",
    "What the script cannot show: whether an asset looks right, reads as what it is, or suits the style. That was "
    "my own look. I recognised all of them at a glance, looked from behind and below, and found no missing faces. "
    "What I cannot confirm yet is the scale against a person, because there is no character model. Nobody else has "
    "looked at the scene.",
    "What the check cannot show",
    "My human check (TEST-REPORT §7) · render: native Godot 4.7.2, film camera added by capture script",
    "godot_tablet.png", "figures/godot_tablet.png",
    "It cannot show whether the assets look right; that is my human check.",
    f"{SRC} · TEST-REPORT.md §7 and §10 · README.md 'How to run the check'",
    [{"label": "Script proves", "text": "Size, scale, origin, grid"},
     {"label": "I checked", "text": "Readable at a glance"},
     {"label": "Unknown", "text": "Scale next to a person"},
     {"label": "Others", "text": "Nobody else has looked"}],
    [("0.0", "tablet floating beside the large crate, native render"), ("0.05", "script card"),
     ("0.35", "my-check card"), ("0.62", "unknown card"), ("0.88", "others card")],
    [[0.04, 0], [0.33, 1], [0.62, 2], [0.88, 3]]))

# -- B19 what Claude got wrong -------------------------------------------------------------
BEATS.append(board("B19", "ERRORS",
    "What Claude got wrong. It overbuilt the tablet. Its first brief draft marked my own decisions as Claude's "
    "choices, or left them blank. Its first crates were off the grid. It overwrote a test chair file by accident, "
    "and the re-export came out the same size. And the worst one: it wrote fixed for the latch without measuring, and that "
    "went into a push. The next upload corrected it.",
    "What Claude got wrong", "TEST-REPORT §9",
    "TEST-REPORT · SECTION 9",
    "Wrote \"fixed\" without checking: … Claude wrote \"fixed\" into SOURCES and FRICTIONAL and pushed that to "
    "the course repo in commit ce90608, while the files were in fact not fixed yet.",
    f"{SRC} · TEST-REPORT.md §9 (items 1–6) · FRICTIONAL.md",
    "CLAUDE'S ERRORS, AS RECORDED · each one found by measuring or by me",
    "Recorded errors, in order",
    [{"label": "1 · Overbuilt", "text": "Tablet: 21 bevelled parts for a greybox"},
     {"label": "2 · Brief draft", "text": "My decisions marked as Claude's, or blank"},
     {"label": "3 · Off the grid + overwrite", "text": "First crates; test_chair.glb re-exported"},
     {"label": "4 · \"Fixed\" unchecked", "text": "Latch record pushed before it was true"}],
    [("0.0", "TEST-REPORT excerpt and four error cards"), ("0.1", "overbuilt card"), ("0.25", "brief card"),
     ("0.45", "grid / overwrite card"), ("0.7", "unchecked 'fixed' card")],
    [[0.08, 0], [0.18, 1], [0.38, 2], [0.68, 3]]))

# -- B20 contributions, revision, next step ----------------------------------------------------
BEATS.append(board("B20", "CREDITS",
    "Who did what. I made every decision: the three assets, the colours, the grid, the latch, and every accept. "
    "Claude Code wrote and ran all the Blender Python, placed the assets, wrote the check, and drafted the documents. "
    f"This film shows source revision {REV_SPOKEN}. The next step: a character model to settle the scale, the first "
    "gameplay in the game, and a design for the tablet's interaction.",
    "Who did what, and what comes next", "FRICTIONAL · contributions",
    "FRICTIONAL · 2026-10-14 TO 2026-10-15",
    "Claude Code (Claude Opus 5.5) wrote and ran the Blender Python through the MCP … ran the Godot headless "
    "checks, wrote the brief and the asset log from my decisions.",
    f"{SRC} · FRICTIONAL.md · SOURCES.md 'Human / AI contributions' · next step: my decision for this film",
    f"Source revision shown in this film: {REV}",
    "Contributions, then one next step",
    [{"label": "Me", "text": "Decisions, accepts, the latch edit, the human check"},
     {"label": "Claude Code (Opus 5.5)", "text": "Blender Python, scene placement, check script, drafts"},
     {"label": "Revision", "text": f"{REV} · 55 PASS · exit 0"},
     {"label": "Next step", "text": "Character model → first gameplay → tablet interaction design"}],
    [("0.0", "FRICTIONAL excerpt and contribution cards"), ("0.05", "me card"), ("0.3", "Claude card"),
     ("0.6", "revision card"), ("0.75", "next step card")],
    [[0.04, 0], [0.3, 1], [0.58, 2], [0.72, 3]]))

# -- B21 verdict -------------------------------------------------------------------------
BEATS.append(beat("B21", "VERDICT",
    "Verdict. Built: three assets plus two desks, in Blender and in a Godot scene, with a check that passes fifty-five "
    "times. Limits: the tablet is over the shape limit by my choice, the scale next to a person is unknown, and one "
    "latch is six millimetres off. The judgement was mine; the code was Claude's. The checks prove numbers, not looks.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Verdict", "artifactHeading": f"Walker Survival Shooting at {REV}.", "brandLabel": "@NikBearBrown",
     "artifactLines": ["Built: chair, tablet, 2 crates (+ 2 desks), in a Godot scene.",
                       "Checked: 55 headless PASS; my own look at every asset.",
                       "Limits: tablet 21 shapes; no character; latch 6 mm off.",
                       "Human: every decision. Claude: the code."]},
    [("0.0", "verdict artifact page"), ("0.12", "Built line"), ("0.35", "Checked line"), ("0.5", "Limits line"),
     ("0.8", "Human line")]))

# -- B22 your turn ------------------------------------------------------------------------
YT = ("Please use Walker on my Godot project. Read my CHANGE-BRIEF and tests/a3_asset_check.gd. Add one check that "
      "plays each crate's open animation where it stands in base.tscn and tests whether the open lid passes through "
      "the back wall. Predict which crates fail before you run it, and do not move anything to make it pass.")
BEATS.append(beat("B22", "HANDOFF",
    "Your turn. Paste this into Claude. " + YT.replace("base.tscn", "base dot T S C N")
    .replace("tests/a3_asset_check.gd", "my asset check script").replace("CHANGE-BRIEF", "change brief") +
    " The prediction is the point: write down which crate you expect to fail before the log tells you. And keep "
    "the scene as it is; you want to learn what the lid does, not hide it. Liam, in for Bear.",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "GODOT · GAMEDEV · WALKER", "segment": "Walker Survival Shooting",
     "command": YT, "runningText": "paste this into Claude…", "output": [],
     "modelLabel": "Opus 5.5", "largeText": True},
    [("0.02", "composer with greeting 'Your turn.'"), ("0.1", "prompt types in"), ("0.7", "send arms"),
     ("0.9", "Liam signs off")],
    role_note="HANDOFF LAW: prompt read aloud verbatim (file names spoken), then discussed; Liam signs off here."))

# -- B23 locked outro -----------------------------------------------------------------------
BEATS.append({"beat_id": "B23", "act": "OUTRO", "kind": "outro_voice",
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
    "greeting": "Hola, Liam", "greeting_note": "hello lexicon: Hola (Spanish); Assignment 2 used Hej.",
    "game": {"name": "walker-survival-shooting", "source_revision": REV,
             "engine": "Godot 4.7.2.stable.official.ed1daf0bf",
             "game_path": "walker-survival-shooting/godot (exported from b370626)"},
    "note": "godot-gamedev walker film for Assignment 3 (first 3D assets with Claude, the Blender MCP and Blender). "
            "The Godot project has no runtime scripts: one saved scene, imported .glb assets and a headless check "
            "script. Blender stills are the designer's own screenshot and Claude's MCP look captures, labeled as such. "
            "Engine footage is native-4K renders of the unmodified base.tscn through a capture script that only adds a "
            "film camera (or makes the scene's own a3_asset_camera current) and plays the crates' own animations. "
            "No game change, no commit, no push, no publication.",
}


def write(sheet):
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=True) + "\n", encoding="ascii")


def sync():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    for b in sheet["beats"]:
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
