# Chapter 5: Game design documents and virtual worlds

## MA-ch05.1

A team talks about its documents before building a 2D platformer. The words pitch, brief, GDD and pillar get mixed up. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A design pillar is a planned feature in the backlog, such as double jump.
- [ ] B. A GDD is the source code of the mechanics written in prose, so editing the document edits the game.
- [ ] C. A GDD is frozen at the start of production so playtest findings do not change it.
- [ ] D. A pitch or brief states the core idea and scope in short form, and the GDD develops those decisions in detail.
- [ ] E. A game design document (GDD) records what the game is and how it should behave, in enough detail for builders and testers to work from.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: A pillar is a short statement of the intended experience, not a feature.
- B: A GDD describes intended behaviour; code is the implementation.
- C: A GDD is revised as prototypes and playtests teach the team; an unrevised one becomes stale.
- D: The brief is the compact form; the GDD is the detailed one.
- E: A GDD is the detailed shared description of intended behaviour.

**Source:** GDD, brief, pillar

## MA-ch05.2

A team has the design pillars "fast restarts", "readable danger" and "one-button depth". Late in development someone proposes a 30-second unskippable cutscene after each death. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Make the game fun" works well as a pillar because it excludes no feature.
- [ ] B. The cutscene conflicts with the pillar "fast restarts", so the pillar gives grounds to reject or change it.
- [ ] C. "Enemies flash 0.4 s before an attack lands" is a requirement, because a test can check it.
- [ ] D. A feature list and a set of pillars are the same document under two names.
- [ ] E. A design pillar is a short statement of the experience the game aims to deliver, used to judge proposed features.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A pillar that excludes nothing settles no decision.
- B: A pillar is used to test a proposal against the intended experience.
- C: A requirement states something checkable; a pillar guides judgement.
- D: A feature list names things to build; pillars name the experience.
- E: Pillars are a decision tool.

**Source:** Design pillars versus requirements

## MA-ch05.3

In a roguelike the player enters a room, fights, picks up a reward and enters the next room. When a run ends, the player spends currency on permanent upgrades and starts a new run. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The engine's game loop (read input, update, draw each frame) is the same thing as the core loop.
- [ ] B. The core loop is the short cycle of player actions repeated most often, here enter, fight and collect.
- [ ] C. A loop in the design sense has an action, an outcome and feedback that leads into the next action.
- [ ] D. Spending currency between runs belongs to a meta loop (progression loop) wrapped around the core loop.
- [ ] E. The core loop is a list of features grouped by importance and by the team that builds each.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: The game loop is a programming construct; the core loop is a design term about what the player repeats.
- B: The core loop is the moment-to-moment cycle the rest of the game is built around.
- C: Feedback closes the cycle and motivates repeating it.
- D: Loops nest: a longer progression loop surrounds the short core loop.
- E: A feature list is not a repeated cycle.

**Source:** Core loop versus game loop, meta loop

## MA-ch05.4

Two requirements arrive for one game. One says "The player can interact with the world." The other says "The player can jump, dash and grapple." A player verb is an action the player chooses to perform. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Jump, dash and grapple are player verbs.
- [ ] B. A verb is buildable once it has a name; the input, the effect and the feedback can be left to the agent.
- [ ] C. "Interact" is a vague verb, since it names no input, target or change of state.
- [ ] D. A genre fixes the verbs, so choosing a verb list is a label and not a design decision.
- [ ] E. Health regeneration is a player verb because it affects the outcome.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: The player chooses when to perform each.
- B: A buildable verb states its input, its rule for what changes, and the feedback the player perceives.
- C: A coding agent cannot tell what to build from it.
- D: Choosing and limiting verbs is a central design choice.
- E: The player does not choose it; it is a system rule.

**Source:** Player verbs

## MA-ch05.5

The MDA framework separates mechanics (rules and systems the designer builds), dynamics (behaviour that emerges when players use the rules) and aesthetics (the emotional responses of players). A designer adds a rule to a shooter: the player carries at most 12 rounds. Players start hoarding rounds and avoiding fights, and report feeling tense. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A dynamic can be read off the rule text, so a playtest adds no information about it.
- [ ] B. The 12-round limit is a mechanic.
- [ ] C. Hoarding rounds and avoiding fights is a dynamic.
- [ ] D. The designer sets an aesthetic directly by writing the feeling into the rules.
- [ ] E. Tension is an aesthetic.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Dynamics appear when players meet the rules, so they are found by observing play.
- B: It is a rule the designer wrote.
- C: It emerges from players meeting the rule and is not a line in the rules.
- D: Aesthetics are players' responses; the designer can only shape rules that tend to produce them.
- E: Aesthetics are the felt experience.

**Source:** Mechanics, dynamics and aesthetics

## MA-ch05.6

