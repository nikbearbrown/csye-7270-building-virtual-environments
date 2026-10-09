# SCRIPT — walker-magic gamedev film (Brutalist `godot-gamedev` + `walker`)

> Approved beat sheet and script (2026-10-07). Narrator: Liam, in for Bear (local Kokoro `am_onyx`). Native 4K landscape. No burned captions. The final card is silent under the stock jingle.
> The SLICE AUDIO method (B18, B20): verbal approval from the instructor the method is acceptable (recorded 2026-10-07; see CAPTURE.md and FACTCHECK.md).

Title: **Her Fire Is the Only Warmth: Building a Cave Mage Slice**

Labels used on screen: **Reconstructed prompt** · **Godot editor reconstruction** (with source path and lines) · **Scripted-input capture** (every gameplay take) · **RAW GEMINI OUTPUT — not in engine** · **Asset file preview — not gameplay** · **Contact sheets — not gameplay** · **SLICE AUDIO — no narration · scripted-input capture** · **Held frame** where a frame is held.

## B01 — Walker opening (Claude composer)
*On screen:* Claude composer typing: "Please use Walker to convert my game design document about a young fire mage carrying the only warm light through a dark cave into a small Godot asset slice." — **Reconstructed prompt** (illustrative, not a session transcript).
*Narration:* "Here's the ask: turn a design document about a small fire mage in a dark cave into something you can actually play."

## B02 — Hesitant-writer summary (≥ 9 s window, `lead_silence_s: 0.8`, one working single-word correction)
"What got built: a two-screen Godot slice. One mage, one wolf, one pit, one exit. The art came from Gemini, the effects from Stable Audio, the music from Lyria. This film is about how those assets were designed, generated and wired in, not just that they exist."

## B03 — The assignment, and the build shown
"The assignment asks for six things. Concept and pillars. One asset traced from design to game. States and sounds in real play. A stretch where the game's own audio plays with no one talking over it. A cause and its effect. And an honest accounting. Everything you'll see running is revision 7 4 c 0 4 4 3, captured from a copy at 5 2 6 6 9 4 6 with identical game files."

## B04 — Concept and pillars
*On screen:* `CONCEPT.md` excerpt, then P1 in engine (**Scripted-input capture**, run-01).
"The pitch is one sentence: she carries the only warm light down into a cold cave. Four pillars. Every failure is fair. Her fire is the only warmth. You can read it at a glance, even muted. Small mage, big threat. Watch for the second pillar: everything in this cave is cool except her."

## B05 — Asset trace 1/5: the design
*On screen:* `CHARACTER-SHEET.md` excerpt (on-screen size, proportions, palette table, collision rectangle).
"The asset we'll follow is her idle pose. It starts as a promise in the character sheet: sixty-four pixels tall with the hat, a slender build, not chibi, six colours plus an outline, and a fourteen-by-forty-four hit box from her feet to her chin."

