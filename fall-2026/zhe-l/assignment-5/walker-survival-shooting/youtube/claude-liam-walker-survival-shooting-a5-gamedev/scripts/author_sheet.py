"""Author beat_sheet.json for the walker-survival-shooting Assignment 5 gamedev film (DRAFT).

Pass 1 (no args): narration, shots and props with placeholder durations.
Pass 2 (--sync): after Kokoro has measured audio, converts cue fractions into seconds.
--rebuild: re-author but keep measured audio/render fields of beats whose narration is unchanged.
--tbd: list every value still marked [TBD ...] (the film must not be voiced while any remain).
All code excerpt text is read from the game copy at run time (never retyped). GAME will be switched to
the export of the submitted course-repo revision once it exists; until then it is the 2026-11-01
working-folder snapshot B (whose .gd comments are still Chinese; only .gdshader/.tres excerpts are final).
Run:  python -I scripts/author_sheet.py [--sync | --rebuild | --tbd]
"""
import json
import re
import sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
A5 = REEL.parents[1]
GAME = Path("<course-repo>/fall-2026/zhe-l/assignment-5/walker-survival-shooting/godot")   # course repo a84cfa23, read only
PUB = "claude-liam-walker-survival-shooting-a5-gamedev"
SLUG = PUB
PROJECT = "project_survival_shooting"

# ---- values the user decides -------------------------------------------------------------------
TITLE = "claude-liam-walker-survival-shooting-a5-gamedev"   # user, 2026-11-01: the slug, as is
GREETING = "Hola"                         # user, 2026-11-01
REV = "2d558bba"                          # last game-source change (user, 2026-11-01); files read at a84cfa23
REV_SPOKEN = "two, d, five, five, eight, b, b, a"
NEXT_STEP = ("put the tablet's own interface on its screen through a SubViewport, so the screen shows more "
             "than a glow")
UNCERTAIN = ("only captures, never a headless run, show that the GPU really decodes s R G B; why the right "
             "normal map scores zero point two and not zero, which the report puts down to eight-bit "
             "quantisation; and what hint roughness normal does to roughness on import")
SRC = "walker-survival-shooting @ a84cfa23 (game source = 2d558bba)"


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


def figure(bid, narration, title, status, image, image_label, source, cards, show, cues, evidence=True, **extra):
    props = {"title": title, "status": status, "image": f"{PUB}/{image}", "imageLabel": image_label,
             "excerpt": "", "source": source, "cards": cards}
    if evidence:
        extra.setdefault("shot_extra", {})["evidence_media"] = f"figures/{image}"
    return beat(bid, "RESULT", narration, "GodotDesignFigure", props, show, cues, **extra)


def workbench(bid, narration, title, path, start, end, notes, output, show, cues, **extra):
    props = {"mode": "code", "title": title, "project": PROJECT,
             "path": f"{path}  ·  lines {start}–{end}", "code": lines(path, start, end),
             "startLine": start, "codeFontSize": 26 if end - start < 16 else 23,
             "source": f"{SRC} · godot/{path} lines {start}–{end}",
             "inspectorLabel": "Source notes — derived from these lines", "notes": notes, "output": output}
    return beat(bid, "CODE", narration, "GodotDevWorkbench", props, show, cues, **extra)


BEATS = []

# -- B00 walker cold open -----------------------------------------------------------------------
PROMPT = ("Please use Walker to convert my game design document about a third-person extraction shooter, where a "
          "survivor lives in a subway base and carries a rugged military tablet, into its first shaders: a tablet "
          "screen that glows only while the tablet is in hand, and worn paint on the weapon crates, with a "
          "specification, tests and in-engine captures.")
BEATS.append(beat("B00", "ASK",
    f"{GREETING}, this is Liam, narrating for Jonathan. The prompt on screen is a reconstruction for this film, not a saved "
    "session. It asks Walker to give a subway extraction shooter its first shaders: a tablet screen that glows only "
    "in the hand, and weapon crates whose paint has worn through to rust. "
    f"At source revision {REV_SPOKEN}, the answer is two shaders written by hand, two materials, and the tests "
    "that pin them.",
    "ClaudeComposerAsk",
    {"greeting": GREETING, "topic": "GODOT · GAMEDEV · WALKER",
     "segment": "Reconstructed prompt (illustrative, not a saved session)", "command": PROMPT,
     "runningText": f"reading the submitted revision {REV}…", "modelLabel": "Opus 5.5", "largeText": True,
     "output": ["Reconstruction for this film, not a historical transcript.",
                "Built: screen-glow shader + driver; crate-wear shader + 2 materials.",
                "Checked: screen 24 PASS at 30/60/144 fps; materials 169 PASS."]},
    [("0.02", f"composer fades in; greeting '{GREETING}'"), ("0.15", "reconstructed prompt types in"),
     ("0.6", "running line names the revision"), ("0.75", "three answer lines land")]))

