#!/usr/bin/env python3
"""
make_sheet.py — A Practical Godot VFX Library
Run from books/ or the reel folder. Writes beat_sheet.json.
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parent
SLUG = REEL.name
TITLE = "A Practical Godot VFX Library"
PLAYLIST = "CSYE 7270 Building Virtual Environments"
COURSE = "CSYE 7270 Building Virtual Environments"
CHANNEL = "claude-liam"

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

PARTICLE_MATERIAL_CODE = """# particle_material.tres — walker-3d-platformer
# Source: Chapter 9 / walker-3d-platformer/godot/
# Shared by: coin burst / enemy explosion / bullet glow
[resource]
script = null
render_priority = 0
shader_parameter/albedo = null
flags_unshaded = true
flags_do_not_receive_shadows = true
shading_mode = 1          # SHADING_MODE_UNSHADED
billboard_mode = 3        # BILLBOARD_PARTICLES
blend_mode = 1            # BLEND_MODE_ADD
params_billboard_keep_scale = true
proximity_fade_enabled = true
proximity_fade_distance = 0.1
# Applied via material_override on three CPUParticles3D nodes"""

beats = []

# ── Opening ─────────────────────────────────────────────────────────
b = base("BOPEN", "Opening",
         "C S Y E seventy-two seventy, Building Virtual Environments. "
         "A Practical Godot VFX Library. "
         "Two demo catalogs, one conversion, three engine comparisons, one reusable file.",
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
         "You've seen four node types, a timing model, and three sessions with an agent. "
         "What do you reach for next? "
         "Godot ships a catalog. Two demo scenes, not games. "
         "You read them like a library.",
         lane="bookend")
b["lead_silence_s"] = 0.8
b["qc"] = {"sparse_by_design": True, "sparse_reason": "Mandated writer bookend."}
beats.append(remotion_shot(b, "BrutalistHesitantWriter",
    {"text": "Godot ships a catalog. Two demo scenes, not games. "
             "You read them like a library.",
     "triggerWords": "not games",
     "replacementWords": "not games. You read them like a library.",
     "fontSize": 60, "charMs": 25, "hesitateBetween": 6, "hesitateWithin": 1,
     "mistakeRate": 3, "jitter": 20, "seed": SLUG, "banner": ""},
    about="Framing: demo scenes as a readable library",
    motion="Type the framing; add the correction"))

b = base("BDEFS", "Opening",
         "Feature catalogue. A scene whose purpose is to show what a system can do. "
         "Not a playable game. Not tested headlessly. "
         "A set of configured effects you read and port from. "
         "Compatibility renderer. The renderer that runs on the widest hardware: "
         "mobile, embedded, older GPUs. "
         "Particle trails and SDF collision are unsupported. The class reference confirms. "
         "Draw pass. One of a particle node's material slots. "
         "The process material decides where particles go. "
         "The draw pass decides what each particle looks like: its texture, blend mode, and shading. "
         "Tres file. A Godot resource file stored separately from any node, with a dot-tres extension. "
         "A particle draw material in its own file can be shared and referenced by multiple effects. "
         "FRICTIONAL dot MD. The human's record of a build: "
         "what the agent did, what you ran, what failed, what you saw on screen. "
         "The only evidence that an effect looks like anything.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [
         {"term": "feature catalogue",        "meaning": "A demo scene showing what a system can do — not a game; readable .tscn text"},
         {"term": "Compatibility renderer",   "meaning": "Widest hardware; particle trails and SDF collision unsupported"},
         {"term": "draw pass",               "meaning": "One material slot per particle node; decides look (texture, blend mode, shading)"},
         {"term": ".tres file",              "meaning": "Godot resource file stored separately; a draw material in its own file can be shared"},
         {"term": "FRICTIONAL.md",           "meaning": "Human's record: what the agent did, what you ran, what you saw — the only visual evidence"},
     ],
     "folderLabel": "@NikBearBrown"},
    about="5 prerequisite terms",
    motion="Terms arrive in spoken order"))

