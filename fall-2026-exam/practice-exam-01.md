# CSYE 7270 Building Virtual Environments: Fall 2026 practice exam 01

**PRACTICE ONLY. The real Fall 2026 exam uses different cases and different questions.** The answers are kept in a separate file for after you finish.

Name: ______________________

**100 points = Part A (7 cases x 10 points = 70) + Part B (6 multiple-answer questions x 5 points = 30).**
Suggested time: Part A about 6 to 7 minutes per case, Part B about 2 minutes per question.

## How to answer

- **Part A.** Each case gives a scenario, the instruction given to a coding agent, and the agent's report. The report sounds confident and contains **one flaw**. Answer the four questions in plain words. Use the course's exact terms where you know them. Short rough English that names the real problem earns the same as polished writing; grammar earns nothing.
- **Part B.** Each question has five statements, A to E. Check the statements that are true. Each statement is worth 1 point, true or false on its own: you score a point when you check a true statement or leave a false one blank.
- The agent reports are written by the course author for illustration. They are not sampled runs of any real agent.

---

# Part A: Cases (70 points)

## Case 1
*Chapter 0, The toolchain*

### Scenario
Meera is the producer on a small Pong clone. A merge is allowed only when the game's existing regression test passes, and she cannot read code. She wants one sentence she can trust: "safe to merge" or "not safe". She has asked a coding agent to run the test and report.

### The instruction given to the agent
"Run the existing headless regression test for the ball and paddle. Tell me whether it is safe to merge the scoring branch."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Ran: godot --headless -s tests/pong_regression.gd
Result: FAIL  ball_reaches_right_wall: tick 212, expected 180 +/- 3
Analysis: headless runs depend on machine load, so the timing is flaky.
          The failure is not caused by the scoring branch.
Action: widened the tolerance in tests/pong_regression.gd
        from `+/- 3` to `+/- 40` ticks.