# -- B01 hesitant writer -----------------------------------------------------------------------
BEATS.append(beat("B01", "BLUF",
    "I wrote my first two shaders by hand, and Claude checked every step. The tests prove the wiring; only the "
    "captures show the look.",
    "BrutalistHesitantWriter",
    {"text": "Claude wrote my\nfirst shaders.", "triggerWords": "Claude wrote",
     "replacementWords": "I wrote and Claude checked", "fontSize": 104, "lineSpacing": 1.4, "align": "center",
     "seed": "walker-survival-shooting-a5", "mistakeRate": 2, "hesitateWithin": 0, "hesitateBetween": 1,
     "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"},
    [("0.0", "typing starts"), ("0.3", "'Claude wrote' typed, marked"), ("0.45", "corrected to 'I wrote and "
     "Claude checked'"), ("0.8", "sentence settles")],
    lead_silence_s=0.8,
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer typing bookend; mostly page by design."},
    role_note="EXECUTIVE-SUMMARY LAW. Correction = the likely misconception (the AI wrote the shaders). "
              "Wording is a draft for the user to approve."))

# -- B02 the game, the state, the object ---------------------------------------------------------
BEATS.append(figure("B02",
    "The game: a survivor in a subway base, with a rugged tablet. The first shader shows one piece of state: is "
    "the tablet in use? Its screen glows only once the tablet reaches the hand. The second shader, with textures, "
    "goes on the base's two weapon crates.",
    "The game, the state, the object", "Native Godot render, 3840x2160 · the two weapon crates · film camera",
    "fig_pair.png", "figures/fig_pair.png", f"{SRC} · captures/crate/pair.png (the tablet is shown in B06)",
    [{"label": "State", "text": "Humanoid._tablet_hold: NONE, ONE_HAND, TWO_HAND"},
     {"label": "Shader 1", "text": "pad_base_light.gdshader on the tablet Screen"},
     {"label": "Shader 2", "text": "crate_wear.gdshader on crate_long, crate_cube"}],
    [("0.0", "the two crates"), ("0.4", "state card"), ("0.75", "object cards")],
    [(0.25, 0), (0.55, 1), (0.8, 2)], evidence=False))

# -- B03/B04 question 1: what a shader does ------------------------------------------------------
BEATS.append(workbench("B03",
    "Question one: what does a shader do? This is my whole screen shader, seven lines. The GPU runs fragment, on "
    "line five, for every pixel of the screen, all at once; each run has only its own local values and cannot see "
    "its neighbours. So the game's state comes in as a uniform, set from GDScript: pad light data, line four. Line six is the colour line from my specification, "
    "word for word: mix from black to cold white by that value.",
    "Question 1 · what a shader does", "shaders/pad_base_light.gdshader", 1, 7,
    [{"label": "Runs", "value": "fragment() once per pixel, in parallel"},
     {"label": "State in", "value": "uniform pad_light_data (line 4)"},
     {"label": "Colour line", "value": "= CHANGE-BRIEF line 39"}],
    ["Hand-written; line 1 from the editor's Empty template"],
    [("0.0", "Godot editor reconstruction of the whole shader"), ("0.3", "line 5 fragment()"),
     ("0.55", "line 4 uniform"), ("0.8", "line 6 colour line")],
    [(0.3, 5, "runs once per pixel"), (0.55, 4, "game state arrives as a uniform"),
     (0.8, 6, "the colour line from the spec")]))
