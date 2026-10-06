# FRICTIONAL — Assignment 2

## Entries

<!-- One entry per work session, newest last. Copy the block below. -->

### 2026-10-03 — Reading the assignment, setting up the project, drafting the concept

- **Date and what I was working on:** 2026-10-03. Read the Assignment 2 requirements, set up the project `walker-survival-shooting`, and drafted CONCEPT.md.
- **I tried / expected:** I wanted to turn my existing game design document (written in Chinese before this assignment, not in this repo) into the concept. The core is shooting, fighting monsters, layered map design, and the computer/tablet software.
- **What happened:** Claude's first draft invented the art reference notes, the audio direction, and a visual and a sound choice for every pillar. I rejected that version: anything Claude does not know should be asked, not made up, and large unknown parts should be left blank. I also asked that drafts be written in Chinese first and translated into English in one pass at the end.
- **What I did:** Answered Claude's questions and made the decisions. The map is open and the player decides what to do, but high-value areas are always guarded by monsters; the main risk is losing items on death. Third-person 3D (first person when aiming); low-poly gear and weapons; anime-style characters that are not cute, because the tone will be serious. Dark, cool colors; technology between the millennium and today in a military style; a thick, hard-edged rugged tablet. No music on the surface, only ambient sound; tense music only when a boss-level enemy spots you. No pause. Death is a black screen with a failure sound; extraction is a sound effect only. The music player overrides all background music. The start menu has a looping track; clicking Start rotates the camera from facing the seated character to the over-the-shoulder view, and the music stops. I kept three pillars: the tablet is gameplay, small but complex maps, and high-risk extraction. For the third pillar I decided there is no single visual or sound choice, because the risk comes from the whole design.
- **What Claude or another person contributed:** Claude (Claude Code) read my design document and the assignment, made the document templates, asked me questions, and organized my answers into the concept draft. No generative model has been used yet.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/CONCEPT.md`.

### 2026-10-03 to 2026-10-06 — Storyboard text

- **Date and what I was working on:** 2026-10-03 to 2026-10-06. Wrote the storyboard text.
- **I tried / expected:** The core action for this slice is opening the tablet.
- **What happened:** I separated the "tablet screen" (the tablet in the game world and how it sits in the character's hands) from the "computer screen" (what the player sees, including the tablet UI window). I defined three tablet states (not looking, one-handed, two-handed) switched by a short or long Tab press. One-handed shows a small window in the bottom-right corner (about 20–40% of the view) so you can read while walking; two-handed shows the tablet large and clear for full interaction, such as sorting the backpack. The tablet never pauses the game.
- **What I did:** Decided the panels. The start menu is set inside the subway base, with the character on a bench on the right and the title and menu on the left; clicking Start rotates the camera into the over-the-shoulder view, the character stands up, the menu fades out, and the music stops, which moves the player seamlessly into the safe house instead of showing a loading screen. The tablet comes out of a pocket or a belt pouch and gives a short startup beep; the camera stays over the shoulder, and the small window slides off the screen in two-handed mode. The asset slice takes place entirely in the subway base. I merged two panels into "sneaking through a dark lab", shown as a close-up on the main character with a mechanical monster. Success is any extraction; death is torso or head HP reaching 0; both return the player to the base. I stopped detailing the storyboard at this point to start the actual work.
- **What Claude or another person contributed:** Claude explained what a storyboard is, asked questions panel by panel, and wrote down my answers. Once Claude asked again about something I had already answered (how the small window leaves the screen), and it suggested camera angles I did not choose.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/STORYBOARD.md`. I asked the professor whether storyboard images may be AI-generated; the answer was yes, and they do not need asset-log entries. I will keep the final images and my intermediate edits.

### 2026-10-06 — First upload of my ideas

- **Date and what I was working on:** 2026-10-06. Uploading my concept and storyboard to the course repository.
- **I tried / expected:** Put my ideas on GitHub first.
- **What happened:** When I said "start the real work", Claude started writing Godot code (project file, input bindings, tablet state logic) without asking me. That part is my job, so I stopped it and had all of it deleted. None of that code is in this upload.
- **What I did:** Decided to work in my own working folder and upload to `fall-2026/zhe-l/assignment-2/` in English.
- **What Claude or another person contributed:** Claude translated the concept, storyboard, and this log into English and prepared the commit.
- **What I understand now / still do not understand:**
- **Evidence and next step:** This commit. Next: the character sheet and the change brief.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-10-06 | Add concept, storyboard text, and design log for Assignment 2 |
