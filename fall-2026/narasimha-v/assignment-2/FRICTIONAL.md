# FRICTIONAL — Assignment 2

## Entries

<!-- One entry per work session, newest last. -->

### 2026-10-01 — Choosing the game: a day of arguing with Claude

- **Date and what I was working on:** 2026-10-01, the whole concept phase. My role in these sessions is deliberately devil's advocate: Claude pitches, I attack, and the game is whatever survives. This log records those real exchanges.
- **I tried / expected:** I started assuming I would extend my Assignment 1 game (THE WORLD IS FALLING) and expected the design docs to be mostly a formality on top of it.
- **What happened:** Claude's first direction (redesign my Runner character, keep the game) didn't survive my own reaction to it — when it offered visual directions I realized I didn't actually know what I wanted, which meant the game identity wasn't as settled as I thought. I asked for brand-new ideas instead. Claude pitched a flagship concept (VELA, a deep-sea light-giving game) plus alternates; I rejected VELA because the thing I actually cared about from Assignment 1 was the upside-down inversion verb, not the setting. Claude then pitched three worlds around that verb (STILLWATER, SKYSUNDER, YESTERDAY HOUSE), then on my request a list of twelve one-liners. I picked two (HOUSEGHOST, ANCHOR) and asked for a merge.
- **What I did:** I drove four hard pivots against Claude's recommendations: (1) rejected continuing my Assignment 1 game outright even though Claude recommended it as lower risk; (2) rejected the storm as the cover story for the death — "it's just a storm, that's boring" — and demanded something with a guilty party, which produced the murdering-father twist; (3) asked for an alternative fake reason and chose "he ran away" from Claude's five options, over Claude's initially storm-shaped design; (4) set the tone rule that horror lives in the inverted world while normal play stays only uneasy. I also challenged Claude's claim about commit visibility in a shared-repo workflow and made it correct itself (it had overstated a disadvantage; forks carry commits in PRs).
- **What Claude or another person contributed:** Claude generated all candidate concepts, the five-rung twist-ladder structure ("one question, five answers" instead of twist soup — its pushback on my ask for "many twists"), the fear-economy difficulty design, the calendar/frost meter, and drafted CONCEPT.md, STORYBOARD.md, CHARACTER-SHEET.md, and CHANGE-BRIEF.md from our agreed brief. No generative image/audio model has been used yet — by design, nothing is generated before these docs are committed.
- **What I understand now / still do not understand:** I understand that the verb (flipping the world) was the real asset from Assignment 1, not the game around it. Still unresolved: the ghost's visual design is specified on paper (character sheet) but I haven't seen it — the first generated reference may force palette or silhouette changes; and we don't yet know which image model we're using.
- **Evidence and next step:** Evidence: this conversation's decision trail, and the four design docs committed alongside this entry before any generation. Next step: commit the docs, then run the first character-reference generation against the sheet and judge it.

### 2026-10-01 — Repo access: finding out we can't push

- **Date and what I was working on:** 2026-10-01, figuring out where this assignment's work should live.
- **I tried / expected:** I believed the professor's course repo had a folder for each student and expected to push into mine (`fall-2026/narasimha-v/assignment-2/`).
- **What happened:** The folder exists (seeded with a README and a blank FRICTIONAL template), but an API permissions check showed student accounts have `push: false` — read-only. The only route in is fork + pull request.
- **What I did:** I decided not to guess the professor's intent. I had Claude verify the permission via the GitHub API, then drafted a short email to Professor Brown proposing two options (grant write access, or work in our own repos like Assignment 1) with one advantage and disadvantage each, and sent it. I chose to wait for his answer before creating any repo, and to prepare all design docs meanwhile so we can commit the moment the workflow is settled.
- **What Claude or another person contributed:** Claude ran the read-only permission checks, explained the fork/PR mechanics (including correcting its own earlier overstatement about commit visibility after I questioned it), and drafted the email which I edited (shortened it, removed dashes, added that these were options from my point of view).
- **What I understand now / still do not understand:** I understand a file copy between repos doesn't carry commit history, and a fork's PR does. Still unknown: which workflow the professor will pick.
- **Evidence and next step:** Evidence: the permission check output (`"push": false`), the seeded folder contents, the sent email. Next step: on his reply, set up the repo accordingly and make the first commit (all four design docs + this file).

### 2026-10-01 — Naming the boy, designing the cast, choosing the image models

