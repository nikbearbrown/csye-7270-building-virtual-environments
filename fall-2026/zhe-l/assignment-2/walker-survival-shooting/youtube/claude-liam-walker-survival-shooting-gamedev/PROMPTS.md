# Prompts and script — Walker Survival Shooting, Before the Slice

## Reconstructed opening prompt (B00)
Illustrative reconstruction written for this film. It is **not** a saved session or a historical transcript.

```text
Please use Walker to convert my game design document about a third-person extraction shooter, where a survivor lives in a subway base and carries a rugged military tablet, into a Godot asset slice with generated art, sound and music.
```

## Your Turn prompt (B19)

```text
Please use Walker on my Godot project. Read my CHANGE-BRIEF event-to-sound map and base.tscn. Pick one sound event and write the smallest change that plays it on that event, plus a test that logs how many times it fired for one short press, one long press and a held key. Predict the counts before you run it.
```

## Generation prompts shown in the film
Prompt A1 (rejected V01) and A4 (accepted V03) are quoted from the game's SOURCES.md appendix; the full
texts and every seed are there. The film adds no new generation; no model was run for the film except
Kokoro for narration.

## Narration script (Kokoro am_onyx, exact text sent to TTS)

**B00 · ASK**

Hej — this is Liam, in for Bear. On screen is a reconstructed prompt, not a saved session. It asks Walker to turn a design document about a subway extraction shooter into a Godot asset slice. The honest answer, at source revision f, eight, four, eight, d, eight, four: the design and the first assets exist. The playable slice does not, yet.

**B01 · BLUF**

Walker Survival Shooting is not a finished asset slice. Right now it is a design record and a greybox: written design, a full asset log, three generated sounds, and one empty subway room. Here is how each piece got made, and what is missing.

**B02 · CONCEPT**

The idea, in plain terms. You live in a subway under a ruined city, and you carry a rugged military tablet. Each run you go up, fight monsters, loot, and extract. Die, and you lose what you carried. Three pillars. The tablet is gameplay, and the world never pauses while it is open. Maps are small but dense. And the best loot is guarded, so extraction is high risk, high reward.

**B03 · STORYBOARD**

This is the designer's hand sketch for storyboard panel three, the core action. A short press of Tab takes the tablet out in one hand, and a small window opens in the corner of the screen while you keep walking. A long press switches to two hands. And the panel's sound line asks for one thing: a short startup beep. That beep is the asset I will trace.

**B04 · CHARACTER**

The character sheet was built the same way. The designer directed ChatGPT image drafts and rejected the wrong ones: glossy materials, a coat tucked into the skirt, a thigh holster, armor built into the body. The accepted turnaround keeps a matte coat outside the skirt, a holster hidden at the right waist, and armor as separate gear. Still missing: the ten pose images, the silhouette test, and the collision overlay.

**B05 · LIMITS**

Now the requirement this film cannot meet. The assignment asks to see the character in two states, and four sound events firing in real play. None of that exists. There is no character, no sound wired to an event, no music, and no mute. So you will not see gameplay here. What you will see is real engine output of the greybox, and the real generated files.

**B06 · TRACE**

The trace starts in the design docs. The concept's audio direction, added on October ninth, says the tablet sounds are short, dry electronic tones with light radio static and squelch, like rugged field electronics. The change brief then names the asset, terminal power on, and its exact event: picking up the tablet, from not looking to one or two hands.

**B07 · TRACE**

The first attempts failed. Version one asked for two confirmation beeps and a rising activation tone. The designer heard something too sharp and explosive, like an electronic transient. Version two rerolled seeds and lengths; none of those satisfied either. So the design changed: one clear beep, layered with short radio static. One more finding: every run used C F G one, so the negative prompts did nothing.

**B08 · TRACE**

Version three is the one that was accepted. The prompt asks for one clear confirmation beep, layered with a brief filtered radio static burst. With the seed on screen, twelve steps, C F G one, and a two point three second length, output zero zero zero four two was accepted with no edits. The repository file is a byte-identical copy. These settings were read back from the metadata Comfy U I embeds in the file itself.

