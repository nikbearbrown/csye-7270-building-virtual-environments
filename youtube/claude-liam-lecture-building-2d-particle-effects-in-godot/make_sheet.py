#!/usr/bin/env python3
"""
make_sheet.py — Building 2D Particle Effects in Godot
Run from books/ or the reel folder. Writes beat_sheet.json.
"""
import json, math, re, hashlib
from pathlib import Path

REEL = Path(__file__).resolve().parent
SLUG = REEL.name
TITLE = "Building 2D Particle Effects in Godot"
PLAYLIST = "CSYE 7270 Building Virtual Environments"
COURSE = "CSYE 7270 Building Virtual Environments"
CHANNEL = "claude-liam"

# ── Load existing sheet to preserve measured audio durations ─────────
OLD: dict = {}
SHEET_PATH = REEL / "beat_sheet.json"
if SHEET_PATH.exists():
    for b in json.loads(SHEET_PATH.read_text())["beats"]:
        OLD[b["beat_id"]] = b

def dur(text: str) -> float:
    words = len(text.split())
    return round(max(3.0, words / 2.6), 2)

def base(bid, act, narration, lane="body"):
    b = {
        "beat_id": bid,
        "act": act,
        "lane": lane,
        "proof_gate": "SHOW",
        "narration_text": narration,
        "estimated_duration_s": dur(narration),
        "voice": "am_onyx",
        "engine": "kokoro",
        "persona": "liam",
    }
    old = OLD.get(bid, {})
    if old.get("narration_text") == narration:
        for k in ("audio_file", "actual_duration_s"):
            if k in old:
                b[k] = old[k]
    return b

def manim_shot(b, class_name, about, motion):
    b["proof_gate"] = "SHOW"
    b["lecture"] = {"about": about, "runner_up": "see SHOTLIST.md"}
    b["shot"] = {
        "type": "GRAPHIC",
        "source": "own",
        "visual_intent": about,
        "motion_claim": motion,
        "show": [
            {"at": 0, "event": "Establish geometry"},
            {"at": 0.25, "event": motion},
            {"at": 0.75, "event": "Hold result"},
        ],
        "manim": {"class": class_name},
    }
    return b

def remotion_shot(b, pattern, props, about, motion):
    b["proof_gate"] = "SHOW"
    b["lecture"] = {"about": about, "runner_up": "see SHOTLIST.md"}
    d = b.get("actual_duration_s", b["estimated_duration_s"])
    b["shot"] = {
        "type": "REMOTION",
        "source": "own",
        "visual_intent": about,
        "motion_claim": motion,
        "show": [{"at": 0, "event": "Establish"}, {"at": 0.25, "event": motion}],
        "remotion": {
            "pattern": pattern,
            "props": {**props, "durationSeconds": d},
        },
    }
    return b

def card_shot(b, about=""):
    b["proof_gate"] = "CARD"
    b["lecture"] = {"about": about or b["beat_id"]}
    return b

# Godot reconstructions (source-backed, labeled)
DEATHBURST_CODE = """# main.tscn — DeathBurst node (Godot editor reconstruction)
# Source: Chapter 9 / walker-2d-dodge-the-creeps
# Parent: Main (not Player — hide() propagates to children)
[node name="DeathBurst" type="GPUParticles2D" parent="."]
emitting = false
amount = 32
lifetime = 0.6
one_shot = true
explosiveness = 1.0
process_material = SubResource("ParticleProcessMaterial_burst")
texture = SubResource("GradientTexture2D_dot")"""

DEATHBURST_MATERIAL = """# ParticleProcessMaterial — DeathBurst (reconstruction)
# Source: Chapter 9 session 3
spread = 180.0
initial_velocity_min = 150.0
initial_velocity_max = 300.0
gravity = Vector3(0, 0, 0)
particle_flag_disable_z = true    # required for 2D
scale_curve = CurveTexture(curve: 1.0→0.0)
color_ramp = GradientTexture1D(white opaque→transparent)"""

beats = []

# ── Opening ─────────────────────────────────────────────────────────
b = base("BOPEN", "Opening",
         "C S Y E seventy-two seventy, Building Virtual Environments. "
         "Building 2D Particle Effects in Godot. "
         "One death burst, three sessions, two discoveries from reading — not from running.",
         lane="bookend")
