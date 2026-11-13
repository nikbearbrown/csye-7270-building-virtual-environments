# Prompts and script — claude-liam-walker-survival-shooting-a6-gamedev

## Reconstructed opening prompt (B00)
Illustrative reconstruction written for this film. It is **not** a saved session or a historical transcript.

```text
Please use Walker to convert my game design document about a third-person extraction shooter, where a survivor lives in a subway base, into its first particle effects: dust at the player's feet on every landing, and dust hanging in the air of the base only while the ceiling lights are on, with a brief, read-back tests, frame strips and a price for each.
```

## Your Turn prompt (B30)

```text
Please use Walker on my Godot project. Read my CHANGE-BRIEF and effects/landing_dust.tscn. Enlarge the Dust emitter's visibility_aabb so it contains the r1 puffs. Before you change anything, predict what my edge-of-screen check will show, then capture again and compare.
```

No model was run for the film except Kokoro (am_onyx) for the narration.

## Narration script (Kokoro am_onyx, exact text sent to TTS)

**B00 · ASK**

Hola, this is Liam, narrating for Jonathan. The prompt on screen is a reconstruction for this film, not a saved session. It asks Walker to give a subway extraction shooter its first particle effects: dust when the player lands, and dust in the air that lives only while the lights are on. At source revision one, eight, two, eight, b, b, six, b, the answer is two effects, four tests, a cost script, and eighteen fixture strips.

**B01 · BLUF**

Claude built the particles from my brief; I judged every strip and every change. The tests prove the settings and the timing; only the pictures show the look.

**B02 · SETUP**

The game: a survivor in a subway base. Effect A is landing dust. Its job is to say you touched the ground, and its event is a new signal, landed, on the character's body. Effect B is dust hanging in the air, for atmosphere. Its condition is the ceiling lights: on, the dust is there; off, it is gone.

**B03 · INTENT**

Before anything was built, I wrote the intent. Timing: strongest at a tenth and a half of a second, gone at one point six. Scale: about one and a half capsules wide. Two layers: dust, and a faint ring on the floor. And the retrigger rule: a second landing restarts it, so at most one burst is alive.

**B04 · CODE**

A particle system has three parts, and this one node shows all three. Emission: how many and when. Line one seventeen, twenty-four particles; one-shot, all at once on line one twenty-one. Process: what each particle does over its life, here a ParticleProcessMaterial on line one twenty-four. Draw: what each particle looks like, a quad mesh on line one twenty-five.

**B05 · RESULT**

The first strip, r zero, from the preview scene, a fixture. Triggered on frame ten; the picture first changes on frame eleven. The ring is clear. The dust is a few warm dots, gone by frame thirty. My verdict before Claude read anything: I want grey cloud-like puffs, not dots.

**B06 · TUNING**

That wish broke the brief's ankle-height rule, so I revised the intent first, then tuned. Revision r one changed one setting: the dust quad from eight to thirty-two centimetres. The agent edited before my approval, and sent its prediction afterwards; I approved after the fact and kept it. Its prediction held at most frames, including thirty: bigger, still visible at point seven seconds. At frame fifty it missed. I stopped tuning here, on my in-game judgement.

**B07 · CODE**

Now the event. After every move, the body asks: am I on the floor now, and was I in the air last frame? Then this frame is a landing, and line one thirteen emits landed, once. Line one fifteen is a fix: on load, the physics engine pushed the player up out of the floor, which counted as a landing. The test caught it.

**B08 · RESULT**

In the running game, with scripted key presses. Two single jumps: dust and a ring at the feet. Then four rapid jumps, mostly while moving left, each landing inside the last burst's lifetime. Each time, the old dust is cleared and plays again where the feet are. Replayed at twice the size: no pile-up.

**B09 · CODE**

The trigger listens to landed. It moves to the feet, then calls restart on both emitters, not emitting equals true. Restart clears a burst that is still alive and starts a new one here. Setting emitting would do nothing to a live one-shot burst.

**B10 · RESULT**

The retrigger strip: a second landing on frame twenty-five, half a metre away. On twenty-five the old dust is gone; on twenty-seven the new ring starts at the new spot; the old cloud never comes back. The state test checks the same rule by real key presses: with emitting equals true instead, it fails.

**B11 · INTENT**

Effect B has a different job: atmosphere, not feedback. Its first intent was a small box of dust under one light. It must already be settled on its first frame, frozen when paused, gone when hidden or when the lights go off. Later I revised it to fill the whole room, lit by the lights.

**B12 · CODE**

Its process material uses what Effect A does not. A box emission shape, moved to the room's centre by an offset. Turbulence, so specks drift on noise instead of straight lines. And an opacity ramp with several peaks, so each speck twinkles in and out. The draw material adds light rather than covering, and preprocess runs six seconds before the first frame.

**B13 · TUNING**

The specks are one or two pixels, so each raw crop sits beside a computed difference against a frame with the dust hidden. First strip, r zero: a hundred and fifty specks under one light. I said the size should vary, and it was too dense. Revision r one changed one setting, amount, from a hundred and fifty to ninety. The agent proposed first this time; its prediction, about seventy changed pixels, measured seventy-four. Kept.

