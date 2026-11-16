# SCRIPT — What Is a Particle System?

Narrator: Liam, in for Bear. Voice: Kokoro am_onyx. Register: Teardown.  
All narration rewritten from source prose into the ear-first register.

---

## BOPEN
> C S Y E seventy-two seventy, Building Virtual Environments. What Is a Particle System? Learn how one rule repeated thousands of times makes smoke, fire, and sparks that respond to your game.

---

## BIDEA
> Hallo. This is Liam, in for Bear. You open Godot's particle system and find seven hundred checkboxes. You start clicking and hoping.

*[Writer corrects to:]*  
> You start running one loop.

> A particle is one short-lived dot. The loop is: born, move, change, die. When you understand that loop, the checkboxes become obvious choices.

---

## BDEFS
> Particle. One short-lived simulation point — it has a position, a velocity, and an age, and when its age exceeds its lifetime, it's gone.  
> Emitter. The source that spawns particles — it decides where and when new ones are born.  
> Lifetime. How long a single particle lives, measured in seconds.  
> Velocity. Rate of position change — direction and speed together.  
> Emission cycle. One complete pass through the emitter's particle budget — its length equals the particle lifetime.

---

## ACT I — One Moving Element

### B01 — The Loop Has a Name (Manim: Reeves credit card)
> In 1983, William Reeves described what he called "fuzzy objects" — fire and smoke in the Genesis sequence from Star Trek Two. His idea: an effect is a cloud of points that are born, that move and change, and that die. Every game engine you'll ever use runs exactly that loop.

### B02 — Position, Velocity, Acceleration (Manim: three labeled arrows on a dot)
> Start with one dot. It has a position — where it is. It has a velocity — how fast it's moving and in which direction. It can have acceleration — what's changing the velocity. These are three different jobs, and they each play a role in how the dot moves.

### B03 — The Update Step (Manim: position += velocity × delta animation)
> Each frame, the velocity changes the position. Acceleration changes the velocity. In Godot, we multiply by delta — the time since the last frame — so the motion is the same speed on a slow machine and a fast one. One step. Done each frame.

### B04 — One Dot Moving (Manim: dot traces arc with velocity/position labels tracking)
> Here's a dot starting at the bottom. Its velocity points up and slightly right. Each frame, delta time advances it. When gravity acts as acceleration pointing down, the dot curves. We're not drawing smoke yet. We're understanding the piece that smoke is made of.

---

## ACT II — Birth, Life and Removal

### B05 — Give It a Lifetime (Manim: age bar fills beneath the dot; dot fades then vanishes)
> Now give the dot an age. It starts at zero. Each frame, age increases by delta. When age exceeds lifetime — say one second — the dot is removed. While it lives, its opacity can track its normalized age: young and opaque, old and fading.

### B06 — A Collection of Dots (Manim: emitter spawns 8-10 dots at intervals; they fan out and fade)
> Spawn several. Each has its own age and velocity, with a little random variation. Now you have a small shower of points — born, traveling, fading, gone. This already looks like something: a brief burst, or a faint rain.

### B07 — The Population Question (Manim: counter appears; 20/sec × 2sec → ~40 alive)
> At twenty births per second with a two-second lifetime, after warm-up you tend toward about forty particles alive at once. That's an illustrative prediction — change either number and predict the new population. This is the planning tool. It's not a benchmark.

### B08 — What Happens Without Removal (Manim: counter climbs unbounded; dots pile up)
> Remove the cleanup step. Every dot born stays forever. The count climbs without bound. The simulation bogs down. Returning cleanup lets the population settle. This is not a bug we're fixing — it's the lesson: a continuous effect stays alive while its individual particles expire. Cleanup is load-bearing.

---

## ACT III — One Emitter, Many Variations

### B09 — Move the Emitter (Manim: emitter dot moves left then right; particles trail from it)
> Move the emitter. The particles still carry their original velocity — they don't follow the source. They were born there, and they go where their velocity sends them.

