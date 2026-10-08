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

### 2026-10-03 to 2026-10-07 — Designing the main character; character sheet and change brief

- **Date and what I was working on:** 2026-10-03 to 2026-10-07. Designed the main character and wrote `CHARACTER-SHEET.md` and `CHANGE-BRIEF.md`.
- **I tried / expected:** I first tried a local model (ChenkinNoob-XL V0.5 in ComfyUI) with a general "anime tactical girl" prompt, then switched to a design conversation with ChatGPT. There I described the character, had ChatGPT produce drafts, judged each draft, and changed the design. I expected to end with one clean turnaround I could use as the reference for every pose and for the 3D model.
- **What happened:** The local front-view tries (CHAR-REF-00) had the wrong hair and trousers or glossy leggings. The local turnarounds (CHAR-REF-02) were far from what I wanted: the first looked like a 3D render instead of an anime sheet, and the later ones still built the plate carrier and thigh holsters into the character. The ChatGPT drafts improved step by step, but each one showed a new problem: armor and emblems built in (CHAR-REF-01), the coat tucked into the skirt from the back and the holster outside the coat (CHAR-REF-03), and no three-quarter view (CHAR-REF-04).
- **What I did:** Made the design decisions recorded in `CHARACTER-SHEET.md` ("Human design decisions") and `CHANGE-BRIEF.md` ("Design changes already made"): matte 80D+ tights instead of glossy materials, the coat hanging outside the skirt, the holster moved from the thigh to the right waist under the coat, no emblems, armor and pouches as separate modular equipment, and a fourth (three-quarter) view. I accepted the final turnaround (CHAR-TURN). ChatGPT's draft of the change brief built the slice around lab stealth; I kept the slice in the subway base, as I decided on 2026-10-06, and moved the lab, robots, and scan items to "planned for later". I added the sitting and tablet poses from my storyboard to the pose list, and decided that in this slice the only music is on the start menu. Looking at the accepted turnaround again, I kept the X-shaped hair clip but decided to remove the choker when modeling: it does not fit a shooter, it is not there to make her cute, and it even reads as sexual.
- **What Claude or another person contributed:** ChatGPT produced the image drafts from my descriptions, and drafted the English character sheet and change brief from our conversation. Claude Code merged that material with my storyboard and concept (subway-base slice, tablet poses, storyboard-style asset IDs), found the exact ComfyUI prompts and seeds in the output files' embedded metadata, made the rejection thumbnails, wrote the asset log, and prepared this commit. Claude at first described the character images as "generated before the character sheet was written"; I corrected that, because the sheet is the record of the design conversation in which the drafts were made and judged.
- **What I understand now / still do not understand:** I understand now: (1) Consistency depends on the seed the model uses; a fixed seed keeps the image generation stable. To keep the character consistent across different poses, a dedicated consistency plugin is actually needed. (2) Negative prompts really do push unwanted things away (adding "glossy / latex" reduced the shiny materials, and adding "3d render" removed the realistic render look), even though in the end I did not use any of the local model's outputs. (3) The models add a lot of what they have learned to the design on their own. As the creator, I have to be clear about what I need and what I do not. I still do not understand: how to make complex 3D models, especially humans and clothing, with AI. Neither the Blender MCP route nor ChatGPT works well for that. It may really need more specialized models, or it may still be work for professionals; I am still exploring how AI can produce complex 3D models. The Blender + Claude route actually builds models by combining basic shapes (spheres, cubes, and so on), so it is still not capable enough for complex models.
- **Evidence and next step:** `walker-survival-shooting/CHARACTER-SHEET.md`, `walker-survival-shooting/CHANGE-BRIEF.md`, the `SOURCES.md` asset log rows CHAR-REF-00 to CHAR-REF-04 and CHAR-TURN, `design/character/turnaround.png`, and the thumbnails in `design/rejected/`. ChatGPT prompts were not saved; ComfyUI prompts are exact. Next: the silhouette test, the collision overlay, the pose images, and the 3D model.

### 2026-10-07 — Storyboard sketches for panels 1–5; first Blender test

- **Date and what I was working on:** 2026-10-07. Drew sketches for storyboard panels 1–5 and tried the Blender workflow.
- **I tried / expected:** Sketch the start menu, the camera move into play, and the tablet states, so the storyboard has pictures.
- **What happened:** While drawing I changed panels 4–5: switching to two hands is a transition animation in which the camera pushes in to focus on the tablet, until the tablet fills the whole screen. I also left the seat in the start menu open (a chair, a sofa, or something else) instead of a bench. Claude first gave feedback on the drawing itself (frame shape, the figure facing the camera in over-the-shoulder panels, a typo); I rejected that, because the sketches only show the idea and my description is what counts.
- **What I did:** Kept the sketches as they are and recorded the changes in the revision history of `STORYBOARD.md` and `CHANGE-BRIEF.md`. Tested Blender with Claude through the Blender MCP: Claude built a simple low-poly test chair from basic shapes with Python and exported it to the Godot project as `assets/furniture/test_chair.glb`. It is a workflow test made by code, not a generated asset, so it is not in the asset log.
- **What Claude or another person contributed:** Claude cropped the iPad interface out of the sketch screenshots, wrote the revision entries, built and exported the test chair, and translated these notes.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `design/storyboard/01-title.png` to `05-tablet-fullscreen.png`; revision history in `STORYBOARD.md` and `CHANGE-BRIEF.md`. Next: sound effects with AI, and completing storyboard panels 8–10.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-10-06 | Add concept, storyboard text, and design log for Assignment 2 |
| 2026-10-07 | Add character sheet, change brief, and asset log with rejected character drafts |
| 2026-10-07 | Add storyboard sketches for panels 1–5 and record the panel 4–5 camera change |
