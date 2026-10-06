# Course build specification — CSYE 7270 Canvas course (Godot, Walker, Claude Code)

## Executive summary

**What this is.** The contract for turning the CSYE 7270 companion book (Chapters 0–15, already drafted and run for real) into a complete Canvas course: one lecture page, one links page and one ungraded practice assessment per module, plus a 100-point assignment every 10 days. Writers (human or agent) read it before drafting any course file.

**Why it exists.** On 2026-10-06 Professor Bear asked for all of the modules to be reworked "to have examples using Godot … and Claude Code. And Walker", built "step by step, modeled on the old Canvas course" (the Spring 2026 `.imscc`). The old course was a skeleton of short link pages (Unity, Unreal, Houdini) plus a few assignments. The new one keeps its shape (Lecture → Assignment → Links per module) and replaces its content with the Godot/Walker/Claude Code material the chapters already prove out.

**What it decides.** The module and assignment map, the exact file formats the Canvas builder reads, the voice, and the hard limits. It signs no gate and approves nothing.

---

## 1. Paths

Course root (call it `$C`): the root of this repository. Every path below is relative to it, and the build scripts resolve it themselves. The writers who built the first draft worked from an absolute path on the instructor's machine; that path is not part of the contract.

| Thing | Where |
|---|---|
| Companion chapters (read-only source of truth) | `$C/chapters/NN-slug.md` |
| Worked-example records (read-only) | `$C/examples/NN-slug/` |
| Chapter writing contract (voice, evidence standard, headless traps) | `$C/pantry/chapter-spec.md` |
| Module 1 lesson (the format already approved) | `$C/modules/01-walker-and-godot/lesson.md` |
| Assignments 1 and 2 (the format already approved) | `$C/assignments/01-extend-walker-jumpman.md`, `02-generate-art-sound-music-for-your-game.md` |
| Policies | `$C/prerequisites/ai-policy.md`, `assessment-policy.md`, `brutalist-godot-explainers.md`; `$C/assignments/rubrics/100-point-assignment.md` |
| Revised syllabus (text) | `$C/CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx` (the schedule table is the plan) |
| Old Canvas course, converted to plain text (read-only) | a plain-text extraction of the old `.imscc` kept outside the repository (pages named `wiki_content_*.txt`, assignments `g…_*.txt`); regenerate it by unzipping the export without `web_resources/` and running pandoc on each HTML file |
| Voice reference | `runtime/prose/teardown/PROSE.md` in the Brutalist toolkit (`github.com/nikbearbrown/brutalist.art`) |
| Course repo on GitHub (for links) | `https://github.com/nikbearbrown/csye-7270-building-virtual-environments` (blob URL form: `…/blob/main/chapters/NN-slug.md`) |

Always use absolute paths in shell commands. Write only the files you were assigned. Never edit `chapters/`, `examples/`, any `walker-*` folder, the DOCX, the `.imscc`, or any file you were not assigned. Never delete anything.

## 2. The course map

One module per week of the revised syllabus, plus Module 0 for setup. A graded assignment is due every 10 days (**Day 10, 20, … 100**; Day 1 is the first class day; Canvas dates govern). Assignments and modules are not one-to-one: an assignment covers every module released since the previous one.

