# Assignment 6 - Audit a Plausible but Incorrect Shader Change

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 60 after the first class day.

**Covers:** [Module 8 — Shader verification](../modules/08-shader-verification/lesson.md) and its chapter, [Shader Verification](../chapters/08-shader-verification.md), applied to the shader you built in Assignment 5.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Executive summary

This is a review assignment. You audit shader changes that compile, pass the usual tests, arrive with a respectable reason, and are wrong, and you decide each with controlled inputs and observed output, not by reading the diff and guessing. Part A uses the seeded change from the course's Chapter 8 record. The chapter names its two defects, but no window was opened for the book, so nobody has observed the visible one; your bench screenshots are the first observation. Part B applies the same method to a change Claude Code makes to your own Assignment 5 effect without telling you what it did. You hand in two audits, the evidence that decided them, the repository tagged `a6`, and one `godot-gamedev` film. Every finding states what you ran, what you saw, what it shows, and what it does not show. A green headless suite is not a verdict: on a shader, it cannot see the defect that matters most.

## Your task

**Part A — the course's seeded change.** In a clone of [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd), apply [Chapter 6's end state](../examples/06-shader-foundations/changes.diff) and then [the seeded commit](../examples/08-shader-verification/seeded-change.diff) from the Chapter 8 record. Audit it against the eight-rule specification in its `CLAUDE.md`. Its message:

```text
Flash: player owns its fade timer; sample the sprite texture explicitly

Presentation should not reach into session internals (retry_remaining).
The player now counts its own fade, and the shader reads TEXTURE directly
instead of relying on the incoming COLOR.
```

Chapter 8 tells you what is wrong with it. That is deliberate: Part A is the method practised on a known answer, plus a gap you can close. The record's claim that the seeded shader loses Clawd's colours rests on Godot's definition of `COLOR` and was never observed. If your screenshots disagree with the chapter or the agents, report what you saw.

**Part B — a change to your own effect.** Claude Code makes one plausible but incorrect change to the shader or driver you built in Assignment 5, commits it on a branch with a respectable message, and reports what it did into a transcript you do not open until your verdict is committed. You audit it with the same method.

**Reading is not deciding.** You will read both diffs and form hypotheses. A hypothesis becomes a finding only when a controlled input produces observed output that a correct change and this change would not both produce.

**Your game, one more layer.** From Assignment 2 on, you build one game, the one you chose in Assignment 2, in a repository whose name begins **`walker-`**. Assignments 3–10 each add one layer and are submitted as a git tag; this one is **`a6`**. This layer is evidence: the oracle, model and bench from Part B are merged into your game; the change under audit stays on its branch. The one change of game the course allows had to happen before Assignment 4; if you made it, your submission note says so. This is an individual assignment.

Claude Code assistance is expected; use your Northeastern access. Nothing paid is required. Codex is an optional second reviewer.

**Keep walker-jumpman-clawd out of your repository.** Its `SOURCES.md` says public availability is not a licence grant for its inherited work. Do Part A in a separate clone and commit only your audit, logs, screenshots, and files you or your agent wrote, under `audits/part-a/`.

### The evidence standard

Every finding, in either audit, takes this form in that part's `AUDIT.md`:

```text
## Finding B1 — one line
- Change under review: branch or commit, file, line
- Spec rule: number and text
- Family and rung: which of the five families; which rung of the ladder
- Controlled input: the values, and why they separate right from wrong
- Predicted (written before running): correct value / changed value
- Ran: the exact command, or the editor procedure
- Saw: the log line or number, or the screenshot path and sampled hex
- Shows: what this evidence establishes
- Does not show: what it leaves open
- Source: observed by me / asserted by an agent / taken from the record
```

The ladder comes from Chapter 8. Name the rung each claim stands on.

