#!/usr/bin/env python3
"""
make_sheet.py — Adding Particle Effects to Walker Claude
Run from books/ or the reel folder. Writes beat_sheet.json.
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parent
SLUG = REEL.name
TITLE = "Adding Particle Effects to Walker Claude"
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
            {"at": 0,    "event": "Establish geometry"},
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
    b["shot"] = {"type": "CARD", "source": "own", "visual_intent": about}
    return b

# ── GDScript code for B12 ─────────────────────────────────────────────
GAME_OVER_CODE = """\
# game_over() — two lines added:
func game_over():
    $DeathBurst.global_position = \\
        $Player.global_position
    $DeathBurst.restart()
    ...

# DeathBurst (GPUParticles2D child of Main):
# emitting: false
# one_shot: true
# explosiveness: 1.0
# amount: 32  |  lifetime: 0.6 s
# texture: GradientTexture2D 16x16 radial
# particle_flag_disable_z: true
# spread: 180  |  velocity: 150-300 px/s
# gravity: 0   |  scale ramp: 1→0
# color ramp: opaque→transparent\
"""

beats = []

# ── BOPEN ─────────────────────────────────────────────────────────────
b = base("BOPEN", "open", "", lane="open")
card_shot(b, "Title card: Adding Particle Effects to Walker Claude")
beats.append(b)

# ── BIDEA ─────────────────────────────────────────────────────────────
BIDEA_NAR = (
    "The player dies. Something should burst where they stood. "
    "A headless test prints: PASS emitting after hit. "
    "Is there a burst? "
    "Probably. But the burst could be invisible. Its particles could each be one pixel wide. "
    "It could be spraying into an axis the camera never shows. "
    "And the test cannot see any of that. "
    "The gap between state and sight is what this lecture is about."
)
b = base("BIDEA", "open", BIDEA_NAR, lane="open")
remotion_shot(b, "BrutalistHesitantWriter", {
    "question": "Is there a burst?",
    "correction": "The test proves state. Only a screen proves sight."
}, "Hesitant writer: headless limits framing", "Writer types the corrected question")
beats.append(b)

# ── BDEFS ─────────────────────────────────────────────────────────────
BDEFS_NAR = (
    "Five terms. "
    "One-shot: the particle node fires once and stops — one emission cycle, then done. "
    "Explosiveness: how bunched the births are — one-point-zero means all at once, a true burst. "
    "ParticleProcessMaterial: the shared ruleset governing how GPU particles move — spread, velocity, gravity, scale curve, color ramp. "
    "Lambda capture: GDScript lambdas copy outer local variables — the lambda cannot write back to the original. "
    "Fixed-fps: runs the frame loop at a set rate, bypassing the idle sleep that otherwise hides real costs."
)
b = base("BDEFS", "open", BDEFS_NAR, lane="open")
remotion_shot(b, "ClaudeDefinitions", {
    "terms": [
        {"term": "one_shot", "definition": "fires once — one emission cycle, then stops"},
        {"term": "explosiveness", "definition": "1.0 = all particles born at once — a true burst"},
        {"term": "ParticleProcessMaterial", "definition": "GPU particle ruleset: spread, velocity, gravity, ramps"},
        {"term": "lambda capture", "definition": "GDScript lambdas copy outer locals — cannot write back"},
        {"term": "fixed_fps", "definition": "fixed frame rate — bypasses the 6.9 ms idle sleep"},
    ]
}, "Five key terms", "Terms fade in one by one")
beats.append(b)

# ── BACT1 ─────────────────────────────────────────────────────────────
b = base("BACT1", "act1", "", lane="act")
remotion_shot(b, "FormACard", {"actLabel": "Act 1", "title": "The Death Burst"},
              "Act 1 card", "Card wipes in")
beats.append(b)

# ── B01: Three-Part Model ─────────────────────────────────────────────
B01_NAR = (
    "Every particle bug lives in one of three places. "
    "Emission is when and where particles are born: amount, lifetime, one-shot, explosiveness. "
    "Process is how they move: the ParticleProcessMaterial — spread, velocity, gravity, the scale curve. "
    "Draw is what they look like: texture, blend mode, billboard. "
    "An effect can be wrong in any part independently. "
    "Correct emission time. Wrong texture. "
    "That gives you thirty-two correct moments with thirty-two invisible pixels."
)
b = base("B01", "act1", B01_NAR)
manim_shot(b, "B01_ThreePartModel",
           "Emission / Process / Draw — three independent failure modes",
           "Three rows reveal with property lists")
beats.append(b)

# ── B02: DeathBurst Config ────────────────────────────────────────────
B02_NAR = (
    "The burst is a GPUParticles2D named DeathBurst. "
    "Emitting: false. One-shot: true. Explosiveness: one-point-zero. Amount: thirty-two. Lifetime: zero-point-six seconds. "
    "The process material: spread one-eighty, velocity one-fifty to three-hundred pixels per second, gravity zero. "
    "Scale curve: shrinks over lifetime. Color ramp: fades to transparent. "
    "Texture: a sixteen-by-sixteen radial GradientTexture2D — a soft round dot. "
    "Particle-flag-disable-Z: true. "
    "Everything in the scene file. Nothing built in code."
)
b = base("B02", "act1", B02_NAR)
manim_shot(b, "B02_DeathBurstConfig",
           "DeathBurst node properties — full config list",
           "Properties reveal in two batches: emission then material")
beats.append(b)

# ── B03: Parent Trap ──────────────────────────────────────────────────
B03_NAR = (
    "The parent matters because visibility is inherited. "
    "Player calls hide when hit. Hide propagates to all children. "
    "A burst parented under Player vanishes at the instant it should fire. "
    "Parented to Main, it stays visible in the tree when the player hides. "
    "The entire gameplay trigger is two lines in game-over. "
    "Set the burst's global position to the player's position at the hit. "
    "Call restart. "
    "That is the change."
)
b = base("B03", "act1", B03_NAR)
manim_shot(b, "B03_ParentTrap",
           "Player parent (invisible) vs Main parent (correct)",
           "Two columns: red bad / green good appear side by side")
beats.append(b)

# ── B04: Nine Checks ──────────────────────────────────────────────────
B04_NAR = (
    "The test is nine checks. "
    "First batch: texture is a GradientTexture2D — not a one-pixel square. Disable-Z is enabled for two-D. Not emitting at load. Not emitting before a hit. "
    "Second batch: emitting after the hit. Visible in tree after the hit. Position matches the player's hit position. Finished signal arrives within lifetime plus half a second. Restarts correctly on a second death. "
    "Nine checks. All state checks. "
    "None of them ask whether you can see the burst."
)
b = base("B04", "act1", B04_NAR)
manim_shot(b, "B04_NineChecks",
           "9-check test spec — what each proves",
           "Checks reveal in two batches with colored dots")
beats.append(b)

# ── BACT2 ─────────────────────────────────────────────────────────────
b = base("BACT2", "act2", "", lane="act")
remotion_shot(b, "FormACard", {"actLabel": "Act 2", "title": "Three Sessions, Three Mistakes"},
              "Act 2 card", "Card wipes in")
beats.append(b)

# ── B05: Session 1 Mistake ────────────────────────────────────────────
B05_NAR = (
    "Session one. Claude Code read five files, added the node, placed it correctly, explained the parent choice correctly. "
    "Then it tried to run Godot and hit its allow list. "
    "Instead of stopping, it produced a table of predicted output. "
    "Three predicted failures. Each with a specific engine explanation. "
    "I ran the test myself. One failure. Two of the three predictions were wrong. "
    "A table of expected output is not output."
)
b = base("B05", "act2", B05_NAR)
manim_shot(b, "B05_SessionOneMistake",
           "Session 1: predicted vs real test output",
           "Table shows predicted FAIL vs real PASS for each check")
beats.append(b)

# ── B06: Lambda Bug ───────────────────────────────────────────────────
B06_NAR = (
    "The one real failure: the finished-signal check. "
    "GDScript lambdas capture outer locals by value. The lambda gets its own copy of finished-received. "
    "It sets that copy. The test reads the original. Signal fires; test never sees it. "
    "Session two ran the tests correctly and reached the same failure. "
    "Then it explained: the dummy renderer never advances particle lifetime timers. "
    "That was also wrong. "
    "A separate probe — run before any agent session — had confirmed finished fires at half a second in headless Godot. "
    "The agent had an explanation for something it had not checked."
)
b = base("B06", "act2", B06_NAR)
manim_shot(b, "B06_LambdaBug",
           "Lambda capture bug — outer var vs lambda copy",
           "Boxes and arrow show capture; signal fires; test reads original")
beats.append(b)

# ── B07: Two Silent Defects ───────────────────────────────────────────
B07_NAR = (
    "Session three corrected both things. "
    "The lambda fix: switch from a boolean to a Dictionary — a reference type the lambda can actually mutate. "
    "Two silent defects found in the documentation, not the test. "
    "Defect one: null texture draws one-by-one-pixel squares. Session one's thirty-two particles were thirty-two pixels on a four-eighty-pixel-wide screen. "
    "Fix: a sixteen-by-sixteen radial GradientTexture2D. "
    "Defect two: ParticleProcessMaterial defaults to three-D, with disable-Z off. Spread of one-eighty in three-D means some velocity points into Z. Nothing on screen shows that. "
    "Fix: particle-flag-disable-Z equals true. "
    "Final run: nine of nine, pass."
)
b = base("B07", "act2", B07_NAR)
manim_shot(b, "B07_SilentDefects",
           "Two silent defects: null texture and Disable Z — each with fix",
           "Two panels reveal with defect description and green fix")
beats.append(b)

# ── BACT3 ─────────────────────────────────────────────────────────────
b = base("BACT3", "act3", "", lane="act")
remotion_shot(b, "FormACard", {"actLabel": "Act 3", "title": "Measuring the Cost"},
              "Act 3 card", "Card wipes in")
beats.append(b)

# ── B08: Sleep Output ─────────────────────────────────────────────────
B08_NAR = (
    "The cost measurement. Codex ran the script exactly as specified. "
    "Every case: empty scene, GPU particles at fifty-thousand, CPU particles at fifty-thousand. "
    "All cost six-point-nine milliseconds. "
    "That is not particle cost. "
    "Godot's frame loop sleeps toward a target of one-forty-four FPS when it cannot draw. "
    "The default sleep duration: six-thousand-nine-hundred microseconds — six-point-nine milliseconds. "
    "Any work under that threshold hides inside the sleep. "
    "The prompt did not name the flag. The agent did exactly what it was told. "
    "What it was told measured a sleep."
)
b = base("B08", "act3", B08_NAR)
manim_shot(b, "B08_SleepOutput",
           "Headless cost script: all cases show 6.9 ms — the idle sleep",
           "Table reveals; label This is a sleep appears last")
beats.append(b)

# ── B09: Fixed-FPS Table ──────────────────────────────────────────────
B09_NAR = (
    "The fix is one flag: fixed-fps sixty. "
    "With a fixed frame rate, the loop returns before sleeping. "
    "The real table. "
    "CPU particles scale linearly: zero-point-zero-three-five milliseconds at one thousand, zero-point-three-three at ten thousand, one-point-six-one at fifty thousand. "
    "About zero-point-zero-three-two microseconds per particle per frame. "
    "At fifty thousand particles, a tenth of a sixteen-point-seven millisecond budget. "
    "GPU rows: zero-point-zero-zero-two milliseconds — the dummy renderer doing nothing. "
    "These numbers are real. They are also on a Mac with a load average between nineteen and twenty-three, from other jobs running. Not a production benchmark."
)
b = base("B09", "act3", B09_NAR)
manim_shot(b, "B09_FixedFpsTable",
           "Fixed-fps 60 cost table: CPU scales linearly, GPU shows dummy",
           "Table headers then column separators then rows reveal")
beats.append(b)

# ── BACT4 ─────────────────────────────────────────────────────────────
b = base("BACT4", "act4", "", lane="act")
remotion_shot(b, "FormACard", {"actLabel": "Act 4", "title": "What Only You Can See"},
              "Act 4 card", "Card wipes in")
beats.append(b)

# ── B10: Headless Limits ──────────────────────────────────────────────
B10_NAR = (
    "What nine passing tests did not establish. "
    "Whether the burst is visible against the teal background. "
    "Whether one-fifty to three-hundred pixels per second over zero-point-six seconds reads as a death on a four-eighty-pixel-wide screen. "
    "Whether the radial gradient looks round at the edges — with fill-to at its default, the gradient reaches full transparency at the corners, not the edges. "
    "How the burst and the game-over text interact. "
    "What any of it costs on a GPU. "
    "No one looked at a screen for this chapter."
)
b = base("B10", "act4", B10_NAR)
manim_shot(b, "B10_HeadlessLimits",
           "Four things 9/9 PASS did not prove — only a screen can",
           "Cross marks and items reveal in two batches")
beats.append(b)

# ── B11: Engine Map ───────────────────────────────────────────────────
B11_NAR = (
    "The burst maps cleanly across engines. "
    "Godot one-shot is Unity's Looping off. Explosiveness one is a Burst event at time zero. Restart is Play. Finished is OnParticleSystemStopped. "
    "In Unreal Niagara: Loop Behavior Once. Spawn Burst Instantaneous. Reset-System or Activate. On-System-Finished. "
    "The vocabulary differs. The birth-life-death loop does not. "
    "The difference that matters for agents: Godot's scene files are text, readable and diffable. "
    "Unreal's uasset is binary. Unity's VFX Graph is binary. "
    "An agent can read what Godot wrote. The others require a workaround."
)
b = base("B11", "act4", B11_NAR)
manim_shot(b, "B11_EngineMap",
           "One-shot burst mapped across Godot / Unity / Unreal",
           "Headers then column separators then rows reveal engine by engine")
beats.append(b)

# ── B12: GodotDevWorkbench ────────────────────────────────────────────
B12_NAR = (
    "Here is what changed. "
    "Two lines in game-over: set the burst's position to the player's, then call restart. "
    "The DeathBurst node holds everything: the config, the texture, the material. "
    "No code builds it at runtime. The scene file is the record. "
    "An agent can read that file, check every property, and add a test. "
    "What it cannot do is run the game and tell you whether the burst looks like a death."
)
b = base("B12", "act4", B12_NAR)
remotion_shot(b, "GodotDevWorkbench", {
    "mode": "code",
    "project": "walker-2d-dodge-the-creeps",
    "source": "godot/main.gd + main.tscn",
    "code": GAME_OVER_CODE,
    "codeFontSize": 26,
    "notes": [
        {"label": "Parent", "value": "Main (not Player)"},
        {"label": "Trigger", "value": "game_over() → restart()"},
        {"label": "Disable Z", "value": "particle_flag_disable_z = true"},
        {"label": "Texture", "value": "GradientTexture2D 16×16 radial"},
    ]
}, "game_over() two lines + DeathBurst node config", "Code and notes panel side by side")
beats.append(b)

# ── BVDT ──────────────────────────────────────────────────────────────
BVDT_NAR = (
    "Parent placement is correctness, not style. A burst parented to the player is always invisible. "
    "The test is a state machine. It proves emission, position, visibility-in-tree, and timing. It cannot see. "
    "The cost tool measures what you tell it to measure. A missing flag measured a sleep for two minutes of Codex time. "
    "What is still open: whether the burst reads as a death, whether the gradient looks round, what it costs on a real GPU. "
    "Only you can close those."
)
b = base("BVDT", "close", BVDT_NAR, lane="close")
remotion_shot(b, "ClaudeVerdictArtifact", {
    "title": "Adding Particle Effects to Walker Claude",
    "items": [
        "Parent placement is correctness — Player parent = invisible burst",
        "The test proves state — not sight",
        "Cost tool measures what you tell it — --fixed-fps 60 reveals the real cost",
        "Visual intent, readability, GPU cost — only a screen closes those",
    ]
}, "Verdict: four takeaways", "Items reveal one by one")
beats.append(b)

# ── BHTF ──────────────────────────────────────────────────────────────
BHTF_NAR = (
    "Open Dodge the Creeps. Add a GPUParticles2D named DeathBurst as a child of Main — not Player. "
    "Set one-shot true, explosiveness one-point-zero, amount thirty-two, lifetime zero-point-six. "
    "Give it a sixteen-by-sixteen radial GradientTexture2D. Enable disable-Z. "
    "Write one test that checks global-position after a hit and that finished arrives within lifetime plus half a second. "
    "Then run the game and die on purpose. "
    "Tell me what you see."
)
b = base("BHTF", "close", BHTF_NAR, lane="close")
remotion_shot(b, "ClaudeComposerAsk", {
    "prompt": (
        "Open walker-2d-dodge-the-creeps. Add GPUParticles2D DeathBurst as child of Main. "
        "Set one_shot=true, explosiveness=1.0, amount=32, lifetime=0.6. "
        "GradientTexture2D 16×16 radial. particle_flag_disable_z=true. "
        "Write one test: position after hit + finished within lifetime+0.5 s. "
        "Run the game and die. Tell me what you see."
    ),
    "folderLabel": "@NikBearBrown",
}, "Your Turn: add DeathBurst, test it, run the game", "Prompt types into composer")
beats.append(b)

# ── BOUT ──────────────────────────────────────────────────────────────
BOUT_NAR = "Adding Particle Effects to Walker Claude. At Nik Bear Brown."
b = base("BOUT", "close", BOUT_NAR, lane="close")
remotion_shot(b, "ClaudeTitleOutro", {
    "title": TITLE,
    "channel": "@NikBearBrown",
}, "Outro title card", "Title and channel fade in")
beats.append(b)

# ── Write ─────────────────────────────────────────────────────────────
sheet = {
    "metadata": {
        "slug": SLUG,
        "title": TITLE,
        "playlist": PLAYLIST,
        "course": COURSE,
        "channel": CHANNEL,
        "skill": "lecture",
        "version": "1.0",
    },
    "beats": beats,
}
SHEET_PATH.write_text(json.dumps(sheet, indent=2, ensure_ascii=False))
print(f"[make_sheet] wrote {len(beats)} beats → {SHEET_PATH}")