| Mod | Wk | Folder | Title | Chapter | Assignment (due) |
|---|---|---|---|---|---|
| 0 | — | `00-start-here` | Start Here: the toolchain | `00-the-toolchain.md` | — |
| 1 | 1 | `01-walker-and-godot` | Walker and Godot | `01-walker-and-godot.md` | A1 Extend Walker Jumpman (Day 10) — written |
| 2 | 2 | `02-prompting-game-art` | Prompting game art (and sound) | `02-prompting-game-art.md` | A2 Generate Art, Sound, and Music for Your Game (Day 20) — written |
| 3 | 3 | `03-blender-mcp-to-godot` | Blender MCP to Godot | `03-blender-mcp-to-godot.md` | A3 (Day 30), with Module 4 |
| 4 | 4 | `04-scenes-collision-and-physics` | Scenes, collision and physics | `04-scenes-collision-and-physics.md` | A3 |
| 5 | 5 | `05-the-gdd-and-virtual-worlds` | The GDD and virtual worlds | `05-the-gdd-and-virtual-worlds.md` | A4 (Day 40) |
| 6 | 6 | `06-shader-foundations` | Shader foundations | `06-shader-foundations.md` | A5 (Day 50), with Module 7 |
| 7 | 7 | `07-materials-and-textures` | Materials and textures | `07-materials-and-textures.md` | A5 |
| 8 | 8 | `08-shader-verification` | Shader verification | `08-shader-verification.md` | A6 (Day 60) |
| 9 | 9 | `09-particle-effects` | Particle effects | `09-particle-effects.md` | A7 (Day 70) |
| 10 | 10 | `10-animation-foundations` | Animation foundations | `10-animation-foundations.md` | A8 (Day 80), with Module 11 |
| 11 | 11 | `11-animation-and-interaction` | Animation and interaction | `11-animation-and-interaction.md` | A8 |
| 12 | 12 | `12-audio-and-triggers` | Audio and triggers | `12-audio-and-triggers.md` | A9 (Day 90), with Module 13 |
| 13 | 13 | `13-profiling-and-optimization` | Profiling and optimization | `13-profiling-and-optimization.md` | A9 |
| 14 | 14 | `14-game-ai-and-systems` | Game AI and systems | `14-game-ai-and-systems.md` | A10 (Day 100), with Module 15 |
| 15 | 15 | `15-final-projects-brief-to-export` | Final projects: from brief to export | `15-final-projects-brief-to-export.md` | A10 |

Assignment files (`$C/assignments/`):

| # | File | Title | Covers | Required film (Brutalist skill) |
|---|---|---|---|---|
| A3 | `03-blender-prop-into-godot.md` | Build a Prop in Blender and Make It Work in Godot | Modules 3, 4 | `godot-gamedev`, `walker` modifier |
| A4 | `04-specify-and-build-a-3d-interaction.md` | Specify It, Then Build One 3D Interaction | Module 5 | `godot-gdd`, `walker` modifier |
| A5 | `05-shader-and-material.md` | A Shader and a Material That Say Something About Your Game | Modules 6, 7 | `godot-gamedev`, `walker` modifier |
| A6 | `06-audit-a-shader-change.md` | Audit a Plausible but Incorrect Shader Change | Module 8 | `godot-gamedev`, `walker` modifier |
| A7 | `07-particle-effects.md` | Two Particle Effects, Tuned and Priced | Module 9 | `godot-walkthrough`, `walker` modifier |
| A8 | `08-animation-and-state.md` | Animation Wired to Player Actions | Modules 10, 11 | `godot-walkthrough`, `walker` modifier |
| A9 | `09-audio-and-a-performance-budget.md` | Sound That Provably Plays, and a Frame You Can Afford | Modules 12, 13 | `godot-gamedev`, `walker` modifier |
| A10 | `10-final-project.md` | Final Project: From Brief to Export | Modules 14, 15 (and the whole course) | two films: `godot-walkthrough` and `godot-gdd`, `walker` modifier |

### The cumulative game (applies to A3–A10; state it, do not rename it)

From Assignment 2 on, every student builds **one game**: the one they chose in Assignment 2, in a repository whose name begins `walker-`. Assignments 3–10 each add one layer to that same repository and are submitted as a git tag (`a3`, `a4`, … `a10`) on it, so the final project is the sum of the semester rather than a restart. A student whose game is 2D adds a 3D scene to it when an assignment needs one (a 3D prop room, a 3D diorama, a 2.5D stage); a project may mix 2D and 3D scenes. Each assignment must work for any genre: ask for a *kind* of thing (a shader that communicates a game state), not a specific effect. A student may change games once, before Assignment 4, with a short written justification in `FRICTIONAL.md`; the tags then continue on the new repository and the change is stated in the submission note.

### Open course decisions (do not resolve them in the text)

