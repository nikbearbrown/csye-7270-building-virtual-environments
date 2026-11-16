#!/usr/bin/env python3
"""
make_sheet.py — What Is a Particle System?
Run from books/ or the reel folder. Writes beat_sheet.json.
"""
import json, math, re, hashlib
from pathlib import Path

REEL = Path(__file__).resolve().parent
SLUG = REEL.name
TITLE = "What Is a Particle System?"
PLAYLIST = "CSYE 7270 Building Virtual Environments"
COURSE = "CSYE 7270 Building Virtual Environments"
CHANNEL = "claude-liam"

# ── Load existing sheet to preserve measured audio durations ──────
OLD: dict = {}
SHEET_PATH = REEL / "beat_sheet.json"
if SHEET_PATH.exists():
    for b in json.loads(SHEET_PATH.read_text())["beats"]:
        OLD[b["beat_id"]] = b

def dur(text: str) -> float:
    """Estimate duration from word count at ~2.6 words/second, min 3 s."""
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

# Inspector values drawn from Chapter 9 ClassDB probe and Godot 4.7.2 class reference
GODOT_TIMING_INSPECTOR = """# GPUParticles2D — Inspector (Godot editor reconstruction)
# Source: Chapter 9 / Godot 4.7.2 class reference
amount = 10
lifetime = 1.0
explosiveness = 0.0
one_shot = false
preprocess = 0.0
randomness = 0.0
speed_scale = 1.0
fixed_fps = 30
emitting = true"""

GODOT_MATERIAL_INSPECTOR = """# ParticleProcessMaterial — Inspector (Godot editor reconstruction)
# Source: Chapter 9 "The process material is 3D, even in 2D"
# Defaults are 3D — must set Disable Z for 2D
direction = Vector3(1, 0, 0)
spread = 45.0
gravity = Vector3(0, -9.8, 0)
initial_velocity_min = 0.0
initial_velocity_max = 0.0
particle_flag_disable_z = false   ← MUST BE TRUE for 2D effects"""

GODOT_NODE_TYPES = """# Godot particle nodes — feature comparison
# Source: Chapter 9 "Four node types, two families"
GPUParticles2D / GPUParticles3D:
  process_material (ParticleProcessMaterial): YES
  sub_emitter: YES
  trail_enabled: YES
  amount_ratio: YES

CPUParticles2D / CPUParticles3D:
  process_material (ParticleProcessMaterial): NO (node props)
  sub_emitter: NO
  trail_enabled: NO
  near-feature parity, wider hardware support"""

GODOT_BURST_INSPECTOR = """# GPUParticles2D 'SignalBurst' — Inspector (Godot editor reconstruction)
# Source: walker-claude/godot/signal-garden/effects/burst.tscn
node_type = CPUParticles3D
emitting = false
amount = 32
lifetime = 0.7
one_shot = true
explosiveness = 1.0
randomness = 0.1
direction = Vector3(0, 1, 0)
spread = 65.0
initial_velocity_min = 1.3
initial_velocity_max = 2.2"""

beats = []

# ── Opening ────────────────────────────────────────────────────────
b = base("BOPEN", "Opening",
         "C S Y E seventy-two seventy, Building Virtual Environments. "
         "What Is a Particle System? "
         "Learn how one rule repeated thousands of times makes smoke, fire, and sparks that respond to your game.",
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
         "You open Godot's particle system and find seven hundred checkboxes. "
         "You start clicking and hoping.",
         lane="bookend")
b["lead_silence_s"] = 0.8
b["qc"] = {"sparse_by_design": True, "sparse_reason": "Mandated writer bookend: the phrase correction carries the distinction."}
beats.append(remotion_shot(b, "BrutalistHesitantWriter",
    {"text": "You open Godot's particle system and find seven hundred checkboxes. "
             "You start clicking and hoping.",
     "triggerWords": "clicking and hoping",
     "replacementWords": "running one loop",
     "fontSize": 60, "charMs": 25, "hesitateBetween": 6, "hesitateWithin": 1,
     "mistakeRate": 4, "jitter": 20, "seed": SLUG, "banner": ""},
    about="Framing: checkboxes → one loop",
    motion="Type the mistaken framing; correct final phrase"))