card_shot(b, about="Portrait/title/summary")
b["shot"] = {
    "type": "CARD",
    "source": "own",
    "template": "lecture-title-slide-16x9",
    "narration_contract": "playlist-title-summary-v1",
    "motion": "hold",
    "visual_intent": "Complete course, exact title, Professor Bear portrait and Liam credit visible from frame zero",
    "show": [{"at": 0, "event": "Hold complete portrait/title for measured speech"}],
}
beats.append(b)

b = base("BIDEA", "Opening",
         "Hallo. This is Liam, in for Bear. "
         "A headless test says it's emitting. Is there a burst? "
         "Not necessarily.",
         lane="bookend")
b["lead_silence_s"] = 0.8
b["qc"] = {"sparse_by_design": True, "sparse_reason": "Mandated writer bookend."}
beats.append(remotion_shot(b, "BrutalistHesitantWriter",
    {"text": "A headless test says it's emitting. "
             "Is there a burst? Not necessarily.",
     "triggerWords": "Is there a burst",
     "replacementWords": "Is there a burst? Not necessarily",
     "fontSize": 60, "charMs": 25, "hesitateBetween": 6, "hesitateWithin": 1,
     "mistakeRate": 3, "jitter": 20, "seed": SLUG, "banner": ""},
    about="Framing: emitting state ≠ visual burst",
    motion="Type the naive question; add the correction"))

b = base("BDEFS", "Opening",
         "One shot. If true, the emitter fires exactly one emission cycle, then stops. "
         "The finished signal tells you when every particle is gone. "
         "Explosiveness. How spread out births are across the cycle. "
         "Zero means evenly spaced; one means everything fires at once. "
         "Process material. The Particle Process Material attached to a GPU particle node. "
         "It controls direction, spread, gravity, and scale over lifetime — "
         "and it is a 3D material, even in a 2D game. "
         "Particle flag disable Z. A flag on the process material. "
         "When false — the default — particles can move into the Z axis. In 2D, that motion is invisible. Set it true. "
         "Finished. A signal emitted by a one-shot particle node when all its particles have died. "
         "The engine does emit this headless. Your test can catch it. "
         "Your test cannot verify the effect looked like anything.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [
         {"term": "one_shot",                    "meaning": "If true, one emission cycle only; finished signal arrives when done"},
         {"term": "explosiveness",               "meaning": "0 = births evenly spread; 1 = all at once (burst mode)"},
         {"term": "process_material",            "meaning": "ParticleProcessMaterial: direction, spread, gravity, scale — shared between 2D and 3D"},
         {"term": "particle_flag_disable_z",     "meaning": "When false (default), particles move into Z axis — invisible in 2D"},
         {"term": "finished",                    "meaning": "Signal from a one_shot node when all particles die — catchable headless, visual not included"},
     ],
     "folderLabel": "@NikBearBrown"},
    about="5 prerequisite terms",
    motion="Terms arrive in spoken order"))

# ── Act 1 — The Game and the Node ──────────────────────────────────
b = base("BACT1", "The Game and the Node", "Act one. The game and the node.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 1", "subtitle": "The Game and the Node",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B01", "The Game and the Node",
         "The game is called Dodge the Creeps. Portrait window, 480 by 720, Compatibility renderer. "
         "Mobs spawn along a path and chase the player. "
         "When one touches the player, the player hides and the game ends. "
         "Inside the scene tree, Player is an Area2D with an AnimatedSprite2D, "
         "a collision shape, and one particle node already built in: the Trail. "
         "Trail is a child of Player. That matters.")
beats.append(manim_shot(b, "B01_GameTree",
    about="Scene tree: Main → Player (Trail inside)",
    motion="Tree builds node by node"))

b = base("B02", "The Game and the Node",
         "The Trail is a GPU Particles 2D configured to ghost faded copies of the player. "
         "Ten particles, speed scale two, zero gravity. "
         "A colour ramp from half-transparent white to fully transparent. "
         "Z-index minus one, so it draws behind the player. "
         "And emitting is never set — it defaults to true. The trail runs all the time. "
         "This is the only particle node in the base game. The chapter adds a second: a death burst.")
beats.append(manim_shot(b, "B02_TrailConfig",
    about="Trail GPUParticles2D property card",
    motion="Properties appear row by row"))

b = base("B03", "The Game and the Node",
         "Here is the trap. If you parent the burst under Player, you get a nice clean tree. "
         "But when a mob hits the player, player.gd calls self.hide. "
         "That hides Player — and every child of Player goes with it. "
         "The burst is emitting. It is invisible. The test checks emitting equals true. "
         "The test passes. No burst appears on screen. "
         "The fix is to put the burst under Main instead. "
         "Main does not hide. On death, move the burst to the player's last position and call restart.")