- **Date and what I was working on:** 2026-10-01, late concept phase: the ghost's name, the supporting cast's visual designs, and which image models we'll generate with.
- **I tried / expected:** I asked for mysterious name ideas, expecting to just pick one and put it in the character sheet.
- **What happened:** Claude offered five options: Hollis (one letter from "the Hollow"), Wren, Ansel, October, and a fifth that wasn't a name at all — leave the boy nameless, hide the name as a relic under a floorboard, and make the child speaking it aloud the thing that completes "being seen."
- **What I did:** I chose the nameless option — the name became a game mechanic instead of a label. Claude's recommended hidden answer (Hollis) is recorded in the character sheet as swappable. I also reviewed Claude's visual designs for the cast (the child's always-on yellow raincoat as the upright world's only saturated color; the father never facing camera, always mid-task, salt pouch; the wife humming the lullaby unknowingly; the Hollow's one-silhouette-two-readings rule) and accepted them. And I settled the image-model question: we'll generate with Gemini and ChatGPT, since that's the access I have.
- **What Claude or another person contributed:** Claude proposed the name candidates and the nameless mechanic, wrote the cast design rules, and documented the no-seed reproducibility plan (exact prompts, model+version+date, screenshots) that Gemini/ChatGPT require since neither exposes seeds. The decisions were mine; no images or audio have been generated yet.
- **What I understand now / still do not understand:** I understand that withholding information (a name, a face, a reason) is doing more design work in this game than adding things. Still unresolved: whether Gemini or ChatGPT will hold character consistency across 12 poses from one reference image — that's the first real generation risk to test.
- **Evidence and next step:** Evidence: the updated CONCEPT.md (name and generation-plan sections), CHARACTER-SHEET.md (name rule, cast section), CHANGE-BRIEF.md (child assets added). Next step: storyboard images for the six panels, then commit everything and run the first ghost reference generation.

### 2026-10-01 — Where the work lives, and four candidate looks for the boy

- **Date and what I was working on:** 2026-10-01, evening: deciding not to wait on the repo question, and starting the character's visual design.
- **I tried / expected:** After emailing Professor Brown about write access (previous entry), I expected to park the work until he replied, or to start a personal repo as a backup.
- **What happened:** Waiting blocks everything downstream — the docs must be committed before generation, and music generation should start daily per the instructor's email. Separately, I caught Claude writing a specific character design (the oversized-sweater boy) into the character sheet as if I had chosen it; I hadn't.
- **What I did:** Two decisions. Repo: clone the course repo, do all work on a local branch (`assignment-2-narasimha-v`) inside my own folder, commit locally with real timestamps, and hold the PR until I decide — this works under every answer the professor might give. Character: I had Claude mark the sheet's visual concept as an open working draft, and asked to discuss the candidate ideas in conversation first; I will generate the character images myself in Gemini/ChatGPT once a look is chosen. The four candidates on the table: Sweater Kid (hand-me-down mustard sweater, sock feet), Pajama Boy (striped pajamas, one slipper — clothes that contradict "he ran away" in every frame), Slicker (hood up; his coat is the same yellow the half-sibling now wears), Outline (a boy-shaped absence that only fills in when the world inverts).
- **What Claude or another person contributed:** Claude set up the sparse clone and branch, assembled all documents from our agreed decisions, drew the four candidates as hand-coded sketch cards (explicitly not generated art), and fixed the design-ownership error when I called it out. All art and audio generation remains at zero.
- **What I understand now / still do not understand:** Local commits keep their timestamps wherever they are later pushed, so the docs-before-generation evidence survives any repo outcome. Still open: which of the four looks (or a merge of two) becomes the boy.
- **Evidence and next step:** Evidence: this branch's commit history and the STATUS note in CHARACTER-SHEET.md. Next step: settle the look in conversation, update the sheet, add storyboard images, then run the first generation.

---

### 2026-10-02 — The assignment changed under us (in our favor), and write access arrived

- **Date and what I was working on:** 2026-10-02: reacting to an updated assignment spec, and the professor's answer to my access email.
- **I tried / expected:** I expected to spend today picking the character's final look and fighting Gemini/ChatGPT for frame-to-frame animation consistency — our #1 flagged risk.
- **What happened:** Two external changes. First, Professor Brown answered my email by sending a collaborator invite; I accepted, and a permissions check now shows `push: true` — students push directly to their folders (option 1 from my email). Second, the assignment was updated: animation is explicitly not required and earns nothing (stated twice, including in the quartile section); each character state is one static image the game swaps; walk is one pose instead of contact+passing; storyboard motion arrows became optional.
- **What I did:** I asked whether we should animate anyway for marks, and accepted the argument against it: the spec says twice it pays nothing, and multi-frame generation reintroduces the consistency risk the update just deleted. Decision: static images per state, with motion done as engine code (tweens for idle bob, the 180° flip, fade-and-scatter on dispersal) — credited as code, not as generated animation. I had the docs aligned: character sheet 12→11 poses (walk merged, loop/once labels removed, static-image rule stated), storyboard motion line marked optional-by-choice, change brief's walk asset reworded. Pushing remains manual-only on my explicit say-so; nothing has been pushed yet.
- **What Claude or another person contributed:** Claude diffed the old and new assignment texts, listed the eight concrete changes, proposed the static-image + engine-motion approach, and made the edits. The animate-or-not decision and the keep-it-local decision were mine.
- **What I understand now / still do not understand:** The update removes our hardest generation problem; 11 single images from one reference is achievable where animation frames were not. Still open: the character's final look (the two-state instant-read formula — mist-legs ghost upright, solid warm boy inverted — is agreed in conversation; the outfit and slow-burn prop are not yet locked in the sheet).
- **Evidence and next step:** Evidence: this commit's diff against yesterday's docs — the original versions are retained in history per the assignment's "add later revisions rather than rewriting the record." Next step: lock the look, update the sheet, then the first reference generation.

---

## GitHub pushes

_No pushes yet — commits are local on branch `assignment-2-narasimha-v`; pushing happens only on my explicit instruction. This table fills in when pushing begins._

| Date | Commit note |
|---|---|