b = base("BDEFS", "Opening",
         "Particle. One short-lived simulation point — it has a position, a velocity, "
         "and an age, and when its age exceeds its lifetime, it's gone. "
         "Emitter. The source that spawns particles — it decides where and when new ones are born. "
         "Lifetime. How long a single particle lives, measured in seconds. "
         "Velocity. Rate of position change — direction and speed together. "
         "Emission cycle. One complete pass through the emitter's particle budget — "
         "its length equals the particle lifetime.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [
         {"term": "Particle",    "meaning": "One short-lived simulation point with position, velocity, and age"},
         {"term": "Emitter",     "meaning": "Source that spawns particles — controls when and where"},
         {"term": "Lifetime",    "meaning": "How long a single particle lives (seconds)"},
         {"term": "Velocity",    "meaning": "Rate of position change — direction and speed"},
         {"term": "Emission cycle", "meaning": "One pass through the particle budget; length = lifetime"},
     ],
     "folderLabel": "@NikBearBrown"},
    about="5 prerequisite terms",
    motion="Terms arrive in spoken order"))

# ── ACT I — One Moving Element ─────────────────────────────────────
b = base("BACT1", "One Moving Element", "One Moving Element.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"lines": ["One Moving Element"], "dark": False},
    about="Act I title", motion="Title card holds"))

b = base("B01", "One Moving Element",
         "In 1983, William Reeves described what he called fuzzy objects — fire and smoke in the "
         "Genesis sequence from Star Trek Two. His idea: an effect is a cloud of points that are "
         "born, that move and change, and that die. Every game engine you'll ever use runs exactly that loop.")
beats.append(manim_shot(b, "B01_ReevesCredit",
    about="Reeves 1983 — the loop named",
    motion="Birth–life–death loop labels arrive in sequence; credit line fades in"))

b = base("B02", "One Moving Element",
         "Start with one dot. It has a position — where it is. It has a velocity — "
         "how fast it's moving and in which direction. It can have acceleration — "
         "what's changing the velocity. These are three different jobs, and they each play a role in how the dot moves.")
beats.append(manim_shot(b, "B02_ThreeJobs",
    about="Position / velocity / acceleration — three distinct roles",
    motion="Each arrow grows on its spoken cue; label lands on the word"))

b = base("B03", "One Moving Element",
         "Each frame, the velocity changes the position. Acceleration changes the velocity. "
         "In Godot, we multiply by delta — the time since the last frame — "
         "so the motion is the same speed on a slow machine and a fast one. One step. Done each frame.")
beats.append(manim_shot(b, "B03_UpdateStep",
    about="Update equation: pos += vel × delta",
    motion="Equation appears; dot steps forward frame by frame under it"))

b = base("B04", "One Moving Element",
         "Here's a dot starting at the bottom. Its velocity points up and slightly right. "
         "Each frame, delta time advances it. When gravity acts as acceleration pointing down, "
         "the dot curves. We're not drawing smoke yet. We're understanding the piece that smoke is made of.")
beats.append(manim_shot(b, "B04_OneDotArc",
    about="One dot tracing a parabolic arc under gravity",
    motion="Dot traces arc; velocity/position labels track; grid provides reference scale"))

# ── ACT II — Birth, Life and Removal ──────────────────────────────
b = base("BACT2", "Birth, Life and Removal", "Birth, Life and Removal.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"lines": ["Birth, Life and Removal"], "dark": False},
    about="Act II title", motion="Title card holds"))

b = base("B05", "Birth, Life and Removal",
         "Now give the dot an age. It starts at zero. Each frame, age increases by delta. "
         "When age exceeds lifetime — say one second — the dot is removed. "
         "While it lives, its opacity can track its normalized age: young and opaque, old and fading.")