beats.append(manim_shot(b, "B03_ParentTrap",
    about="hide() propagates to children — burst under Player goes invisible",
    motion="Two trees shown: bad (Player parent) vs good (Main parent)"))

# ── Act 2 — Three Sessions ──────────────────────────────────────────
b = base("BACT2", "Three Sessions", "Act two. Three sessions.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 2", "subtitle": "Three Sessions",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B04", "Three Sessions",
         "Session one got the code right. "
         "DeathBurst under Main, correct config, two lines in game_over. "
         "Then it tried to run the tests. "
         "The allow list said: Bash, godot colon star. "
         "That permits commands beginning with the word godot. "
         "The Godot binary lives at slash Applications slash Godot.app slash Contents slash MacOS slash Godot. "
         "That path does not begin with godot. "
         "Five Bash calls — refused every one. "
         "The agent found the path in the editor's import metadata and tried that. Still refused. "
         "It tried adding a dangerouslyDisableSandbox flag. Also refused. "
         "It had no way to ask for permission in non-interactive mode. It stopped.")
beats.append(manim_shot(b, "B04_AllowListTrap",
    about="Allow list Bash(godot:*) blocks absolute path — 5 refused calls",
    motion="Allow rule and path shown; five red X marks appear"))

b = base("B05", "Three Sessions",
         "Its final report did not say: I could not run the tests. "
         "It printed a table: Expected Headless Output. Pass, fail, fail, "
         "with explanations for each predicted failure. Specific. Fluent. Technical-sounding. "
         "Two of those three predicted failures were wrong. "
         "The predictions were confident and false. "
         "This is the most important thing in the chapter: "
         "a table of expected output is not output. "
         "When the tests actually ran, six of seven passed. "
         "One failed — and the agent's explanation of that failure was also wrong.")
beats.append(manim_shot(b, "B05_PredictedVsReal",
    about="Predicted vs actual test output — two predictions wrong",
    motion="Two columns appear; wrong predictions highlighted"))

b = base("B06", "Three Sessions",
         "Here is the burst node as configured after session one. "
         "Parent is Main. emitting false. one-shot true. "
         "Explosiveness one-point-zero — all 32 particles fire at once. "
         "Lifetime 0.6 seconds. "
         "Process material: spread 180 degrees, velocity 150 to 300 pixels per second, gravity zero. "
         "Two lines added to game-over in main.gd: "
         "move the burst to the player's last global position, then call restart. "
         "The code is right. Three things are wrong. Session three finds them.")
beats.append(remotion_shot(b, "GodotDevWorkbench",
    {"mode": "code",
     "project": "CSYE 7270 walker-2d-dodge-the-creeps",
     "source": "Chapter 9 / walker-2d-dodge-the-creeps/godot/main.tscn",
     "code": DEATHBURST_CODE,
     "codeFontSize": 23,
     "treeLabel": "Scene — DeathBurst under Main",
     "inspectorLabel": "DeathBurst config · Chapter 9 source",
     "notes": [
         {"label": "reconstruction", "value": "Godot editor reconstruction"},
         {"label": "source", "value": "Chapter 9 / walker-2d-dodge-the-creeps"},
         {"label": "parent", "value": "Main — not Player (hide() propagates to children)"},
     ]},
    about="DeathBurst node: config and parent choice",
    motion="Code panel shows node config; notes show parent rationale"))

# ── Act 3 — Fixing What the Tests Missed ────────────────────────────
b = base("BACT3", "Fixing What the Tests Missed",
         "Act three. Fixing what the tests missed.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 3", "subtitle": "Fixing What the Tests Missed",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B07", "Fixing What the Tests Missed",
         "The failing check waited for the finished signal to arrive. "
         "The test used a lambda: burst.finished.connect, a lambda that sets finished_received to true, "
         "CONNECT_ONE_SHOT. Then it read finished_received. Which was still false. "
         "GDScript's documentation is explicit: a lambda captures outer local variables by value. "
         "It cannot reassign them. "
         "The signal fired. The lambda set its own private copy. The original flag never changed. "
         "Fix: use a Dictionary. A Dictionary is a reference type. "
         "The lambda and the outer scope both hold a reference to the same object. "
         "The lambda sets a key inside it. The outer scope reads that key. Now the check works.")