## B06 — Asset trace 2/5: the prompt
*On screen:* three prompt cards, verbatim from `SOURCES.md` → Image prompts — **Prompt drafted by Claude, sent by the author in the Gemini app** (model shown in the app: Gemini 3.8 Flash):
1. CHAR-REF v1 — "Pixel art character reference sheet for a 2D side-scrolling game. One original character shown four times at exactly the same height: front view, side view facing right, three-quarter view, back view. …" (full text on the card, including the palette line: white #E8E6F0, red #D62839, indigo #3A40A0, gold #D4A63A, gray-brown #6B5A4E, skin #F5DCCD).
2. Setup message (reference sheet + 9 pose sketches uploaded, no generation) — "… Use the sketches ONLY for body pose; ignore their faces, the eyepatch and their colors. …"
3. CHAR-IDLE v1 — "One correction: the tunic is mid-thigh length, exactly as in the reference sheet, not knee-length. Match the reference sheet whenever the text and the image disagree. Now draw the idle pose (sketch #02 Idle)."
*Narration:* "These are the prompts that went into the Gemini app, word for word. First a reference sheet: one original mage, four views at the same height, on flat green, with the character sheet's six colours written right into the prompt. Then a setup message that uploads the reference and nine pose sketches and says, use the sketches only for the pose. And then the idle pose itself, with one correction: the tunic stops at mid-thigh, because the reference sheet already drew it that way."

## B07 — Asset trace 3/5: the raw output
*On screen:* `design/character/generated/CHAR-IDLE-v1.jpg`, 1920x2184 on green — **RAW GEMINI OUTPUT — not in engine**.
"And this is what came back. To be clear, this is the raw Gemini output, not the game. It's nineteen hundred pixels tall on a green screen. Nothing on this screen has touched the engine yet."

## B08 — Asset trace 4/5: the edits (code)
*On screen:* `tools/clean_sprites.py` excerpt: green key, face-width scale, outline rule — a source view with path and line numbers (a Python tool, so not a Godot editor view).
"Cleanup is a script, so every edit is repeatable and logged. It keys out the green, scales the idle frame so she's exactly sixty-four pixels tall, and sizes every other pose by face width. Face height drifted about twenty percent with the hat brim, so width was the honest ruler."

## B09 — Asset trace 4/5: the edits (result)
*On screen:* `assets/sprites/EDIT-LOG.md` numbers and `assets/sprites/mage/mage_idle.png` at x6 — **Asset file preview — not gameplay**.
"Here's the result as a file: sixty-two by sixty-nine pixels, every pixel on the sheet's palette, all logged with hashes. Still a file preview, not gameplay."

## B10 — Asset trace 5/5: in the engine (code)
*On screen:* `features/player/player.gd` lines 17–26 (`TEXTURES`) and 130–135 (`_set_state`) — **Godot editor reconstruction**.
"In the engine, there's no animation. Each state is one image, and this dictionary decides which one. When the state changes, the texture swaps."

## B11 — Asset trace 5/5: in the engine (result)
*On screen:* idle → run → rise → fall over the pit → land — **Scripted-input capture** (run-01).
"And there it is, running: idle, run, up, down, over the pit and landing. This is a scripted-input capture, driven by real key events, not a person playing."

## B12 — Cause and effect (code)
*On screen:* `tools/clean_sprites.py` `apply_mage_revision` (dark fill, brim, boots).
"Now the cause and effect. On the cave background her stockings, boots and hat brim vanished. They'd been mapped to the outline colour, which is as dark as the cave itself. This rule lifts thick dark areas one step: stockings to the tunic shade, boots to the tunic base, and the brim to a lifted indigo."

## B13 — Cause and effect (result)
*On screen:* `design/checks/mage-palette-revision1-before-after.png` — **Contact sheets — not gameplay**; then the mage on the dark cave in engine — **Scripted-input capture**.
"Before and after, on the cave tone. That's a contact sheet, not gameplay. The darks moved from about L-star seven to between twenty and forty, against a cave whose darkest tones sit near five. And in the game, there she is: boots, stockings and brim all readable on the dark cave."

## B14 — Cast (code)
*On screen:* `features/player/player.gd` lines 101–113 (`cast()`) — **Godot editor reconstruction**.
"Her core action. A click turns her toward the cursor, spawns one fireball at the crystal, and starts a 0.35-second cooldown. Holding the button doesn't repeat."

## B15 — Cast and the wolf (result)
*On screen:* growl telegraph, cast, white flash, second hit, down image, gone — **Scripted-input capture** (run-01).
"The wolf always warns you. That's half a second of growl before it lunges. One hit flashes it white, the second puts it down, and then it's gone. Every failure is fair."

## B16 — Sound wiring (code)
*On screen:* `audio/audio_director.gd` lines 40–55 (`connect_game`) — **Godot editor reconstruction**.
"Sound is wired backwards from how you'd guess. The game never asks for a sound. It just announces events: cast, hurt, defeated, failed, cleared. This one node listens and plays. Mute everything and the game behaves exactly the same; the tests check that."

## B17 — Sound wiring (result)
*On screen:* the five event moments, each labelled with its sound ID — **Scripted-input capture** (run-01, run-02); footage silent under narration.
"Five events, five sounds: the cast, the hit she takes, the wolf going down, the fall into the pit, and the clear at the exit. You'll hear them for yourself in a second."

## B18 — SLICE AUDIO (no narration)
*On screen, throughout:* **SLICE AUDIO — no narration · scripted-input capture**. run-01 (cast, hurt, wolf down, clear, music stopping at the exit), then run-02 (pit fall, fail sound, music stops).
*Sound:* the take's own audio only, cut to the same interval as its video (verbal approval from the instructor the method is acceptable; see CAPTURE.md).

## B19 — Mute (code)
*On screen:* `game/main.gd` lines 65–70 (`toggle_mute`) — **Godot editor reconstruction**.
"Music and effects mute separately. M is the music bus, N is the effects bus."

## B20 — Mute (result), with a short SLICE AUDIO slot
*On screen:* M → "music off (M)", N → "sfx off (N)", a silent cast, then both back on — **Scripted-input capture** (run-03).
*Narration:* "M, and the music drops out. N, and now even her cast is silent." Then a short **SLICE AUDIO — no narration** slot from the same take.

## B21 — The automated check (code)
*On screen:* `tests/test_sound_triggers.gd` lines 121–125.
"This is the check the assignment asks for. A scripted run through the whole slice counts sound requests per event, and every count has to match the game event behind it."

## B22 — The automated check (result)
*On screen:* the recorded command output from `TEST-REPORT.md` (`WALKER TESTS: 11 checks / 0 failures`, route counts).
"And this is its real output: eleven checks, zero failures. Five casts give five cast sounds. A held button gives one, not a stream. Two fireballs in the same frame give one defeat. Here's the limit, though: the test runs headless on a dummy audio driver. It proves the triggers, not what you hear. That part was a person listening."

## B23 — Models, contributions and credits
*On screen:* which model made which asset · human and AI contributions · credits card: **Powered by Stability AI** and "This Stability AI Model is licensed under the Stability AI Community License, Copyright © Stability AI Ltd. All Rights Reserved." (Stable Audio Open 1.0), plus the SynthID note for Gemini images and music.
"Who made what. The Gemini app, on Gemini 3.8 Flash, made every image. Lyria in the same app made the music. Stable Audio Open, running locally, made the five effects; they're powered by Stability AI, under its community license. The exit, the hearts, the crosshair and the dark pit fill are drawn in code. The human chose the design, every accept and reject, and the scope. Claude drafted, wrote the code and ran the checks."

## B24 — Verdict
"The verdict. Implemented: every state, one wolf, five sounds on real events, a looping track, and readable when muted. Limitations: no boss, the HUD font is smooth instead of pixel, the hit box covers her head when she crouches, and the wolf's defeat image still has running legs. And six playtests, all human, are where 'it feels fair' and 'the loop is clean' come from. The next step toward the full game is the boss arena: the same wolf scene at twice the size, ten HP, and a two-damage lunge, exactly as the concept already specifies."

## B25 — Your Turn
"Your turn. Ask Walker to shorten the wolf's growl from half a second to a third. Before you run it, predict what happens to the hurt count in the real-lunge test. Then run the test and see if you were right."

## B26 — Outro
Locked `ClaudeTitleOutro` (exact title, @NikBearBrown, one slug-seeded mascot, no subline). Silent under the stock jingle; no narration, no game audio.
