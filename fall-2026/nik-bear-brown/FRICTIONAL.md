# FRICTIONAL — Professor Bear's course log

## Executive summary

**What this is.** The honest process log for the work in this folder, written the way the course asks students to write theirs: what was tried, what went wrong, what changed, and who did what, the human or the AI.

**What it records so far.** Everything I said on 2026-09-25 about CSYE 7270 outside my own assignment work: writing Assignment 2, putting the course on GitHub, and setting up a folder for everyone in the class. On 2026-09-27 I asked for the companion-book chapters to be adapted to Godot. My Assignment 2 example has its own log: [Assignment 2](assignment-2/FRICTIONAL.md).

Everything I say in a session is recorded here or in the matching assignment's log. Pushes are listed at the bottom of each log.

---

## Entries

### 2026-09-25 — Setting up the example folder

- **Date and what I was working on:** 2026-09-25. Creating my own example folder in the CSYE 7270 repository, matching the one in the INFO 7375 repository.
- **I tried / expected:** A folder under `fall-2026/` named with the `first-name-last-initial` convention used in INFO 7375, with a README, a CLAUDE.md, and this log.
- **What happened:** My first request named the INFO 6205 repository by mistake, and Claude Code built the folder there. I caught it before anything was committed, and the INFO 6205 changes were undone. The CSYE 7270 repository had no `fall-2026/` folder yet, so this also creates it with a one-row roster.
- **What I did:** Asked Claude Code to create `fall-2026/nik-bear-brown/` with the same three files as my INFO 7375 folder, adapted to CSYE 7270, and a `fall-2026/README.md` roster with only my folder for now.
- **What Claude or another person contributed:** Claude Code (Opus 5.5) wrote the three files and the roster, adapted from my INFO 7375 folder. I asked for the folder; I have not yet reviewed the wording.
- **What I understand now / still do not understand:** Nothing new yet; this is setup.
- **Evidence and next step:** This commit. Next: my first assignment example.

### 2026-09-25 — What I asked for today: Assignment 2, the course repo, and the class folders

- **Date and what I was working on:** 2026-09-25. Writing Assignment 2 for CSYE 7270, putting the course materials on GitHub, and setting up the class folders.
- **I tried / expected:** My requests, in order, in my words (dictation errors fixed):
  1. "I need an assignment to use generative models to create game art, sound and music … use this as a template; a storyboard and character sheet should be created; a Frictional log of the thinking in the design." (The template was Assignment 1.)
  2. "Push this csye-7270-building-virtual-environments/ to https://github.com/nikbearbrown/csye-7270-building-virtual-environments.git"
  3. "No Canvas export." · "No third-party books."
  4. "Why HTML if on GitHub? Md files."
  5. "No, not Walker Jumpman's art … any art, hopefully for the game they want to build."
  6. "Suggest some poses for the character sheet … a full sheet not required but at least 10 distinct poses."
  7. "Storyboard should be at least 3 views (close-ups etc.) and three angles, and indicating motion on at least 2 frames … their choice, but 16:9 is recommended."
  8. "Create a directory for me like this, just me, nik-bear-brown … in the info-6205 GitHub." Then: "Whoops, wrong repo, this one: nikbearbrown/csye-7270-building-virtual-environments."
  9. "Yes, push, and update FRICTIONAL for my assignment 2." (This granted standing push approval for this folder.)
  10. "Can you hear me speak?"
  11. "These are Frictional notes for Assignment 2 … assignment three will have its own Frictional … its own subfolder; each subfolder, assignment one, two, three, four, has its own FRICTIONAL.md."
  12. "Lower kebab case, first name last initial, and a folder for everyone in the class." (With the Canvas people list pasted.)
  13. "Create an assignment-2 folder in each of those." · "Also put a blank FRICTIONAL.md into all of the assignment two folders."
  14. "Everything I say goes into the FRICTIONAL.md log."
  15. "Push the latest updates to Assignment 2 to GitHub, and then I'll put it in Canvas." (It was already pushed; the Canvas HTML paste was rebuilt from that version and copied to my clipboard.)
  16. "Look at AAX … we created two character sheets for Dorothy … use the riff skill from brutalist.art, and also the video that we created, to show that in spite of creating a character sheet, which looked pretty on model for all the pictures, when we actually tried to render it, the film looked pretty off model. For this assignment it's not to render it yet, just to be aware of that. The assignment is just to make the sheet. Comment on the sheet, whether it looks on model or off model. In the video, riff in a much more succinct way using the Liam persona: show the character sheet, talk about it, riff about it. Then just play the video as is, with the music." Then: "All the other images in the directory are slices I took of the actual video."
     - Claude Code built the film in `youtube/claude-liam-csye-7270-character-sheet-off-model/`: the two sheets judged on model, the film played unedited with its music, then a sheet-versus-film comparison from my slices (face and hair drift, costume holds best), verdict, and a Your Turn prompt. It dropped a claim about the hem getting longer because the frame cut off at the hips. The AAX folder was only read.
  17. "Write a YouTube title, description, keywords, and hashtags." (Saved beside the film as `claude-liam-csye-7270-character-sheet-off-model-youtube.md`; not published.)