| Rung | Question | Headless in Godot 4.7.2? |
|---|---|---|
| 1. Parse | Is it valid shading language? | Yes: a `SHADER ERROR` line and an empty uniform list |
| 2. Contract | Do uniforms, types, hints and defaults match the spec? | Yes, plus the source text for defaults |
| 3. Driver | Does game code set the uniforms right, at the right moments? | Yes, at several pinned frame rates with real input |
| 4. Model | What should each pixel be? | Yes, as arithmetic about the spec, not the GPU |
| 5. Observation | What did the GPU draw? | No: a bench, a screenshot, a colour picker, a person |

## 1. Predict

Commit `CHANGE-BRIEF.md`, your audit plan, before any review, evidence session, or seed runs. Keep the original; add dated revisions below it.

- **Part A.** Answer Chapter 8's four Predict questions in your own words, with numbers.
- **Part B.** For each of Chapter 8's five families (wrong input, colour space, alpha convention, coordinate flips, time), say whether it can occur in your Assignment 5 effect. For each that can, give the controlled input that would expose it, the correct and wrong predicted values, and the rung that can observe it; for each that cannot, say why. This is your plan for finding a defect you have not seen.
- **At least three predicted failures of your own audit**, each with the check that would catch it: for example, an oracle whose tolerance rejects correct code, a test that reads last frame's value against this frame's clock, or a screenshot tool that applies colour management.

## 2. Build It

