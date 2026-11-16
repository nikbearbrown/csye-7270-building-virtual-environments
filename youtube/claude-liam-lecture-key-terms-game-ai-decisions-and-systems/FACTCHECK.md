# FACTCHECK - Key Terms: Game AI, Decisions and Systems

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 3 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Computed, Simulation, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `33` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; Deciding with states | PASS | Second-pass check against slide 2 step 1 and 14-game-ai-and-systems.md | none |
| 5 | B0102 | Explanation of: Trees, scores and plans; Three ways to decide what to do next | PASS | Second-pass check against slide 2 step 2 and 14-game-ai-and-systems.md | none |
| 6 | B0103 | Explanation of: Generating and checking; Making levels from a seed, and proving they work | PASS | Second-pass check against slide 2 step 3 and 14-game-ai-and-systems.md | none |
| 7 | B0104 | Explanation of: Learning and networks | PASS | Second-pass check against slide 2 step 4 and 14-game-ai-and-systems.md | none |
| 8 | B0201 | Explanation of: Finite state machine; in the book text; A set of states with transitions; one is active.; TELL THESE APART | PASS | Second-pass check against slide 3 step 1 and 14-game-ai-and-systems.md | none |
| 9 | B0202 | Explanation of: Transition table; in the glossary; A list of every state, condition and next state.; THE SAME FOUR TRANSITIONS AS A TABLE | PASS | Second-pass check against slide 3 step 2 and 14-game-ai-and-systems.md | none |
| 10 | B0203 | Figures spoken: `90 ticks`, `240`, `switches so far: 37` | PASS | Each figure is printed on slide 3 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 11 | B0203 | Explanation of: in the book text; Rapid back-and-forth switching between states.; Flicker; ONE THRESHOLD: CHASE WHEN DISTANCE < 240 | PASS | Second-pass check against slide 3 step 3 and 14-game-ai-and-systems.md | none |
| 12 | B0204 | Figures spoken: `220`, `260`, `37`, `give 3` | PASS | Each figure is printed on slide 3 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 13 | B0204 | Explanation of: in the book text; Hysteresis; TWO THRESHOLDS: ENTER < 220, LEAVE > 260; 220 | PASS | Second-pass check against slide 3 step 4 and 14-game-ai-and-systems.md | none |
| 14 | B0301 | Explanation of: Behavior tree; in the book text; A tree of nodes that decides what an agent does each tick.; TELL THESE APART | PASS | Second-pass check against slide 4 step 1 and 14-game-ai-and-systems.md | none |
| 15 | B0302 | Figures spoken: `tick 1`, `tick 2`, `tick 3` | PASS | Each figure is printed on slide 4 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 16 | B0302 | Explanation of: in the book text; One update step; the tree is evaluated again from the root.; Tick; tick 3 of 3: root RUNNING, doing Patrol | PASS | Second-pass check against slide 4 step 2 and 14-game-ai-and-systems.md | none |
| 17 | B0303 | Figures spoken: `TICK 2`, `6 of 8` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 18 | B0303 | Explanation of: in the book text; Success/failure/running; Nodes ticked: 6 of 8. SUCCESS 1, FAILURE 2, RUNNING 3.; WHAT EACH NODE RETURNED (TICK 2) | PASS | Second-pass check against slide 4 step 3 and 14-game-ai-and-systems.md | none |
| 19 | B0304 | Figures spoken: `TICK 2` | PASS | Each figure is printed on slide 4 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 20 | B0304 | Explanation of: Blackboard; in the book text; A shared memory of facts the AI reads and writes.; BLACKBOARD | PASS | Second-pass check against slide 4 step 4 and 14-game-ai-and-systems.md | none |
| 21 | B0401 | Figures spoken: `tick 4` | PASS | Each figure is printed on slide 5 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 22 | B0401 | Explanation of: Condition and action; in the book text; TELL THESE APART; Selector | PASS | Second-pass check against slide 5 step 1 and 14-game-ai-and-systems.md | none |
| 23 | B0402 | Explanation of: in the book text; Also called a fallback; Tries children in order until one succeeds.; Selector | PASS | Second-pass check against slide 5 step 2 and 14-game-ai-and-systems.md | none |
| 24 | B0403 | Explanation of: in the book text; Runs children in order and stops at the first failure.; Sequence; SEQUENCE: STOPS AT FIRST NON-SUCCESS | PASS | Second-pass check against slide 5 step 3 and 14-game-ai-and-systems.md | none |
| 25 | B0501 | Figures spoken: `100 PX`, `HEALTH 0.8`, `0.63` | PASS | Each figure is printed on slide 6 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 26 | B0501 | Explanation of: Utility AI; in the glossary; Scores every option and picks the highest.; TELL THESE APART | PASS | Second-pass check against slide 6 step 1 and 14-game-ai-and-systems.md | none |
| 27 | B0502 | Figures spoken: `150 PX`, `HEALTH 0.3`, `0.66`, `health 0.8`, `0.51` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 28 | B0502 | Explanation of: Weighted sum; in the glossary; Adding scores, each multiplied by an importance weight.; SCORES AT 150 PX AND HEALTH 0.3 | CORRECTED | Second-pass check against the slide and the chapter: The slide's patrol formula is 0.6 x (1 - c) + 0.4 x 0.5, a closeness part plus a constant, so not every score has a health part. | Reworded. Was: "A Weighted sum adds several inputs, each multiplied by a weight that says how much it matters. Here each score has a closeness part and a health part. At one hu" |
| 29 | B0601 | Figures spoken: `6 world states` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 30 | B0601 | Explanation of: GOAP; in the glossary; TELL THESE APART; GOAP | PASS | Second-pass check against slide 7 step 1 and 14-game-ai-and-systems.md | none |
| 31 | B0602 | Figures spoken: `plan step 2` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 32 | B0602 | Explanation of: Precondition and effect; in the glossary; WHAT EACH ACTION NEEDS AND CHANGES; ACTION | PASS | Second-pass check against slide 7 step 2 and 14-game-ai-and-systems.md | none |
| 33 | B0701 | Figures spoken: `step 5` | PASS | Each figure is printed on slide 8 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 34 | B0701 | Explanation of: Reinforcement learning; in the book text; Learning behaviour by trial and reward.; TELL THESE APART | PASS | Second-pass check against slide 8 step 1 and 14-game-ai-and-systems.md | none |
| 35 | B0702 | Figures spoken: `−0.01`, `+1.00`, `+0.96` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 36 | B0702 | Explanation of: in the book text; The number telling the agent how well it did.; Reward; REWARD AT EACH STEP OF THE SAME EPISODE | PASS | Second-pass check against slide 8 step 2 and 14-game-ai-and-systems.md | none |
| 37 | B0703 | Figures spoken: `γ = 0.95`, `0.815`, `0.78`, `γ = 0.5`, `0.063` | PASS | Each figure is printed on slide 8 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 38 | B0703 | Explanation of: Discount factor; in the book text; How much future reward is worth compared to now.; EACH REWARD × γ TO THE POWER OF ITS STEP | PASS | Second-pass check against slide 8 step 3 and 14-game-ai-and-systems.md | none |
| 39 | B0801 | Figures spoken: `500`, `8 steps` | PASS | Each figure is printed on slide 9 at step 1 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 40 | B0801 | Explanation of: Q-learning; in the book text; Learning the value of each action in each state.; TELL THESE APART | PASS | Second-pass check against slide 9 step 1 and 14-game-ai-and-systems.md | none |
| 41 | B0802 | Figures spoken: `1.00`, `0.05`, `last 25 episodes`, `80%`, `313` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 42 | B0802 | Explanation of: in the book text; Epsilon-greedy; TRAINING, 500 EPISODES; 0 | PASS | Second-pass check against slide 9 step 2 and 14-game-ai-and-systems.md | none |
| 43 | B0901 | Figures spoken: `seed 42`, `0.000000`, `seed 7` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 44 | B0901 | Explanation of: Seed; in the book text; Pseudo-random: looks random, computed from a seed; A number that fixes a random sequence. | CORRECTED | Second-pass check against the slide and the chapter: Chapter 14 says a seed reproduces a level only on a pinned engine version, and Lab B's pass establishes determinism 'for a seed on this engine version', so an unqualified 'every time' overclaims. | Reworded. Was: "Three strips of smooth noise, in this simulated run. A Seed is the number that fixes a random sequence. The values look random but are computed from the seed, w" |
| 45 | B0902 | Figures spoken: `0.61`, `0.06` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 46 | B0902 | Explanation of: Coherent noise; in the book text; Random values that change smoothly (Perlin, simplex).; NEIGHBOURS: UNRELATED OR RELATED | PASS | Second-pass check against slide 10 step 2 and 14-game-ai-and-systems.md | none |
| 47 | B0903 | Figures spoken: `octave 1`, `octave 2`, `octave 3`, `strength 0.5`, `strength 0.25` | PASS | Each figure is printed on slide 10 at step 3 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 48 | B0903 | Explanation of: Octave; in the glossary; One layer of noise at a set scale, added to others.; THREE OCTAVES, THEN THEIR SUM ÷ 1.75 | PASS | Second-pass check against slide 10 step 3 and 14-game-ai-and-systems.md | none |
| 49 | B0904 | Figures spoken: `64`, `seed 42`, `seed 7` | PASS | Each figure is printed on slide 10 at step 4 (machine check, check_narration.py). Badge: Simulation (seeded). | none |
| 50 | B0904 | Explanation of: in the book text; Same inputs and seed give the same output every run.; Determinism; A FINGERPRINT OF EACH RUN'S 64 NUMBERS | PASS | Second-pass check against slide 10 step 4 and 14-game-ai-and-systems.md | none |
| 51 | B1001 | Figures spoken: `42`, `0.2`, `668 of 1536` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 52 | B1001 | Explanation of: Heightmap; in the book text; A grid with one height value per position.; TELL THESE APART | PASS | Second-pass check against slide 11 step 1 and 14-game-ai-and-systems.md | none |
| 53 | B1002 | Figures spoken: `384`, `0 of 384` | PASS | Each figure is printed on slide 11 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 54 | B1002 | Explanation of: in the book text; Compute shader; SAME FORMULA, TWO WAYS TO RUN IT; loop: one cell after another | PASS | Second-pass check against slide 11 step 2 and 14-game-ai-and-systems.md | none |
| 55 | B1101 | Figures spoken: `STEP ≤ 2`, `JUMP ≤ 6`, `15`, `19 of 19` | PASS | Each figure is printed on slide 12 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 56 | B1101 | Explanation of: Validator; in the book text; A check that tests generated content against rules.; TELL THESE APART | PASS | Second-pass check against slide 12 step 1 and 14-game-ai-and-systems.md | none |
| 57 | B1102 | Figures spoken: `60`, `12 of 60`, `20%`, `20 seeds`, `15 levels` | PASS | Each figure is printed on slide 12 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 58 | B1102 | Explanation of: in the book text; Make content randomly, then reject what fails.; Generate-and-test; SEEDS 1 TO 60, MADE AT RANDOM, THEN CHECKED | CORRECTED | Second-pass check against the slide and the chapter: Chapter 14 (Lab B Verify) says a validator pass 'does not establish that an accepted level can be crossed', so calling validator-accepted levels 'playable' overclaims. | Reworded. Was: "Generate-and-test means making content at random, then checking each piece and throwing away whatever fails. Sixty seeds, one square each, and only twelve pass," |
| 59 | B1103 | Figures spoken: `60 of 60` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 60 | B1103 | Explanation of: Constructive generation; in the book text; Build content by rules that guarantee validity.; SEEDS 1 TO 60, BUILT BY RULES | PASS | Second-pass check against slide 12 step 3 and 14-game-ai-and-systems.md | none |
| 61 | B1104 | Figures spoken: `limit 6`, `44`, `200`, `limit 5`, `margin of 1`, `32`, `12 levels` | PASS | Each figure is printed on slide 12 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 62 | B1104 | Explanation of: Safety margin; in the book text; LEVELS ACCEPTED OF 200 SEEDS; limit 6 (no margin) | PASS | Second-pass check against slide 12 step 4 and 14-game-ai-and-systems.md | none |
| 63 | B1201 | Figures spoken: `id 1`, `188.6` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 64 | B1201 | Explanation of: Authority; in the book text; The part of the system allowed to change a value.; TELL THESE APART | PASS | Second-pass check against slide 13 step 1 and 14-game-ai-and-systems.md | none |
| 65 | B1202 | Figures spoken: `3 of 3`, `0 → 3`, `0 of 3` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 66 | B1202 | Explanation of: RPC; in the book text; A function one computer asks another computer to run.; THREE CLIENT CALLS, TWO RPC MODES | PASS | Second-pass check against slide 13 step 2 and 14-game-ai-and-systems.md | none |
| 67 | B1203 | Figures spoken: `60 TICKS`, `3 ticks late`, `1 packet`, `in 5 lost`, `13.0 px` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 68 | B1203 | Explanation of: in the book text; Replication; PLAYER1 HEIGHT OVER 60 TICKS; host's value (black), client's copy (red) | PASS | Second-pass check against slide 13 step 3 and 14-game-ai-and-systems.md | none |
| 69 | B1301 | Explanation of: PAIR 1 · LEFT; Selector; Tries children until one succeeds.; Selector | PASS | Second-pass check against slide 14 step 1 and 14-game-ai-and-systems.md | none |
| 70 | B1302 | Figures spoken: `3 new exit edges`, `1 new branch` | PASS | Each figure is printed on slide 14 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 71 | B1302 | Explanation of: PAIR 2 · LEFT; Finite state machine; Exits are stored on each state.; add “flee when hurt”: | PASS | Second-pass check against slide 14 step 2 and 14-game-ai-and-systems.md | none |
| 72 | B1303 | Figures spoken: `seeds 1 to 12`, `2 accepted`, `12 accepted` | PASS | Each figure is printed on slide 14 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 73 | B1303 | Explanation of: PAIR 3 · LEFT; Generate-and-test; Make at random, reject the bad.; seeds 1 to 12: 2 accepted | PASS | Second-pass check against slide 14 step 3 and 14-game-ai-and-systems.md | none |
| 74 | B1304 | Figures spoken: `4 actions` | PASS | Each figure is printed on slide 14 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 75 | B1304 | Explanation of: PAIR 4 · LEFT; Utility AI; Score every option, pick the top.; chase | PASS | Second-pass check against slide 14 step 4 and 14-game-ai-and-systems.md | none |
| 76 | B1401 | Figures spoken: `220 px`, `260`, `37 switches become 3` | PASS | Each figure is printed on slide 15 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 77 | B1401 | Explanation of: “stop the guard jittering”; WHAT THE INSTRUCTION DOES; one threshold: 37 switches; two thresholds: 3 switches | PASS | Second-pass check against slide 15 step 1 and 14-game-ai-and-systems.md | none |
| 78 | B1402 | Figures spoken: `44 of 200`, `156 of 200` | PASS | Each figure is printed on slide 15 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 79 | B1402 | Explanation of: “make the levels random but fair”; accepted: 44 of 200 seeds; rejected: 156 of 200 seeds; only 44 of 200 raw levels can be crossed | PASS | Second-pass check against slide 15 step 2 and 14-game-ai-and-systems.md | none |
| 80 | B1403 | Figures spoken: `0 to 1`, `150 px`, `health 0.8`, `chase 0.51` | PASS | Each figure is printed on slide 15 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 81 | B1403 | Explanation of: “make the AI choose sensibly”; chase 0.51; flee 0.41; patrol 0.42 | PASS | Second-pass check against slide 15 step 3 and 14-game-ai-and-systems.md | none |
| 82 | B1404 | Figures spoken: `seed 42`, `seed 7` | PASS | Each figure is printed on slide 15 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 83 | B1404 | Explanation of: “make it repeatable”; run 1, seed 42; 628158ee; reference | PASS | Second-pass check against slide 15 step 4 and 14-game-ai-and-systems.md | none |
| 84 | B1405 | Figures spoken: `3 of 3`, `0 of 3` | PASS | Each figure is printed on slide 15 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 85 | B1405 | Explanation of: “don't let a client cheat”; any_peer: client calls accepted 3 of 3; authority: client calls accepted 0 of 3; 3 forged points in Chapter 14's audit; 0 with authority | PASS | Second-pass check against slide 15 step 5 and 14-game-ai-and-systems.md | none |
| 86 | B1501 | Explanation of: Before you trust a Game AI change | PASS | Second-pass check against slide 16 step 1 and 14-game-ai-and-systems.md | none |
| 87 | B1502 | Explanation of: Before you trust a Game AI change | PASS | Second-pass check against slide 16 step 2 and 14-game-ai-and-systems.md | none |
| 88 | B1503 | Explanation of: Before you trust a Game AI change | PASS | Second-pass check against slide 16 step 3 and 14-game-ai-and-systems.md | none |
| 89 | B1504 | Explanation of: Before you trust a Game AI change | PASS | Second-pass check against slide 16 step 4 and 14-game-ai-and-systems.md | none |
| 90 | B1505 | Explanation of: Before you trust a Game AI change | PASS | Second-pass check against slide 16 step 5 and 14-game-ai-and-systems.md | none |
| 91 | B1506 | Explanation of: Before you trust a Game AI change | PASS | Second-pass check against slide 16 step 6 and 14-game-ai-and-systems.md | none |
| 92 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 93 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 4 (Conditions, actions, selectors and sequences), step 1: the two leaf rows contradict the slide's own tree. can_see returns FAILURE on tick 1 while chase returns RUNNING on tick 1, but in Sequence[can_see, chase] chase is not ticked when can_see fails. The rows read as if both leaves were ticked independently.
- Slide 7 step 3: the header says 'EACH REWARD × γ TO THE POWER OF ITS STEP', and the steps are numbered 1 to 5, but the last reward counts 0.815 = 0.95^4 and 0.063 = 0.5^4. The power is the step number minus one. The discounted returns 0.78 and 0.04 are right for that rule.
- Slide 11 step 1: 'gap too wide: 8 columns, limit 6'. In the drawing, the last reached column is 7 and the first unreached is 15, so the gap is seven empty columns; 8 is the jump distance, not the gap width.
- Slide 11 step 4 and slide 14 step 2: 44 of 200 accepted and '81 of the 200 levels the last column is a gap' come from the page's own generator, while the notes cite Lab B's limits. Lab B's run in Chapter 14 gave 43 of 200 and 16 levels ending in a gap. Nothing on screen says these levels are the page's own, so a viewer can take 44 and 81 as the course's results.
- Slide 14 step 2: the caption 'only 44 of 200 raw levels can be crossed' overclaims. Chapter 14 says a validator pass 'does not establish that an accepted level can be crossed'. 'pass the validator' would be accurate. The narration says 'pass'.
- Slide 14 is badged Computed, but step 3 shows the utility scores (chase 0.51, flee 0.41, patrol 0.42) whose weights slide 5 badges Illustrative data. The narration says 'made-up example' there.
- Slide 12 notes say '188.6, 113.0 and the 3 of 3 forged points are from the chapter's Lab C logs', but 113.0 appears on no step. Step 3 shows a simulated '13.0 px' instead, so the note looks stale or confused.
- Slide 2 step 1: the guard returns from Search to Patrol after 'wait 2 ticks', under the title 'A GUARD WITH THREE STATES' and a source naming Task 2, where the guard waits 1.0 s at the last known position. The notes call the run an illustrative script, but the picture does not say so.
- Slide 6 step 2: in the open_door row, the NEEDS text 'has_key, at_door' runs into the GIVES text '+door_open' with no space between them.

## Open after the second pass

- slide 14 step 2: 'In this run, forty-four of two hundred seeds pass' uses the page's own generator, while Chapter 14's Lab B run gave 43 of 200; the narration does not call it the course's result, but 'this run' does not say whose run it is.
