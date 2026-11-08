"""Author the A6 particle film (beat sheet + source ledger) from exact excerpts.

    python tools/film.py author   # writes beat_sheet.json (resets measured fields!)
    python tools/film.py ledger   # writes gamedev-evidence.json (after media exist)

Every code excerpt is read from the game folder at the given line range; the
checker (art godot-gamedev --check) compares it with the file again.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1]
TITLE = "Downfall: Sparks, Flames and Particle Evidence"
CURVE_NOTE = "Source notes — not Inspector values"

# beat -> (path, start, end, title, notes, font)
EXCERPTS = {
    "B02": ("entities/player.gd", 948, 954, "Effect A: The Landed Hit",
            [("Event", "a landed melee hit: player.gd 915, 977, 1784"), ("Retrigger rule", "overlap: a new HitSpark per hit,\nchild of GameManager, never the enemy")], 34),
    "B04": ("entities/fire_pit.gd", 104, 110, "Effect B: Fuel Drives The Fire",
            [("Value", "burn_left, 0–300 s of fuel"), ("Mapping", "emitting = burn_left > 0\nratio = 0.3 + 0.7 · clamp(burn_left / 120)")], 30),
    "B06": ("CHANGE-BRIEF.md", 52, 63, "Effect A: The Intent Block",
            [("Written", "before any build prompt"), ("Phases", "impact → throw → settle → clear")], 23),
    "B08": ("effects/hit_spark.tscn", 177, 191, "Emission: When And How Many",
            [("Part", "EMISSION"), ("Sparks", "amount 14, one_shot,\nexplosiveness 1.0: all leave on one frame")], 26),
    "B10": ("effects/hit_spark.tscn", 79, 95, "Process: What Happens Over Life",
            [("Part", "PROCESS"), ("Sparks", "speed 3–6, gravity −9.8,\ndamping 6–10, ramp white → orange → red")], 25),
    "B12": ("effects/hit_spark.tscn", 145, 152, "Draw: How Each Particle Looks",
            [("Part", "DRAW"), ("Puff", "blend_mode 0 = MIX: a dark smudge\nunshaded, billboarded, vertex colour")], 32),
    "B13a": ("effects/hit_spark.tscn", 154, 156, "Effect A Revision r1: One Quad Size",
            [("Before (r0)", "Puff QuadMesh 0.5 × 0.5"), ("After (r1)", "1.0 × 1.0 — one setting")], 40),
    "B14": ("CHANGE-BRIEF.md", 205, 212, "Effect B: The Intent Block",
            [("Written", "before any build prompt"), ("Phases", "lighting → steady → dwindling → out")], 23),
    "B16": ("effects/fire_pit_flames.tscn", 59, 61, "The Kept Change: One Quad Size",
            [("Before (r0b)", "Flames QuadMesh 0.30 × 0.30"), ("After (r1, kept)", "0.55 × 0.55 — one setting")], 40),
    "B18": ("effects/fire_pit_flames.tscn", 113, 125, "What Effect A Doesn't Use",
            [("Continuous", "one_shot false, explosiveness 0"), ("Feedback + preprocess", "amount_ratio driven by burn_left\npreprocess 0.8 s: full on first frame")], 28),
    "B20": ("effects/fire_pit_flames.tscn", 44, 48, "Turbulence: The Sideways Waver",
            [("Feature", "turbulence (GPU only in this brief)"), ("Flames", "influence 0.05–0.12; embers 0.15–0.30")], 36),
    "B22": ("shaders/particles_generated.gdshader", 138, 140, "Generated Process Shader: Velocity",
            [("Line 140 ↔ brief", "Sparks initial_velocity_min–max\n3.0–6.0"), ("Status", "reference only; no game material uses it")], 26),
    "B24": ("shaders/particles_generated.gdshader", 159, 164, "Generated Process Shader: Colour Over Life",
            [("Line 162 ↔ brief", "colour ramp white → orange → red"), ("Line 161 ↔ brief", "scale curve 1 → 0")], 28),
    "B26": ("shaders/particles_generated.gdshader", 235, 238, "Generated Process Shader: Amount Ratio",
            [("Line 236 ↔ fire_pit.gd", "amount_ratio mapping"), ("Effect", "skip a particle at spawn;\nbuffer never reallocated")], 34),
    "B28": ("tests/test_hit_spark_config.gd", 118, 120, "Config Tests Read Every Value Back",
            [("Effect A", "165 checks"), ("Effect B", "123 checks\nexpected values = the brief's table")], 23),
    "B30": ("tests/cost_effects.gd", 276, 287, "Price: Is The Instrument Honest?",
            [("Control", "empty scene, a bare Node"), ("Headless", "dummy renderer: no particle\nprocess, nothing drawn")], 23),
}

N = {}  # narration
N["B00"] = "Jambo. This is Liam, in for Bear. Today it's Downfall, the walker-downfall Godot game, and its Assignment Six particle work: a hit spark that bursts when an operator's melee blow lands, and fire pit flames whose size follows the fuel that's left. We read each setting, then watch what it does on screen."
N["B01"] = "A particle effect is a message. Each burst answers one game event. The settings live in scene files, where a test can read them back. And the eyes that decide whether it reads belong to the player, not the agent."
N["B02"] = "Effect A is hit spark. Three call sites in the player script run this function after a melee blow lands: the basic combo hit, Lappland's cross cut, and Amiya's combo cut. Each call instances a fresh burst and parents it to the Game Manager, at the struck enemy's position. Never to the enemy, so a killing blow can't take it along."
N["B03"] = "Here it is in the real game loop, driven by scripted mouse input on fixture dummies, not by a human player. Amiya holds attack, and her cuts land a fraction of a second apart. Each landed cut adds its own burst on top of one still settling: that's the overlap rule. Then a one health dummy dies on the blow, and its burst still plays out."
N["B04"] = "Effect B is fire pit flames, a feedback loop. The pit owns one number, burn left, the seconds of fuel remaining. This function only reads it. Emitting is burn left above zero. Amount ratio is full above a hundred twenty seconds and thins to thirty percent at the last second. Amount itself is never written, because that would restart the buffer."
N["B05"] = "This is the fire preview fixture on the snow floor, cycling through its fuel values. Fed from cold, the fire is full almost at once. When fuel drops to twenty four seconds, the flames thin without a gap. At zero, emission stops and the flames already alive finish. At default zoom the whole fire is a few dozen pixels, so the crop on the right is enlarged."
N["B06"] = "Before any code, the brief wrote the intent in time. Impact on frame zero: one white hot flash. Throw, to about a tenth of a second: ten to eighteen sparks flying outward. Settle, to about a third of a second: damping brakes them, they turn orange then red, droop and shrink, while a dark puff fades. Clear, by under half a second."
N["B07"] = "Strip r zero is a fixture capture: the real city floor, a stand in enemy, a fixed particle seed, and bursts fired at frames ten and sixteen. The flash is there on the trigger frame, with no one frame lag. By frame fifteen it's gone. Frame twenty carries the second burst. Frames thirty and fifty are empty, and the log counts zero hit spark nodes."
N["B08"] = "Now the three parts of any particle system. Emission decides when and how many. On the Sparks node: fourteen particles, one shot, explosiveness one, so all fourteen leave on the same frame, each living about a third of a second, with forty percent randomness. Local coords is false: once a spark is out, it belongs to the world."
N["B09"] = "Here are those frames enlarged. Claude's reading of the stills was that the sparks looked too small and travelled too little to read as an outward throw. The user ran the same preview, in motion, and answered: I can see it splashing outward. The user's verdict stood, and nothing was changed on Claude's reading."
N["B10"] = "Process decides what each particle does over its life. A sphere of radius point one, a full hundred eighty degree spread, starting speed three to six units a second, gravity pulling down, and damping of six to ten braking them hard. The scale curve and colour ramp shrink each spark and walk it from white, through orange, to transparent red."
N["B11"] = "This is a new fixture capture of the looping preview, in motion, with an enlarged crop beside it. Two bursts fire six frames apart, then the pair repeats every three seconds. Watch the sparks leave the centre, slow hard, and darken. This is what the user judged, and it's why a still strip can't settle a question about motion."
N["B12"] = "Draw decides what each particle looks like. The Puff's material is unshaded and billboarded, takes its colour from the vertex colour the process step writes, and uses a soft radial gradient defined inside the scene. Blend mode zero is mix, not add. Additive light adds almost nothing to white snow, so this layer exists to darken it."
N["B13"] = "On the snow strip, r zero, the flash and sparks read mostly over the stand in's dark body, and the puff barely shows. A snow patch just below measured one fifty eight point three on every frame: the puff never reached the snow. The user's words: barely see a little. Claude's arithmetic: a half unit quad stays inside the body's outline."
N["B13a"] = "Claude proposed one setting: the Puff quad, from half a unit to one unit, and committed the prediction before any edit. The patch below should darken by at least eight levels on frames fifteen and twenty, and the city strip should barely change. The user first said: don't change. Later the same day, the user approved it."
N["B13b"] = "Strips r one and r one snow: same seeds, same stand ins. The snow patch below the body still read one fifty eight point three on frames fifteen and twenty. The predicted darkening didn't happen: a miss. What changed stayed inside the body, a larger, darker haze over the torso. The puff fades as it grows, so its wide edge is nearly transparent. The user watched it run and said: keep."
N["B14"] = "Effect B's intent has four phases. Lighting: fed from cold, the flames are full on the next frame, because a freezing player cares about that moment. Steady: flames lick up and waver sideways, embers wander for about two seconds. Dwindling: below a hundred twenty seconds of fuel, the flames thin. Out: emission stops, and the fire dies rather than blinking off."
N["B15"] = "The first fire strip, r zero, showed a small tuft. The user said it was blocked by the stones. Claude blamed the emitter's height inside the pit model and wrote a prediction. The user's screenshot showed level boulders covering the pit. The real fault was the fixture: runs placed pits differently. Seeding every random stream and choosing an open pit produced strip r zero b."
N["B16"] = "On r zero b, the user said the fire looked smothered in the wood and should be bigger. Claude proposed one setting: the flame quad, from point three zero to point five five. The user approved it. The prediction came first: at least twice the warm pixels on the full fire frames, and the top at least five pixels higher."
N["B17"] = "Before and after: same seed, same fixture. Warm pixels on the full fire frames went from about seventy to about one sixty five, two point two to two point eight times. That part matched. The top rose only two or three pixels, not five: a miss. Height comes from speed and lifetime; a bigger quad mostly thickens the core. The user's verdict on the running preview: keep."
N["B18"] = "Effect B uses three things Effect A doesn't. Continuous emission instead of one shot. Preprocess of point eight seconds, so a fire lit from cold is simulated ahead and drawn full at once. And amount ratio, which the pit drives from the fuel left. In this engine version, CPU particles have no amount ratio, which is why the fire moved to the GPU."
N["B19"] = "A new fixture capture, labelled on screen, drives the real pit through each state. Fed: full at once. Tree paused: the flames freeze in place. Running again, then the effect hidden, and shown at the current ratio. Burned to twenty four seconds: thinner. Burned to zero: emission stops and the live flames finish. The headless state test asserts the same rules as numbers."
N["B20"] = "The fourth feature is turbulence, a noise field that pushes each flame sideways while it rises. Strength one, noise scale two point five, and a small influence of five to twelve percent, so the flames waver without blowing apart. The embers get more influence, so they wander as they climb."
N["B21"] = "Compare three full fire frames from strip r one. Same seed, same ratio, but the flame stack leans and spreads differently each time: that's the turbulence moving it. The embers, though, are five hundredths of a unit, about one and a half pixels, and they barely show at default zoom. That stays an open limitation."
N["B22"] = "Behind the process step is a generated particles shader. The user converted the Sparks process material in the editor and saved it, for reference; nothing in the game uses it. Line one forty picks each particle's starting speed between the min and max uniforms. That's where the brief's three to six lands."
N["B23"] = "So what if a Godot three name sneaks in? Writing initial velocity as a single float left the minimum at zero. The effect still fired, with no warning, and sparks started at zero to six instead of three to six. Only the config read back caught it. The Vector2 spelling passed, because this version still translates that old name."
N["B24"] = "Line one sixty two multiplies each particle's colour by the ramp, sampled at its age, and line one sixty one does the same with the scale curve. But the first conversion didn't contain these lines at all. That function held only its comment, and the emission shape was a point."
N["B25"] = "Here is the recorded difference. Attempt one was a stale default shader: no sphere radius, no colour ramp, no scale curve. The converter copies whatever the material last generated. The user toggled the emission shape to point and back to sphere, converted again, and got the complete shader. On screen, the ramp is what turns these sparks orange and then red."
N["B26"] = "Line two thirty six is why Effect B drives amount ratio. At spawn, each particle draws a random number; above the ratio, it simply stays inactive. The buffer of twenty four is never reallocated, so lowering the ratio thins the fire without a restart."
N["B27"] = "Strip r one: frame fifty four at full ratio, then frame seventy after the fuel drops to twenty four seconds, ratio point four four. Warm pixels fall from one sixty two to one hundred eight, with no blank frame between. Headless, the state test's monitor checked eleven thousand eight hundred forty six samples: the ratio matched the mapping every frame, and amount never changed."
N["B28"] = "The configuration tests load each scene and read every setting back against the brief's table: amounts, lifetimes, speeds, curves, ramp stops, quad sizes and blend modes. A value can only drift if someone changes the test along with it."
N["B29"] = "These are the recorded results. Config: one sixty five checks and one twenty three, zero failed. The Godot three float: exit one. The Vector2 spelling: passes. Damping drifted to four: exit one. State tests, headless, through real mouse and E key input: twenty two passes for Effect A, zero failures for Effect B. The full suite went from seventy eight of eighty nine to eighty two of ninety three; the same old failures remain."
N["B30"] = "Price, headless first. The cost script keeps an empty scene control, and checks that it isn't timing its own frame sleep. Headless runs a dummy renderer: the particle process shader never runs and nothing is drawn. Only node bookkeeping reaches the CPU, so a GPU effect's headless price should be close to zero."
N["B31"] = "And it is. The empty scene takes three microseconds and the game frame seven point seven milliseconds, so the instrument sees the scene. Eight live hit sparks add about two hundredths of a millisecond, give or take three; one pit and three pits tell the same story. None is distinguishable from effects off. And none of it says anything about the GPU."
N["B32"] = "For the GPU, the user ran the price fixture in the editor's Visual Profiler on an RTX forty sixty laptop. The Update GPU Particles row appears only while these effects run. Effect A at its peak: point one four milliseconds, against a budget of point two five. Effect B, three pits full: point oh nine, against point one five. Inside budget, but two to three times the prediction. These readings predate the puff change, and the draw step was not isolated."
N["B33"] = "Who did what. Claude wrote the brief, every prediction and strip reading, the fixtures, the documents and commits; delegated agent sessions built the effects and tests, because the claude command line tool isn't installed on this machine. The user chose the effects and gave every runtime verdict, every tuning decision, the editor conversion and the GPU readings. No textures were sourced: the gradients and curves live inside the scenes."
N["B34"] = "The verdict. Both effects fire on their events, and the tests, strips and GPU readings agree. Each effect has one kept, user approved revision, and each prediction missed in part. The user caught the agent's mistakes: a wrong occlusion diagnosis, an unrepeatable fixture, and debug keys the editor already owns. Still uncertain: the draw step's GPU cost, the embers, and the boss arena fire on screen. Next step: make the embers readable, prediction first."
PROMPT = "Use Walker to tune one particle setting in my game. Name the event it answers, predict what a fixed-seed frame strip will show, capture before and after, and let me give the verdict while it runs."
N["B35"] = PROMPT + " Notice the last clause. The agent can read stills; you watch it move. Keep the prediction when it misses, the way the flame height did here. Liam, in for Bear."

RESULTS = {  # result beat -> visible sequence
    "B03": "Scripted-input capture: rapid Amiya cuts stack overlapping bursts; a killed dummy's burst plays out",
    "B05": "Fire preview loop: lit full, thinned at 24 s, out; enlarged crop",
    "B07": "Strip r0 (city), frames 10/12/15/20/30/50 against the intent phases",
    "B09": "Strip r0 crops enlarged; Claude's still reading beside the user's verdict",
    "B11": "New looping capture in motion with an enlarged crop: throw, brake, darken",
    "B13": "Strip r0-snow crops: the puff barely reaches the snow (158.3 on every frame)",
    "B13b": "r0-snow vs r1-snow and r0 vs r1 crops: prediction, measurement, the user's verdict",
    "B15": "Strip r0 under boulders, the user's screenshot, r0b in open snow",
    "B17": "r0b vs r1 crops with warm-pixel counts: prediction, match, miss, Keep",
    "B19": "New fixture capture: lit, tree paused, hidden/shown, thinned, out",
    "B21": "Strip r1 frames 12/40/54: turbulence changes the stack; embers barely visible",
    "B23": "Mutation M1: r0 frame 12 beside the mutated frame 12; the config FAIL line",
    "B25": "Attempt 1 vs attempt 2 recorded diff; r0 colour over life",
    "B27": "Strip r1 frame 54 vs 70; the state-test monitor line",
    "B29": "Recorded test, mutation and suite results",
    "B31": "Recorded headless cost table with its self-checks",
}


def excerpt(bid):
    path, start, end = EXCERPTS[bid][:3]
    return "\n".join((GAME / path).read_text(encoding="utf-8").splitlines()[start - 1:end])


def graphic(pattern, props, event):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "reveal",
            "show": [{"at": "0", "event": event}], "remotion": {"pattern": pattern, "props": props}}


def code(bid):
    path, start, end, title, notes, font = EXCERPTS[bid]
    return graphic("GodotDevWorkbench", {
        "mode": "code", "title": title, "project": "downfall-godot", "path": "res://" + path,
        "source": f"{path}:{start}-{end}", "code": excerpt(bid), "startLine": start, "codeFontSize": font,
        "inspectorLabel": CURVE_NOTE, "notes": [{"label": a, "value": b} for a, b in notes],
        "cues": [{"at": 1.0, "line": start, "label": title}, {"at": 7.0, "line": end, "label": notes[-1][1].replace("\n", " ")}]},
        f"Read {path} lines {start}-{end}, then watch the result in the next beat")


def media(bid, event, motion=False):
    return {"type": "GAMEPLAY" if motion else "GRAPHIC", "class": "SHOW", "source": "capture" if motion else "image",
            "evidence_media": f"media/{ID[bid]}.mp4", "show": [{"at": "0", "event": event}]}


MOTION = {"B03", "B05", "B11", "B19"}
ORDER = [f"B{i:02}" for i in range(14)] + ["B13a", "B13b"] + [f"B{i:02}" for i in range(14, 37)]
ID = {k: f"B{i:02}" for i, k in enumerate(ORDER)}


def author():
    beats = []

    def add(bid, shot, **kw):
        n = N.get(bid, "")
        beats.append({"beat_id": ID[bid], "film_key": bid, "act": kw.pop("act", "BODY"), "narration_text": n, "voice": "am_onyx",
                      "engine": "kokoro", "estimated_duration_s": max(8, len(n.split()) / 2.5), "shot": shot, **kw})

    add("B00", graphic("ClaudeComposerAsk", {
        "greeting": "Jambo, Liam", "topic": "GODOT GAMEDEV · ASSIGNMENT 6", "segment": "Sparks, Flames and Evidence",
        "command": "Please use Walker to convert my game design document about Downfall's hit sparks and fire-pit flames into two GPU particle effects, with predictions, frame strips, state tests and a price against a budget.",
        "runningText": "reading the brief, strips and logs…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
        "output": ["Effect A: hit_spark — one burst per landed melee hit", "Effect B: fire_pit_flames — sized by burn_left", "Strips, tests and GPU readings; misses kept"]},
        "Composer opens on the A6 demonstration prompt"), act="ASK")
    add("B01", graphic("BrutalistHesitantWriter", {
        "text": "A particle effect is decoration.\nEach burst answers one game event.\nSettings live in scene files.\nThe player's eyes decide.",
        "triggerWords": "decoration", "replacementWords": "a message", "seed": "downfall-a6-20261107",
        "fontSize": 88, "lineSpacing": 1.55, "charMs": 22, "jitter": 10, "mistakeRate": 0, "hesitateWithin": 0,
        "hesitateBetween": 0, "brandLabel": "@NikBearBrown"}, "The writer changes decoration to a message"), lead_silence_s=0.8)
    for bid in ORDER[2:-3]:
        if bid in EXCERPTS:
            add(bid, code(bid))
        elif bid in RESULTS:
            add(bid, media(bid, RESULTS[bid], bid in MOTION))
        elif bid == "B32":
            add(bid, media(bid, "The user's Visual Profiler screenshots: Update GPU Particles row against the budget"))
        elif bid == "B33":
            add(bid, media(bid, "Who did what, texture sources and the filmed commit"))
    add("B34", graphic("ClaudeVerdictArtifact", {
        "artifactTitle": "A6 Verdict", "artifactHeading": "What The Evidence Supports", "brandLabel": "@NikBearBrown",
        "artifactLines": ["Both effects fire on their events; tests, strips and GPU readings agree.",
                          "Caught by the user: wrong occlusion diagnosis, unrepeatable fixture, F7/F8 keys; Claude's r0 still reading overruled.",
                          "One kept revision each (Puff 0.5→1.0, Flames 0.30→0.55); both predictions partly missed.",
                          "Open: draw-step GPU cost, ember visibility, boss-arena fire on screen."]},
        "The verdict separates evidence, mistakes and open questions"), act="VERDICT")
    add("B35", graphic("ClaudeComposerAsk", {
        "greeting": "Your turn.", "topic": "ONE SETTING · ONE PREDICTION", "segment": "Let The Player Judge",
        "command": PROMPT, "runningText": "paste this into Claude…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
        "output": ["Name the event.", "Predict the strip first.", "Keep the miss; the human gives the verdict."]},
        "The viewer's bounded experiment is typed and read aloud"), act="HANDOFF")
    add("B36", graphic("ClaudeTitleOutro", {"title": TITLE, "slug": REEL.name}, "Exact title, regular mascot and stock jingle"),
        act="OUTRO", audio_policy="silence", actual_duration_s=7.0)
    sheet = {"metadata": {"title": TITLE, "slug": REEL.name, "topic": "GODOT GAMEDEV · A6 PARTICLES", "kind": "godot-gamedev",
                          "mode": "walker", "brand": "claude-liam", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
                          "palette": "claude", "aspect_ratio": "16:9", "captions": False, "channel": "@NikBearBrown",
                          "folderLabel": "@NikBearBrown",
                          "game": {"name": "downfall-godot (walker-downfall)", "engine_version": "Godot 4.7.2",
                                   "revision": "git HEAD at filming (see gamedev-evidence.json source_revision) + source hashes"}},
             "beats": beats}
    for b in beats:
        assert b["film_key"] == "B36" or b["narration_text"], b["beat_id"]
    (REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(beats), "beats")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


ASSOC = {  # component -> extra files it explains or rests on
    "b02": ["effects/hit_spark.gd", "tests/test_hit_spark_state.gd", "logs/test_hit_spark_state_60fps.log", "README.md"],
    "b04": ["tests/test_fire_pit_flames_state.gd", "previews/fire_pit_flames_preview.gd", "previews/fire_pit_flames_preview.tscn"],
    "b06": ["previews/hit_spark_preview.gd", "previews/hit_spark_preview.tscn", "TUNING.md"] +
           [f"captures/hit_spark/r0/{n}" for n in ("command.txt", "capture.log", "frame00000010.png", "frame00000012.png", "frame00000015.png", "frame00000020.png", "frame00000030.png", "frame00000050.png")],
    "b08": ["effects/hit_spark.gd"],
    "b10": [],
    "b12": [f"captures/hit_spark/r0-snow/{n}" for n in ("command.txt", "capture.log", "frame00000010.png", "frame00000012.png", "frame00000015.png", "frame00000020.png", "frame00000030.png", "frame00000050.png")],
    "b14": ["evidence/a6/user/fire_pit_preview_occluded_by_boulders.png", "FRICTIONAL.md"] +
           [f"captures/fire_pit_flames/{r}/{n}" for r in ("r0", "r0b") for n in ("command.txt", "capture.log", "frame00000012.png", "frame00000054.png", "frame00000070.png", "frame00000130.png")],
    "b13a": [f"captures/hit_spark/{r}/{n}" for r in ("r1", "r1-snow") for n in ("command.txt", "capture.log", "frame00000010.png", "frame00000012.png", "frame00000015.png", "frame00000020.png", "frame00000030.png", "frame00000050.png")] + ["tests/test_hit_spark_config.gd"],
    "b16": ["tests/test_fire_pit_flames_config.gd"] +
           [f"captures/fire_pit_flames/r1/{n}" for n in ("command.txt", "capture.log", "frame00000010.png", "frame00000012.png", "frame00000040.png", "frame00000054.png", "frame00000070.png", "frame00000099.png", "frame00000105.png", "frame00000130.png", "frame00000175.png")],
    "b18": ["entities/fire_pit.gd", "previews/play_check.gd", "previews/play_check.tscn", "logs/test_fire_pit_flames_state_60fps.log"],
    "b20": [],
    "b22": ["evidence/a6/mutations/m1_godot3_name.log", "evidence/a6/mutations/m1_godot3_name_preview.log",
            "evidence/a6/mutations/m1_godot3_name_frame12_fixture.png", "evidence/a6/mutations/m1b_compat_vector2.log",
            "tests/a6_make_scratch_process_scene.gd", "previews/scratch_process_shader.tscn"],
    "b24": ["evidence/a6/step6/attempt1_particles_generated.gdshader.txt", "logs/a6_dump_process_shader_windowed.log"],
    "b26": [],
    "b28": ["tests/test_fire_pit_flames_config.gd", "logs/test_hit_spark_config_60fps.log", "logs/test_fire_pit_flames_config_60fps.log",
            "evidence/a6/mutations/m2_value_drift.log", "logs/test_hit_spark_state_60fps_mutation_parent.log", "TEST-REPORT.md",
            "logs/baseline-before/summary.txt", "logs/baseline-after-step5/summary.txt"],
    "b30": ["logs/cost_effects_60fps.log", "tests/a6_probe_headless.gd", "logs/a6_probe_headless_60fps.log", "CLAUDE.md"],
}
EXTRA = [  # non-code components: (id, beats, files, explanation)
    ("gpu_price", ["B32"], ["previews/gpu_price.gd", "previews/gpu_price.tscn"] + [f"evidence/a6/gpu/{n}" for n in (
        "visual_profiler_1_U.png", "visual_profiler_2_I.png", "visual_profiler_3_O.png", "visual_profiler_round2_I_B_on.png",
        "visual_profiler_round2_U_A_on.png", "visual_profiler_round3_both_off.png")],
     "The user's Visual Profiler readings of the GPU particle process step against the brief's budget."),
    ("credits", ["B33", "B34"], ["SOURCES.md", "CHANGE-BRIEF.md", "project.godot"],
     "Who did what, texture sources, the filmed revision and the verdict on the A6 evidence."),
]


def ledger():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    narr = {b["film_key"]: b["narration_text"] for b in sheet["beats"]}
    files, comps, excerpts, pairs = {}, [], [], []

    def attach(path, cid, role):
        rec = files.setdefault(path, {"path": path, "sha256": sha(GAME / path), "role": role, "component_ids": []})
        if cid not in rec["component_ids"]:
            rec["component_ids"].append(cid)
        comp = next(c for c in comps if c["id"] == cid)
        if path not in comp["files"]:
            comp["files"].append(path)

    for bid, (path, start, end, *_rest) in EXCERPTS.items():
        cid = bid.lower()
        result = ORDER[ORDER.index(bid) + 1]
        comps.append({"id": cid, "explanation": narr[bid] + " " + narr[result], "beat_ids": [ID[bid], ID[result]], "files": []})
        attach(path, cid, "A6 source shown verbatim on screen")
        for extra in ASSOC.get(cid, []):
            attach(extra, cid, "Input, fixture, capture or recorded evidence explained by this component")
        excerpts.append({"beat_id": ID[bid], "path": path, "start_line": start, "end_line": end, "text": excerpt(bid)})
        clip = REEL / f"media/{ID[result]}.mp4"
        pairs.append({"code_beat": ID[bid], "result_beat": ID[result], "observation": narr[result],
                      "media": {"path": f"media/{ID[result]}.mp4", "sha256": sha(clip)}})
    for cid, bids, paths, text in EXTRA:
        comps.append({"id": cid, "explanation": text, "beat_ids": [ID[b] for b in bids], "files": []})
        for p in paths:
            attach(p, cid, "Evidence or record shown or cited in this beat")
    inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*") if p.is_file()
                 and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts) and p.suffix != ".uid")
    film = "youtube/" + REEL.name + "/"
    exclusions = []
    for p in inv:
        if p in files:
            continue
        if p.startswith(film):
            reason = "This film's own authoring, capture, media or QC file (not game source)."
            if p == film + "gamedev-evidence.json":
                reason = "This source inventory; self-hash would be recursive."
        else:
            reason = "Outside the A6 particle-effect components: the rest of the game, earlier assignments, other tests/logs or authoring files."
        exclusions.append({"path": p, "reason": reason})
    if not any(e["path"] == film + "gamedev-evidence.json" for e in exclusions):
        exclusions.append({"path": film + "gamedev-evidence.json", "reason": "This source inventory; self-hash would be recursive."})
    data = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
            "source_revision": {"git_commit": subprocess.run(["git", "-C", str(GAME), "log", "-1", "--format=%H"], capture_output=True, text=True).stdout.strip(),
                                "working_tree_note": "Tracked files: " + (subprocess.run(["git", "-C", str(GAME), "status", "--short", "--untracked-files=no", "."], capture_output=True, text=True).stdout.strip() or "no modifications") + ". Untracked: this film folder and pre-existing .uid sidecars. Hashes below are of the working tree."},
            "files": list(files.values()), "components": comps, "excerpts": excerpts, "exclusions": exclusions,
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(files), "files,", len(exclusions), "exclusions,", len(pairs), "pairs")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["author", "ledger"])
    a = ap.parse_args()
    author() if a.mode == "author" else ledger()
