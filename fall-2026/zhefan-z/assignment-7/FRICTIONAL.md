# FRICTIONAL — Assignment 7

Prediction, attempts, obstacles, changes, results and the next test, from my session of 2026-11-10 to 2026-11-12. Organized by claude.ai (chat) from what happened; every entry is something that happened and that I checked. "Agent" means Claude Code (desktop app, Opus 5.5, manual permissions). Tuning details are in `TUNING.md`.

## Predictions and what happened

| My prediction (brief) | Result |
|---|---|
| The wolf's phases are 30 / 21 / 36 ticks | **Wrong**: the pin measured 31 / 22 / 36 (floating-point timer); the table and keys follow the measurement |
| The growl-cancel change alters only the `hit_growl` pin | **Wrong**: `kill` also hits during GROWL; the pin caught it, and the agent held the commit and asked me rather than use my message claiming otherwise |
| F1: a Godot 3 `loop = true` makes the run play once | **Did not occur**: Godot 4.7.2 maps it to `loop_mode = 1` (mutation a7-1) |
| F6: the waist seam opens when the front part rotates | **Did not occur**: no gap in my play or in the game strip at 4× |
| Wiring the clips changes no behaviour | **Held**: pin identical at 30, 60, 144 |

## Struggle and revision: the run cycle

This took most of the time, and I learned the most from it.

1. **What I saw:** the two-frame run "twitched while sliding". My first guess was that the same foot was always forward.
2. **Measured:** the agent's game strip showed a 1 px body hop and a planted foot sliding 13–15 px, then snapping back.
3. **Three attempts at the other foot failed:** mirroring the leg region gave a kick with backward boots; Gemini twice redrew my contact pose with the same foot forward (103 px differed, all in the trailing leg); darkening the far leg changed 19 px, invisible at 2×.
4. **My own correction:** on a closer look the problem wasn't the foot (the skirt hides the legs) but that two pictures just swap. That changed what to try next.
5. **r1, a body bob from the same two frames:** every hat row landed exactly as the agent predicted, and I still rejected it in play. A correct prediction was not a good result.
6. **r2:** a four-frame cycle drawn in one image, prompted for contact, down, passing and up poses rather than asking for an edit; cleaned onto my A2 palette; at 10 fps so each frame is a whole number of ticks. I kept it.

**What I learned:** an image model asked to edit a reference copies it, but asked for a whole sheet it draws new poses; and a measured match to a prediction proves the mechanics, not the feel. The next test is in-betweens for the planted foot, in the final project.

## Other entries

**Assignment page.** Canvas showed the instructor's revision notes for A7 rather than the full text. I worked from them: every requirement they state is covered, and the pin, state-machine and edge steps follow the clues in its "Still standing" section.

**A second clock in my own game.** The wolf's removal after death runs on a frame-clock timer: tick 79 at 60 fps, 80 at 30 and 144. Found by the pin; kept, because gameplay never reads it.

**The growl window is 0.2 s.** In play, the cancel seemed not to work. The agent's probe with real clicks showed the rule works, but the fireball's 20-tick flight leaves only the first 12 growl ticks. I kept the timings and recorded it as a design finding.

**Two alignment bugs** the read-backs could not see: the edges test found that a cancel drew clip frame 54 instead of 53, and the windowed lunge capture's tick log showed a growl after a one-tick patrol starting one frame late. Both fixed without changing behaviour; the edges test was extended to the second and checked by removing the fix and watching it fail.

**Silent integer keys, twice.** The agent wrote 0° and 1.0 as integers on float properties, first in the wolf clip and again in the light clip; its own key-type check caught both.

**Visual upgrades "not noticeable".** My first look at the torches, embers and afterimage: too subtle. The agent listed old and new values, measured the result and lightened the darkening so the mage stayed readable; then they were clearly visible.

**An interrupted session.** The film update's build agent stopped on an expired login (HTTP 401) while exporting the 4K master; its last export was refused and no new film was written. Following the resume rule, the next session did not continue it: it checked the snapshot against `ad7935f`, checked the new capture's three hits (GROWL cancelled, LUNGE not, RECOVER HP only), reran every test (all passing), found the refusal was the process being killed (the same ffmpeg command succeeded alone in 16 s), and finished the film in a new session (`b3c8963`).

**Process slips.** The agent amended one local commit (the first CLAUDE.md draft was 122 lines); during the mutation run it kept one temporary backup one folder above the assignment root for a few seconds and ran its mutation script from its own temporary folder outside the repository; nothing was left behind. I let the agent make the commits I asked for, each labelled with who wrote the content; it never pushed.

## Human and AI contributions

- **Mine:** both clips and their look (8 fps, clear crouch and stretch, later 10 fps for r2), the per-phase interrupt rule, keeping the 0.2 s window, every first look and every verdict in the running game (run r0, r1 rejected, r2 kept; visual upgrades r0 rejected, r1 kept), generating the run images in Gemini, accepting the re-pin after play, three reviews of the agent's CLAUDE.md draft, and the human checks (five-wrap cycle, an interrupt in each phase, registration, darkest and lightest art).
- **Claude Code:** CLAUDE.md drafts, the pin, the clips and rig, read-backs, structure, edges and afterimage tests, the probes and capture harnesses, the cleanup tools, the visual upgrades, mutations, figures, measurements, predictions and comparisons.
- **claude.ai (chat):** planning, commands, the brief and its revisions from my decisions, the Gemini prompts, and these documents.

## Still open

- In-between frames so the planted foot stops sliding.
- Whether the growl window should be wider (a longer growl or a faster fireball): a gameplay change for later, with its own pin and re-pin.
