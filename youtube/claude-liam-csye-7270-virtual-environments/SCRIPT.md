# CSYE 7270: Virtual Environments and Real-Time 3D

Persona: Liam. Sources: supplied course text plus identified existing game evidence.

## B00 — A different job

Please use Walker to explain what I must understand when Claude Code builds my Godot game. That is the question behind C S Y E seventy-two seventy. I'm Liam, in for Professor Bear. This course is about directing and evaluating virtual environments, not collecting impressive-looking code you cannot explain.

## B01 — The thesis

The scarce skill is not typing. It is judgment. Claude can help produce the implementation. You must decide what the game is trying to do, recognize a plausible mistake, and explain why a revision is better. We will follow one small platformer from a vague request to evidence you can defend.

## B02 — Who does what?

Separate the roles. You supply the intent and acceptance criteria. Walker organizes the brief, build, playtest, inspection, revision, and export cycle. Claude Code proposes and edits code. Godot runs the interactive world. An agent's confident description is not a substitute for observing that world.

## B03 — Start from a baseline

Here is the actual Walker Jumpman starter, before a student's extension. This is an archived frame from the existing project, not a proposed redesign. Establish that baseline first. If you never observe the original controls and level, you will not know whether your changes preserved them.

## B04 — An engine, not a chatbot

Godot supplies nodes, scenes, rendering, physics, and the running game. G D Script connects those pieces with behavior. The course uses the regular Godot engine. The starter does not require C sharp or the dot net edition. Claude Code is the coding assistant; it is not the engine.

## B05 — The production loop

The Walker loop has six moves: game brief, build, playtest, inspect, revise, export. Notice where inspection sits. Playing reveals an observation; inspection traces its cause; revision changes the cause. Export packages a version. It does not retroactively prove that the version was good.

## B06 — Check access early

These exercises assume working Claude Code access through the course's Northeastern arrangements. Check that access early and contact the instructor if it fails. Separate A P I credits are not a starter prerequisite. Install the course-specified Godot version, then open the starter's project file rather than creating an unrelated empty project.

## B07 — Five supervisory capacities

The course names five supervisory capacities. Plausibility auditing asks whether the result makes sense. Problem formulation defines the task. Tool orchestration orders the work. Interpretive judgment gives the result game-specific meaning. Executive integration keeps the session aimed at one goal. These are the course's vocabulary for supervision, not five buttons in Godot.

## B08 — PF · Define the task

Problem formulation begins before prompting. Make the character better is not a specification. Give the character a distinct silhouette while preserving movement speed and collision behavior is closer. Name one concern, an invariant you will preserve, and the files or systems the agent must leave alone.

## B09 — TO · Sequence the work

Tool orchestration is about dependencies. Inspect the existing player first. Change its visual identity next. Check the silhouette in motion. Only then extend the level in a separate change. If art, physics, camera behavior, and geometry all move together, a regression has too many possible causes.

## B10 — PA · Hear the wrong note

Plausibility auditing starts with a specific suspicion. This archived jump frame tells us where the visible character was. It does not prove that every landing works. A new sprite could look centered while its collision shape stays elsewhere. Ask what observation would reveal that mismatch, then test it.

## B11 — IJ · Judge the experience

Interpretive judgment supplies the meaning of a result. A collision test can report contact. It cannot decide for your audience whether the landing feels fair or the character reads clearly against the background. Use machine checks as evidence. Make the design judgment yourself, and explain the tradeoff you accepted.

## B12 — EI · Keep one goal

Executive integration prevents the session from drifting. The assignment is to change a character and extend a playable level. A proposed inventory system might be clever and completely irrelevant. Keep the brief visible, record deferred ideas, and judge each new task against the goal instead of the agent's enthusiasm.

## B13 — Read the ownership map

Now inspect the real starter. Player drawing and movement live in the player script. Level geometry comes from a data file. The session script builds and manages the running world. That ownership map tells you where to ask for a change and where to look when the result surprises you.

## B14 — Changing the character

The first change is a new character identity, not just a new color. Use the baseline as a comparison reference. A student might change the silhouette, face, or accessories while preserving the movement contract. That redesigned character is proposed work here. This film is not presenting an unbuilt student solution as finished gameplay.

## B15 — The hidden rectangle

In this source snapshot, the player's collision rectangle is eighteen by twenty-eight game units. The drawing is a separate concern. Our schematic enlarges both so you can see the difference. Changing the art does not automatically change the collider. If you intentionally change collision, update the specification and the tests too.

## B16 — Extending the level

For the first assignment, add at least two new jump-and-landing opportunities and relocate the finish to the new end. More floor is not automatically more play. Show the route, explain the choices it asks of the player, and preserve a reachable start-to-finish experience.

