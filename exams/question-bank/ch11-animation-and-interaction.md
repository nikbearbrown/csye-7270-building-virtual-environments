# Chapter 11: Animation and interaction

## MA-ch11.1

A developer describes a platformer character as an animation state machine with the states Idle, Run, Jump and Fall. Check each statement that is true about the vocabulary. Each statement is worth 1 point (5 points total).

- [ ] A. A transition is the test that compares a value with a threshold.
- [ ] B. A transition is an allowed route from one state to another, usually guarded by a condition.
- [ ] C. A state is a named situation of the character, and the machine is in one current state at a time within a layer.
- [ ] D. A condition is the allowed route from one state to another.
- [ ] E. A parameter is a value supplied by the game, such as speed or on-floor, that conditions read.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: That describes a condition; the transition is the route the condition guards.
- B: Transitions are the explicit connections that say which state may follow which.
- C: A state machine has one current state, which separates it from a set of independent flags.
- D: That describes a transition; a condition is the test that lets a transition fire.
- E: Parameters are the inputs that the game writes and the conditions read.

**Source:** State machine: state, transition, condition, parameter

## MA-ch11.2

A script tracks animation with four independent boolean flags (is_jumping, is_attacking, is_crouching, is_hurt) inside nested if statements. A teammate proposes a state machine instead. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Four flags describe four situations, one per flag, so the flags stay consistent with each other.
- [ ] B. The number of transitions in a state machine equals the number of states.
- [ ] C. In a state machine the current state is one named value, so a bug report can name the state the character was in.
- [ ] D. A state machine removes the need for conditions, because each state picks its own next state.
- [ ] E. Four independent booleans give 16 combinations, and some of them, such as jumping and hurt at once, were not designed.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Independent flags can be set in contradictory ways, which is the weakness of the flag approach.
- B: Transitions are the allowed routes between states and their count is independent of the state count.
- C: One current state is a single value that can be logged, shown and reported.
- D: Transitions still need conditions or events that say when a change happens.
- E: Four booleans give 2^4 = 16 combinations, many of them undesigned.

**Source:** State machine versus flags and nested conditionals

## MA-ch11.3

In Godot, an AnimationTree node plays clips stored in an AnimationPlayer. Check each statement that is true about the node types. Each statement is worth 1 point (5 points total).

- [ ] A. The clips live in the AnimationPlayer, and the tree decides how much of each clip enters the final pose.
- [ ] B. A state machine and a blend tree are two names for the same graph.
- [ ] C. The AnimationTree keeps its own copy of the clips, separate from the AnimationPlayer.
- [ ] D. A blend space picks its output from a position on one or two axes and mixes the clips placed near that position.
- [ ] E. A blend tree plays one active state at a time and moves between states with transitions.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: The AnimationPlayer stores clips; the tree mixes them into one pose.
- B: A state machine selects among states; a blend tree combines inputs by weight, so they are different nodes.
- C: The tree references the player's clips and does not hold its own copy.
- D: A blend space maps a continuous position to a weighted mix of neighbouring clips.
- E: That describes a state machine; a blend tree mixes inputs by weight.

**Source:** Animation tree, state machine, blend tree and blend space

## MA-ch11.4

A character should walk, jog or sprint according to how far the stick is pushed, and should commit to a jump once it has started. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A jump suits a blend, because a blend gives a committed action its own entry, exit and duration.
- [ ] B. Walk, jog and sprint suit a blend space driven by a speed parameter, because speed varies continuously.
- [ ] C. A blend space can prevent a started jump from being interrupted by movement input.
- [ ] D. One state per tiny speed step, such as walk_1 to walk_20, is a more precise form of blending.
- [ ] E. A blend space needs a transition with its own condition between neighbouring clips on its axis.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: A committed action is a state with defined ways in and out; a blend only mixes clips.
- B: A blend space maps a continuous number such as speed to a mix of neighbouring clips.
- C: Interrupt rules belong to states and transitions; a blend only sets clip weights.
- D: Many states need many transitions and still jump between steps; a blend changes smoothly with one parameter.
- E: Blend spaces mix by position and do not use per-pair transitions.