A designer wants a stealth meter that fills while an enemy can see the player. Sort what is built from what emerges using mechanic, dynamic and aesthetic. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Players waiting at cover for a patrol gap is an aesthetic.
- [ ] B. Players rushing between blind spots is a mechanic because the player performs it.
- [ ] C. The rule "the meter fills at a set rate while seen and drains when unseen" is a mechanic.
- [ ] D. The satisfaction of slipping past a guard is a dynamic.
- [ ] E. A fill rate per second and the threshold at which enemies attack are parameters of the mechanic, and a test can check them.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: That is behaviour that emerges, so it is a dynamic.
- B: Emergent player behaviour is a dynamic; the mechanic is the rule that makes it worthwhile.
- C: It is a rule the designer builds.
- D: A felt response is an aesthetic.
- E: Numbers and observable results make a mechanic buildable and checkable.

**Source:** Classifying with MDA

## MA-ch05.7

A team plans three builds: a weekend build of the core mechanic with placeholder boxes, a vertical slice, and a minimum viable product (MVP). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A minimum viable product (MVP) is the smallest complete game that can be released to real players.
- [ ] B. A vertical slice is a thin portion of the game built to near-final quality across art, audio, UI and rules.
- [ ] C. A prototype is a quick build made to answer a design question, and may be thrown away.
- [ ] D. A prototype needs final art and audio, otherwise testers can not judge the mechanic.
- [ ] E. A vertical slice is a rough version of the whole game with the full set of levels present but unpolished.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: It has the minimum feature set but is complete and releasable.
- B: Slice means deep, not wide.
- C: Prototypes are tools for learning, not products.
- D: Placeholder art is normal for a prototype.
- E: That describes a horizontal pass.

**Source:** Prototype, vertical slice, MVP

## MA-ch05.8

A studio pitches a 2D stealth puzzle game with thirty levels. Match each build to its term. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Adding the long-term feature roadmap to an MVP keeps it minimum.
- [ ] B. One finished level with final art, sound, UI and saving, built to show the whole game can reach that standard, is a vertical slice.
- [ ] C. One room with a guard and a hiding spot built from placeholder boxes, to ask whether hiding is fun, is a prototype.
- [ ] D. Polishing a prototype's art before its design question is answered mixes up prototype and vertical slice, and delays learning.
- [ ] E. A handful of levels with menus and saving, released to test whether players want the game, is a vertical slice.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Adding roadmap features grows the scope beyond minimum.
- B: A slice shows near-final quality across disciplines.
- C: It tests one design question.
- D: Confusing the builds spends effort on the wrong question.
- E: That is an MVP.

**Source:** Matching builds to terms

## MA-ch05.9

Four weeks before a deadline a team has one working level, and a teammate proposes online co-op, a crafting system and ten new enemy types. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An out-of-scope list records non-goals already decided, so a proposal for one is declined without a new argument.
- [ ] B. Scope is the set of features and content a team commits to deliver by a date.
- [ ] C. Small additions are not scope creep, because a small feature adds no schedule cost.
- [ ] D. Scope, schedule and quality trade against each other, so cutting a feature is a lever for protecting the date.
- [ ] E. Scope creep is growth of that commitment without a matching change in time or resources.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: A written non-goal turns a repeated argument into a settled decision.
- B: Scope is a commitment tied to a date.
- C: Small additions add up, and each needs design, building and testing.
- D: Cutting is a legitimate trade.
- E: Creep is uncontrolled growth.

**Source:** Scope and scope creep

## MA-ch05.10

Three weeks before a deadline a team is offered online leaderboards, a branching story with cutscenes, and generated levels. The lead names four responses: cut, defer, swap and move the date. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Cutting removes a feature from the commitment to protect the date.
- [ ] B. Swapping accepts a new feature and removes one of equal cost.
- [ ] C. Accepting a new feature while keeping the date and the other features unchanged is a trade, not creep.
- [ ] D. Deferring deletes the idea from the design for good.
- [ ] E. An estimate of cost is made after a proposal is accepted.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Cut is the lever that reduces scope.
- B: A swap keeps the total commitment the same.
- C: Accepting without a trade is scope creep.
- D: Deferring moves it to later, so a rejected idea can become a post-release candidate.
- E: Each proposal gets a cost estimate before the decision.

**Source:** Scope levers: cut, defer, swap

## MA-ch05.11

A studio has a level designer and a worldbuilder. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A world map is a level, because worldbuilding is level design at a larger scale.
- [ ] B. Level design arranges space, obstacles, enemies and pacing so the player's verbs are tested in sequence.
- [ ] C. Drawing the tile layout of the first level counts as finishing the worldbuilding.
- [ ] D. Worldbuilding establishes the setting: places, history, rules and cultures.
- [ ] E. An abstract puzzle room with no lore can still be a well-designed level.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: A map describes the setting; a level is playable.
- B: A level is a playable arrangement.
- C: A tile layout is level work; the setting can remain undefined.
- D: Setting can inform levels without being a layout.
- E: Level quality rests on verbs, pacing and teaching.