Read the module lesson and the chapter. [Example 08](../examples/08-shader-verification/) holds the prompts, both oracles, the colour model, the bench, and every log. [walker-compute-post-shader](https://github.com/nikbearbrown/walker-compute-post-shader) shows the same ladder for a compute shader.

Wrap every headless run in `timeout 120`, pin every frame-counted run with `--fixed-fps`, and grep every log for `SHADER ERROR`: exit code 0 does not mean the shader parsed.

### Part A — the seeded change in walker-jumpman-clawd

Rebuild the review commit exactly as Chapters 6 and 8 do. Their commands assume the course repository's `examples/` folder sits beside your clone; if yours is elsewhere, change only that path. `git add -A` matters because the first patch creates new files.

```bash
git clone https://github.com/nikbearbrown/walker-jumpman-clawd.git
```

```bash
cd walker-jumpman-clawd
```

```bash
git checkout -b ch06-failure-flash 382f2baa5ee5e90a5afc083d82a5337845157f34
```

```bash
git apply ../examples/06-shader-foundations/changes.diff
```

```bash
git add -A
```

```bash
git commit -m "Chapter 6 end state"
```

```bash
git apply ../examples/08-shader-verification/seeded-change.diff
```

```bash
git add -A
```

```bash
git commit -m "Seeded change for review"
```

```bash
godot --headless --path godot --import
```

1. **Green first.** Before any agent runs, run the three original suites and `verify_flash.gd` at `--fixed-fps 60`, then `verify_flash.gd` at 30 and 144. Record, from your own logs, what green looks like on a broken commit.

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 30
```

2. **The review.** Save [Prompt 1](../examples/08-shader-verification/prompts/prompt-1-review.txt) as `prompt-1-review.txt` and give it to Claude Code with read-only tools, so the review cannot edit:

```bash
claude -p "$(cat prompt-1-review.txt)" --allowedTools "Read,Glob,Grep,Bash(git:*),Bash(godot --headless:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose > review-claude.jsonl
```

Read the review against the code. Mark each claim **observed** (the agent ran something and quoted its output) or **asserted**.

3. **The evidence.** Give [Prompt 2](../examples/08-shader-verification/prompts/prompt-2-evidence.txt) to Claude Code. It asks for a spec oracle (`verify_flash_spec.gd`), a CPU colour model (`flash_model.gd`), a bench (`flash_bench.tscn`) with a headless structure test, and `BENCH.md`. If your session limit stops you, as it stopped the book's run, copy the record's files from [its tests folder](../examples/08-shader-verification/tests/) and `BENCH.md` from [its files folder](../examples/08-shader-verification/files/), taking the agent's oracle, `verify_flash_spec.agent.gd`, not the corrected one, and say so in `FRICTIONAL.md`.

4. **Test the test.** Keep a second copy with the Chapter 6 versions of `player.gd` and `clawd_flash.gdshader`: the known-good code. Run the oracle on both copies at 30, 60 and 144. It must pass on known-good code and fail on the seeded change. If it rejects known-good code, the oracle is wrong: work out the tolerance the engine's frame and physics clocks force, change it by hand, and commit that change on its own with the reason. At 60 fps no tolerance separates the two: a 33-frame counter and a 0.55 s countdown are the same function there.

5. **The bench (HUMAN CHECK).** In Godot 4.7.2, open `res://tests/flash_bench.tscn`; its `@tool` script draws in the 2D view. Screenshot it with the seeded and the known-good shader, at the same zoom, with no colour management in your screenshot tool. On each copy, sample one pixel inside the body and one inside an eye, and compare with `flash_model.gd`'s table, allowing one step per channel at 0.5. The documentation predicts the seeded shader loses the body and eye colours at 0.0; the record's agents predicted white. Your screenshot decides.

[Prompt 3](../examples/08-shader-verification/prompts/prompt-3-fix.txt), the fix, is optional; the known-good copy can stand as the fixed version.

### Part B — a change Claude Code makes to your Assignment 5 effect

**1. The change, made without telling you.** In your game repository, save this prompt as `a6-seed-prompt.txt`:

```text
Read CLAUDE.md first. Create a branch named a6-change from the tag a5
and work only there; do not change main or any tag.

Make one plausible but incorrect change to the effect specified in
CLAUDE.md (its shader or the code that drives it), the kind a careful
reviewer could merge. Choose it from one of these families, whichever can
really occur in this code:
- wrong input: start from a value that does not carry the object's color;
- color space: a missing or wrong source_color or hint_normal;
- alpha: apply alpha twice under the default blend mode;
- coordinates: mix the UV and FRAGCOORD conventions;
- time: count frames, or key the effect to the global TIME.
The change must parse, keep every uniform name, and pass every existing
test at --fixed-fps 60. Commit it with a message, and any code comments,
that give a respectable reason for the change and do not describe the
defect. End your reply with the family, the exact lines, and the
consequence you expect a player to see or a test to measure.
```

Run it non-interactively, so the reply lands in a transcript outside the repository:

```bash
claude -p "$(cat a6-seed-prompt.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot --headless:*),Bash(git:*),Bash(ls:*)" --max-turns 40 --output-format stream-json --verbose > ../a6-seed-session.jsonl
```

Do not open `../a6-seed-session.jsonl` until your verdict is committed. Read `git log` and `git show a6-change` as a reviewer would. If the run ends without an `a6-change` commit, record that and rerun in a fresh session.

**2. Green first.** On `a6-change`, run your whole suite at `--fixed-fps 60`, then your timing checks at 30 and 144, and record the results.

**3. The evidence, plan first.** An optional read-only review may come first: Prompt 1 in a fresh session, with the names changed to yours. Then:

```text
Do not fix anything. The branch a6-change changes the effect specified
in CLAUDE.md. Build evidence that decides whether it breaks the spec.

First propose, without editing:
- for each spec rule, a controlled input that separates a correct result
  from a wrong one, and whether a headless check or a human check on a
  display can observe it;
- a timing check that compares each driven uniform with the spec's own
  rule (not with the current code), sampled by a node that runs after
  every other _process in the frame, through a real game event, at
  --fixed-fps 30, 60 and 144, with a tolerance justified from the
  engine's frame and physics clocks;
- a CPU model of the spec's color arithmetic, not of the current shader,
  that prints predicted values for my controlled inputs;
- a bench scene: copies of the shaded object at fixed uniform values on
  the game's real background (for a 3D effect, also a fixed camera and
  fixed lights), with no gameplay, input or timers, for me to screenshot
  in the editor, and a headless test of its structure.
After I approve, write them on a branch named a6-evidence made from the
tag a5, run each with --headless against a5, and show the real output.
Do not edit the shader, its driver or the existing tests. Do not commit.
```

Commit the agent's evidence unedited, then your corrections separately.

**4. Test the test.** Make a scratch branch from `a6-change`, merge `a6-evidence` into it, and run every new check there too. Each check must pass on `a6-evidence` (your Assignment 5 effect) and fail on the scratch branch (the change), or you must explain why its rung cannot see this change. A check that rejects your Assignment 5 effect is wrong: fix it by hand, in its own commit, with the reason. Never merge the scratch branch into main.

**5. Observe (HUMAN CHECK).** Open the bench in the editor on `a6-evidence` and on the scratch branch. Screenshot both, sample your named pixels, and compare with the model. For a timing change, also watch the effect in normal play at your display's refresh rate.

**6. Verdict, then the answer.** Write the verdict (merge or do not merge) and its findings in `audits/part-b/AUDIT.md`, and commit it. Only then open the transcript and add a dated reconciliation: did the agent's stated consequence match what you observed? An agent's description of its own defect is a claim like any other. If your evidence shows no observable defect at your controlled inputs, that is a legitimate finding; report it and say what input might still expose one.

**7. Resolution.** Do not merge `a6-change`. Merge `a6-evidence`, with your corrections, into main, so the oracle, model and bench protect your effect from now on.

### What the agents are likely to get wrong

Each row happened in the runs behind Chapters 6 and 8.

| Recorded mistake | What catches it |
|---|---|
| A review stated an unobserved consequence as fact: "Godot 4 provides a default 1×1 white texture". | Marking it asserted; the bench decides. |
| A review ranked an implementation-coupled test failure "CRITICAL", above the player-visible regression. | Asking which spec rule each failure breaks. |
| "Not yet run; expected to fail" at the frame rate that mattered. | Running it. |
| An oracle's tolerance rejected correct code at 144 fps: error 0.0369 against 0.0303. | Testing the test against known-good code. |
| A test called the update function directly, so the frame rate stopped mattering. | Driving the state through real frames. |
| An agent-written `FRICTIONAL.md` entry credited a named person with work that person did not do, twice. | Reading who it says did the work. |

## 3. Use It

Record actual results in `TEST-REPORT.md`, with source revisions, Godot version and renderer, one section per part:

| Check | Evidence to collect |
|---|---|
| Green before review | Every existing suite at 60 fps on the change, with counts and `SHADER ERROR` lines, before any agent ran. |
| Frame-rate sweep | Timing checks at 30, 60 and 144: first and last values, largest gap. |
| Agent claims | Each review claim marked observed or asserted, with its evidence line. |
| Oracle tested both ways | Known-good and changed code at three rates, pass or fail with the measured error; any tolerance change and its reason. |
| CPU model | Predicted values from the spec for every pixel you sample. |
| Bench structure | The headless bench test's result, and why it cannot see a shader defect. |
| Bench observation (HUMAN CHECK) | Screenshots with known-good and changed shaders; sampled hex beside the model's. |
| In play (HUMAN CHECK) | Where the defect shows in normal play, if it does, and at what refresh rate. |
| Reconciliation (Part B) | The verdict commit, then the agent's stated defect beside what you observed. |

Include at least one documented inspect-and-revise cycle driven by an observation, such as an oracle corrected or a prediction revised after a screenshot. Do not delete a failing assertion or weaken an expected result to obtain a green report. If another person reviews your audit, record their actual words; do not invent a reviewer.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier. It pairs each code excerpt with its visible result: here, the changed lines, then your bench screenshots side by side, and recorded test output for the timing rungs. Ask Claude Code to read the installed skill instructions and follow them. If your checkout lacks the skill, request the course-provided version.

Make **one** landscape film that:

1. Shows your Part B change as a reviewer receives it: the commit message and the changed lines.
2. Shows why the usual checks were green, and what that green could not see.
3. For each finding, shows the controlled input and its prediction, then the observed output.
4. Shows a check passing on known-good code and failing on the change.
5. Shows your Part A bench result, seeded beside known-good, and whether it matched the documented and the agents' predictions.
6. States the verdicts, what the evidence does not establish, what each agent observed and what it asserted, the human and AI contributions, and the revisions shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed editor views, recorded test output and held frames; never present a reconstruction as a screenshot. Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. There is no minimum runtime. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**. The film is part of the 60-point category below, not a substitute for the audits.

### Post the version on GitHub

Your submitted source includes:

- `audits/part-a/` and `audits/part-b/`, each with `AUDIT.md`, logs, screenshots, and review transcripts under about 1 MB (otherwise a labelled excerpt). Part A adds the files you or your agent wrote and your tolerance diff, and no copy of walker-jumpman-clawd.
- The `a6-change` branch, unmerged, and the seed transcript, copied into `audits/part-b/` after your verdict.
- On main: the merged evidence (oracle, model, bench, bench test, and a `BENCH.md` procedure for your effect).
- `README.md` with this assignment's section, `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, and `SOURCES.md`.
- The film's beat sheet, script/prompts, and evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Commit in the order the work happened: the agent's change, your green-before-review logs, the agent's evidence unedited, your corrections, your verdict, the reconciliation, the merge. If an agent writes a `FRICTIONAL.md` entry for you, read who it says did the work. Push `a6-change` and `a6-evidence`, and tag the final submission commit on main **`a6`**.

## 5. Verify and submit to Canvas

Clone the `a6` tag into a fresh folder. Run `--import` once, then the merged evidence at its pinned frame rates; confirm it passes with no `SHADER ERROR` lines, that both branches are on the remote, and that every cited screenshot opens. A working local folder is not proof that everything was posted.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 6 - Audit a Plausible but Incorrect Shader Change
Student:
Project name:
GitHub repository URL:
Git tag and submitted commit SHA:
Part A: walker-jumpman-clawd base commit and seeded-change file:
Part B: a6-change commit SHA and the family my evidence found:
Part B: verdict, and whether it matched the sealed answer:
Source revisions shown in the film:
Godot version, renderer, and operating system:
Final film URL and filename:
Final film SHA-256:
Summary of my work:
Known limitations:
Changed games since Assignment 2 (yes/no; if yes, FRICTIONAL.md entry):
```

It is fine to render from a source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit. Canvas, GitHub, and the film must refer to the same submitted work; identify later changes as a new revision.

## Rubric — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| Frictional — honest log | 10 |
| GitHub version posting matching Canvas | 10 |
| Relative Quartile | 20 |
| **Total** | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|---|---:|
| Part A: your own baseline showing the suite green at 60 fps and the sweep failing at other rates, with logs (5); the agent review read against the code, each claim marked observed or asserted (4); the oracle tested on known-good and seeded code at three rates, any tolerance change reasoned and committed separately (5); bench screenshots with both shaders, sampled pixels compared with the model (6). | 20 |
| Part B: the change produced without your knowledge of its defect, kept off main, its transcript sealed until your verdict (3); controlled inputs and predicted values written before any evidence ran (5); evidence at the right rung, headless where a machine can observe the rule and bench screenshots where only a display can (6); each new check shown passing on your Assignment 5 effect and failing on the change, or a reasoned account of why it cannot (5); a verdict reconciled with the sealed answer, with your Assignment 5 behaviour intact on main (3). | 22 |
| Audit write-up: every finding in the ran / saw / shows / does-not-show form with its rung (5); verdicts that follow from observed evidence rather than from reading the diff, with each audit's limits stated (3). | 8 |
| Brutalist explainer: accurate account of the changes, the evidence and the verdicts (4); captured bench output and recorded test output shown after the lines they test (3); contributions and the evidence's limits stated (2); readable, audible final film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing automated check establishes at most rungs 1 to 4, never what the GPU drew, so a verdict on a visual defect without your screenshots is not supported.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible audit source and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted audits.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit walker-jumpman-clawd and the course record as your Part A starting point, collaborators, and tools. Describe what AI contributed to the seeded change, the reviews, the evidence, the script, and the narration, and what you personally predicted, ran, observed, corrected, or rejected.

The instructor or a TA may hand you a one-line shader change and ask which controlled input would expose it, what you predict, and which rung could observe it. Inability to explain reduces points under the relevant criteria. Opening the sealed transcript before your verdict, or recording a screenshot or sample you did not take, misrepresents verification; misrepresenting authorship or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.