**Source:** Blend space versus state

## MA-ch11.5

In Unity, an Animator Controller reads Animator parameters of type float, int, bool and trigger, and a script writes them. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A parameter is an output of the controller, written back to the script to say what to do next.
- [ ] B. A bool holds its value until the script changes it, so a condition on it stays satisfied while it is true.
- [ ] C. An int is the parameter type meant for a one-shot event that resets itself.
- [ ] D. A float such as Speed suits a comparison like greater than 0.1 and can also drive a blend tree.
- [ ] E. A trigger is meant for a one-time event and is reset once a transition consumes it.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Parameters are inputs that the script writes and the controller reads.
- B: A bool is a level: it keeps its value until it is changed.
- C: That describes a trigger; an int holds a whole number.
- D: Floats feed numeric comparisons and blend parameters.
- E: A trigger is a boolean that the controller clears when a transition uses it.

**Source:** Animator parameter types

## MA-ch11.6

Physics runs in fixed ticks and the animation graph updates once per rendered frame. A held jump key makes the character land on one tick and jump on the next, and the graph reads on-floor only at its own update. Players see the character stay in its Fall state while it rises. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Running the graph in the physics step is one way to align the two sampling rates.
- [ ] B. The fault is a physics engine bug, because physics should not let a landing and a take-off share one frame.
- [ ] C. A tick is one step of the physics simulation, and an update is one evaluation of the animation graph.
- [ ] D. Polling means the engine calls your code at the moment a value changes.
- [ ] E. A condition read once per graph update can miss a value that changed and changed back between two reads.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Engines offer update or callback modes that run animation in the physics step.
- B: Physics is correct; the graph samples more slowly than the state changes.
- C: Ticks belong to the physics clock and updates belong to the animation or render clock.
- D: That describes a callback or event; polling is checking a value on each update.
- E: A sampled value can miss a short-lived state, which is a sampling gap.

**Source:** Sampling gap: tick, update, polling

## MA-ch11.7

A developer tells a coding agent: 'when the player presses Space, switch to the jump state'. The character also has a Hurt state that ignores input. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Choosing animation straight from key presses keeps the picture in step with what the movement code does.
- [ ] B. A guard is an extra condition on a transition, such as the character being on the floor.
- [ ] C. Driving Jump from physical state, such as leaving the floor with upward velocity, stays consistent when a bounce pad causes the launch.
- [ ] D. Interpreting key presses is the job of the animation state machine itself.
- [ ] E. The phrase ties the state change to the key press, so the agent may start a jump during Hurt.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Movement code can ignore or override a press, so picture and movement can disagree.
- B: Guards add conditions so a transition fires only in the right situation.
- C: A condition on what the body is doing agrees with movement whatever caused it.
- D: Gameplay code interprets input and then sets state or parameters for animation.
- E: A press-only condition ignores whether the character can jump now.

**Source:** Input-driven versus state-driven change; guard

## MA-ch11.8

A character has the states Idle, Run, Attack, Hurt and Dead. Hit reactions interrupt an attack, Dead overrides the other states, and Run input does not interrupt an attack. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Priority is needed because two states can be active at once.
- [ ] B. A transition from Any State to Dead expresses that death overrides the other states.
- [ ] C. An interrupt is a transition taken out of the current state before its clip ends.
- [ ] D. Leaving out an Attack-to-Run transition forbids that interruption, and Attack still needs some exit.
- [ ] E. Priority or order decides which transition is taken when more than one is valid at the same moment.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: A machine has one active state; priority chooses between several valid transitions.
- B: Any State is a special source that stands for the states in the machine.
- C: An interrupt leaves a state early, through a transition that does not wait for the clip to finish.
- D: A missing transition is how a machine forbids a change, but a state without an exit sticks.
- E: Equal-looking choices are settled by an order, which should be stated.

