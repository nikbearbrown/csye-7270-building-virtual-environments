# Chapter 14: Game AI and systems

## MA-ch14.1

A developer asks a coding agent to build a guard non-player character (NPC) as a finite state machine (FSM) instead of nested if statements. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. An FSM has a defined set of states, one of which is the current state.
- [ ] B. A transition is a rule for moving from one state to another.
- [ ] C. Ordered child nodes that are re-evaluated from a root describe an FSM.
- [ ] D. A guard stuck in Search is often missing a transition out of that state.
- [ ] E. An FSM lets the guard be in the Chase state and the Patrol state at the same time.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: A finite state machine has states and one current state at a time.
- B: Transitions are the rules that connect states.
- C: Ordered children ticked from a root describe a behavior tree.
- D: A missing or unreachable exit leaves the NPC stuck in that state.
- E: An FSM has one current state, so blending needs a different design.

**Source:** Finite state machine, state, transition

## MA-ch14.2

A designer wants to add a Flee state that the guard can enter when hurt. Check each statement that is true about where the logic lives. Each statement is worth 1 point (5 points total).

- [ ] A. A transition table is a list of nodes that are ticked from the root.
- [ ] B. In an FSM, transitions are edges between states, and their number can grow quickly as states are added.
- [ ] C. In an FSM, adding Flee needs edits to the new state alone, because existing states need no way of reaching it.
- [ ] D. In a behavior tree, "flee when hurt" can be one new high-priority branch.
- [ ] E. A behavior tree stores its logic as edges between states.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: A transition table lists which states lead to which, with conditions.
- B: Each state that can lead to another needs its own edge.
- C: Existing states need a new exit edge into Flee.
- D: A priority branch checked first avoids adding edges to the other behaviors.
- E: A behavior tree has no state-to-state edges; its logic is in node order and type.

**Source:** FSM transitions versus behavior tree priority

## MA-ch14.3

A guard's behavior tree has a root selector with children: a sequence of CanSeePlayer then Chase, a sequence of HasLastKnownPosition then Search, and Patrol. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A tick is one evaluation pass of the tree starting at the root.
- [ ] B. A selector tries its children in order and stops at the first child that does not fail.
- [ ] C. Nodes report one of success, failure or running.
- [ ] D. A sequence returns success as soon as its first child succeeds.
- [ ] E. RUNNING means the node has failed.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Each tick walks the tree from the root.
- B: A selector looks for the first child that works or is still in progress.
- C: Success, failure and running are the three results.
- D: A sequence needs its children to succeed in turn; it stops at the first child that does not succeed.
- E: RUNNING means the node is still in progress and has not finished.

**Source:** Behavior tree: tick, selector, sequence, status

## MA-ch14.4

A studio is choosing a decision architecture for its NPCs. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In GOAP the designer writes the fixed order of actions for each goal.
- [ ] B. In a behavior tree, priority comes from the order of child nodes.
- [ ] C. A finite state machine is ticked from a root node so higher-priority behaviors pre-empt lower ones.
- [ ] D. Utility AI scores candidate actions from numeric considerations and picks the highest score.
- [ ] E. GOAP describes actions by preconditions and effects, and a planner searches for a sequence that reaches a goal.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: GOAP's planner finds the sequence; the designer supplies actions and goals.
- B: Earlier children are tried first.
- C: Root ticking with ordered priority describes a behavior tree.
- D: Utility AI chooses by score.
- E: Preconditions, effects and a search are what define GOAP.

**Source:** FSM, behavior tree, utility AI, GOAP

## MA-ch14.5

A developer wants to tell a coding agent how a guard patrols, chases and searches. Check each statement that is a precise instruction using the correct terms. Each statement is worth 1 point (5 points total).

- [ ] A. "Go from Chase to Search when the player is lost for a while."
- [ ] B. "Use machine learning so the guard learns to catch the player and will not get stuck."
- [ ] C. "Make the guard intelligent and believable."
- [ ] D. "Build a finite state machine with states Patrol, Chase and Search, and a table of transitions with their conditions."
- [ ] E. "Expose the current state name as a readable property so a test can read it."

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: Lost and a while are undefined, so no test can check them.
- B: It names no states or conditions and promises an outcome that cannot be checked.
- C: It names no structure, states or conditions.
- D: It names the architecture, the states and the transition conditions.
- E: A readable state name gives a test hook.

**Source:** Precise NPC behavior instruction

## MA-ch14.6

A guard enters Chase when the player is within a radius, and leaves Chase at a larger radius. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Hysteresis is meant to make the guard move faster.
- [ ] B. Flicker is rapid switching between two states near a boundary.
- [ ] C. Using one radius for both entering and leaving Chase invites flicker when the player stays near the edge.
- [ ] D. Hysteresis means the NPC remembers the last known position of the player.
- [ ] E. Hysteresis uses different thresholds for entering and leaving a state.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Its purpose is to stop flicker, not to change speed.
- B: Flicker is the unwanted rapid state change.
- C: A player hovering at the boundary toggles the state each decision.
- D: Remembering a position is memory, often held in a blackboard.
- E: Separate enter and exit thresholds define hysteresis.

