# Game design terms: source notes (Crash Course Games, "Game Design", host Andre Meadows)

Status: source list only, for the future "Terms - Game design" deck. No deck built yet. Bear said he will look for more sources; add them here. Meanings are in my own words, not the transcript's; timestamps point to where the video explains each one. Check the glossary overlap before building: `GLOSSARY-jargon-midterm.md`, "Game design documents" already defines Core loop, Player verb, Mechanic, Level design, GDD, Pitch, Brief.

## Five building blocks (0:48 to 2:46)

| Term | Plain meaning | At | Glossary overlap |
|---|---|---|---|
| Game design | Turning a story or gameplay idea into something playable; includes art, programming and writing | 0:48 | no |
| Space | The look, sound, lighting and physical setting of the game; it shapes which characters, feelings and actions fit | 1:38 | no |
| Components | The objects in the space that the player uses or meets: characters, weapons, vehicles, even Easter eggs | 1:53 | no |
| Mechanics | What the player can do; think verbs | 2:04 | yes: Mechanic, Player verb |
| Core mechanic | The action the player repeats most (running and shooting in Halo) | 2:08 | partly: Core loop |
| Goals | What the player is trying to achieve to win; the designer maps a route to it | 2:16 | no |
| Rules | The constraints on what players can and cannot do; they also shape the play experience | 2:32 | no |
| House rules | Rules players change for their own table, which changes the play | 2:43 | no |
| Play testing | Having players challenge the design so it can be revisited and improved | 1:13 | no |

## Wants and needs (2:47 to 3:11)

| Term | Plain meaning | At |
|---|---|---|
| Eight Kinds of Fun (Marc LeBlanc) | A list of what players broadly want: challenge, narrative, fantasy, discovery and others. The video names four | 2:55 |

## Dice-game principles (Gerald Cameron, 3:11 to 4:29)

| Term | Plain meaning | At |
|---|---|---|
| Downtime | Time a player waits with nothing to do; "downtime is the enemy". Dice turns average about 15 s | 3:23 |
| One roll per turn | More rolls per turn add downtime and distort the odds | 3:42 |
| Give players a chance to react | Everyone has something to do on every roll | 3:58 |
| Low rolls should not suck, high rolls should not rule | Every result should count a little; no all-or-nothing outcome | 4:11 |
| Probability | What dice games are built on; the odds of each result | 4:23 |

## Board-game principles (Ananda Gupta, 4:29 to 5:24)

| Term | Plain meaning | At |
|---|---|---|
| Player count sweet spot | Two to three players keeps downtime low | 4:38 |
| Playtime | About two hours: short games leave players wanting more, long games cause burnout | 4:48 |
| Luck and strategy | Strategy tests skill; luck gives enough randomness to bring players back | 5:04 |
| Balance | No role has an unfair advantage at the start; every player feels they can win | 5:14 |

## Video-game principles (5:24 to 6:25)

