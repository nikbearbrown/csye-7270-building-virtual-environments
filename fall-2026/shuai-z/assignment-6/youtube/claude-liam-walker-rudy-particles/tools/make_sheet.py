#!/usr/bin/env python3
"""Author beat_sheet.json for the walker-rudy Assignment 6 godot-gamedev film.

Every code excerpt is cut by line range from game/ here, so the text on screen
is the text in the file. Timing fields (durationSeconds, cue times) are filled
later by build_reel.py from the measured narration. Gameplay frame numbers are
the frames of capture/play-01.mp4, read from capture/play-01-run.log.

    python3 tools/make_sheet.py        # from the reel folder
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
A6 = REEL.parents[1]
PUB = "reels/claude-liam-walker-rudy-particles"   # Remotion public/ subfolder for this reel's figures
TITLE = "Sparks and Dust for Walker Rudy."
SLUG = "claude-liam-walker-rudy-particles"
REV = "d0ed415"
PROJECT = f"Walker Rudy · game/ @ {REV}"
TOPIC = "WALKER-RUDY · PARTICLE EFFECTS IN GODOT 4.7"
CHIP = "SCRIPTED INPUT · a film-only driver on a copy presses Enter, move, jump, slash and Esc"


def lines(path, a, b):
    return "\n".join((A6 / "game" / path).read_text().splitlines()[a - 1:b])


def code(bid, act, path, a, b, title, narration, cues, notes, output, components, font=25):
    return {
        "beat_id": bid, "act": act, "narration_text": narration, "components": components,
        "shot": {"type": "REMOTION", "lane": "code", "remotion": {"pattern": "GodotDevWorkbench", "props": {
            "mode": "code", "title": title, "project": PROJECT, "path": "res://" + path,
            "source": f"Source: assignment-6/game/{path}, lines {a}–{b} (verbatim). Godot editor reconstruction.",
            "code": lines(path, a, b), "startLine": a, "codeFontSize": font,
            "inspectorLabel": "Source notes — not Inspector values",
            "notes": [{"label": k, "value": v} for k, v in notes],
            "output": output}},
            "cue_phrases": [{"phrase": p, "line": ln, "label": lb} for p, ln, lb in cues]},
        "excerpt": {"project": "game", "path": path, "start_line": a, "end_line": b},
    }


def figure(bid, act, title, status, image, source, cards, cues, narration, components=()):
    return {"beat_id": bid, "act": act, "narration_text": narration, "components": list(components),
            "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "GodotDesignFigure", "props": {
                "title": title, "status": status, "image": f"{PUB}/{image}", "imageLabel": "",
                "excerpt": "", "source": source, "cards": [{"label": a, "text": b} for a, b in cards]}},
                "cue_cards": [[p, k] for p, k in cues]}}


# Stills whose engine images fill most of the frame: the whole-frame ink average measures the pictures, so the
# contrast check is made on the card's own title instead (normalised boxes).
TITLE_REGIONS = {"game-card.png": [0.052, 0.05, 0.6, 0.095]}
for name in ("strip-a-r0", "strip-a-r1", "strip-b-r0", "strip-b-r1", "strip-b-r2", "strip-b-r3", "headless-limits"):
    TITLE_REGIONS[name + ".png"] = [0.052, 0.05, 0.62, 0.098]


def still(bid, act, image, observation, narration, components=()):
    qc = {"full_bleed": False}
    if image in TITLE_REGIONS:
        qc.update({"contrast_regions": [{"label": "card title", "box": TITLE_REGIONS[image]}],
                   "contrast_reason": "Engine captures fill much of this card; the whole-frame ink average measures them, not text. The title is measured locally."})
    return {"beat_id": bid, "act": act, "narration_text": narration, "components": list(components),
            "shot": {"type": "VIDEO", "lane": "evidence", "source": "own", "treatment": "none",
                     "evidence_media": f"stills/{image}", "still_plan": {"image": f"stills/{image}"},
                     "observation": observation},
            "qc": qc}


def gameplay(bid, act, segments, observation, narration, components, chips=(CHIP,)):
    return {"beat_id": bid, "act": act, "components": components, "narration_text": narration,
            "shot": {"type": "VIDEO", "lane": "gameplay", "source": "own", "treatment": "none", "evidence_media": f"media/{bid}.mp4",
                     "capture_plan": {"capture": "play-01", "segments": segments, "chips": list(chips)}, "observation": observation},
            "qc": {"full_bleed": True, "full_bleed_reason": "Engine capture renders edge to edge at 3840x2160; the film's chips sit inside the title-safe inset. Only the edge-bleed check is waived."}}


def seg(a, b, speed=1.0, label="", crop=None):
    d = {"from": a, "to": b, "speed": speed, "label": label}
    if crop:
        d["crop"] = list(crop)
    return d


STAND = (1110, 960, 1920, 1080)     # 2× around Rudy standing at the screen's centre: the hitbox and the spray
APEX = (1040, 680, 1920, 1080)      # 2× around the top of the jump
RUN = (640, 640, 2560, 1440)        # 1.5× around a running jump: the trail behind and his head at the top
RUN_START = (0, 640, 2560, 1440)    # 1.5× at the level's left edge, where the camera cannot centre him yet


B = []

# ── walker bookends ─────────────────────────────────────────────────────────
B.append({"beat_id": "B00", "act": "cold open — the Walker ask", "components": [],
  "role_note": "walker modifier B00. Reconstructed prompt, said out loud; not a transcript.",
  "narration_text": "Jambo, this is Liam, in for Bear. That prompt is an illustrative reconstruction, not something anyone typed. "
                    "What is real is underneath it: walker-rudy, the 2D game shuai-z started in Assignment 2, now with two particle effects: "
                    "sparks where Rudy's sword cut can land, and a trail of dust behind his boots while he runs.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Jambo, Liam", "topic": TOPIC, "segment": TITLE,
    "command": "Please use Walker to convert my game design document about Walker Rudy — a chibi boy who crosses the Harvest Fields with a "
               "sword — into two particle effects: sparks that mark where and when his cut can land, and a dust trail while he runs, each "
               "specified before it is built, tuned by eye against frame strips, tested headless, and priced against a budget.",
    "runningText": "reconstructed prompt — illustrative, not a transcript…",
    "output": [f"Repo walker-rudy · assignment-6/game at {REV} · Godot 4.7.2 · GL Compatibility · one 2D game.",
               "Built: SlashSparks (a burst per live cut) and RunDust (a world-space trail), their previews, tests and driver.",
               "Effects and tests: scoped claude -p sessions · every verdict and approval: shuai-z · Use It records: Codex."],
    "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"}}}})

B.append({"beat_id": "B01", "act": "BLUF — what was actually built", "components": [], "lead_silence_s": 0.8,
  "role_note": "EXECUTIVE-SUMMARY LAW. The correction is the misconception: Claude's strip readings did not decide the look.",
  "qc": {"sparse_by_design": True, "sparse_reason": "BrutalistHesitantWriter types the overview token by token; mid-beat frames are mostly cream by design."},
  "narration_text": "Sparks and dust for Walker Rudy, built by agents, and judged by eye. Not by Claude. Claude read every strip and predicted "
                    "every round, but those readings are claims. shuai-z's verdict, watching the effect at real speed, decided each one.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
    "text": "Sparks and dust for Walker Rudy,\nbuilt by agents,\njudged by Claude.",
    "triggerWords": "Claude", "replacementWords": "eye",
    "seed": "walker-rudy-particles-bluf-2026-11-07", "face": "serif", "fontSize": 112, "lineSpacing": 1.4,
    "align": "center", "charMs": 24, "jitter": 6, "mistakeRate": 3, "hesitateWithin": 1, "hesitateBetween": 4, "banner": ""}}}})

# ── the game, the effects, the three parts ──────────────────────────────────
B.append(still("B02", "the game, both effects, their jobs", "game-card.png",
  "Two frames of the film's own Movie Maker capture of the real Main at d0ed415: two SlashSparks bursts alive during fast cuts, and RunDust's "
  "trail behind Rudy while he runs.",
  "Walker Rudy is a 2D side-scroller in Godot four point seven, on the Compatibility renderer. Effect A, slash sparks, is a burst. Its job: "
  "show where and when the cut can land, because the sword's hitbox is live for only point one five seconds of a point three second swing, "
  "fifty pixels in front of him. Its event is that hitbox going live. Effect B, run dust, is a trail. Its job: show that he is running, "
  "which way, and where his feet meet the ground. Its condition: in control, on the floor, and moving.", ["slash-sparks", "run-dust", "effects-driver"]))

B.append(figure("B03", "the three parts of a particle system", "Emission, Process, Draw",
  "THREE PARTS — each with a line from the scene file or the generated shader", "three-parts.png",
  "Source: game/effects/slash_sparks.tscn lines 108, 79 and 109; game/shaders/particles_generated.gdshader line 311. Headless price: logs/cost_effects_60fps_rerun.log.",
  [("Emission", "how many, how often, how long"), ("Process", "how each particle moves and changes"), ("Draw", "what each one looks like"),
   ("Headless", "≈ 0: no process runs, nothing is drawn")],
  [["Emission", 0], ["Process", 1], ["Draw", 2], ["headless", 3]],
  "Every particle system has three parts. Emission: how many, how often, how long. Line one oh eight: twenty-eight sparks, all at once. "
  "Process: how each particle moves and changes over its life. Line seventy-nine sets gravity, and in the shader Godot generated from that "
  "material, line three eleven reads it, once per particle, per step, on the GPU. Draw: what each one looks like, here a small gradient "
  "streak with a dark rim. That is also why a GPU effect's headless price is near zero. A headless run uses a dummy renderer: it runs no "
  "process shader and draws nothing, so the CPU pays only for node bookkeeping.", ["slash-sparks", "process-shader"]))

# ── Effect A ────────────────────────────────────────────────────────────────
B.append(figure("B04", "Effect A — the intent", "Effect A: the Intent, Written First",
  "CHANGE-BRIEF.md §2 · revision 1, committed before the first prompt", "intent-a.png",
  "Source: CHANGE-BRIEF.md §2, The intent (cc9f7195), and Revision 3. Drafted by Claude, reviewed by shuai-z.",
  [("Strike", "frame 0: white flash, full size"), ("Spray", "0.03–0.15 s: out and up"), ("Fall-off", "0.15–0.45 s: down, orange, gone"),
   ("Rim", "#290F0D: 10–14 : 1")],
  [["Strike", 0], ["Spray", 1], ["fall-off", 2], ["dark rim", 3]],
  "The intent was written before anything was built. Strike: on frame zero, a white flash at the hitbox, at full size. Spray: the sparks "
  "fly out forward and a little up, white turning yellow. Fall-off: they arc down under gravity, shrink, turn orange and fade; the last is "
  "gone by point four five seconds. Yellow alone barely separates from the wheat and the sky, so every spark carries a dark rim in the "
  "art's own line colour. Claude drafted this brief; shuai-z chose the effect and reviewed it.", ["slash-sparks"]))

B.append(code("B05", "Effect A — the process settings", "effects/slash_sparks.tscn", 73, 82, "How Each Spark Moves",
  "This is the process part, Sparks' process material. Align Y turns each streak along its own velocity. Disable Z keeps every bit of speed "
  "in the plane. The direction is nineteen degrees above forward, with a thirty degree spread. Speed between two sixty and four twenty pixels "
  "a second, and gravity seven hundred, pulling down. No damping: that is Effect B's feature. And lifetime randomness cuts up to forty percent "
  "off some lives.",
  [("Align Y", 73, "particle_flag_align_y: streaks point along velocity"), ("Disable Z", 74, "particle_flag_disable_z: 2D, no lost speed"),
   ("nineteen degrees", 75, "direction (0.944, −0.33): 19° above forward"), ("thirty degree", 76, "spread ±30°"),
   ("two sixty", 77, "initial_velocity_min / _max: 260–420 px/s"), ("gravity seven hundred", 79, "gravity (0, 700): px/s² down"),
   ("No damping", 80, "damping 0 / 0: B's feature, not A's"), ("forty percent", 82, "lifetime_randomness 0.4: lives 0.27–0.45 s")],
  [("Material", "ParticleProcessMaterial"), ("Also here", "scale curve 1 → 0.3, colour ramp white → orange"), ("Built by", "claude -p (ea4419ae)")],
  ["game/effects/slash_sparks.tscn · Sparks · process_material"], ["slash-sparks"], font=27))
B.append(still("B06", "result — the first strip, r0", "strip-a-r0.png",
  "Fixture captures (the preview, r0, 14 sparks, the same process settings): frames 10, 12, 15, 20, 30 and 50 against the brief's predictions, "
  "with Claude's reading and shuai-z's first verdict.",
  "And this is what those settings drew, in the first strip: a fixture, the preview scene over a frozen level, with fourteen sparks. Frame "
  "ten, the flash. Twelve and fifteen, the spray out and up, turning orange. Twenty, the second burst, with only two specks left of the first. "
  "shuai-z watched it at real speed first, before Claude read a frame, and said: too sparse, too few. Claude's reading agreed: the spray reads "
  "as a crowd for only five frames.", ["slash-sparks"]))

B.append(code("B07", "Effect A — the emission settings, tuned", "effects/slash_sparks.tscn", 107, 115, "One Number Changed",
  "The node holds the emission part. Emitting is saved as false, so nothing fires on load. Amount twenty-eight: this is the one value "
  "tuning changed, from fourteen. The texture is the draw part. Lifetime point four five seconds, one shot, and explosiveness one, so all "
  "twenty-eight are born on the same frame. Local coords off: sparks already born stay in the world.",
  [("Emitting is saved as false", 107, "emitting = false: no burst on load"), ("Amount twenty-eight", 108, "amount 28 (r1; was 14)"),
   ("The texture", 109, "GradientTexture2D 12 × 40, dark rim"), ("Lifetime", 110, "lifetime 0.45 s"),
   ("explosiveness one", 113, "explosiveness 1.0: one burst"), ("Local coords off", 115, "local_coords false: world space")],
  [("Changed by", "r1, approved by shuai-z (fed848b8)"), ("Peak", "29 a burst · 58 for two"), ("Flash", "one particle, 0.12 s")],
  ["Sparks: amount 14 → 28; speed, spread, size, colour and timing unchanged"], ["slash-sparks"], font=28))
B.append(still("B08", "result — tuning r1, before and after", "strip-a-r1.png",
  "Fixture captures r0 and r1 at frames 12, 15 and 20: Claude predicted 16–20 streaks, 18–22 with halved gaps, and 3–5 specks of the first "
  "burst; r1 shows about 14–18, about 20, and about 8, higher. shuai-z kept it.",
  "One change, proposed by Claude and approved by shuai-z: fourteen sparks to twenty-eight. Claude predicted each frame first. Frame twelve: "
  "sixteen to twenty streaks; about fourteen to eighteen can be told apart. Fifteen: about twenty, with the gaps halved, as predicted. "
  "Twenty: Claude predicted three to five specks of the first burst, and got about eight, higher. Its prediction doubled r zero's two "
  "specks instead of working out how many lives outlast a third of a second. shuai-z watched it three times at real speed, and kept it.",
  ["slash-sparks"]))

B.append(code("B09", "Effect A — the trigger", "effects/effects_driver.gd", 35, 46, "A New Burst on Every Live Edge",
  "The trigger. Every physics tick, the driver reads whether the sword's hitbox is disabled. Live after disabled is the event, and it fires. "
  "Each cut instantiates a new burst, so a fast second cut leaves the first one running: that is the retrigger rule, overlap. It places the "
  "burst on the hitbox, and mirrors it with Rudy's facing. The driver sits after Rudy in Main, so it sees the edge on the same tick. "
  "It reads his state, and never writes it.",
  [("reads whether", 35, "_sword_box.disabled, each physics tick"), ("Live after disabled", 36, "the true → false edge: the event"),
   ("instantiates a new burst", 43, "a new SlashSparks per cut: overlap (A3)"), ("on the hitbox", 45, "global_position = the hitbox's"),
   ("mirrors it", 46, "scale.x = facing: ±1")],
  [("No signal", "rudy.gd is unchanged"), ("At most", "2 bursts alive"), ("Written by", "claude -p (ebe2d9d5)")],
  ["main.tscn order: Level1, DustTrail, Rudy, Effects, Camera, Hud"], ["effects-driver", "slash-sparks"], font=23))
B.append(gameplay("B10", "result — Effect A in play, rapid repeats",
  [seg(196, 345), seg(210, 232, 1 / 3, "REPLAY ⅓× · ENLARGED 2× · one cut", STAND),
   seg(236, 296, 1 / 3, "REPLAY ⅓× · ENLARGED 2× · five cuts as fast as the game allows", STAND),
   seg(312, 342, 1 / 3, "REPLAY ⅓× · ENLARGED 2× · facing left: the spray goes left", STAND)],
  "The real Main in Godot 4.7.2 Compatibility, Movie Maker at 3840×2160 and 30 fps, scripted input: one cut (burst at frame 214); five cuts "
  "as fast as the game allows, two bursts alive at once on frames 250–253, 260–263, 270–273 and 280–283; two cuts facing left, spraying left. "
  "Then labelled one-third-speed replays, enlarged 2× around Rudy, of the single cut, the five cuts and the two left cuts.",
  "Here it is in play, the real game at 4K. One cut. Then five, as fast as the game allows: each burst lives longer than the gap between "
  "cuts, so for a few frames two are alive at once. He turns, and the sparks fly left. Now a third of the speed: the first burst's orange "
  "sparks are still falling when the next flash lands.", ["effects-driver", "slash-sparks"]))
B.append(gameplay("B11", "replay — the goblin, the sky, the pause",
  [seg(440, 490), seg(455, 486, 0.25, "REPLAY ¼× · ENLARGED 2× · a cut at the top of a jump: against the sky", APEX),
   seg(515, 586), seg(552, 580, 0.25, "REPLAY ¼× · ENLARGED 2× · the goblin hides at 0.4 s; its sparks live 0.45 s", STAND),
   seg(586, 595), seg(595, 631, 1.0, "ESC · THE GAME IS PAUSED: the sparks hold still"), seg(631, 663)],
  "The same capture: a run and a cut at the top of a jump (burst at frame 469) against the sky, at 1.0× and a labelled ¼× replay enlarged 2×; "
  "the walk to the second goblin and the cut that defeats it (burst at 561), the goblin hidden from frame 573 while the burst lives to 574, at "
  "1.0× and ¼×; then at full speed a cut and Esc at once, paused frames 595–630, the burst frozen and still drawn, carrying on after the resume.",
  "A cut at the top of a jump: the dark rims keep the sparks readable against the sky. The cut that defeats a goblin: the goblin vanishes "
  "first, and its sparks outlive it, because they belong to an effects container, not to the goblin. Then a cut and Esc at once: the "
  "sparks hold still while paused, and carry on when play resumes.", ["effects-driver", "slash-sparks"]))

# ── Effect B ────────────────────────────────────────────────────────────────
B.append(figure("B12", "Effect B — the intent", "Effect B: the Intent, Written First",
  "CHANGE-BRIEF.md §3 · revision 1, committed before the first prompt", "intent-b.png",
  "Source: CHANGE-BRIEF.md §3, The intent (cc9f7195), and Revision 4. Drafted by Claude, reviewed by shuai-z.",
  [("Fade-in", "0–0.075 s at his feet"), ("Hang", "damping stops each puff"), ("Dissipate", "lighten into the ground"), ("Start · stop", "within 2 frames · empty in 0.5 s")],
  [["fades in", 0], ["damping", 1], ["dissipate", 2], ["as a whole", 3]],
  "Effect B, the same way. Each puff fades in at his feet, then hangs: damping slows it to a stop in the air while it grows. Then it "
  "dissipates, lightening toward the ground's colour. For the trail as a whole: a puff within two frames of the first running tick, and "
  "after he stops, the trail empties from its old end within half a second. The brief also predicted the dust would show at two point nine "
  "to one against the wheat. That prediction did not survive the first strip.", ["run-dust"]))
B.append(still("B13", "the first strip, r0", "strip-b-r0.png",
  "Fixture captures (the preview, r0: 20 puffs, 40–90 px/s, the ramp at 0.75 opacity): nothing visible in frames 10–56; against a no-dust "
  "render, at most 224 pixels change by 20 levels or more. shuai-z: I could not see the dust trail at all.",
  "The first strip, again a fixture. shuai-z watched it six times at real speed and said: I could not see the dust trail at all. Was it "
  "there? Claude rendered the same preview with the dust hidden, and compared them pixel by pixel. At frame twenty-five the dust changed only "
  "a hundred and thirty-six pixels by twenty levels or more. The brief's contrast assumed opaque dust over the wheat. The puffs were born in "
  "the green grass strip, at three-quarters opacity, with soft edges.", ["run-dust"]))
B.append(still("B14", "tuning r1 — a darker ramp", "strip-b-r1.png",
  "Fixture captures r0 and r1 at frames 13, 25 and 46: the ramp darker and opaque; at frame 25, 612 pixels changed by 20 levels or more "
  "(target at least 500, met) and a largest change of 87 (target at least 90, missed). shuai-z: visible now, not enough.",
  "Round one: one setting, the colour ramp, darker and fully opaque. Claude's prediction set two numbers to meet at frame twenty-five: five "
  "hundred pixels, met with six hundred and twelve; and a largest change of ninety levels, missed at eighty-seven. shuai-z's verdict: I can "
  "see it now, but there is still not enough dust, and it is not obvious enough.", ["run-dust"]))
B.append(still("B15", "tuning r2 — twice the puffs", "strip-b-r2.png",
  "Fixture captures r1 and r2 at frames 13, 25 and 46: amount 20 → 40; at frame 25, 1,054 pixels changed by 20 levels or more and a largest "
  "change of 105, both targets met. Claude read a continuous band; shuai-z judged that it stayed on the ground.",
  "Round two: twenty puffs to forty, so they overlap into one band. Claude read r two as a continuous band, with both of its measured "
  "targets met. shuai-z overruled that reading. The dust could rise at a steeper angle; right now it nearly all stays on the ground. "
  "Measured afterwards, the trail reached at most thirty-four pixels above the walk line: inside the grass strip, as the eye said.", ["run-dust"]))
B.append(still("B16", "tuning r3 — twice the speed", "strip-b-r3.png",
  "Fixture captures r2 and r3 at frames 13, 25 and 46: initial velocity 40/90 → 80/160 px/s with damping unchanged; at frame 25 the top of "
  "the changed pixels is 58 px above the walk line (predicted 50–62) and 1,501 pixels (target at least 1,000); frames 13 and 46 lower than predicted.",
  "Round three: the initial speed doubled, damping left alone, so each puff still slows to a hang, about twice as high. Predicted top at "
  "frame twenty-five: fifty to sixty-two pixels. Measured: fifty-eight. Frames thirteen and forty-six came out lower than predicted. "
  "shuai-z watched it three times, and kept it.", ["run-dust"]))

B.append(code("B17", "Effect B — the process settings, as tuned", "effects/run_dust.tscn", 31, 41, "Damping: the Feature A Lacks",
  "The dust's process settings, as the three rounds left them. A box emission shape, twenty-eight by six pixels, where the sparks use a point. "
  "Straight up, with a fifty degree spread. Speed eighty to one sixty, round three's change. No gravity. And damping, a hundred and twenty "
  "to a hundred and eighty pixels per second squared: the feature Effect A does not use. It brakes every puff until it hangs in the air.",
  [("box emission shape", 31, "emission_shape 3: box"), ("twenty-eight by six", 32, "emission_box_extents (14, 3): 28 × 6 px"),
   ("Straight up", 35, "direction (0, −1)"), ("fifty degree", 36, "spread ±50°"),
   ("eighty to one sixty", 37, "initial_velocity 80–160 px/s (r3)"), ("No gravity", 39, "gravity 0"),
   ("damping", 40, "damping_min / _max 120–180 px/s²: A has none")],
  [("Rounds", "r1 ramp · r2 amount · r3 speed"), ("Ramp", "#5C4A35 at α 1.0 (r1)"), ("Built by", "claude -p (017e8a52)")],
  ["game/effects/run_dust.tscn · RunDust · process_material"], ["run-dust"], font=25))
B.append(gameplay("B18", "result — the dust in play",
  [seg(0, 205), seg(60, 100, 0.5, "REPLAY 0.5× · ENLARGED 1.5× · the trail rises behind him and hangs", RUN_START),
   seg(182, 206, 0.5, "REPLAY 0.5× · ENLARGED 1.5× · he stops: the trail empties", RUN)],
  "The real Main, Movie Maker at 3840×2160 and 30 fps, scripted input: Enter on the title, the run to the right from frame 61 with RunDust "
  "emitting, the jump over the first spikes and over the first goblin, the sword and the stop at frame 190; then labelled half-speed replays, "
  "enlarged 1.5×, of frames 60–99 (the trail building) and 182–205 (the stop, the trail emptying).",
  "In the game. Enter, and he runs: puffs rise behind his boots, slow down, and hang, then thin into the ground. He jumps the spikes and "
  "the goblin, and walks into the sword. At half speed: each puff is braked by damping, so the band climbs behind him instead of flying off.",
  ["run-dust", "effects-driver"]))

B.append(code("B19", "Effect B — the emission settings and the space", "effects/run_dust.tscn", 52, 63, "A Trail Without Trails",
  "The node. Emitting saved as false. Amount forty, round two's change, in a steady stream with jittered birth times. Lifetime half a second. "
  "Trail enabled is false: Godot's own trail feature draws nothing under the Compatibility renderer, a probe showed. The trail is local coords "
  "off. The emitter rides at his feet, and every puff stays where it was born, so his motion lays them out in a line.",
  [("Emitting saved as false", 52, "emitting = false: nothing on load"), ("Amount forty", 53, "amount 40 (r2; was 20)"),
   ("steady stream", 58, "explosiveness 0.0"), ("jittered", 59, "randomness 0.2"), ("Lifetime half a second", 55, "lifetime 0.5 s"),
   ("Trail enabled is false", 61, "trail_enabled: not drawn by Compatibility"), ("local coords", 62, "local_coords false: the trail itself")],
  [("Probe", "evidence/compat-probe/ (9e19fe47)"), ("Peak", "40 particles"), ("Draws", "before Rudy: behind him")],
  ["Godot 4.7.2: “The Compatibility renderer does not support particle trails.”"], ["run-dust"], font=23))
B.append(gameplay("B20", "result — world space, and nothing in the air",
  [seg(85, 165), seg(92, 130, 1 / 3, "REPLAY ⅓× · ENLARGED 1.5× · over the spikes: no puff in the air", RUN),
   seg(130, 165, 1 / 3, "REPLAY ⅓× · ENLARGED 1.5× · over the goblin: on again at the landing", RUN)],
  "One-third-speed replays of the same capture: the jump over the first spikes (RunDust off from frame 97 while airborne, on again at the "
  "landing on frame 118), the trail already laid staying in world space as the camera follows; the same over the first goblin (off at 136, on at "
  "157). Frames 85–164 first at 1.0×, then the two replays, enlarged 1.5×.",
  "A third of the speed. He leaves the ground, and no new puff is born; the ones already laid stay where they were, in the world, while "
  "the camera follows him. He lands, and the trail starts again on that tick. The same over the goblin.", ["run-dust", "effects-driver"]))

B.append(code("B21", "Effect B — the condition", "effects/effects_driver.gd", 52, 59, "Start, Stop, Pause",
  "The condition, in the same driver. Every tick it keeps the emitter at his soles, even when he stands, so a respawn's jump lays down no "
  "streak. Running means: in play, on the floor, and moving faster than one pixel a second. It emits only while that holds and the emitter "
  "is visible, and it changes emitting only on the tick the answer changes. While the game is paused this script does not run at all, so "
  "emitting keeps its value.",
  [("at his soles", 54, "Rudy + (0, −4), every tick (B2)"), ("in play, on the floor", 55, "mode PLAY and is_on_floor()"),
   ("one pixel a second", 56, "absf(velocity.x) > 1.0"), ("is visible", 57, "and is_visible_in_tree(): no unseen puffs (B4)"),
   ("only on the tick", 58, "set emitting on change only")],
  [("Pause", "the driver stops; puffs freeze"), ("No signal", "read each physics tick"), ("Written by", "claude -p (d0abc9dd)")],
  ["rudy.gd's run test minus its swing override: cuts keep the trail"], ["effects-driver", "run-dust"], font=27))
B.append(gameplay("B22", "result — start, stop and pause",
  [seg(342, 376), seg(350, 376, 0.5, "REPLAY 0.5× · ENLARGED 1.5× · he starts: a puff within two frames", RUN),
   seg(376, 412, 1.0, "ESC · THE GAME IS PAUSED: the puffs hold still"), seg(412, 440),
   seg(418, 445, 0.5, "REPLAY 0.5× · ENLARGED 1.5× · he stops: the trail empties from its old end", RUN), seg(440, 520)],
  "The real Main, scripted input, with two labelled half-speed replays enlarged 1.5× (the start at frame 356, the stop at 422): running left from frame 356 with RunDust emitting; Esc at frame 376, paused frames 376–411 with the puffs "
  "frozen and still drawn; the resume, the run carrying on, the stop at 422 and the trail emptying; a turn, a run and a jump with a cut at "
  "the top (no puffs in the air), and the landing.",
  "He runs left, and Esc pauses the game: the puffs freeze, still drawn, and none is born. Resume: they carry on from where they were. "
  "He stops, and the trail empties from its old end. Then a run and a jump, with a cut at the top: no dust in the air.",
  ["effects-driver", "run-dust"]))

# ── the process shader, the tests, the prices ───────────────────────────────
B.append(still("B23", "two lines of the generated process shader", "shader-lines.png",
  "Verbatim lines 10–11, 43, 139 and 311 of game/shaders/particles_generated.gdshader, generated by shuai-z in the editor from a copy of "
  "Sparks' material, annotated beside the brief's velocity and gravity rows.",
  "The process part, as code. shuai-z converted a copy of Sparks' material into shader code in the editor, and read it. Two lines, beside "
  "the brief. Line one thirty-nine picks each particle's speed at random between two uniforms: the brief's two sixty and four twenty. "
  "Line three eleven starts the force from the gravity uniform, and a later line adds it to the velocity every step: the brief's seven "
  "hundred, down. The numbers are not in the shader's text. They arrive as uniforms, from the material.", ["process-shader"]))

B.append(code("B24", "what the tests proved", "tests/test_slash_sparks_state.gd", 181, 190, "Two Cuts, Through Real Input",
  "Now what the tests proved. This is the overlap check in Effect A's state test. It runs the real Main, and cuts through the real slash "
  "action: one cut, wait until the swing ends, a second cut, then forty-five ticks. Then it checks that two bursts were alive at the "
  "second cut, and that the first was the same node, not moved, and still emitting. It never calls the driver.",
  [("real slash", 184, "Input.action_press via _tap(&\"slash\")"), ("wait until the swing ends", 185, "not _rudy.is_slashing()"),
   ("a second cut", 186, "the fastest real retrigger: 19 ticks"), ("forty-five ticks", 187, "past the first burst's 27-tick life"),
   ("two bursts were alive", 188, "S7 and S8 read the recorded bursts")],
  [("Rate", "--fixed-fps 60, through the wrapper"), ("Writes", "Rudy's position only, for setup"), ("Written by", "claude -p (ebe2d9d5)")],
  ["scripts/run-test.sh test_slash_sparks_state.tscn 60"], ["effects-tests"], font=24))
B.append(still("B25", "result — the tests", "tests.png",
  "Recorded headless output through scripts/run-test.sh at pinned frame rates: configuration tests 108 and 61 PASS, state tests 14 and 14, "
  "the existing 141 and 15; S7, S8 and D11 lines shown.",
  "Headless output, through the course's wrapper. The configuration tests compare every setting with the brief: a hundred and eight for "
  "the sparks, sixty-one for the dust. The state tests: fourteen and fourteen, through real input. Two cuts nineteen ticks apart, both "
  "bursts alive, the first living its full twenty-seven ticks. Emitting matching the condition on all three hundred and eighty recorded ticks. "
  "And the old hundred and forty-one checks, and fifteen, unchanged.", ["effects-tests"]))
B.append(still("B26", "mutations", "mutations.png",
  "Recorded headless output of eight mutations, each exiting 1: two scene mutations per effect (a Godot 3 name, a value drifted from the "
  "brief) and two driver mutations per effect (a reused burst, a late driver; a dropped visibility test, a moved node).",
  "Can the checks fail? Eight mutations, and each one exits with one. A Godot 3 name in each scene: it loads without a word, and only the "
  "configuration test notices, from the loaded values and a text scan. A value drifted from the brief. One reused burst instead of a new one "
  "per cut: six failures. The driver one tick late. The dust's visibility test dropped. Its node moved after Rudy.", ["effects-tests"]))
B.append(still("B27", "both prices against the budget", "prices.png",
  "The headless cost table from logs/cost_effects_60fps_rerun.log beside a crop of Codex's Visual Profiler capture (GPU column 0.0 ms) and "
  "the FPS fallback with vsync off: 438, 239, 357, 311.",
  "The prices. Headless, per frame: an empty scene costs point zero zero four milliseconds, the game without the effects about point "
  "zero five, and each effect adds less than a hundredth, inside the noise between rounds. The budget, a quarter of a millisecond of GPU "
  "time per effect, needed the editor's Visual Profiler. On this M three, its GPU column read zero in every row: the brief's predicted failure "
  "twelve. A zero is not a pass, so the budget could not be evaluated here. With vsync off on F nine, the frame rate stayed between two hundred "
  "and thirty-nine and four hundred and thirty-eight, but frames per second are not GPU time.", ["effects-tests", "vsync-debug"]))
B.append(still("B28", "what no headless run can show", "headless-limits.png",
  "Fixture captures of r1 and of the Godot 3 name mutation at frame 15, and two of Codex's paused engine captures 0.7 s apart, pixel-identical.",
  "And what no headless run can show. With the Godot 3 name, the burst still sprays; nothing in the picture announces the fault. "
  "Headless, nothing is drawn at all. No test sees the sparks fly the way he faces, a paused puff hold still, or the dust read against "
  "the wheat. Those were eyes: Codex's captures, and shuai-z's own play, which found the size and the feel of both effects fine.",
  ["effects-tests"]))

# ── verdict, your turn, outro ───────────────────────────────────────────────
B.append({"beat_id": "BVD1", "act": "verdict — checked, overruled, caught, uncertain", "components": ["effects-tests"], "lead_silence_s": 0.4,
  "narration_text": "Verdict. Checked by machine: both configuration tests and both state tests pass, the old checks still pass, and eight "
                    "mutations each fail. Checked by eye: shuai-z judged every round at real speed and played the game. Overruled: Claude read "
                    "the dust's second round as done; shuai-z said it stayed on the ground, and round three followed. Caught: dust the brief said would show, "
                    "which shuai-z could not see at all; Effect B, built and tuned but not yet wired in, which shuai-z found "
                    "missing in the game; Effect B's scene mutations, missed and then run; and Claude's shell, left in a strip folder, which "
                    "broke shuai-z's command. Uncertain: the GPU price, which this Mac would not report, and nobody else has played it.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Checked, overruled, caught, uncertain",
    "artifactLines": ["Machine: config 108/108 and 61/61; state 14/14 and 14/14; the existing 141 and 15 (at 30, 60, 144); 8 mutations, each exit 1. Eyes: every round judged at real speed; shuai-z's own play in the 1280 × 720 window.",
                      "Overruled: Claude's reading of dust r2 (a continuous band, both targets met); shuai-z: it stays on the ground → r3. Also wrong: the brief's 2.9 : 1 dust contrast, and Claude's 3–5 specks for sparks r1 (about 8).",
                      "Caught: the invisible dust (shuai-z's eyes); Effect B not yet wired in, found missing in the game by shuai-z; B's scene mutations missed, then run; Claude's shell left in captures/, which broke shuai-z's command.",
                      "Uncertain: GPU time reads 0.0 ms on this M3, so the 0.25 ms budget is not evaluated; vsync held ~120 FPS on a display reporting 60 Hz, unexplained; one machine; no other player."]}}}})
B.append({"beat_id": "BVD2", "act": "verdict — who made what, next step", "components": [],
  "narration_text": "Who made what. shuai-z chose both effects, judged every preview and every strip, approved each change, generated the "
                    "process shader and wrote its reading, chose what to measure, and played the game. Scoped Claude sessions built the effects, "
                    "previews, driver, tests and cost script. Claude drafted the brief and the records, ran the captures, mutations and "
                    "measurements, wrote the F nine key, and made this film. Codex recorded the editor's profiler and the captures in play. "
                    "There are no texture files: every texture is a gradient defined inside the scene files. The source shown is d zero e d "
                    "four one five. The next step: measure the GPU time on a machine whose profiler reports it.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Who made what",
    "artifactLines": ["shuai-z: chose both effects; judged every preview and strip at real speed; approved every change (A r1; B r1–r3); generated particles_generated.gdshader and wrote its reading; chose the Use It measurements; played the game.",
                      "Claude Code (Opus 5.5): drafted CHANGE-BRIEF, TUNING, TEST-REPORT, FRICTIONAL; ran the scoped claude -p sessions (CLAUDE.md, both effects and previews, the driver, the tests, the cost script); the captures, mutations and strip measurements; F9; this film. Codex: the Use It editor measurements and captures.",
                      "Textures: none from outside. Every texture is a GradientTexture2D sub-resource inside slash_sparks.tscn and run_dust.tscn: no image asset, nothing to license. Narration: Liam, local Kokoro am_onyx.",
                      f"Source shown: walker-rudy assignment-6/game at {REV} (game source unchanged since d60fb03). Next: measure GPU time on a machine whose Visual Profiler reports it, and compare both effects with the 0.25 ms budget."]}}}})
B.append({"beat_id": "BHTF", "act": "your turn", "components": [],
  "narration_text": "Your turn. Here is the prompt; read it with me. Read my change brief and the dust scene. Before you change anything, "
                    "let me predict by hand how high the dust band's top rises if damping is halved, with the model from round three. Then, "
                    "on a copy, halve only damping, capture the preview strip, measure the top against a no-dust render, and show me your "
                    "number beside my prediction. Write your prediction down first. Liam, in for Bear.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Your turn.", "topic": TOPIC, "segment": TITLE,
    "command": "Read my CHANGE-BRIEF.md and game/effects/run_dust.tscn. Before you change anything, let me predict by hand how high the dust "
               "band's top rises above the walk line at strip frame 25 if damping_min / _max go from 120 / 180 to 60 / 90, using TUNING.md's "
               "r3 model. Then, on a copy of game/, change only those two lines, capture run_dust_preview.tscn with Movie Maker, measure the "
               "top against a no-dust render, and show me your number beside my prediction.",
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
    "game": {"name": "walker-rudy (assignment-6: game/)", "revision": "d0ed4152ba4c5dc88ac2d712dbdb5889b07c9f54", "short_revision": REV,
             "engine": "4.7.2.stable.official.ed1daf0bf", "folders": ["assignment-6/game"]}},
    "beats": B}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
print(f"wrote beat_sheet.json: {len(B)} beats")