**Source:** Hysteresis and flicker

## MA-ch14.7

Check each statement that is true about steering behaviors and pathfinding. Each statement is worth 1 point (5 points total).

- [ ] A. Pursue steers toward where a moving target will be, not where it is now.
- [ ] B. Arrive is seek that slows down near the target so the NPC stops on it.
- [ ] C. Flee steers toward the target.
- [ ] D. Pathfinding computes a route as a list of points, and steering turns it into per-frame motion by adjusting velocity.
- [ ] E. Seek knows the level layout, so it routes around walls.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Pursue predicts the target's position.
- B: Arrive reduces speed inside a slowing radius.
- C: Flee steers away from the target.
- D: Pathfinding is global planning; steering is local, per-frame motion.
- E: Seek heads straight at the target and has no knowledge of walls.

**Source:** Seek, pursue, arrive, flee, pathfinding

## MA-ch14.8

A flock of birds follows three local rules with no code describing the flock's shape. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emergent behavior means the AI is defective.
- [ ] B. Separation steers a bird away from very close neighbors.
- [ ] C. Emergent behavior is a global pattern that arises from local rules and is not coded directly.
- [ ] D. Alignment steers a bird toward the average position of nearby neighbors.
- [ ] E. Cohesion steers a bird toward the average position of nearby neighbors.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Emergence is often the goal, as with flocks and crowds.
- B: Separation avoids crowding.
- C: The flock shape emerges from simple interactions.
- D: Alignment matches heading, not position.
- E: Cohesion pulls birds toward the local center.

**Source:** Separation, alignment, cohesion, emergent behavior

## MA-ch14.9

A developer needs enemies to navigate a level with walls and furniture. Check each statement that is true about grids, A* and navigation meshes. Each statement is worth 1 point (5 points total).

- [ ] A. A grid and a navigation mesh are two ways to represent walkable space, and A* is a search algorithm that can run on either.
- [ ] B. A larger agent radius widens the walkable area of the navigation mesh.
- [ ] C. A* is a representation of walkable space, like a grid.
- [ ] D. A navigation mesh covers walkable surface with polygons, so open floor needs fewer nodes than a grid.
- [ ] E. A navigation mesh is baked from level geometry and agent size, so it goes stale when static geometry changes.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Grid and navmesh describe space; A* searches over a graph built from either.
- B: A larger radius shrinks the walkable area.
- C: A* is an algorithm, not a data structure for the world.
- D: A grid stores one node per cell, while polygons cover open floor cheaply.
- E: Baking happens from geometry, so changes need a rebake.

**Source:** Grid, A*, navigation mesh, baking, agent radius

## MA-ch14.10

A* picks nodes by f = g + h. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. An admissible heuristic lets A* return a shortest path.
- [ ] B. Manhattan distance is admissible on a grid with 4-direction movement.
- [ ] C. An admissible heuristic overestimates the true remaining cost.
- [ ] D. Setting h to zero makes A* order nodes by cost so far, like Dijkstra's algorithm.
- [ ] E. g is the cost so far and h is the heuristic estimate of the remaining cost.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: With no overestimate, A* cannot skip the best route.
- B: With 4-direction moves, Manhattan distance equals the true cost without obstacles.
- C: Admissible means the heuristic does not overestimate.
- D: With h = 0, f equals g.
- E: f combines the cost so far and the estimate.

**Source:** A*, f, g, h, admissible heuristic

## MA-ch14.11

In Godot, a developer tells a coding agent: "Use a NavigationAgent2D so the enemy walks to the player." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The navigation agent moves its parent body along the path by itself.
- [ ] B. The next path position is queried once when the target is set and needs no update afterward.
- [ ] C. Navigation data is synchronised a step after it is added, so a path requested in the same frame the level is built can be empty.
- [ ] D. Having a computed path means the enemy has arrived.
- [ ] E. The navigation agent computes the path, and the body's movement code follows the next path position.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: The agent does not move the body.
- B: The next path position changes as the body moves, so it is queried each physics frame.
- C: The navigation system applies changes after a physics step.
- D: A path is a plan; arrival depends on the body reaching the target.
- E: The agent supplies the path; the body does the moving.

**Source:** Navigation agent in Godot

## MA-ch14.12

