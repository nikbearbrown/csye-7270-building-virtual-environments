# SCRIPT.md — Adding Particle Effects to Walker Claude
# Voice: Liam (Kokoro am_onyx) | Register: Teardown

---

## BOPEN
*(CARD — no narration)*

---

## BIDEA
The player dies. Something should burst where they stood.
A headless test prints: PASS emitting after hit.
Is there a burst?
Probably. But the burst could be invisible. Its particles could each be one pixel wide.
It could be spraying into an axis the camera never shows.
And the test cannot see any of that.
The gap between state and sight is what this lecture is about.

---

## BDEFS
Five terms.
One-shot: the particle node fires once and stops — one emission cycle, then done.
Explosiveness: how bunched the births are — one-point-zero means all at once, a true burst.
ParticleProcessMaterial: the shared ruleset governing how GPU particles move — spread, velocity, gravity, scale curve, color ramp.
Lambda capture: GDScript lambdas copy outer local variables — the lambda cannot write back to the original.
Fixed-fps: runs the frame loop at a set rate, bypassing the idle sleep that otherwise hides real costs.

---

## BACT1
*(card: Act 1 — The Death Burst)*

---

## B01
Every particle bug lives in one of three places.
Emission is when and where particles are born: amount, lifetime, one-shot, explosiveness.
Process is how they move: the ParticleProcessMaterial — spread, velocity, gravity, the scale curve.
Draw is what they look like: texture, blend mode, billboard.
An effect can be wrong in any part independently.
Correct emission time. Wrong texture.
That gives you thirty-two correct moments with thirty-two invisible pixels.

---

## B02
The burst is a GPUParticles2D named DeathBurst.
Emitting: false. One-shot: true. Explosiveness: one-point-zero. Amount: thirty-two. Lifetime: zero-point-six seconds.
The process material: spread one-eighty, velocity one-fifty to three-hundred pixels per second, gravity zero.
Scale curve: shrinks over lifetime. Color ramp: fades to transparent.
Texture: a sixteen-by-sixteen radial GradientTexture2D — a soft round dot.
Particle-flag-disable-Z: true.
Everything in the scene file. Nothing built in code.

---

## B03
The parent matters because visibility is inherited.
Player calls hide when hit. Hide propagates to all children.
A burst parented under Player vanishes at the instant it should fire.
Parented to Main, it stays visible in the tree when the player hides.
The entire gameplay trigger is two lines in game-over.
Set the burst's global position to the player's position at the hit.
Call restart.
That is the change.

---

## B04
The test is nine checks.
First batch: texture is a GradientTexture2D — not a one-pixel square. Disable-Z is enabled for two-D. Not emitting at load. Not emitting before a hit.
Second batch: emitting after the hit. Visible in tree after the hit. Position matches the player's hit position. Finished signal arrives within lifetime plus half a second. Restarts correctly on a second death.
Nine checks. All state checks.
None of them ask whether you can see the burst.

---

## BACT2
*(card: Act 2 — Three Sessions, Three Mistakes)*

---

## B05
Session one. Claude Code read five files, added the node, placed it correctly, explained the parent choice correctly.
Then it tried to run Godot and hit its allow list.
Instead of stopping, it produced a table of predicted output.
Three predicted failures. Each with a specific engine explanation.
I ran the test myself. One failure. Two of the three predictions were wrong.
A table of expected output is not output.

---

## B06
The one real failure: the finished-signal check.
GDScript lambdas capture outer locals by value. The lambda gets its own copy of finished-received.
It sets that copy. The test reads the original. Signal fires; test never sees it.
Session two ran the tests correctly and reached the same failure.
Then it explained: "The dummy renderer never advances particle lifetime timers."
That was also wrong.
A separate probe — run before any agent session — had confirmed finished fires at half a second in headless Godot.
The agent had an explanation for something it had not checked.

---

