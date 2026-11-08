# Chapter 9: Particle effects

## MA-ch09.1

A technical artist describes a campfire to a coding agent and has to pick the exact particle-effect noun for each part. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An emitter is the source that creates particles, either steadily at a rate or in bursts.
- [ ] B. A particle is one small element that the system creates, updates and removes over time, with its own age, position and velocity.
- [ ] C. A particle system is the whole effect (spawning, simulation and drawing), and one system can combine several emitters.
- [ ] D. A particle is a separate game object with its own script, which is why it is called a particle.
- [ ] E. An emitter is the name for the whole finished effect, including its drawing settings and each particle it has made.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: The emitter is where particles are born, and its rate or burst settings say when.
- B: A particle is a lightweight record with a life cycle: it is born, updated each step and removed.
- C: The system covers emission, simulation and drawing, and a larger effect can use more than one emitter.
- D: Particles are data processed in bulk by the system, not individual objects with scripts.
- E: The whole effect is the particle system; the emitter is only the part that creates particles.

**Source:** Particle, emitter and particle system

## MA-ch09.2

A developer separates two settings that both control where particles come from and how they move. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emission shape (point, sphere, box or cone) sets the region where particles are born.
- [ ] B. A larger spread makes each particle leave the emitter faster.
- [ ] C. Emission shape and initial velocity are separate settings.
- [ ] D. Initial velocity sets the starting speed and direction of a particle after it is born.
- [ ] E. Spread is the exact word for the launch speed of a particle.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: The emission shape decides placement of births.
- B: Speed comes from the initial velocity, not from the spread.
- C: Placement of births and motion after birth are independent controls.
- D: Initial velocity is the speed and direction a particle has at birth.
- E: Spread is the range of launch directions; launch speed comes from the initial velocity.

**Source:** Emission shape, initial velocity and spread

## MA-ch09.3

A coding agent is asked for the right emission term for each behaviour. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emission rate is the number of particles born per unit time, such as 40 per second.
- [ ] B. A looping system plays one cycle and then stops until it is triggered again.
- [ ] C. A burst is a stated count of particles born at one instant.
- [ ] D. One-shot (non-looping) means the system keeps cycling until it is stopped.
- [ ] E. A burst puts its particles at one instant, unlike a high continuous rate.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Rate is a count per unit time, so it spreads births over time.
- B: A looping system starts its cycle again when it ends.
- C: A burst delivers its whole count at one moment.
- D: One-shot controls how many cycles play; it plays one and stops.
- E: A high rate spreads births over time, whereas a burst delivers them at one moment.

**Source:** Emission rate, burst, one-shot and looping

## MA-ch09.4

A smoke emitter runs continuously. Check each statement that is true about the terms that fix how many particles are alive. Each statement is worth 1 point (5 points total).

- [ ] A. The steady-state live count is roughly emission rate times lifetime.
- [ ] B. Doubling the emission rate at the same lifetime leaves the live count unchanged.
- [ ] C. Lifetime is the time a particle stays alive after it is born, before the system removes it.
- [ ] D. Doubling the lifetime at the same rate leaves the live count unchanged.
- [ ] E. Lifetime is the number of particles the emitter makes per second.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Births per second times seconds of life gives the number alive once the effect has settled.
- B: Live count scales with the rate, so doubling the rate doubles the count.
- C: Lifetime is the length of a particle's life in seconds.
- D: A longer life means particles pile up for longer before removal, so the count grows.
- E: That describes emission rate, not lifetime.

**Source:** Rate, lifetime and live particle count

## MA-ch09.5

A newly started smoke effect looks thin for its first seconds. Check each statement that is true about the term for fixing this. Each statement is worth 1 point (5 points total).

- [ ] A. Burst mode is a separate emission setting from prewarm.
- [ ] B. Prewarm lets the effect start with its steady-state population instead of ramping up from nothing.
- [ ] C. Prewarm raises the emission rate for the whole run of the effect.
- [ ] D. Prewarm simulates the system for some time before the first visible frame.
- [ ] E. Prewarm needs to cover less than one particle lifetime to reach a full population.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Prewarm changes the starting state; burst mode changes how particles are emitted.
- B: Skipping the ramp-up is the whole purpose.
- C: Prewarm changes the starting state, not the rate.
- D: Prewarm runs the simulation ahead of the first drawn frame.
- E: Particles reach full population only after one lifetime has passed, so the prewarm has to be at least that long.