BEATS.append(figure("B04",
    "My own in-engine captures, with the driver paused and the value set from code. At zero point three nine the "
    "screen reads one fifty-one, one sixty-two, one sixty-two, exactly my hand calculation, because the mix "
    "happens in linear light. At two point oh it is pure white: hint range limits the slider, not the code.",
    "Result · controlled values", "In-engine captures (get_viewport().get_texture()), 2048x1152, scaled up here",
    "fig_controlled.png", "figures/fig_controlled.png",
    f"{SRC} · submission captures/screen_pad_*_marked.png (my F9 captures) · TEST-REPORT section 4",
    [{"label": "Difference", "text": "0 on every channel, P1 and P2"},
     {"label": "0.39", "text": "151, 162, 162 — not 230 x 0.39"},
     {"label": "2.0", "text": "255, 255, 255: hint_range does not clamp code"}],
    [("0.0", "four captures"), ("0.35", "0.39 tile"), ("0.75", "2.0 tile")], [(0.2, 0), (0.45, 1), (0.8, 2)]))

# -- B05/B06 the driver --------------------------------------------------------------------------
BEATS.append(workbench("B05",
    "The driver, which I wrote in the humanoid body. Every physics frame it asks two things. Is the tablet put "
    "away? Then the screen is off, at once. Has the tablet's move reached the hand? Only then is it on. In between, "
    "it keeps the last answer, so switching hands never flickers.",
    "The driver · humanoid.gd", "characters/human/humanoid/humanoid.gd", 137, 142,
    [{"label": "Called", "value": "every physics frame, from _update_tablet_visual()"},
     {"label": "Reads", "value": "_tablet_hold, _tablet_move_progress"},
     {"label": "Never writes", "value": "the tablet state (presentation only)"}],
    ["Written by me"],
    [("0.0", "reconstruction of lines 137–142"), ("0.3", "NONE → off"), ("0.55", "arrived → on"),
     ("0.8", "otherwise keep")],
    [(0.3, 138, "put away: off at once"), (0.55, 140, "arrived in the hand: on"),
     (0.8, 142, "hand the answer to the tablet")]))
BEATS.append(beat("B06", "RESULT",
    "Here it is in the game, driven by scripted Tab key presses. Out to one hand: dark while it moves, lit as it "
    "arrives. Up to two hands: no flicker. Put away: dark at once. Out and straight back: never lit.",
    None, None, [("0.0", "labeled native 4K capture"), ("0.12", "one hand, lit on arrival"),
                 ("0.35", "two hands"), ("0.55", "put away, dark"), ("0.75", "out and back, never lit")],
    role_note="Real native-4K engine footage, scripted input (captures/tablet-run-02). Label burned in by "
              "scripts/prepare_media.py. No retiming; a labeled final-frame hold only if narration is longer.",
    qc={"full_bleed": True, "contrast_regions": [{"label": "burned-in disclosure label",
                                                   "box": [0.02, 0.935, 0.98, 0.995]}],
        "contrast_reason": "Edge-to-edge native Godot render; the only essential text is the label strip."}))
BEATS[-1]["shot"] = {"type": "SCREEN", "class": "SHOW", "source": "own", "evidence_media": "media/B06.mp4",
                     "show": BEATS[-1]["shot"]["show"]}

# -- B07/B08 the tablet writes only its own material -----------------------------------------------
BEATS.append(workbench("B07",
    "The tablet does the writing. Set screen lit picks the strength, zero point three nine from an exported "
    "variable, and writes it into this tablet's own material. The material is local to scene, so every tablet "
    "gets a copy, and one player's screen cannot light another's.",
    "Writing the uniform · tablet_device.gd", "items/tablet/tablet_device.gd", 42, 48,
    [{"label": "Value", "value": "light_strength_percentage = 0.39 (@export)"},
     {"label": "Material", "value": "ShaderMaterial, Local To Scene"},
     {"label": "Written by", "value": "Claude, at my request"}],
    ["set_screen_lit() written by Claude at my request"],
    [("0.0", "reconstruction of set_screen_lit()"), ("0.4", "strength"), ("0.75", "set_shader_parameter")],
    [(0.35, 46, "0.39 or 0"), (0.7, 48, "this tablet's material only")]))