**Source:** Interrupt, priority, Any State

## MA-ch11.9

After the player is hit, the character plays the Hurt animation and then freezes in its last pose. The only transition out of Hurt has the condition 'hurt_finished is true', and nothing in the code sets it. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An unconditional transition from Hurt to Dead is a clean fix without side effects.
- [ ] B. This is a stuck state: the machine sits in a state whose exit condition stays false.
- [ ] C. A stuck state is hard to detect because a machine has no single current state to look at.
- [ ] D. An exit-time transition, which leaves when the clip ends, removes the dependence on a flag nobody sets.
- [ ] E. The cause is a fault in the animation clip, because clips decide transitions.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: An unconditional route would send every hurt character to Dead, which is a new fault.
- B: A state whose exit condition is never met cannot be left.
- C: The current state is one visible value, so logging it shows the machine sitting in Hurt.
- D: Leaving at the end of the clip needs no extra flag.
- E: Conditions and parameters decide transitions; a clip supplies the pose over time.

**Source:** Stuck state; exit-time transition

## MA-ch11.10

The animation state machine has the states Idle, Run, Attack and Dodge, and no transition from Attack to Dodge is defined. A developer tells an agent: 'when the player presses Dodge, play the dodge animation'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A state is reachable when a path of defined transitions leads to it from the current state.
- [ ] B. A clip played directly, outside the machine, leaves the machine's recorded state unchanged, so the machine and the screen disagree.
- [ ] C. The engine adds the missing Attack-to-Dodge transition the first time Dodge is pressed.
- [ ] D. The sentence leaves open whether Dodge may cancel an attack, so the agent has to choose.
- [ ] E. A trigger or condition request for a state needs a defined transition, while a direct play call that forces a state skips transitions.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Reachability comes from transitions that were defined.
- B: A clip played outside the machine does not update the machine's current state.
- C: Engines do not invent transitions; missing ones are authored.
- D: Whether an attack can be cancelled is a rule the sentence does not state.
- E: Forcing a state skips transitions, as with Animator.Play in Unity.

**Source:** Impossible (missing) transition; forced state

## MA-ch11.11

An attack clip lasts 0.5 s and the player presses Attack five times in quick succession. Three input policies are named: an input lock (ignore presses while attacking), a restart (begin the attack again on each press) and an input buffer (remember one press and use it when the attack ends). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An input lock is the policy that remembers a press for later.
- [ ] B. An input lock discards presses that arrive while the attack is playing.
- [ ] C. An input buffer remembers a press made during the attack and starts the next attack when the first one ends.
- [ ] D. An input buffer discards the presses that arrive during the attack.
- [ ] E. A restart cuts off the swing in progress each time a new press arrives.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Remembering a press is buffering, not locking.
- B: A lock ignores input while the action runs.
- C: A buffer keeps a press and uses it when the action becomes available.
- D: A buffer keeps the press instead of discarding it.
- E: A restart replaces the running attack with a new one.

**Source:** Rapid input: lock, restart, buffer

## MA-ch11.12

A game uses an input buffer for Attack. The next attack becomes available at t = 0.50 s when recovery ends, and a press is remembered for 0.15 s. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A press whose window expires before the attack becomes available is dropped.
- [ ] B. Lengthening the buffer improves precision with no downside.
- [ ] C. An input buffer is the delay between the button press and the start of the animation.
- [ ] D. A press that arrives when the attack is already available is remembered until the window ends and then used.
- [ ] E. A press at 0.40 s is still remembered when the attack becomes available, so the next attack starts at 0.50 s.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: A press that expires early is lost.
- B: A long buffer queues presses the player did not mean and makes controls feel loose.
- C: That delay is input latency, a different idea.
- D: When the action is available the press is used at once; the buffer matters for early presses.
- E: The press at 0.40 s lasts until 0.55 s, past 0.50 s, so it is used then.

