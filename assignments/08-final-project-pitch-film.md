# Assignment 8 - Final Project Pitch Film — Show What You Will Build

CSYE 7270 · Fall 2026 · **50 points**

**Due:** five days from release; Canvas shows the date. This is an exception to the course's usual 10-day cadence.

**Submit:** one .zip through Canvas, plus the matching `pitch/` folder in your `walker-` repository, tagged `a8`.

**Required viewing:** [AI Policy for Professor Bear's Courses \| Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw).

## What to do

Your final project is a portfolio piece: something a studio recruiter, lead or hiring manager can open and judge in a few minutes, that shows you can do the game-development work you want to be hired for.

Most final projects grow from the game you have been building since Assignment 2. That might be the game taken to a finished vertical slice, or a tool or system built on it. Either way, it lives in your `walker-` repository.

In five days, make a short film with Brutalist that says clearly what you think that project will be.

This is a pitch, not a build. Part of your game already exists; most of the final project may not. The film must be honest about which is which. You are not locked in: you may change direction later and log the change in `FRICTIONAL.md`.

**Length:** 2–4 minutes. Shorter is fine if the pitch is finished.

## The seven questions the film must answer

1.  **What is it?** One sentence. Then say what exists when it is done: the artifact and its form. That might be a playable build (web or desktop export), a vertical slice, an editor tool or plugin, a shader and effects pack, or a gameplay system with a demo scene.
2.  **Why would anyone care — what makes it special?** This is your unique value proposition.
    - What does it give the person who plays or uses it?
    - What makes it different from what already exists?
    - Name one or two real comparable games or tools you actually played or used, and say what yours does that they do not.

    This project may outlive the course and become real work, so "it is a platformer" is not an answer. "It gives a \[specific player\] \[specific experience\] that \[the comparable game\] does not" is. For a tool: "it saves a \[specific role\] \[specific step\] that \[the alternative\] does not."
3.  **Who opens it, and what do they do with it?** Name the target role (gameplay programmer, technical artist, VFX artist, tools programmer, technical designer or generalist) and the reader (recruiter, hiring manager, lead engineer, or a player). What do they do in the first sixty seconds? For a game: can they be playing within a minute, without reading anything?
4.  **What does it prove about you?** Which skills, tied to what this course teaches:
    - shaders and materials;
    - particle effects;
    - animation and state;
    - profiling;
    - the verification habits: pinned behaviour tests, headless checks and the human checks they cannot replace, and directing an agent with scoped tools.

    What could a reviewer fairly conclude, and what evidence will back it?
5.  **What is in, what is out, what comes first?** One thing it will deliberately not do: no multiplayer, no save system, one level only. The first piece you will make run (usually the core loop, playable in one room), and how someone would know it ran.
6.  **What could sink it?** One concrete risk specific to this project, and what you would do about it. For example: a web export runs only on the Compatibility renderer, so a shader or particle feature built on Forward+ may not survive it.
7.  **Why this project?** Why did you pick it? Is it something new you are learning, something you already know how to do and want to show off, or a mix? Say which skills are new to you and which you already have. For the ones you already have, say what you can point to as evidence: a tagged assignment, a test report, a capture. There is no wrong answer; learning and showing off are both good reasons. But be honest about which it is.

"I don't know yet, and here is how I will find out" is a complete, respectable answer. A confident answer you cannot defend is not.

## The honesty rule

Past tense only for things that exist and that you can show. Everything else is "will." Label what ran, label what is proposed, and never present one as the other.

- No invented players, playtest quotes, studios, wishlists, downloads, metrics or results. "It feels great" is a claim. "Runs at 60 fps" is a measurement: say on what machine, or don't say it.
- Gameplay footage you show is real captured play from your game, and you say which revision it came from. Scripted-input captures and slowed replays are labelled as such.
- Mock-ups, greyboxes, concept sketches and paintovers are labelled *constructed* on screen. Generated art follows Assignment 2's rules and is labelled as generated.
- Any Claude response you show is one you actually got, with the date.

A pitch that fabricates progress to sound ready has failed the assignment, however good it looks.

## Choosing a project

**The right size** is something a stranger can open and verify, that one person can finish, with a failure mode you can name. For example:

- your `walker-` game taken to a finished vertical slice: one level from title screen to end screen, with the layers you have built and a test report a stranger can rerun;
- a technical-art piece built on your game: a shader and effects pack with before-and-after captures, a material audit, and measured cost on a real GPU;
- a gameplay system with pinned behaviour: a character controller and animation state machine with a full edge-test suite and a tuning log;
- a Godot editor tool or plugin that saves a designer one specific step, with a demo scene and tests;
- a small game plus a write-up of where Claude's output was wrong and how you caught it.

**The wrong size:**

- an open world, an MMO, or anything needing a team or an art budget you don't have;
- a tutorial clone with nothing of yours in it, or no evidence that it works;
- anything built on assets you have no right to use: licensed characters, ripped sprites, commercial music;
- anything whose only claim is "it feels good," with no build a stranger can play.

**Rights and privacy.** Assignment 2's rules still apply. No copyrighted characters, brands or music, and no real person's likeness or voice without their agreement. Use your own, generated or properly licensed assets, and credit them in `SOURCES.md`.

**Name your stack.** The course scaffolds are Godot 4, GDScript and Claude Code. Name your Godot version, renderer and export target, since the target decides what the renderer can do.

## Using Brutalist

bash

``` bash
git clone https://github.com/nikbearbrown/brutalist.art
```

Work from the toolkit's own README. Free pipeline only: narration and rendering run locally. No paid generation, no API keys, no media account, and no public upload is required.

If your checkout includes the **show-tell** skill, it is the right format for the pitch beats: one simple drawn picture per beat, minimal on-screen text, narration carrying the explanation. For anything that already exists, show the thing itself. The **`godot-walkthrough`** workflow with the **`walker`** modifier captures the real rendered viewport. A pitch for a game that shows none of the game is a weaker pitch.

Run the toolkit's own quality gates and include their reports. Fix a film that fails its render-integrity check; do not submit over it.

AI narration, including Liam, is allowed, but it speaks as you. Do not use the instructor's name, persona or credit line.

If Brutalist won't run on your machine, that is a legitimate `FRICTIONAL.md` entry, not an automatic loss of points. Record what you tried, what broke, and what you did instead.

## A five-day shape (a suggestion)

| Day | Do |
|----|----|
| 1 | Choose the project. Write the seven answers in `PROJECT-BRIEF.md`, in plain sentences. |
| 2 | Turn the seven answers into a beat sheet: one picture, one idea per beat. Capture real play of anything that exists. |
| 3 | Build the film. |
| 4 | Run the gates. Check every claim against the honesty rule. Re-render what failed. |
| 5 | Write Frictional, assemble the folder, tag `a8`, and submit to Canvas and GitHub. |

## What to submit

**Canvas file name:** `LastName_FirstName_CSYE7270_FinalProjectPitch.zip`

**GitHub folder:** `pitch/` in your `walker-` repository, with the submitted commit tagged `a8`. It contains:

- `README.md`: your name, the project's working title, the target role, the runtime, the film link with its filename and SHA-256 checksum, and how to rebuild the film;
- `PROJECT-BRIEF.md`: one page answering the seven questions in text, ending with two lists, **exists today** (with the tag or commit where each thing can be seen) and **will exist**;
- `beat_sheet.json`: your narration and visual plan;
- `BUILD-PROMPT.md`: the prompts and commands that rebuild the film;
- `SOURCES.md`: what you used, what you made, what Claude contributed, and any third-party asset with its licence;
- the toolkit's gate reports, if it produced them;
- `FRICTIONAL.md`: dated entries as you worked.

Keep the rendered film (.mp4) and any file over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Test reviewer access to the source and media.

Include the GitHub folder link, the tag, and your final commit hash in the Canvas submission. Leave out caches, credentials, private data and private conversation transcripts.

## Optional: share it for feedback

Sharing is entirely optional. It earns no points, and skipping it costs none. Reviewers do not see or consider where a film was posted. Posting publicly is a separate decision from submitting.

Don't post another person's private information, restricted course material, or work you don't have the right to share. Remember that once something is public it can be copied and indexed, even if you delete it later.

## Grading — 50 points

| Component                              | Points |
|----------------------------------------|--------|
| The pitch                              | 30     |
| Frictional (honest log)                | 5      |
| GitHub version posting matching Canvas | 5      |
| Relative Quartile                      | 10     |
| **Total**                              | **50** |

**The pitch (30):**

| Criterion | Points |
|----|----|
| What and who: one clear sentence, a named artifact and its form, target role and reader, the first sixty seconds | 7 |
| Unique value: why anyone would care, at least one real comparable game or tool named, a specific difference, no invented market or competitor claims | 5 |
| What it proves: course skills named, evidence planned (tests, captures, measurements), no overclaiming | 5 |
| Why this project: honest about new learning versus existing skill on show, new and existing skills separated, existing ones backed by something real | 4 |
| Scope and honest risk: in, out and first separated; the first playable piece and how anyone would know it ran; a concrete risk; exists versus will-exist explicit | 5 |
| Shown, not asserted: real captured play for what exists, constructed material labelled, nothing presented as done that is not, the film passes its own quality checks | 4 |

**Relative Quartile (10)** compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication across the whole comparison group. Meeting the stated requirements earns the 40 criterion-based points; it does not guarantee these 10. The instructor and TAs review the full group before assigning it.

| Placement  | Points |
|------------|--------|
| Top 25%    | 8–10   |
| Second 25% | 5–7    |
| Third 25%  | 2–4    |
| Bottom 25% | 0–1    |

Production polish counts only as professional communication. A plain, honest pitch for a modest project will outrank a beautiful one that overclaims.

## AI use and responsibility

Read the course AI policy and watch [AI Policy for Professor Bear's Courses \| Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw).

Use Claude throughout if you want: script, beat sheet, build. Name what it contributed in `SOURCES.md`.

You remain responsible for what you submit. The instructor or a TA may ask you to explain any part of the film, the brief, or the build. Not being able to explain your own submission reduces points under the relevant criteria. Misrepresenting what you verified is an academic-integrity matter.

 