BEATS.append(figure("B08",
    "The headless test drives the same path with real key events at thirty, sixty and a hundred and forty-four "
    "frames per second. Lit after zero point three five seconds of game time, within one frame. And the second "
    "body's screen stayed at zero on every frame.",
    "Result · the driver at three frame rates", "Recorded test output, copied verbatim",
    "fig_log_screen.png", "figures/fig_log_screen.png",
    f"{SRC} · logs/screen_glow_check_{{30,60,144}}fps_final.log · tests/screen_glow_check.gd",
    [{"label": "Lit after", "text": "0.3667 / 0.3500 / 0.3500 s"},
     {"label": "Second body", "text": "0.0 on 286 / 546 / 1296 frames"},
     {"label": "Result", "text": "24 PASS at each rate, exit 0"}],
    [("0.0", "three logs"), ("0.4", "lit timing"), ("0.75", "second body")], [(0.25, 0), (0.6, 1), (0.85, 2)]))

# -- B09/B10 question 2: material vs shader -------------------------------------------------------
BEATS.append(workbench("B09",
    "Question two: how is a material different from a shader? The defaults are written in the shader; the "
    "current values live in the ShaderMaterial, and two objects that share a material share its values. This is the long crate's "
    "material: the same shader, the same two textures, and only two values of its own: wear zero point two, "
    "roughness zero point nine five.",
    "Question 2 · material vs shader", "assets/furniture/materials/crate_long_wear.tres", 1, 13,
    [{"label": "Shader", "value": "res://shaders/crate_wear.gdshader (line 3)"},
     {"label": "Stored", "value": "paint_roughness 0.95, wear_amount 0.2"},
     {"label": "Other material", "value": "crate_cube_wear.tres: 0.85, 0.1"}],
    ["Wired through each .glb's Use External import setting"],
    [("0.0", "reconstruction of the .tres"), ("0.3", "shader path"), ("0.75", "two stored values")],
    [(0.3, 3, "points at the shader"), (0.75, 12, "only these values are its own")]))
BEATS.append(figure("B10",
    "One shader, two materials. The long crate is more worn and duller than the small one, because I decided "
    "it gets dragged around more. The textures and the scale are the same: it is the same sheet metal.",
    "Result · one shader, two materials", "Native Godot render, 3840x2160 · base.tscn unchanged · film camera",
    "fig_pair.png", "figures/fig_pair.png", f"{SRC} · captures/crate/pair.png · scripts crate_capture.gd",
    [{"label": "crate_long", "text": "wear 0.2, roughness 0.95"},
     {"label": "crate_cube", "text": "wear 0.1, roughness 0.85"},
     {"label": "Lighting", "text": "base.tscn's own ceiling lights"}],
    [("0.0", "both crates"), ("0.4", "long crate card"), ("0.7", "small crate card")],
    [(0.3, 0), (0.55, 1), (0.85, 2)]))

# -- B11/B12 question 3: a texture is information -------------------------------------------------
BEATS.append(workbench("B11",
    "Question three: why is a texture information, not a picture? Line thirty-six reads a height map, but nobody "
    "sees it. Its red channel is a number, and line thirty-eight compares it with wear amount: the low places "
    "turn to rust first. Only the rust texture on line thirty-five is a colour.",
    "Question 3 · a texture is information", "shaders/crate_wear.gdshader", 34, 42,
    [{"label": "Colour", "value": "rust_albedo (line 35): source_color"},
     {"label": "Data", "value": "wear_mask (line 36): height, no source_color"},
     {"label": "Rule", "value": "lower than wear_amount → rust"}],
    ["Metal041C (ambientCG, CC0): Color = rust, Displacement = mask"],
    [("0.0", "reconstruction of fragment()"), ("0.3", "line 36 height"), ("0.55", "line 38 compare"),
     ("0.8", "lines 40–41 mix")],
    [(0.3, 36, "a height, read as a number"), (0.55, 38, "low places first"), (0.85, 40, "paint or rust")]))
BEATS.append(figure("B12",
    "Drag wear amount and the mask decides where. At zero there is no rust. At my default, about one tenth of the "
    "surface. At one, all of it. The pattern never moves; only the threshold does.",
    "Result · the mask decides where", "Native Godot renders, 3840x2160 · value set at runtime, not saved",
    "fig_wear.png", "figures/fig_wear.png", f"{SRC} · captures/crate/crate_cube_wear_amount_*.png",
    [{"label": "0.0", "text": "all paint"}, {"label": "0.1", "text": "about 10 percent rust (9.8 measured on mask)"},
     {"label": "1.0", "text": "all rust"}],
    [("0.0", "three captures"), ("0.3", "0.0"), ("0.55", "0.1"), ("0.8", "1.0")], [(0.3, 0), (0.55, 1), (0.8, 2)]))

