# FRICTIONAL — Professor Bear's process log

## Executive summary

**What this is.** The honest process log for the work in this folder, written the way the course asks students to write theirs: what was tried, what went wrong, what changed, and who did what, the human or the AI.

**What it records so far.** The folder was set up on 2026-09-25. The same day, the design thinking for my Assignment 2 example started: the game is *Clawd Closes the Loop*, and its enemies are bugs drawn from the ways agentic AI actually fails. No art, sound, or music has been generated yet.

Every push to GitHub is listed at the bottom with its date and commit note.

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

### 2026-09-25 — Assignment 2: choosing the game and turning agent failures into bugs

- **Date and what I was working on:** 2026-09-25. The design stage of my own Assignment 2 example (*Generate Art, Sound, and Music for Your Game*): what game, and what the enemies are, before any generation.
- **I tried / expected:** I wanted the art to come out of the game's idea, not decorate it. The game is *Clawd Closes the Loop*: a coding agent runs every level as a loop of tasks, and the obstacles are the things that go wrong for agents. I expected a short list of failure types that could become enemies.
- **What happened:**
  - I asked Claude Code for the most common bugs and errors in agentic AI. It grouped about twenty into six families: instructions and planning, tool use, verification and honesty, memory and context, safety and security, and multi-agent coordination.
  - I asked which could be shown as a creepy crawly bug. The useful answer was that the creature's **behavior** has to act out the failure, not just carry its name:

    | Failure | Creature | What it does in play |
    |---|---|---|
    | Retry loop | Loop Beetle | Circles the same track forever; break the loop to pass |
    | Hallucinated fact | Mirage Moth | Lures you to a platform or pickup that isn't there |
    | Ignored error | Silent Tick | Latches on silently; the damage shows up later |
    | Claimed but unverified success | Checkmark Mimic | Looks like a completed-task marker until you step on it |
    | Weakened test | Termite | Eats the floor and railings, the safety checks |
    | Compounding error | Brood Mother | Cheap to squash early, a swarm if left |
    | Context loss | Memory Moth | Eats pieces of the HUD, like the task list |
    | Prompt injection | Parasite Wasp | Stings a sign or friendly creature so it gives false directions |
    | Scope creep | Vine Centipede | Keeps adding segments and blocks unrelated routes |
    | Stale state | Shed-Skin Cricket | Leaves a husk where it used to be |
    | Conflicting writes | Twin Ants | Two ants tear apart the platform you need |

  - Three failures didn't fit as bugs: credential leakage, excess permissions, and unbounded cost. They are about access and budget, not something to dodge, so they would be HUD meters or level rules.
- **What I did:** Kept the list as the enemy pool for the concept, the storyboard, and the character sheets.
- **What Claude or another person contributed:** Claude Code (Opus 5.5) wrote the failure list, all eleven creature ideas, and the "behavior acts out the failure" rule. It proposed three creatures as the strongest set: the Loop Beetle (easy to read), the Checkmark Mimic (it teaches the verify step my earlier design draft was missing), and the Parasite Wasp (it is both the malware and the vague path from the original concept). I chose the game and asked the questions. I have **not yet** decided which creatures go in.
- **What I understand now / still do not understand:** The bugs are good teaching when the player learns the agent's lesson by beating them. The Checkmark Mimic is the clearest case: players learn not to trust a green tick. Still open: whether one main character plus three enemies is too much to generate consistently at this scope, and whether the enemies need character sheets of their own or one shared sheet.
- **Evidence and next step:** This entry; the design draft of the game is in `walker-jumpman-clawd/design/` (not in this repository). Next: pick the enemies, then write `CONCEPT.md`, the storyboard, and Clawd's character sheet before generating anything.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-09-25 | Add fall-2026 roster and nik-bear-brown example folder |
| 2026-09-25 | Log Assignment 2 design thinking; record standing push approval |