**Source:** Input buffer

## MA-ch11.13

A dash lasts 0.2 s and cannot be used again until 1.5 s after it starts. Check each statement that is true about the terms cooldown, animation lock and input buffer. Each statement is worth 1 point (5 points total).

- [ ] A. An animation lock blocks actions for a time that outlasts the animation.
- [ ] B. A cooldown is a minimum time between uses of an action and can last longer than the animation.
- [ ] C. A cooldown and an animation lock are the same thing.
- [ ] D. An input buffer can hold a press made shortly before the cooldown ends and use it when the dash is allowed again.
- [ ] E. A cooldown is the grace period after leaving the ground in which a jump is still accepted.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: A lock blocks action while the animation plays, so it ends with the animation.
- B: A cooldown is measured between uses and can run past the end of the clip.
- C: A cooldown restricts repeated use; a lock restricts action during playback.
- D: A buffer remembers an early press and uses it when the action is available.
- E: That describes coyote time.

**Source:** Cooldown versus animation lock versus buffer

## MA-ch11.14

Players complain that jumping 'does not work' when they press Jump a few milliseconds after running off a ledge, and when they press it just before landing. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Jump buffering remembers a press made shortly before landing and performs the jump on landing.
- [ ] B. Jump buffering is another name for coyote time.
- [ ] C. Coyote time is a brief grace period after leaving the ground in which a jump is still accepted.
- [ ] D. Coyote time is the delay between the button press and the jump animation.
- [ ] E. Both are input tolerance windows and leave the physics of the jump unchanged.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Jump buffering forgives an early press before landing.
- B: The two forgive opposite timing errors.
- C: Coyote time forgives a late press after the edge.
- D: Press-to-animation delay is input latency.
- E: They adjust when input is accepted and not how high or far the jump goes.

**Source:** Coyote time and jump buffering

## MA-ch11.15

A sword swing clip is 0.6 s long. The designer needs the hitbox on from 0.20 s to 0.35 s, a sound at 0.20 s, and a return to Idle when the clip ends. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An animation event is a call keyed at a time on the clip's timeline, which suits the hitbox and sound moments.
- [ ] B. Events are evaluated when the playhead passes their time during an update, so a frame at the exact time is not needed.
- [ ] C. A finished signal reports that a clip or state has ended, which suits the return to Idle.
- [ ] D. A code timer set to 0.20 s stays in step with the clip's events when playback speed is doubled.
- [ ] E. A property track in the clip can switch the hitbox's enabled property on and off.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Events run code at keyed times inside the clip.
- B: Events fire when the playhead passes them.
- C: Completion is signalled by a finished signal or an end-of-state transition.
- D: At double speed the clip reaches its 0.20 s mark early and a seconds timer fires late.
- E: A property track stores the timing inside the clip.

**Source:** Animation event, property track, finished signal

## MA-ch11.16

In a melee game the player's sword and an enemy both need collision shapes. A developer asks an agent for 'a collider on the sword and one on the enemy'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A hitbox is the attacker's damaging region, and a hurtbox is the defender's region that can receive damage.
- [ ] B. A hurtbox is a solid collider that physically stops the blade.
- [ ] C. The word 'collider' names neither which shape deals damage nor which receives it.
- [ ] D. Layers and masks make a body's own hitbox able to detect its own hurtbox.
- [ ] E. A hurtbox is the attacker's region that deals damage.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Hitbox is the dealing region and hurtbox is the receiving region.
- B: Both are normally detection shapes, such as areas, that report overlap without blocking.
- C: 'Collider' states neither role nor behaviour.
- D: Layers and masks are used to stop a body detecting its own boxes.
- E: That describes a hitbox.

**Source:** Hitbox versus hurtbox

## MA-ch11.17

