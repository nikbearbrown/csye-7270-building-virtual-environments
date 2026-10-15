#!/usr/bin/env python3
"""Write beat_sheet.json for the Lanternfall godot-gamedev (walker) film.

Code excerpts are read from godot/ at run time by line range, so what the film shows is the file's text. Run it
again after narration is measured: measured durations are kept and every Remotion beat's durationSeconds and
highlight times are re-derived from them (a highlight lands where its phrase sits in the narration).

    python3 tools/make_reel.py
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / "godot"
FILM_SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()
SHORT = FILM_SHA[:7]
SLUG = "claude-liam-walker-lanternfall-bao-x-gamedev"
TITLE = "Lanternfall, Taken Apart"
PROJECT = "walker-lanternfall-bao-x"
HANDLE = "@NikBearBrown"


def excerpt(path: str, a: int, b: int) -> str:
    return "\n".join((GAME / path).read_text().splitlines()[a - 1:b])


def at(text: str, phrase: str, dur: float, lead: float = 0.25) -> float:
    """Seconds into the beat where `phrase` is spoken, by its position in the narration."""
    i = text.find(phrase)
    if i < 0:
        raise SystemExit(f"cue phrase not in narration: {phrase!r}")
    return round(max(0.0, dur * i / max(1, len(text)) - lead), 2)


def code_beat(bid, act, path, a, b, title, narration, cues, notes, output, est, font=None):
    return {"beat_id": bid, "act": act, "kind": "code",
            "role_note": f"Code beat (code-then-result-v1): {path} lines {a}-{b} at {SHORT}, read verbatim; the next beat shows the result.",
            "narration_text": narration, "estimated_duration_s": est,
            "_cues": cues,
            "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "line-highlight",
                     "show": [{"at": "0.0", "event": f"Godot editor reconstruction opens on {path}, lines {a}-{b}"}] +
                             [{"at": c[0], "event": f"line {c[1]} highlights — {c[2]}"} for c in cues] +
                             [{"at": "notes", "event": "source-notes panel (not Inspector values) lists the related lines"}],
                     "remotion": {"pattern": "GodotDevWorkbench", "props": {
                         "mode": "code", "title": title, "project": PROJECT, "path": f"res://{path}",
                         "source": f"godot/{path} · lines {a}–{b} · source revision {SHORT} · Godot editor reconstruction",
                         "code": excerpt(path, a, b), "startLine": a, "codeFontSize": font or 25,
                         "inspectorLabel": "Source notes — not Inspector values",
                         "notes": [{"label": k, "value": v} for k, v in notes], "output": output,
                         "cues": [], "durationSeconds": est}}},
            "_excerpt": {"path": path, "start_line": a, "end_line": b}}


OBSERVED = {
    "B08": "In the 4K capture the walking courier shows the walk_contact and walk_passing frames of pc_sheet.png, mirrored when he moves left; the comparison image lines up blockout, generated frame and in-game capture.",
    "B10": "Real captures show each pose the code selects: walk, cast, hurt with the red flash, the levelup card-screen portrait, sunflare after evolving, and the defeat and victory result-panel portraits.",
    "B12": "In 2:55-3:00 of the main take the counters, taken from the take's own play log and kill signal, show many kills sharing few kill sounds.",
    "B14": "Esc at run 0:40 freezes the field under the PAUSED line for 3 s and the run resumes where it stopped; the timer reads 0:40 before and after.",
    "B17": "Build 40102ab: a bolt overlaps a moth's visible wing outside the old 10 px circle and flies on, the moth unharmed. Film build: a bolt meets a wing tip outside the old circle and the moth drops a gem.",
    "B19": "At run 0:58 the Sunflare Lighthouse card is offered first; once taken, the banner, the zoom-out and the sunflare pose appear.",
    "B22": "Holding right, the courier stops at the stall's edge; holding down-right, he slides along it instead of sticking.",
    "B24": "Each M, 9 and 0 press flips the HUD's MUSIC/SFX line while the moths keep coming and the run continues.",
    "B28": "Recorded output of the three suites on an isolated copy of the film build: 32 + 65 + 25 checks pass, and the independence record shows identical summaries with and without sound.",
}


def media_beat(bid, act, narration, show, est, role, evidence=False):
    b = {"beat_id": bid, "act": act, "kind": "result" if evidence else "evidence",
         "role_note": role, "narration_text": narration, "estimated_duration_s": est,
         "shot": {"type": "VIDEO", "class": "SHOW", "source": "own", "motion": "real-footage",
                  "show": [{"at": s[0], "event": s[1]} for s in show], "treatment": "none"}}
    if evidence:
        b["shot"]["evidence_media"] = f"media/{bid}.mp4"
        b["observation"] = OBSERVED[bid]
    return b


def listen_beat(bid, show, role):
    return {"beat_id": bid, "act": "REPORT", "kind": "source_report", "clock": "source", "audio_policy": "preserve",
            "role_note": role, "narration_text": "",
            "shot": {"type": "SOURCE_REPORT", "class": "SHOW", "source": "own", "motion": "real-footage",
                     "show": [{"at": s[0], "event": s[1]} for s in show], "treatment": "none"}}


ASK = ("Please use Walker to convert my game design document about a lamp-headed courier who must survive three "
       "minutes in a fog-bound night market into a playable Godot asset slice. Generate every sprite, sound effect "
       "and music loop with local open models, log every candidate, and make sure sound never decides the game.")

BEATS = [
    {"beat_id": "B00", "act": "ASK",
     "role_note": "COLD OPEN LAW — Claude composer; reconstructed Walker prompt from Bao's design documents (not a recorded session). Liam introduces himself.",
     "narration_text": ("Merhaba — this is Liam, in for Bear. Bao Xing's second assignment: design a game on paper first, "
                        "then generate its art, four sound effects and a music loop with free local models, and prove they "
                        "work together in a playable Godot scene. Bao's game is called Lanternfall. Here is the ask, "
                        "rebuilt from his design documents."),
     "estimated_duration_s": 22,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card on cream; greeting 'Merhaba, Liam'"},
                       {"at": "0.25", "event": "the reconstructed Walker prompt types in"},
                       {"at": "0.62", "event": "send arms; running line names the four design documents"},
                       {"at": "0.75", "event": "three result lines: assets and runs, source revision, checks and playtests"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Merhaba, Liam", "topic": "WALKER · GODOT GAMEDEV", "segment": "Lanternfall",
                  "command": ASK,
                  "runningText": "reading CONCEPT.md · STORYBOARD.md · CHARACTER-SHEET.md · CHANGE-BRIEF.md…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["23 assets from local models · 99 runs logged",
                             f"Playable slice: godot/ at source revision {SHORT}",
                             "122 automated checks · two playtests by Bao"]}}}},
    {"beat_id": "B01", "act": "BLUF",
     "role_note": "EXECUTIVE-SUMMARY LAW — hesitant writer. The framing a viewer arrives with ('AI made the game') is corrected to what the film shows ('AI made the assets').",
     "narration_text": ("The short version. AI made the assets — not the game. Local models produced twenty-three of them: "
                        "fourteen sprites and props, seven sound effects and two music loops, chosen from ninety-nine logged "
                        "runs. Every one that shipped was Bao's pick. And one rule runs through the code: sound reacts to the "
                        "game, but never decides anything in it."),
     "estimated_duration_s": 20, "lead_silence_s": 0.8,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on-correct",
              "show": [{"at": "0.0", "event": "cream page; 'AI made the game' types"},
                       {"at": "0.3", "event": "'game' struck in terracotta, 'assets' typed in"},
                       {"at": "0.6", "event": "'Bao picked every one' and 'sound decides nothing' type in"}],
              "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
                  "text": "AI made the game\nBao picked every one\nsound decides nothing",
                  "triggerWords": "game", "replacementWords": "assets", "fontSize": 180, "lineSpacing": 1.5,
                  "align": "center", "seed": str(sum(map(ord, SLUG))), "mistakeRate": 2, "hesitateWithin": 0,
                  "hesitateBetween": 1, "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"}}}},
    {"beat_id": "B02", "act": "CONCEPT",
     "role_note": "Concept and pillars (film item 1). Excerpt verbatim from CONCEPT.md at design-v1; pillar cards are the four pillar headings with their first sentence.",
     "narration_text": ("The design was committed and tagged before a single image existed. A lamp-headed courier has to keep "
                        "moving for three minutes in a fog-bound night market until the fog lifts. Four pillars. Light is "
                        "power. Feet, not fingers: moving is the only verb. Readable in silence. And three-minute runs, where "
                        "losing costs nothing. Every later change is appended as a revision, never rewritten."),
     "estimated_duration_s": 25,
     "_cards": [("Light is power", 0), ("Feet, not fingers", 1), ("Readable in silence", 2), ("three-minute runs", 3)],
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "card-cues",
              "show": [{"at": "0.0", "event": "CONCEPT.md excerpt (In two sentences) beside four pillar cards"},
                       {"at": "Light is power", "event": "card 1 highlights"},
                       {"at": "Feet, not fingers", "event": "card 2 highlights"},
                       {"at": "Readable in silence", "event": "card 3 highlights"},
                       {"at": "three-minute runs", "event": "card 4 highlights"}],
              "remotion": {"pattern": "GodotDesignBoard", "props": {
                  "title": "The concept, frozen first", "section": "CONCEPT.md · In two sentences",
                  "excerpt": ("A lamp-headed courier is trapped in a fog-bound midnight market, and the light on his "
                              "shoulders is his only weapon. Keep moving, grow the light, and survive three minutes until "
                              "the fog lifts."),
                  "source": "CONCEPT.md at tag design-v1 (46d2fe2, 2026-09-28 15:21 EDT) · first generation commit e384933 is a day later",
                  "status": "Committed before any generation · later changes appended as revisions R1–R6",
                  "visualLabel": "Design pillars", "layout": "cards",
                  "cards": [{"label": "1 · Light is power", "text": "Everything that helps you is warm light; everything that hurts you is cool fog."},
                            {"label": "2 · Feet, not fingers", "text": "Movement is the only verb. Every real decision lives in the level-up cards."},
                            {"label": "3 · Readable in silence", "text": "Every event that has a sound also has a visual."},
                            {"label": "4 · Three-minute runs", "text": "A run is short, a loss costs nothing, retry is one key."}],
                  "cues": [], "durationSeconds": 25}}}},
    listen_beat("B03", [("0.0", "title screen — silent by design (the menu has no music)"),
                        ("3.0", "the run starts: MUS-01 night-market loop from the top"),
                        ("5.9", "first kill — SFX-01; gems fly in — SFX-02"),
                        ("11.5", "level-up — SFX-04; cards held 2 s; music −6 dB"),
                        ("13.5", "card taken, music back to full")],
                "Game sound only, no narration (film item 5): the first 16 s of the main take, seed 11. SFX labels come from the capture's own AudioBus play log."),
    media_beat("B04", "TRACE",
               ("Now one asset, traced end to end: the courier's sprite sheet. It starts as design, not generation. "
                "Before any model ran, the character sheet fixed the rules: a thirty-two pixel frame, a lamp eleven to "
                "thirteen pixels tall, feet on the bottom row, facing right with the code flipping it, and five locked "
                "colours. Everything generated later is measured against this page."),
               [("0.0", "CHARACTER-SHEET.md blockout, design-v1: 12 poses drawn by script at 32 px, shown x8"),
                ("rules", "the seven consistency rules appear one by one"),
                ("palette", "the five character colours with their hex values")], 22,
               "Asset trace 1/4 (film item 2): design. Pre-generation blockout and palette images from design/character/ (committed at design-v1)."),
    media_beat("B05", "TRACE",
               ("The first prompt asked for a flat-vector model sheet with twelve poses. FLUX returned a shaded, "
                "three-dimensional illustration and ignored the grid. Bao rejected it: this is a two-dimensional pixel "
                "game, and it doesn't need many poses. So the prompt was rewritten for each pose as a pixel-art sprite, "
                "with every exclusion spelled out, because this model takes no negative prompt."),
               [("0.0", "first batch raw output (seed 11) with its logged prompt — REJECTED, Bao's words"),
                ("rewritten", "the walk_contact prompt, verbatim from its log, with seed and settings"),
                ("negative", "'no negative prompt' note from the log")], 24,
               "Asset trace 2/4: prompt. Raw output and prompts verbatim from gen/log/ART-PC-01 sidecars."),
    media_beat("B06", "TRACE",
               ("Here is the raw output for the walking pose, seed eleven. Then the logged edits, in order: key out the "
                "white background and the grey shadow, mirror it to face right, scale it so the lamp is exactly twelve "
                "pixels, and lock every pixel to the palette at thirty-two by thirty-two. Re-running those steps "
                "reproduces the shipped frame, pixel for pixel."),
               [("0.0", "raw 512 x 512 output, walk_contact, seed 11"),
                ("key out", "keyed: background and shadow transparent"),
                ("mirror", "mirrored to face right"),
                ("twelve", "fitted at 4x: lamp 48 px = 12 px at game size"),
                ("lock", "palette-locked 32 x 32 frame, shown x16"),
                ("pixel for pixel", "check: identical to frame 3 of pc_sheet.png")], 24,
               "Asset trace 3/4: raw output and edits. Stage images re-run with gen/art_process.py functions (tools/asset_trace_stages.py); the last stage equals the shipped frame."),
    code_beat("B07", "CODE", "features/player/player.gd", 106, 113, "Drawing the frame in Godot.",
              ("In Godot, that frame is drawn by the courier's draw function. Line one oh seven mirrors the whole sprite "
               "when he faces left, so only right-facing art exists. Line one oh nine turns the current pose into a "
               "frame index, and line one ten cuts that thirty-two pixel cell out of the sheet, offset so the torso, not "
               "the lamp, sits on the hurtbox."),
              [("Line one oh seven", 107, "facing = −1 mirrors the sprite"),
               ("Line one oh nine", 109, "pose → frame index (POSES, line 11)"),
               ("line one ten", 110, "32 × 32 cell, drawn from -SPRITE_ORIGIN (16, 23)")],
              [("POSES (lines 11–12)", "10 frames; walk_contact is index 2"),
               ("SPRITE_ORIGIN (line 15)", "(16, 23): coat on the r = 10 hurtbox"),
               ("No texture (line 112)", "placeholder shapes; same run (tested)")],
              ["Art.texture(Art.PC_SHEET) · res://assets/art/pc_sheet.png (320 × 32)"], 22),
    media_beat("B08", "RESULT",
               ("And this is the result in the running game: the same walking frame, mirrored when he heads left. The "
                "comparison image lines up the blockout, the generated frame and the in-game capture. What held: size, "
                "palette, outline, feet on the floor. What broke: the generated courier came out shorter, so his torso "
                "sat below the hurtbox until the sprite origin moved down three pixels."),
               [("0.0", "real capture: the courier walking, zoomed crop of the 4K take, frame-accurate"),
                ("comparison", "design/character/sheet-vs-game.png: blockout · generated · in game · silhouette"),
                ("broke", "callout: origin (16, 20) → (16, 23), test hurtbox-centred-on-torso")], 24,
               "Result of B07 and asset trace 4/4: Godot. Real 4K engine capture and the comparison image from CHARACTER-SHEET R3.",
               evidence=True),
    code_beat("B09", "CODE", "features/player/player.gd", 78, 87, "Which pose, when.",
              ("Which frame? This function decides, in priority order. A pose the session forces wins first: level-up, "
               "Sunflare, victory or defeat. Then twelve ticks of hurt after a hit, then eight ticks of cast after "
               "every shot, then the two walking frames, swapping every eight ticks. Standing still falls through to "
               "idle."),
              [("A pose the session forces", 79, "override_pose: levelup · sunflare · victory · defeat"),
               ("twelve ticks of hurt", 81, "hurt: first 12 of the 48 i-frame ticks"),
               ("eight ticks of cast", 83, "cast: 8 ticks after each shot"),
               ("two walking frames", 86, "walk_contact / walk_passing every 8 ticks"),
               ("idle", 87, "idle")],
              [("override_pose (session.gd)", "levelup · victory · sunflare · defeat"),
               ("Tuning", "i-frames 48 · hurt 12 · cast 8 ticks"),
               ("WALK_FRAME_TICKS (line 16)", "8")],
              ["step() calls choose_pose() once per tick (line 73)"], 20),
    media_beat("B10", "RESULT",
               ("Here are those states in real footage. Walking, with the two frames swapping. Casting each time the "
                "beam fires. The hurt flinch with the red flash. The level-up pose while the cards are up. The Sunflare "
                "pose after the evolution, coat brightened. And the two endings, defeat and victory. Every one of them "
                "also reads with the sound off."),
               [("Walking", "walk_contact / walk_passing (main take)"), ("Casting", "cast"),
                ("hurt", "hurt + red flash (main take 1:08)"), ("level-up", "levelup during a card screen"),
                ("Sunflare", "sunflare pose after evolving"), ("defeat", "defeat (lose take)"),
                ("victory", "victory at 3:00 (main take)")], 22,
               "Result of B09 (film item 3: character states). Real 4K captures, each labelled with the pose the code chose.",
               evidence=True),
    code_beat("B11", "CODE", "audio/audio_bus.gd", 19, 28, "One table throttles every sound.",
              ("Now sound. Every effect goes through one table. A kill sound can repeat only every sixty milliseconds, "
               "with at most three voices at once. Pickups share one voice. Hurt waits eight hundred milliseconds, and "
               "the evolution plays once per run. The clock is the simulation tick, not the wall clock, so the same run "
               "always makes the same sounds."),
              [("A kill sound", 20, "kill: 60 ms cooldown, 3 voices"),
               ("Pickups share one voice", 21, "pickup: 1 voice"),
               ("Hurt waits", 22, "hurt: 800 ms"),
               ("once per run", 24, "evolve: once"),
               ("simulation tick", 28, "VOICE_MS 300: one voice slot")],
              [("sfx() (lines 84–103)", "asks sfx_gate.gd: time + live voices"),
               ("now_ms() (lines 81–82)", "tick_count × 1000 / 60 — simulation time"),
               ("Line 2", "“…Never writes game state.”")],
              ["signals in: enemy_killed · gem_collected · player_hurt · evolved · state.changed (lines 63–68)"], 22),
    media_beat("B12", "RESULT",
               ("In a dense wave the throttle shows up in these counters, read from this very take: monsters die faster "
                "than the kill sound is allowed to fire, so several kills share one sound instead of machine-gunning. "
                "In Bao's sound-on playtest, his note was simply that nothing ran together."),
               [("0.0", "real capture of a dense wave"),
                ("counters", "live counters from the take's own logs: kills vs kill sounds played"),
                ("nothing ran together", "Bao's Run A note, quoted on screen: 不会连起来")], 16,
               "Result of B11. Real 4K capture; counters computed from the capture's AudioBus play log and the session's kill count.",
               evidence=True),
    code_beat("B13", "CODE", "audio/audio_bus.gd", 126, 137, "Music follows the game state.",
              ("Music follows the game state through one signal. Paused: a low-pass filter and ten decibels down. "
               "Level-up cards: the chime, and six decibels down, like a held breath. Back to play: both restored. On a "
               "loss or a win, further down, the music fades and a stinger plays. None of this writes anything back into "
               "the game."),
              [("Paused", 128, "PAUSED → low-pass on, −10 dB"),
               ("Level-up cards", 132, "LEVELUP → SFX-04, −6 dB")],
              [("PLAYING (lines 138–142)", "after pause or cards: filter off, 0 dB"),
               ("LOST / WON (lines 143–148)", "fade 0.5 s / 1 s, then the stinger")],
              ["PAUSE_DB −10 · LEVELUP_DB −6 · LOWPASS_HZ 900 (lines 29–32) · lines 133–134: one chime per card screen (review fix 8aaad72)"], 22, font=23),
    media_beat("B14", "RESULT",
               ("At forty seconds the script presses Escape. For three seconds the field freezes under the pause line, "
                "then the run picks up exactly where it stopped. In the mix, those three seconds sit ten decibels down "
                "behind a nine-hundred-hertz low-pass, and the timer reads forty on both sides. Next, the same stretch "
                "with only the game's own sound."),
               [("0.0", "real capture: run at 0:40"), ("Escape", "key label at the real press; PAUSED line; label: low-pass 900 Hz, −10 dB"),
                ("picks up", "key label at the second press; label: filter off, 0 dB")], 16,
               "Result of B13. Real 4K capture of the scripted pause at 0:40 (Esc via the input map).",
               evidence=True),
    listen_beat("B15", [("0.0", "level-up chime, cards held 2 s, music ducked"),
                        ("pause", "pause: music muffled and quieter"),
                        ("resume", "resume: full music")],
                "Game sound only: level-up duck, then pause and resume (main take)."),
    code_beat("B16", "CODE", "game/session.gd", 273, 284, "The change: bullets hit what you see.",
              ("The code change. In his first playtest Bao saw bullets fly on through monsters, and asked for them to "
               "vanish on a hit. The old test compared the bolt's centre with a small circle, ten pixels for a moth. "
               "The new loop treats the bolt as "
               "the fourteen-pixel segment it is, on line two seventy-eight, and tests the monster's visible sprite box. "
               "A hit spends one pierce; at zero, the bolt is gone."),
              [("The old test", 278, "was: centre distance < radius + 4"),
               ("fourteen-pixel segment", 278, "now: segment ±7 px tested against the sprite box"),
               ("spends one pierce", 281, "pierce − 1"),
               ("the bolt is gone", 283, "pierce 0 → removed")],
              [("Before a51af69", "centre distance < e.radius + BEAM_RADIUS (4)"),
               ("enemy.gd lines 33–38", "touches_segment: a point every 2 px"),
               ("Tuning hit_half", "moth 11 × 7 · wraith 13 × 19 (half px)")],
              ["Bao, 2026-09-29: “子弹 打到怪物之后 要求消失” · commit a51af69 · tests beam-stops-on-moth-wing, beam-stops-on-wraith-hood"], 24, font=23),
    media_beat("B17", "RESULT",
               ("Here is what the player sees. On the left, the build Bao played: this bolt clips the moth's wing and "
                "keeps going. On the right, the film build: a bolt meets a wing tip, outside the old ten-pixel circle, "
                "and stops there. Two tests failed before the fix and pass after it, and Bao's next playtest note read: "
                "the bullets are right."),
               [("0.0", "left: build 40102ab (Bao's first playtest), held frame, bolt inside a moth's wing; right: film build"),
                ("keeps going", "left: the next frames, the bolt flies on"),
                ("stops there", "right: held frame at a wing-tip hit, then the bolt is gone"),
                ("Two tests", "RED → GREEN test names; Bao: 子弹对的")], 22,
               "Result of B16 (film item 6: a source change and what the player sees). Two real captures with the same capture driver: build 40102ab (before a51af69) and the film build. Held frames are labelled; overlap/hit moments come from the driver's read-only diagnostic.",
               evidence=True),
    code_beat("B18", "CODE", "features/progression/progression.gd", 93, 102, "The evolution rule.",
              ("The evolution rule lives in the card offer. The pool of eligible cards is shuffled with the run's own "
               "seeded generator. But once both weapons reach level three, the Sunflare card goes first, so it can't be "
               "missed. Taking it replaces the beam and the moths with one pulsing burst of light."),
              [("shuffled", 96, "Fisher–Yates with the run's seeded rng"),
               ("goes first", 102, "evolution_ready() → 'sunflare' first")],
              [("evolution_ready() 76–77", "beam ≥ 3 and moths ≥ 3, not evolved"),
               ("WEAPON_MAX (line 8)", "3"),
               ("session.gd _evolve() 341", "clears bolts; brighter coat, pose")],
              ["offer_cards(rng) runs when a level-up is pending (session.gd line 142)"], 20),
    media_beat("B19", "RESULT",
               ("In this run that happens at fifty-eight seconds. The Sunflare Lighthouse card leads the offer, and the "
                "script takes it. The banner appears, the camera pulls back to show the burst's reach, and the courier "
                "takes the Sunflare pose, coat brightened. The music gains its second layer. Next, the same moment with "
                "only the game's sound."),
               [("0.0", "real capture: card screen, SUNFLARE LIGHTHOUSE first"), ("banner", "banner and zoom-out"),
                ("Sunflare pose", "sunflare pose, brighter coat")], 18,
               "Result of B18. Real 4K capture, main take, run time 0:58.", evidence=True),
    listen_beat("B20", [("0.0", "hit — SFX-03 hurt"), ("chime", "level-up — SFX-04"),
                        ("evolve", "Sunflare card — SFX-05 evolve; MUS-02 layer fades in over 2 s")],
                "Game sound only: hurt, level-up, evolution and the music layer (main take)."),
    code_beat("B21", "CODE", "features/player/player.gd", 56, 63, "Props that block.",
              ("Bao also asked for the lamp posts and stalls to block him. Movement is still one line: position plus "
               "input times speed. Then, on line sixty-one, the market pushes the courier's ten-pixel circle out of any "
               "solid box, along the shortest way out, before the arena clamp. Monsters never make this call, so they "
               "fly over the stalls."),
              [("Movement is still one line", 58, "position += (axis × speed + knock) / 60"),
               ("line sixty-one", 61, "blocker.push_out(position, PLAYER_RADIUS)"),
               ("arena clamp", 63, "arena clamp")],
              [("blocker", "the market (ground.gd); null = open field"),
               ("ground.gd push_out 153–177", "shortest way out of each solid box"),
               ("SOLID_BOX ground.gd 25–30", "sprite's opaque area inset 2 px")],
              ["CONCEPT R5 — Bao: “路灯这些有阻挡效果”"], 20),
    media_beat("B22", "RESULT",
               ("In the real take, the script walks the courier to a stall and holds right: he stops at the stall's edge. "
                "Then it holds down and right, and instead of sticking, he slides along the edge. The box is the sprite's "
                "opaque area inset by two pixels, so what stops him is what you see."),
               [("0.0", "real capture: the courier walks to the nearest stall"), ("holds right", "blocked at the edge"),
                ("slides", "holding down-right: slides along the stall")], 16,
               "Result of B21. Real 4K capture, props take (seed 11): scripted input through the real input map.",
               evidence=True),
    code_beat("B23", "CODE", "game/session.gd", 362, 374, "Mute touches the mixer only.",
              ("Mute is three keys: M for everything, nine for music, zero for effects. Each one flips the mute flag of an "
               "audio bus, nothing else. The game state never hears about it, and the heads-up display rebuilds its "
               "music and effects line from those bus flags, so the screen always says what the speakers are doing."),
              [("M for everything", 369, "mute_all → Master bus"),
               ("nine for music", 371, "mute_music → Music bus"),
               ("zero for effects", 373, "mute_sfx → SFX bus")],
              [("audio_bus.gd 198–200", "toggle_bus: flips the bus mute"),
               ("hud.gd line 49", "MUSIC/SFX on-off line from the flags"),
               ("Key map (line 397)", "mute_all M · mute_music 9 · mute_sfx 0")],
              ["no game state is read or written on these lines"], 20, font=23),
    media_beat("B24", "RESULT",
               ("Watch the top-right corner while the script presses M, then nine, then zero, each one twice. The line "
                "flips between on and off for music and effects, and the moths keep coming. The run itself doesn't change "
                "at all: a test replays a seeded run with every sound removed and ends in exactly the same state."),
               [("0.0", "real capture, props take; HUD corner enlarged beside it"), ("M,", "key labels at each real press: M, M, 9, 9, 0, 0"),
                ("flips", "HUD line: MUSIC off SFX off → on → MUSIC off → on → SFX off → on")], 16,
               "Result of B23. Real 4K capture: M / 9 / 0 sent through the input map, each toggled back after 2 s.",
               evidence=True),
    listen_beat("B25", [("0.0", "music and effects"), ("M", "M: silence while the game plays on"),
                        ("9", "9: effects only"), ("0", "0: music only")],
                "Game sound only: what the mute keys do to the mix (props take)."),
    listen_beat("B26", [("0.0", "hits — SFX-03"), ("lose", "HP 0: music fades 0.5 s, SFX-06a lose stinger"),
                        ("restart", "R: the stinger stops, a fresh run starts the music from the top")],
                "Game sound only: losing and retrying (lose take, seed 3)."),
    code_beat("B27", "CODE", "tests/test_audio.gd", 69, 74, "Testing that sound decides nothing.",
              ("The tests. These lines close the audio suite's seeded autoplay run. First, exactly one stinger at the end. "
               "Then the same seed is replayed with every sound stream removed and the master bus muted, and the final "
               "state is compared field by field: tick, kills, level, health, position. If sound could change the game, "
               "these two summaries would differ."),
              [("exactly one stinger", 70, "one-stinger"),
               ("every sound stream removed", 71, "fresh(11, false, true): no streams, Master muted"),
               ("compared field by field", 74, "independence: loud == silent")],
              [("Lines 64–68", "once-* checks, kill throttle, pickups"),
               ("summary() (lines 43–46)", "state, tick, kills, level, hp, x, y …"),
               ("Limits", "how it feels needs a playtest")],
              ["evidence/audio.json"], 22),
    media_beat("B28", "RESULT",
               ("Recorded output from the film build: thirty-two logic checks, sixty-five gameplay, twenty-five audio, all "
                "passing. The independence check prints both runs: same tick, same kills, same level, same position. "
                "What tests can't prove is how it feels, which is why Bao played it twice himself, once with sound and "
                "once muted."),
               [("0.0", "recorded terminal output of the three suites, run on an isolated copy of the film build"),
                ("independence", "the independence record: with sound vs silent"),
                ("twice", "Bao's Run A / Run B notes, quoted")], 20,
               "Result of B27. Recorded tool output (not drawn): the suites run on the film build; Bao's notes from evidence/playtest.",
               evidence=True),
    media_beat("B29", "ROLES",
               ("Who did what. Bao chose the genre, the theme, the scope and the local-only rule, picked every asset "
                "that shipped, listened to every sound-effect candidate, and played both test runs. Claude wrote the Godot code, the tests and the generation "
                "scripts, ran the models, measured each candidate and suggested a pick. FLUX made all fourteen images, "
                "Stable Audio Open the seven effects, and MusicGen both loops."),
               [("0.0", "three columns: Bao · Claude · models"), ("FLUX", "asset table: every asset ID with its model and revision")], 24,
               "Who did what (film item 8) and which model made each asset (film item 9). From FRICTIONAL.md's header line, SOURCES.md and the gen/log sidecars."),
    media_beat("B30", "LIMITS",
               ("What's still uncertain. The fog-wraith has the lowest measured contrast against the ground, though it "
                "read fine in Bao's muted run. The hurtbox also reaches the lower lamp. The gamepad is untested, balance "
                "comes from Bao and scripted bots, and his two playtests came before the final review fixes, which tests "
                "cover. Next: more weapons, a boss, and progress between runs."),
               [("0.0", "three panels: tested · uncertain · next"), ("uncertain", "open items from TEST-REPORT §16 and §12")], 24,
               "Tests, uncertainties and next steps (film item 7). From TEST-REPORT.md and CONCEPT.md."),
    {"beat_id": "B31", "act": "VERDICT",
     "role_note": "ClaudeVerdictArtifact — implemented work, limitations, human judgment; shows the source revision (film item 10).",
     "narration_text": ("The verdict. What's implemented: the design came first, every asset is local and logged, and it all "
                        "runs together in one playable slice at source revision eight a six f nine eight eight. The strongest "
                        "engineering choice is that sound can never decide the game, and a test proves it. The limits are "
                        "small and written down. The judgment calls were Bao's."),
     "estimated_duration_s": 22,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "artifact-reveal",
              "show": [{"at": "0.0", "event": "artifact card 'Verdict', heading with the source revision"},
                       {"at": "0.2", "event": "implemented line"}, {"at": "0.45", "event": "sound-independence line"},
                       {"at": "0.65", "event": "limits line"}, {"at": "0.85", "event": "human-judgment line"}],
              "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
                  "artifactTitle": "Verdict", "artifactHeading": f"Lanternfall · source revision {SHORT}",
                  "brandLabel": HANDLE,
                  "artifactLines": ["Implemented: design-v1 before any generation; 23 local assets in one playable slice.",
                                    "Sound decides nothing: same seed, sound removed, same final state.",
                                    "Limits: wraith contrast, hurtbox over the lamp, no gamepad test.",
                                    "Human judgment: every shipped asset picked, both playtests — Bao's."]}}}},
    {"beat_id": "B32", "act": "HANDOFF",
     "role_note": "HANDOFF LAW — Your Turn: one bounded code change plus a prediction and a test. Liam reads the prompt and signs off.",
     "narration_text": ("Your turn. Paste this: Please use Walker to read the audio bus in my Lanternfall project. Change "
                        "only the kill sound's cooldown from sixty milliseconds to zero. Before running anything, predict how "
                        "many kill sounds play when twenty moths die in the same tick, and which audio tests fail. Then run "
                        "the suite and compare. Write your number down first: the voice cap still applies. Liam, in for "
                        "Bear."),
     "estimated_duration_s": 32,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card; greeting 'Your turn.'"},
                       {"at": "0.1", "event": "the paste-ready prompt types in"},
                       {"at": "0.7", "event": "three output lines: prediction first, run, revert"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Your turn.", "topic": "WALKER · GODOT GAMEDEV", "segment": "Lanternfall",
                  "command": ("Please use Walker to read godot/audio/audio_bus.gd in my Lanternfall project. Change only "
                              "the kill sound's cooldown_ms from 60 to 0. Before running anything, predict how many kill "
                              "sounds play when twenty moths die in the same tick, and which checks in "
                              "tests/test_audio.gd will fail. Then run the audio suite and compare."),
                  "runningText": "reading godot/audio/audio_bus.gd · godot/audio/sfx_gate.gd…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Prediction written before the run.", "Audio suite run: compare with your number.",
                             "Then put the 60 ms back."], "animateTyping": True}}}},
    {"beat_id": "B33", "act": "OUTRO",
     "role_note": "OUTRO LAW — ClaudeTitleOutro: exact title, @NikBearBrown, slug-seeded mascot, stock jingle only, no narration.",
     "narration_text": "", "estimated_duration_s": 10.361, "actual_duration_s": 10.361,
     "audio_file": "mp3/beat-B33.wav",
     "audio_note": "stock @NikBearBrown jingle logos/bear-brown/bear-brown-6.mp3, picked by the slug seed the outro uses (char-sum 4283 mod 6 pool files), never cut: padded with 1.0 s of silence; no narration (Liam signs off in B32)",
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "mascot-title",
              "show": [{"at": "0.0", "event": f"title '{TITLE}'"}, {"at": "0.25", "event": "@NikBearBrown"},
                       {"at": "0.45", "event": "slug-seeded mascot"}],
              "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "durationSeconds": 10.361}}}},
]


# B29 (who did what, which model) plays right after the asset trace ends (B08), so the two summary boards
# (B29, B30) never run back to back.
ORDER = ["B00", "B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B29", "B09", "B10", "B11", "B12", "B13",
         "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28",
         "B30", "B31", "B32", "B33"]
BEATS = sorted(BEATS, key=lambda b: ORDER.index(b["beat_id"]))


def main() -> None:
    path = REEL / "beat_sheet.json"
    old = {b["beat_id"]: b for b in json.loads(path.read_text())["beats"]} if path.exists() else {}
    beats = []
    for b in BEATS:
        b = json.loads(json.dumps(b))
        prev = old.get(b["beat_id"], {})
        for k in ("actual_duration_s", "audio_file", "render_duration_s"):
            if k in prev and k not in b and prev.get("narration_text") == b.get("narration_text"):
                b[k] = prev[k]
        if prev.get("shot", {}).get("remotion", {}).get("rendered") and "remotion" in b["shot"]:
            b["shot"]["remotion"]["rendered"] = prev["shot"]["remotion"]["rendered"]
        dur = b.get("actual_duration_s") or b.get("estimated_duration_s")
        cues = b.pop("_cues", None)
        cards = b.pop("_cards", None)
        b.pop("_excerpt", None)
        rem = b["shot"].get("remotion")
        if rem and "durationSeconds" in rem["props"]:
            rem["props"]["durationSeconds"] = round(float(dur), 2)
        if cues:
            rem["props"]["cues"] = [{"at": at(b["narration_text"], p, dur), "line": ln, "label": lab} for p, ln, lab in cues]
        if cards:
            rem["props"]["cues"] = [{"at": at(b["narration_text"], p, dur), "card": i} for p, i in cards]
        b.setdefault("voice", "am_onyx")
        b.setdefault("engine", "kokoro")
        beats.append(b)
    sheet = {"metadata": {
        "title": TITLE, "slug": SLUG, "topic": "WALKER · GODOT GAMEDEV", "kind": "godot-gamedev", "modifier": "walker",
        "playlist": "CSYE 7270", "brand": "claude-liam", "audience": "CSYE 7270 classmates and instructors",
        "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
        "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "contain",
        "captions": False, "channel_title": "", "channel": HANDLE, "folderLabel": HANDLE,
        "channel_title_note": "empty on purpose: B00's composer already shows @NikBearBrown (OUTRO-LOCK: one handle per beat)",
        "greeting": "Merhaba, Liam",
        "greeting_note": "hello lexicon: Merhaba (Turkish). Liam never takes Wagwan (IN-FOR-BEAR LAW).",
        "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
        "game": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x", "project_dir": "godot",
                 "source_revision": FILM_SHA, "godot": "4.7.2.stable.official.ed1daf0bf"},
        "teaching_contract": "code-then-result-v1",
        "note": ("godot-gamedev + walker teardown of Bao Xing's CSYE 7270 Assignment 2. Every code panel is a verbatim "
                 f"excerpt of godot/ at {FILM_SHA}; every gameplay shot is a real Movie Maker capture of an isolated copy "
                 "of that revision (one comparison shot comes from build 40102ab), driven through the real input map by "
                 "the disclosed capture driver. No paid call, no upload."),
        "links": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x"},
        "tags": ["Godot 4", "godot-gamedev", "Walker", "game audio", "FLUX.1-schnell", "Stable Audio Open",
                 "MusicGen", "CSYE 7270", "Teardown register", "Kokoro"]},
        "beats": beats}
    path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    words = sum(len(b["narration_text"].split()) for b in beats)
    est = sum(float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in beats)
    print(f"{path}: {len(beats)} beats, {words} words, ~{est:.0f}s before source reports are measured")


if __name__ == "__main__":
    main()