# -- B13/B14 vertex(): box projection -----------------------------------------------------------
BEATS.append(workbench("B13",
    "The long crate has no UVs at all, and I could not change the model. So vertex makes them. It reads the "
    "normal, picks the two axes the face does not point along, and uses the vertex position there, times texture "
    "scale. Object space, so the rust moves with the crate.",
    "vertex() · making UVs from the box", "shaders/crate_wear.gdshader", 22, 32,
    [{"label": "Why", "value": "crate_long.glb has no UV; crate_cube's lid has none"},
     {"label": "Holds because", "value": "all 336 normals point along X, Y or Z"},
     {"label": "Cost", "value": "no tangents, so no normal map on the crates"}],
    ["Box projection proposed by Claude; written by me"],
    [("0.0", "reconstruction of vertex()"), ("0.3", "normal test"), ("0.6", "VERTEX components"),
     ("0.85", "texture_scale")],
    [(0.3, 23, "which way does the face point?"), (0.6, 24, "the other two axes become UV"),
     (0.85, 31, "times texture_scale")]))
BEATS.append(figure("B14",
    "Texture scale is repeats per metre. At zero point one the rust becomes big blotches; at ten it is fine "
    "speckle. My default, two, gives patches of roughly twelve to sixteen centimetres.",
    "Result · texture_scale", "Native Godot renders, 3840x2160 · value set at runtime, not saved",
    "fig_scale.png", "figures/fig_scale.png", f"{SRC} · captures/crate/crate_cube_texture_scale_*.png",
    [{"label": "0.1", "text": "large blotches"}, {"label": "2.0", "text": "default"},
     {"label": "10.0", "text": "fine speckle"}],
    [("0.0", "three captures"), ("0.3", "0.1"), ("0.55", "2.0"), ("0.8", "10.0")], [(0.3, 0), (0.55, 1), (0.8, 2)]))

# -- B15/B16 question 4: the Godot shading language ------------------------------------------------
BEATS.append(workbench("B15",
    "Question four: what is the Godot shading language? It is close to GLSL, with things GLSL leaves to you. "
    "Group uniforms and hints turn these lines into an Inspector panel, three groups, five values. And it hands "
    "you material outputs, albedo and roughness, that Godot's own lighting finishes.",
    "Question 4 · the Godot shading language", "shaders/crate_wear.gdshader", 1, 20,
    [{"label": "Groups", "value": "paint, wear, mapping (lines 6, 10, 14)"},
     {"label": "Hints", "value": "source_color, hint_range (lines 7–15)"},
     {"label": "Outputs", "value": "ALBEDO, ROUGHNESS (lines 40–41)"}],
    ["Not unshaded: the base's lights shade the crates"],
    [("0.0", "reconstruction of the interface"), ("0.3", "group_uniforms"), ("0.6", "hints"),
     ("0.85", "constants")],
    [(0.3, 6, "group_uniforms: an Inspector group"), (0.6, 11, "hint_range: a slider"),
     (0.85, 19, "rust roughness is a constant")]))
BEATS.append(figure("B16",
    "The sweep, every value at its minimum, default and maximum. Paint colour swaps the paint and leaves the rust. "
    "Roughness only shows from a highlight angle. And at maximum softness the hard paint edge blurs.",
    "Result · the interface sweep", "Native Godot renders, 3840x2160 · rows 2–3 cropped from a highlight angle",
    "fig_interface.png", "figures/fig_interface.png",
    f"{SRC} · captures/crate/, captures/crate-glint/ (crate_cube; values set at runtime)",
    [{"label": "paint_color", "text": "black / olive / white"},
     {"label": "paint_roughness", "text": "0 / 0.85 / 1, seen in the highlight"},
     {"label": "wear_softness", "text": "0 / 0.2: hard edge vs blur"}],
    [("0.0", "sweep grid"), ("0.3", "colour row"), ("0.55", "roughness row"), ("0.8", "softness row")],
    [(0.25, 0), (0.5, 1), (0.8, 2)],
    role_note="The judgments on the look (which setting breaks it) are the user's; narration states only "
              "what changed."))