**B14 · TUNING**

Then, in the game, I had to walk up to a light to see anything. So I asked for the whole room, lit by the lights, sizes from three millimetres to three centimetres, all at once. That is a redesign recorded in the brief, not a tuning round. Three thousand specks was too dense and too bright; I chose nine hundred at half brightness, then thirteen hundred.

**B15 · CODE**

The condition lives in a listener on the dust. Lights on: show it and restart once, which reruns preprocess. Lights off: hidden that frame, and no new births. It never touches the lights; it only reads them.

**B16 · RESULT**

In the game, through a film camera near the first light, with scripted F presses at the switch. The inset is computed: it shows where the dust is. Lights off, the dust is gone that frame. Lights on, it is back already spread out. Paused from code, it freezes. Hidden, gone; shown again, full at once.

**B17 · CODE**

I converted Effect B's process material into a shader in the editor. Line two sixty-one is my brief's box: a random point in a cube, times emission box extents, seven, one point three, four point five. Line two sixty-three adds the offset, zero, point one five, three point two. That is why the box is fourteen by nine metres and centred on the room.

**B18 · RESULT**

And here is that box on screen: the computed difference of the final strip spans the whole frame, not one light. The settings decide where specks are born; the shader is the code that does it, on the GPU.

**B19 · CODE**

Line two fifty-three runs every frame: the colour is multiplied by the colour ramp at the particle's age. That is my opacity ramp, zero, point six, point one five, point nine, and so on, so each speck brightens and dims several times. Gravity is lines three ninety-seven and four ten, but both effects set gravity to zero.

**B20 · RESULT**

The ramp on screen, in the final fixture strip. Frames eleven and forty have the same density but different specks lit. Paused, frames forty-six and fifty-four are identical. Hidden, nothing. Shown on sixty-six, full at once. Lights off on seventy-one, nothing left glowing.

**B21 · CODE**

The tests read settings back from the loaded scene. First they ask ClassDB whether each property name exists in this engine, so a stale name fails loudly. Then every value is compared with the brief.

**B22 · RESULT**

All four pass, headless at sixty frames per second: a hundred fifty-seven, twenty-seven, a hundred ten and forty-one. The state tests press real keys: Space and D for landings, S and F for the lights, and check restart counts, pause and hide.

**B23 · RESULT**

Then I broke it. Mutation one: the Godot three name, initial velocity. The engine loaded it silently; in four point seven that name is an editor-only pair, so the float is dropped and the minimum speed becomes zero. Only the read-back caught it. Mutation two: amount thirty, brief unchanged. Both exit one.

**B24 · CODE**

The headless price, the chapter's way: time each frame as the gap between two process frames, three hundred frames, three repeats, round-robin, with an empty-scene control and a ten thousand CPU-particle control.

**B25 · RESULT**

Empty scene: point zero zero four milliseconds. Ten thousand CPU particles: one point eight eight. So the script sees CPU work. Effect A adds point zero zero six, Effect B point zero two five, both inside the noise. That is expected: headless Godot uses a dummy renderer, so GPU simulation and drawing never run. Near zero says nothing about the GPU.

**B26 · RESULT**

The GPU price, on an R T X fifty-seventy Ti laptop GPU, windowed, vsync off, lights kept on, reading the engine's measured GPU time. Effect B adds point zero one seven milliseconds against a point three budget; Effect A about point zero zero one against point two. With vsync on, F P S reads one forty-four; my debug key V turns it off, and F P S rises to about thirteen fifty, so the comparison is not capped.

**B27 · LIMITS**

What no headless run can show: whether anything is visible, reads well, or is too bright. That is the strips and my own play. One thing I am not sure of: Effect A's visibility box. Since r one, the puffs reach point two three metres up and point six eight out, beyond the box's point two and point six, so they may vanish early at the screen edge. Enlarging it is my next step.

**B28 · JUDGEMENT**

Agent mistakes I caught: it forgot the fixed seed on the preview; its first wiring fired the dust on scene load; and in tuning it edited before I approved. Claude's strip readings I overruled: it said the dust was too warm, cut flat by the floor, hidden by the capsule, and not six to eight separate puffs. In the game I do not see those as problems. A human lands, not a mech.

**B29 · VERDICT**

Verdict. Built: two effects, their triggers, four tests, a cost script and a GPU helper. Human: the brief, every verdict, the redesign values, the shader conversion and the play test. AI: the scenes, tests, previews and strip readings, by Claude Code with Opus five point five; and this narration, by local Kokoro. Textures: none from outside; both effects draw with gradient textures defined in their scene files. Shown: revision one, eight, two, eight, b, b, six, b. Next: enlarge Effect A's visibility box.

**B30 · HANDOFF**

Your turn. Paste this into Claude. Please use Walker on my Godot project. Read my change brief and my landing dust scene. Enlarge the Dust emitter's visibility box so it contains the r1 puffs. Before you change anything, predict what my edge-of-screen check will show, then capture again and compare. The prediction is the point: write down what should change before you look. This was Liam, narrating for Jonathan.

**B31 · OUTRO**

claude liam, walker survival shooting, a six, gamedev. At Nik Bear Brown.