- The syllabus line "a group project and an individual project" has no assignment yet. Write every assignment as an **individual** assignment and do not invent a group-project mechanism. The instructor will decide where a group project goes.
- `/gdd` (Walker's Zelda design skill) exists only in the local Walker checkout; public Walker `main` does not carry it, but does carry the reusable prompt `prompts/zelda-gdd.md`. Anything that depends on `/gdd` must say so and give the prompt as the fallback.
- The Brutalist `godot-*` skills are used from a course-provided checkout of `https://github.com/nikbearbrown/brutalist.art`; say "course-provided" and tell students to request the update if their copy lacks the skill.

## 3. Files each module owns

Under `$C/modules/<folder>/`:

| File | Required | What it is |
|---|---|---|
| `lesson.md` | yes | The Canvas lecture page. 2,200–3,400 words. Skeleton in §4. |
| `links.md` | yes | The Canvas "Helpful links" page. Format in §5. |
| `assessment.json` | yes | The ungraded practice assessment. Format in §6. |
| `lesson-2.md` … | only where named in your brief | An extra lecture page (Module 14 only: `labs.md`). |

Module 0 also owns two extra pages written by the instructor's assistant, not by you: `course-map.md` and the policy pages that already exist in `prerequisites/`. Do not write them.

## 4. Lesson skeleton (`lesson.md`)

Follow Module 1's discipline and its Predict → Build It → Use It → Ship It → Verify template. Headings are exactly these, in this order (Module 14 also gets `labs.md`; Module 0 differs, see its brief):

```
# Module N — Title

CSYE 7270 · Fall 2026 · Week W

## Executive summary
   What this module is, why it matters, what the student will build, what that build does and
   does NOT prove. 4–7 sentences, plain language, no jargon the student has not met.
   (Bear's rule: the executive summary is the first thing under the title, before any technical header.)

## The question
   One concrete puzzle or failure the module resolves (from the chapter's "The question").

## The ideas
   3–6 short subsections that teach the machinery (how it works and why it was designed that way).
   Official Godot documentation links (https://docs.godotengine.org/en/stable/…). Small tables and code welcome.
   Use the course vocabulary from Module 1: node, scene, scene tree, signal, script, collision shape, asset.

## The Walker example: <project name>
   What the build is, where to get it (public repo link), what its checks establish, what is
   still unverified. Real file paths. Real numbers from the chapter.

## Predict → Build It → Use It → Ship It → Verify
### 1. Predict      2–4 questions to answer in writing BEFORE delegating.
### 2. Build It     The exact prompt(s) to paste into Claude Code, in ```text blocks, copied from the
                    chapter's Build It section (the prompts that were really run). Shell commands in
                    ```bash blocks, ONE command per block. Say where Codex differs only if the chapter does.
### 3. Use It       What to do in the editor / the running game, what to observe. Mark every visual,
                    audible or feel judgment as a HUMAN CHECK.
### 4. Ship It      What to commit, what to log in FRICTIONAL.md, which Brutalist Godot film skill fits.
### 5. Verify       The headless command(s) and what a pass does and does not prove.

## What the agents got wrong
   The 2–4 most instructive agent mistakes from the chapter's "What we actually ran", each in
   2–3 sentences, and how it was caught. This is a teaching section: an AI's "done" is a claim.

## If you know Unity or Unreal
   A short table (Godot | Unity | Unreal) for this module's 5–7 key terms, plus 2–3 sentences on the
   biggest difference for an agent workflow (text a CLI agent can read and diff vs editor-only/binary).
   Link the chapter for the full comparison. Say once that Unity and Unreal were not run.

## Practice assessment (ungraded)
   3–5 open-ended questions (like Module 1's Verify list). One line pointing to the Canvas
   practice quiz. "Do not paste Claude's explanation as proof of your understanding."

## The next step
   Which assignment this module feeds (name it, say it opens in Module M and is due about Day D),
   or which module comes next. One short paragraph. Link the companion chapter here.
```

Rules for lessons:

- **Condense, do not copy.** The chapter is the long reading (4,000–8,000 words). The lesson is the class page: shorter, step-by-step, written to be followed at a keyboard. Re-express; keep every prompt, command and number exactly as the chapter has it.
- **Prompts and commands are the chapter's.** Copy each ```text prompt and ```bash command that the chapter reports it ran, byte for byte, including `--fixed-fps 60` and `timeout` wrappers. Do not "improve" a prompt, and do not invent one. If you want a prompt the chapter does not have, you cannot have it.
- **No fabrication.** A factual claim about Godot, Claude Code, Codex, Unity or Unreal must come from the chapter (which cites its source) or from official documentation you fetched today. Version numbers, benchmark numbers and dates come only from the chapter. If you cannot support it, leave it out.
- **Say who ran what.** Where the chapter reports a run, say "run on 27 September 2026 with Claude Code (or Codex)", never "we measured" about something nobody ran. Never present an unrun step as run.
- **Headless honesty.** Keep the chapter's rules: `--headless`, `--import` once, `timeout`, `--fixed-fps 60` for frame-counted tests, exit code 0 is not "no errors", a passing headless test is not a playtest.
- **Executive summary first** (§ above). No emoji. No hype or filler ("In this module we will explore"). Teardown register: take the thing apart, explain how each piece works, judge the design, admit limits. Address the student as **you**. Avoid first-person "I" (the course author speaks in the chapters; the lesson speaks for the course).
- **Canvas-safe Markdown.** GFM only: headings, paragraphs, lists, tables, fenced code with a language tag, links. No raw HTML, no images, no footnotes, no `<br>`. Link text must be meaningful. External links `https://` only. Links to files in this course repo may be written as relative paths (`../../chapters/…`); the builder turns them into GitHub URLs.
- **Course repo links resolve only after the repo is pushed.** That is expected; do not drop them.
- **Walker projects are public** at `https://github.com/nikbearbrown/walker-<name>` (except `walker-gui-bidi-and-font-features`, which is private and not used here). Link them, and say each keeps the upstream MIT license.
- **Do not name a book, chapter or course in anything a student might film.** (Not relevant to lessons, but the assignments' film requirements must not tell students to say "this course" in their films unless the assignment says so.) The lesson may of course point to the companion chapter by title and link.

## 5. Links page (`links.md`)

```
# Module N — Helpful links

## Executive summary
   One or two sentences: what is on this page and when to open it.

## Read first            the companion chapter (GitHub blob URL) + the lesson's own Walker projects
## Godot documentation   4–8 official pages for this module's ideas (docs.godotengine.org/en/stable/...)
## Walker projects       the public repos used, one line each on what to open them for
## Tools                 anything the module needs installed (name, official download/doc page)
## Going deeper          2–5 optional, well-known, still-live resources (talks, articles, papers)
```

Every entry: `- [Title](https://…) — one line saying what you would open it for.` 10–18 entries. **Every URL you did not copy from the chapter must be checked live today** with `curl -sIL -o /dev/null -w '%{http_code}' <url>` (or a fetch) and return 200. You may carry over still-relevant, engine-neutral links from the old Canvas pages (the converted text is in the old-course path in §1; do not carry Unity-only or Unreal-only links), but only if they pass the same check. Do not invent URLs; do not guess documentation page names.

## 6. Practice assessment (`assessment.json`)

Ungraded Canvas practice quiz (the syllabus's "Assessments"). Exactly this shape, indented 2 spaces:

```json
{
  "title": "Module N practice assessment",
  "description": "One or two plain sentences: ungraded; take it as often as you like; read the feedback.",
  "questions": [
    {
      "prompt": "Plain text question (no markdown tables). Code identifiers in backticks.",
      "choices": ["choice A", "choice B", "choice C", "choice D"],
      "answer": 2,
      "feedback": "Why the answer is right and why the tempting wrong choice is wrong. Cite the lesson section."
    }
  ]
}
```

Rules: **6 questions**, 4 choices each, exactly one correct, `answer` is the zero-based index of the correct choice. **Vary the position of the correct answer** (no position may hold more than 2 of the 6). No "all of the above" or "none of the above". At least 3 questions must test judgment ("which evidence would show X", "what does this passing test NOT prove"), not recall. Every question must be answerable from the lesson plus the chapter, and the correct answer must be literally supported there. Distractors must be plausible mistakes a student (or an agent) would actually make, taken from the chapter's agent errors where possible. Feedback is 1–3 sentences and teaches.

## 7. Assignments (`$C/assignments/NN-slug.md`)

Copy the shape of Assignments 1 and 2 (read both in full first). Required sections, in this order:

```
# Assignment N - Title                                  (hyphen, as in A1 and A2)

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. … (use A1's two lines: cadence + 10% daily late penalty; add "Suggested Canvas due date: Day D after the first class day.")

**Required viewing:** [AI Policy …](…)   (same link as A1)

## Executive summary
   What the student builds, what they hand in, how it is graded, and what it does not prove. 5–8 sentences.

## Your task
   The task, the cumulative-game rule in one short paragraph (§2), tool/cost rules (Claude Code via NEU,
   no paid services), project naming (`walker-` prefix), rights and provenance. Kind-of-thing requirements,
   not genre-specific ones.

## 1. Predict
## 2. Build It
## 3. Use It
## 4. Ship It — source and explainer
## 5. Verify and submit to Canvas
## Rubric — 100 points
## You must be able to explain it
```

Content rules for assignments:

- **Predict:** the written artefacts due before building (`CHANGE-BRIEF.md` with predicted failures, and anything else the task needs). Keep the originals; add revisions, do not rewrite.
- **Build It:** ask for work in inspectable increments; give a plan-first Claude Code prompt, as A1 does; say what must not change; say what counts as done. Point to the module lesson(s) and chapter(s) by name and link, and to the Walker projects that demonstrate the technique. Tell students what the agent is likely to get wrong, using the chapters' recorded agent mistakes.
- **Use It:** a table of checks with the evidence to collect (as A1), automated checks AND an actual human playtest, `TEST-REPORT.md`, at least one inspect-and-revise cycle, never delete a failing assertion to get green.
- **Ship It:** the required Brutalist film (skill and modifier from the table above; explain what the film must show and what it must say, as A1 does), the source/documentation list (`README.md`, `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md`, beat sheet, evidence), the git tag `aN`, and A1's media rules (no MP3/MP4 or files over 25 MB in GitHub; film filename and SHA-256 in the README). Do not require YouTube publication or a vertical Short.
- **Verify and submit:** run from a fresh clone of the tag; a `SUBMISSION.md` note in the same shape as A1's (adapt the field names to this assignment); the render-commit versus final-commit rule from A1; Canvas, GitHub and film refer to the same revision.
- **Rubric:** the 60 / 10 / 10 / 20 table; a task-specific subdivision of the 60 points as a table whose numbers **sum to exactly 60** (check the arithmetic); then the Frictional (10), GitHub version posting matching Canvas (10) and Relative Quartile (20) paragraphs, copied from Assignment 1 with only identifiers changed. Do not invent numeric quartile bands.
- **Honesty:** partial credit, "claims must be defensible", and one sentence on what a passing automated check does not establish for this task.
- Length: 2,000–3,500 words. Every file path, command and tool you name must exist in a chapter, an example record or a public Walker repo; verify by reading them.
- Do not tell students to run `walker` as an executable. Walker is a workflow and a set of instruction files; Claude Code is told to follow it.

## 8. Voice and hard limits

- Voice: Teardown register (see the voice reference and the Voice section of `pantry/chapter-spec.md`). Short sentences for clarity; longer ones to show how systems connect. No hype, no filler, no emoji.
- **No spend, no publishing.** No paid generation, no GitHub pushes, no commits, no Canvas calls, no YouTube.
- **No stubs.** Write every file in full or report that you could not.
- **Do not run Godot windows.** You write text; you do not need to run the game. If you run any Godot command to check a fact, use `--headless`, wrap it in `timeout 120`, and work on a scratch copy outside this repo.
- **Do not read or quote** the third-party books in the course root (`*Z-Library*`, `930723439-Game-AI-Made-Easy-*`).
- **Course folders carry no student names.** Do not write any student's name.
- When a source (chapter, example, Walker README) disagrees with this spec, trust the source, say so in your report, and do not paper over it.

## 9. Your report

Finish with a short report: the files you wrote (path and word count), anything you could not support and therefore left out, any error you found in a chapter or in this spec (quote the line), and any link you carried over from the old Canvas course.
