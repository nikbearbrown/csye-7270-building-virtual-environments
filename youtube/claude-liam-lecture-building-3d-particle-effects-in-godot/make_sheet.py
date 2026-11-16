#!/usr/bin/env python3
"""
make_sheet.py — Building 3D Particle Effects in Godot
Run from books/ or the reel folder. Writes beat_sheet.json.
"""
import json, math, re, hashlib
from pathlib import Path

REEL = Path(__file__).resolve().parent
SLUG = REEL.name
TITLE = "Building 3D Particle Effects in Godot"
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

# Godot reconstruction — coin burst from walker-3d-platformer
COINBURST_CODE = """# coin.tscn — CoinBurst node (Godot editor reconstruction)
# Source: Chapter 9 / walker-3d-platformer
# Trigger: take animation → CPUParticles3D:emitting = true at t=0
[node name="CoinBurst" type="CPUParticles3D" parent="."]
emitting = false
amount = 16
lifetime = 0.5
lifetime_randomness = 0.2
one_shot = true
explosiveness = 1.0
emission_shape = 1          # EMISSION_SHAPE_SPHERE
draw_pass_1 = SubResource("QuadMesh_coin")
material_override = "res://particle_material.tres"

# particle_material.tres — StandardMaterial3D (reusable)
flags_unshaded = true
billboard_mode = 3           # BILLBOARD_PARTICLES
blend_mode = 1               # BLEND_MODE_ADD
proximity_fade_enabled = true
proximity_fade_distance = 0.1"""

beats = []

# ── Opening ─────────────────────────────────────────────────────────
b = base("BOPEN", "Opening",
         "C S Y E seventy-two seventy, Building Virtual Environments. "
         "Building 3D Particle Effects in Godot. "
         "One coin burst, four acts, three features that only GPU nodes have.",
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
         "In 3D, particle effects are the same loop: born, move, die. "
         "But you pick up one more axis, one more renderer decision, "
         "and three new features that only GPU nodes have. "
         "The traps are the same. The surprises are new.",
         lane="bookend")
b["lead_silence_s"] = 0.8
b["qc"] = {"sparse_by_design": True, "sparse_reason": "Mandated writer bookend."}
beats.append(remotion_shot(b, "BrutalistHesitantWriter",
    {"text": "In 3D, particle effects are the same loop. "
             "But three new features only GPU nodes have.",
     "triggerWords": "only GPU nodes have",
     "replacementWords": "only GPU nodes have. The traps are the same. The surprises are new.",
     "fontSize": 60, "charMs": 25, "hesitateBetween": 6, "hesitateWithin": 1,
     "mistakeRate": 3, "jitter": 20, "seed": SLUG, "banner": ""},
    about="Framing: same loop, new axis, GPU-only features",
    motion="Type the naive question; add the correction"))

b = base("BDEFS", "Opening",
         "Sub-emitter. A second GPU particle system that spawns particles from the first one's particles. "
         "When a spark dies, it can leave a puff. CPU nodes have no sub-emitter at all. "
         "Particle shader. A shader whose first line is shader-type particles. "
         "It runs before drawing, not after. "
         "It writes TRANSFORM, VELOCITY, and COLOR for each particle per frame. Only GPU nodes support it. "
         "Billboard. A draw mode where each particle's quad always faces the camera. "
         "Required for round soft dots that stay round regardless of camera angle. "
         "Proximity fade. A material flag that fades a particle out as it gets close to geometry. "
         "Without it, soft particles clip hard into floors and walls. "
         "Visibility A-A-B-B. The 3D axis-aligned bounding box the engine checks to decide "
         "whether to simulate a particle node at all. "
         "Too small: effect vanishes when the node is only partly visible. Too large: simulation runs off-screen.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [
         {"term": "sub_emitter",        "meaning": "Second GPU particle system spawned from the first; CPU nodes have none"},
         {"term": "particle shader",    "meaning": "shader_type particles; runs before drawing; writes TRANSFORM, VELOCITY, COLOR; GPU-only"},
         {"term": "billboard",          "meaning": "Draw mode where each quad always faces the camera — keeps round dots round"},
         {"term": "proximity_fade",     "meaning": "Material flag: fades particle near geometry instead of clipping through it"},
         {"term": "visibility_aabb",    "meaning": "3D bounding box the engine checks to cull simulation; wrong size wastes or breaks effects"},
     ],
     "folderLabel": "@NikBearBrown"},
    about="5 prerequisite terms",
    motion="Terms arrive in spoken order"))

