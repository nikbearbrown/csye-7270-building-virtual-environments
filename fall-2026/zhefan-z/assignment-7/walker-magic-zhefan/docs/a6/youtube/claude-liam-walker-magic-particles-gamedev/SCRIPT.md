# SCRIPT — walker-magic Assignment 6 gamedev film (Brutalist `godot-gamedev` + `walker`)

> Narrator: Liam, in for Bear (local Kokoro `am_onyx`). Native 4K landscape, 30 fps. No burned captions. The final card is silent (this toolkit copy has no stock jingle, as in Assignments 1–5).
> Narration lines are written for the voice: numbers, names and the commit are spelled the way they should be spoken. On-screen text keeps the exact spelling and figures of the source named on each card.
> Sources of truth, in order: CHANGE-BRIEF.md (with revisions), TUNING.md, TEST-REPORT.md, FRICTIONAL.md, SOURCES.md, effects/, shaders/particles_generated.gdshader, the tests and their logs, the strips in captures/. FACTCHECK.md maps every sentence. Game source revision shown: 3c37fe0.

Title: **A Burst and a Trail: Two Particle Effects for One Fireball**

Labels used on screen: **Reconstructed prompt** · **Suggested prompt** · **Scripted input · real engine output** (capture/run-01: the real main scene, played by capture/driver.gd through mouse and key events; Movie Maker, windowed, 640×360 at 30 fps, shown ×5 nearest neighbour) · **Replay, ×0.25** · **Last frame held** · **Fixture capture** (the committed preview strips, 640×360, not gameplay) · **Document view — reconstruction of the text, not a screenshot** · **Godot editor reconstruction** (with path and lines) · **Source view — reconstruction, not a screenshot** · **Recorded results — not a render**.

## B00 — Walker opening (Claude composer)
*On screen:* `ClaudeComposerAsk`, greeting "Merhaba, Liam". Prompt (**Reconstructed prompt**): "Please use Walker to convert my game design document about a fire mage's fireball into two particle effects: an impact burst of sparks and smoke wherever it lands, and a flame trail while it flies — each specified first, tested headlessly, tuned from frame strips and priced on the GPU." Output lines: `effects/fireball_impact.tscn · Sparks + Smoke · on Fireball.explode()`; `effects/fireball_trail.tscn · turbulence · sphere emission · while the fireball exists`; `test_fireball_impact.gd · 14 checks / 0 failures at 30, 60 and 144 fps`; `test_fireball_trail.gd · 20 checks / 0 failures at 30, 60 and 144 fps`.
*Narration:* "Merhaba — this is Liam, in for Bear. The ask: two particle effects for one fireball. A burst of sparks and smoke wherever it lands, and a flame trail while it flies — each one specified first, tested without a screen, tuned from frame strips, and priced on the GPU."

## B01 — Hesitant-writer summary (window ≥ 9 s)
*On screen:* typed in five lines, "Two effects for / one fireball: / a burst, a trail. / Each is a / picture." Correction (one word): "picture" → "program".
*Narration:* "Two effects for one fireball: a burst, and a trail. Each one is a program, not a picture — particles are born, moved, then drawn. The hard part was checking all three steps without ever seeing them."

## B02 — The game, the jobs, the event and the condition
*On screen:* card: one frame of the scripted-input capture (a cast at the start of the level, the trail behind the fireball) and one at the impact; Effect A's job and event, Effect B's job and condition (CHANGE-BRIEF.md "The job" sections; fireball.gd lines); game source revision 3c37fe0.
*Narration:* "The game is walker magic: a pixel-art mage crosses a cave and casts fireballs at a wolf. Effect A, the impact, tells the player where and when a shot landed — on the wolf, a wall or the ground. Its event is Fireball dot explode. Effect B, the trail, shows where a shot is heading. Its condition: the fireball exists and hasn't exploded."

## B03 — Where both effects hook in (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `features/fireball/fireball.gd` lines 43–49 (the panel shows no more at a readable size); cues on lines 43–45 (the unchanged A2 flash), 46–48 (the impact), 49 (`_release_trail()`). Notes: lines 61–63, the release (reparent, stop, free); line 28, the timeout path calls the same release.
*Narration:* "Both effects hang off one function. Explode keeps the old flash exactly as it was, then instances the new impact into the fireball's parent — Main — so the impact outlives the fireball. Then it releases the trail: reparent it to Main, keeping its place; switch emitting off; free it one particle lifetime later. The two second timeout calls the same release."

