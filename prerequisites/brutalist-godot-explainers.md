# Required Brutalist Godot explainers

CSYE 7270 · Fall 2026

Every 100-point assignment, due every 10 days, includes an explainer made with [Brutalist](https://github.com/nikbearbrown/brutalist.art) and the Godot skill appropriate to the assignment. The assignment tells you the required film coverage; do not assume all three skills mean three required films each time.

Read the [course AI policy](ai-policy.md) and watch [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Choose the skill by what you need to explain

| Skill | What the film explains | Evidence to show |
|---|---|---|
| `godot-walkthrough` (alias of `godot-waikthrough`) | What the implemented game does while it is played | Real Godot gameplay, controls, feature outcomes, failure/recovery, and completion where present |
| `godot-gamedev` | How the game is built | Actual code, scenes, resources, assets/art, an input → state → output trace, and relevant tests |
| `godot-gdd` | Why the design is specified that way | GDD requirements and trade-offs connected to game evidence; clear separation of proposals, implemented features, tests, and pending human decisions |

The spelling `godot-waikthrough` is the toolkit's original command; `godot-walkthrough` is a supported alias. These are **agent-driven film workflows**, not a standalone `walker` executable that automatically makes a game or a film. Ask Claude Code to read and follow the installed skill. Check that your course-provided Brutalist version includes the selected skill; if it is missing, ask for the appropriate update rather than inventing commands.

The optional `walker` modifier adds the Claude/Walker prompt opening, a summary of what was actually built, and the Verdict → Your Turn → regular outro sequence. A reconstructed opening prompt must be labeled as a reconstruction, not represented as a historical session. Use the modifier when the assignment requests it or when it helps explain the Walker process.

## Example requests to the coding agent

These are requests to Claude Code, not commands to paste directly into a shell. Replace the example path with your own game package.

```text
Read Brutalist's godot-walkthrough skill and follow its walker mode on
/path/to/walker-my-game. Show the implemented features and a real failure
and recovery. Identify my changes from the starter. Preserve the game.
Render the film, review it against its evidence, and do not publish it.
```

```text
Use Brutalist's godot-gamedev walker workflow on /path/to/walker-my-game.
Explain the actual components, source, assets, and tests. Make my changes
from the starter explicit. Label reconstructed editor views and distinguish
headless checks from human playtesting. Render and check the final film.
```

```text
Use Brutalist's godot-gdd walker workflow on /path/to/walker-my-game
and its GDD.md. Explain the design contract using existing game evidence.
Keep planned, built, tested, and human-reviewed claims separate. Render
and check the film; do not change the GDD or implement missing features.
```

## What a sufficient explanation does

- Explains the concept correctly, with claims you can defend.
- Shows the mechanism through meaningful motion, a worked example, or actual output—not narration alone.
- Uses real, reproducible numbers where numbers matter; labels constructed examples and reconstructed views.
- Identifies at least one thing the evidence does not establish.
- Identifies the starter, your substantive changes, the source revision, and the human/AI contributions.

Use the current skill's rendering, audio, coverage, and regular-outro checks. Those checks support the submission; they do not certify truth or replace watching the final film. Skill defaults target native 4K landscape output. No extra vertical version or public upload is required unless the assignment explicitly asks for it. If a Short is requested, it must be a separate native 9:16 cut strictly under 3:00, not a crop of the entire long film.

## Film as code: what to submit

Keep the game's source, film source, and rendered media tied to the same submitted revision:

- **GitHub:** required game source, `README.md`, `SOURCES.md`, `FRICTIONAL.md`, the beat sheet, script/prompts, relevant coverage/evidence records, and reproducible build instructions. Preserve provenance; remove secrets and unnecessary private chat content.
- **Designated media storage:** the final rendered film and other MP3/MP4 or files over 25 MB. Link the exact media version from the README, with filename and checksum where available. Ensure reviewers can access it.
- **Canvas:** required submission files, the matching GitHub folder/repository link, final commit hash, and accessible film link. A beat sheet without the rendered film does not satisfy the video requirement.

Implementation and substantive explanation belong to the assignment's **60-point** category. Frictional is **10**, proper GitHub/Canvas version matching is **10**, and Relative Quartile is **20**. There is no additional video-points category. Visual polish can support clarity but cannot substitute for correct work.
