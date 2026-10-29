#!/usr/bin/env python3
"""Author beat_sheet.json for the walker-rudy Assignment 5 godot-gamedev film.

Every code excerpt is cut by line range from game/ or godot/ here, so the text
on screen is the text in the file. Timing fields (durationSeconds, cue times)
are filled later by build_reel.py from the measured narration.

    python3 tools/make_sheet.py        # from the reel folder
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
A5 = REEL.parents[1]
PUB = "reels/claude-liam-walker-rudy-shaders"   # Remotion public/ subfolder for this reel's figures
TITLE = "Two Shaders for Walker Rudy."
SLUG = "claude-liam-walker-rudy-shaders"
REV = "a2a3a77"
PROJECTS = {"game": f"Walker Rudy · game/ @ {REV}", "godot": f"Walker Rudy Props 3D · godot/ @ {REV}"}
TOPIC = "WALKER-RUDY · SHADERS AND MATERIALS IN GODOT 4.7"


def lines(project, path, a, b):
    return "\n".join((A5 / project / path).read_text().splitlines()[a - 1:b])


def code(bid, act, project, path, a, b, title, narration, cues, notes, output, components, font=25):
    return {
        "beat_id": bid, "act": act, "narration_text": narration, "components": components,
        "shot": {"type": "REMOTION", "lane": "code", "remotion": {"pattern": "GodotDevWorkbench", "props": {
            "mode": "code", "title": title, "project": PROJECTS[project], "path": "res://" + path,
            "source": f"Source: assignment-5/{project}/{path}, lines {a}–{b} (verbatim). Godot editor reconstruction.",
            "code": lines(project, path, a, b), "startLine": a, "codeFontSize": font,
            "inspectorLabel": "Source notes — not Inspector values",
            "notes": [{"label": k, "value": v} for k, v in notes],
            "output": output}},
            "cue_phrases": [{"phrase": p, "line": ln, "label": lb} for p, ln, lb in cues]},
        "excerpt": {"project": project, "path": path, "start_line": a, "end_line": b},
    }


def figure(bid, act, title, status, image, image_label, source, cards, cues, narration, components=()):
    return {"beat_id": bid, "act": act, "narration_text": narration, "components": list(components),
            "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "GodotDesignFigure", "props": {
                "title": title, "status": status, "image": f"{PUB}/{image}", "imageLabel": image_label,
                "excerpt": "", "source": source, "cards": [{"label": a, "text": b} for a, b in cards]}},
                "cue_cards": [[p, k] for p, k in cues]}}


# Stills whose engine images fill most of the frame: the whole-frame ink average measures the pictures, so the
# contrast check is made on the card's own title instead (normalised boxes).
TITLE_REGIONS = {"game-card.png": [0.052, 0.05, 0.5, 0.095], "two-materials.png": [0.052, 0.05, 0.54, 0.098]}


def still(bid, act, image, observation, narration, components=()):
    qc = {"full_bleed": False}
    if image in TITLE_REGIONS:
        qc.update({"contrast_regions": [{"label": "card title", "box": TITLE_REGIONS[image]}],
                   "contrast_reason": "Engine captures fill most of this card; the whole-frame ink average measures them, not text. The title is measured locally."})
    return {"beat_id": bid, "act": act, "narration_text": narration, "components": list(components),
            "shot": {"type": "VIDEO", "lane": "evidence", "source": "own", "treatment": "none",
                     "evidence_media": f"stills/{image}", "still_plan": {"image": f"stills/{image}"},
                     "observation": observation},
            "qc": qc}


def gameplay(bid, act, capture, segments, chips, observation, narration, components):
    return {"beat_id": bid, "act": act, "components": components, "narration_text": narration,
            "shot": {"type": "VIDEO", "lane": "gameplay", "source": "own", "treatment": "none", "evidence_media": f"media/{bid}.mp4",
                     "capture_plan": {"capture": capture, "segments": segments, "chips": chips}, "observation": observation},
            "qc": {"full_bleed": True, "full_bleed_reason": "Engine capture renders edge to edge at 3840x2160; the film's chips sit inside the title-safe inset. Only the edge-bleed check is waived."}}


B = []

# ── walker bookends ─────────────────────────────────────────────────────────
B.append({"beat_id": "B00", "act": "cold open — the Walker ask", "components": [],
  "role_note": "walker modifier B00. Reconstructed prompt, said out loud; not a transcript.",
  "narration_text": "Jambo, this is Liam, in for Bear. That prompt is an illustrative reconstruction, not something anyone typed. "
                    "What is real is underneath it: walker-rudy, the game shuai-z started in Assignment 2, now with two shaders, "
                    "one on the hearts of the 2D game, and one on two stones in the 3D props scene.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Jambo, Liam", "topic": TOPIC, "segment": TITLE,
    "command": "Please use Walker to convert my game design document about Walker Rudy — a chibi boy who crosses the Harvest Fields, "
               "safe for a moment after each hit — into two shaders: hearts that tint while he is invulnerable, driven from game state, "
               "and a textured stone shader with two materials for the waystone and the teleport circle, each claim checked headless or by eye.",
    "runningText": "reconstructed prompt — illustrative, not a transcript…",
    "output": [f"Repo walker-rudy · assignment-5/ at {REV} · Godot 4.7.2 · game/ GL Compatibility · godot/ Forward+.",
               "Built: invulnerable_tint.gdshader on the hearts; weathered_stone.gdshader with two materials; the hint experiment.",
               "Every shader line: shuai-z, by hand · brief, driver, tests and captures: Claude Code, reviewed by shuai-z."],
    "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"}}}})

B.append({"beat_id": "B01", "act": "BLUF — what was actually built", "components": [], "lead_silence_s": 0.8,
  "role_note": "EXECUTIVE-SUMMARY LAW. The correction is the misconception: the shaders were not written by the agent.",
  "qc": {"sparse_by_design": True, "sparse_reason": "BrutalistHesitantWriter types the overview token by token; mid-beat frames are mostly cream by design."},
  "narration_text": "Two shaders for Walker Rudy, written by hand. Not by Claude. Claude drafted the brief, the driver and the tests; "
                    "shuai-z typed every shader line. Then the machine checked what a machine can, and eyes checked the rest.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
    "text": "Two shaders for Walker Rudy,\nwritten by Claude,\nchecked by machine and by eye.",
    "triggerWords": "Claude", "replacementWords": "hand",
    "seed": "walker-rudy-shaders-bluf-2026-10-28", "face": "serif", "fontSize": 112, "lineSpacing": 1.4,
    "align": "center", "charMs": 24, "jitter": 6, "mistakeRate": 3, "hesitateWithin": 1, "hesitateBetween": 4, "banner": ""}}}})

# ── the game, the questions, the brief ──────────────────────────────────────
B.append(still("B02", "the game, the state, the object", "game-card.png",
  "Two frames from the film's own Movie Maker captures at a2a3a77: the 2D game three frames after hit 1 (two full hearts, one empty, "
  "Rudy knocked back and see-through), and the 3D props scene from its own camera with the textured waystone and circle.",
  "Walker Rudy is a 2D side-scroller in Godot four point seven, on the Compatibility renderer. The state this assignment shows is "
  "Rudy's invulnerability: for one point two seconds after a hit, or after he gets back up, hits are ignored. While that window is open, "
  "the hearts in the corner tint toward the waystone's pale blue. The textured shader is in the 3D props scene, in Forward Plus, "
  "on two surfaces: the waystone's stone, and the teleport circle's dark inner disc.", ["tint-shader", "stone-shader"]))

B.append(figure("B03", "four questions, four lines", "Four Questions, Four Lines",
  "THE ASSIGNMENT'S FOUR QUESTIONS — each answer points at a line", "four-questions.png", "",
  "Source: game/shaders/invulnerable_tint.gdshader line 8; godot/materials/circle_darkstone.tres line 9; godot/shaders/weathered_stone.gdshader lines 4 and 7.",
  [("Shader", "runs per fragment"), ("Material", "one object's values"), ("Texture", "colour or data"), ("Language", "Godot's own words")],
  [["What a shader does", 0], ["a material differs", 1], ["texture is information", 2], ["shading language", 3]],
  "Four questions run through this film, and each answer points at a line. What a shader does: line eight of the tint shader. "
  "How a material differs from a shader: a material file that names the shader it uses. Why a texture is information: "
  "a sampler that reads directions, not colours. And what Godot's shading language is: words like group uniforms, which plain GLSL does not have.",
  ["tint-shader", "stone-materials", "stone-shader"]))

B.append(figure("B04", "the specification, before any shader", "The Colour Line, Specified First",
  "CHANGE-BRIEF.md · revision 1, committed before either shader existed", "brief-colour-line.png", "",
  "Source: CHANGE-BRIEF.md §2 (fc9cd523; the shader came later, ae0a3757). Drafted by Claude, reviewed by shuai-z.",
  [("Colour line", "mix toward tint_color"), ("Strength", "0.4: outline 3.5 : 1"), ("Duration", "1.183 s ± one frame"), ("Order", "brief, then shader")],
  [["colour line", 0], ["point four", 1], ["one point one eight three", 2], ["Claude drafted", 3]],
  "The specification came first. The brief was committed before either shader existed, and it holds the colour line: mix the incoming colour "
  "toward the tint colour, by tint amount times tint strength. The strength is point four, not more: at point six the heart's outline would "
  "fall to two point one to one against the sky, under the three to one the brief requires. It also fixes the timing: the tint shows for "
  "one point one eight three seconds, plus or minus one frame, at thirty, sixty and a hundred and forty-four frames a second. "
  "Claude drafted it, and shuai-z reviewed it.", ["tint-shader"]))

# ── the shader from code ────────────────────────────────────────────────────
B.append(code("B05", "the shader from code", "game", "shaders/invulnerable_tint.gdshader", 1, 9, "Nine Lines, Typed by Hand",
  "This is the shader, nine lines, typed by shuai-z from the brief. Shader type canvas item makes it a 2D shader. Three uniforms: "
  "tint amount, which the game drives, and the colour and the strength, which only the material sets. Then the answer to the first question. "
  "A shader is a small program the GPU runs for every fragment it draws, and here fragment runs once for each fragment of the hearts. "
  "COLOR arrives already holding the heart's texel times its modulate, and line eight moves only its red, green and blue toward the pale blue. "
  "Alpha is never written, so transparent pixels stay transparent.",
  [("canvas item", 1, "a 2D shader; no render_mode, so blend_mix"), ("Three uniforms", 3, "tint_amount: the game drives it"),
   ("the colour and the strength", 4, "tint_color, tint_strength: the material only"), ("every fragment", 7, "fragment() runs per fragment"),
   ("line eight", 8, "the colour line, as the brief wrote it"), ("Alpha is never written", 8, ".rgb only: alpha untouched")],
  [("Written", "by shuai-z (ae0a3757)"), ("Defaults", "0.0 · #99E0FF · 0.4"), ("Renderer", "GL Compatibility")],
  ["Hud/Hearts → material res://ui/hearts_tint.tres → shader res://shaders/invulnerable_tint.gdshader"], ["tint-shader"], font=30))
B.append(still("B06", "result — the colour line at controlled values", "tint-captures.png",
  "Windowed Compatibility captures with the driver stopped and tint_amount set from code to 0.0, 0.5, 1.0 and 2.0: P1 and P2 equal the "
  "brief's predictions at 0.0, 0.5 and 1.0; at 2.0 P1 is one step off the unclamped prediction and 81 from the clamped one; P3 stays the sky.",
  "And this is what line eight does, in a window, in the Compatibility renderer. A scripted run stopped the driver and set tint amount from code: "
  "zero, a half, one, and two. The full heart's red is two hundred, sixty-four, fifty-three at zero, and a hundred and eighty-one, one twenty-eight, "
  "one thirty-four at one: exactly the brief's prediction, and the half matches too. Inside the empty heart, where alpha is zero, the sky stays the "
  "same at every value. At two, the red lands one step from the unclamped prediction and eighty-one steps from the clamped one. "
  "So hint range shapes the Inspector's slider. It does not clamp a value set from code.", ["tint-shader", "tint-tests"]))

B.append(code("B07", "the driver", "game", "ui/hud.gd", 108, 111, "One Line Drives It",
  "The driver is one line in the HUD script, and it runs every frame. It divides Rudy's invulnerable time left by the window's length, "
  "and sets that as tint amount on the hearts' material. It reads his state and never writes it. That is half of the second answer, too. "
  "The shader file holds the default, zero. The material, hearts tint dot t r e s, holds the current value, and it is local to the scene, "
  "so no other node shares it.",
  [("every frame", 110, "_process() calls _tint_hearts() (lines 89–92)"), ("divides", 111, "_invulnerable_left / invulnerable_time"),
   ("never writes it", 109, "reads Rudy's state; assigns nothing"), ("holds the current value", 111, "set_shader_parameter on the hearts' own material")],
  [("Rudy's window", "1.2 s, per physics tick"), ("Material", "local to the scene"), ("Written by", "claude -p (bd797945)")],
  ["rudy.gd is unchanged byte for byte; the driver reads _invulnerable_left and invulnerable_time"], ["tint-driver"], font=30))
B.append(gameplay("B08", "result — the effect in play", "play-01-inset",
  [{"from": 0, "to": 425, "speed": 1.0, "label": ""},
   {"from": 30, "to": 210, "speed": 0.5, "label": "REPLAY 0.5× · Enter, the fade-in and hit 1"}],
  ["SCRIPTED INPUT · a film-only driver on a copy presses Enter, move_right and move_left"],
  "The real main scene in Godot 4.7.2 Compatibility, Movie Maker at 3840×2160, 30 fps, scripted input: Enter on the title, the hearts fade in; "
  "hit 1 at frame 131 (tint_amount 0.986), a walk back onto the spikes with no heart lost and no rise; hit 2 at 223; hit 3 takes the last heart "
  "at 308; the respawn at 343 starts the tint again at 0.972. Then a labelled half-speed replay of frames 30–209. The inset shows the same frames' hearts, 3×.",
  "Here it is in play: the real game, at 4K, with scripted input. The spikes. A heart empties, and the full hearts pale toward blue, then fade back. "
  "Back onto the spikes: nothing. Two more hits. The last heart goes, Rudy gets back up, and the tint starts again. "
  "Now at half speed, from the title. Enter, and the hearts still fade in as before. Movie Maker rendered every frame, and a film-only driver "
  "on a copy pressed the same keys a player would. The inset enlarges the hearts from each frame, with the value their material held.",
  ["tint-driver", "tint-shader"]))
B.append(gameplay("B09", "replay — the window, not the hit", "play-01-inset",
  [{"from": 125, "to": 215, "speed": 1 / 3, "label": "REPLAY ⅓× · hit 1, and back onto the spikes"},
   {"from": 300, "to": 385, "speed": 1 / 3, "label": "REPLAY ⅓× · the last heart, and the respawn"}],
  ["SCRIPTED INPUT · a film-only driver on a copy presses Enter, move_right and move_left"],
  "One-third-speed replays of the same capture, labelled: hit 1 (0.986, falling) with Rudy back on the spikes inside the window and no rise or "
  "heart lost, until 0.000 on the first frame he is not invulnerable; then hit 3 and the respawn, where tint_amount jumps from 0.042 to 0.972.",
  "Slower still: the first hit. The window opens at point nine eight six, and the value falls with game time. He walks back onto the spikes "
  "while it is open: no heart goes, and the tint does not jump. Then the last heart. Its window is still running out when he gets back up, "
  "and the respawn opens a new one: the value jumps from point oh four to point nine seven. The tint follows the window, not the hit.",
  ["tint-driver"]))

# ── the textured shader ─────────────────────────────────────────────────────
B.append(figure("B10", "textures are information", "Three Maps, One Colour",
  "ROCK 01 · Poly Haven · Rob Tuytel · CC0 — the 1k PNGs as committed", "rock-textures.png", "",
  "Source: godot/assets/textures/rock_01/ and ATTRIBUTION.md (https://polyhaven.com/a/rock_01); import settings in each .import file; "
  "curl ratios: logs/godot_calibrate_normal_map_check_60fps.log. The 16-bit roughness map is shown scaled to 8 bits.",
  [("Colour", "sRGB, decoded"), ("Normal", "directions in R and G"), ("Roughness", "0 smooth · 1 rough"), ("Curl check", "0.1444 vs 1.8556")],
  [["the first is a colour", 0], ["normal map stores", 1], ["roughness map stores", 2], ["curl check", 3]],
  "Now the 3D side, and the third question: why is a texture information? These are Rock 01's three maps, from Poly Haven, by Rob Tuytel, "
  "C C zero. Only the first is a colour. The normal map stores the direction each bit of surface faces, in its red and green; the roughness map "
  "stores how sharp a reflection is. Those are numbers, not colours, so they must not be decoded as sRGB, and every import setting is set "
  "explicitly, so the editor has nothing left to change. A curl check, calibrated on the OpenGL and DirectX pair, confirmed the normal map's convention: "
  "point one four four, against one point eight six.", ["stone-textures"]))

B.append(code("B11", "the textured shader — its interface", "godot", "shaders/weathered_stone.gdshader", 3, 13, "Where a Texture Becomes Data",
  "The textured shader, also typed by shuai-z. Lines three to five are where a texture becomes information. The albedo sampler says source color, "
  "so Godot decodes it from sRGB. The normal sampler says hint normal. The roughness sampler says neither, so its numbers arrive as stored. "
  "Then the fourth question, Godot's shading language. Group uniforms sorts the controls into surface and relief in the Inspector, and hint range "
  "gives each a slider, with a range and a step. Plain GLSL has neither.",
  [("albedo sampler", 3, "source_color: decoded from sRGB"), ("hint normal", 4, "hint_normal: data, a direction"),
   ("says neither", 5, "no hint: numbers as stored"), ("Group uniforms", 7, "Inspector group 'surface'"),
   ("hint range", 9, "hint_range(min, max, step): a slider"), ("relief", 11, "Inspector group 'relief'")],
  [("Written", "by shuai-z (a87a18be)"), ("Used by", "two materials")],
  ["line 1: shader_type spatial · Forward Plus · two stone surfaces"], ["stone-shader"], font=24))
B.append(still("B12", "result — the interface, swept", "sweep.png",
  "Close-up windowed captures under the scene's own lighting, each uniform at min, default and max on the loaded material: albedo_tint black "
  "73.51 steps; uv_scale 0.25 12.51 and 4.0 9.20; normal_strength 2.62 and 2.93; roughness_offset 2.64 and 0.90 (mean largest-channel change).",
  "This is that interface swept, captured in a window under the scene's own light. Claude did this check at shuai-z's request, and shuai-z "
  "reviewed it. Albedo tint at black takes away the photo's colour. U V scale breaks the look at both ends: at a quarter the texels blur, and at four "
  "the grain is too fine to read. Normal strength and roughness offset barely move it, under three steps on average. The normal map is gentle, the "
  "roughness map is nearly flat, and the sun's highlight cannot land on the stone's sides. The numbers show both uniforms reach the shader. "
  "Under this light, an eye cannot judge them.", ["stone-shader", "stone-materials"]))

B.append(code("B13", "the textured shader — fragment()", "godot", "shaders/weathered_stone.gdshader", 16, 22, "Four Outputs Godot Lights",
  "The fragment function. Scale the U V once, then write four outputs. ALBEDO, the photo times the tint. NORMAL MAP and its depth, the relief. "
  "And ROUGHNESS, the map plus an offset, clamped to between zero and one. These upper-case names are Godot's, not GLSL's: Godot wires them "
  "into its own lighting, which is the other thing its language adds.",
  [("Scale the U V once", 17, "one scaled_uv for all three maps"), ("ALBEDO", 18, "photo × albedo_tint"),
   ("NORMAL MAP and its depth", 19, "NORMAL_MAP, NORMAL_MAP_DEPTH = normal_strength"), ("clamped", 21, "ROUGHNESS kept within 0–1")],
  [("Lit by", "the Sun, energy 1.1"), ("Tonemap", "Filmic"), ("Not written", "METALLIC, ALPHA")],
  ["the lighting itself is Godot's; this shader only supplies the surface"], ["stone-shader"], font=30))
B.append(gameplay("B14", "result — the stone, running", "stone-01",
  [{"from": 0, "to": 690, "speed": 1.0, "label": ""},
   {"from": 690, "to": 930, "speed": 1.0, "label": "CUT · a close arc in front of the waystone"},
   {"from": 1000, "to": 1240, "speed": 1.0, "label": "CUT · a close arc over the teleport circle"}],
  ["CAMERA MOVED BY A FILM-ONLY SCRIPT · props, light, floor and materials untouched"],
  "The real main scene res://scenes/props_room.tscn in Godot 4.7.2 Forward+, Movie Maker at 3840×2160, 30 fps: the scene's own camera, one orbit "
  "at its radius and height, then two close arcs. The waystone's Stone and the circle's DarkStone show Rock 01's grain, lit by the scene's Sun; "
  "the rune, moss and gold keep flat colours; the disc is darker and smoother in relief.",
  "And here it is running: the real props scene, in Forward Plus, at 4K. Only the camera moves, on a film-only script on a copy; the props, "
  "the light and both materials are as saved. Once around the scene. The waystone's stone and the circle's dark disc are drawn by this shader, "
  "through their own materials, while the rune, the moss, the spikes and the gold keep their flat imported colours. "
  "Then close to the waystone: the grain is the photo's, lit by the scene's one sun. "
  "And over the circle. Its material makes the disc darker, flatter in relief and glossier: three values, on the same shader.",
  ["stone-shader", "stone-materials", "stone-textures"]))

B.append(code("B15", "the hint experiment", "godot", "shaders/hint_experiment.gdshader", 2, 13, "One Word, Isolated",
  "The hint experiment isolates one word. One grey strip, three texels: sixty-four, one twenty-eight and one ninety-two. Two samplers read the "
  "same file, and only one says source color. The shader is unshaded, so no light changes the numbers, and a bool picks which sampler writes ALBEDO. "
  "The brief's prediction: with source color the screen shows the file's own values. Without it they are encoded once more on the way out, and "
  "come out at one thirty-seven, one eighty-eight and two twenty-five. Claude's script computed them, and shuai-z "
  "rechecked the left band by hand.",
  [("unshaded", 2, "no lighting: the value goes straight out"), ("only one says source color", 4, "source_color_tex: decoded from sRGB"),
   ("same file", 5, "plain_tex: the same PNG, taken as linear"), ("a bool picks", 6, "use_source_color, set per material"),
   ("writes ALBEDO", 10, "one sampler or the other")],
  [("Written", "by shuai-z (9481663a)"), ("Strip", "3 texels: 64, 128, 192"), ("Tonemap", "Linear, exposure 1.0")],
  ["predicted: A 64, 128, 192 · B 137, 188, 225 (brief §4)"], ["hint-experiment"], font=23))
B.append(still("B16", "result — predicted and measured", "hint-result.png",
  "The windowed Forward+ capture of hint_experiment.tscn: quad A shows 64, 128, 192 and quad B 137, 188, 225, each flat over 9 × 9 pixels; "
  "all six equal the brief's predictions.",
  "Measured in a window: sixty-four, one twenty-eight and one ninety-two on top, and one thirty-seven, one eighty-eight and two twenty-five below. "
  "All six bands are exactly as predicted, and each is flat across nine by nine pixels. So source color is not a label for the Inspector. "
  "It changes the numbers the shader reads. That is why the colour map has it, and the normal and roughness maps do not.", ["hint-experiment"]))

B.append(code("B17", "two materials, one shader", "godot", "materials/circle_darkstone.tres", 8, 16, "A Material Holds Values",
  "The second question, answered with two files. This is the circle's material. It points at the same shader and the same three textures as the "
  "waystone's. What it stores is values: a cooler tint, normal strength point three five, and roughness offset minus a quarter. The shader holds "
  "the code and the defaults; a material holds one object's values for it.",
  [("same shader", 9, "res://shaders/weathered_stone.gdshader"), ("same three textures", 10, "albedo, normal, roughness: Rock 01"),
   ("a cooler tint", 13, "#A4A7B4, chosen by shuai-z (brief revision 2)"), ("point three five", 15, "the waystone's is 1.0"),
   ("minus a quarter", 16, "the waystone's is 0.0")],
  [("Waystone's", "white · 1.0 · 1.0 · 0.0"), ("Attached", "surface overrides"), ("Why", "a worn disc")],
  ["circle_darkstone.tres and waystone_stone.tres differ in three values and share their textures"], ["stone-materials"], font=27))
B.append(still("B18", "result — one shader edit, one material edit", "two-materials.png",
  "Windowed captures from the scene's Camera, in memory only: ALBEDO halved in the loaded shader's line 18 darkens both stones (22.54 and 10.52 "
  "steps); the circle's normal_strength at 2.0 moves it 0.76 steps; its albedo_tint at white moves it 19.97 steps and the waystone 0.00.",
  "The test, in memory and never saved. The two materials share one shader object. Halve ALBEDO in line eighteen of the loaded shader, and both "
  "stones darken: by twenty-two and a half steps, and by ten and a half. Change one value in the circle's material, its tint to white, and only "
  "the circle changes, by twenty steps; the waystone by zero. The first try, normal strength at two, moved the circle by less than a step, too "
  "little to see, so the check was revised to the tint.", ["stone-materials"]))

B.append(still("B19", "the generated shader beside mine", "generated-vs-mine.png",
  "Verbatim lines from standard_generated.gdshader (10–11, 69–72, with shuai-z's comments) above their equivalents in weathered_stone.gdshader "
  "(3–4, 19–20).",
  "For comparison, shuai-z converted a standard material with the same textures into shader code in the editor, and annotated it. Two of its lines, "
  "beside mine. Its albedo sampler says source color, as mine does on line three. Its normal goes to NORMAL MAP, with the strength set apart "
  "on NORMAL MAP DEPTH, as my lines nineteen and twenty do. But its normal hint is hint roughness normal, not hint normal. And the generated file "
  "has sixteen uniforms; mine has seven.", ["generated-shader"]))

# ── verification ────────────────────────────────────────────────────────────
B.append(code("B20", "what the tests proved", "game", "tests/invulnerable_tint_checks.gd", 347, 354, "Measuring the Window",
  "Now what the tests proved. This is the duration check in the driver's test. The test plays through real input and samples tint amount once a frame. "
  "Here it measures how long the tint shows, from its first frame to its last: seventy-one sixtieths of a second, plus or minus one frame, and two "
  "point four seconds of real time at half speed. The test never calls take hit, and never sets the shader parameter itself.",
  [("how long the tint shows", 350, "frames from first > 0 to the end, ÷ fps"), ("seventy-one sixtieths", 349, "71 ticks of 1/60 s = 1.1833 s"),
   ("plus or minus one frame", 351, "tolerance: 1 / fps"), ("half speed", 349, "time scale 0.5: 144/60 = 2.4 s")],
  [("Input", "Input.action_press()"), ("Sampler", "after every _process()"), ("Written by", "claude -p (bd797945)")],
  ["scripts/run-test.sh game invulnerable_tint_checks.tscn 30 | 60 | 144"], ["tint-tests"], font=23))
B.append(still("B21", "result — three frame rates", "tint-tests.png",
  "Recorded headless output at 30, 60 and 144 fps through scripts/run-test.sh: 15 PASS and 'all checks passed' at each; A9 1.2000, 1.1833 and "
  "1.1806 s against 1.1833 ± one frame, and 2.4 s at time scale 0.5; A10 no rise; A11 the respawn's jump; A12 the pause holds.",
  "Headless output, at three pinned frame rates, through the course's wrapper. One point two, one point one eight three three, and one point one "
  "eight oh six seconds, each within one frame of the prediction. Fifteen of fifteen checks at every rate. In the driver's own session, a frame-counting "
  "version of the HUD failed this check at thirty and at a hundred and forty-four. But these are numbers about what the material holds, not about "
  "a single pixel.", ["tint-tests"]))
B.append(still("B22", "mutations", "mutations.png",
  "Recorded headless output of the three mutations shuai-z made: no semicolon (SHADER ERROR, 2 failed), tint_amount renamed (2 failed, no shader "
  "error), source_color deleted from albedo_tex (1 failed); and test_materials.gd at 125 PASS.",
  "Can the checks fail? shuai-z made three mutations. Delete the semicolon after shader type, and there is a shader error, and the test exits with one. "
  "Rename tint amount: the shader still parses, so only the uniform check catches it, and it exits with one. Delete source color from the albedo "
  "sampler: no error at all, but the materials test reads the hint from the source, fails one check, and exits with one. Clean, that test passes "
  "a hundred and twenty-five of a hundred and twenty-five, after a fresh import from an empty cache.", ["tint-tests", "stone-tests"]))
B.append(still("B23", "what no headless run shows", "headless-limits.png",
  "The hint scene's engine capture beside a macOS screenshot of the same window: the screenshot reads 4 to 11 steps darker in every band; "
  "converted from the display profile to sRGB it matches the engine exactly.",
  "And what no headless run can show. The headless renderer draws nothing, so every look in this film comes from a window. Even then, which picture "
  "you trust matters. A macOS screenshot of the hint scene reads four to eleven steps darker than the engine's own capture, because it carries the "
  "display's colour profile; converted to sRGB, it matches exactly. And no test can say the hearts read well, or that the stone looks like stone. "
  "Those were eyes: shuai-z played the game, watched the fade-in, and checked the materials in the editor.", ["stone-tests", "hint-experiment"]))

# ── verdict, your turn, outro ───────────────────────────────────────────────
B.append({"beat_id": "BVD1", "act": "verdict — checked, uncertain, caught", "components": ["tint-tests", "stone-tests"], "lead_silence_s": 0.4,
  "narration_text": "Verdict. Checked by machine: the existing hundred and forty-one and forty-four checks still pass; the tint test passes at three "
                    "frame rates; the materials test passes after a fresh import; and three mutations each fail. In windowed captures, the hearts at zero, a "
                    "half and one, and all six hint bands, match the predictions exactly. By eye, shuai-z played it, including the three edge cases. Uncertain: why the hearts need "
                    "no sRGB step is read from the engine's source, not checked here; one edge pixel is one step off, unexplained; two stone controls "
                    "cannot be judged under this light; and nobody else has played it. The agents' mistakes that were caught: a probe that counted "
                    "its own marker as a shader error; permission rules that stopped matching after a change of folder; Rock 01 copied to the wrong "
                    "folder, which the first import showed; and an audit's three megabytes that nobody measured.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Checked, uncertain, caught",
    "artifactLines": ["Machine: 141/141 and 44/44 existing checks; the tint test 15/15 at 30, 60 and 144 fps; test_materials 125/125 after a fresh import; three mutations each exit 1.",
                      "Windowed captures: hearts P1/P2 exact at 0.0, 0.5, 1.0; six hint bands exact. Eyes: shuai-z played: tint, fade-in, back on the spikes, last heart, pause. Sweep and two materials: Claude, at shuai-z's request; reviewed.",
                      "Uncertain: no sRGB step for the hearts (read from the source, not checked); one edge pixel 1 step off; normal_strength, roughness_offset below sight here; macOS M3 only; no other player.",
                      "Caught: a probe's own marker counted as SHADER ERROR; relative permission rules re-anchored by a cd; Rock 01 copied to the wrong folder; 'about 3 MB' unmeasured (1,908,496 bytes)."]}}}})
B.append({"beat_id": "BVD2", "act": "verdict — who made what, next step", "components": [],
  "narration_text": "Who made what. shuai-z wrote the three shaders and committed each alone, reviewed the brief and every prompt, made the mutations, "
                    "chose the circle's tint and the curl threshold, annotated the generated shader, wrote the language notes, and played the game. "
                    "Claude drafted the brief and the records, ran the scoped sessions that wrote the driver, its test and the materials audit, wrote "
                    "the capture tools, did the sweep at shuai-z's request, and made this film. The textures are Rock 01, by Rob Tuytel, C C zero. "
                    "The source shown is a two a three a seven seven. The next step: a test scene with a low, grazing light, so normal strength and "
                    "roughness offset can be judged by eye.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Who made what",
    "artifactLines": ["shuai-z: wrote all three shaders (ae0a3757, a87a18be, 9481663a); reviewed the brief and every prompt; the mutations; the circle's tint #A4A7B4 and the curl threshold 0.5; annotated the generated shader; LANGUAGE-NOTES.md; the playtest.",
                      "Claude Code (Opus 5.5): drafted CHANGE-BRIEF, FRICTIONAL, SOURCES, TEST-REPORT; ran the scoped claude -p sessions (CLAUDE.md, the driver and its test, the materials audit); the capture tools; the sweep, two-materials and OS checks at shuai-z's request; this film.",
                      "Textures: Rock 01 by Rob Tuytel, Poly Haven, CC0 (rock_01_diff, _nor_gl, _rough; _nor_dx for calibration). Grey strip: written by code. Narration: Liam, local Kokoro am_onyx.",
                      f"Source shown: walker-rudy assignment-5/ at {REV} (runtime source unchanged since bd79794 in game/, fe79590 in godot/). Next: a grazing-light test scene to judge normal_strength and roughness_offset by eye."]}}}})
B.append({"beat_id": "BHTF", "act": "your turn", "components": [],
  "narration_text": "Your turn. Here is the prompt; read it with me. Read my change brief and the hearts' tint shader. Before you change anything, work out "
                    "by hand the full heart's red pixel at tint amount one if the tint strength were point six, and the outline's contrast against the sky. "
                    "Then, on a copy, set the strength to point six in the hearts' material, not the shader, run the tint capture, and show me the pixels "
                    "beside my prediction. Write your prediction down first. Liam, in for Bear.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Your turn.", "topic": TOPIC, "segment": TITLE,
    "command": "Read my CHANGE-BRIEF.md and game/shaders/invulnerable_tint.gdshader. Before you change anything, let me predict by hand P1's colour "
               "at tint_amount 1.0 if tint_strength were 0.6, and the heart outline's contrast against the sky (rule 9 asks for 3:1). Then, on a copy "
               "of game/, set tint_strength to 0.6 in ui/hearts_tint.tres, not in the shader, run tests/capture_tint.tscn in a window, and show me "
               "the measured pixels beside my prediction.",
    "runningText": "paste this into your own Claude session…", "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"}}}})
B.append({"beat_id": "BOUT", "act": "outro", "components": [], "kind": "outro_voice",
  "role_note": "OUTRO-LOCK: exact title, @NikBearBrown, slug-seeded mascot, no subline; spoken, never scored; 1.0 s tail.",
  "narration_text": f"{TITLE} At Nik Bear Brown.", "tail_s": 1.0,
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG}}}})

for b in B:
    b.setdefault("voice", "am_onyx")
    b.setdefault("engine", "kokoro")

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "register": "Teardown",
    "audience": "Claude", "brand": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "engine": "kokoro",
    "voice_kokoro": "am_onyx", "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "greeting": "Jambo, Liam",
    "folderLabel": "@NikBearBrown", "in_for_bear": True, "aspect_ratio": "16:9", "fps": 30,
    "skill": "godot-gamedev (walker modifier)", "student": "shuai-z",
    "game": {"name": "walker-rudy (assignment-5: game/ and godot/)", "revision": "a2a3a77d50c5c9d8a65663d21898b7de54096604", "short_revision": REV,
             "engine": "4.7.2.stable.official.ed1daf0bf", "folders": ["assignment-5/game", "assignment-5/godot"]}},
    "beats": B}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
print(f"wrote beat_sheet.json: {len(B)} beats")