- **What happened:**
  - Assignment 2 went through three versions: first tied to Walker Jumpman's art, then retargeted to each student's own game (my correction in 5), then given the 10-pose and storyboard rules (6, 7).
  - The first push excluded the Canvas export and the two third-party books before I said so; my two messages confirmed it. The QC frame sweeps (1.4 GB) were also left out.
  - The generated HTML Canvas pastes had gone to GitHub with the Markdown; I asked why (4), and they were taken off.
  - I named the wrong repository (8). Claude Code built the folder in INFO 6205 first; nothing was committed there, and it was undone.
  - Claude Code can't hear me (10): it only receives text, so dictation reaches it already transcribed.
- **What I did:** Made each request and correction above, and approved the pushes.
- **What Claude or another person contributed:** Claude Code (Opus 5.5) wrote Assignment 2 and each revision, the pose menu and storyboard rules, the `.gitignore`, the class folders and roster, the README and blank log in each `assignment-2` folder, and this entry. Its judgment calls, for me to check: the 60-point split (12 / 14 / 14 / 10 / 10); surnames for two multi-part names from Canvas's sort order (`kiran-r`, `abhinav-g`); leaving out the two Canvas observers with no section; listing me once as `nik-bear-brown`.
- **What I understand now / still do not understand:** Nothing new about the material; this was setup.
- **Evidence and next step:** Commits on `main` from today (the push tables below and in the Assignment 2 log). Next: my own Assignment 2 work (ants, a parasite, a termite).

### 2026-09-27 — Adapting the course chapters to Godot

- **Date and what I was working on:** 2026-09-27. Turning the old Unity/Unreal course (the Spring 2026 Canvas export) into hands-on Godot chapters for CSYE 7270.
- **I tried / expected:** My request, in my words (dictation errors fixed): "This course needs to be adapted for Godot. It is hands on, and needs a chapter and example for doing this with a CLI like Claude Code or Codex, the Walker tool and Godot. Look at the .imscc for what to build. The end of each chapter should have a section of similarities/differences doing the same thing with Unity Engine, and similarities/differences doing the same thing with Unreal Engine. Use the existing Walker Godot builds, or adapt them if useful." I pasted the list of `walker-*` projects with it.
- **What happened:**
  - Claude Code read the Canvas export's modules and assignments. It followed the fifteen-module sequence already in my revised Fall 2026 Word syllabus, which was built from that export, and added a Chapter 0 for the command-line toolchain. It drafted all sixteen chapters in the course repository's `chapters/`, with a worked-example record for each in `examples/`. Every chapter ends with "Doing the same thing in Unity" and "Doing the same thing in Unreal Engine."
  - Every hands-on example was really run with Claude Code and/or Codex on copies of the Walker projects, and then checked with a separate headless Godot command. The agents' mistakes are kept in the record. Examples: in Chapter 0, both agents ran the Pong regression test without `--fixed-fps 60`, saw it fail, and explained the failure wrongly. In Chapter 4, an agent's test still passed after its shield was shortened from 3 s to 0.5 s. In Chapter 15, an agent said no test touched the player's real save file, when two did.
  - Claude Code's usage limit was reached during the day, so Codex finished several examples. The chapters say which tool did which step.
  - A separate session published the `walker-*` repositories on GitHub the same day. The chapters now link them. The Walker `/gdd` skill that Chapter 5 uses is not in the public Walker repository yet.