## B17 — A finish screen is narrow evidence

This archived completion frame came from scripted input. It demonstrates one successful route in the recorded build. It is not a human playtest, not a measurement of enjoyment, and not evidence about your future extension. Preserve that distinction when you describe tests in your own submission.

## B18 — Trace the dangerous middle

A larger level affects more than one visible platform. The finish position, camera limits, resource references, and runtime behavior may depend on other values. The course calls this the dangerous middle. Follow the dependency links. Do not approve a change merely because the file you edited looks reasonable.

## B19 — Make the claim falsifiable

Before the next build, write a prediction that can fail. After extending the level, I can land on both new platforms, reach the new finish, die, and restart at the original spawn. Record the observed result for each part. A claim becomes useful when you know what would contradict it.

## B20 — A controlled revision

Suppose the second new landing fails. That is a constructed teaching example, not a new test run. Compare the geometry with the movement you promised to preserve. Adjust one cause, rerun the failing case, then repeat the baseline checks. Quietly weakening the test would hide the problem instead of fixing it.

## B21 — Week 2 · Prompted art

In week two, the same supervisory pattern moves to game art. Use tools you can access, compare candidates, record prompts and provenance, and inspect the imported result at game scale. A beautiful isolated image can become an unreadable character. A paid image subscription is not the learning objective.

## B22 — Week 3 · Blender to Godot

Week three adds Blender through the community Blender M C P integration. A generated mesh is an intermediate artifact. Inspect its geometry, scale, materials, and exported form, then verify it inside Godot. A correct-looking Blender viewport does not prove that the imported asset behaves correctly in the game.

## B23 — Weeks 4–8 · Behavior and appearance

The middle of the course connects scenes, collision, and physics to the game design document, then to shaders and materials. Specify what should happen before asking for code. A shader compiling establishes one kind of conformance. Compare controlled inputs and visible output before calling its appearance correct.

## B24 — Weeks 9–12 · Time matters

Particles, animation, interaction, and audio unfold over time. A still screenshot cannot show whether an effect starts too early, an animation transition pops, or a sound repeats after restart. Trace the event, the state change, and the visible or audible response. Then test that sequence in the running scene.

## B25 — Weeks 13–15 · Evidence and integration

Later work adds profiling, analytics, navigation, behavior trees, procedural content, and appropriately scoped networking, mobile, or extended-reality constraints. These are still Walker and Godot problems. Measure a baseline, justify a focused change, and integrate the result into projects you can reproduce and defend.

## B26 — Two clocks, not one

Modules map one-to-one to companion-book chapters, released one or two per week. Assignments follow a separate clock: one hundred points every ten days. There is an individual project and a group project. Canvas supplies the deadlines and project milestones; this overview does not invent dates or project weightings.

## B27 — Play, then explain

Every assignment also includes a Brutalist Godot explainer. Use a walkthrough to show behavior, a game-development explainer to connect it to implementation, or a game-design-document explainer when that is the assignment's focus. Selected films become class discussion material. Narration should explain actual evidence, not promise footage you never recorded.

## B28 — The learning loop

Predict, build it, use it, ship it, verify. Predict the result before prompting. Build one focused change. Use it in the game. Ship a reproducible version and explanation. Verify the claims against evidence. This learning loop and Walker's production loop reinforce each other; neither means press generate and trust the result.

## B29 — Show the division of labor

In your sources and Frictional log, name what you contributed and what the A I contributed. Include the wrong turns, the evidence that changed your mind, and what remains unverified. The GitHub version and the Canvas submission must match. A polished film cannot replace an honest account of the work.

## B30 — Do not confuse recovery with quality

A failed run can teach more than a confident summary. Here the archive captures the starter's failure state. In your own work, inspect what triggered failure and whether recovery behaves as specified. Then ask the human question: does this teach the player fairly, or merely satisfy a machine check?

## B31 — The responsibility boundary

The agent can help propose acceptance tests, analyze traces, and suggest revisions. Those are useful contributions. It still does not inherit your responsibility for choosing the goal or defending the result. Conformance asks whether the system meets stated checks. Adequacy asks whether those checks and that experience serve the intended player.

## B32 — The verdict

The verdict: this is a course in supervising interactive systems. Learn the subsystems well enough to specify behavior and catch plausible errors. Use Claude Code to accelerate implementation. Use Godot to observe the result. Use the five capacities to explain the decisions that no generated code listing can make for you.

## B33 — Your turn

Your turn. Please use Walker to inspect Jumpman, preserve its movement, and propose a new character and two new landings. Start with that prompt, then review the proposed changes before accepting them. Your evidence should show the baseline, the extension, a failure and restart, and one revision you can explain.

## B34 — Outro

[Regular outro jingle; no narration.]