# ── Act 1 — CPU vs GPU in 3D ─────────────────────────────────────────
b = base("BACT1", "CPU vs GPU in 3D", "Act one. CPU versus GPU in 3D.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 1", "subtitle": "CPU vs GPU in 3D",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B01", "CPU vs GPU in 3D",
         "The walker-3D-platformer is a Forward Plus 3D game. It uses CPU Particles 3D for three distinct effects. "
         "The coin burst: 16 particles, one-shot, explosiveness one, sphere emission shape, "
         "lifetime 0.5, lifetime randomness 0.2. The coin fires it when its take animation starts. "
         "The enemy explosion: 16 particles, one-shot, explosiveness one. "
         "Mesh particles — each one is a full piece of geometry, not a texture quad. "
         "The enemy's explode animation fires it. "
         "The bullet glow: 16 particles, lifetime 0.4, looping. It runs continuously behind each bullet. "
         "Three effects, three timing modes, one node type — "
         "and none of them have sub-emitters, trails, or particle shaders. CPU nodes don't.")
beats.append(manim_shot(b, "B01_ThreeEffects",
    about="Three CPUParticles3D effects: coin burst / enemy explosion / bullet glow",
    motion="Effect cards appear in sequence with property tables"))

b = base("B02", "CPU vs GPU in 3D",
         "The same feature gap from the 2D side exists in 3D. "
         "GPU Particles 3D: process material is a Particle Process Material on the node. "
         "Sub-emitter exists. Trail enabled exists. Particle shaders work. "
         "CPU Particles 3D: the settings that would be on a process material "
         "are instead direct properties of the node. "
         "No sub-emitter. No trail enabled. No particle shaders. "
         "Wider hardware, fewer features. "
         "The 3D manual says so: CPU particles work on a wider range of hardware "
         "but there are no plans to add new features to CPU Particles — same for 3D.")
beats.append(manim_shot(b, "B02_CPUvsGPU3D",
    about="Feature comparison: GPUParticles3D vs CPUParticles3D",
    motion="Comparison rows appear; GPU-only features highlighted"))

b = base("B03", "CPU vs GPU in 3D",
         "Here is where agents get lost. A particle effect starts. "
         "Nothing in the code calls restart or sets emitting. "
         "The agent searches every script. It can't find it. "
         "Look in the animations. "
         "The coin's take animation track has one key at time zero: "
         "CPU Particles 3D colon emitting set to true. "
         "The enemy's explode animation has the same key for its Explosion node. "
         "The animation player is the trigger. "
         "An Animation Player can key any exported property on any node in the scene tree. "
         "Emitting is an exported property. "
         "When an agent says it cannot find where the effect starts, "
         "check the animation tracks before opening a new prompt.")
beats.append(manim_shot(b, "B03_AnimTrack",
    about="AnimationPlayer keying CPUParticles3D:emitting at t=0",
    motion="Animation track diagram builds; key at t=0 highlighted"))

# ── Act 2 — Sub-Emitters ─────────────────────────────────────────────
b = base("BACT2", "Sub-Emitters", "Act two. Sub-emitters.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 2", "subtitle": "Sub-Emitters",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B04", "Sub-Emitters",
         "A sub-emitter is a GPU particle system that spawns new particles "
         "from the first system's particles. "
         "Set sub-emitter-mode on the process material, point sub-emitter to a sibling node, "
         "and each particle in the parent system can spawn a batch of particles from the child. "
         "AT END means: when a parent particle dies, fire the sub-emitter at that location. "
         "Sparks that each leave a puff as they die are an AT END sub-emitter. "
         "AT COLLISION requires the particle to hit geometry — "
         "which needs the renderer's SDF collision support. "
         "AT START fires at birth. CONSTANT fires continuously from live particles.")
