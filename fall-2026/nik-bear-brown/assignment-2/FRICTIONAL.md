# FRICTIONAL — Assignment 2, Professor Bear's example

## Executive summary

**What this is.** My process log for my own example of Assignment 2, *Generate Art, Sound, and Music for Your Game*, written the way the course asks students to write theirs: what was tried, what went wrong, what changed, and who did what, the human or the AI.

**What it records so far.** The design stage, on 2026-09-25. The game is *Clawd Closes the Loop*, and its enemies are bugs drawn from the ways agentic AI actually fails. I rejected most of Claude's creature ideas as forced and kept three directions: a **termite** that eats the game's foundations if not stopped early, a **blood-sucking parasite** for prompt injection (not a wasp), and **ants** as workers. No art, sound, or music has been generated yet.

Every push that touches this assignment is listed at the bottom with its date and commit note.

---

## Entries

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
- **What I did:** Kept the list as the enemy pool for the concept, the storyboard, and the character sheets. Then I went through every suggestion and judged it:

    | Suggestion | My verdict |
    |---|---|
    | Loop Beetle (retry loop) | Makes absolutely no sense. Forced. |
    | Mirage Moth (hallucinated fact) | Makes no sense. Forced. |
    | Silent Tick (ignored error) | Better done as something clock-like: a clock or a stopwatch. |
    | Checkmark Mimic (unverified success) | Makes no sense. |
    | **Termite (weakened test)** | **I like it.** It destroys your foundations if you don't get rid of it early. |
    | Brood Mother (compounding error) | Makes no sense. |
    | Memory Moth (context loss) | What is a memory moth? Makes no sense. |
    | **Parasite Wasp (prompt injection)** | **The parasite idea is interesting; the wasp is wrong.** Prompt injection is adversarial, something trying to bite into you. Most people don't associate wasps with parasites. Something that sucks your blood, like a mosquito, is a better metaphor for draining something away from you. |
    | Vine Centipede (scope creep) | Forced. Scope creep is a good challenge, but not as a centipede or cricket. |
    | Shed-Skin Cricket (stale state) | Forced. |
    | **Twin Ants (conflicting writes)** | **Maybe.** I like ants because they're little workers; they just work and work and work. Hold ants for something later. |

  - **Termite, as I see it now:** a termite-like character whose bug eats away at the game over time. If you don't get rid of your termites quickly and early, they destroy your foundation. What exactly it eats, I haven't decided.
  - **Parasite:** a blood-sucking parasite for prompt injection, something adversarial that drains you. I haven't settled the direction or the creature. I asked Claude for alternatives to the wasp (below).
  - **Plan for today:** make ant figures, make a parasite (not a wasp), and make a termite character.
- **Later the same day, the termite:** I asked, "What kinds of termites are there? I want to design the termite. I assume there are many kinds of termites. I'm looking for a handful of scary-looking termites that I can go searching on the web and use as a basis for making a termite obstacle in my game."
  - **Claude's answer (not yet checked by me):** termites come in castes, and the scary ones are mostly **soldiers**. Search terms it suggested:
    - **Macrotermes soldier:** African mound builders; big dark armored heads and long sickle jaws.
    - **Formosan subterranean termite** (*Coptotermes formosanus*): known as one of the most destructive to buildings, so the closest real match to "eats your foundations."
    - **Snapping termite soldier** (*Termes*, *Pericapritermes*): twisted jaws that snap shut.
    - **Nasute termite soldier** (*Nasutitermes*): a nozzle head that sprays sticky defensive fluid.
    - **Cryptotermes soldier:** a flat, dark head used as a plug to block the tunnel.
    - **Exploding termites:** *Globitermes sulphureus* soldiers and *Neocapritermes taracua* old workers, which burst to defend the colony.
    - **Termite queen:** a huge swollen pale body, a possible boss.
  - It also pointed out game hooks from real termite life: workers eat unseen, soldiers are the visible threat, and a swarm of winged termites is the real-world warning sign of an infestation. I haven't decided on any of this yet.
