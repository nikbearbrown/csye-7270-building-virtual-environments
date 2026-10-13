# Preface — Conducting AI Through Games and Virtual Worlds

## Executive summary

Building a game makes Conducting AI tangible. An agent can help produce sophisticated code, model geometry, connect systems and run checks; a person must decide what experience is worth creating and whether the result serves it. Games make that distinction unusually visible because they combine engineering with art, fun, frustration, taste and opinion. You can have a technically functioning game that nobody wants to play. This course teaches you to direct AI toward an intended experience, gather evidence, play the result and make a defensible decision about what happens next. The preface comes before the toolchain module because knowing what you are responsible for comes before learning which command to run.

## A working game can still be the wrong game

Imagine a platform game with a new character. The image imports. The animation plays. The player moves, jumps and lands. A script completes the level. The automated checks pass. Then you pick up the controls.

The character disappears into the background. Its wide coat seems to touch a hazard before the game registers a collision. A landing effect hides the edge of the next platform. The jump is consistent, but it feels heavy when you wanted something quick and playful. These are illustrative possibilities, not a report of a new playtest. They show the kind of question this course asks: which part of the intended experience did the technical checks establish, and which part still needs investigation?

There is real engineering in making any of those systems work. There is also real work in deciding that they belong together. A program's correctness depends on its specification; the specification's adequacy depends on the purpose and people it serves. The person directing the game must attend to both.

Games make this visible in a few seconds. You can watch a beautiful effect and immediately find it distracting. You can play a technically simple game and want another turn. Complexity, polish and enjoyment are different properties. None should silently stand in for the others.

## The conductor chooses and directs

A film director need not personally operate every camera, act every part, record every voice or build every effect. The director makes decisions about what those contributions should produce together. An orchestra conductor does not play all the instruments. The work is choosing an interpretation, coordinating the parts, hearing what needs attention and directing a revision.

Conducting AI applies that division of work to engineering. You choose the problem, the audience, the constraints and the grounds for accepting the result. AI helps produce the implementation and evidence. You inspect the work, revise the direction when necessary and remain responsible for the outcome.

The measure of your contribution is not how many lines you typed. It is the quality of your decisions and what those decisions make possible. You still need technical understanding. If you cannot explain what a collision shape is, you will have difficulty recognizing why a character appears to hit an obstacle without the game detecting it. Delegating the typing gives you a different reason to learn the machinery: to direct it and recognize consequential mistakes.

This course uses five capacities from Professor Bear's Conducting AI framework:

| Capacity | What it looks like while building a game |
|---|---|
| Problem formulation | Decide who the game is for and what the player should experience; turn that intention into a bounded task. |
| Plausibility auditing | Notice that a claim sounds wrong or unsupported, then investigate it rather than trusting the feeling alone. |
| Tool orchestration | Choose which work belongs in the coding agent, Blender, the engine, a test or a human playtest; define the handoff. |
| Interpretive judgment | Explain what the result means for this game and these players. |
| Executive integration | Reconsider the whole design when an art, physics, performance or audience decision changes another part. |

A suspicion starts an investigation. It does not finish one. Human judgment can be mistaken, and the conductor must be willing to revise a favorite idea when use, measurement or player feedback contradicts it.

## Why games make the argument visceral

Consider character generation. Suppose you ask for fifty variants, then another fifty. The numbers describe a hypothetical exercise, not a promise about a particular tool. Producing more candidates increases the selection work. It does not settle the choice.

A face that looks excellent in a large portrait may become unreadable at game size. A silhouette that you like in isolation may blend into the level. A costume may suggest a genre or personality that conflicts with the story. A character may satisfy the brief and still be one you do not want to spend time with.

You can ask AI to organize alternatives, identify inconsistencies or compare them against explicit criteria. That assistance is useful. The ranking remains a proposal. You choose the criteria, decide whose responses matter and observe what happens in the actual scene. Your preference is part of the design, but your preference is not evidence that every intended player agrees.

The same division appears in gameplay. An agent can implement a jump, expose its parameters and run a route through a level. You must still decide whether the jump expresses the experience you intend. A hard jump might be satisfying in a precision platformer and inappropriate in a relaxed exploration game. The parameter cannot answer the design question without the context.

Games are therefore a particularly direct way to learn a principle that extends to all engineering: producing the artifact and deciding what makes it good are connected responsibilities. Good code matters. So do the purposes, values and experiences that make the code worth running.

## What AI evaluation can establish