**Source:** Level design versus worldbuilding

## MA-ch05.12

A team writes acceptance criteria in the given-when-then form. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A tolerance such as within 4 px states how far a measured value may differ and still pass.
- [ ] B. In a given-when-then criterion, "given" states the starting situation.
- [ ] C. "Then the player feels a satisfying response" is a valid then clause, because it states the outcome.
- [ ] D. "When" names the action or trigger, and "then" names an observable result.
- [ ] E. A time limit such as within 0.1 s turns "responds quickly" into something checkable.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: A tolerance defines what counts as a pass.
- B: It fixes the state before the action.
- C: A feeling is a judgement, not an observable result.
- D: The result must be observable.
- E: A stated limit replaces a vague adjective.

**Source:** Given-when-then criteria

## MA-ch05.13

A designer tells a coding agent: "The jump should feel snappy and reach a good height." With 32 px tiles, the intent is a rise of 96 px from the floor. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "The highest point is 96 px above the starting height" names a quantity and a unit.
- [ ] B. Adding "and the jump should be fun" makes the criterion more testable.
- [ ] C. A starting state, such as the player standing on the floor, belongs in the criterion.
- [ ] D. "Snappy" is a subjective adjective, so a stranger can not turn it into a pass or fail test.
- [ ] E. A tolerance such as 4 px is needed, since discrete physics steps seldom land the apex on exactly 96 px.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Quantity and unit remove guessing.
- B: It adds a judgement no automated test decides.
- C: The same input gives a different jump from the air.
- D: A test needs a quantity, not a feeling.
- E: A tolerance absorbs step size.

**Source:** Vague adjective versus quantity

## MA-ch05.14

Two instructions are given for a shield pickup. X: "Add a Timer node named ShieldTimer set to 3.0 s, store the state in a boolean called shielded, and connect area_entered in code." Y: "After the player touches a shield pickup, enemy contact deals no damage for 3.0 s; a second pickup restarts the 3.0 s." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Instruction X is a specification, because it names exact nodes and variables.
- [ ] B. A test written from behaviour Y stays valid after the implementation is rewritten (refactored).
- [ ] C. Reading the code recovers what the designer intended, because the code is the final design.
- [ ] D. An implementation names the mechanism, such as nodes, variables and signals.
- [ ] E. A specification states observable behaviour that has to hold.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Naming mechanisms does not state behaviour, so no test can be written from it.
- B: Behavioural tests survive changes of mechanism.
- C: Code shows what the game does, not what it was meant to do.
- D: X is implementation detail.
- E: Y is a specification.

**Source:** Specification versus implementation

## MA-ch05.15

A developer instructs a coding agent: "Add a double jump. Do not change run speed, gravity or the camera. Edit only player.gd and a new test file. If a criterion cannot be met, stop and report which one instead of loosening it." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An invariant is something that stays true after the change, such as run speed staying unchanged.
- [ ] B. Naming the files the agent may edit limits the change surface to something a reviewer can read in full.
- [ ] C. "Loosening" a criterion means making it easier to pass, and stopping to report guards against a false pass.
- [ ] D. Invariants make a requirement untestable, because they add conditions beyond the feature.
- [ ] E. Invariants are implementation detail that belongs in code comments, not in the instruction.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Invariants fence off existing behaviour.
- B: A small surface is easier to review.
- C: Weakening a criterion or test is the easy route to a false pass.
- D: Invariants make it more testable, since existing behaviour can be re-checked.
- E: They are requirements on the work and bind the agent only if stated.

**Source:** Invariants and change surface

## MA-ch05.16

A coding agent reports: "Shield pickup finished; all tests pass." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A playtest replaces automated tests, because people notice rare exact-timing errors.
- [ ] B. Passing tests that check reachability of a level exit show the level is fair.
- [ ] C. A playtest shows whether players notice, understand and enjoy the shield.
- [ ] D. An automated test checks stated conditions, such as the shield lasting 180 physics ticks, and can be rerun.
- [ ] E. Passing tests show the shield feature is fun, since the tests were written from the design.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: People miss rare exact-timing cases that scripted tests catch.
- B: Passing tests establish only the conditions they check.
- C: Comprehension and enjoyment need people.
- D: Repeatable exact checks are what automation offers.
- E: A test checks stated conditions, not enjoyment.

**Source:** Playtest versus automated test

## MA-ch05.17