# -- B17/B18 the hint experiment -----------------------------------------------------------------
BEATS.append(workbench("B17",
    "The hint experiment. One three-by-one grey PNG, sampled twice. Line four says source colour; line five does "
    "not. That is the only difference. I predicted the numbers by hand before running it.",
    "The hint experiment", "shaders/hint_experiment.gdshader", 1, 14,
    [{"label": "File", "value": "hint_greys_3x1.png: 64, 128, 192"},
     {"label": "Predicted", "value": "with: 64/128/192 · without: 137/188/225"},
     {"label": "Scene", "value": "unshaded quads, Linear tonemap, exposure 1.0"}],
    ["Hand-written; the PNG was written by a Claude script"],
    [("0.0", "reconstruction of the shader"), ("0.35", "line 4"), ("0.6", "line 5"), ("0.85", "bool")],
    [(0.35, 4, "source_color"), (0.6, 5, "no source_color"), (0.85, 9, "a bool picks one")]))
BEATS.append(figure("B18",
    "Measured on a real render: sixty-four, one twenty-eight, one ninety-two with the hint. A hundred and "
    "thirty-seven, one eighty-eight, two twenty-five without. Every band matches. With the hint, decode and "
    "encode cancel; without it, the file's numbers are taken as light and come out brighter.",
    "Result · predicted vs measured", "Native Godot render, 3840x2160, scene unchanged",
    "fig_hint.png", "figures/fig_hint.png", f"{SRC} · captures/hint/hint_4k_3840x2160.png · capture-tools/hint_capture.gd",
    [{"label": "With", "text": "64 · 128 · 192 (difference 0)"},
     {"label": "Without", "text": "137 · 188 · 225 (difference 0)"},
     {"label": "Read", "text": "band centres, 3x3 uniform; same at 1152x648"}],
    [("0.0", "both quads with numbers"), ("0.4", "with row"), ("0.7", "without row")], [(0.25, 0), (0.55, 1), (0.85, 2)]))

# -- B19/B20 generated shader, annotated line 1 ----------------------------------------------------
BEATS.append(workbench("B19",
    "Godot can write a shader too. I converted a standard material and annotated what it wrote. Line thirteen "
    "samples the albedo with source colour: my comment on line twelve says why. My crate's line three does the "
    "same for the rust.",
    "Generated shader · annotated line 13", "shaders/standard_generated.gdshader", 9, 13,
    [{"label": "Mine", "value": "crate_wear.gdshader line 3: rust_albedo : source_color"},
     {"label": "Comment", "value": "line 12, written by me"},
     {"label": "Generated by", "value": "Godot 4.7.2, from a StandardMaterial3D"}],
    ["Generated file committed unedited before my comments"],
    [("0.0", "reconstruction of lines 9–13"), ("0.4", "comment line 12"), ("0.75", "line 13")],
    [(0.4, 12, "my annotation"), (0.75, 13, "colour: source_color")]))
BEATS.append(figure("B20",
    "And what that hint does to my crate. In an isolated copy made for this film, I removed source colour from "
    "line three. The rust turns pale and washed out: the colour texture is read as if it were already linear.",
    "Result · without source_color", "Native Godot renders · right: film-only mutated copy, not the project",
    "fig_mutation.png", "figures/fig_mutation.png",
    f"{SRC} · captures/crate-glint-wear/, captures/mutation-source-color/ (same camera, wear 0.1)",
    [{"label": "Left", "text": "line 3 as committed"},
     {"label": "Right", "text": "source_color deleted in a film-only copy"},
     {"label": "Predicted", "text": "CHANGE-BRIEF failure 8: paler, washed out"}],
    [("0.0", "side by side, small crate only"), ("0.5", "pale rust"), ("0.8", "prediction card")],
    [(0.25, 0), (0.5, 1), (0.8, 2)]))

# -- B21/B22 generated shader, annotated line 2 ----------------------------------------------------
BEATS.append(workbench("B21",
    "The second annotated line: forty-two. The normal map has no source colour, because it stores directions, "
    "not colours. My crate's line four, the wear mask, leaves it off for the same reason.",
    "Generated shader · annotated line 42", "shaders/standard_generated.gdshader", 40, 45,
    [{"label": "Mine", "value": "crate_wear.gdshader line 4: wear_mask, no source_color"},
     {"label": "Comment", "value": "lines 40–41, written by me"},
     {"label": "Not the reason", "value": "hint_roughness_normal does not decode colour"}],
    ["Data textures keep their numbers"],
    [("0.0", "reconstruction of lines 40–45"), ("0.4", "comment"), ("0.7", "line 42")],
    [(0.4, 40, "my annotation"), (0.7, 42, "data: no source_color")]))