### B10 — Vary the Launch (Manim: narrow cone vs wide spread comparison side by side)
> Control the spread. A tight angle makes a jet. A wide spread makes a burst. Add random variation to the initial speed and the dot size. Now a handful of rules produces a cloud that looks organic. The key word is controlled: randomize everything and you lose the readable intention.

### B11 — Add a Force (Manim: wind vector arrow; particles bend together)
> A shared force — say, wind — affects every particle. All the dots bend in the same direction. This is how gravity works too: one rule applied to every particle, every frame. The force is part of the process, not the emission.

### B12 — Stream Versus Burst (Manim: side-by-side; left = continuous, right = explosiveness=1)
> Two modes. Spread births evenly across the lifetime and you get a continuous stream. Emit all of them at once — an explosiveness of one — and you get an instantaneous burst. Same parameters, different birth timing. That single knob is the difference between smoke and an explosion.

---

## ACT IV — From Rules to Godot's Nodes

### B13 — Three Separable Parts (Manim: Emission / Process / Draw table animating in)
> Godot formalizes the loop into three parts. Emission: how many particles are born, when, and where — set on the particle node itself. Process: how each particle moves and changes over its life — set on a material or shader. Draw: what each particle looks like — a texture, a mesh, and a material on top of that. An effect can be wrong in any one part independently.

### B14 — Four Node Types (GodotDevWorkbench: node type comparison side by side)
> Godot gives you four nodes: G P U Particles 2D and 3D, and C P U Particles 2D and 3D. G P U nodes hand simulation to the graphics card and support sub-emitters, trails, and particle shaders. C P U nodes work on more hardware and are fully readable headlessly. The key difference is where the loop runs — not what the loop does.

### B15 — The Timing Model (GodotDevWorkbench: inspector showing amount/lifetime/explosiveness/one_shot)
> The four timing properties. Lifetime: how long each particle lives — also the length of one emission cycle. Amount: how many particles in one cycle. Explosiveness: zero spreads births across the cycle; one fires them all at once. One shot: if true, the cycle runs exactly once. These four together determine when and how many particles appear.

### B16 — The Process Material Is 3D (GodotDevWorkbench: inspector showing Disable Z + gravity defaults)
> The process material is shared between 2D and 3D nodes. Its defaults are three-dimensional: gravity pointing down on the Y axis in 3D, spread that fans into all three axes. In a 2D game, particles without Disable Z set will spray into an axis the camera never shows. Always enable Disable Z for 2D effects. The official demo README says exactly this.

### B17 — Triggering and Parenting (Manim: scene tree diagram; parent hides → child hidden)
> A particle node inherits its parent's transform and visibility. If the emitter's parent hides at the moment the effect should fire — a player dying, a pickup collected — the burst can be emitting and invisible. Parenting is a design choice, not a default. Choose the parent so the effect is still visible when it needs to be seen.

### B18 — The Built-in Node in Practice (GodotDevWorkbench: Godot scene with GPUParticles2D node + sparks preview)
> Replace the teaching simulation with a built-in node. Add G P U Particles 2D to a scene. Attach a Particle Process Material. Set the spread and velocity range. The node runs the same loop we built by hand — born, moved by the material's rules, drawn by its texture — but the engine handles the simulation. The artist still chooses the behavior.

---

## Closing

### BVDT
> Let's recap with Claude. For C S Y E seventy-two seventy, Building Virtual Environments. A particle system is a birth-life-death loop running on each short-lived element. Position, velocity, and acceleration are three distinct jobs the update step handles every frame. Removal is load-bearing: without it, the population climbs without bound. Three settings — amount, lifetime, and explosiveness — determine how many particles appear and when. Godot separates emission, process, and draw: each part can be wrong on its own.

### BHTF
> Your turn. Make a fountain in a Godot teaching scene. Predict how wind and particle lifetime will change its shape, then change them separately. Your two checks: the population stops growing indefinitely; and the particles move in the direction you predicted.

### BOUT
> What Is a Particle System. At Nik Bear Brown.

---

*End of script. All narration original. Teardown register applied: direct, ear-first, no hedging.*