- **What I did:** Made the request above. I have not yet reviewed the chapters.
- **What Claude or another person contributed:** Claude Code (Opus 5.5) planned the chapters, wrote the writing contract and course map, wrote Chapter 0, and coordinated seven Claude Code sub-agents that wrote Chapters 1–15. Nested Claude Code (Sonnet 4.6) and Codex sessions did the hands-on examples. Judgment calls for me to check: following the syllabus's module order plus a Chapter 0, rather than one chapter per old Canvas module; chapter lengths (about 6,000–15,000 words); and showing the agents' mistakes so prominently.
- **What I understand now / still do not understand:** Not yet recorded; waiting on my review.
- **Evidence and next step:** The chapters, examples and `pantry/chapter-spec.md` are in the course repository but not committed or pushed. They wait for my word. Next: review the chapters, do the human checks each one lists, and decide whether to publish the `/gdd` skill.

### 2026-10-06 — Reworking every module into a full Godot, Walker and Claude Code course

- **Date and what I was working on:** 2026-10-06. Turning the old Spring 2026 Canvas course (the `.imscc`) into a complete new CSYE 7270 course, module by module, built around Godot, Walker and Claude Code.
- **I tried / expected:** My request, in my words (dictation errors fixed): "Look at the Building Virtual Environments course, CSYE 7270. In particular, the Canvas IMSCC file. Also, look at the Walker directory. Walker helps use Claude Code to build game art, to build animations, to build games using Godot. All of the modules need to be reworked to have examples using Godot to do it, and Walker. So, for example, building a game design document, doing animation, doing particle effects, doing whatever with Godot and Claude Code and Walker. Take your time. Build out a full course, step by step, modeled on the old Canvas course, integrated with Walker, Godot and Claude Code." I pasted the path of the `.imscc`, the path of the Walker folder, and a listing of the course folder.
- **What happened:**
  - Claude Code found that most of the base already existed: the sixteen chapters, Module 1, and Assignments 1 and 2. What was missing was Modules 0 and 2–15 as Canvas lecture pages, Assignments 3–10, anything to test understanding, and a way to get it into Canvas.
  - It read the old export's modules, pages, assignments and quizzes. The old course was a skeleton: most pages were short link lists, and only three pages (Game AI, Unity ML-Agents, CgFX) had real teaching text. It kept the skeleton (Lecture, Assignment, Links per module) and replaced the content.
  - It built: 17 lecture pages (Module 14 has a second page for its labs), 16 Helpful-links pages, 16 ungraded practice quizzes (96 questions), Assignments 3–10, a course map, an old-to-new map, and a script that builds an importable Canvas package and per-page HTML pastes. Twelve sub-agents wrote the pages and assignments from the chapters.
  - Then independent sub-agents checked it. Three answered all 96 quiz questions blind and matched the answer key, but they also found the quizzes could be passed by length alone: the correct choice was the longest in 81 of 96 questions. The wrong choices were rewritten (now 17 of 96) and a second blind check matched 96 of 96 again. Other agents checked every number and quotation in the lessons against the chapters (56 fixes) and the assignments against the chapters and the Godot docs (12 fixes), and 230 links were checked live.
  - The checks also found errors in my chapters, which were not edited. The main one: twelve chapters still say a Walker build "is not public" right beside a paragraph saying it is public. The full list is in `STATUS.md`.
  - Things it decided without asking, for me to check: an assignment appears in the first module it covers (and again in the second); every assignment is individual, because the group project has no assignment yet; the Canvas package imports unpublished with no due dates; and Assignment 4 tells students to keep the unreleased `/gdd` skill out of their pushed repositories.
- **What I did:** Made the request above. I have not yet reviewed any of it.
- **What Claude or another person contributed:** Claude Code (Sonnet 5.5) planned the course, wrote the build contract, the checker, the packager, the course map and the old-to-new map, restructured Module 1's lesson (my 10 September text kept; the original is in `pantry/backups/`), and coordinated sub-agents (Sonnet 5.5 and Opus 5.5) that wrote and checked the modules and assignments. Nothing was run in Godot except one headless test of `walker-2d-bullet-shower`. Not checked by me.
- **What I understand now / still do not understand:** Not yet recorded; waiting on my review. Questions for me are in `STATUS.md`, the biggest being that Assignment 10 is probably too much for its 8 to 10 days.
- **Evidence and next step:** `STATUS.md` ("Canvas course build — 2026-10-06"), `modules/README.md`, `canvas/README.md`, `canvas/OLD-TO-NEW.md`. Everything is in the course repository but not committed or pushed, except this log. The Canvas package has never been imported into a live Canvas. Next: review it, decide the open questions, and push when ready.