# ── Act 1 — The Godot Catalog ─────────────────────────────────────────
b = base("BACT1", "The Godot Catalog", "Act one. The Godot catalog.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 1", "subtitle": "The Godot Catalog",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B01", "The Godot Catalog",
         "The godot-demo-projects repository, pinned at commit a3b5c113, "
         "has a scene called 2d/particles. "
         "Seventeen GPU Particles 2D nodes. One scene. Mobile renderer. "
         "Each node is one pattern: a fountain, a fire, a trail, sparks, smoke, a galaxy, a flame thrower. "
         "There is no Walker adaptation. No test harness. No game logic. "
         "Every effect in it is readable. Open the .tscn file, "
         "trace each node's process material, port it to your project. "
         "That catalogue is the fastest particle library a Godot project can have.")
beats.append(manim_shot(b, "B01_TwoDCatalog",
    about="2d/particles: 17 GPUParticles2D nodes listed, Mobile renderer",
    motion="Effect dots appear in two batches; readable label appears"))

b = base("B02", "The Godot Catalog",
         "The same commit has 3d/particles. Forward Plus renderer. "
         "This scene exercises three GPU features that the 2D catalog does not show in action: "
         "trails, SDF collision, and attractors. "
         "Trail enabled: GPU nodes only. CPUParticles3D has no trail enabled at all, "
         "and Compatibility does not support it even on GPU nodes. "
         "SDF collision: particles that bounce off scene geometry. "
         "Needs depth rendering — Forward Plus or Mobile only. "
         "Attractors: velocity fields that shape all live particles. "
         "Everything in this catalog that uses trails, SDF collision, or sub-emitters "
         "requires Forward Plus or Mobile. On Compatibility, those effects don't run.")
beats.append(manim_shot(b, "B02_ThreeDCatalog",
    about="3d/particles: Forward+ — trails / SDF collision / attractors / sub-emitters",
    motion="Feature boxes appear in sequence; Compatibility note highlights"))

b = base("B03", "The Godot Catalog",
         "When you port an effect from a catalog, the three-part frame tells you what to carry. "
         "Emission: amount, lifetime, explosiveness, one-shot. "
         "These are on the node. They port directly between CPU and GPU. "
         "Process: velocity, gravity, spread, turbulence, attractors, sub-emitters. "
         "On GPU nodes these live in the Particle Process Material. "
         "On CPU nodes they are node properties. Sub-emitters and particle shaders are GPU only. "
         "Draw: the texture, the material, the blend mode. This is the draw pass. "
         "It is independent of whether you use CPU or GPU. "
         "A tres file for the draw half ports anywhere. "
         "The catalog tells you what effect exists. "
         "The frame tells you what to carry when you move it.")
beats.append(manim_shot(b, "B03_ThreePartFrame",
    about="Three-part frame: emission / process / draw and what ports where",
    motion="Three column headers appear; body fills per column"))

# ── Act 2 — Node Conversion ───────────────────────────────────────────
b = base("BACT2", "Node Conversion", "Act two. Node conversion.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 2", "subtitle": "Node Conversion",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B04", "Node Conversion",
         "The Godot editor converts a CPU Particles 2D to GPU Particles 2D "
         "with one button in the 2D toolbar. The 3D toolbar has the same option. "
         "What the conversion preserves: amount, lifetime, explosiveness, "
         "one-shot, local-coords, fixed FPS, and the timing model. "
         "The emission settings — spread, velocity range, gravity, lifetime randomness — "
         "move from node properties into a new Particle Process Material. "
         "What you gain: the GPU node now has sub-emitter, trail enabled, "
         "and a process material that supports turbulence, attractors, and collision. "
         "CPU to GPU is additive. You keep the effect and gain features.")
beats.append(manim_shot(b, "B04_CPUToGPU",
    about="CPU→GPU: preserved properties; new ParticleProcessMaterial; gained features",
    motion="CPU box lists properties; arrow appears; GPU box gains features"))