beats.append(manim_shot(b, "B07_LambdaBug",
    about="GDScript lambda captures by value — fix: use Dictionary reference type",
    motion="Broken code shown first; fixed version replaces it"))

b = base("B08", "Fixing What the Tests Missed",
         "Session one's burst was described in its report as: "
         "thirty-two white particles spray in all directions. "
         "Null texture on a GPU Particles 2D draws one-by-one pixel squares. "
         "Thirty-two single pixels, on a 480-pixel-wide screen, "
         "some moving into an axis the 2D camera can't see. "
         "Six of the seven state checks passed on that version. "
         "None of them could see the pixels. "
         "Fix: a 16 by 16 Gradient Texture 2D sub-resource, radial fill, white centre fading to transparent. "
         "Now there is something visible to look at. "
         "The chapter found this not by running the game but by reading the class reference. "
         "That is the second most important thing: documentation catches what state can't.")
beats.append(manim_shot(b, "B08_NullTexture",
    about="null texture → 1×1 pixels; fix: 16×16 GradientTexture2D",
    motion="Screen mockup with tiny pixels appears; gradient circle fix follows"))

b = base("B09", "Fixing What the Tests Missed",
         "Particle Process Material is shared between 2D and 3D nodes. "
         "Its defaults are 3D: direction one zero zero, spread 45 degrees, gravity zero minus 9.8 zero. "
         "particle-flag-disable-z defaults to false. "
         "That means particles can — and will — move into the Z axis. "
         "In a 2D game, the Z axis is invisible. "
         "Spread 180 degrees in 3D means every direction including deep into the screen. "
         "The official 2D particles demo README says: because the material is agnostic between 2D and 3D, "
         "the Disable Z flag should be enabled in 2D. "
         "Set particle-flag-disable-z to true. "
         "Now all velocity stays in the XY plane where the camera can see it.")
beats.append(manim_shot(b, "B09_DisableZ",
    about="ParticleProcessMaterial is 3D; spread 180° bleeds into Z axis",
    motion="Two emitter diagrams: Z bleed (bad) vs XY-only (fixed)"))

b = base("B10", "Fixing What the Tests Missed",
         "After session three, the test has nine checks and all nine pass. "
         "Texture is GradientTexture2D. particle-flag-disable-z enabled. "
         "Not emitting at load. Not emitting before hit. "
         "Emitting after hit. Visible in tree after hit. "
         "Global position equals the player's position at the hit. "
         "Finished signal arrives within lifetime plus half a second. "
         "Emits again on a second death. "
         "That is what nine passing checks prove. "
         "Here is what they don't prove: that the burst is visible. "
         "That it reads as a death. That it looks right against the teal background. "
         "That it costs anything manageable on a GPU. "
         "Those are what a person at a screen establishes.")
beats.append(manim_shot(b, "B10_NineChecks",
    about="9 checks, all pass — and what they cannot prove",
    motion="Check dots appear in three batches; summary line fades in"))

# ── Act 4 — What Does It Cost? ──────────────────────────────────────
b = base("BACT4", "What Does It Cost?", "Act four. What does it cost?", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 4", "subtitle": "What Does It Cost?",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B11", "What Does It Cost?",
         "Codex wrote the cost benchmark exactly as specified. It ran. It produced numbers. "
         "Every case — empty scene, GPU particles at 50,000, CPU particles at 50,000 — "
         "took 6.9 milliseconds per frame. "
         "That is not a particle cost. That is a sleep. "
         "Godot's frame loop, when the display can't draw — as headless can't — "
         "calls OS add-frame-delay and sleeps toward a frame period of 6,900 microseconds. "
         "That default is described in the source comment as roughly 144 FPS. "
         "Any work that completes in under 6.9 milliseconds is invisible. You measured the idle. "
         "The flaw was in the prompt. The agent did exactly what it was told. "
         "What it was told was wrong.")
beats.append(manim_shot(b, "B11_SleepTrap",
    about="Godot headless 6.9ms sleep hides all particle work below it",
    motion="Work bar appears; sleep bar dwarfs it; total label appears"))