beats.append(manim_shot(b, "B05_LifetimeFade",
    about="Age bar fills; opacity fades with normalized age",
    motion="Age bar advances; dot opacity decreases proportionally; dot vanishes at lifetime"))

b = base("B06", "Birth, Life and Removal",
         "Spawn several. Each has its own age and velocity, with a little random variation. "
         "Now you have a small shower of points — born, traveling, fading, gone. "
         "This already looks like something: a brief burst, or a faint rain.")
beats.append(manim_shot(b, "B06_Collection",
    about="Small collection of dots — each with independent velocity and age",
    motion="Dots spawn from emitter, fan outward with varied velocities, fade and vanish"))

b = base("B07", "Birth, Life and Removal",
         "At twenty births per second with a two-second lifetime, after warm-up you tend toward "
         "about forty particles alive at once. That's an illustrative prediction — "
         "change either number and predict the new population. This is the planning tool. It's not a benchmark.")
beats.append(manim_shot(b, "B07_PopulationCalc",
    about="Population steady-state: 20/s × 2s ≈ 40 alive",
    motion="Formula builds; counter advances to 40; bar fills; 'not a benchmark' note fades in"))

b = base("B08", "Birth, Life and Removal",
         "Remove the cleanup step. Every dot born stays forever. The count climbs without bound. "
         "The simulation bogs down. Returning cleanup lets the population settle. "
         "This is not a bug we're fixing — it's the lesson: "
         "a continuous effect stays alive while its individual particles expire. Cleanup is load-bearing.")
beats.append(manim_shot(b, "B08_UnboundedGrowth",
    about="Without removal, population climbs unbounded; with cleanup, it settles",
    motion="Counter climbs past 120 with warning; then cleanup restores and counter falls to 40"))

# ── ACT III — One Emitter, Many Variations ─────────────────────────
b = base("BACT3", "One Emitter, Many Variations", "One Emitter, Many Variations.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"lines": ["One Emitter, Many Variations"], "dark": False},
    about="Act III title", motion="Title card holds"))

b = base("B09", "One Emitter, Many Variations",
         "Move the emitter. The particles still carry their original velocity — "
         "they don't follow the source. They were born there, and they go where their velocity sends them.")
beats.append(manim_shot(b, "B09_MovingEmitter",
    about="Emitter moves; particles retain birth velocity (local_coords = false)",
    motion="Emitter dot moves left-to-right; particle trails diverge from birth positions"))

b = base("B10", "One Emitter, Many Variations",
         "Control the spread. A tight angle makes a jet. A wide spread makes a burst. "
         "Add random variation to the initial speed and the dot size. "
         "Now a handful of rules produces a cloud that looks organic. "
         "The key word is controlled: randomize everything and you lose the readable intention.")
beats.append(manim_shot(b, "B10_SpreadComparison",
    about="Narrow cone vs wide spread — same emitter, different angle ranges",
    motion="Left: tight jets; right: full-sphere burst; angles labeled"))

b = base("B11", "One Emitter, Many Variations",
         "A shared force — say, wind — affects every particle. "
         "All the dots bend in the same direction. This is how gravity works too: "
         "one rule applied to every particle, every frame. The force is part of the process, not the emission.")
beats.append(manim_shot(b, "B11_WindForce",
    about="Shared wind force bends all particles together",
    motion="Force vector arrow appears; all particles curve in wind direction"))

b = base("B12", "One Emitter, Many Variations",
         "Two modes. Spread births evenly across the lifetime and you get a continuous stream. "
         "Emit all of them at once — an explosiveness of one — and you get an instantaneous burst. "
         "Same parameters, different birth timing. That single knob is the difference between smoke and an explosion.")