Saying that AI cannot evaluate a game needs precision. The course's existing examples include agents writing tests, inspecting source, measuring state and running scripted interactions. These can establish useful facts. An automated route through a level is a form of testing; it is not a report of a person's enjoyment.

Keep three kinds of evidence distinct:

| Question | Useful evidence | What remains open |
|---|---|---|
| Does the implementation meet this explicit rule? | A test with appropriate inputs and assertions, plus inspection of what actually ran. | Whether the rule captures the intended design. |
| Does the artifact behave as expected in use? | A running build, visible output, audible output and observations under stated conditions. | How different players or devices may experience it. |
| Is this the experience we want to offer? | Human play, interpretation, feedback and a reasoned design decision. | Disagreement, uncertainty and the need for further revision. |

AI can contribute to the first two and help organize evidence for the third. It does not supply your lived response, the actual feedback of people who have not tried the game, or your authority to accept the tradeoff. Asking the agent to invent a playtest report replaces missing evidence with a story.

The course's own records make this distinction concrete. The toolchain chapter records agents misreading a regression test. The physics chapter records a shield test that did not detect a deliberately shortened duration. The materials chapter records an ambient-occlusion change whose checks missed a disabled setting. These are historical course examples, linked in the sources below. None establishes that a human has judged the final appearance or feel.

## Computational Skepticism gives doubt a job

Computational Skepticism asks: how do we know the output is correct for the claim we are making? In game development, a useful answer often requires using the thing. Play the level. Listen to the cue. Look at the character while it moves. Check the supposed collision. Try the input that would expose the failure.

Before delegating, write one observation that would count against the agent's eventual success claim. For a shield, that might be damage occurring before the promised duration expires. For an audio cue, it might be silence when the intended event occurs. For character readability, it might be losing track of the player against the actual background.

The check must be capable of disagreeing with the implementation. If the agent implements a duration and then reads that same value to decide what the duration should be, both can share the wrong assumption. Compare behavior with the intended rule. Sometimes the implementation is wrong. Sometimes the test is wrong. Sometimes the original rule needs a human revision. Keep those possibilities separate.

When you cannot check something, mark it pending. This is useful engineering information. It tells the next person what remains to be established and prevents an attractive demonstration from becoming a broader claim than the evidence supports.

## Irreducibly Human names the contribution you retain

Professor Bear's Irreducibly Human framework argues that exceptional pattern production does not constitute the whole intelligence needed to direct a project. Its Tier One covers pattern and association: a place where AI can be extremely capable at producing code, alternatives and analyses. The course draws on the framework's wider attention to embodied experience, social understanding, supervision, causal judgment, collective deliberation and purposes.

The practical distinction is visible when you play. You bring your attention, fatigue, expectations, history with other games and reactions to what happens. Other players bring different experiences. A generated account of those reactions does not establish that those people had them.

You also retain authority over the purpose. Should the game reward speed or exploration? Should failure punish the player or invite experimentation? Which compromises are acceptable for accessibility, performance or visual expression? These questions need reasons and evidence, but the evidence does not appoint the decision-maker.

The framework's strongest claims about structural limits are philosophical arguments, not a scientific result established by this preface. You can debate those claims while practicing the operational rule: let AI perform suitable technical work, inspect its evidence, bring actual human experience into the process and remain accountable for acceptance.

## Why Godot

The primary reason for choosing Godot here is the direct workflow between a coding agent and an inspectable project. Claude Code can work on the course's GDScript and text scene files, and the Godot command line can import, run and check the project. That path does not require an MCP bridge. The official [command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) and [text scene format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) document the underlying facilities.

For this course, the benefit is pedagogical: you can follow a change from the human brief to a file diff, then to engine behavior and a playtest. There are fewer integration steps in that chosen path between asking for a bounded code change and inspecting what the agent actually changed. This is a course-design judgment, not a benchmark claiming that Godot is the best engine for every project.

MCP means Model Context Protocol, a way for an agent to call tools exposed by another program. It can provide valuable access to a running editor. The course does not depend on its presence or absence in Godot's wider ecosystem; the required Godot workflow simply does not need it.

As checked on October 12, 2026, Unity's [May 11 introduction to its MCP integration](https://unity.com/blog/unity-ai-mcp-how-to-get-started) describes the AI tools as open beta. Epic's [Unreal MCP documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor) labels the feature Experimental and identifies incomplete features and changeable APIs. Professor Bear's assessment for this course is that these integrations still have rough edges. The vendor labels support caution about maturity; they are not measurements of every available integration's reliability. Reassess the choice as the tools develop, including for a later offering of the course.