**Source:** Prewarm and steady state

## MA-ch09.6

A developer sends two prompts for a 2D grenade explosion. Prompt 1: "add an explosion effect". Prompt 2: "add a one-shot burst of 40 particles at the grenade's position, lifetime 0.6 seconds, initial speed 150 to 300 pixels per second in all directions, no gravity, scale curve to zero and alpha ramp to transparent over life". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "One-shot burst of 40" leaves the number of particles for the agent to guess.
- [ ] B. "Explosion" in Prompt 1 names no count, lifetime, speed, direction or loop behaviour, so the agent has to guess them.
- [ ] C. Prompt 1 leaves the agent free to build a looping emitter that keeps spraying after the grenade has gone off.
- [ ] D. Adding "and make it look cool" to Prompt 2 adds a constraint the agent can measure.
- [ ] E. Prompt 1 is precise because explosion is a standard term with one settled meaning across engines.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: One-shot sets the cycle count and burst with a number fixes the particles born at one instant.
- B: A scene word like explosion fixes none of the properties that define the effect.
- C: Without one-shot, looping versus playing once is the agent's choice.
- D: An adjective that cannot be measured adds no constraint and no check.
- E: Explosion is a description of a look, not a defined particle setting.

**Source:** Vague versus precise particle prompt

## MA-ch09.7

Particles launched in a 2D game are described with physics terms. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Initial velocity is the velocity a particle has at birth.
- [ ] B. A particle launched with zero initial velocity stays still while gravity acts on it.
- [ ] C. Gravity is a constant velocity that is added once at birth.
- [ ] D. Gravity on a particle is a constant acceleration, so it keeps changing the particle's velocity.
- [ ] E. Acceleration is another word for the speed of a particle.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: Initial velocity is the starting speed and direction.
- B: Velocity grows by the acceleration each second, so it leaves zero and the particle moves.
- C: A velocity added once would be an initial velocity, not gravity.
- D: Acceleration is a rate of change of velocity, applied continuously.
- E: Speed is how fast; acceleration is how quickly the velocity changes.

**Source:** Initial velocity, gravity and acceleration

## MA-ch09.8

A particle has a lifetime of 0.6 seconds, a scale curve falling from 1 to 0 and a colour ramp fading alpha from 1 to 0. Check each statement that is true about over-lifetime terms. Each statement is worth 1 point (5 points total).

- [ ] A. A colour ramp sets the colour at birth, and fading needs a script that updates the colour as the particle ages.
- [ ] B. A curve or ramp over lifetime is read by normalised age, which is age divided by lifetime and runs from 0 to 1.
- [ ] C. Because curves use normalised age, the same curve works for particles with different lifetimes.
- [ ] D. A scale curve changes the colour of a particle over its life.
- [ ] E. A curve read by normalised age ends at the particle's death for lifetimes of 0.6 s and 1.2 s alike.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A colour ramp is sampled across the whole life, which is how fades are made without code.
- B: Normalised age is the fraction of life used so far.
- C: Reading by fraction of life stretches one curve over any lifetime.
- D: A scale curve changes size; a colour ramp changes colour.
- E: Reading by fraction of life puts the end of the curve at death for any lifetime.

**Source:** Scale curve, colour ramp and normalised age

## MA-ch09.9

Engines let a particle system simulate on the CPU or on the GPU. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. GPU particles lose textures and blend modes, because those belong to the CPU side.
- [ ] B. CPU simulation cost stays flat as the particle count rises.
- [ ] C. Both CPU particles and GPU particles are drawn by the GPU.
- [ ] D. GPU particles update their state in shaders on the graphics card.
- [ ] E. The setting decides where the per-particle update (the simulation) runs.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Textures and blending belong to drawing, which both kinds share.
- B: CPU simulation is per-particle work, so more particles take more CPU time.
- C: Both kinds are drawn by the GPU; the setting is about where the simulation runs.
- D: GPU simulation is a data-parallel update on the graphics card.
- E: Simulation means the update, and it runs in one place or the other.

**Source:** CPU versus GPU particles

## MA-ch09.10