An attack clip has three phases named startup, active and recovery. Its hitbox is on only in one of them. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Startup is the part of the attack before the hitbox turns on.
- [ ] B. Recovery is the part after the hitbox turns off, before the character is free to act.
- [ ] C. A hit list records the enemies already hit, so an overlap lasting several updates damages one enemy once per swing.
- [ ] D. Active is the phase in which the weapon is drawn back before the swing.
- [ ] E. Recording already-hit enemies means the hitbox switches off after its first overlap.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Startup is the lead-in before damage can happen.
- B: Recovery is the wind-down after the active window.
- C: Without a hit list, an overlap on several updates damages again on each update.
- D: That describes startup; active is when the hitbox is on.
- E: The hitbox can stay on for other enemies; the record only blocks repeat hits on the same one.

**Source:** Startup, active, recovery; hit list

## MA-ch11.18

A developer tells a coding agent: 'make the character animate when it moves'. The project has idle, walk, run and jump clips. Check each statement that is true about what the instruction leaves open. Each statement is worth 1 point (5 points total).

- [ ] A. The word 'moves' fixes an exact condition, so two agents would build the same machine.
- [ ] B. It leaves open the speed threshold at which walk gives way to run.
- [ ] C. It names the transitions between the clips.
- [ ] D. It leaves open whether each clip loops or plays once.
- [ ] E. It leaves open whether clips cross-fade or cut, and how long a cross-fade lasts.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: 'Moves' leaves thresholds, directions and priorities open.
- B: The walk-to-run threshold is a number the sentence does not give.
- C: The sentence lists no transitions at all.
- D: Loop mode against one-shot playback is a per-clip choice not stated.
- E: Blend behaviour and its length are not mentioned.

**Source:** Vague prompt: threshold, loop, cross-fade

## MA-ch11.19

A developer must tell a coding agent how four states (Idle, Run, Jump, Fall) connect. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A loop setting is a per-clip choice that needs its own line in the instruction.
- [ ] B. Naming the four states without conditions is enough, because the conditions follow from the names.
- [ ] C. A table with one row per transition (from state, to state, condition, cross-fade time) leaves the agent little to guess about which routes exist and when they fire.
- [ ] D. An arrow diagram shows which routes exist but not when they fire.
- [ ] E. An interrupt rule says which state may be cut short and by what.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Looping belongs to the clip, not the transition, and needs its own statement.
- B: A name such as Fall does not say whether the condition is velocity or floor contact.
- C: Each row fixes both ends, the trigger and the blend.
- D: Arrows show routes, not conditions or blend times.
- E: Interrupt rules are design decisions to state.

**Source:** Specifying transitions to an agent

## MA-ch11.20

A designer says: 'the attack can be cancelled into a dodge, but not into another attack, until its recovery phase starts'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Markers in clip time keep the window aligned with the visuals when playback speed changes.
- [ ] B. A timer in code measured in seconds keeps the window aligned when playback speed changes.
- [ ] C. An animation event can set a flag such as can_cancel that a transition condition reads.
- [ ] D. Recovery is the phase before the hitbox turns on.
- [ ] E. This describes a cancel window: a span of an action during which another action may interrupt it.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Clip-time markers scale with playback.
- B: Fixed seconds drift away from the visuals when speed changes.
- C: Events can set flags that conditions use to allow transitions.
- D: Recovery comes after the active phase.
- E: A cancel window is the portion of an action in which interruption is allowed.

**Source:** Cancel window

## MA-ch11.21

A project has a gameplay state machine in code. An agent asked to 'add an animation state machine' builds a second machine that tracks its own Idle, Move, Attack and Hurt states from the player's input. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A single source of truth means one machine, usually gameplay, is the authority and the other reads it.
- [ ] B. The animation machine should decide whether damage is dealt.
- [ ] C. Two machines fed the same input agree, because identical input gives identical states.
- [ ] D. The two machines can disagree, for example when gameplay says Hurt while animation is still in Attack.
- [ ] E. The animation machine should keep its own copy of gameplay state rather than read a parameter.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: One authority keeps picture and gameplay in agreement.
- B: Damage is a gameplay decision; animation presents state.
- C: Different rules and sampling give different states from the same input.
- D: Separate rules and timing let the two fall out of step.
- E: A copy can drift; reading a parameter keeps one source.

