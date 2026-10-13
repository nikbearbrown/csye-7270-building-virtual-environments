# Preface — Conducting AI Through Games and Virtual Worlds

## Executive summary

Conducting AI is the central practice of this course. You choose the experience, delegate suitable technical work, inspect the evidence, play the result and decide what should change. Games make this relationship tangible: code, art, animation and sound can all function while the game still feels wrong. An agent can help build the machinery and test explicit rules; its report cannot replace the actual player's experience or your responsibility for the design. This preface comes before Module 0 and requires no new software installation. Read the [companion preface](../../chapters/preface-conducting-ai.md) for the full argument and sources.

## The question

A character imports correctly, moves correctly and passes every existing test. When you play, you keep losing it against the background. Is the work done?

The tests may be accurate about what they checked. The design may still fail the player. Your task is to identify the unanswered question, gather the relevant evidence and decide whether to revise the art, background, motion or original intention. Asking the agent whether it thinks the character is good does not establish what happened when a person tried to use it.

## The ideas

### Conducting is decision making

A film director does not need to perform every role in the production. A conductor does not play every instrument. They direct skilled contributions toward an intended whole. In this course, AI performs suitable implementation work, while you define purpose, provide context, select tools, inspect outcomes and retain the acceptance decision.

Blender, Godot, Unity and Unreal involve sophisticated technical work. An agent's ability to help with that work gives you more scope to build. It also gives you more consequential decisions to make. Typing fewer lines does not reduce your responsibility to understand the result. Learn enough about the machinery to notice a meaningful failure and explain your judgment.

### Games combine engineering with art and opinion

Imagine fifty character variants, then fifty more. This is a hypothetical selection problem, not a generation task you must pay for. More candidates do not answer which one belongs in your game. The richest portrait may fail at the small size the player sees. A beautiful effect may obscure a hazard. A perfectly repeatable jump may feel wrong for the experience you intended.

You may ask AI to compare candidates against explicit criteria, but the criteria and final choice still need a human owner. Try the work in context. Explain the difference between your taste, an observation of behavior and a claim about what other players prefer. Real feedback can change your mind; invented feedback cannot support a decision.

### Skepticism produces a check

Computational Skepticism asks how you know a claim is supported. Before prompting, predict a failure and name the observation that would expose it. A check should be able to disagree with the implementation. A second agent agreeing with the first is not enough if both rely on the same untested assumption.

The existing [physics chapter](../../chapters/04-scenes-collision-and-physics.md) records a shield test that passed despite a deliberately shortened shield duration. This is why checking the checker matters. The [materials chapter](../../chapters/07-materials-and-textures.md) records another gap between passing checks and the intended material setting. These are historical examples, not fresh runs performed for this preface.

### Technical checks and human experience

AI can inspect code, write tests and run scripted interactions. Those are useful forms of evaluation. They do not supply your lived response or the actual response of a player who has not played. Separate implementation evidence from experience evidence and the decision to accept the design.

Professor Bear's Irreducibly Human framework distinguishes strong pattern-production capability from the wider capacities involved in lived experience, supervision, interpretation and responsibility. Its strongest structural claims are arguments you can examine. The practical course obligation is clear: delegate suitable work, bring real experience into the evaluation and defend your decisions with reasons.

## Why Godot

The course chooses Godot primarily because Claude Code can work directly with its code and text project artifacts, then use engine commands to inspect and test the result. The core workflow needs no MCP bridge. Godot documents both its [command-line workflow](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) and [text scene format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html).

MCP, the Model Context Protocol, lets an agent call tools exposed by another application. It can be useful for operating an editor, but it is not what makes this Godot workflow possible. Whether a Godot MCP integration is available is a separate question from whether this course needs it.

The October 2026 course choice also reflects Professor Bear's assessment that other editor integrations still have rough edges. Unity's [May 11 MCP introduction](https://unity.com/blog/unity-ai-mcp-how-to-get-started), checked October 12, describes its AI tools as open beta; Epic's [Unreal MCP documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor) labels its feature Experimental. These are dated maturity signals, not permanent judgments about either engine.

Unity, Unreal and Blender also have non-MCP scripting routes. In particular, the course's own [Blender chapter](../../chapters/03-blender-mcp-to-godot.md) records a Python-script workflow. Distinguish direct code editing, engine commands and a live editor bridge. Choose the path that provides the operation and evidence you need. Revisit this choice when teaching with newer integrations.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Choose an existing game you can play or two existing character images you may inspect. Name the player and intended experience. Predict one technical failure and one experience failure before consulting an AI.

### 2. Build It

Build a short brief here; implementation begins after toolchain setup. State the desired change, what must remain unchanged, what you will delegate and two acceptance checks. You can ask the agent:

```text
Help me make my game-design intention checkable. Ask about the player, desired experience and constraints where needed. Separate delegated technical work from human decisions. Propose a technical check and a real playtest or visual comparison. Do not invent player feedback, claim an unperformed check or implement anything yet.
```

### 3. Use It

Play or inspect the actual available artifact. Record what you did and observed. A still image cannot establish animation quality; an automated route cannot establish enjoyment. If you cannot perform the needed check, mark it pending.

### 4. Ship It

Keep a five-part decision record: intention, delegated work, evidence, human judgment and next action. This is ungraded practice. No new deadline, paid generation or public posting is required.

### 5. Verify

Read the record against what actually happened. Can every claimed observation be traced to a real action? Does your reason for accepting or rejecting the result follow from the evidence and intended experience? State what would change your mind.

## Practice assessment (ungraded)

Take the six-question practice quiz, then answer these two questions in your own words: what useful evaluation can an agent perform, and what would still require your judgment in the game you chose? Explain why choosing Godot for a direct workflow does not imply that other tools universally require MCP.

## The next step

Continue to [Module 0: the toolchain](../00-start-here/lesson.md). Carry the same questions into every module: what do I intend, what do I delegate, what could disprove success, what happened in use, and what do I decide now? The course's existing *Why Godot?* film is a companion to this rationale, not a substitute for testing the workflow you actually use.

## Doing the same thing in Unity

**Similarities:** keep the player intention, independent checks and human acceptance decision. **Differences:** use Unity's C# and editor workflows for the implementation; an MCP connection is one possible route to editor operations. Start with [Unity command-line editor methods](https://docs.unity.com/en-us/engine/6000.3/manual/unity-editor/command-line-arguments/editor) and [the Unity MCP introduction](https://unity.com/blog/unity-ai-mcp-how-to-get-started). These are documentation-based pointers, not a Unity run performed for this module.

## Doing the same thing in Unreal Engine

**Similarities:** preserve the design contract, evidence and real playtest. **Differences:** distinguish code edits from operations on editor assets, and choose suitable engine tools. Start with [editor Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) and [Unreal MCP](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor). Editor Python is not the gameplay runtime. These are documentation-based pointers, not an Unreal run performed for this module.