A game needs ambient snowfall with 20,000 flakes and, separately, 80 sparks that each damage an enemy on touch. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. GPU particles keep their particle data on the CPU, so scripts read each flake cheaply.
- [ ] B. A cosmetic effect is one whose particles feed back into gameplay logic.
- [ ] C. Snowfall is a cosmetic effect with a large count, which suits GPU particles.
- [ ] D. A CPU particle system runs on a wider range of devices because it does not need good GPU compute.
- [ ] E. Sparks that apply a gameplay rule need their state read by a script, which is easier with CPU particles or with separate gameplay objects.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: GPU particle data stays on the graphics card, so scripts cannot cheaply read it.
- B: A cosmetic effect only changes the look; gameplay-affecting particles are the opposite.
- C: Large cosmetic effects are what GPU simulation is built for.
- D: Older hardware can lack GPU compute, so CPU particles are the safe fallback.
- E: Gameplay logic runs in scripts, which need particle state on the CPU side.

**Source:** Choosing CPU or GPU particles

## MA-ch09.11

A spaceship flies across the screen. Its exhaust should trail behind it, and its shield shimmer should stay around it. Check each statement that is true about the coordinate-space term for each. Each statement is worth 1 point (5 points total).

- [ ] A. The shield shimmer needs world coordinates so that its particles stay around the ship.
- [ ] B. The exhaust needs local coordinates so that its particles follow the ship.
- [ ] C. Local coordinates keep particle positions relative to the emitter, so the particles travel with it.
- [ ] D. The local or world setting changes the result for an emitter that stays still.
- [ ] E. World coordinates leave a particle where it was born while the emitter moves, which forms a trail.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A shimmer around a ship needs local coordinates, so particles move with it.
- B: Local space would carry the exhaust along with the ship, so no trail would form.
- C: Local-space positions are stored relative to the emitter's transform.
- D: With a stationary emitter both settings give the same positions.
- E: A world-space particle is no longer tied to the emitter after birth.

**Source:** Local versus world coordinates

## MA-ch09.12

Particles are combined with the background by a blend mode. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Additive blending suits fire, sparks and glows.
- [ ] B. Additive blending suits dark smoke, because a dark colour darkens the background when it is added.
- [ ] C. Additive blending adds the particle's light to the background, so overlap brightens toward white.
- [ ] D. Alpha blending mixes the particle colour with the background in proportion to alpha, so drawing order matters.
- [ ] E. Two additive particles give the same result in either drawing order.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Emissive effects accumulate light where they overlap, which suits additive blending.
- B: Adding a dark colour adds close to nothing, so additive smoke would be nearly invisible.
- C: Adding colours can only brighten, and results clamp at white.
- D: Alpha blending is particle times alpha plus background times one minus alpha, which depends on order.
- E: Addition does not depend on order.

**Source:** Additive versus alpha blending

## MA-ch09.13

A 3D game draws each smoke particle as a flat textured quad. Check each statement that is true about billboarding. Each statement is worth 1 point (5 points total).

- [ ] A. A billboarded particle can still spin about the view direction, which is how rotation over lifetime works for flat particles.
- [ ] B. In a 2D game with a flat orthographic camera, billboarding has to be switched on to face the quads to the screen.
- [ ] C. Without billboarding, a flat quad seen edge-on shrinks to a thin line.
- [ ] D. A billboard is a quad turned each frame to face the camera.
- [ ] E. A particle drawn as a mesh keeps its 3D shape instead of being a billboard.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Spinning about the view direction leaves the quad facing the camera.
- B: Quads already face the screen with a flat orthographic camera.
- C: A flat quad has no thickness, so from the side it has almost no area.
- D: Turning toward the camera each frame is what billboarding means.
- E: A mesh particle keeps its 3D shape and orientation; it is the alternative to a billboard.

**Source:** Billboarding

## MA-ch09.14

A smoke effect uses many large transparent quads. Check each statement that is true about the cost terms. Each statement is worth 1 point (5 points total).

- [ ] A. Transparent corners of a quad are still shaded, so they add fragment cost.
- [ ] B. Overdraw is the same screen pixel being shaded more than once by overlapping surfaces.
- [ ] C. Fill rate is how many pixels the GPU can shade and write per second, and overdraw uses it up.
- [ ] D. A fragment is one pixel-sized unit of work for the fragment shader.
- [ ] E. Doubling the width and height of each quad doubles its fragment count.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Transparent pixels are still shaded and blended.
- B: Overdraw describes layers of overlapping surfaces on one pixel.
- C: Fill rate is the throughput limit, and many layers per pixel consume it.
- D: Each covered pixel of a quad runs the fragment shader once.
- E: Area scales with the square of the side, so the count quadruples.