A guard's sight uses a range, a field-of-view cone and a line-of-sight test. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A line-of-sight test, such as a raycast, checks whether obstacles block the view.
- [ ] B. Field of view is the distance at which the guard can see.
- [ ] C. A cone check can compare the dot product of facing and direction-to-target with the cosine of the half-angle.
- [ ] D. Range and cone checks also handle walls.
- [ ] E. Sight range limits how far the guard can see.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: A raycast tests for blockers.
- B: Field of view is an angle, not a distance.
- C: A larger dot product means the target is within the half-angle.
- D: Range and angle ignore obstacles.
- E: Range is the distance limit.

**Source:** Perception: range, cone, line of sight

## MA-ch14.13

A guard hears a bottle break out of sight and goes to the sound's position, stored in a blackboard entry. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A blackboard is shared memory that nodes read and write.
- [ ] B. Hearing is usually modelled as an event with a position and loudness.
- [ ] C. An NPC that reads the player's position directly is omniscient.
- [ ] D. A stored noise position should expire or be cleared once it has been checked.
- [ ] E. The blackboard is the logic that decides whether the guard searches or patrols.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: A blackboard shares facts between nodes.
- B: A noise event carries a location and loudness.
- C: Omniscient means knowing the player's position without perceiving it.
- D: Knowledge goes stale, so it should be cleared.
- E: The blackboard stores data; states or the tree hold the logic.

**Source:** Blackboard, hearing, omniscient NPC

## MA-ch14.14

A developer asks an agent for "random terrain" and gets static-looking heights. Check each statement that is true about noise. Each statement is worth 1 point (5 points total).

- [ ] A. Adding octaves smooths the terrain by removing detail.
- [ ] B. White noise returns similar values for nearby coordinates.
- [ ] C. An octave is a layer of noise at higher frequency and lower amplitude that adds finer detail.
- [ ] D. Coherent noise gives a different value each time the same coordinate is sampled.
- [ ] E. Coherent noise needs a separate seed for each coordinate.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: More octaves add detail rather than smoothing.
- B: White noise has no relation between neighbors, which is why it looks like static.
- C: Octaves layer finer detail over broad shapes.
- D: Noise is a deterministic function of coordinate and seed.
- E: One seed defines the whole noise field.

**Source:** White noise, coherent noise, octaves

## MA-ch14.15

A level generator should produce the same level whenever it is given seed 7. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Adding a random call for decorations before the layout code leaves the layout unchanged.
- [ ] B. A seed makes the output unpredictable.
- [ ] C. A seed fixes a pseudo-random sequence, so the same seed and algorithm give the same level.
- [ ] D. A seed gives the same level across engine updates even if the engine changes its generator.
- [ ] E. Seeding from the clock keeps levels reproducible.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: An extra draw shifts the later values.
- B: A seed makes output repeatable.
- C: Pseudo-random output is deterministic given its seed.
- D: A changed generator algorithm changes the sequence.
- E: A clock-based seed differs each run.

**Source:** Seed, determinism, pseudo-random

## MA-ch14.16

A platform generator sometimes makes gaps wider than the player's jump. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Constructive generation builds within the player's limits, so an impossible gap is not representable.
- [ ] B. A validator proves that a level is fun.
- [ ] C. A safety margin keeps gaps below the exact measured jump limit.
- [ ] D. Generate-and-test rejects failing levels and re-rolls them.
- [ ] E. A validator checks reachability against the measured jump limits.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Limits applied during building prevent bad gaps.
- B: A validator only checks rules in a model of the game.
- C: A margin guards against frame-perfect jumps.
- D: Generate-and-test discards failures.
- E: Reachability is a playability rule.

**Source:** Validator, generate-and-test, constructive generation, safety margin

## MA-ch14.17

A team trains an NPC with reinforcement learning (RL) to cross a grid and reach a goal. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The environment is the NPC that acts.
- [ ] B. Reward is the agent's current location.
- [ ] C. Training uses a labeled dataset of correct moves.
- [ ] D. The agent is the grid world and its rules.
- [ ] E. The policy maps what the agent observes to the action it takes.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: The agent is the NPC that acts.
- B: Reward is a numeric feedback signal; location is state.
- C: RL learns from reward by trial and error.
- D: The grid world and rules are the environment.
- E: A policy is the decision rule.

**Source:** Agent, environment, reward, policy

## MA-ch14.18

An RL agent collects rewards over several steps. Check each statement that is true about return and Q-learning. Each statement is worth 1 point (5 points total).

- [ ] A. The learning rate sets how far Q moves toward the target in an update.
- [ ] B. A Q-learning update needs labeled correct moves.
- [ ] C. Return is the sum of the rewards over steps, each weighted by a discount.
- [ ] D. A discount factor below 1 values a distant reward less than an immediate one.
- [ ] E. With a discount factor of 0, the agent values a distant reward as much as an immediate one.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: The learning rate scales the step toward the target.
- B: Q-learning learns from reward and next-state values, not labels.
- C: Return is the discounted sum of rewards.
- D: Discounting shrinks later rewards.
- E: With a discount of 0, only the immediate reward counts.