A coding agent says its tests pass. A reviewer wants to check the tests themselves. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Can the player say what the goal was without being told?" is a good automated criterion.
- [ ] B. A test needs no stated starting state, since the test finds its own.
- [ ] C. A test that passes on a broken build gives a false pass.
- [ ] D. Breaking the feature on purpose and confirming the test fails shows the test measures what it claims.
- [ ] E. Passing tests establish just the specific conditions they check.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: It is a playtest question, since it needs a person.
- B: A test needs a defined starting state to be repeatable.
- C: A false pass hides a defect.
- D: A test that still passes on a broken build is not measuring the feature.
- E: They do not cover fun, readability or fairness.

**Source:** Testing the tests

## MA-ch05.18

A designer writes to a coding agent: "Make the boss hard." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Multiplying the boss health by ten is the plain reading of "hard".
- [ ] B. Adjectives such as "hard" belong in acceptance criteria because the team shares an understanding.
- [ ] C. A threshold test can show that players find the boss hard enough.
- [ ] D. "Hard" is a judgement, so it becomes parameters and is confirmed by playtesting.
- [ ] E. "Attack interval 1.2 s, damage 2 of 5 hearts, 0.4 s wind-up" is still too vague to test.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: Hard could mean fast, accurate, numerous or punishing.
- B: A shared understanding is not a stranger-testable criterion.
- C: A test confirms numbers; only players say whether the result is hard.
- D: Parameters can be built and tested; the judgement is confirmed with players.
- E: It gives quantities and times a test can read.

**Source:** Judgement versus parameter

## MA-ch05.19

A requirement for a checkpoint reads: "When the player reaches the checkpoint flag, dying should send them back there." The precise instruction adds details. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Invariants, such as existing movement and existing tests still passing, are stated in the instruction.
- [ ] B. "Reaches the flag" is stated as an observable event, such as the player's body entering a trigger region.
- [ ] C. Reaching a state by real input exercises the whole path; writing the state directly tests just the step checked, so the instruction says which is used.
- [ ] D. A rule for re-entering the flag can be left out because the sentence defines the behaviour.
- [ ] E. "Back there" is given a location with a unit and a tolerance, such as within 8 px of a named respawn marker.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: They protect behaviour the change should leave alone.
- B: A vague verb becomes an observable event.
- C: A direct write is a shortcut that skips part of the path.
- D: Repeat entry is an edge case that an unstated rule leaves to chance.
- E: A location without a tolerance is not testable.

**Source:** Writing a precise requirement

## MA-ch05.20

Rewriting "The checkpoint should reset the player quickly" for a stranger who tests it. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A physics tick is one fixed-step update of the physics simulation.
- [ ] B. A limit of 120 frames lasts the same real time at 60 and 144 frames per second.
- [ ] C. A limit of 0.5 s is fully specified even if the clock it is measured on is left unstated.
- [ ] D. A test that writes game state directly is labelled as a shortcut in the criterion.
- [ ] E. "Quickly" is an imprecise word; "within 2 physics ticks" is a time limit with a stated basis.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Ticks run at a fixed rate, unlike rendered frames.
- B: A frame count changes duration with the frame rate.
- C: The basis, such as a tick rate, needs stating.
- D: Labelling it shows what part of the path is not exercised.
- E: A limit needs a basis such as ticks or seconds at a stated rate.

**Source:** Time basis and state setup

## MA-ch05.21

A shield should protect the player for 3.0 s after a pickup. The specification needs edge cases. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Expiry while an enemy overlaps is not an edge case, because it is rare.
- [ ] B. A file the agent may edit replaces the behaviour statement, since both constrain the work.
- [ ] C. An edge case is a situation at the boundary of the normal rule, such as a second pickup during the window.
- [ ] D. The 3.0 s is made measurable with a tolerance or a tick count.
- [ ] E. If the specification is silent on a second pickup, the agent's choice is as good as another.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Rare boundary situations are exactly where edge cases arise.
- B: Implementation constraints sit beside the behaviour, not in place of it.
- C: Edge cases are where unstated rules cause disagreement.
- D: A bare duration leaves room for disagreement.
- E: An unstated rule is left to chance; restart, extend or ignore should be stated.

**Source:** Edge cases in a specification

## MA-ch05.22

A team on a desktop computer scopes a touch version and a networked version of its game. It has no phone and no second machine. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Two copies on one computer talking over loopback show behaviour under internet latency and packet loss.
- [ ] B. A feature that can not be verified on the available hardware is marked unverified in the scoping note.
- [ ] C. A desktop headset simulator proves the movement is comfortable in virtual reality.
- [ ] D. Mouse-emulated touch shows the game feels right on a phone's screen.
- [ ] E. Code existing for a platform is evidence that the feature works on the target.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: Loopback has no real network distance, loss or latency.
- B: Marking it keeps the gap visible.
- C: Comfort depends on the real device and the person wearing it.
- D: Emulation tests event handling, not real hands and screen.
- E: Working on the target is shown by running there.

**Source:** Scoping platforms honestly