**Source:** Overdraw, fragment and fill rate

## MA-ch09.15

A developer asks why many large transparent particles cost more than opaque ones. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Halving the lifetime at the same emission rate doubles the number of live particles.
- [ ] B. The depth test can reject a hidden opaque fragment when something nearer is already drawn.
- [ ] C. Lowering alpha everywhere reduces the number of fragments shaded.
- [ ] D. Overdraw is a cheap cost on mobile GPUs.
- [ ] E. Stacked transparent particles are skipped by early rejection, like hidden opaque ones.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: Live count equals rate times lifetime, so halving the lifetime halves the count.
- B: Early rejection by depth skips opaque work that would be hidden.
- C: Alpha changes the result colour, not the fragment count.
- D: Fill rate is a main constraint on mobile, and overdraw spends it.
- E: Blended layers are not skipped, because each contributes to the final colour.

**Source:** Transparency, depth test and live count

## MA-ch09.16

A burst effect gives each particle a random speed and direction. Check each statement that is true about random seeds. Each statement is worth 1 point (5 points total).

- [ ] A. A fixed seed makes the effect look different each time it plays.
- [ ] B. A fixed seed makes a burst identical at 30 and at 144 frames per second, because time does not matter.
- [ ] C. Tests fix the seed so a burst can repeat and a failure can be reproduced.
- [ ] D. The same seed with a different draw order gives the same number for each particle.
- [ ] E. A random seed is the starting value of a pseudo-random generator.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: The same seed gives the same sequence, so each play looks the same.
- B: Positions also depend on the time step, so frame rates can still differ.
- C: Repeatability is the point of seeding in a test.
- D: A different order of draws changes which number each particle gets, even with the same seed.
- E: The seed initialises the generator's sequence.

**Source:** Random seed and determinism

## MA-ch09.17

A developer needs a campfire in 3D and writes a prompt: "a looping emitter, 80 particles per second, lifetime 0.8 seconds, world-space coordinates, additive blending, billboarded quads, initial upward velocity, colour ramp from yellow to transparent red, scale shrinking to zero over life". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Billboarded quads" tells the agent to turn each particle toward the camera.
- [ ] B. "Looping" tells the agent the emitter keeps cycling until it is stopped.
- [ ] C. "World-space" on a carried torch lets the flames trail behind as the player moves.
- [ ] D. "Make the fire look good" would carry the same settings as the prompt.
- [ ] E. "Additive blending" is the exact term for flames that cover and darken the background.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Billboarding keeps flat particles facing the camera.
- B: A looping emitter restarts its cycle again and again.
- C: World-space particles are left behind when the emitter moves.
- D: A look word fixes no rate, lifetime, space or blend mode.
- E: Additive blending adds light, so it brightens; covering and darkening is alpha blending.

**Source:** Precise looping effect prompt

## MA-ch09.18

An enemy is destroyed the instant it is hit, and a one-shot burst effect is a child of the enemy in the scene hierarchy. A log line says "burst started", yet players never see it. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A child effect can be cut off the moment its parent is destroyed or hidden.
- [ ] B. A one-shot effect plays again on the next hit without further action.
- [ ] C. Spawning the effect as its own object at the enemy's position lets it outlive the enemy.
- [ ] D. The log line proves the burst was drawn, because starting the effect means drawing it.
- [ ] E. Switching to GPU particles fixes this, because GPU particles are not tied to a parent.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Children go with their parent when it is destroyed, hidden or deactivated.
- B: A one-shot plays one cycle and stays finished until restarted or spawned again.
- C: A separate effect object has its own lifetime.
- D: A log line records that the effect started, not that it was visible.
- E: The cause is the parent-child relationship, not where the simulation runs.

**Source:** Parenting and triggering an effect

## MA-ch09.19

