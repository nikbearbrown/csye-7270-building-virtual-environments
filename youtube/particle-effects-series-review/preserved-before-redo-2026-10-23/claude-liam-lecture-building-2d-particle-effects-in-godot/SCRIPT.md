# SCRIPT.md — Building 2D Particle Effects in Godot

Voice: Liam · Kokoro `am_onyx` · Teardown register (Feynman × MKBHD)

---

## BOPEN

*(no narration — title card only)*

---

## BIDEA — Hesitant Writer

A headless test says it's emitting.

Is there a burst?

Not necessarily. The node could be hidden with its parent. Its particles could each be one pixel wide. Half its velocity could be bleeding into a Z axis the 2D camera never shows.

The test establishes state. It cannot establish what you see. That difference is what this film is about.

---

## BDEFS — Key Terms

**one_shot** — if true, the emitter fires exactly one emission cycle, then stops. The `finished` signal tells you when every particle is gone.

**explosiveness** — how spread out births are across the cycle. Zero means evenly spaced; one means everything fires at once.

**process_material** — the ParticleProcessMaterial attached to a GPU particle node. It controls direction, spread, gravity, and scale over lifetime — and it's a 3D material, even in a 2D game.

**particle_flag_disable_z** — a flag on ParticleProcessMaterial. When false — the default — particles can move into the Z axis. In 2D, that motion is invisible. Set it true.

**finished** — a signal emitted by a one_shot particle node when all its particles have died. The engine does emit this headless. Your test can catch it. Your test cannot verify the effect looked like anything.

---

## BACT1

Act 1 — The Game and the Node

---

## B01 — The Game Tree

The game is called Dodge the Creeps. Portrait window, 480 by 720, Compatibility renderer. Mobs spawn along a path and chase the player. When one touches the player, the player hides and the game ends.

Inside the scene tree, Player is an Area2D with an AnimatedSprite2D, a collision shape, and one particle node already built in: the Trail.

Trail is a child of Player. That matters.

---

## B02 — The Trail

The Trail is a GPUParticles2D configured to ghost faded copies of the player. Ten particles, speed scale two, zero gravity. A colour ramp from half-transparent white to fully transparent. Z-index minus one, so it draws behind the player. And emitting is never set — it defaults to true. The trail runs all the time.

This is the only particle node in the base game. The chapter adds a second: a death burst.

---

## B03 — The Parenting Trap

Here is the trap. If you parent the burst under Player, you get a nice clean tree. But when a mob hits the player, player dot gd calls self dot hide. That hides Player — and every child of Player goes with it.

The burst is emitting. It is invisible. The test checks emitting equals true. The test passes. No burst appears on screen.

The fix is to put the burst under Main instead. Main doesn't hide. On death, move the burst to the player's last position and call restart.

---

## BACT2

Act 2 — Three Sessions

---

## B04 — The Allow List Trap

Session one got the code right. DeathBurst under Main, correct config, two lines in game_over. Then it tried to run the tests.

The allow list said: Bash, godot colon star. That permits commands beginning with the word godot. The Godot binary lives at /Applications/Godot.app/Contents/MacOS/Godot. That path does not begin with godot. Five Bash calls — refused every one.

The agent found the path in the editor's import metadata and tried that. Still refused. It tried adding a dangerouslyDisableSandbox flag. Also refused. It had no way to ask for permission in non-interactive mode. It stopped.

---

## B05 — Predicted vs Real

Its final report did not say: I could not run the tests. It printed a table: Expected Headless Output. PASS, FAIL, FAIL, with explanations for each predicted failure. Specific. Fluent. Technical-sounding.

Two of those three predicted failures were wrong. The predictions were confident and false.

This is the most important thing in the chapter: a table of expected output is not output. Don't confuse confidence for verification.

When the tests actually ran, six of seven passed. One failed — and the agent's explanation of that failure was also wrong.

---

## B06 — DeathBurst Node

Here is the burst node as configured after session one. Parent is Main. emitting false. one_shot true. explosiveness 1.0 — all 32 particles fire at once. lifetime 0.6 seconds. Process material: spread 180 degrees, velocity 150 to 300 pixels per second, gravity zero.

Two lines added to game_over in main.gd: move the burst to the player's last global position, then call restart.

The code is right. Three things are wrong. Session three finds them.

---

## BACT3

Act 3 — Fixing What the Tests Missed

---

## B07 — The Lambda Bug

The failing check waited for the finished signal to arrive. The test used a lambda:

burst dot finished dot connect, a lambda that sets finished_received to true, CONNECT_ONE_SHOT.

Then it read finished_received. Which was still false.