## B04 — One cast, in the running game (result)
*On screen:* **Scripted input · real engine output** — capture/run-01 frames 6–70 at real speed (the click at frame 16, the impact at 29), then **Replay, ×0.25** of frames 10–70, then **Last frame held**.
*Narration:* "Here's that code in the running game, with scripted input: one click into the ground — and then the same second again, at quarter speed. The trail follows the fireball out of the staff. It lands: the flash and the sparks burst, and the trail's last particles fade where they were, instead of vanishing with the fireball."

## B05 — Emission, process, draw
*On screen:* **Source view — reconstruction, not a screenshot**: three panels, one line each — emission `effects/fireball_impact.tscn:80` `amount = 24` (with 83 `one_shot = true`, 85 `explosiveness = 1.0`); process `shaders/particles_generated.gdshader:324` `USERDATA1.xyz += force * DELTA;`; draw `effects/fireball_impact.tscn:8` `blend_mode = 1` (with 81 `texture = ExtResource("2_spark")`).
*Narration:* "Every particle system has three parts. Emission decides how many particles are born, and when: twenty-four sparks, all at once, once. Process moves each one, every frame, in a shader on the GPU. Draw turns them into pixels: a four-by-four pixel texture, added onto the cave. The colour ramp belongs to process, not draw — the author's first answer got that one wrong."

## B06 — Why the headless price is near zero
*On screen:* **Recorded results — not a render**: what a headless run sees (CLAUDE.md "Headless facts", A6; TEST-REPORT.md): 0 draw calls, empty `capture_rect()`, no GPU particle process; instance counts, `one_shot`, `amount_ratio`, visibility observable; `emitting` false once all are emitted; `finished` did not fire → aliveness by instance; 4.6 vs 6.6 µs/frame with 6 impacts.
*Narration:* "So why does a GPU effect cost almost nothing headless? A headless run swaps in a dummy renderer: zero draw calls, an empty capture rect, and no process shader ever runs. The CPU only pays for a few nodes. What headless can see is node state — instance counts, one shot, emitting. And emitting turns false as soon as a burst has emitted, not when its sparks die. So every test here checks aliveness by instance."

## B07 — Effect A, the intent
*On screen:* **Document view** · `CHANGE-BRIEF.md` lines 27–34 (the intent) and 69–74 (rules A1–A6); the timing phases highlighted.
*Narration:* "Effect A's intent was written before any setting. Frame zero, a bright flash. Sparks fly fast for point one five seconds, then slow, cool to red and vanish by point four five. A small grey puff grows and fades by point eight. Everything is gone by point nine, so the next cast lands on a clean spot. Six rules say when it must appear, and when it must not."

## B08 — The sparks' process settings (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `effects/fireball_impact.tscn` lines 25–36; cues on 25 (`particle_flag_disable_z`), 28 (`spread`), 29–30 (velocity), 31 (gravity), 32–33 (damping), 36 (scale curve).
*Narration:* "These are the sparks' process settings, as saved in the scene. Spread one eighty — a full circle, and flat, because particle flag disable z is on. Initial velocity ninety to one sixty, gravity three hundred down, damping forty to sixty, a scale curve from one to zero. Every value lives in the scene file; none of it is in code."

## B09 — The first strip (result)
*On screen:* **Fixture capture** — `captures/fireball_impact/r0/` frames 10, 12, 15, 20, 30, 50, cropped around the impact and enlarged; under each, the brief's reading for that frame (CHANGE-BRIEF.md line 141).
*Narration:* "Here's the first strip: a fixture capture from the preview scene, thirty frames a second — not gameplay. Frame ten: the flash and the first sparks. Twelve: spreading. Fifteen: the flash is gone. Twenty: dark-red specks, and the smoke. Thirty: faint smoke. Fifty: empty. Frame n shows about n minus nine thirtieths of a second after the trigger."

## B10 — Tuning step r0b: the preview, not the effect
*On screen:* **Fixture capture** — `r0-retrigger/` and `r0b-retrigger/` frames 20 and 30 side by side; Claude's measurement (0.83 scale fit, 1.6 px vs 4.1 px for a 15°-rotated control); the change (preview seeds `first_seed + 1000 × spawn index`, `0069149`); the prediction; the author's verdict (TUNING.md r0b).
*Narration:* "Tuning step one wasn't the effect at all. In the retrigger strip, the author saw two impacts that looked stamped. Claude measured it: the second matched the first scaled by point eight three, a one point six pixel error, against four point one for a rotated control. The preview had given it seed plus one. The fix spaced the seeds by a thousand. Prediction: from frame twenty they stop lining up. The author's verdict: different now. Kept."