**Source:** Return, discount factor, learning rate, Q-learning

## MA-ch14.19

A designer discusses reward design and deployment of an RL NPC. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A sparse reward is feedback that arrives rarely, which makes learning hard.
- [ ] B. A trained policy is expected to keep learning during play by default.
- [ ] C. RL lets designers directly author each behavior.
- [ ] D. Reward shaping removes the need to inspect the trained behavior.
- [ ] E. Reward hacking is an agent exploiting a loophole that scores well without doing what the designer meant.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Rare reward gives little signal.
- B: A trained policy typically runs as a fixed decision function.
- C: Behavior is learned, so it is hard to author or debug directly.
- D: Shaping adds guiding rewards; the result still has to be inspected.
- E: The agent optimizes the score, not the intent.

**Source:** Sparse reward, reward hacking, reward shaping, training versus deployment

## MA-ch14.20

A developer tells a coding agent: "Add enemy AI." Check each statement that is a precise rewrite using the correct terms. Each statement is worth 1 point (5 points total).

- [ ] A. "Use a sight range and a line-of-sight raycast that walls can block."
- [ ] B. "Make the AI smart."
- [ ] C. "Use pathfinding on a navigation mesh with steering, so the guard goes around walls."
- [ ] D. "Leave Chase at a larger radius than the radius used to enter it, so the guard does not flicker."
- [ ] E. "Move the guard toward the player each frame."

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: It names the range and an obstacle-aware check.
- B: Smart names no mechanism.
- C: It names pathfinding, the representation and steering.
- D: It names hysteresis in effect.
- E: Moving straight at the target ignores walls.

**Source:** Rewriting a vague NPC prompt

## MA-ch14.21

A game has a door guard, a boss with several interruptible phases and attacks, and a villager balancing hunger, tiredness and work. Check each statement that is a sound match of architecture to NPC. Each statement is worth 1 point (5 points total).

- [ ] A. An FSM suits the door guard, which has a few distinct modes.
- [ ] B. Utility AI suits the villager, whose competing needs are continuous.
- [ ] C. An FSM is best for choosing among continuous competing needs.
- [ ] D. GOAP picks the action with the highest numeric score.
- [ ] E. A behavior tree suits the boss, with priority branches that interrupt one another.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: A few distinct modes fit states.
- B: Scoring suits continuous needs.
- C: FSMs switch between discrete modes, not weighted needs.
- D: That describes utility AI; GOAP plans a sequence.
- E: Ordered priority supports interruption.

**Source:** Choosing an architecture per NPC

## MA-ch14.22

An enemy walks into the first wall when told to move toward the player each frame. Check each statement that is true about pathfinding terms. Each statement is worth 1 point (5 points total).

- [ ] A. Local avoidance is steering that reacts to nearby moving objects.
- [ ] B. A larger agent radius lets the agent through narrower passages.
- [ ] C. A waypoint is a check of whether the player is visible.
- [ ] D. A stale navigation mesh still gives correct paths after geometry changes.
- [ ] E. An unreachable target is a case where pathfinding returns no path and the code has to handle it.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Steering handles local, moving things.
- B: A larger radius blocks narrow passages.
- C: A waypoint is a point along a path.
- D: A stale mesh no longer matches the level.
- E: A missing path is a case to handle.

**Source:** Waypoint, local avoidance, unreachable target, stale navmesh

## MA-ch14.23

A designer wants a crowd of 100 pedestrians that walk to destinations and avoid bumping into each other. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emergent crowd results can be guaranteed without simulation.
- [ ] B. Weights are tuned to balance the combined behaviors.
- [ ] C. Pathfinding handles the reaction to other moving pedestrians.
- [ ] D. Obstacle avoidance steers toward the nearest obstacle.
- [ ] E. Several steering outputs can be combined as a weighted sum.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Emergent results depend on conditions and need testing.
- B: Weights set the balance.
- C: Pathfinding gives the global route; steering reacts locally.
- D: Obstacle avoidance steers away from obstacles.
- E: Weighted sums combine steering outputs.

**Source:** Combining steering behaviors, emergent behavior

## MA-ch14.24

A developer says: "Our level generator is random, so we cannot test it." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A random generator is untestable by definition.
- [ ] B. Fixing the seed makes the generated output reproducible for tests.
- [ ] C. A validator passing means the level fits a model of the rules, not that it is fun.
- [ ] D. Playtests are still needed alongside a validator.
- [ ] E. A pseudo-random generator is deterministic given its seed.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Fixed seeds and validators make it testable.
- B: A fixed seed repeats the output.
- C: The validator checks rules only.
- D: Human play checks what the model misses.
- E: Determinism follows from the seed.

**Source:** Testing a procedural generator