beats.append(manim_shot(b, "B12_StreamVsBurst",
    about="explosiveness 0 → stream vs explosiveness 1 → burst",
    motion="Left side: particles drip continuously; right side: all fire at once"))

# ── ACT IV — From Rules to Godot's Nodes ───────────────────────────
b = base("BACT4", "From Rules to Godot's Nodes", "From Rules to Godot's Nodes.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"lines": ["From Rules to Godot's Nodes"], "dark": False},
    about="Act IV title", motion="Title card holds"))

b = base("B13", "From Rules to Godot's Nodes",
         "Godot formalizes the loop into three parts. Emission: how many particles are born, when, and where — "
         "set on the particle node itself. Process: how each particle moves and changes over its life — "
         "set on a material or shader. Draw: what each particle looks like — a texture, a mesh, and a material on top of that. "
         "An effect can be wrong in any one part independently.")
beats.append(manim_shot(b, "B13_EmissionProcessDraw",
    about="Emission / Process / Draw — three separable parts",
    motion="Table rows animate in on spoken cues; each row names Godot properties"))

b = base("B14", "From Rules to Godot's Nodes",
         "Godot gives you four nodes: G P U Particles 2D and 3D, and C P U Particles 2D and 3D. "
         "G P U nodes hand simulation to the graphics card and support sub-emitters, trails, and particle shaders. "
         "C P U nodes work on more hardware and are fully readable headlessly. "
         "The key difference is where the loop runs — not what the loop does.")
beats.append(remotion_shot(b, "GodotDevWorkbench",
    {"mode": "code",
     "title": "Godot particle nodes — feature comparison (editor reconstruction)",
     "project": "CSYE 7270 walker-claude",
     "source": "Chapter 9 / Godot 4.7.2 class reference",
     "code": GODOT_NODE_TYPES,
     "codeFontSize": 23,
     "treeLabel": "Scene — node types",
     "inspectorLabel": "Feature comparison · Chapter 9 source",
     "notes": [
         {"label": "reconstruction", "value": "Godot editor reconstruction"},
         {"label": "source", "value": "Chapter 9 ClassDB probe / Godot 4.7.2 docs"},
     ]},
    about="Four node types — GPU vs CPU feature differences",
    motion="Node names appear; feature rows highlight GPU-only features"))

b = base("B15", "From Rules to Godot's Nodes",
         "The four timing properties. Lifetime: how long each particle lives — also the length of one emission cycle. "
         "Amount: how many particles in one cycle. "
         "Explosiveness: zero spreads births across the cycle; one fires them all at once. "
         "One shot: if true, the cycle runs exactly once. "
         "These four together determine when and how many particles appear.")
beats.append(remotion_shot(b, "GodotDevWorkbench",
    {"mode": "code",
     "title": "GPUParticles2D — timing properties (editor reconstruction)",
     "project": "CSYE 7270 walker-claude",
     "source": "Chapter 9 / Godot 4.7.2 class reference",
     "code": GODOT_TIMING_INSPECTOR,
     "codeFontSize": 23,
     "treeLabel": "GPUParticles2D",
     "inspectorLabel": "Inspector · Godot 4.7.2",
     "notes": [
         {"label": "reconstruction", "value": "Godot editor reconstruction"},
         {"label": "source", "value": "Godot 4.7.2 GPUParticles2D class reference"},
     ]},
    about="amount / lifetime / explosiveness / one_shot — the four timing knobs",
    motion="Each property highlights on its spoken cue"))

b = base("B16", "From Rules to Godot's Nodes",
         "The process material is shared between 2D and 3D nodes. Its defaults are three-dimensional: "
         "gravity pointing down on the Y axis in 3D, spread that fans into all three axes. "
         "In a 2D game, particles without Disable Z set will spray into an axis the camera never shows. "
         "Always enable Disable Z for 2D effects. The official demo README says exactly this.")