## B11 — Tuning step r1: the smoke's colour ramp (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `effects/fireball_impact.tscn` lines 44–46; cues on 45 (offsets 0, 0.125, 1) and 46 (alpha 0 → 0.55 → 0). Notes: before (offsets 0, 1; alpha 0.55 → 0), TUNING.md r1; `35a1f70`.
*Narration:* "Step two came from play. The author wanted the moment of impact brighter. Measured against an empty frame, frame ten's centre was a grey disc: the smoke, drawn over the sparks at full opacity from age zero. The change was one setting — the smoke's colour ramp — so the puff now fades in over its first tenth of a second."

## B12 — r0 against r1 (result)
*On screen:* **Fixture capture** — `r0/` and `r1/` frames 10 and 12, same crop, enlarged; prediction and measurement (TUNING.md r1): frame 10, pixels above 200 within 12 px 86 → 175, centre 144 → 230; frame 12 −5 % (predicted −33 %); the author's verdict.
*Narration:* "Before and after, same fixture. Frame ten matched the prediction, and more: pixels above two hundred went from eighty-six to one seventy-five, and the centre from one forty-four to two thirty. Frame twelve missed — about minus five percent, not minus thirty-three. The reason: each frame was one step older than assumed. The author's verdict, in the game: brighter. Kept."

## B13 — Effect A in play, with rapid repeats (result)
*On screen:* **Scripted input · real engine output** — capture/run-01 frames 72–527 at real speed: a shot into the left wall at the screen edge (frames 86–92), the walk and the jump over the pit, two hits on the wolf (311, 333), nine casts into the ground, one click every 11 frames (0.367 s; cooldown 0.35 s) (384–496); then **Replay, ×0.25** of the two hits on the wolf (frames 302–340), then **Last frame held**.
*Narration:* "And in play, with scripted input. A shot into the left wall bursts right at the screen's edge, and nothing is cut off. The mage walks, jumps the pit, and hits the wolf twice — one impact per hit. Then rapid casting, a click about every point three seven seconds, just over the cooldown: each impact is a new instance, overlapping the last. How it reads in play was judged by the author in the running game."