| Term | Plain meaning | At |
|---|---|---|
| Meaningful play | The player acts and the game responds in a way that matters | 5:33 |
| Descriptive meaningful play | Action, then a clear response (the bola shatters the ice) | 5:38 |
| Evaluative meaningful play | The player steps back and asks why this action matters to the whole game | 5:47 |
| Gameplay balance | Every advantage has a disadvantage (the sniper's blind spot; Pokemon type triangle) | 5:56 |
| Rock-paper-scissors balance | Each option beats one and loses to another, so no option wins everywhere | 6:09 |

## Two worked examples (6:25 to 9:04)

| Term | Plain meaning | At |
|---|---|---|
| Teaching through level design | World 1-1 teaches jump, move, enemy versus power-up and hidden blocks without text | 6:33 |
| Design the middle first | Miyamoto designs the engaging middle levels first, then the opening levels that lead players there | 7:49 |
| Risk, deduction and luck | The mix Love Letter relies on | 8:06 |
| Simple rules, deep tactics | Learnable in minutes yet worth replaying; rounds are short so no one is out for long | 8:28 |

## Deck notes

- About 28 terms. Fits one deck. The animations are easy to compute: downtime as a timeline of turns, balance as a payoff table, probability of dice sums, one roll versus re-roll distribution, type triangle.
- Several terms are about board and dice games. Say so on the slide, or keep the deck to the ones that apply to a Godot game (mechanic, goal, rules, space, components, playtesting, balance, meaningful play, teaching through level design, downtime).
- Attribution: cite the video by name on each slide. Do not copy its wording.

---

# Source 2: "basic tips on game design" (YouTube video; title and channel not in the pasted transcript, add them)

Meanings in my own words; timestamps from the transcript. Sponsor and thanks sections skipped.

| Term | Plain meaning | At | Overlap with source 1 / glossary |
|---|---|---|---|
| Intended experience | Every design choice must fit the experience you want the player to have; no rule fits all games | 1:37 | no |
| Three pillars: player, communication, appeal | The foundation of a game | 1:45 | no |
| Player role and purpose | What the player does and why; the player, not the game, drives it forward | 1:57 | partly: Goals |
| Player agency | The player's actions change the game; without it they only complete tasks | 2:08 | partly: meaningful play |
| Communication | Showing the player the goal and how to reach it, with the environment or visual clues; without it they feel powerless | 2:18 | no |
| Appeal | The pull to keep playing; varies by game and by player (action, story, puzzle) | 2:51 | no |
| Prototype | A simplified version made first to test whether the appeal is there | 3:28 | no |
| Guiding the main focus | Making clear what the player should concentrate on | 3:56 | no |
| Linear / nonlinear | Straight from start to end / the player has alternate choices such as a side quest | 4:06 | no |
| Side quest | A detour from the main storyline | 4:18 | no |
| Anticipation | Preparing the player for what comes next, such as a charge-up animation before an enemy attack, so it does not feel cheap | 4:27 | no |
| Build-up | A sequence that raises tension toward an event (sound, sparks, camera shake before an explosion) | 4:40 | no |
| Logical events | What happens in the game must make sense and meet the player's unspoken expectations (bullet holes, fitting sounds) | 5:00 | no |
| Consistent rules | Even where a game bends physics, it does so the same way every time | 5:27 | partly: Rules |
| Games can cheat | Hidden help the player does not notice, such as enemies told not to turn around when sneaked up on | 5:38 | no |
| Dynamic | Many things happening at once so play stays fresh (smoke, flank and charge in one round) | 6:08 | no |
| Progression | A natural rise in challenge; do not over-stimulate or under-stimulate | 6:50 | no |
| Pacing | Alternating high-concentration and calm moments; tower defence alternates waves with building | 7:01 | no |
| Spacing (environment) | Open areas to admire the view versus tight, claustrophobic ones; changes pace and gameplay; leave enough room for AI and other players | 7:27 | partly: Level design |
| Wave | A group of enemies sent together; many weak or few strong | 7:19 | no |
| Guidelines, not rules | The tips steer creativity; the rest is up to the designer | 8:14 | no |

Deck notes for both sources together: about 49 terms, which would be over the 40-term cap in TERMS-TEMPLATE.md. Split into two decks: "Game design A: elements and principles" (space, components, mechanics, goals, rules, balance, intended experience, pillars) and "Game design B: pacing and guidance" (communication, anticipation, progression, pacing, spacing, prototype, playtesting). Overlaps to merge: goals, rules, balance, mechanics, meaningful play and agency, level-teaching and communication.

---

# Source 3: Game/Show episode on interesting choices (host Jamin; episode title not in the pasted transcript, add it)

Only the first 6:40 is about design. The second half (viewer comments on VR environments, apocalypse media) and the sponsor read are off topic and skipped. Meanings in my own words.

| Term | Plain meaning | At | Overlap |
|---|---|---|---|
| Meaningful choice | A choice that changes what happens and that the player has to think about, even in a simple game (the Space Invaders UFO) | 0:36 | yes: meaningful play (source 1), agency (source 2) |
| Risk versus reward | A harder or riskier action pays more (UFO worth 50 to 300 points, tricky to hit) | 1:10 | no |
| Factors in a decision | What the player weighs: score, lives left, how the fight is going right now | 1:21 | no |
| Multiple lives | A stock of tries; it changes how risky a choice feels (first used in Space Invaders, per the video) | 1:30 | no |
| "Games are a series of interesting decisions" (Sid Meier) | The idea that design is mostly about the decisions the player makes | 2:08 | no |
| Trade-off | Give up one thing to get another (Galaga: lose a ship to rescue it and fire twice; Shovel Knight: destroy a checkpoint for treasure; Ikaruga: absorbing shield, weaker attack) | 2:25 | no |
| Persistence | You live with the choice for a set time (Pac-Man's four power pellets; robbing the Spelunky shop) | 3:17 | no |
| Situational choice | The same choice is better or worse depending on the situation the player is in (Doom's enemy mix) | 3:50 | no |
| Orthogonal unit differentiation (Harvey Smith) | Each unit or enemy type does something different, which forces the player to prioritise | 4:37 | no |
| Enemy behaviour matrix | Enemies sorted by charge versus stay back and dodgeable versus certain hit (imp, cacodemon, shotgun guy, heavy weapon guy) | 4:08 | no |
| Prioritising targets | Choosing which enemy to deal with first by how dangerous it is in this arrangement | 4:49 | no |
| Personalisation (personal choice) | Players build their own play style from their decisions: aggressive chess, turtling in Street Fighter, a Netrunner deck | 5:21 | no |
| Autonomy / agency | The player takes control of how they play | 5:18 | yes: agency (source 2) |

Computable animations for the deck: expected value of the UFO choice (score, lives, risk), Doom priority queue (damage per second the player cannot dodge), Pac-Man power-pellet budget over a stage, trade-off payoff table.

Deck note: sources 1 to 3 total about 62 terms with overlaps; after merging duplicates roughly 50. Proposed split: A "Game design: elements and principles", B "Game design: pacing and guidance", C "Game design: choices" (this source, about 13 terms plus the overlaps with meaningful play and agency).

---

# Source 4: "So You Wanna Make Games?? | Episode 10: Game Design" (Riot Games series; https://www.youtube.com/watch?v=yYYtBFSxoCg; transcript saved in books/youtube-transcripts/playlist-PL42m9XiTqPHJdJuVXO6Vf5ta5D07peiVx)

Meanings in my own words. Terms: game (goal, opposition, decisions, rules), types of fun, target experience, art / design / engineering aim together, mechanics set thematic feel, movement patterns, clear progress toward a goal, climactic arc, opposition and frustration (good versus bad), fairness (clear expectations, consistency), luck and skill (Candy Land, Counter-Strike, battle royale mix), goals versus tactics, curating ideas.

# Deck assignment (decided 2026-11-10)

- **A: `01 Game design A.html` (BUILT, 14 slides, 22 terms):** game, goal, opposition, decisions, rules, house rules, mechanic, player verb, core mechanic, core loop, thematic feel, movement pattern, types of fun, target experience, appeal, art/design/engineering, space, components, prototype, play testing, clear progress, climactic arc.
- **B: `02 Game design B.html` (BUILT, 14 slides, 19 terms):** meaningful play (descriptive, evaluative), meaningful choice, agency / autonomy, risk versus reward, trade-off, persistence, situational choice, orthogonal unit differentiation, personalisation, frustration (good and bad), fairness, difficulty, luck and skill, balance, rock-paper-scissors, downtime, probability.
- **C: `03 Game design C.html` (BUILT, 15 slides, 19 terms):** pillars (player, communication, appeal), communication, guiding focus, linear / nonlinear / side quest, anticipation, build-up, logical events, consistent rules, games can cheat, dynamic, progression, pacing, waves, spacing, level design, teaching through level design, design the middle first, goals versus tactics.

Tag scheme used in deck A: "in the book text" (chapters use and explain it: only Mechanic, Chapter 5), "in the glossary" (a row in GLOSSARY-jargon-midterm.md: Goal, Player verb, Core loop), "video only".