beats.append(remotion_shot(b, "GodotDevWorkbench",
    {"mode": "code",
     "title": "ParticleProcessMaterial — 3D defaults (editor reconstruction)",
     "project": "CSYE 7270 walker-claude",
     "source": "Chapter 9 / ParticleProcessMaterial docs / official 2d/particles README",
     "code": GODOT_MATERIAL_INSPECTOR,
     "codeFontSize": 23,
     "treeLabel": "ParticleProcessMaterial",
     "inspectorLabel": "Inspector · 3D defaults, Disable Z highlighted",
     "notes": [
         {"label": "reconstruction", "value": "Godot editor reconstruction"},
         {"label": "source", "value": "Chapter 9; official Godot 2d/particles demo README"},
         {"label": "key warning", "value": "particle_flag_disable_z must be true for 2D effects"},
     ]},
    about="Process material 3D defaults; Disable Z required for 2D",
    motion="Property values appear; 'Disable Z' row highlighted in terracotta"))

b = base("B17", "From Rules to Godot's Nodes",
         "A particle node inherits its parent's transform and visibility. "
         "If the emitter's parent hides at the moment the effect should fire — "
         "a player dying, a pickup collected — the burst can be emitting and invisible. "
         "Parenting is a design choice, not a default. "
         "Choose the parent so the effect is still visible when it needs to be seen.")
beats.append(manim_shot(b, "B17_ParentingAndVisibility",
    about="Parenting trap: parent hides → child hidden even while emitting",
    motion="Scene tree shows Player parent fading; burst node dims; then Main parent shown as correct choice"))

b = base("B18", "From Rules to Godot's Nodes",
         "Replace the teaching simulation with a built-in node. Add G P U Particles 2D to a scene. "
         "Attach a Particle Process Material. Set the spread and velocity range. "
         "The node runs the same loop we built by hand — born, moved by the material's rules, drawn by its texture — "
         "but the engine handles the simulation. The artist still chooses the behavior.")
beats.append(remotion_shot(b, "GodotDevWorkbench",
    {"mode": "code",
     "title": "CPUParticles3D 'SignalBurst' — Inspector (editor reconstruction)",
     "project": "CSYE 7270 walker-claude",
     "source": "walker-claude/godot/signal-garden/effects/burst.tscn",
     "code": GODOT_BURST_INSPECTOR,
     "codeFontSize": 23,
     "treeLabel": "signal-garden/effects/burst.tscn",
     "inspectorLabel": "Inspector · from walker-claude source",
     "notes": [
         {"label": "reconstruction", "value": "Godot editor reconstruction"},
         {"label": "source", "value": "walker-claude/godot/signal-garden/effects/burst.tscn"},
         {"label": "node type", "value": "CPUParticles3D — amount=32, one_shot=true, explosiveness=1.0"},
     ]},
    about="Built-in particle node replacing hand-built loop — same rules, engine manages simulation",
    motion="Inspector values appear; correspondence to the hand-built loop is made explicit"))

# ── Closing ────────────────────────────────────────────────────────
b = base("BVDT", "Closing",
         "Let's recap with Claude. For C S Y E seventy-two seventy, Building Virtual Environments. "
         "A particle system is a birth-life-death loop running on each short-lived element. "
         "Position, velocity, and acceleration are three distinct jobs the update step handles every frame. "
         "Removal is load-bearing: without it, the population climbs without bound. "
         "Three settings — amount, lifetime, and explosiveness — determine how many particles appear and when. "
         "Godot separates emission, process, and draw: each part can be wrong on its own.",
         lane="bookend")
b["lead_silence_s"] = 0.5
beats.append(remotion_shot(b, "ClaudeVerdictArtifact",
    {"artifactTitle": "Recap",
     "artifactHeading": "What You Can Now Explain",
     "artifactLines": [
         "A particle is a short-lived element in a birth–life–death loop",
         "Position, velocity, and acceleration are three distinct update jobs",
         "Removal is load-bearing — without it, the population is unbounded",
         "amount × lifetime and explosiveness control how many appear and when",
         "Godot splits emission, process, and draw — each can fail independently",
         "Parenting determines visibility; choose it before the first emit",
     ],
     "lectureLayout": True,
     "brandLabel": "@NikBearBrown"},
    about="Recap — six statements, two per page",
    motion="Recap statements arrive two at a time"))

