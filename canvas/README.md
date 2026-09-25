# Separate Canvas pastes

> **On GitHub:** the HTML fragments are not committed. The Markdown sources are the course content: [Module 1 lesson](../modules/01-walker-and-godot/lesson.md), [Assignment 1](../assignments/01-extend-walker-jumpman.md), [Assignment 2](../assignments/02-generate-walker-art-sound-music.md). To make the Canvas pastes, run `node scripts/build-canvas-pastes.cjs` (needs pandoc); it writes the `.html` files into this folder.

1. **Canvas Page:** Module 1 — Walker and Godot. Paste the content of `01-module-1-walker-and-godot.html` into the page's HTML editor. It includes “What is Walker?” and “What is Godot?”, the learning loop, setup, and ungraded practice assessments.
2. **Canvas Assignment:** Assignment 1 - Extend Walker Jumpman. Set the assignment to **100 points**, then paste `02-assignment-1-extend-walker-jumpman.html` into its HTML editor. Use the course's 10-day cadence when setting the Canvas deadline. Enable file-upload submission for the source ZIP and submission note.

Both files are HTML fragments, not full websites. Their links are external HTTPS links; no local images, scripts, or local file links need to be imported. The Markdown originals are `modules/01-walker-and-godot/lesson.md` and `assignments/01-extend-walker-jumpman.md`.

Rebuild both fragments with `node scripts/build-canvas-pastes.cjs`. Local browser checks cover desktop and 390-pixel mobile layouts; headings, tables, and long prompt wrapping were inspected. This does not claim an actual Canvas paste check.

The lesson and assignment are deliberately separate. This folder is the manual-paste delivery requested by Professor Brown; no new IMSCC has been built and no Canvas page or assignment has been created remotely.

## Review notes

- Source paths and starter behavior were checked against walker-jumpman commit `9387542ca473b0a252c43bfe6d4fd39b61f8d439` and the public repository. This was a content check, not a new game test run.
- Godot's official download, key-concepts, custom-drawing, and editor documentation were checked while drafting.
- Northeastern's Claude page returned a fetch error during this check. The page is linked for access help, but no unverified current account entitlement or purchase requirement is asserted.
- The public URL for the new Brutalist Godot skill was not available during the check. The assignment explicitly refers to the course-provided checkout and tells students to request that version if their installation lacks the skill. Make that version available with the course materials before release.
- The existing course policy specifies the 20-point relative allocation, not numeric quartile bands or tie rules. This assignment preserves that policy without inventing a new scoring scale. Apply the course's communicated comparative-grading rules.
- The source ZIP submission, two added jump landings, and task-specific subdivision of the 60 points are concrete Assignment 1 drafting choices for instructor review.
- These teaching drafts do not sign an AI+1 book gate or represent a human review. The Word syllabus and original Canvas export are unchanged.

## Assignment 2 paste (added 2026-09-25)

3. **Canvas Assignment:** Assignment 2 - Generate Walker Jumpman's Art, Sound, and Music. Set it to **100 points** and paste `03-assignment-2-generate-walker-art-sound-music.html`. Enable file-upload submission for the source ZIP and submission note. Markdown source: `assignments/02-generate-walker-art-sound-music.md`.

Open items for instructor review: the assignment does not name a covered module because only Module 1 is drafted; the 60-point subdivision (12 / 14 / 14 / 10 / 10) is a drafting choice; `godot-gamedev` is chosen as the required explainer because this assignment is about how assets were made and wired in; students need a course-provided way to keep game audio audible in the film if the skill silences captured gameplay by default.