**Source:** Single source of truth

## MA-ch11.22

A team wants automated tests for a character's animation state machine. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A test that writes the state variable straight to the target tests the transitions.
- [ ] B. A test can check for dead ends, meaning states with no exit other than a deliberate end state.
- [ ] C. A passing state test shows that the motion looks and feels right to players.
- [ ] D. Because states and transitions can be listed, a test can try each listed transition and check that unlisted ones do not occur.
- [ ] E. A test can drive the real jump action and then read the current state.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Writing the state skips the transition logic being tested.
- B: A dead end is a property of the graph that a check can find without playing.
- C: Looks and feel need a person to watch and play.
- D: Enumerable transitions can be exercised one by one.
- E: Real input exercises the conditions that link input to state.

**Source:** Testing state machines: dead end, enumerable transitions

## MA-ch11.23

A teammate says a nested-if flag approach and a state machine are the same thing written differently. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. One boolean per state is the same thing as a state machine.
- [ ] B. In a state machine, transitions are decided by deeply nested if checks on flags.
- [ ] C. Nested conditionals make the current state one explicit named value.
- [ ] D. In a state machine, jumping, crouching and hurt can be active together by default.
- [ ] E. Independent flags can combine into undesigned situations, and a state machine lists the situations that were designed.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: Several booleans can be true at once, which a single current state excludes.
- B: Transitions are explicit routes guarded by conditions, not nested flag checks.
- C: With nested conditionals the state is implied by flag combinations, not named.
- D: A machine has one current state within a layer.
- E: Designed states are listed; flags allow combinations nobody designed.

**Source:** Undesigned flag combinations versus designed states

## MA-ch11.24

Four rewrites of a vague animation prompt are being compared. Check each statement that is true about whether the wording uses exact terms. Each statement is worth 1 point (5 points total).

- [ ] A. 'Go from Idle to Walk when speed is above 0.1, with a 0.1 s cross-fade' names a transition, a condition with a threshold and a blend time.
- [ ] B. 'Animate sensibly' specifies the states and their conditions.
- [ ] C. 'Loop walk and run, and play jump once' uses loop and one-shot correctly.
- [ ] D. 'Transitions not in this table do not exist' states that the table is the complete set of routes.
- [ ] E. 'Blend nicely between the clips' names a cross-fade time.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: It gives source, destination, a numeric condition and a blend duration.
- B: It names no states or conditions.
- C: Looping repeats a clip; one-shot plays it once.
- D: It closes the list of routes, so none are invented.
- E: 'Nicely' gives no number or duration.

**Source:** Rewrite a vague animation prompt with exact terms

## MA-ch11.25

A character has an animation tree: a ground state that holds a speed-driven blend space, plus Jump and Fall states. Check each statement that is true about the vocabulary. Each statement is worth 1 point (5 points total).

- [ ] A. A state machine is one possible part of the animation tree.
- [ ] B. The animation tree is the whole graph that plays clips through nodes such as state machines and blends.
- [ ] C. A ground state that contains a speed blend space is an example of nesting.
- [ ] D. Unity's Animator Controller plays a similar role to the animation tree in Godot.
- [ ] E. 'State machine' is a synonym for the whole animation tree.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: State machines, blend trees and blend spaces can all appear in a tree.
- B: The tree is the whole graph; nodes are parts of it.
- C: One kind of node can sit inside another.
- D: Animator Controller, like Unreal's Animation Blueprint, holds the graph that drives clips.
- E: A state machine is one kind of node, not the whole tree.

**Source:** Animation tree nesting and engine names

## MA-ch11.26

A jump animation intermittently stays in Fall after a quick land-and-jump, only on some runs. Check each statement that is true about the vocabulary of this fault. Each statement is worth 1 point (5 points total).