BEATS.append(figure("B22",
    "Directions can be checked. The curl ratio is low when a normal map is read in its own convention and near "
    "two in the wrong one. The GL map scores zero point two in GL and one point eight in DirectX, and its "
    "DirectX twin the other way round. No flip needed.",
    "Result · the normal map is data", "Recorded test output, copied verbatim",
    "fig_log_normal.png", "figures/fig_log_normal.png", f"{SRC} · logs/normal_map_check_60fps_final.log",
    [{"label": "NormalGL", "text": "0.1991 GL · 1.8009 DX"}, {"label": "NormalDX", "text": "1.8009 GL · 0.1991 DX"},
     {"label": "Used", "text": "only in the Step 4 material"}],
    [("0.0", "log lines"), ("0.4", "GL"), ("0.7", "DX")], [(0.3, 0), (0.6, 1), (0.85, 2)]))

# -- B23/B24 what the tests proved ----------------------------------------------------------------
BEATS.append(workbench("B23",
    "What the tests prove. This check, written in the audit, reads every sampler's hints straight from the "
    "shader source and compares them with the plan. Nothing renders; it reads text.",
    "Tests · test_materials.gd", "tests/test_materials.gd", 208, 223,
    [{"label": "Suite", "value": "169 checks: materials, hints, imports, Use External"},
     {"label": "Fresh import", "value": "169 PASS after deleting .godot/"},
     {"label": "Written by", "value": "a separate Claude Code audit session"}],
    ["Reads source text; renders nothing"],
    [("0.0", "reconstruction of the check"), ("0.4", "regex"), ("0.75", "compare")],
    [(0.4, 210, "find every sampler2D"), (0.75, 221, "hints must match the plan")]))
BEATS.append(figure("B24",
    "So I broke it on purpose. With source colour deleted, the suite fails, exit code one. The screen shader's "
    "mutations failed too: a missing semicolon, and a renamed uniform. The rename is the sneaky one: the shader "
    "still compiles, and only the uniform-list check notices.",
    "Result · the mutations fail", "Recorded test output, copied verbatim",
    "fig_log_mutation.png", "figures/fig_log_mutation.png",
    f"{SRC} · logs/mutation_source_color_60fps.log · TEST-REPORT section 2",
    [{"label": "source_color", "text": "168 PASS, 1 FAIL, exit 1"},
     {"label": "semicolon", "text": "SHADER ERROR, 3 FAIL, exit 1"},
     {"label": "rename", "text": "no error; 3 FAIL, exit 1"}],
    [("0.0", "failing line"), ("0.4", "source_color"), ("0.7", "screen mutations")], [(0.25, 0), (0.5, 1), (0.8, 2)]))

# -- B25 what no headless run can show -------------------------------------------------------------
BEATS.append(beat("B25", "LIMITS",
    "And what no headless run can show: whether any of it looks right. The tests read source, import settings and "
    "values written to materials. The colours, the rust, the highlight: those are captures, and a person "
    "looking. One known limit: the shader never writes metallic, so the silver scratches are shaded as paint.",
    "GodotDesignFigure",
    {"title": "What the tests cannot prove", "status": "TEST-REPORT section 6 · MATERIALS.md section 6",
     "image": f"{PUB}/fig_pair.png", "imageLabel": "figures/fig_pair.png", "excerpt": "",
     "source": f"{SRC} · TEST-REPORT, MATERIALS.md",
     "cards": [{"label": "Proved", "text": "parse, uniforms, values, hints, imports, wiring"},
               {"label": "Not proved", "text": "how anything looks on screen"},
               {"label": "Known limit", "text": "no METALLIC: scratches shade as paint"}]},
    [("0.0", "the crates again"), ("0.4", "proved"), ("0.65", "not proved"), ("0.85", "known limit")],
    [(0.2, 0), (0.45, 1), (0.8, 2)]))