b = base("B05", "Node Conversion",
         "Converting from GPU Particles 2D to CPU Particles 2D is a one-way degradation. "
         "Most emission settings survive. "
         "The process material becomes node properties for the settings that have equivalents. "
         "What cannot survive: sub-emitter. Trail enabled. Particle shaders. "
         "The process material's turbulence, attractors, and collision. "
         "If an effect uses any of those, converting to CPU changes the effect. "
         "A particle shader becomes a plain process material with whatever settings can be matched. "
         "A sub-emitter chain disappears entirely. "
         "GPU to CPU is not the same effect on different hardware. "
         "It is a simpler effect on wider hardware.")
beats.append(manim_shot(b, "B05_GPUToCPU",
    about="GPU→CPU: sub_emitter / trail_enabled / shaders cannot survive — lossy path",
    motion="Loss crosses appear in two batches; note appears"))

b = base("B06", "Node Conversion",
         "Every effect in your library should carry a renderer tag. "
         "Compatibility: the widest target. Particle trails: unsupported. "
         "SDF collision: unsupported. "
         "emit-particle, the scripted spawn method on GPU nodes: "
         "Forward Plus or Mobile only. Effects built for Compatibility cannot use any of those. "
         "Mobile: modern devices. Trails work. SDF collision works. emit-particle works. "
         "Forward Plus: the full feature set. Everything works, "
         "including the 3D demo's sub-emitter chains and attractor fields. "
         "A library that does not tag renderer requirements "
         "will fail on the wrong machine without a clear error.")
beats.append(manim_shot(b, "B06_CompatibilityMap",
    about="Three-renderer table: Compatibility / Mobile / Forward+ vs particle features",
    motion="Renderer headers appear; feature rows fill with check/cross marks"))

# ── Act 3 — Cross-Engine Map ──────────────────────────────────────────
b = base("BACT3", "Cross-Engine Map", "Act three. Cross-engine map.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 3", "subtitle": "Cross-Engine Map",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B07", "Cross-Engine Map",
         "Unity's two particle systems map directly to Godot's two families. "
         "The Built-in Particle System is CPU-simulated. "
         "Its scene files serialise as YAML. An agent can read them, diff them, edit them. "
         "The sub-emitter mechanism is the Sub Emitters module. "
         "The equivalent of Godot's finished signal is OnParticleSystemStopped. "
         "The Visual Effect Graph is GPU-simulated. Its assets are dot-vfx files. "
         "VFX Graph assets are not described as text-diffable by Unity's documentation. "
         "An agent cannot inspect the emitter stack the way it reads a .tscn. "
         "For the death burst: one-shot maps to Looping off; "
         "amount plus explosiveness one maps to Spawn Burst Instantaneous; "
         "finished maps to OnParticleSystemStopped.")
beats.append(manim_shot(b, "B07_UnityComparison",
    about="Unity Built-in (CPU, YAML readable) vs VFX Graph (GPU, binary) vs Godot",
    motion="Comparison table rows appear in sequence"))

b = base("B08", "Cross-Engine Map",
         "Unreal Engine's Niagara is one particle system with CPU and GPU "
         "selectable per emitter via the Sim Target setting. "
         "The one-shot burst: Emitter State with Loop Behavior Once — Godot's one-shot. "
         "Spawn Burst Instantaneous with a count of 32 — Godot's amount with explosiveness one. "
         "The equivalent of finished is UNiagara Component dot OnSystemFinished. "
         "Niagara systems are stored as dot-uasset files. "
         "Epic's own source-control documentation confirms they are binary "
         "and cannot be opened as text or merged with text tools. "
         "An agent can write the C++ that spawns the system "
         "and can drive the editor with the Python Editor Script Plugin. "
         "Niagara events — the sub-emitter mechanism — work on CPU simulation only. "
         "Godot's sub-emitters are GPU only. The two are mirrors of each other.")
beats.append(manim_shot(b, "B08_UnrealNiagara",
    about="Unreal Niagara: Sim Target, .uasset binary, CPU-only events",
    motion="Comparison table rows appear in sequence"))