A coding agent reports "test passes: the burst is emitting" from a headless run (no window, a dummy renderer that draws nothing). Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Visual intent is what the effect should look like, and a person has to look at the screen to check it.
- [ ] B. State, visual intent and cost are three names for the same check.
- [ ] C. Emitting is engine state, a flag the engine reports, not proof of appearance.
- [ ] D. A headless run does not show overdraw or fill rate, since nothing is drawn.
- [ ] E. A dummy renderer does no GPU work, so its timing says nothing about GPU cost.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Appearance needs a human, or a real render, to judge.
- B: They are separate kinds of evidence, each reached by a different test.
- C: State covers what the engine reports, such as emitting, position and finished.
- D: Drawing costs exist only when a real renderer runs.
- E: A dummy renderer does no GPU work, so its figure is a property of the instrument.

**Source:** State versus visual intent versus cost

## MA-ch09.20

In Godot, a 2D death burst uses a GPU particle node with a process material (the object that holds speed, direction, spread, gravity and over-life settings). The node reports it is emitting, yet players see almost nothing. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emitting means the particles are on screen at a visible size.
- [ ] B. The process material holds the motion and over-life settings for the particles.
- [ ] C. A node with no texture draws each particle as a tiny square, which is nearly invisible.
- [ ] D. A texture is a property of the GPU particle node, not of the CPU node alone.
- [ ] E. A wide spread in a 2D game keeps the motion in the visible plane.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Emitting is a state flag and says nothing about size.
- B: The process material is the settings object for how particles move and change.
- C: A missing texture leaves a very small default particle.
- D: Both node kinds take a texture as an ordinary property.
- E: The material also serves 3D, so velocity can point along the z axis, which a 2D view cannot show.

**Source:** Details a 2D particle node needs

## MA-ch09.21

An agent rewrites "add an explosion when the grenade hits" into a precise instruction. Check each statement that is true about which wording is exact. Each statement is worth 1 point (5 points total).

- [ ] A. "Spread" is the exact word for the range of launch directions.
- [ ] B. "Fade out" is an exact term for a scale curve.
- [ ] C. "One-shot burst of N particles" is exact wording for a single cycle with a stated count at one instant.
- [ ] D. "Spawn at the grenade's position in world coordinates, as its own object" keeps the effect visible after the grenade is hidden.
- [ ] E. "Loop a continuous emission" is the exact wording for a single explosion.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Spread is the width of the cone of launch directions.
- B: Fading is a colour or alpha ramp; a scale curve changes size.
- C: One-shot gives one cycle and burst gives a count at one instant.
- D: World coordinates and a separate object keep the effect independent of the grenade.
- E: Looping with a rate keeps spraying; an explosion is a burst.

**Source:** Rewrite of the grenade explosion prompt

## MA-ch09.22

A smoke effect has a limit on live particles. A burst of 100 particles fires every 0.5 seconds, each living 1.2 seconds. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A limit on live particles is checked against the average, not the peak.
- [ ] B. The peak live count is the highest number of particles alive at one instant.
- [ ] C. The average live count is emission rate times lifetime, so bursts can have a higher peak than the average.
- [ ] D. Shortening the lifetime lowers the peak, since fewer bursts overlap.
- [ ] E. Overlapping bursts raise the peak, because particles from earlier bursts are still alive.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: A hard cap applies to the peak, because that is when it is exceeded.
- B: Peak means the maximum over time.
- C: A burst pattern is lumpy, so its peak sits above the steady average.
- D: A shorter life means older bursts are removed before the next one arrives.
- E: Burst overlap adds counts.

**Source:** Peak versus average live count

## MA-ch09.23

A rocket flies around a 2D screen with an exhaust and a glowing aura. A developer writes: "Attach two particle effects to the rocket." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An exhaust set to local coordinates is carried as a rigid plume with no trail.
- [ ] B. Naming rate, lifetime and parent alongside the space makes the instruction more exact.
- [ ] C. An aura set to world coordinates stays around the rocket as it moves.
- [ ] D. The instruction leaves the coordinate space to the agent's default.
- [ ] E. "Exhaust in world coordinates, aura in local coordinates" removes the guess.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Local-space particles travel with the emitter.
- B: Each named setting is one fewer guess for the agent.
- C: A world-space aura is left behind and smears across the screen.
- D: The word attach does not state the space.
- E: Naming the space for each effect decides trail versus follow.

**Source:** Rewrite of the exhaust and aura prompt