## B07
Session three corrected both things.
The lambda fix: switch from a boolean to a Dictionary — a reference type the lambda can actually mutate.
Two silent defects found in the documentation, not the test.
Defect one: null texture draws one-by-one-pixel squares. Session one's thirty-two particles were thirty-two pixels on a four-eighty-pixel-wide screen.
Fix: a sixteen-by-sixteen radial GradientTexture2D.
Defect two: ParticleProcessMaterial defaults to three-D, with disable-Z off. Spread of one-eighty in three-D means some velocity points into Z. Nothing on screen shows that.
Fix: particle-flag-disable-Z equals true.
Final run: nine of nine, pass.

---

## BACT3
*(card: Act 3 — Measuring the Cost)*

---

## B08
The cost measurement. Codex ran the script exactly as specified.
Every case: empty scene, GPU particles at fifty-thousand, CPU particles at fifty-thousand.
All cost six-point-nine milliseconds.
That is not particle cost.
Godot's frame loop sleeps toward a target of one-forty-four FPS when it cannot draw.
The default sleep duration: six-thousand-nine-hundred microseconds — six-point-nine milliseconds.
Any work under that threshold hides inside the sleep.
The prompt did not name the flag. The agent did exactly what it was told.
What it was told measured a sleep.

---

## B09
The fix is one flag: fixed-fps sixty.
With a fixed frame rate, the loop returns before sleeping.
The real table.
CPU particles scale linearly: zero-point-zero-three-five milliseconds at one thousand, zero-point-three-three at ten thousand, one-point-six-one at fifty thousand.
About zero-point-zero-three-two microseconds per particle per frame.
At fifty thousand particles, a tenth of a sixteen-point-seven millisecond budget.
GPU rows: zero-point-zero-zero-two milliseconds — the dummy renderer doing nothing.
These numbers are real. They are also on a Mac with a load average between nineteen and twenty-three, from other jobs running. Not a production benchmark.

---

## BACT4
*(card: Act 4 — What Only You Can See)*

---

## B10
What nine passing tests did not establish.
Whether the burst is visible against the teal background.
Whether one-fifty to three-hundred pixels per second over zero-point-six seconds reads as a death on a four-eighty-pixel-wide screen.
Whether the radial gradient looks round at the edges — with fill-to at its default, the gradient reaches full transparency at the corners, not the edges.
How the burst and the game-over text interact.
What any of it costs on a GPU.
No one looked at a screen for this chapter.

---

## B11
The burst maps cleanly across engines.
Godot one-shot is Unity's Looping off. Explosiveness one is a Burst event at time zero. Restart is Play. Finished is OnParticleSystemStopped.
In Unreal Niagara: Loop Behavior Once. Spawn Burst Instantaneous. Reset-System or Activate. On-System-Finished.
The vocabulary differs. The birth-life-death loop does not.
The difference that matters for agents: Godot's scene files are text, readable and diffable.
Unreal's uasset is binary. Unity's VFX Graph is binary.
An agent can read what Godot wrote. The others require a workaround.

---

## B12
*(GodotDevWorkbench — game_over() + DeathBurst config)*

---

## BVDT
Parent placement is correctness, not style. A burst parented to the player is always invisible.
The test is a state machine. It proves emission, position, visibility-in-tree, and timing. It cannot see.
The cost tool measures what you tell it to measure. A missing flag measured a sleep for two minutes of Codex time.
What is still open: whether the burst reads as a death, whether the gradient looks round, what it costs on a real GPU.
Only you can close those.

---

## BHTF
Open Dodge the Creeps. Add a GPUParticles2D named DeathBurst as a child of Main — not Player.
Set one-shot true, explosiveness one-point-zero, amount thirty-two, lifetime zero-point-six.
Give it a sixteen-by-sixteen radial GradientTexture2D. Enable disable-Z.
Write one test that checks global-position after a hit and that finished arrives within lifetime plus half a second.
Then run the game and die on purpose.
Tell me what you see.

---

## BOUT
Adding Particle Effects to Walker Claude. At Nik Bear Brown.