b = base("B09", "Cross-Engine Map",
         "The practical difference for agent work is file format. "
         "A Godot scene file is plain text. "
         "A particle node's configuration, its process material, "
         "and its sub-emitter reference are all visible in the .tscn. "
         "The draw material is in a .tres. "
         "An agent can read both, run a diff, and verify specific properties without running the game. "
         "Unity prefabs are YAML — the Built-in system is readable. VFX Graph assets are not. "
         "Unreal's .uasset is binary for all visual content. "
         "That is why the Chapter 9 agent could confirm that DeathBurst is a child of Main, "
         "that its process material has particle-flag-disable-z set to true, "
         "and that its texture is a GradientTexture2D — from the scene file, "
         "before a single test ran. "
         "No other engine in this course gives agents that reach into a particle configuration.")
beats.append(manim_shot(b, "B09_TscnAdvantage",
    about=".tscn text vs binary: Godot agent reads config; Unity/Unreal cannot",
    motion="Engine rows appear; reach labels highlight green/red"))

# ── Act 4 — Building Your Library ────────────────────────────────────
b = base("BACT4", "Building Your Library", "Act four. Building your library.", lane="bookend")
b["proof_gate"] = "CARD"
beats.append(remotion_shot(b, "FormACard",
    {"title": "Act 4", "subtitle": "Building Your Library",
     "backgroundColor": "#F2F0E9", "textColor": "#3D3929", "accentColor": "#D97757"},
    about="Act divider", motion="Card appears"))

b = base("B10", "Building Your Library",
         "Walker-3d-platformer's particle-material-dot-tres is a Standard Material 3D in its own file, "
         "with four flags: additive blend mode, unshaded shading mode, "
         "particle billboard mode, proximity fade enabled. "
         "The coin burst, the enemy explosion, and the bullet glow "
         "all reference the same file via material-override. "
         "Change additive to alpha-blend for smoke: one edit, three effects update. "
         "The draw half is stable. "
         "For a given art style, the blend mode and billboard mode do not change between effects. "
         "What changes is the process material — velocity, spread, lifetime randomness. "
         "Keep the draw half in a named file. Reference it everywhere.")
beats.append(manim_shot(b, "B10_TresPattern",
    about="particle_material.tres: one file shared by three effects via material_override",
    motion="Central .tres box appears; three effect boxes fan out with arrows"))

b = base("B11", "Building Your Library",
         "A practical VFX library entry has five fields. "
         "Name: what the effect is called in this project. "
         "Renderer: Compatibility, Mobile, or Forward Plus. The minimum needed to run the effect. "
         "Node type: CPU or GPU. "
         "CPU runs anywhere within its renderer; GPU gains sub-emitters, trails, and shaders. "
         "Draw material: the tres file this effect uses for its draw pass. "
         "Shared effects point to the same file. "
         "Test status: what the headless test establishes. "
         "Not what it proves visually — what it checks in state. "
         "Build one card per effect before you build the effect. "
         "It answers the questions your prompt needs to ask.")
beats.append(manim_shot(b, "B11_LibraryCard",
    about="Library entry: name / renderer / node type / .tres / test status",
    motion="Five field rows appear; dots then labels"))

b = base("B12", "Building Your Library",
         "Here is particle-material-dot-tres as the Godot editor shows it. "
         "A Standard Material 3D. Four flags. "
         "Blend mode: additive. Shading mode: unshaded. "
         "Billboard mode: particle. Proximity fade: enabled. "
         "Applied via material-override to the coin burst, "
         "the enemy explosion, and the bullet glow in walker-3d-platformer. "
         "Copy this file into any 3D particle project. "
         "Change additive to alpha-blend for smoke. "
         "Change proximity-fade-distance to control the softness of the fade at geometry edges. "
         "The pattern holds.")