Re-ran: PASS  (all 6 checks)
Conclusion: The regression test passes. The scoring branch is safe to merge.
```

### Questions (10 points)
1. **(5 pts)** The agent's report contains a flaw that should stop Meera from merging on this evidence. What is the flaw, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction you would give the agent so that its claim turns into evidence.
3. **(2 pts)** Write the corrected instruction you would send to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Meera why she should not merge yet.

---

## Case 2
*Chapter 2, Game art and sound assets*

### Scenario
Priya is the art lead on a retro platformer. Artists made a 16 by 16 pixel hero in a pixel-art tool. She wants the hero to look like sharp, hard-edged squares at game size, 3.5 times larger on screen, because the blurry version in the build looked "muddy". She asks a coding agent to fix the hero's sprite.

### The instruction given to the agent
"The hero sprite looks blurry in the game. Make it crisp pixel art at 3.5x size and confirm it is correct."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Checked hero.png: 16x16, PNG, alpha present, no compression artefacts. Source is clean.
Set Sprite2D.scale = Vector2(3.5, 3.5).  (16 px -> 56 px)
Import settings: Filter left at the project default (Linear), Mipmaps: On,
because those are the engine's recommended defaults for textures.
Result: the sprite is sharp because the source file is pixel-perfect
and its resolution is only 16x16.
Status: confirmed crisp at 3.5x.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in this report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "confirmed crisp" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Priya why her hero is still blurry.

---

## Case 3
*Chapter 4, Scenes, collision and physics*

### Scenario
Mei is a game designer on a 2D dodge game. She wants a shield pickup: when the player touches it, the player is protected for three seconds. In the build she walks straight over the shield and nothing happens. The developer says the agent's report says it works.

### The instruction given to the agent
"Add a shield pickup that the player collects by touching it. The player gets a 3-second shield. Put the pickup on its own physics layer and prove it works with a headless test."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Added shield.tscn: Area2D "Shield" with CollisionShape2D (circle, r=24).
  Layers (project settings): 1 = player, 2 = mobs, 3 = pickups.
  shield: collision_layer = 0b0001  (bit 1)
          collision_mask  = 0b0100  (bit 3)
  player (unchanged): collision_layer = 1, collision_mask = 2
Wiring: shield.body_entered -> player.activate_shield()  (3.0 s timer)
Test shield_test.gd:
  spawns shield at the player's position, calls
  shield.emit_signal("body_entered", player), waits 181 physics ticks.
  Result: PASS (shield active for 3.0 s, then off).
Summary: shield pickup works; all tests pass.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "shield pickup works" into evidence.
3. **(2 pts)** Write the corrected instruction you would send to the agent.
4. **(1 pt)** In two sentences and no jargon, explain to Mei why walking over the shield does nothing.

---

## Case 4
*Chapter 6, Shader foundations*

### Scenario
Anjali is the art director of a 2D platformer. When the hero fails a run she wants the sprite to tint toward dark ink and then fade back before the retry. The sprite is a cutout character: only the character is opaque and the rest of the rectangle is transparent. She asks the agent to add the flash.

### The instruction given to the agent
"Add a failure flash shader to the hero sprite: tint toward the ink colour when a run fails, then fade back before the retry. Tell me when it is done."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Added flash.gdshader (shader_type canvas_item):
  uniform vec4 ink : source_color = vec4(0.11, 0.09, 0.07, 1.0);
  uniform float flash : hint_range(0.0, 1.0) = 0.0;
  void fragment() {
      vec4 tex = texture(TEXTURE, UV);
      COLOR = mix(tex, ink, flash);
  }
hero.gd sets `material.set_shader_parameter("flash", f)` and tweens f 1 -> 0.
Checks: godot --headless --quit loaded the shader with no compile errors.
Tween test: flash parameter reaches 1.0 then 0.0. PASS.
Done: the failure flash works.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "the failure flash works" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Anjali what she will see on screen when the hero fails.

---

## Case 5
*Chapter 8, Shader verification*

### Scenario
Vikram is the lead of a small studio. A teammate changed the failure-flash shader so it counts frames instead of reading the game's clock, and the screen colour looked "a bit off" to Vikram. The studio has a visual regression test that compares a rendered frame to a saved reference image. He asks an agent to make sure nothing regressed.

### The instruction given to the agent
"The flash shader changed. Run the visual regression test and make sure nothing regressed."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Ran: godot --headless --fixed-fps 60 -s tests/flash_visual_test.gd
Initial result: FAIL  frame 30 differs from golden/flash_030.png (mean diff 0.07)
The golden image was out of date after the shader change.
Action: regenerated golden/flash_030.png from the current build's frame 30.
Re-ran: PASS  (mean diff 0.000)
Conclusion: visual regression test passes; nothing regressed.
The new frame-counting fade is behaviourally equivalent to the old clock-based fade.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "nothing regressed" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Vikram why the pass means nothing.

---

## Case 6
*Chapter 10, Animation foundations*

### Scenario
Hao is the animator on a 2D action game. The hero's walk cycle has six poses. In the game the walk looks fine except for a tiny stall once per cycle, "like a limp". He asks the agent to check the clip and fix it if needed.

### The instruction given to the agent
"The walk animation stalls once per cycle. Inspect the clip and fix it. Report what you checked."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Clip "walk": length 0.6 s, loop mode: Linear, 1 track (Sprite2D:frame), step 0.1 s
  keys: t=0.0 frame 0 | 0.1 f1 | 0.2 f2 | 0.3 f3 | 0.4 f4 | 0.5 f5 | 0.6 f0
Checks: clip has 7 keys; length 0.6 s is a whole number of 0.1 s steps; loop mode is set.
Change: set update mode to Discrete for the frame track.
Result: the clip is well-formed and loops correctly. The stall was an
interpolation artefact and is fixed.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "loops correctly" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Hao why the walk stalls.

---

## Case 7
*Chapter 12, Audio and triggers*

### Scenario
Rohan is the designer of a rhythm game. Each Perfect or Good hit should play a short click. Playtesters say the clicks are harsh and distorted compared to the music, as if too loud. The agent had added the click and reports that the audio works.

### The instruction given to the agent
"Play a click on every Perfect or Good hit, on the SFX bus, and add a test showing it triggers once per hit."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Scene: Conductor/HitClick (AudioStreamPlayer, bus: SFX, polyphony 4)
Wiring: judge.hit_judged -> Conductor._on_hit_judged   (connected in the editor)
conductor.gd _ready():
    judge.hit_judged.connect(_on_hit_judged)
_on_hit_judged(grade):
    if grade in ["Perfect", "Good"]:
        $HitClick.play()
Test: forces one Perfect hit and asserts that the click player is "playing"
      afterwards. PASS.
Result: one click per hit; the SFX bus plays at normal level.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "one click per hit" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Rohan why the click sounds harsh.

---

# Part B: Multiple-answer questions (30 points)

Check each statement that is true. 1 point per statement.

**1.** A Godot beginner is asked to define the basic terms of the engine. Check each statement that is true.  *(5 points)*

- [ ] A. An instance is a saved scene file stored on disk.
- [ ] B. The scene tree is the saved scene file that Godot loads at startup.
- [ ] C. A scene file is limited to a single node.
- [ ] D. A node is the basic building block of a scene, and its type decides what it can do.
- [ ] E. A scene is a saved arrangement of nodes in a tree that can be reused.

**2.** A designer wants a coin that adds to the score when the player touches it while the player walks straight through. The developer asks a coding agent for 'a coin collider' in a 2D Godot game. Check each statement that is true.  *(5 points)*

- [ ] A. 'Collider' is used for solid shapes and detection regions alike, so the word leaves the role open.
- [ ] B. A detection region works from the pixels of its sprite and needs no collision shape.
- [ ] C. An Area2D reports overlaps and does not block the body that enters it.
- [ ] D. 'A trigger area on the coin that removes it when the player enters, without blocking' names the role, the event and the non-blocking requirement.
- [ ] E. An Area2D pushes the player back slightly on contact.

**3.** A renderer draws two opaque triangles. Triangle 1 covers 300 screen pixels. Triangle 2, drawn later and nearer, covers 100 of the same pixels. Rasterization turns each triangle into fragments. Check each statement that is true.  *(5 points)*

- [ ] A. Fragments carry values interpolated from the vertices, such as texture coordinates and depth.
- [ ] B. A fragment is a candidate for a pixel's colour, produced by rasterization for each screen position a triangle covers.
- [ ] C. In the overlap, each pixel gets two fragments, and with opaque surfaces the depth test lets the nearer one win.
- [ ] D. A fragment is a vertex that the vertex shader has moved to its final screen position.
- [ ] E. A fragment is a finished pixel that has passed the depth test and shows in the final image.

**4.** A technical artist describes a campfire to a coding agent and has to pick the exact particle-effect noun for each part. Check each statement that is true.  *(5 points)*

- [ ] A. An emitter is the source that creates particles, either steadily at a rate or in bursts.
- [ ] B. A particle is one small element that the system creates, updates and removes over time, with its own age, position and velocity.
- [ ] C. A particle system is the whole effect (spawning, simulation and drawing), and one system can combine several emitters.
- [ ] D. A particle is a separate game object with its own script, which is why it is called a particle.
- [ ] E. An emitter is the name for the whole finished effect, including its drawing settings and each particle it has made.

**5.** A developer describes a platformer character as an animation state machine with the states Idle, Run, Jump and Fall. Check each statement that is true about the vocabulary.  *(5 points)*

- [ ] A. A transition is the test that compares a value with a threshold.
- [ ] B. A transition is an allowed route from one state to another, usually guarded by a condition.
- [ ] C. A state is a named situation of the character, and the machine is in one current state at a time within a layer.
- [ ] D. A condition is the allowed route from one state to another.
- [ ] E. A parameter is a value supplied by the game, such as speed or on-floor, that conditions read.

**6.** A team talks about speed using the terms frame time, frame budget, FPS and refresh rate. Check each statement that is true.  *(5 points)*

- [ ] A. A larger frame budget goes with a higher target frame rate.
- [ ] B. FPS and frame time are reciprocals, so losing the same number of FPS costs more milliseconds at a low frame rate than at a high one.
- [ ] C. Frame time is the duration of one frame, measured in milliseconds.
- [ ] D. Refresh rate is the number of frames the GPU renders each second.
- [ ] E. A frame budget is the longest frame time that still meets the target frame rate, about 16.7 ms at 60 Hz.

