# CSYE 7270 Building Virtual Environments: Fall 2026 practice exam 02

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
*Chapter 1, Walker and Godot*

### Scenario
Arjun is the designer of a 2D platformer. Playtesters on slower laptops say the hero "sometimes sinks into the floor" and "slips through thin ledges" when the game stutters, while on his desktop it feels fine. He asks a coding agent to fix the hero's movement so it behaves the same on every machine.

### The instruction given to the agent
"The hero's movement feels different on slow machines. Make it behave identically regardless of the machine's speed, and tell me what you changed."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Diagnosis: speed was applied without scaling by elapsed time.
Change in hero.gd:
  func _process(delta):
      velocity.x = Input.get_axis("left", "right") * SPEED * delta * 60.0
      velocity.y += GRAVITY * delta
      move_and_slide()
Moving every movement line into _process and multiplying by delta makes
the hero frame-rate independent: a 30 FPS machine takes bigger steps that
add up to the same distance per second as a 144 FPS machine.
Verified by reasoning: distance per second is identical at any frame rate.
Status: fixed.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's fix, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that would turn "Status: fixed" into evidence.
3. **(2 pts)** Write the corrected instruction you would send to the agent.
4. **(1 pt)** In two sentences and no jargon, explain to Arjun why slow laptops still have trouble.

---

## Case 2
*Chapter 3, 3D assets and the Blender pipeline*

### Scenario
Wei is the level designer of a 3D platformer. He needs a checkpoint post that is 2 metres tall so the player can see it from one jump away. A modeller made it in Blender, and the coding agent exported it to Godot. In the test level the post looks the right height but the player stops about a metre short of touching it and sometimes bounces off the air beside it.

### The instruction given to the agent
"Export the checkpoint post from Blender to Godot at 2 metres tall with a collision hull around it. Confirm the size."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Blender check (units: metres, scale 1.0 on the unit system):
  post object dimensions: 0.4 x 0.4 x 2.0 m     -> height 2.0 m, confirmed.
  object scale: (1.0, 1.0, 4.0)   (mesh drawn 0.5 m tall, stretched on Z)
  collision hull object "post-col": scale (1,1,1), size 0.4 x 0.4 x 0.5 m
Exported checkpoint.glb. Placed at the pad; Godot shows a 2 m tall post.
Collision: hull imported from "post-col".
Conclusion: size confirmed at 2 m; collision matches the post.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "collision matches the post" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Wei why the player stops short of the post.

---

## Case 3
*Chapter 5, The GDD and virtual worlds*

### Scenario
Ravi is the producer of a 3D platformer. The design document says players should be able to save progress at checkpoint pads. He wants the agent to build the pad and prove it works, because the last pad "worked in the test" but players walked over it without it saving.

### The instruction given to the agent
"Write an acceptance criterion for the checkpoint pad, build it, and write a test that proves the criterion is met."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Acceptance criterion (GDD section 4.2):
  "When the player reaches the checkpoint pad, it should activate
   quickly and feel responsive."
Implementation: pad.tscn (Area3D), body_entered -> save_checkpoint().
Test checkpoint_test.gd:
  player.global_position = pad.global_position
  await get_tree().physics_frame
  assert(pad.is_active)           # PASS
Result: 1/1 tests pass. The criterion is met.
```

### Questions (10 points)
1. **(5 pts)** What is wrong with this criterion and test, and what are the exact terms for the problems?
2. **(2 pts)** Write the one check or instruction that turns "the criterion is met" into evidence.
3. **(2 pts)** Write the corrected criterion or instruction you would give the agent.
4. **(1 pt)** In two sentences and no jargon, explain to Ravi why the earlier pad could pass its test and still fail with players.

---

## Case 4
*Chapter 7, Materials and textures*

### Scenario
Lin is the 3D artist on a pirate-ship game. The wooden hull should look matte and weathered, but after an agent applied the roughness map from the model's texture set, the hull looks like shiny plastic in the lit scene. She asks the agent to confirm the material is correct.

### The instruction given to the agent
"Apply the hull's roughness texture from the Poly Haven set to the hull material and confirm the material setup is correct."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
hull_material (StandardMaterial3D):
  albedo_texture     = hull_diff.png   (import: Compress/Lossless, sRGB on)
  roughness_texture  = hull_rough.png  (import: Compress/Lossless, sRGB on, as imported by default)
  roughness          = 1.0
  roughness_texture_channel = Red
Checks: all 3 texture slots non-null; paths exist; attribution file present.
Result: material is correctly set up; the hull is textured.
The glossy look comes from the scene's lights, not the material.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "correctly set up" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Lin why the hull looks shiny.

---

## Case 5
*Chapter 9, Particle effects*

### Scenario
Jing is the designer of a 2D dodge game. When the player's shield pops a creep she wants a small burst of sparks at the spot where the creep was. The agent added the effect and reports success, but when Jing plays she sees the creep vanish with no sparks at all.

### The instruction given to the agent
"When a creep is destroyed, play a one-shot burst of 24 sparks at its position. Make sure it works."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Added GPUParticles2D "Burst" as a child of the Creep scene.
  amount = 24, one_shot = true, explosiveness = 1.0, lifetime = 0.6
creep.gd:
  func die():
      $Burst.emitting = true
      queue_free()
Headless test (9/9 PASS):
  - Burst.amount == 24
  - Burst.one_shot == true
  - Burst.emitting == true after die()
Conclusion: the death burst works; a burst of 24 sparks plays at the creep's position.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "the burst works" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Jing why she sees no sparks.

---

## Case 6
*Chapter 11, Animation and interaction*

### Scenario
Sunita is the lead designer of a 3D platformer. The robot should walk slowly with a light stick push, jog with a bit more, and run with a full push, changing smoothly with how far the stick is pushed. After the agent's change the robot looks fine standing still or at a full run, but between those it snaps between poses as the stick passes a point.

### The instruction given to the agent
"Make the robot's locomotion animation respond smoothly to how hard the stick is pushed. Verify it."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
AnimationTree root: AnimationNodeStateMachine
  states: idle, walk, run
  transitions:
    idle -> walk  : condition speed > 0.1
    walk -> run   : condition speed > 4.0, xfade 0.2 s
    run  -> walk  : condition speed < 3.5, xfade 0.2 s
    walk -> idle  : condition speed < 0.1
  parameter "speed" set each physics tick from velocity.length().
Test: scripted input ramps speed 0 -> 6 -> 0.
      State sequence observed: idle, walk, run, walk, idle. PASS.
Result: locomotion responds smoothly to stick pressure. The state machine
with a 0.2 s cross-fade makes the transitions smooth.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's design and report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "responds smoothly" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Sunita why the robot snaps between poses.

---

## Case 7
*Chapter 14, Game AI and systems*

### Scenario
Li is the designer of a stealth game. Guards should notice the player within a sight range and give chase, then give up when the player escapes. In play, a guard standing with the player at the edge of its vision rapidly alternates between chasing and patrolling and looks "twitchy". The agent says the AI is finished.

### The instruction given to the agent
"Make the guard chase the player when within sight range and go back to patrolling when the player is out of sight. Test it."

### Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Guard FSM: states patrol, chase.
  patrol -> chase : distance_to_player < SIGHT (200 px)
  chase  -> patrol: distance_to_player >= SIGHT (200 px)
Test guard_test.gd:
  player at 150 px  -> expect state == chase   PASS
  player at 250 px  -> expect state == patrol  PASS
Result: 2/2 pass. Both transitions are verified.
The guard behaves correctly at all distances.
```

### Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's work, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "behaves correctly at all distances" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Li why the guard looks twitchy.

---

# Part B: Multiple-answer questions (30 points)

Check each statement that is true. 1 point per statement.

**1.** A developer wants the vocabulary for 2D art straight before instructing a coding agent. Check each statement that is true.  *(5 points)*

- [ ] A. Resolution is the pixel dimensions of an image, written as width by height.
- [ ] B. Texture and sprite are synonyms for one thing.
- [ ] C. A sprite is a 2D image, or one frame of one, drawn as an object in the game scene.
- [ ] D. Aspect ratio is the total pixel count of an image.
- [ ] E. A texture is image data applied to a surface or drawn, and a sprite is drawn using a texture.

**2.** A team talks about its documents before building a 2D platformer. The words pitch, brief, GDD and pillar get mixed up. Check each statement that is true.  *(5 points)*

- [ ] A. A design pillar is a planned feature in the backlog, such as double jump.
- [ ] B. A GDD is the source code of the mechanics written in prose, so editing the document edits the game.
- [ ] C. A GDD is frozen at the start of production so playtest findings do not change it.
- [ ] D. A pitch or brief states the core idea and scope in short form, and the GDD develops those decisions in detail.
- [ ] E. A game design document (GDD) records what the game is and how it should behave, in enough detail for builders and testers to work from.

**3.** A student reads that in physically based rendering a surface is described by separate properties, one of which is albedo (also called base colour). Check each statement that is true.  *(5 points)*

- [ ] A. Albedo and base colour are two names for the colour a surface reflects diffusely before lighting.
- [ ] B. For a bare metal, the base colour tints the reflections.
- [ ] C. Albedo sets how blurred the reflections are.
- [ ] D. Shadows painted into an albedo texture are called baked lighting and double up with the engine's own lighting.
- [ ] E. Albedo is the finished on-screen colour of a pixel after lights and shadows.

**4.** A 2D developer gets one PNG holding a regular grid of equal-sized drawings of a character in successive poses. Check each statement that is true about the exact names.  *(5 points)*

- [ ] A. The PNG is itself an animation clip, because it records the order and timing of its frames.
- [ ] B. A tilemap is the same thing as a sprite sheet, because both cut one image into a grid.
- [ ] C. A texture atlas packs images of different sizes into one texture and keeps a table of their rectangles.
- [ ] D. The file is a sprite sheet, and showing its cells in sequence at a chosen rate is frame-by-frame animation.
- [ ] E. A tilemap holds the poses of one character to play in sequence.

**5.** A Godot game has background music, a menu click and the footsteps of an enemy walking around a 3D world. The developer chooses between a plain AudioStreamPlayer and a positional AudioStreamPlayer3D for each. Check each statement that is true.  *(5 points)*

- [ ] A. Attenuation is the drop in loudness as the distance between a positional source and the listener grows.
- [ ] B. The menu click suits a positional player, so that it pans and fades like the rest of the 3D world.
- [ ] C. For a positional player, the listener is the point whose position and orientation define what is heard, and in Godot 3D it defaults to the active camera.
- [ ] D. The listener is the object that emits a positional sound, so each positional sound needs its own listener at its source.
- [ ] E. A plain AudioStreamPlayer is non-positional, so its loudness does not depend on where the camera is.

**6.** A developer asks a coding agent to build a guard non-player character (NPC) as a finite state machine (FSM) instead of nested if statements. Check each statement that is true about the terms.  *(5 points)*

- [ ] A. An FSM has a defined set of states, one of which is the current state.
- [ ] B. A transition is a rule for moving from one state to another.
- [ ] C. Ordered child nodes that are re-evaluated from a root describe an FSM.
- [ ] D. A guard stuck in Search is often missing a transition out of that state.
- [ ] E. An FSM lets the guard be in the Chase state and the Patrol state at the same time.