beats.append(remotion_shot(b, "GodotDevWorkbench",
    {"mode": "code",
     "project": "CSYE 7270 walker-3d-platformer",
     "source": "Chapter 9 / walker-3d-platformer/godot/particle_material.tres",
     "code": PARTICLE_MATERIAL_CODE,
     "codeFontSize": 24,
     "treeLabel": "Shared draw material — 3 effects",
     "inspectorLabel": "particle_material.tres · Chapter 9 source",
     "notes": [
         {"label": "blend mode", "value": "additive — sparks and fire"},
         {"label": "shading", "value": "unshaded — ignores scene lights"},
         {"label": "billboard", "value": "BILLBOARD_PARTICLES — always faces camera"},
         {"label": "shared by", "value": "coin burst / enemy explosion / bullet glow"},
     ]},
    about="particle_material.tres: four flags, referenced by three CPUParticles3D nodes",
    motion="Code panel shows .tres content; notes show flag purposes"))

# ── Closing ─────────────────────────────────────────────────────────
b = base("BVDT", "Closing",
         "Here is what a practical library gives you. "
         "The Godot catalog: 2D has 17 GPU effects on Mobile. "
         "3D has trails, attractors, SDF collision, and sub-emitters on Forward Plus. "
         "Both are plain text .tscn files. Neither has a Walker adaptation. "
         "Conversion: CPU to GPU gains a process material and all GPU features. "
         "GPU to CPU loses sub-emitters, trails, and shaders. "
         "Compatibility drops trails and SDF collision entirely. "
         "Tag every library effect with its renderer requirement. "
         "Cross-engine: Godot's text scene format gives agents the most reach. "
         "Unity's Built-in YAML is readable. VFX Graph and Niagara assets are binary. "
         "Agents can configure the spawn call in code; "
         "they cannot inspect the full effect stack from a file. "
         "The tres pattern: one draw material file, shared by multiple effects. "
         "Change the look once. Port the file to the next project.",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeVerdictArtifact",
    {"title": "Practical VFX Library — What You Have",
     "verdictLabel": "Library gains",
     "verdict": "catalog · conversion · cross-engine map · .tres pattern",
     "items": [
         "✓  2d/particles — 17 GPU effects, Mobile renderer, readable .tscn",
         "✓  3d/particles — trails / SDF collision / attractors / sub-emitters, Forward+",
         "✓  CPU→GPU: additive; GPU→CPU: lossy (sub-emitter, trail, shaders gone)",
         "✓  Compatibility: trails and SDF collision unsupported — tag every effect",
         "✓  Godot .tscn: agent reads particle config directly; Unity VFX / Niagara: binary",
         "✓  .tres pattern: one draw file shared across multiple effects",
         "=  Build the library entry card before the effect",
         "=  FRICTIONAL.md is the only evidence the effect looks like anything",
     ],
     "folderLabel": "@NikBearBrown"},
    about="Verdict: catalog / conversion / cross-engine / .tres pattern",
    motion="Verdict card appears; items populate"))

b = base("BHTF", "Closing",
         "Open godot-demo-projects at commit a3b5c113. Navigate to 2d/particles. "
         "Read the .tscn file. "
         "Which of the 17 effects uses sub-emitters? Which uses collision? "
         "Which would stop working on Compatibility? "
         "Pick one effect and convert it to CPU Particles 2D in the editor. "
         "Which properties survive intact? Which disappear? "
         "If a property disappears, where did its settings go?",
         lane="bookend")
beats.append(remotion_shot(b, "ClaudeComposerAsk",
    {"prompt": "Open godot-demo-projects at commit a3b5c113. Open 2d/particles. "
               "Which effects use sub-emitters or collision? Which are Compatibility-safe? "
               "Convert one effect to CPUParticles2D. What survives the conversion?",
     "folderLabel": "@NikBearBrown"},
    about="Your turn: catalog exploration + conversion exercise",
    motion="Composer card prompts the viewer"))

b = base("BOUT", "Closing",
         "A Practical Godot VFX Library. At Nik Bear Brown.",
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
        "source_chapter": "09-particle-effects.md (cross-engine / demo catalog / .tres pattern)",
        "film_number": 4,
    },
    "beats": beats,
}

SHEET_PATH.write_text(json.dumps(sheet, indent=2))
print(f"[make_sheet] wrote {len(beats)} beats → {SHEET_PATH}")