beats.append(manim_shot(b, "B04_SubEmitterChain",
    about="Sub-emitter chain: parent → AT_END → child at particle death",
    motion="Chain diagram builds left to right; AT_END trigger highlighted"))

b = base("B05", "Sub-Emitters",
         "The sub-emitter-mode enum on Godot 4.7.2. "
         "DISABLED — no sub-emitter. "
         "CONSTANT — sub-particles spawn continuously from live parent particles. "
         "AT END — sub-particles spawn when a parent particle dies. "
         "AT COLLISION — sub-particles spawn when a parent particle hits geometry. "
         "Needs SDF collision, Forward Plus or Mobile renderer. "
         "AT START — sub-particles spawn when a parent particle is born.")
beats.append(manim_shot(b, "B05_SubEmitterModes",
    about="sub_emitter_mode enum: DISABLED / CONSTANT / AT_END / AT_COLLISION / AT_START",
    motion="Enum rows appear in order; AT_COLLISION constraint noted"))

b = base("B06", "Sub-Emitters",
         "Three things the sub-emitter documentation says that agents miss. "
         "One: a system used as a sub-emitter stops emitting, "
         "even if the Emitting property was checked in the inspector. "
         "It only emits when the parent system drives it. "
         "Two: the sub-emitter's own Amount is its total particle budget. "
         "The parent's particle count does not multiply it. "
         "If the sub-emitter has Amount 8, it has at most 8 particles, "
         "however many parents spawn it. "
         "Three: a system cannot be its own sub-emitter. "
         "CPU nodes have no sub-emitters. Full stop.")
beats.append(manim_shot(b, "B06_SubEmitterSurprises",
    about="Three sub-emitter gotchas: stops own emitting / capped amount / no self-sub",
    motion="Three gotcha cards appear in sequence"))

# ── Act 3 — Particle Shaders ─────────────────────────────────────────
b = base("BACT3", "Particle Shaders", "Act three. Particle shaders.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 3", "subtitle": "Particle Shaders",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B07", "Particle Shaders",
         "When the Particle Process Material's checkboxes run out, "
         "replace it with a Shader Material whose shader begins shader-type particles. "
         "The shader runs before drawing — it does not draw anything itself. "
         "It has two functions: start, called for a newly born particle, "
         "and process, called every frame for every live particle. "
         "You write to built-ins: "
         "TRANSFORM gives position and orientation, VELOCITY gives motion, "
         "COLOR changes the tint. ACTIVE lets you kill a particle early by setting it to false. "
         "Two booleans tell you when a particle is new: "
         "RESTART POSITION and RESTART VELOCITY, both true when the particle is first born. "
         "EMISSION TRANSFORM gives you the emitter's transform for positioning.")
beats.append(manim_shot(b, "B07_ShaderStructure",
    about="Particle shader anatomy: shader_type particles; start()/process(); built-ins",
    motion="Shader structure appears line by line; built-ins labeled"))

b = base("B08", "Particle Shaders",
         "A particle shader compiles in headless mode. "
         "The dummy renderer does not simulate particles, "
         "but it does compile shader source through its material storage. "
         "That is useful. You can give an agent a shader, run Godot headless, "
         "and catch type errors before opening a window. "
         "A minimal working shader parses clean. "
         "A deliberately broken copy — with VELOCITY equals vec2 of 1.0 — "
         "is rejected with: SHADER ERROR, "
         "Invalid arguments to operator equals: vec3, vec2. "
         "The headless run finds the type error. "
         "What the particles then look like was not checked. The compiler cannot see that.")
beats.append(manim_shot(b, "B08_HeadlessCompile",
    about="Headless shader compile: valid → OK; vec2 assign → ERROR",
    motion="Two terminal outputs appear: clean shader then broken shader with error"))

b = base("B09", "Particle Shaders",
         "Over the process material, a particle shader adds three things. "
         "Custom forces. Turbulence, vortices, attractors based on any math you write — "
         "anything that can be expressed in GLSL. "
         "The material gives you built-in turbulence and attractors; "
         "the shader gives you anything. "
         "Procedural emission shapes. The material's emission shape is a fixed enum. "
         "A shader can emit from any shape: a parametric curve, a mesh sampled by UV, a grid. "
         "The CUSTOM channel. Four floats per particle, computed in start or process, "
         "readable in the draw shader. "
         "It passes per-particle data from the simulation to the visual — "
         "a fire particle can pass its temperature as a CUSTOM float "
         "and the draw shader uses it to pick colour.")