- [ ] A. A good test runs the sequence at both tick offsets within an update, with real input.
- [ ] B. If the landing and take-off ticks share one graph update, the graph does not see on-floor, and the landing is missed.
- [ ] C. An intermittent fault depends on certain timing and is absent on some runs.
- [ ] D. An event-driven fix has the movement code push the state change at the moment it happens, instead of waiting for the graph to poll.
- [ ] E. Intermittent means the fault lies in the clip data.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Running both offsets catches the unlucky timing.
- B: A sampled condition misses a state that comes and goes between reads.
- C: Intermittent means timing dependent.
- D: Pushing an event avoids reading the value late.
- E: The cause is sampling, not the clip.

**Source:** Intermittent fault, sampling, event-driven fix

## MA-ch11.27

A tester reports three bugs. Match each symptom to its name. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A character frozen in a pose is an impossible transition.
- [ ] B. Rapid input needs no policy, because the engine picks the right behaviour.
- [ ] C. Repeated presses that restart, stack up or get lost show a rapid-input problem.
- [ ] D. A character frozen in a pose because its exit condition stays false is a stuck state.
- [ ] E. A requested change with no defined route between the states is an impossible (missing) transition.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: A freeze points to a stuck state; an impossible transition concerns a missing route.
- B: A chosen policy such as lock, restart or buffer is needed.
- C: With no rule for presses during an action, the behaviour is accidental.
- D: A state with an unmet exit condition cannot be left.
- E: Reachability needs a defined route.

**Source:** Naming edge cases

## MA-ch11.28

Players say the game 'eats' their jump presses just before landing. Check each statement that is true about the fix. Each statement is worth 1 point (5 points total).

- [ ] A. A jump buffer is the fix for presses made shortly before landing.
- [ ] B. A longer animation lock is the fix for presses made shortly before landing.
- [ ] C. Coyote time is the fix for presses made shortly before landing.
- [ ] D. The length of the buffer window is a design value to state in the instruction.
- [ ] E. A cooldown is the fix for presses made shortly before landing.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: A buffer remembers the early press and uses it on landing.
- B: A lock blocks action and does not remember presses.
- C: Coyote time covers late presses after leaving ground.
- D: The window length changes the feel, so it should be stated.
- E: A cooldown limits repeated use and does not remember presses.

**Source:** Choosing buffer versus coyote time

## MA-ch11.29

A sword attack has a hitbox switched on and off by animation events. The attack can be interrupted partway. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Hitbox timing is best set by a fixed seconds timer in code.
- [ ] B. The instruction should give the active window in frames or clip time.
- [ ] C. Leaving or interrupting the attack state should also switch the hitbox off.
- [ ] D. If the attack is interrupted before the off event, the event may not fire and the hitbox stays on.
- [ ] E. A hit list is a record kept for each swing of the targets already damaged.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Seconds in code drift from the animation when speed changes.
- B: The active window should be stated in the clip's own time.
- C: Cleanup on exit keeps the hitbox from lingering.
- D: Events keyed after the interruption point do not run.
- E: A hit list stops repeat damage in one swing.

**Source:** Hitbox cleanup on interrupt

## MA-ch11.30

A developer writes: 'add an animation state machine that tracks its own states from the player's input'. Check each statement that is true about the wording. Each statement is worth 1 point (5 points total).

- [ ] A. 'Tracks its own states' creates a second authority that can disagree with gameplay.
- [ ] B. A better wording also says which transitions the animation machine has.
- [ ] C. 'Reads raw input' is the intended way for the animation machine to learn the state.
- [ ] D. Letting the animation machine decide whether damage is dealt is fine.
- [ ] E. A better wording says the animation machine reads gameplay state through a parameter.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Two machines can fall out of step.
- B: Naming the transitions removes guesses.
- C: Raw input is for gameplay code to interpret.
- D: Damage belongs to gameplay.
- E: A parameter carries state from the authority.

**Source:** Rewrite for single source of truth
