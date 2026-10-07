#!/usr/bin/env python3
"""Author beat_sheet.json for the walker-rudy godot-gamedev film.

Every code excerpt is cut from the game's own files by line range here, so
the text on screen is the text in the file. Timing fields (durationSeconds,
cue times) are filled later by finalize.py from the measured narration.

    python3 tools/make_sheet.py        # from the reel folder
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / "game"
PUB = "reels/claude-liam-walker-rudy-gamedev"   # Remotion public/ subfolder for this reel's stills
TITLE = "Walker Rudy, Wired In."
SLUG = "claude-liam-walker-rudy-gamedev"
PROJECT = "walker-rudy · game/ @ 3b7aa1c"


def lines(path, a, b):
    return "\n".join((GAME / path).read_text().splitlines()[a - 1:b])


def code(bid, act, path, a, b, title, narration, cues, notes, output, components, font=25):
    return {
        "beat_id": bid, "act": act, "narration_text": narration, "components": components,
        "shot": {"type": "REMOTION", "lane": "code", "remotion": {"pattern": "GodotDevWorkbench", "props": {
            "mode": "code", "title": title, "project": PROJECT, "path": "res://" + path,
            "source": f"Source: game/{path}, lines {a}–{b} (verbatim). Godot editor reconstruction.",
            "code": lines(path, a, b), "startLine": a, "codeFontSize": font,
            "inspectorLabel": "Source notes — not Inspector values",
            "notes": [{"label": k, "value": v} for k, v in notes],
            "output": output}},
            "cue_phrases": [{"phrase": p, "line": ln, "label": lb} for p, ln, lb in cues],
            "show": [{"at": p, "event": f"line {ln} highlighted — {lb}"} for p, ln, lb in cues]},
        "excerpt": {"path": path, "start_line": a, "end_line": b},
    }


def play(bid, act, capture, segments, narration, observation, components, chips=(), game_gain_db=-14.0, no_narration=False):
    return {
        "beat_id": bid, "act": act, "narration_text": narration, "components": components,
        "shot": {"type": "VIDEO", "lane": "gameplay", "source": "own", "treatment": "none",
                 "evidence_media": f"media/{bid}.mp4",
                 "capture_plan": {"capture": capture, "segments": segments, "chips": list(chips),
                                  "game_audio_gain_db": game_gain_db, "no_narration": no_narration},
                 "observation": observation},
        "qc": {"full_bleed": True, "full_bleed_reason": "Engine capture. The game renders edge to edge at 3840x2160 (hearts and the F1 debug line sit at the very top by design); the film's provenance chips sit on the soil at the bottom. Only the edge-bleed check is waived."},
    }


def seg(a, b, speed=1.0, label=""):
    return {"from": a, "to": b, "speed": speed, "label": label}


B = []

# ── walker bookends ─────────────────────────────────────────────────────────
B.append({"beat_id": "B00", "act": "cold open — the Walker ask", "components": [],
  "role_note": "walker modifier B00. Reconstructed prompt, said out loud; not a transcript.",
  "narration_text": "Jambo, this is Liam, in for Bear. That prompt is an illustrative reconstruction of the ask, not a transcript of anything anyone typed. What is real is underneath it: walker-rudy, an asset slice by shuai-z for CSYE seventy-two seventy, and the Godot source I am about to take apart, file by file.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Jambo, Liam", "topic": "WALKER-RUDY · GODOT 4.7 GAME DEVELOPMENT", "segment": TITLE,
    "command": "Please use Walker to convert my game design document about Walker Rudy — a cheerful chibi boy in a grey robe who runs, jumps and stomps goblins across autumn harvest fields to a teleport circle, with generated art, sound effects and a looping folk theme — into a small playable Godot asset slice I can run, read and extend.",
    "runningText": "reconstructed prompt — illustrative, not a transcript…",
    "output": ["Repo walker-rudy · game/ at 3b7aa1c · Godot 4.7.2 · started from an empty repository.",
               "Built: Level 1, Harvest Fields — 16 Rudy frames, 6 sound effects, 1 music loop, 141 checks.",
               "Design and every accept/reject: shuai-z · code: Claude Code · art: Gemini · sound: Firefly, ElevenLabs · music: Suno."],
    "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"}}}})

B.append({"beat_id": "B01", "act": "BLUF — what was actually built", "components": [], "lead_silence_s": 0.8,
  "role_note": "EXECUTIVE-SUMMARY LAW. The correction is the film's actual misconception: the models did not make the game.",
  "qc": {"sparse_by_design": True, "sparse_reason": "BrutalistHesitantWriter types the overview token by token; mid-beat frames are mostly cream by design."},
  "narration_text": "Walker Rudy is one level built from generated parts. The models made the pictures, the sound effects and the music. Code makes them behave like one game, and that code is what we are opening.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
    "text": "Walker Rudy is one level\nthat AI generated.\nModels made the pictures and sounds;\ncode makes them one game.",
    "triggerWords": "that AI generated", "replacementWords": "built from generated parts",
    "seed": "walker-rudy-gamedev-bluf-2026-10-04", "face": "serif", "fontSize": 104, "lineSpacing": 1.4,
    "align": "center", "charMs": 22, "jitter": 6, "mistakeRate": 3, "hesitateWithin": 1, "hesitateBetween": 4, "banner": ""}}}})

B.append({"beat_id": "B02", "act": "concept and pillars", "components": ["app-flow"],
  "narration_text": "The design came first, committed before any generation. Here is the game in two sentences, and the four pillars every asset had to serve. Your gear is your plan. Read every threat. It stings, then you try again. And a journey into another world. Now watch the whole level, with nothing but its own sound.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "GodotDesignBoard", "props": {
    "title": "The Design, Before Any Generation", "section": "CONCEPT.md — the game in two sentences",
    "excerpt": "You play Rudy, a cheerful chibi boy with medium-length, center-parted blond hair that leans toward light brown, green eyes and a grey robe with a large hood worn down, who crosses a medieval countryside to reach the teleport circle at the end of each level. He runs, jumps and stomps goblins; with a sword and shield or a magic staff he can also fight and block, until a hit knocks the gear away.",
    "source": "Source: CONCEPT.md draft v4 (design tagged design-v1 before the first generation). Cards: the pillars and what serves each in the slice.",
    "status": "DESIGN DOCUMENT · the slice builds Level 1 only; the staff and the mushroom are not in it",
    "visualLabel": "Design pillars → what serves each one in the running slice",
    "layout": "cards",
    "cards": [{"label": "P1 · Your gear is your plan", "text": "the sword form: its own poses, its own swish"},
              {"label": "P2 · Read every threat", "text": "outlined goblins and spikes on a soft painted world"},
              {"label": "P3 · It stings, then you try again", "text": "the gear flies off, he flashes, the music dips"},
              {"label": "P4 · A journey into another world", "text": "a castle on a slow far layer; a folk loop"}]}},
    "cue_cards": [["Your gear", 0], ["Read every", 1], ["It stings", 2], ["journey", 3]]}})

B.append(play("B03", "the whole slice — its own audio, no narration", "run-01",
  [seg(55, 580, 1.0, "")],
  "", "Title, Enter, the full level: a spike jump, a stomp, the pickup, two cuts, two cliffs, the circle and the silent end card. Only the game's own mix.",
  ["app-flow", "audio", "level"], chips=["SLICE AUDIO ONLY · NO NARRATION"], game_gain_db=-6.0, no_narration=True))

B.append({"beat_id": "B04", "act": "where things live — the main scene", "components": ["app-flow", "audio", "hud"],
  "narration_text": "Here is how a developer finds it. One main scene: the level, Rudy, a camera, the HUD, and a small node that reads the keys that must work while paused. Two autoloads sit outside it, Sfx and Music, so reloading the level never cuts the sound. And some nodes exist only at runtime: code makes the sound players and the ground's collision boxes.",
  "shot": {"type": "REMOTION", "lane": "code", "remotion": {"pattern": "GodotDevWorkbench", "props": {
    "mode": "tree", "title": "One Scene, Two Autoloads", "project": PROJECT,
    "source": "Source: game/app/main.tscn, game/project.godot [autoload] and [layer_names]. Godot editor reconstruction.",
    "treeLabel": "Scene — app/main.tscn (saved) + autoloads",
    "tree": ["Main (Node2D) · app/main.gd", "├ Level1 · content/level_1/level_1.tscn", "├ Rudy (CharacterBody2D) · rudy.tscn",
             "├ Camera (Camera2D) · smoothing 6.0", "├ Hud (CanvasLayer) · ui/hud.tscn", "└ SystemKeys (Node) · app/system_keys.gd",
             "Autoload  Sfx · systems/audio/sfx.gd", "Autoload  Music · systems/audio/music.gd"],
    "inspectorLabel": "Source notes — not Inspector values",
    "notes": [{"label": "Main.State (main.gd:37)", "value": "TITLE · PLAYING · DYING · COMPLETE"},
              {"label": "Made by code at runtime — in no .tscn", "value": "6 Sfx players, Music's Loop player, each ground block's CollisionShape2D, the flying gear"},
              {"label": "Physics layers (project.godot)", "value": "1 World · 2 Player · 3 Enemy · 4 Hazard · 5 Trigger"}],
    "output": ["saved scene + project autoloads", "runtime nodes named from source, not a remote-tree capture"]}},
    "cue_phrases": [{"phrase": "the level", "line": 2, "label": "Level1"}, {"phrase": "Rudy", "line": 3, "label": "Rudy"},
                    {"phrase": "a small node", "line": 6, "label": "SystemKeys"}, {"phrase": "Sfx and Music", "line": 7, "label": "the autoloads"}]}})

B.append({"beat_id": "B05", "act": "where things live — the level", "components": ["level", "hazards-checkpoints", "goblin", "sword-pickup"],
  "narration_text": "Level one is one scene laid out by numbers. Three ground blocks, so two gaps, two hundred ten and two hundred pixels wide. Two rows of spikes, three goblins, one pickup, one waystone, one circle, seven thousand seven hundred pixels end to end. The painted sky moves at two percent of the camera and the fields at forty, which is why the castle feels far away.",
  "shot": {"type": "REMOTION", "lane": "code", "remotion": {"pattern": "GodotDevWorkbench", "props": {
    "mode": "tree", "title": "Level 1, Laid Out by Numbers", "project": PROJECT,
    "source": "Source: game/content/level_1/level_1.tscn positions; backdrop.gd FAR_MOTION and FIELDS_MOTION. Godot editor reconstruction.",
    "treeLabel": "Scene — content/level_1/level_1.tscn (x in game px)",
    "tree": ["Backdrop · Far/Sky (CanvasLayer −1)", "Ground/Segment1  x 0–4300", "Ground/Segment2  x 4510–6400",
             "Ground/Segment3  x 6600–7700", "Hazards/SpikesA 1065 · SpikesB 5180", "Enemies/GoblinA 1500 · B 3000 · C 5600",
             "SwordPickup 2500 · Waystone 4000", "Portal 7200 · StartPoint 300"],
    "notes": [{"label": "Gaps between ground blocks", "value": "210 px and 200 px"},
              {"label": "Parallax (backdrop.gd)", "value": "sky_castle.jpg at 0.0218 of the camera · fields.png at 0.4"},
              {"label": "Goblin patrols", "value": "400, 500 and 400 px to the right of where each starts"}],
    "output": ["walk line y = 840 · kill line y = 1300 (main.gd)"]}},
    "cue_phrases": [{"phrase": "Three ground", "line": 2, "label": "three ground blocks"}, {"phrase": "Two rows", "line": 5, "label": "spikes"},
                    {"phrase": "three goblins", "line": 6, "label": "goblins"}, {"phrase": "one pickup", "line": 7, "label": "pickup and waystone"},
                    {"phrase": "one circle", "line": 8, "label": "the teleport circle"}, {"phrase": "painted sky", "line": 1, "label": "the far layer"}]}})

# ── components: code → result ───────────────────────────────────────────────
B.append(code("B06", "app flow — the title", "app/main.gd", 98, 110, "Enter: From Title to Play",
  "The first state change. On the title, Rudy is waiting, out of the player's control. Enter calls start play: a static flag records that the title has shown, the state becomes playing, Rudy's mode becomes play, and the HUD fades the title out while the hearts fade in. Notice what is missing: no music call. The theme started under the title and simply carries on.",
  [("Enter calls", 98, "Enter on the title"), ("static flag", 107, "title_shown: once per run"), ("state becomes", 108, "TITLE → PLAYING"),
   ("mode becomes", 109, "Rudy.Mode.PLAY: control"), ("fades the title", 110, "title out, hearts in")],
  [("Rudy before Enter", "Mode.WAITING (set in _ready)"), ("Fade", "FADE_TIME = 0.35 s"), ("Music", "Music.start() ran in _ready")],
  ["_process reads Enter; Main is the only reader"], ["app-flow", "hud"], font=23))
B.append(play("B07", "result — the title fades", "run-01", [seg(10, 215)],
  "Watch the title fade and the hearts arrive. Same screen, no load, and the music carries straight through.",
  "Enter at frame 77; the title fades and the hearts fade in; Rudy starts running at frame 85 on the same screen.", ["app-flow", "hud"]))

B.append(code("B08", "controller — turning on the spot", "content/rudy/rudy.gd", 203, 215, "Turning on the Spot",
  "Movement. When the input direction differs from his facing, he turns at once. On the ground the turn also zeroes his speed and starts a hold timer of a hundred and twenty milliseconds, and while it runs his target speed is zero. So a tap turns him in place, and only a held key moves him. The trade: crisp turning, for a tiny delay before a reverse run.",
  [("he turns at once", 205, "facing = dir"), ("zeroes his speed", 207, "velocity.x = 0 on the ground"), ("hold timer", 208, "turn_hold_time = 0.12 s"),
   ("target speed is zero", 214, "no movement while the timer runs")],
  [("run_speed", "560 px/s (rudy.gd:55)"), ("run_accel", "5600 px/s² — full speed in 0.1 s"), ("turn_hold_time", "0.12 s")],
  ["_physics_process, 60 ticks per second"], ["rudy-controller"]))
B.append(play("B09", "result — tap to turn", "run-03", [seg(40, 175), seg(80, 106, 0.25, "REPLAY 0.25× — the two taps, no sound")],
  "Debug line on, with F one. Tap left: he faces left, and x stays at three hundred. Tap right, the same. Hold it, and he runs.",
  "Debug line shows x 300 through both taps (frames 82 and 104); the run starts at frame 125.", ["rudy-controller", "hud"], chips=["DEBUG LINE ON (F1)"]))

B.append(code("B10", "controller — the jump and its sound", "content/rudy/rudy.gd", 217, 227, "The Jump, and Its One Sound",
  "The jump needs a fresh press and ground underfoot, so holding the key cannot jump again. The jump sound is called on the line after the velocity is set: sound follows the state, it never decides it. Fifteen hundred pixels a second upward, with heavier gravity on the way down. That gives a two hundred ninety four pixel apex, a rise in point three eight seconds and a fall in point three two.",
  [("fresh press", 219, "is_action_just_pressed + floor"), ("jump sound", 222, "Sfx.play after the state change"), ("Fifteen hundred", 221, "velocity.y = −jump_velocity"),
   ("heavier gravity", 218, "fall_gravity on the way down")],
  [("jump_velocity", "1500 px/s (rudy.gd:60)"), ("gravity / fall_gravity", "4000 / 6400 px/s²"), ("rudy.gd:60 comment", "apex 294 px · rise 0.38 s · fall 0.32 s")],
  ["input → velocity → Sfx.play(&\"jump\") → SFX-JUMP.wav on the SFX bus"], ["rudy-controller", "audio"]))
B.append(play("B11", "result — one key, one jump, one sound", "run-03", [seg(150, 262), seg(190, 218, 0.25, "REPLAY 0.25× — the held key, no sound")],
  "A jump in place: one sound. Now the key is held for a second and a half. One takeoff, one sound, nothing more.",
  "Jump in place at frame 158 plays one SFX-JUMP; the key held 90 ticks from frame 195 gives one takeoff and one sound (driver check).", ["rudy-controller", "audio"], chips=["DEBUG LINE ON (F1)"]))

B.append(code("B12", "art — which frame is on screen", "content/rudy/rudy.gd", 297, 309, "Sixteen Frames, Chosen by State",
  "Which picture is on screen is a pure function of state. A slash comes first; then the form picks the prefix, plain or sword. In the air he shows rising, or falling only if he was moving sideways when the fall began. On the ground, two run frames alternate every eighth of a second. Sixteen generated frames, chosen by a dozen lines.",
  [("prefix", 297, "CHAR- or CHAR-SWORD-"), ("rising, or falling", 304, "FALL only if moving sideways"),
   ("two run frames", 308, "RUN-A / RUN-B every 0.125 s")],
  [("Look node", "rudy_look.gd swaps the Sprite's texture by pose ID"), ("Frames", "content/rudy/frames/*.png, 410×386 canvas, drawn at half scale")],
  ["pose ID → RudyLook.show_pose(id) → texture (a slash pose wins, lines 295–296)"], ["rudy-controller", "rudy-art"], font=23))
B.append(play("B13", "result — rise, then fall", "run-03", [seg(240, 305), seg(266, 302, 0.25, "REPLAY 0.25× — the running jump, no sound")],
  "A running jump over the spikes. Read the debug line: rise, then at the top, fall, because he was moving.",
  "Debug line reads CHAR-RISE after takeoff at frame 272 and CHAR-FALL from the top of the arc; he clears SpikesA.", ["rudy-art"], chips=["DEBUG LINE ON (F1)"]))

# ── one asset, design → game: CHAR-HURT ─────────────────────────────────────
B.append({"beat_id": "B14", "act": "asset trace 1 — design", "components": ["rudy-art"],
  "narration_text": "Now one asset, all the way from design to game: Rudy's hurt pose. It starts as pose seven on the character sheet, a blockout Claude drew in code, not a model output. Recoiling from a hit, played once, and any gear he carries flies off as its own sprite.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "GodotDesignFigure", "props": {
    "title": "One Asset, Design to Game: CHAR-HURT", "status": "1 · DESIGN — character sheet pose #7",
    "image": f"{PUB}/trace-1-sheet.png", "imageLabel": "design/character/poses.png — code-drawn blockout, not a generative-model output",
    "excerpt": "| 7 | Hurt | took a hit; carried gear flies off as a separate sprite | single | default |",
    "source": "Source: CHARACTER-SHEET.md pose table; design/character/poses.png (drawn by make_blockouts.py).",
    "cards": [{"label": "State", "text": "took a hit"}, {"label": "Plays", "text": "once"},
              {"label": "Faces", "text": "toward the hit"}, {"label": "Storyboard", "text": "panel 4, failure"}]}},
    "cue_cards": [["pose seven", 0], ["played once", 1], ["Recoiling", 2], ["gear he carries", 3]]}})
B.append({"beat_id": "B15", "act": "asset trace 2 — prompt and raw output", "components": ["rudy-art"],
  "narration_text": "The prompt is a template: the reference image attached, the pose line swapped in. Recoiling from a hit from the right, leaning back, arms flung out. Gemini's first answer leaned toward the hit instead. shuai-z rejected it and asked, in one sentence, for him to lean back. The second answer was accepted: thrown almost flat, with gold trim the sheet never asked for, judged at game size and kept.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "GodotDesignFigure", "props": {
    "title": "Prompt → Raw Output → Judgment", "status": "2 · RAW GENERATIONS — not in-engine",
    "image": f"{PUB}/trace-2-raw.png", "imageLabel": "",
    "excerpt": "…the boy in side view facing right, hurt: recoiling from a hit coming from the right, leaning back, eyes squeezed shut, arms flung out. … Change nothing except the pose.",
    "source": "Source: design/generation-prompts.md pose template; ASSET-LOG.md rows CHAR-HURT-01 and -02; generated/rejected and generated/accepted.",
    "cards": [{"label": "Model", "text": "Gemini app (Nano Banana)"}, {"label": "HURT-01", "text": "rejected: leans in"},
              {"label": "Edit", "text": "one sentence: lean back"}, {"label": "HURT-02", "text": "accepted, 2048 px"}]}},
    "cue_cards": [["Gemini", 0], ["first answer", 1], ["one sentence", 2], ["second answer", 3]]}})
B.append({**code("B16", "asset trace 3 — the edits, recorded", "content/rudy/frames/frames.json", 108, 117, "The Edits Are Data Too",
  "Edits are data too. The matting script keyed out that steel-blue background, here is the colour it sampled, then scaled the frame by point one eight one six so his head matches the idle pose, and placed him on the shared canvas, soles on the origin, two texture pixels per game pixel. frames.json records the source file and its hash, so the frame can be traced back.",
  [("keyed out", 111, "background_rgb sampled"), ("scaled the frame", 117, "scale 0.1816"), ("source file", 109, "the accepted original"),
   ("its hash", 110, "source_sha256_12")],
  [("Canvas", "410 × 386 texture px, shared by all 16 frames (frames.json:342)"), ("Body origin", "205, 370: the soles"),
   ("Tool", "design/tools/matte_sprites.py (written by Claude)")], ["frames.json → CHAR-HURT.png → rudy_look.gd FRAMES"], ["rudy-art"])})
B.append({"beat_id": "B16R", "act": "asset trace 3b — the frame the game loads", "components": ["rudy-art"],
  "narration_text": "And this is what that record produced: the frame the game actually loads. Background gone, scaled, standing on the shared canvas, with no outline in the file. Nothing in it was redrawn by hand.",
  "shot": {"type": "VIDEO", "lane": "evidence", "source": "own", "treatment": "none", "evidence_media": "stills/hurt-frame.png",
           "still_plan": {"image": "stills/hurt-frame.png"},
           "observation": "game/content/rudy/frames/CHAR-HURT.png at its 410×386 canvas, enlarged 4× on a dark backing: transparent background, the figure from CHAR-HURT-02 scaled ×0.1816, soles at the 205,370 origin; no outline pixels in the file."},
  "qc": {"full_bleed": False}})
B.append(play("B17", "asset trace 4 — in the engine", "run-02", [seg(40, 160), seg(74, 98, 0.25, "REPLAY 0.25× — the hit, no sound")],
  "And in the engine: he walks into the spikes. The hurt frame, the flash, the knockback. A heart empties. You hear the cry, and the music dips under it.",
  "Frame 79: SpikesA hit; CHAR-HURT shows, Rudy flashes and is knocked back; hearts 3 → 2; SFX-HURT plays and the music dips 6 dB (log music_db).", ["rudy-art", "rudy-controller", "hazards-checkpoints", "audio"]))

B.append(code("B18", "art — the outline shader", "systems/art/outline.gdshader", 31, 41, "The Outline Is Code, Not Paint",
  "One source change you can see. Rudy's gold hair against the generated gold wheat measured a contrast of one point seven one. So instead of trusting the model to draw an outline, a shader adds one. For each pixel it looks at three rings of neighbours, eight texture pixels out, and paints the line colour under the sprite's edge. The same width on every frame, whatever the model drew.",
  [("three rings", 31, "8, 16, 24 points per ring"), ("eight texture", 34, "offset by radius, out to width = 8"),
   ("paints the line", 39, "outline under the edge"), ("same width", 40, "same in every frame")],
  [("width (outline.tres)", "8 texture px = 4 game px"), ("line_color", "#290F0D, the art's line colour"), ("Contrast, hair vs wheat", "1.71 without · 11.13 with (TEST-REPORT.md)")],
  ["used by Rudy, the goblins and the spikes; rings: line 29"], ["rudy-art"], font=23))
B.append({"beat_id": "B19", "act": "result — outline on, outline off", "components": ["rudy-art"],
  "narration_text": "Same frame, same build. Left, the shader at its source width. Right, the width set to zero at runtime on an isolated copy: a diagnostic, not the game. Without it, his hair melts into the wheat.",
  "shot": {"type": "VIDEO", "lane": "evidence", "source": "own", "treatment": "none", "evidence_media": "stills/outline-pair.png",
           "still_plan": {"image": "stills/outline-pair.png"},
           "observation": "Engine frames at 4K, Rudy at x 664 over the wheat: with width 8 the dark line separates hair from wheat; with width 0 the hair and the wheat run together."},
  "qc": {"contrast_regions": [{"label": "left heading", "box": [0.03, 0.04, 0.42, 0.10]}, {"label": "right heading", "box": [0.48, 0.04, 0.85, 0.10]},
                              {"label": "caption", "box": [0.04, 0.79, 0.80, 0.88]}],
         "contrast_reason": "Two engine frames of painted art fill most of the card; the essential text is the two headings and the caption, measured locally."}})

B.append(code("B20", "goblin — stomp or hit", "content/goblin/goblin.gd", 100, 109, "Stomp, or Get Hit",
  "The stomp. Every tick the goblin asks the physics space directly whether its box touches Rudy, because the area's overlap list reports a contact two ticks late. Then one question: was he falling, with his soles at most fourteen pixels below the goblin's top before his last move? Yes: defeat and bounce. No: it is a hit.",
  [("one question", 105, "falling, soles within the margin"), ("fourteen pixels", 104, "soles before this tick's move"),
   ("defeat and bounce", 106, "defeat(&\"stomp\") + bounce"), ("it is a hit", 109, "take_hit")],
  [("Box", "40 × 118 px — body, not ears or arms"), ("STOMP_MARGIN", "14 px (goblin.gd:23)"), ("stomp_bounce", "600 px/s up (rudy.gd:63)")],
  ["intersect_shape every physics tick, not the overlap list"], ["goblin"]))
B.append(play("B21", "result — the stomp, with collision shapes", "run-04", [seg(120, 205), seg(156, 172, 0.25, "REPLAY 0.25× — the stomp, no sound")],
  "Collision shapes on. He comes down on the box: squashed frame, bounce, one stomp sound.",
  "Frame 165: Rudy's capsule lands on GoblinA's 40×118 box from above; the squashed frame shows, he bounces; one SFX-STOMP.", ["goblin", "audio"], chips=["DEBUG: VISIBLE COLLISION SHAPES"]))

B.append(code("B22", "sword — the swing", "content/rudy/rudy.gd", 239, 247, "A Hitbox With a Lifetime",
  "The sword. Its hitbox sits fifty pixels in front of him, and it is live only from point oh three to point one eight seconds of a point three second swing. While it is live, it queries the space for goblins and defeats every one it overlaps, on the same tick.",
  [("fifty pixels", 240, "slash_reach in front"), ("live only", 241, "0.03–0.18 s of 0.3 s"), ("defeats every one", 247, "defeat(&\"slash\")")],
  [("Hitbox", "56 × 70 px (rudy.tscn)"), ("slash_time", "0.3 s; no new swing until it ends")],
  ["one SFX-SLASH per swing (rudy.gd:226)"], ["rudy-controller", "sword-pickup", "goblin"]))
B.append(play("B23", "result — the cut", "run-04", [seg(205, 275), seg(232, 250, 0.25, "REPLAY 0.25× — the cut, no sound")],
  "The box appears in front of him for a few frames. The goblin is cut. One slash sound.",
  "Frame 237: slash pressed with GoblinB 115 px ahead; the hitbox shows in front of Rudy and GoblinB is squashed; one SFX-SLASH.", ["sword-pickup", "goblin"], chips=["DEBUG: VISIBLE COLLISION SHAPES"]))

B.append(code("B24", "damage — gear first, then hearts", "content/rudy/rudy.gd", 134, 146, "Gear First, Then Hearts",
  "Damage. If he carries gear, the hit knocks it away and costs no heart. Otherwise a heart goes. Either way there is one hurt sound, a turn toward the hit, and one point two seconds of invulnerability, so a spike and a goblin together still make one sound.",
  [("knocks it away", 136, "_drop_gear: the flying sprite"), ("a heart goes", 138, "hearts −1"), ("one hurt sound", 140, "Sfx.play(&\"hurt\")"),
   ("invulnerability", 144, "invulnerable_time = 1.2 s")],
  [("knockback", "350 px/s away, 400 up (rudy.gd:73)"), ("hurt_time", "0.35 s without control")],
  ["Main shakes the camera and dips the music on Rudy.hit"], ["rudy-controller", "sword-pickup"]))
B.append(play("B25", "result — the gear flies", "run-02", [seg(215, 320), seg(238, 260, 0.25, "REPLAY 0.25× — the hit, no sound")],
  "No slash this time. He runs into the goblin carrying the sword. The gear spins away, the hearts stay at two, and he flashes.",
  "Frame 243: GoblinB touches Rudy in the sword form; FlyingGear spins up and fades; hearts stay at 2; SFX-HURT.", ["sword-pickup", "rudy-controller"]))

B.append(code("B26", "app flow — a fall", "app/main.gd", 116, 124, "A Fall Costs a Heart",
  "A fall. Below the kill line, the state becomes dying first, so the line cannot fire twice. The fall costs a heart, the hurt sound plays, and the music dips nine decibels and stays down through the fade and the respawn.",
  [("dying first", 117, "state = DYING before anything else"), ("costs a heart", 120, "Rudy.fall_out()"), ("hurt sound", 121, "a fall plays SFX-HURT"),
   ("nine decibels", 122, "Music.DEATH_DIP = −9 dB")],
  [("KILL_Y", "1300 px (main.gd:39)"), ("Checkpoint", "the lit waystone's spawn point, else the start")],
  ["SFX-FALL was cut: the fall plays the hurt cry"], ["app-flow", "hazards-checkpoints", "audio"]))
B.append(play("B27", "result — the fall and the waystone", "run-02", [seg(330, 470), seg(386, 402, 0.25, "REPLAY 0.25× — the fall, no sound")],
  "The waystone lights as he passes. Then he runs off the cliff with two hearts, and gets back up at the waystone with one.",
  "Frame 362 the waystone lights (ring, halo); frame 393 he crosses the kill line (hearts 2 → 1, SFX-HURT); frame 432 he is back in control at x 4120.", ["hazards-checkpoints", "app-flow"]))

B.append(code("B28", "app flow — starting over", "app/main.gd", 125, 135, "The Last Heart Starts It Over",
  "If that was the last heart, the level starts over from the opening: the checkpoint goes back to the start, and the waystone goes dark. Either way, every goblin and the sword pickup are reset, so he always gets back up without gear.",
  [("starts over", 127, "_back_to_the_opening()"), ("every goblin", 130, "monster.reset()"), ("sword pickup", 131, "_pickup.reset()")],
  [("Fade", "0.35 s each way"), ("Hearts after", "a fall: what is left · a start-over: full")],
  ["Music.end_dip(&\"death\") when control returns"], ["app-flow", "goblin", "sword-pickup"]))
B.append(play("B29", "result — the last heart", "run-02", [seg(440, 597), seg(486, 496, 0.25, "REPLAY 0.25× — the last hit, no sound")],
  "One heart left, and a goblin. The defeat pose, the fade, and the opening again: three hearts, the waystone dark.",
  "Frame 490: GoblinB takes the last heart (CHAR-DEFEAT); after the fade Rudy is at x 300 with 3 hearts and the waystone is dark (driver check).", ["app-flow", "hud", "hazards-checkpoints"]))

B.append(code("B30", "audio — the music's dips", "systems/audio/music.gd", 95, 103, "The Deepest Dip Wins",
  "The music. Its dips are named, pause, hurt and death, and kept in a dictionary. It plays at the deepest dip in force, never the sum, so a hit that takes the last heart dips nine decibels, not fifteen. Every change ramps over point one five seconds, so nothing clicks.",
  [("deepest dip", 101, "every dip in force"), ("never the sum", 102, "minf: the deepest, not the sum")],
  [("Dips", "pause −12 · hurt −6 for 0.6 s · death −9 dB"), ("RAMP_TIME", "0.15 s"), ("Fade-out", "1.5 s on the teleport circle")],
  ["dips act on the player's volume, never on the Music bus"], ["audio"]))
B.append(play("B31", "result — pause", "run-03", [seg(290, 405)],
  "Escape: the game freezes, and the music plays on, twelve decibels down.",
  "Frames 313–375: tree paused, 'Paused' over a dimmed screen; log music_db −12.0 while paused, 0.0 after.", ["audio", "hud", "app-flow"], chips=["DEBUG LINE ON (F1)"]))

B.append(code("B32", "audio — the mute keys", "app/system_keys.gd", 18, 29, "Mutes the Game Never Reads",
  "M and N are bus mutes, read by a node that keeps processing while the game is paused. Nothing in the game reads them back, and that is the point. Sound never decides state.",
  [("bus mutes", 29, "AudioServer.set_bus_mute"), ("keeps processing", 18, "_process; PROCESS_MODE_ALWAYS (line 15)"), ("Nothing in the game", 27, "static: no game state")],
  [("Buses", "Music −6 dB · SFX 0 dB (default_bus_layout.tres)")], ["checks: muted, the route runs the same, tick for tick"], ["audio", "app-flow"]))
B.append(play("B33", "result — music muted, then effects muted", "run-03", [seg(395, 600)],
  "Music muted: the jump still sounds. Then effects muted: he still jumps, in silence, and the debug line still counts the call.",
  "Frame 408 M mutes the Music bus; the jump at 427 is audible. Frame 499 N mutes SFX; the jump at 518 is silent and the debug line's jump count rises.", ["audio", "hud"], chips=["DEBUG LINE ON (F1)"]))

B.append(code("B34", "app flow — completion", "app/main.gd", 184, 195, "The Teleport Circle",
  "Completion. The circle can only be entered once; the state guard sees to that. Rudy celebrates, the portal sound plays, the music fades out over a second and a half, a column of light rises, the camera pulls back, and after two seconds the screen fades to the end card.",
  [("entered once", 185, "state guard"), ("celebrates", 188, "CHAR-CELEBRATE"), ("portal sound", 189, "SFX-PORTAL"),
   ("fades out", 190, "Music.fade_out()"), ("column of light", 192, "portal.gd _draw"), ("pulls back", 193, "zoom to 0.8")],
  [("CELEBRATE_TIME", "2.0 s"), ("End card", "silent; Enter plays again")], ["Portal.reached → _on_portal_reached"], ["app-flow", "hazards-checkpoints", "audio", "hud"], font=23))
B.append(play("B35", "result — the circle and the end card", "run-01", [seg(425, 632)],
  "The shimmer, the light, the pull-back, the silent end card. Enter plays again, straight into play: the title shows once per run.",
  "Frame 452 the circle is reached (SFX-PORTAL, music fades); the end card shows at 522; Enter at 582 reloads straight into play.", ["app-flow", "hud", "hazards-checkpoints"]))

B.append(code("B36", "tests — what the checks can and cannot prove", "tests/checks.gd", 1328, 1339, "A Check That Sound Decides Nothing",
  "Then the tests: a hundred and forty one headless checks. This one runs the same scripted route twice, once with sound and once with both buses muted, and demands the same tick count, the same position, the same sound calls. Note the limits. Headless, the audio driver never mixes, so the checks know what the players were told to do, not what anyone heard. And the checks may teleport Rudy to set up a case. This film's footage never does.",
  [("runs the same", 1338, "_run_route, the scripted route"), ("both buses muted", 1332, "SFX and Music muted"),
   ("same tick count", 1339, "ticks, x and sounds, per run")],
  [("Compared at 1342–1343", "runs[0] == runs[1]"), ("Limit", "test-only teleports set up some cases (checks.gd:1696)")],
  ["141 checks; exit code 1 if any fails"], ["tests"], font=23))
B.append({"beat_id": "B37", "act": "result — the actual run", "components": ["tests"],
  "narration_text": "This is the actual run, on the film's snapshot. All checks passed, a hundred and forty one pass lines, exit code zero. Seven hundred thirty three ticks either way.",
  "shot": {"type": "VIDEO", "lane": "evidence", "source": "own", "treatment": "none", "evidence_media": "stills/checks-output.png",
           "still_plan": {"image": "stills/checks-output.png"},
           "observation": "Recorded output of the checks on an isolated copy of game/ at 3b7aa1c: 141 PASS lines, 'all checks passed', exit 0; the muted-route line reports 733 ticks at x 7118.076 both ways."},
  "qc": {"full_bleed": False}})

# ── verdict, your turn, outro ───────────────────────────────────────────────
B.append({"beat_id": "BVD1", "act": "verdict — tested, and not", "components": [], "lead_silence_s": 0.4,
  "narration_text": "Verdict. Settled by machine: a hundred and forty one checks pass on this snapshot. Shown by scripted input in four native 4K takes: every state change in the slice, and all six sounds on real events. Settled by a person: shuai-z's own playtest, sound on and muted, the only person who has played it. Uncertain: the checks cannot hear, the mix had one listener, it ran only on a Mac, and it is one level. Not built: the mushroom, its spores and blocking, and four planned sounds.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Tested, and not",
    "artifactLines": ["Machine: 141 headless checks pass on game/ at 3b7aa1c, re-run for this film on an isolated copy, exit code 0. One of them runs the whole route muted and unmuted: 733 ticks both ways.",
                      "Scripted input, four native-4K takes: every state change in the slice and all six sounds on real events, each asserted by the driver. It is not a human playtest and says nothing about fun.",
                      "Human: shuai-z's own playtest, sound on and then muted (2026-10-04): the effects were clear and the music was fine. No one else has played or listened yet.",
                      "Uncertain: the headless checks cannot hear; one listener judged the mix; tested on macOS only; one level of about thirty seconds.",
                      "Not built: the mushroom, its spores and the shield block; four planned sounds (SFX-FALL, SFX-CHECKPOINT, SFX-SPORE, SFX-BLOCK)."]}}}})
B.append({"beat_id": "BVD2", "act": "verdict — who made what", "components": [],
  "narration_text": "Who made what. Gemini drew Rudy's sixteen frames and every picture in the level. Adobe Firefly made the jump; ElevenLabs the stomp, hurt, portal, slash and pickup; Suno the music loop. Claude Code wrote the GDScript and the preparation scripts, and drafted the documents and prompts. shuai-z made the design decisions, every accept and reject, and the playtests. The next step is the mushroom, so pillar two's shot and block finally exist.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Who made what",
    "artifactLines": ["Gemini app (Nano Banana): Rudy's reference and his 16 game frames; the sky and castle, fields, ground and cliffs, spikes, waystone, teleport circle, sword pickup, goblin, hearts and end card.",
                      "Adobe Firefly: SFX-JUMP. ElevenLabs: SFX-STOMP, -HURT, -PORTAL, -SLASH, -PICKUP. Suno v6 mini: MUS-LOOP. ChatGPT: three run frames, all rejected.",
                      "Claude Code: the GDScript in game/, the matting, prop, sound and music preparation scripts, the checks, and drafts of the documents and prompts.",
                      "shuai-z: the design decisions, every accept and reject, the edit prompts, the loop judgment by ear, and the playtests.",
                      "Source shown: walker-rudy game/ at 3b7aa1c. Next step: the mushroom, its spore and the shield block, so pillar P2's shot-and-block exists."]}}}})
B.append({"beat_id": "BHTF", "act": "your turn", "components": [],
  "narration_text": "Your turn. Here is the prompt, read it with me. Read my change brief and goblin dot g d. Before you edit anything, predict what happens to stomps if the stomp margin goes from fourteen pixels to four. Write a headless check that measures it, then make the change and show me the check before and after. The prediction is the exercise: write yours down first, then let the engine correct you. Liam, in for Bear.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Your turn.", "topic": "WALKER-RUDY · GODOT 4.7 GAME DEVELOPMENT", "segment": TITLE,
    "command": "Read my CHANGE-BRIEF.md and game/content/goblin/goblin.gd. Before you edit anything, predict what happens to stomps if STOMP_MARGIN goes from 14 px to 4 px. Write a headless check that measures it, then make the change and show me the check's result before and after.",
    "runningText": "paste this into your own Claude session…", "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"}}}})
B.append({"beat_id": "BOUT", "act": "outro", "components": [], "kind": "outro_voice",
  "role_note": "OUTRO-LOCK: exact title, @NikBearBrown, slug-seeded mascot, no subline; spoken, never scored; 1.0 s tail.",
  "narration_text": "Walker Rudy, Wired In. At Nik Bear Brown.", "tail_s": 1.0,
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG}}}})

for b in B:
    b.setdefault("voice", "am_onyx")
    b.setdefault("engine", "kokoro")

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": "WALKER-RUDY · GODOT 4.7 GAME DEVELOPMENT", "register": "Teardown",
    "audience": "Claude", "brand": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "engine": "kokoro",
    "voice_kokoro": "am_onyx", "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "greeting": "Jambo, Liam",
    "folderLabel": "@NikBearBrown", "in_for_bear": True, "aspect_ratio": "16:9", "fps": 30,
    "skill": "godot-gamedev (walker modifier)", "student": "shuai-z",
    "game": {"name": "walker-rudy", "revision": "3b7aa1c51663c614af1997720223622979ddcfbf", "short_revision": "3b7aa1c",
             "engine": "4.7.2.stable.official.ed1daf0bf"}},
    "beats": B}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
print(f"wrote beat_sheet.json: {len(B)} beats")