beats.append(manim_shot(b, "B09_ShaderVsMaterial",
    about="What a shader adds: custom forces / procedural shapes / CUSTOM channel",
    motion="Three-column table appears; each column fills with examples"))

# ── Act 4 — The Draw Half ─────────────────────────────────────────────
b = base("BACT4", "The Draw Half", "Act four. The draw half.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 4", "subtitle": "The Draw Half",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B10", "The Draw Half",
         "Simulation and drawing are separate. "
         "The process material or shader runs the loop. "
         "A separate material — applied to the particle node's draw passes — "
         "decides what each particle looks like. "
         "In walker-3d-platformer, that is particle-material-dot-tres. "
         "A Standard Material 3D with four specific flags. "
         "Blend mode: additive. Particles that overlap add their brightness together. "
         "Smoke uses alpha blend; sparks and fire use additive. "
         "Shading mode: unshaded. The particle ignores the scene's lights. "
         "A spark that dims in shadow looks wrong — leave it unshaded. "
         "Billboard mode: particle. Each quad always faces the camera. "
         "Turn this off and a round soft dot becomes an angled diamond as the camera moves. "
         "Proximity fade: enabled. "
         "The particle fades out near geometry instead of clipping through it hard.")
beats.append(manim_shot(b, "B10_DrawMaterial",
    about="StandardMaterial3D flags: additive / unshaded / billboard / proximity_fade",
    motion="Four flag cards appear; each with diagram of effect vs no-flag"))

b = base("B11", "The Draw Half",
         "Six levers for particle cost, regardless of CPU or GPU. "
         "Amount — the direct multiplier. Halve the amount, halve the simulation work. "
         "Lifetime — at a fixed amount, a longer lifetime means fewer births per second "
         "and a larger spread, but still at most amount particles alive at once. "
         "Fixed FPS — update less often. "
         "30 updates per second instead of 60 halves the simulation calls "
         "without halving the visual frame rate. Interpolation fills the gaps. "
         "Visibility A-A-B-B — if the bounding box is too small, the effect turns off "
         "when the node is only partly visible. "
         "Too large: simulation runs even when the effect is fully off-screen. "
         "Set it to the real footprint. "
         "Texture size — a 512-pixel transparent soft dot costs more fill rate than a 64-pixel one. "
         "Overdraw from transparent, overlapping quads is the GPU cost "
         "the Profiler needs a real renderer to measure. "
         "Chapter 13 has the Profiler. That is where GPU costs land.")
beats.append(manim_shot(b, "B11_CostLevers",
    about="Six cost levers: amount / lifetime / fixed_fps / visibility_aabb / texture_size / overdraw",
    motion="Six cards appear in sequence; each with cost direction arrow"))

b = base("B12", "The Draw Half",
         "Here is the coin burst from walker-3d-platformer as the editor shows it. "
         "CPU Particles 3D. Amount 16. One shot. Explosiveness one. "
         "Sphere emission shape — particles born from the surface of an invisible sphere, "
         "not from a single point. "
         "Lifetime 0.5. Lifetime randomness 0.2 — each particle lives between 0.4 and 0.6 seconds. "
         "The draw material: particle-material-dot-tres, "
         "a Standard Material 3D with additive blending, unshaded shading, "
         "particle billboarding, and proximity fade. "
         "This is a complete minimal effect: "
         "the simulation half on the node, the draw half in its own reusable file.")