It would be inaccurate to say Unity, Unreal or Blender can only be driven through MCP. Unity supports C# and command-line editor methods; Unreal supports C++ and editor scripting; Blender can execute Python scripts in background mode. The existing Blender chapter itself uses that script route. A bridge is one route to editor operations, not a prerequisite for writing any code for these applications. The course chooses Godot's direct path for the core engine work and teaches Blender MCP as a particular asset workflow, with its script alternative clearly identified.

## Your first conducting exercise

No software installation or paid generation is required. Choose a game you can already play, or use two pieces of character art you already have permission to inspect. Begin with an intention: one player, one situation and one experience you want to improve.

1. **Predict.** Name one technical failure and one experience failure. Write what you expect to observe before asking an AI for advice.
2. **Build It.** In this preface, build a brief rather than a game. State the desired change, the boundary and two acceptance checks. The toolchain module will give you the setup for implementation.
3. **Use It.** Play the available game or compare the available art in its intended context. If all you have is a static image, record that limit; do not claim you tested animation or gameplay.
4. **Ship It.** Keep a short decision record: intention, delegated work, observed evidence, human judgment and next action. This is ungraded practice, not an extra submission deadline.
5. **Verify.** Check that each observation came from an action you actually performed. Separate a personal preference from a claim about other players.

You may use this prompt after writing your initial position:

```text
Help me turn my game-design intention into a small, checkable brief. Ask for the intended player, desired experience and constraints if I have not supplied them. Separate work I can delegate from decisions I need to make. Propose one technical check and one human playtest or visual comparison. Treat your recommendations as proposals. Do not claim that anyone played, listened, approved or preferred something unless I provide that observation. Do not implement anything yet.
```

Check the response yourself: does the proposed test actually challenge the intended behavior, and does the brief leave the experience judgment with a real person? A useful outcome is a clearer decision, including a decision to reject the AI's recommendation.

## The method continues through every module

The same five questions accompany the whole course: what experience do I intend, what work am I delegating, what evidence could disprove success, what happened when someone used it, and what do I decide now? In art, the decision concerns readability and expression. In physics, it concerns fair and understandable contact. In audio, it concerns timing and feeling. In optimization, it concerns which cost is worth paying. In game AI, it concerns whether an opponent is interesting to encounter.

Module 0 establishes the toolchain. Modules 1–15 practice this relationship through increasingly connected systems. Conducting AI remains the subject even when the immediate task is a shader, an animation or an export.

## Doing the same thing in Unity

**Similarities.** Begin with the same player intention, delegation boundary, independent evidence and human acceptance decision. The engine does not choose your artistic purpose.

**Differences.** Unity work commonly involves C# and editor-managed scenes and assets. Its [command-line editor methods](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/editor) and [MCP introduction](https://unity.com/blog/unity-ai-mcp-how-to-get-started) describe distinct automation routes. Select a route for the operation you need and verify the result in the project. The module endings provide topic-specific comparisons and pointers; this course does not require a second Unity implementation of every assignment.

## Doing the same thing in Unreal Engine

**Similarities.** Keep the same design contract, checks and actual playtesting. A working implementation still needs a human decision about the intended experience.

**Differences.** Unreal's editor assets require appropriate engine tools; editing source code alone is not the same as inspecting every asset. Read Epic's [editor Python guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) and [Unreal MCP guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor). Python here is an editor automation facility, not the gameplay runtime. Compare operations and evidence rather than treating one tool connection as proof of a complete development workflow.

## Sources

Conceptual foundation: Professor Bear's October 12, 2026 course directions; Conducting AI, particularly the conductor and five supervisory capacities; Computational Skepticism, particularly delegation, validation and limits; and Irreducibly Human, particularly Tier One, embodiment and supervisory judgment. Exact local reading paths and the course-wide application map are in [the teaching foundation](../teaching-foundation.md). These are Bear's frameworks and arguments, used as the course's teaching position.

Historical course examples: [toolchain](00-the-toolchain.md), [collision and physics](04-scenes-collision-and-physics.md), [materials](07-materials-and-textures.md), and [Blender to Godot](03-blender-mcp-to-godot.md). No new engine session, character generation or human playtest was performed to write this preface.

Technical pointers were checked against the official pages linked above on October 12, 2026. Blender's [command-line documentation](https://docs.blender.org/manual/en/4.5/advanced/command_line/index.html) and [Python testing instructions](https://developer.blender.org/docs/handbook/testing/python/) document its non-MCP script route. Unity and Unreal comparisons are documentation-based; neither engine was run for this preface.
