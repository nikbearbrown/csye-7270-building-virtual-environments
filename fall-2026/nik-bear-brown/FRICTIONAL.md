# FRICTIONAL — Professor Bear's course log

## Executive summary

**What this is.** The honest process log for the work in this folder, written the way the course asks students to write theirs: what was tried, what went wrong, what changed, and who did what, the human or the AI.

**What it records so far.** Everything I said on 2026-09-25 about CSYE 7270 outside my own assignment work: writing Assignment 2, putting the course on GitHub, and setting up a folder for everyone in the class. My Assignment 2 example has its own log: [Assignment 2](assignment-2/FRICTIONAL.md).

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