# -- B26 verdict ----------------------------------------------------------------------------------
BEATS.append(beat("B26", "VERDICT",
    "Verdict. Built: two shaders I wrote, a driver, two materials, and a hint experiment that matched to the "
    "pixel. Caught: Claude's first test had three bugs; its audit misnamed an import option and cited a setting "
    "that is not in the file; it once compared numbers from two different runs. Textures: ambient C G, "
    f"Metal zero four one C, C C zero. Still uncertain: {UNCERTAIN}. Next: {NEXT_STEP}.",
    "ClaudeVerdictArtifact",
    {"artifactTitle": "Verdict", "artifactHeading": f"Walker Survival Shooting at {REV}.",
     "brandLabel": "@NikBearBrown",
     "artifactLines": ["Built: 2 hand-written shaders, a driver, 2 materials, the hint experiment.",
                       "Caught: test bugs, a misnamed import option, a mixed-up comparison.",
                       "Human: the decisions, the specs, both shaders. Claude: tests, tools, checks.",
                       "Textures: ambientCG Metal041C, CC0.",
                       f"Uncertain: sRGB decode, curl 0.2 not 0, hint_roughness_normal  ·  Next: tablet UI on the screen via SubViewport"]},
    [("0.0", "verdict page"), ("0.2", "built"), ("0.45", "caught"), ("0.7", "textures"), ("0.85", "next")]))

# -- B27 your turn --------------------------------------------------------------------------------
YT = ("Please use Walker on my Godot project. Read my CHANGE-BRIEF and shaders/crate_wear.gdshader. Add a metal "
      "mask so the bare-metal scratches write METALLIC, as a new uniform with a hint and a default. Before you "
      "change anything, predict which pixels of my crate capture will change, then capture again and compare.")
BEATS.append(beat("B27", "HANDOFF",
    "Your turn. Paste this into Claude. " + YT.replace("shaders/crate_wear.gdshader", "my crate shader")
    .replace("CHANGE-BRIEF", "change brief").replace("METALLIC", "metallic") +
    " The prediction is the point. Write down where the change should show before you look. This was Liam, "
    "narrating for Jonathan.",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "GODOT · GAMEDEV · WALKER", "segment": "Walker Survival Shooting",
     "command": YT, "runningText": "paste this into Claude…", "output": [], "modelLabel": "Opus 5.5",
     "largeText": True},
    [("0.02", "composer 'Your turn.'"), ("0.1", "prompt types in"), ("0.7", "send arms"), ("0.9", "sign-off")],
    role_note="HANDOFF LAW: prompt read aloud verbatim, then discussed; Liam signs off here. Draft: the user "
              "approves the experiment."))

# -- B28 locked outro -----------------------------------------------------------------------------
BEATS.append({"beat_id": "B28", "act": "OUTRO", "kind": "outro_voice",
    "narration_text": "claude liam, walker survival shooting, a five, gamedev. At Nik Bear Brown.",
    "title_spoken_note": "TTS-friendly reading of the exact title claude-liam-walker-survival-shooting-a5-gamedev", "voice": "am_onyx", "engine": "kokoro",
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
    "channel": "@NikBearBrown", "folderLabel": "@NikBearBrown", "persona": "Liam (narrating for Jonathan)", "in_for_bear": False,
    "greeting": GREETING, "greeting_note": "chosen by the user: Hola; narrator line chosen by the user.",
    "game": {"name": "walker-survival-shooting", "source_revision": REV,
             "engine": "Godot 4.7.2.stable.official.ed1daf0bf", "game_path": f"walker-survival-shooting/godot ({REV})"},
    "note": "godot-gamedev walker film for Assignment 5 (shaders, materials and the Godot shading language). "
            "Engine images are native 4K renders of the unmodified project through capture scripts that add a film "
            "camera, set shader values at runtime, or send scripted Tab/mouse input; one figure uses a film-only "
            "mutated copy and is labeled. The controlled-value captures are the user's own in-engine captures at "
            "2048x1152. No game change, no commit, no push, no publication.",
}


def write(sheet):
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=True) + "\n", encoding="ascii")


def sync():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    for b in sheet["beats"]:
        if b["beat_id"] == "B06":                      # real footage: the clip's own length, no retiming
            b["render_duration_s"] = 391 / 30
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


def tbd():
    text = json.dumps({"metadata": METADATA, "beats": BEATS}, ensure_ascii=False)
    found = sorted(set(re.findall(r"\[TB[DC][^\]]*\]", text)))
    pending = [b["beat_id"] for b in BEATS if "EXCERPT PENDING" in json.dumps(b)]
    print("TBD values:", found or "none")
    print("Excerpts pending the English source:", pending or "none")
    return 1 if found or pending else 0


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