b = base("BHTF", "Closing",
         "Your turn. Make a fountain in a Godot teaching scene. "
         "Predict how wind and particle lifetime will change its shape, then change them separately. "
         "Your two checks: the population stops growing indefinitely; "
         "and the particles move in the direction you predicted.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeComposerAsk",
    {"greeting": "Your turn.",
     "topic": "YOUR TURN — Particle Fountain",
     "command": "Make a fountain in a Godot teaching scene. "
                "Predict how wind and particle lifetime will change its shape, then change them separately. "
                "Check: the population stops growing indefinitely; "
                "the particles move in the direction you predicted.",
     "output": [
         "Population settles — not growing without bound",
         "Particles move in the predicted direction after each change",
     ],
     "folderLabel": "@NikBearBrown"},
    about="Your Turn — fountain prediction task with two checks",
    motion="Prompt text types in; two check lines appear"))

b = base("BOUT", "Closing",
         "What Is a Particle System. At Nik Bear Brown.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeTitleOutro",
    {"title": TITLE,
     "handle": "@NikBearBrown",
     "seed": SLUG,
     "kind": "outro_voice"},
    about="Outro card",
    motion="Title + handle hold; 1 s silent tail"))
beats[-1]["silent_tail_s"] = 1.0

# ── Build sheet ────────────────────────────────────────────────────
sheet = {
    "metadata": {
        "slug": SLUG,
        "title": TITLE,
        "skill": "lecture",
        "style_preset": "lecture",
        "channel": CHANNEL,
        "channel_title": "@NikBearBrown",
        "persona": "Liam (in for Bear)",
        "voice": "am_onyx",
        "voice_kokoro": "am_onyx",
        "engine": "kokoro",
        "register": "Teardown",
        "clock": "narration",
        "palette": "claude",
        "fps": 24,
        "width": 3840,
        "height": 2160,
        "aspect_ratio": "16:9",
        "caption_policy": "sidecar",
        "course": COURSE,
        "playlist": PLAYLIST,
        "series_title": PLAYLIST,
        "lecture_opening_description": "Learn how one rule repeated thousands of times makes smoke, fire, and sparks",
        "lecture_opening_title_lines": ["What Is a", "Particle System?"],
        "lecture_opening_template": "lecture-title-slide-16x9",
        "source_doc": str(Path("/Users/bear/Downloads/seis-course-publish/chapters/09-particle-effects.md")),
        "audience": "CSYE 7270 students and independent Godot beginners",
        "tags": ["Godot", "particles", "VFX", "game development", "CSYE 7270", "Building Virtual Environments"],
        "bookend_exempt": ["cold-open"],
        "bookend_exempt_reason": "Lecture portrait/title opening replaces composer cold open.",
        "godot_capture_note": "All Godot editor views are source-backed reconstructions using GodotDevWorkbench, labeled as such. No display was available for live Godot captures in this build session.",
    },
    "beats": beats,
}

SHEET_PATH.write_text(json.dumps(sheet, indent=2, ensure_ascii=False))
total_est = sum(b.get("actual_duration_s", b["estimated_duration_s"]) for b in beats)
print(f"[make_sheet] Wrote {SHEET_PATH}")
print(f"[make_sheet] {len(beats)} beats, estimated runtime {total_est/60:.1f} min ({total_est:.0f} s)")
print(f"[make_sheet] Manim classes: {sum(1 for b in beats if b.get('shot',{}).get('type')=='GRAPHIC')}")
print(f"[make_sheet] Remotion beats: {sum(1 for b in beats if b.get('shot',{}).get('type')=='REMOTION')}")