### 2026-10-06 — Pushing the course repository so I can read it

- **Date and what I was working on:** 2026-10-06. Getting the rebuilt course, the chapters and the examples onto GitHub so I can read them there.
- **I tried / expected:** My request, in my words: "Push the course repo. I'd like to read it on GitHub."
- **What happened:**
  - Because the repository is public, Claude Code checked what would go up first. It found local file paths in its own build spec and made them repository-relative. Two recorded sessions matched a key pattern; the matches were pieces of base64 text, not keys. One Codex transcript still shows file paths from Blender's own error output, which is how it was recorded. Nothing was over 5 MB.
  - It left one thing out: the build files for my 25 September on-model/off-model riff film (`youtube/claude-liam-csye-7270-character-sheet-off-model/`), because I asked for the course and not that film. It stays on my machine until I say otherwise.
  - The remote had moved while I was away (a student's Assignment 2 pull requests were merged), so my earlier log commit was rebased onto it. Nothing was overwritten.
  - It pushed three commits: the Canvas course (modules, Assignments 3 to 10, build spec, checker, packager), then the chapters and examples, then this log.
  - A second session I started to fix the chapter errors was editing the chapters at the same time. The chapters on GitHub are as they were at the push; its fixes will arrive in a later commit.
- **What I did:** Asked for the push.
- **What Claude or another person contributed:** Claude Code (Sonnet 5.5) ran the pre-push checks, made the commits and pushed. I have not yet read anything on GitHub.
- **What I understand now / still do not understand:** Not yet recorded; I have not read it.
- **Evidence and next step:** The three commits on `main` from today. Next: read the course on GitHub, then decide the open questions in `STATUS.md`.

### 2026-10-06 — A very basic Blender assignment as Assignment 3

- **Date and what I was working on:** 2026-10-06. Changing the next CSYE 7270 assignment (Assignment 3) into a gentle first Blender assignment.
- **I tried / expected:** My request, in my words (dictation errors fixed): "The next assignment for CSYE 7270 should be a very basic one, using Claude, the Blender MCP and Blender to make a very simple model. The basic idea behind the assignment is just to get familiar with the Blender interface, and how Claude plus the MCP plus Blender can make game assets. The 20% as usual will be awarded for how well it's done, but 80 points for basically building a moderately complex, not too complex, model, because this is their very first time typically using Blender or 3D software. So a 100-point assignment, with the 20-point qualitative score as usual. The basic idea is that they should use Claude, the Blender MCP and Blender to make a game asset or two, let's say three simple 3D assets, and preferably some that they think for their game."
- **What happened:**
  - Claude Code had already written an Assignment 3 on a Blender prop. It was much heavier: colliders, physics layers, and tests that had to catch deliberate breakage. It replaced it with your version and saved the old one in `pantry/backups/` so it can be reused later.
  - The new Assignment 3 is "Your First 3D Game Assets with Claude, the Blender MCP, and Blender": three simple assets for the student's game, built with Claude through the MCP, at least one edit made by hand in Blender's window, six notes on the interface in the student's own words, each asset exported as `.glb` and shown in a small Godot 3D scene. It keeps the 60 / 10 / 10 / 20 split and the required film. Assignment 3 now covers Module 3 only, so Module 4 (collision and physics) has no assignment of its own until Assignment 4.
  - An independent check found that the MCP project had changed nine days after the chapter was written. Version 2.1.1 became 2.1.9, three tools the chapter names were removed, the add-on now starts its server automatically, and the README now leads with a one-line installer. The assignment and Module 3's lesson were corrected. Nobody on the course has run the MCP route, so the assignment tells students that, and lets them fall back to the script route after about two hours.
  - Claude Code settled some things without asking: a ceiling of six shapes and 500 triangles per asset so students' work is comparable; the film is kept because the syllabus requires one per assignment; a student whose honest MCP attempt fails can still earn up to 6 of the 8 process points.
- **What I did:** Made the request above.
- **What Claude or another person contributed:** Claude Code (Sonnet 5.5) wrote the assignment and updated the lesson, course map and package; an Opus 5.5 sub-agent fact-checked it against the project's live README and the Blender manual and fixed seven errors. Not checked by me.
- **What I understand now / still do not understand:** Not yet recorded; waiting on my review. I still need someone to run the MCP route once before release.
- **Evidence and next step:** `assignments/03-first-3d-assets-with-blender-mcp.md` and the "Canvas course build" section of `STATUS.md`. The new files are in the course repository but not committed or pushed. Next: read the assignment, run the MCP route once, and decide whether it is the right length.

### 2026-10-06 — A film of Assignment 3 (lecture skill, Liam persona)

- **Date and what I was working on:** 2026-10-06. Making a film of the new Assignment 3, "Your First 3D Game Assets with Claude, the Blender MCP, and Blender".
- **I tried / expected:** My request, in my words (dictation errors fixed): "Use the lecture skill, Liam persona, to make a film on this." I pasted the full text of Assignment 3 below it.
- **What happened:**
  - Claude Code read the whole assignment and planned one film in seven acts that follows the assignment's own order: three simple assets, learn Blender's window first, write the brief before you build, connect Claude to Blender, build the assets, export / import / check, ship it and how it is graded. Liam narrates in for me. It is 80 beats and 13 minutes 21 seconds, and it is now built as a 4K master that passes every machine check (visual QC, type check, bookend check). I have not watched it.
  - A sub-agent ran the real tools to get pictures that are not drawings: it built the crate, the lantern and the coin with a Blender script, captured the real Blender window, and ran a headless check in Godot on them. The three assets measure 60, 202 and 180 triangles, under the 500 limit.
  - That evidence caught four things the assignment and my first narration got wrong. A crate whose origin is in the middle sinks half its height at floor level, and a crate lifted by exactly that amount sits, so the floor-gap check passes it and only an origin check catches it. The installer in the MCP project's README lets you pick which client to set up; it does not set up every client. The next version after 2.1.1 came three days later, not nine; 2.1.9 came nine days later. Blender's factory settings keep one backup, `.blend1`. The narration is corrected; the installer wording in the assignment is corrected too.
  - The film cannot show the MCP route running, because nobody on the course has run it. Those steps are shown as the typed commands, labelled "documented, not run". The assets in the film come from the script route, and the film says so.
- **What I did:** Made the request above.
- **What Claude or another person contributed:** Claude Code (Sonnet 5.5) planned the acts and wrote the narration; Opus 5.5 sub-agents built the pictures, one act each, and fixed the six pictures the type check rejected. Nothing is published, and nothing will be without my word. The film folder is on my machine only; it is not committed or pushed.
- **What I understand now / still do not understand:** Not yet recorded; I have not watched it. I still need someone to run the MCP route once before release.
- **Evidence and next step:** `youtube/claude-liam-lecture-first-3d-assets-blender-mcp/` (narration, `ACTS.md`, `EVIDENCE-INDEX.md`). Next: I watch the master, someone runs the MCP route once so the "documented, not run" steps can become real, and only then does anything get posted. `BUILD-LOG.md` in the film folder lists the open items.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-09-25 | Add fall-2026 roster and nik-bear-brown example folder |
| 2026-09-25 | Move Assignment 2 notes into assignment-2/ with its own log |
| 2026-09-25 | Add assignment-2 folders for everyone; rename mine to match |
| 2026-09-25 | Record everything I said today; rule: all my words go in the log |
| 2026-09-25 | Log my request to post Assignment 2 to Canvas |
| 2026-09-25 | Log my request for the on-model/off-model riff film |
| 2026-09-25 | Log my request for the riff film's YouTube text |
| 2026-09-27 | Log my request to adapt the course chapters to Godot |
| 2026-10-06 | Log my request to rebuild the course modules into a full Godot, Walker and Claude Code course |
| 2026-10-06 | Log my request to push the course repo to GitHub |
| 2026-10-06 | Log my request for a very basic Blender assignment as Assignment 3 |
| 2026-10-06 | Log my request for a film of Assignment 3 |
| 2026-10-06 | Update the Assignment 3 film entry: master built, nothing published |