beats.append(remotion_shot(b, "GodotDevWorkbench",
    {"mode": "code",
     "project": "CSYE 7270 walker-3d-platformer",
     "source": "Chapter 9 / walker-3d-platformer/godot/coin.tscn + particle_material.tres",
     "code": COINBURST_CODE,
     "codeFontSize": 23,
     "treeLabel": "Scene — CoinBurst under Coin",
     "inspectorLabel": "CoinBurst config · Chapter 9 source",
     "notes": [
         {"label": "reconstruction", "value": "Godot editor reconstruction"},
         {"label": "trigger", "value": "take animation → emitting=true at t=0"},
         {"label": "draw material", "value": "particle_material.tres — reusable StandardMaterial3D"},
     ]},
    about="Coin burst: simulation half on node, draw half in reusable tres file",
    motion="Code panel shows node config and material; notes show trigger"))

# ── Closing ─────────────────────────────────────────────────────────
b = base("BVDT", "Closing",
         "Here is what 3D adds over 2D. "
         "Sub-emitters — GPU nodes only, four trigger modes. "
         "Particle shaders — GPU nodes only; headless compilation catches type errors. "
         "Visibility A-A-B-B — the 3D equivalent of visibility rect; set it to the real footprint. "
         "Draw material flags — additive blend, unshaded, billboard, proximity fade; "
         "keep them in a reusable tres file. "
         "Animation track triggers — any exported property, including emitting, can be keyed. "
         "Here is what stays the same. "
         "One shot, explosiveness, lifetime, restart — identical contracts in 3D. "
         "The process material is still 3D — no Disable Z trap in a 3D game, "
         "but the material's 3D defaults mean gravity is still minus 9.8 on Y. "
         "Headless limits — the dummy renderer still does no GPU simulation and no drawing. "
         "State checks work. Visual checks don't. "
         "New trap: the sub-emitter stops its own emitting. "
         "Check that before assuming it's broken.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeVerdictArtifact",
    {"title": "3D Particles — What Changes",
     "verdictLabel": "3D adds",
     "verdict": "sub-emitters · particle shaders · visibility_aabb · draw material flags · anim triggers",
     "items": [
         "✓  sub_emitter — GPU-only; 4 trigger modes (CONSTANT / AT_END / AT_COLLISION / AT_START)",
         "✓  particle shader — GPU-only; headless compile catches type errors",
         "✓  visibility_aabb — 3D culling box; wrong size breaks or wastes simulation",
         "✓  draw material flags — additive, unshaded, billboard, proximity_fade in a reusable .tres",
         "✓  AnimationPlayer can key CPUParticles3D:emitting at t=0",
         "=  one_shot / explosiveness / lifetime / restart — same contracts as 2D",
         "=  process_material still 3D defaults — gravity −9.8 Y still applies",
         "=  headless: state checks work; visual checks don't",
         "!  new trap — sub-emitter stops its own emitting when parented",
     ],
     "folderLabel": "@NikBearBrown"},
    about="Verdict: what 3D adds, what stays same, new trap",
    motion="Verdict card appears; items populate in sequence"))

b = base("BHTF", "Closing",
         "Open walker-3d-platformer. Find the coin burst. "
         "Convert CPU Particles 3D to GPU Particles 3D. "
         "What becomes possible? "
         "Add a sub-emitter: AT END, a small puff where each coin particle dies. "
         "What breaks if you leave the renderer on Forward Plus? "
         "Then measure: run the particle-cost script from Chapter 9 with dash-dash fixed-fps 60. "
         "Does GPU Particles 3D still cost near zero headless? "
         "Is that useful information?",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeComposerAsk",
    {"prompt": "Open walker-3d-platformer. Convert the coin burst CPUParticles3D to GPUParticles3D. "
               "Add a sub-emitter: AT_END, a small puff where each coin particle dies. "
               "Run --fixed-fps 60. Does GPUParticles3D still cost near zero headless?",
     "folderLabel": "@NikBearBrown"},
    about="Your turn: CPU→GPU conversion + sub-emitter + cost measurement",
    motion="Composer card prompts the viewer"))

b = base("BOUT", "Closing",
         "Building 3D Particle Effects in Godot. At Nik Bear Brown.",
         lane="bookend")
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
        "source_chapter": "09-particle-effects.md (3D hands-on section)",
        "film_number": 3,
    },
    "beats": beats,
}

SHEET_PATH.write_text(json.dumps(sheet, indent=2))
print(f"[make_sheet] wrote {len(beats)} beats → {SHEET_PATH}")