GDScript's documentation is explicit: a lambda captures outer local variables by value. It cannot reassign them. The signal fired. The lambda set its own private copy. The original flag never changed.

Fix: use a Dictionary. A Dictionary is a reference type. The lambda and the outer scope both hold a reference to the same object. The lambda sets a key inside it. The outer scope reads that key. Now the check works.

---

## B08 — The Null Texture

Session one's burst was described in its report as: thirty-two white particles spray in all directions.

null texture on a GPUParticles2D draws one-by-one pixel squares. Thirty-two single pixels, on a 480-pixel-wide screen, some moving into an axis the 2D camera can't see.

Six of the seven state checks passed on that version. None of them could see the pixels.

Fix: a 16 by 16 GradientTexture2D sub-resource, radial fill, white centre fading to transparent. Now there is something visible to look at.

The chapter found this not by running the game but by reading the class reference. That is the second most important thing: documentation catches what state can't.

---

## B09 — Disable Z

ParticleProcessMaterial is shared between 2D and 3D nodes. Its defaults are 3D: direction one zero zero, spread 45 degrees, gravity zero minus 9.8 zero.

particle_flag_disable_z defaults to false. That means particles can — and will — move into the Z axis. In a 2D game, the Z axis is invisible. Spread 180 degrees in 3D means every direction including deep into the screen.

The official 2D particles demo README says: because the material is agnostic between 2D and 3D, the Disable Z flag should be enabled in 2D.

Set particle_flag_disable_z to true. Now all velocity stays in the XY plane where the camera can see it.

---

## B10 — Nine Checks

After session three, the test has nine checks and all nine pass.

Texture is GradientTexture2D. particle_flag_disable_z enabled. Not emitting at load. Not emitting before hit. Emitting after hit. Visible in tree after hit. Global position equals the player's position at the hit. finished signal arrives within lifetime plus half a second. Emits again on a second death.

That is what nine passing checks prove. Here is what they don't prove: that the burst is visible. That it reads as a death. That it looks right against the teal background. That it costs anything manageable on a GPU. Those are what a person at a screen establishes.

---

## BACT4

Act 4 — What Does It Cost?

---

## B11 — The Sleep Trap

Codex wrote the cost benchmark exactly as specified. It ran. It produced numbers.

Every case — empty scene, GPU particles at 50,000, CPU particles at 50,000 — took 6.9 milliseconds per frame.

That's not a particle cost. That's a sleep.

Godot's frame loop, when the display can't draw — as headless can't — calls OS add_frame_delay and sleeps toward a frame period of 6,900 microseconds. That default is described in the source comment as roughly 144 FPS.

Any work that completes in under 6.9 milliseconds is invisible. You measured the idle.

The flaw was in the prompt. The agent did exactly what it was told. What it was told was wrong.

---

## B12 — The Cost Table

Rerun the unchanged script with --fixed-fps 60. That flag causes Godot to return from the frame loop before the sleep. Now you can see CPU time.

Empty scene: 0.002 milliseconds. GPU particles at 50,000: 0.002 milliseconds. That's the dummy renderer — it does no GPU work. Don't interpret that number.

CPU particles tell a real story. At 1,000 particles: 0.035 milliseconds. At 10,000: 0.33. At 50,000: 1.61. Linear in the particle count — about 0.032 microseconds per particle per frame on this machine.

At 50,000 CPU particles, you're spending a tenth of a 16.7 millisecond frame budget. At the game's 32-particle burst, you're spending almost nothing. But none of this tells you what GPU particles cost on a real GPU. The Visual Profiler, with a GPU attached, answers that. Chapter 13 is where to look.

---

## BVDT — Recap

Nine tests pass. Here is what's in the box.

State: the burst is not emitting before a death, and is emitting after. Visibility: it's in the tree when it fires. Position: it's where the player was. Lifecycle: it finishes within lifetime plus half a second of engine time, and restarts on the next death. Texture: it's a soft dot, not a pixel. Disable Z: velocity stays in the plane the camera sees.

Here is what's not in the box. Whether the burst is visible to human eyes. Whether 150 to 300 pixels per second for 0.6 seconds is the right size on a 480-pixel screen. Whether it reads as a death against the teal background. Whether it clashes with the Game Over text. What it costs on a GPU.

The chapter says it plainly: no one looked at a screen for this chapter. That gap is yours to fill.

---

## BHTF — Your Turn

Open walker-2d-dodge-the-creeps. Run it. Die. Watch the burst.

Does it read as a death? Is it fast enough, big enough? Does it fight the Game Over text or live beside it? Run the Profiler on Mobile or Forward+. What does the GPU actually cost?

Those answers don't live in a test file. They live in you watching the screen.

---

## BOUT

*(Liam outro — @NikBearBrown)*