- **Then I picked one:** I found three photos of Macrotermes soldiers on the web and said: "So this one looks pretty scary to me. Are you able to upload those images to the GitHub as well, so people can see what I mean? The big head in particular, I've never seen a termite like that. But it looks like a pretty scary termite."
  - **What Claude did:** it didn't push my three photos. The repo is public and I have no source or license for them, which is exactly what my Assignment 2 tells students to record. It kept them on my machine in `reference/local-only/`, which git ignores. It found two openly licensed Macrotermes soldier photos on Wikimedia Commons and made [`reference/README.md`](reference/README.md), which shows them from Commons with the photographers' credit and license, without copying them into the repo.
  - **Open:** where my three photos came from, so they can go up with credit, or stay local.
  - **My decision:** "Okay, I'll redo the images using AI. And then you can upload those. If you're concerned about it, I think they're from Wikimedia Commons. But I'll go ahead and just redo them with AI." So the three web photos stay local, and my own AI-generated termite images go up instead, logged with the model, prompt, and settings like any other Assignment 2 asset.
  - **The AI versions:** I made them and said: "Attached are AI versions. Non-copyright versions of that kind of termite." One image, three soldiers: a dark-red big head seen from above at an angle, a black-headed one from straight above, and a smaller golden one. Saved as [`reference/termite-soldiers-ai-01.jpg`](reference/termite-soldiers-ai-01.jpg), asset ID **TERM-REF-01**, shown on the reference page.

    | Field | TERM-REF-01 |
    |---|---|
    | Model and version | Not yet recorded |
    | Prompt and settings | Not yet recorded |
    | Based on | My three web photos of Macrotermes soldiers, redone with AI |
    | Outcome | Accepted as a reference for the termite's look; not an in-game asset |
    | Where used | `reference/README.md` |

    **Model:** Gemini, by voice. That's how I found out what happened next.

  - **Gemini misheard me.** I said: "This is what happens when Gemini misheard me. I said 'create those termites,' and it thought I said 'Kratos termites,' and made Kratos God of War termites." It produced two sketchbook-style images of termites with Kratos's face, beard, and red tattoo, one with wings, surrounded by axes, a Spartan helmet, and omega symbols. It also made a **pixel-art** version of my three termites, which I kept.

    | Asset | Model | Outcome |
    |---|---|---|
    | TERM-REF-02, pixel-art termites ([`reference/termite-soldiers-pixel-02.jpg`](reference/termite-soldiers-pixel-02.jpg)) | Gemini, by voice | **Accepted** as a reference; closer to a game sprite than TERM-REF-01 |
    | Kratos termites, two versions | Gemini, by voice ("those" heard as "Kratos") | **Rejected.** Wrong request, and a copyrighted character (Sony's God of War). Kept on my machine only, in `reference/local-only/`, not published |

    Two of the five images I sent were repeats: one was TERM-REF-01 again, and the two pixel-art images were identical.

    **Claude noted (not yet checked by me):** this is the "misread task" failure from my own list of agent bugs, happening to me: the model did something confident and detailed with the wrong instruction, and nothing in the output said it had guessed. It's also why "can you hear me speak?" mattered earlier: voice goes through a transcription step first, and that step can be wrong.

    **Claude noted (not yet checked by me):** the poses follow the web photos closely, so an image made from them may still count as derived from those photos. If they are from Wikimedia Commons as I think, finding their pages would settle it and give them credit.
- **What Claude or another person contributed:** Claude Code (Opus 5.5) wrote the failure list, all eleven creature ideas, and the "behavior acts out the failure" rule. It proposed three creatures as the strongest set: the Loop Beetle (easy to read), the Checkmark Mimic (it teaches the verify step my earlier design draft was missing), and the Parasite Wasp (it is both the malware and the vague path from the original concept). I chose the game and asked the questions. I rejected eight of the eleven creatures as forced, including all three of Claude's "strongest set" picks except the parasite idea, and I rejected the wasp as the parasite. The termite's foundation-eating role, the clock for ignored errors, the mosquito direction, and the ants-as-workers idea are mine. After my notes, Claude suggested parasites that read as draining at a glance:
  - **Mosquito:** the one everyone knows; it flies in, drinks, and leaves, and its whine is a ready sound cue before it bites.
  - **Tick:** latches on and visibly **swells** as it drains, so the player can see how much has been taken. It clashes with the clock "tick" for ignored errors, so one of the two needs another name.
  - **Leech:** clings, stretches, and drains slowly; hard to shake off, which fits an injected instruction that keeps steering you.
  - **Flea:** tiny, jumps between hosts, and comes in numbers, if the parasite should spread.
  - **Bedbug:** hides in the furniture of the level and comes out when you rest.

  I haven't chosen among these yet.
- **What I understand now / still do not understand:** A creature has to fit the failure the way a termite fits rotten foundations: the metaphor has to be one most people already carry, not one invented to match a label. Most of the first list failed that test. Still open: which parasite; what the termite actually eats in the game; what the ants' job is; how the clock for ignored errors works in play; how scope creep becomes a challenge without being a creature; whether one main character plus three enemies is too much to generate consistently at this scope, and whether the enemies need character sheets of their own or one shared sheet.
- **Evidence and next step:** This entry; the design draft of the game is in `walker-jumpman-clawd/design/` (not in this repository). Next, today: ant figures, a parasite, and a termite character. Then `CONCEPT.md`, the storyboard, and the character sheets before generating the final assets.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-09-25 | Log Assignment 2 design thinking; record standing push approval |
| 2026-09-25 | Log my verdicts on the bug creatures; termite, parasite, ants kept |
| 2026-09-25 | Move Assignment 2 notes into assignment-2/ with its own log |
| 2026-09-25 | Add assignment-2 folders for everyone; rename mine to match |
| 2026-09-25 | Log my termite question and the candidate species |
| 2026-09-25 | Add Macrotermes soldier reference; log my termite pick |
| 2026-09-25 | Log my decision to redo the termite images with AI |
| 2026-09-25 | Add my AI termite reference image (TERM-REF-01) |
| 2026-09-25 | Add pixel-art termite reference (TERM-REF-02); log the Kratos mishearing |