## B14 — Effect B, the intent and the feature A doesn't use
*On screen:* **Document view** · `CHANGE-BRIEF.md` lines 84–91 (the intent), 117–121 (rules B1–B5), 82 (the feature A doesn't use: turbulence, a sphere emission shape).
*Narration:* "Effect B is a trail. It shows where a shot is heading. Its intent: start on the fireball's first frame, a short steady flame behind it — sixty to eighty pixels at two sixty a second — and when the fireball ends, stop emitting and fade within point three seconds, where it is. It also uses what Effect A doesn't: turbulence, and a sphere emission shape."

## B15 — The trail's process settings (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `effects/fireball_trail.tscn` lines 25–38; cues on 25–26 (sphere, radius 3), 27 (direction), 31 (gravity), 36–38 (turbulence); lines 39–40 (influence) as a note. Note: the direction probe (CHANGE-BRIEF revision 2026-11-06, `7957614`; probe `e174c96`).
*Narration:* "In the scene: emission shape one, a sphere of radius three. Direction minus one, zero — which the brief first called world space. A probe on the GPU showed it follows the fireball's rotation, so it always means behind the fireball, while gravity stays in world space, so the flame rises either way. Turbulence is on: strength one, scale two, influence point one to point two."

## B16 — The trail's first strip (result)
*On screen:* **Fixture capture** — `captures/fireball_trail/r0/` frames 10, 12, 20, 30, 40, 45, 50, cropped along the path and enlarged; the measurements from TUNING.md (r1 entry, Claude's reading of r0).
*Narration:* "The trail's first strip: a carrier crossing the frame at two sixty pixels a second, from frame ten, stopping at frame forty. At frame thirty it's about seventy-one pixels long — on target. But it's only four to six pixels tall, a third of the intent, and beaded: dots every eight point seven pixels, with dark gaps between them."

## B17 — Tuning step r1: the scale curve (code)
*On screen:* `GodotDevWorkbench` · **Godot editor reconstruction** · `effects/fireball_trail.tscn` lines 15–18; cues on 16 (`max_value = 2.0`) and 17 (points (0, 2) → (1, 0)). Notes: before, linear 1 → 0; `cc1f2f2`; the colour ramp stays "same as Sparks" (CHANGE-BRIEF.md).
*Narration:* "The author wanted the trail a little thicker, or brighter. The colour ramp had to stay the same as the sparks, so the change was the scale curve: from one-to-zero to two-to-zero, with max value two — because a curve clamps its points to one by default."

## B18 — r0 against r1 (result)
*On screen:* **Fixture capture** — `r0/` and `r1/` frames 30 and 40, same crop, enlarged; prediction and measurement (TUNING.md r1): head 4–6 → 11–13 px, frame 40 changed pixels 120 → 370, gaps 3–5 → 1–3 px; the author's verdict.
*Narration:* "The prediction: heads of eight to twelve pixels, overlapping into a continuous strip. The measurement: every pixel lit in r zero is still lit, the head is eleven to thirteen pixels, and lit pixels at frame forty tripled. But the strip closes only behind the head; one to three pixel gaps remain further back, because each dot shrinks as it ages. The author: thicker, and brighter. Kept."

## B19 — Effect B in play: start, stop, pause (result)
*On screen:* **Scripted input · real engine output** — capture/run-01 frames 531–907 at real speed: a shot to the right that times out (cast 623, released 683), a shot to the left into the wall (706–740), a shot to the right with Esc pressed mid-flight (paused 787–835) and Esc again; then **Replay, ×0.25** of the leftward shot (frames 700–745), then **Last frame held**.
*Narration:* "Effect B in play, scripted input again. A shot to the right times out after two seconds, and its trail fades in place. A shot to the left trails behind it, to the right — the rotation at work. Then Escape, mid-flight: the trail freezes under the pause screen, and resumes on the second Escape. In the state test, a pause right after an impact held the fading trail, and it was freed point three seconds of game time later."

## B20 — The process shader Godot writes
*On screen:* **Source view — reconstruction, not a screenshot**: `shaders/particles_generated.gdshader` line 139 beside `effects/fireball_impact.tscn` lines 29–30; lines 311 and 324 beside line 31 (gravity); annotations (TEST-REPORT.md "The process shader").
*Narration:* "What does the process step look like inside? The author converted a scratch process material into the shader Godot writes. Line one thirty-nine picks each particle's speed between the minimum and the maximum — the sparks' ninety and one sixty. Lines three eleven and three twenty-four start the force from gravity and add it to the velocity every frame, times delta — the sparks' three hundred."

## B21 — What the tests proved
*On screen:* **Recorded results — not a render** (TEST-REPORT.md "Machine checks"): configuration A 54 / 0, B 32 / 0; state A 14 / 0 and B 20 / 0 at 30, 60 and 144 fps, what each covers (A1–A6, B1–B5); the nine earlier suites with their baseline counts; not covered.
*Narration:* "What did the tests prove? Two configuration tests read every setting back from the loaded resources: fifty-four checks for the impact, thirty-two for the trail. Two state tests drive real mouse casts and real Escape presses through the game loop, at thirty, sixty and one forty-four frames a second: fourteen and twenty checks, zero failures at every rate. The nine earlier suites kept their counts."

## B22 — Broken on purpose
*On screen:* **Recorded results — not a render**: mutation a1 (`initial_velocity_min = 90.0` → `initial_velocity = 90.0`: exit 1, 2 failures; no error or warning; still fires, speed 0–160 instead of 90–160) and a2 (Sparks `lifetime` 0.45 → 0.6: exit 1, 1 failure); `ab0784c`.
*Narration:* "Do the tests fail when they should? Mutation one renamed initial velocity min to its Godot three name. Godot four point seven still has a property by that name — a pair — so the float was dropped silently: no error, no warning, and the effect still fired, at zero to one sixty instead of ninety to one sixty. Only the read-back caught it: exit one, two failures. Mutation two drifted the sparks' lifetime to point six: exit one."

## B23 — The headless price, with its control
*On screen:* **Recorded results — not a render** (TEST-REPORT.md "Price", `tests/cost_effects.gd`, `f7787c4`): control 3.82 ± 0.96 µs, effects off 240.83 ± 45.38, Effect A ×6 253.58 ± 47.54, Effect B heaviest 296.42 ± 57.87; own price after the dry case A +8.2 µs, B +25.1 µs.
*Narration:* "The price. Headless, the empty control scene costs under four microseconds a frame; the game scene with effects off, about two forty. Six impacts add about eight microseconds of their own; the heaviest trail load, about twenty-five — both inside the scene's own frame-to-frame spread. A dry run of the same driver, with no effects, kept the script from measuring itself."

## B24 — The GPU price, against the budget
*On screen:* **Recorded results — not a render** (TEST-REPORT.md, Visual Profiler, RTX 5060 Laptop GPU): Update GPUParticles absent / 0.01 / 0.09 ms; Render Viewport 0.03 / 0.04 / 0.04 ms; over case 1 ≈ 0.02 and ≈ 0.10 ms; budgets 0.5 ms (about 4 %) and 0.3 ms (about 33 %); FPS vsync on 160 / 161 / 167, off 995 / 999 / 985.
*Narration:* "On the GPU, in the Visual Profiler: Update GPU Particles is absent with the effects off, point zero one milliseconds with six impacts, and point zero nine at the heaviest trail load. Against budgets of point five and point three milliseconds, that's about four percent, and a third. With vsync off, FPS sat near a thousand in all three cases, under one percent apart — so FPS alone would have hidden both costs."

## B25 — What no headless run shows
*On screen:* **Recorded results — not a render**: TEST-REPORT.md "What no headless run shows" beside "Human checks" (the author's words, translated).
*Narration:* "And what can't any headless run show? Whether either effect is visible, or reads well; its colour, size and timing on screen; whether the GPU keeps simulating a hidden emitter; and real frame timing. Those are the strips, and the author's eyes in the running game: the smoke clearly visible over the pit, the trail readable over the lighter ground, nothing cut off at the walls."

## B26 — What the agent got wrong
*On screen:* card: FRICTIONAL.md entries 10, 13 and 14 — the agent's claim and what corrected it.
*Narration:* "What did the agent get wrong? Three things, each caught by measuring. Its smoke prediction assumed the wrong frame timing; frame twelve missed, and that taught the n minus nine rule. Its trail prediction used the head's size for the whole trail, so the gaps stayed. And its first cost script timed its own bookkeeping — forty-one and eighty-one microseconds — until it timed only the frame."

## B27 — Overruled, uncertain, and one next step
*On screen:* card: the frame-20 reading the author overruled (TUNING.md r0b, FRICTIONAL.md 9); still open (FRICTIONAL.md "Still open"); one next step, **Proposed by this film**.
*Narration:* "Where the author overruled Claude: it read frame twenty as sparks too dark, too soon. Watching in slow motion, the author judged the rhythm right, and nothing changed. Still uncertain: why the trail beads every eight point seven pixels, why vsync-off FPS stops near a thousand, whether a hidden emitter keeps simulating — and the spent guard, which no test reaches. One next step: a test that makes one fireball touch two bodies in a single frame."

## B28 — Who did what
*On screen:* card: FRICTIONAL.md "Human and AI contributions"; SOURCES.md and assets/textures/fx/ATTRIBUTION.md (spark.png and smoke.png written by code; no sourced or model-generated textures); game source revision 3c37fe0.
*Narration:* "Who did what. The author chose both effects and their look, made every prediction-to-verdict call, played, captured the strips, read the GPU, and converted the shader. Claude Code built the scenes, tests, previews, probe and price tools. Claude in chat planned and compiled the documents. No sourced texture: the spark and the smoke are written by code. The game shown is revision three c three seven f e zero."

## B29 — Verdict
*On screen:* `ClaudeVerdictArtifact` — Built · Measured · Judged · Unknown.
*Narration:* "The verdict. Built: two GPU particle effects, wired to one function, with settings only in scene files. Measured: every setting read back, every rule tested at three frame rates, two mutations caught, a GPU price inside both budgets. Judged by the author: both effects read in play, after one change to each effect. Unknown: why the trail beads, and the guard no test has reached."

## B30 — Your Turn
*On screen:* `ClaudeComposerAsk`, greeting "Your turn.", **Suggested prompt**: "Please use Walker to add a test to my fireball state test that makes one fireball touch two bodies in the same physics frame — a wall corner and the ground — and checks that explode() spawns exactly one impact and detaches exactly one trail. Predict first which of my rules fails if the _spent guard is removed, then remove it on a copy and show the test fail."
*Narration:* "Your turn. Here's a prompt: Please use Walker to add a test to my fireball state test that makes one fireball touch two bodies in the same physics frame — a wall corner and the ground — and checks that explode spawns exactly one impact and detaches exactly one trail. Predict first which of my rules fails if the spent guard is removed, then remove it on a copy and show the test fail. That's the one gap this film left open; the interesting part is whether your test can actually produce two contacts in one frame. Take it, run it on your own game. Liam, in for Bear."

## B31 — Regular outro
*On screen:* `ClaudeTitleOutro` (locked): the title, @NikBearBrown, one slug-seeded mascot. Silent.
