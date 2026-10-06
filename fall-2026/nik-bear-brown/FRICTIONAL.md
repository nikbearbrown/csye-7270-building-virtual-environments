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