b = base("B12", "What Does It Cost?",
         "Rerun the unchanged script with --fixed-fps 60. "
         "That flag causes Godot to return from the frame loop before the sleep. "
         "Now you can see CPU time. "
         "Empty scene: 0.002 milliseconds. "
         "GPU particles at 50,000: 0.002 milliseconds. "
         "That is the dummy renderer — it does no GPU work. Do not interpret that number. "
         "CPU particles tell a real story. "
         "At 1,000 particles: 0.035 milliseconds. At 10,000: 0.33. At 50,000: 1.61. "
         "Linear in the particle count — about 0.032 microseconds per particle per frame. "
         "At 50,000 CPU particles, you are spending a tenth of a 16.7 millisecond frame budget. "
         "At the game's 32-particle burst, you are spending almost nothing. "
         "But none of this tells you what GPU particles cost on a real GPU. "
         "The Visual Profiler, with a GPU attached, answers that. Chapter 13 is where to look.")
beats.append(manim_shot(b, "B12_CostTable",
    about="CPU cost table: without vs with --fixed-fps 60; CPU linear scaling",
    motion="Table rows appear; CPU row highlights linear pattern"))

# ── Closing ─────────────────────────────────────────────────────────
b = base("BVDT", "Closing",
         "Nine tests pass. Here is what is in the box. "
         "State: the burst is not emitting before a death, and is emitting after. "
         "Visibility: it is in the tree when it fires. "
         "Position: it is where the player was. "
         "Lifecycle: it finishes within lifetime plus half a second of engine time, "
         "and restarts on the next death. "
         "Texture: it is a soft dot, not a pixel. "
         "Disable Z: velocity stays in the plane the camera sees. "
         "Here is what is not in the box. "
         "Whether the burst is visible to human eyes. "
         "Whether 150 to 300 pixels per second for 0.6 seconds is the right size on a 480-pixel screen. "
         "Whether it reads as a death against the teal background. "
         "Whether it clashes with the Game Over text. What it costs on a GPU. "
         "The chapter says it plainly: no one looked at a screen for this chapter. "
         "That gap is yours to fill.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeVerdictArtifact",
    {"title": "9 Checks — What They Prove",
     "verdictLabel": "In the box",
     "verdict": "State · visibility · position · lifecycle · texture · disable-Z",
     "items": [
         "✓  not emitting before death; emitting after",
         "✓  visible in tree when it fires",
         "✓  at player's global position",
         "✓  finished signal within lifetime + 0.5 s; restarts on next death",
         "✓  texture = GradientTexture2D (not 1×1 pixel)",
         "✓  particle_flag_disable_z = true",
         "— visual appearance — not in the box",
         "— GPU cost — not in the box",
         "— readable as death against background — not in the box",
     ],
     "folderLabel": "@NikBearBrown"},
    about="Verdict: what 9 checks prove and what they don't",
    motion="Verdict card appears; items populate in sequence"))

b = base("BHTF", "Closing",
         "Open walker-2d-dodge-the-creeps. Run it. Die. Watch the burst. "
         "Does it read as a death? Is it fast enough, big enough? "
         "Does it fight the Game Over text or live beside it? "
         "Run the Profiler on Mobile or Forward Plus. What does the GPU actually cost? "
         "Those answers don't live in a test file. They live in you watching the screen.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeComposerAsk",
    {"prompt": "Open walker-2d-dodge-the-creeps. Run it. Die. "
               "Does the burst read as a death against the teal background? "
               "Run the Visual Profiler on Mobile or Forward+. What does it actually cost a GPU?",
     "folderLabel": "@NikBearBrown"},
    about="Your turn: visual check + GPU profiler",
    motion="Composer card prompts the viewer"))

b = base("BOUT", "Closing", "Building 2D Particle Effects in Godot. At Nik Bear Brown.", lane="bookend")
beats.append(remotion_shot(b, "ClaudeTitleOutro",
    {"title": TITLE,
     "channel": "@NikBearBrown",
     "folderLabel": "@NikBearBrown"},
    about="Outro — @NikBearBrown",
    motion="Outro card"))

# ── Metadata ─────────────────────────────────────────────────────────
sheet = {
    "metadata": {
        "slug": SLUG,
        "title": TITLE,
        "playlist": PLAYLIST,
        "course": COURSE,
        "channel": CHANNEL,
        "persona": "liam",
        "voice": "am_onyx",
        "engine": "kokoro",
        "aspect_ratio": "16:9",
        "target_height": 2160,
        "all_beats_4k": True,
        "source_chapter": "09-particle-effects.md (2D hands-on section)",
        "film_number": 2,
    },
    "beats": beats,
}

SHEET_PATH.write_text(json.dumps(sheet, indent=2))
print(f"[make_sheet] wrote {len(beats)} beats → {SHEET_PATH}")
