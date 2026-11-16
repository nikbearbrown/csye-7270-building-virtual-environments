# Assignment 9 - Teach One Game-AI Technique: Explain, Show, Try

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies.

**Required viewing:** [AI Policy for Professor Bear's Courses \| Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw).

## Executive summary

You implement one significant AI technique so it does real work in your game, and then you teach it.

Before building, you write what a learner should be able to do afterward and what you predict they will get wrong. Then you build the technique in your game, with a debug view anyone can toggle. Then you build the teaching:

- a starter project and a solution project;
- at least three exercises, each with a headless check that fails on the starter for the right reason and passes on the solution;
- a tutorial;
- a debugging guide built from failures that really happened;
- an Explain → Show → Try film;
- a short pedagogical report.

At least one real person works an exercise. If nobody does, every claim about how well the teaching works is labelled as predicted.

You hand in the repository tagged `a9`, a test report, and a `godot-walkthrough` film. Grading follows the course's 60/10/10/20 split. A passing exercise check proves that a learner's code meets the check. It does not prove the learner understood, and only a real tryout shows where the teaching works.

## Your task

1.  **The technique, in your game.** One significant AI technique doing real work in your game, with deterministic tests, a measured cost, and a debug visualization a player or learner can toggle.
2.  **The exercises.** A starter project and a solution project. At least three exercises, each with a headless check and a solution.
3.  **The tutorial.** A progression from the starter to the working technique, with a debugging guide built from real failures.
4.  **The film.** Explain → Show → Try.
5.  **The pedagogical report and a real tryout.** Who the teaching is for, what it should achieve, how the implementation performs, and what happened when someone actually used it.

**Choosing the technique.** It must be relevant to games, complex enough to show mastery, and small enough for one person to implement and teach in ten days. For example:

- a finite or hierarchical state machine for an NPC (A7's machine served the player; this one decides for a character the player doesn't control);
- a behaviour tree written from scratch (Godot has none built in);
- utility AI, or goal-oriented action planning;
- steering and flocking;
- A\* on a grid, or navigation meshes;
- influence maps;
- wave function collapse, or another procedural-generation technique;
- Monte Carlo tree search for a turn-based game;
- an AI-assisted development technique this course taught: pinning behaviour before an agent changes it, closing the visual loop with frame captures Claude can read, or separating headless checks from human checks, demonstrated on a real change to your game.

Three rules shape the choice.

- **Built-ins.** If Godot already provides the technique (`NavigationAgent2D`, `NavigationAgent3D`, `AStarGrid2D`), you may teach the built-in, but the tutorial must show what it does underneath, at least once, in your own code.
- **LLM dialogue** is allowed only with a local model or a provider's free tier. Nothing paid is required. The key is read from an environment variable and never committed, and the dialogue data is synthetic. Your checks test the integration (the context you assemble, the fallback when the model is unavailable), not the model's exact words, which change between runs. If no free route runs on your machine, choose another technique.
- **Reinforcement learning** is allowed only with a tiny environment that trains in under an hour on your machine, or a pre-trained policy you credit. Commit the training scripts and record the seeds.

**Your game, one more layer.** From Assignment 2 on, you build one game: the one you chose in Assignment 2, in a repository whose name begins **`walker-`**. This assignment adds one layer to it and is submitted as the git tag **`a9`**. The starter and solution projects live in the same repository, under `teach/`. If your Assignment 8 pitch was a teaching package or an AI system, this assignment can be its first piece; say so in `CHANGE-BRIEF.md`. If you changed games before Assignment 4, the tag continues on the new repository; say so in your submission note. This is an individual assignment.

**Who writes what.** You write the learning objectives, the exercise designs, and the tutorial's explanations, in your own words. A tutorial an agent wrote teaches what the agent understands. Claude Code assistance is expected for everything else: the implementation, the checks, the starter and solution projects, and review of your tutorial. If you adopt an edit Claude suggests for your tutorial, record it in `SOURCES.md`. Use your Northeastern access. Nothing paid is required, and paid output earns no bonus. You remain responsible for every line and every check.

### What counts

| Part | Minimum |
|----|----|
| The technique | Doing real work in your game, not a side demo. Its behaviour tests drive the game through the real loop with seeded randomness. Its CPU cost is measured. A debug visualization is toggled by an input action. It runs in more than one scenario. |
| Starter and solution | Two standalone Godot projects, `teach/starter/` and `teach/solution/`, that a learner can open without the rest of your game. |
| Exercises | At least three, each mapped to a learning objective. Each check fails on the starter on an assertion, with a failure message that teaches; a script error is the wrong reason. Each check passes on the solution. |
| Tutorial | `teach/TUTORIAL.md`, in Markdown, progressing from the starter to the working technique, with the command that runs each exercise's check. `teach/DEBUGGING.md` is built from failures that actually happened. |
| Film | Explain → Show → Try, at most 15 minutes. |
| Report and tryout | `teach/REPORT.md`, and at least one real person's attempt at an exercise, recorded. Without a tryout, effectiveness claims are labelled as predicted. |

### Rights and provenance

- The starter and solution projects carry only assets you have the right to share with a learner. Greybox shapes are fine, and preferable. Credit everything in `SOURCES.md`, and give `teach/` a licence a learner can use.
- When the film or tutorial says how a commercial game uses your technique, cite the source: a talk, a postmortem, or an interview. Otherwise, say it's your own reading of the game. Claims about how a shipped game's AI works are often folklore.
- Assignment 2's rules apply to any generated asset. Never commit credentials.

## 1. Predict

Replace the contents of `CHANGE-BRIEF.md` with this assignment's brief and commit it before your first prompt. The previous brief stays in history at its tag, and `CLAUDE.md` already imports this file. Keep the original; add dated revisions below it.

### `CHANGE-BRIEF.md` — the technique, the learner, the predictions

- **The technique:** what it is, why it's worth teaching, and where it does real work in your game: which character or system, and what it replaces.
- **The learner:** who they are, what they already know, and what they don't. For example: a Godot programmer who has never written game AI, or a student who has finished this course's first seven assignments.
- **Learning objectives:** three to five, each written as "after the tutorial, the learner can…", and each mapped to the exercise and the check that exercise it.
- **The implementation specification:**
  - *Observable rules* that can be measured: what the AI decides, and when. For example, "a guard switches from Patrol to Chase when the player is within six tiles and in line of sight, within one decision tick."
  - *Boundaries:* player movement, collision, input, the game-state authority from Assignment 7, earlier effects and earlier tests stay unchanged.
  - *The evidence split:* for each rule, a headless test or your eyes, and how.
  - *A budget:* CPU time per agent per frame at the most agents your design allows, at your target frame rate.
- **The exercise plan:** for each exercise, what the starter provides, what the learner writes, what the check asserts, and the failure message a typical wrong answer produces.
- **At least three predicted learner challenges.** You will compare them with what the tryout actually shows.
- **At least three predicted failure cases** in the implementation, each with the check that would catch it.

Then answer briefly:

1.  Is your technique built into Godot? If it is, what will your tutorial show of what it does underneath?
2.  On which clock does your AI decide (every physics tick, every rendered frame, or on a timer), and what does that cost at your agent count? (Assignment 7's two clocks apply here.)
3.  What makes your AI's behaviour deterministic enough to test: seeded `RandomNumberGenerator` instances, a pinned frame rate, fixed spawn positions?
4.  Which of your learning objectives can a headless check verify, and which can only a real learner show?

## 2. Build It

Read the module material on your technique first, and look at how the Walker examples structure their tests. Commands assume your game lives in `godot/`.

Run every check through the course wrapper. This version adds a project path, so the same script runs the starter and the solution:

bash

``` bash
#!/usr/bin/env bash
# scripts/run-test.sh <test-file.gd> <fps|realtime> [timeout-seconds]
# Project path from GODOT_PROJECT (default: godot).
set -o pipefail
project="${GODOT_PROJECT:-godot}"
mkdir -p logs
if [ "$2" = "realtime" ]; then
    fps_args=(); tag="realtime"
else
    fps_args=(--fixed-fps "$2"); tag="${2}fps"
fi
log="logs/$(basename "$project")_$(basename "$1" .gd)_${tag}.log"
timeout "${3:-120}" godot --headless "${fps_args[@]}" --path "$project" --script "res://tests/$1" 2>&1 | tee "$log"
status=$?
if grep -qE "SHADER ERROR|SCRIPT ERROR|Failed loading resource" "$log"; then status=1; fi
exit $status
```

Run each existing test with `./scripts/run-test.sh <test>.gd 60` and record the counts: that is your baseline.

After every agent session, read the final result event in the session's `.jsonl` file, which records a `--max-turns` stop and any permission denials. Then run `git status` and `git diff` before you accept anything. If a session ended early, rerun every check before committing its work.

### Step 1 — context

Update `CLAUDE.md` so its "Project context" section gives the exact check commands for the game, the starter and the solution, each with a file reference. Add an "Ownership" line saying that the tutorial's prose and the learning objectives are yours, and that agents do not edit them. Commit the agent's draft and your review separately, as before.

### Step 2 — the technique in your game

Plan first. If the technique changes behaviour your game already has, such as an enemy that already moves, pin that behaviour first, as in Assignment 7, and keep the change and the re-pin apart.

text

``` text
Read CLAUDE.md first. The implementation specification in
CHANGE-BRIEF.md is the contract for this change.

Inspect first and change nothing. Tell me, with file and line
references, where the character or system my technique replaces lives
now, what decides its behaviour today, and which tests cover it.

Then propose the smallest plan: the nodes and scripts you would add,
how the AI reads game state without writing it, the debug
visualization and the input action that toggles it, and one headless
test per observable rule. The tests drive the game through the real
loop: input with Input.parse_input_event where the player is involved,
seeded RandomNumberGenerator instances, and the time step pinned. They
never call the AI's decision function directly. Say which rule each
assertion covers and which rules only a human can check. Do not edit
yet.

After I approve a step, implement only that step, run every check
through ./scripts/run-test.sh, show the real output, and list what
still needs a human at a screen. Use Godot 4 API for the version in
CLAUDE.md; if you are unsure something exists, say so instead of
guessing. Do not commit.
```

Price it. AI decisions are CPU work, so a headless run measures them, unlike the GPU particles of Assignment 6. Use the Assignment 6 cost-script method: an empty-scene baseline, 60 warm-up frames, then 300 timed frames, three repeats in three fresh processes, all at `--fixed-fps 60`. Instance the most agents your design allows, and switch the debug visualization off while you time.

### Step 3 — starter, solution and exercises

Build `teach/solution/` as a standalone Godot project containing only what the technique needs: greybox shapes, one scene per scenario, and the technique itself. Build `teach/starter/` from it by replacing the parts the learner writes with stubs that parse and run. Each exercise gets a check in both projects' `tests/` folders.

text

``` text
Read CLAUDE.md, CHANGE-BRIEF.md and teach/TUTORIAL.md first. The
exercise plan in CHANGE-BRIEF.md is the contract.

For each exercise, write one headless check in teach/solution/tests/
and the identical file in teach/starter/tests/. Each check drives the
scenario through the real loop with seeded randomness, prints one
PASS/FAIL line per assertion, exits 1 on any failure, and on failure
prints the message the exercise plan specifies, phrased to help a
learner find the mistake.

Then run every check against both projects:
GODOT_PROJECT=teach/solution ./scripts/run-test.sh <check>.gd 60
GODOT_PROJECT=teach/starter ./scripts/run-test.sh <check>.gd 60
Every check must pass on the solution. Every check must fail on the
starter on an assertion; a SCRIPT ERROR is a failure for the wrong
reason. Show the real output for both. Never put solution code in the
starter to make a check behave. Do not edit TUTORIAL.md. Do not commit.
```

A check that passes on the starter has tested nothing, and a learner who runs it learns nothing from the PASS. A check that fails on the starter with a script error teaches the learner only that the starter is broken. Record both runs for every check.

### Step 4 — the tutorial and the debugging guide

Write `teach/TUTORIAL.md` yourself. It covers:

- the theoretical foundation, at your learner's level;
- the progression from the starter;
- one section per exercise, with its objective and the exact command that runs its check;
- diagrams, as images or Mermaid blocks;
- a challenge beyond the exercises.

Write `teach/DEBUGGING.md` from failures that actually happened: entries in `FRICTIONAL.md`, agent mistakes you caught, and anything your tryout turned up. Give each entry the symptom, the check output or observation that revealed it, and the fix.

Then follow your own tutorial from a fresh clone, exactly as written, and record every place it breaks.

### Step 5 — the tryout

Ask at least one real person (a classmate, a friend who programs) to work at least one exercise from the starter, using only the tutorial. Record the date, what they attempted, where they got stuck, what the check told them, and their actual words. Then change the tutorial in response, and record what you changed.

Do not invent a learner. If no one is available, say so in `REPORT.md` and label every effectiveness claim as predicted.

### What the agent is likely to get wrong

Each of the first five happened in an earlier assignment's record. The last is a prediction.

| Likely mistake | How to catch it |
|----|----|
| A test that calls the decision function directly, so the real loop, the clock and the input path stop mattering (Assignment 5). | Read the test, not the summary. |
| Checks that set a value and read it back, passing on broken code (Assignment 5). | Make sure each check fails on the starter for the right reason. |
| A counter that reaches the right number while nothing visible happens: counting is not watching (Assignment 7). | The debug visualization, and your eyes. |
| Godot 3 API in a Godot 4 project (Assignments 6 and 7). | A failing check, or the class reference. |
| A refused command followed by a confident "expected output" table (Assignment 6). | The session's result event and its permission denials. |
| Solution code copied into the starter so the checks behave. | A check that passes on the starter, and `git diff teach/starter/`. |

### What must not change, and what counts as done

These must not change: player movement, collision, input, the game-state authority from Assignment 7, your earlier effects and animations, and earlier tests.

Done means:

- every observable rule has a recorded machine or human check;
- every exercise check fails on the starter for the right reason and passes on the solution;
- the tutorial works from a fresh clone;
- the debugging guide's entries all happened;
- the tryout is recorded, or its absence is stated;
- the earlier suites give their baseline counts.

"Claude said it works" is not on the list.

## 3. Use It

Open the game in the Godot editor and run it. Record actual results in `TEST-REPORT.md`, with the source revision, Godot version and renderer:

| Check | Evidence to collect |
|----|----|
| Baseline | Every earlier test, before and after, with pinned frame rate and counts. |
| Technique behaviour | Each observable rule's test output, in the mode it ran in. |
| Price | The cost script's output: the baseline, and per-agent cost at your maximum agent count, against the budget. |
| Exercise checks | Every check against the starter (FAIL, on an assertion) and the solution (PASS), with both logs. |
| Debug visualization (HUMAN CHECK) | Toggled in play: does it show the decision the tests assert? |
| In play (HUMAN CHECK) | The technique in every scenario, several times: does it do its job, and do the boundaries hold? |
| Fresh-clone walkthrough (HUMAN CHECK) | Where your own tutorial broke when you followed it exactly, and what you changed. |
| Tryout (HUMAN CHECK) | Who, when, which exercise, where they got stuck, their actual words, and the change you made. |

Include at least one inspect-and-revise cycle driven by an observation: a check message the learner misread, or a decision the debug view showed was wrong. Do not delete a failing assertion or weaken an expected result to obtain a green report. Your own playtest is required, and no headless run replaces it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-walkthrough`** workflow with the **`walker`** modifier for the Show segment, which needs real captured play. If your checkout includes the **show-tell** skill, it suits the Explain segment: one simple drawn picture per beat, with narration carrying the explanation. Ask Claude Code to read the installed skill instructions and follow them. If your checkout lacks a skill, request the course-provided version.

Make **one** landscape film, at most 15 minutes, in three segments. Explain is short, Show is the longest, and Try gets the rest:

1.  **Explain:** the concept, why games use it, and real examples, with sources as the provenance rules require. Then your learner and the learning objectives.
2.  **Show:** the technique working in your game in more than one scenario, with the debug visualization on. Then the key lines of the implementation, each followed by the behaviour it produces.
3.  **Try:** one exercise from the starter, its check failing with its teaching message, the fix, the check passing, and a challenge the viewer can attempt from the repository.

Close with what the checks prove and what they don't, what the tryout showed (or that there wasn't one), one next step, the human and AI contributions, and the revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed views, scripted-input captures and held frames; never present a reconstruction as a screenshot. Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. A second film, a vertical Short, paid media generation and public YouTube publication are **not required**. The film is part of the 60-point category below, not a substitute for working source.

### Post the version on GitHub

Your submitted source includes:

- The game with the technique, its tests and the debug visualization; `teach/starter/` and `teach/solution/`, each opening on its own; no `.godot` cache or credentials.
- `README.md`: project name, starting point, engine version and renderer, run instructions, controls, how to toggle the debug view, what this assignment added, known limitations, and the film link.
- `teach/TUTORIAL.md`, `teach/DEBUGGING.md`, `teach/REPORT.md`, and a licence for `teach/`.
- `CLAUDE.md`, `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, and `SOURCES.md`.
- Your tests, the cost script, cited logs for both the starter and the solution, prompts, and any `claude -p` transcript under about 1 MB (otherwise a labelled excerpt).
- The film's beat sheet, script/prompts, and evidence/coverage records.

`teach/REPORT.md` covers three things:

- your learner, the objectives and the rationale for the progression;
- an implementation analysis, with its architecture, measured cost and limits;
- your predicted learner challenges set beside what the tryout and the fresh-clone walkthrough actually showed.

Write it at whatever length those need.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Commit in the order the work happened, with messages that say what was checked, for example `Guard behaviour tree (agent); 6 rule tests pass at 60 fps; debug view checked in play`. Tag the final submission commit **`a9`**.

## 5. Verify and submit to Canvas

Clone the `a9` tag into a fresh folder. Import each project once. Then run:

- every game test, at its pinned rate;
- every exercise check against the solution, all of which must pass;
- every exercise check against the starter, all of which must fail on an assertion.

Confirm the counts match `TEST-REPORT.md`. Then follow the tutorial's first exercise from that clone. A working local folder is not proof that everything was posted.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

text

``` text
Assignment: Assignment 9 - Teach One Game-AI Technique: Explain, Show, Try
Student:
Project name:
GitHub repository URL:
Git tag and submitted commit SHA:
Game-source revision shown in the film:
Godot version, renderer, and operating system:
Technique, and where it works in the game:
Learner (target audience):
Exercises and their checks (starter: all FAIL; solution: all PASS):
Measured cost per agent, at how many agents, on what machine:
Tryout (who, date, which exercise; or "none, effectiveness labelled predicted"):
Final film URL and filename:
Final film SHA-256:
Summary of my work:
Known limitations:
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions, and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit. Canvas, GitHub, and the film must refer to the same submitted work. Identify later changes as a new revision.

## Rubric — 100 points

| Component                              | Points  |
|----------------------------------------|---------|
| Implementation and explanation         | 60      |
| Frictional — honest log                | 10      |
| GitHub version posting matching Canvas | 10      |
| Relative Quartile                      | 20      |
| **Total**                              | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|----|----|
| Brief before building: a learner, objectives mapped to exercises and checks, an implementation specification with rules, boundaries, evidence split and budget, predicted learner challenges and failure cases, all committed before the first build step. | 6 |
| Concept and implementation: an accurate explanation at the right depth (4); the technique doing real work in the game, with real-loop deterministic tests, boundaries kept and cost measured against the budget (7); a toggleable debug visualization, and more than one scenario (3). | 14 |
| Tutorial and exercises: a progression from the starter, with objectives mapped to exercises (5); at least three exercises whose checks fail on the starter for the right reason and pass on the solution, with failure messages that teach (7); solutions, and a debugging guide built from real failures (4). | 16 |
| Show-and-tell film: Explain → Show → Try with real captured play in Show (5); a Try challenge a viewer can attempt from the repository (3); accurate, sourced claims, with test limits, contributions and the revision stated (3); a readable, audible film made with the required workflow (1). | 12 |
| Pedagogical report: learner, objectives and rationale (2); an implementation analysis with measured cost and limits (3); predicted versus observed learner challenges (3). | 8 |
| Real tryout: a real person worked at least one exercise from the starter, with their actual results recorded and a tutorial change made in response (4). Without a tryout, effectiveness honestly labelled as predicted earns at most 1. | 4 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing exercise check establishes that code meets the check. It does not establish that a learner understood, so the tryout and the fresh-clone walkthrough carry points that no check can earn.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source, teaching projects and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit your starting point, every asset, every source you cite about how commercial games use your technique, collaborators, and tools. Describe what AI contributed to the implementation, checks, starter and solution projects, script and narration. Describe what you personally wrote, designed, checked, changed or rejected.

The instructor or a TA may ask you to:

- explain any line of your implementation;
- predict what a check prints for a wrong answer before running it;
- show why a check fails on the starter.

Inability to explain reduces points under the relevant criteria. Presenting agent-written tutorial prose as your own misrepresents authorship. Recording a tryout that did not happen misrepresents verification. Misrepresenting authorship, provenance, or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw) and the course/university policies.