**B09 · LISTEN**

(no narration — listening segment: generated sound files, not in-engine)

**B10 · TRACE**

And the last step of the trace: the in-engine result. There is not one yet. This is the saved scene tree of base dot T S C N. There is no audio player node. The Godot project contains no sound files at all, and project dot godot defines no input actions, so nothing could trigger the beep. The sounds still sit in the design folder as FLAC files, not yet converted to Ogg.

**B11 · CODE**

The second trace has real engine output: the greybox. The designer built the floor and side walls, then asked Claude to finish it from basic shapes. Read the last step and the ramp. Each step rises zero point two metres and runs zero point three. Then a collision box with no mesh, tilted by the matrix entries zero point five five four seven and zero point eight three two one. That is a thirty-three point seven degree slope: exactly rise over run.

**B12 · RESULT**

Here is what those lines do. On the left, a normal render: you only see steps. On the right, the same frame with Godot's collision drawing turned on: the invisible ramp lies across every step edge. A raycast check I ran for this film agrees: the ramp surface meets the first five step edges within a millimetre, and ends at the sixth. A prediction I have not tested: change the step height alone, and the ramp stops matching.

**B13 · CODE**

One more cause and effect: the lighting. The concept asks for dark, cool tones. In the scene file, two omni lights hang at x minus three point five and plus three point five, just under the ceiling, with a pale blue colour, energy one point five, and an eight metre range. The environment behind them is nearly black, with a weak blue-grey ambient light.

**B14 · RESULT**

And the result, rendered by Godot at native four K. A film camera added by my capture script pans across the room. Nothing in the scene moves, because nothing in it can. You can see the two cool pools of light on the ceiling, the test chair against the back wall, and the stairs. It is dark and blue-grey, as the concept asked. Whether a near-black character would read against these walls is still untested.

**B15 · TESTS**

What was tested. A fresh export of the submitted revision imports cleanly, and base dot T S C N runs a hundred and twenty frames with no errors or warnings. The ramp raycast passes. Re-running a sound with the same prompt and seed gave identical decoded audio. These are headless machine checks. No human has played anything, because there is nothing to play, and none of this shows that a sound fires once per event.

**B16 · CREDITS**

Who made what. ChatGPT image generation made the character turnaround, the extra views and the tablet references. A local model, ChenkinNoob X L, made early drafts, all rejected. Stable Audio 3 Small made all the sound. Claude Code built the greybox and the test chair in code. The assignment text says code-drawn art does not meet the generative model requirement; the professor confirmed to the designer that these basic-shape 3D builds count. Both are true, so both are on screen.

**B17 · NEXT**

What is still uncertain. The error sound keeps coming out with tremolo and repeated tones, and the designer does not yet know how to get one clean tone. Nobody knows whether the dark outfit reads against this room. And the once-per-event logic is not written. The next concrete step: convert the three sounds to Ogg, add an audio player, and fire power on when the tablet's state changes, with a log that proves one trigger per press.

**B18 · VERDICT**

Verdict. What is real: a careful design record, a reproducible asset log, three accepted sounds, and a greybox whose stair ramp demonstrably lines up. What is missing is the slice itself: no character, no events, no music, no mute, so this film cannot show play. The judgment, every accept, reject and redesign, was the designer's. The models produced drafts; Claude built shapes and kept the records.

**B19 · HANDOFF**

Your turn. Paste this into Claude. Please use Walker on my Godot project. Read my change brief event-to-sound map and base dot T S C N. Pick one sound event and write the smallest change that plays it on that event, plus a test that logs how many times it fired for one short press, one long press and a held key. Predict the counts before you run it. The prediction is the point: write down the counts first, so the log can prove you wrong. Start with one sound, not four. Liam, in for Bear.

**B20 · OUTRO**

Walker Survival Shooting, Before the Slice. At Nik Bear Brown.
