# walker-rudy

A 2D side-scroller for CSYE 7270, Assignment 2: *Generate Art, Sound, and Music for Your Game*. By Shuai Zhang.

You play Rudy, a cheerful chibi boy who crosses a medieval countryside to reach the teleport circle at the end of each level. The game on one page: [CONCEPT.md](CONCEPT.md).

| | |
| --- | --- |
| Status | The art is generated and in the game: Rudy's reference (CHAR-REF-07), his nine default-form and seven sword-form poses, the Level 1 sky, fields and ground, the spikes, the waystone, the teleport circle, the pickup, the goblin, the hearts and the end card; see [ASSET-LOG.md](ASSET-LOG.md). The game in `game/` was built as a greybox with code-drawn placeholders in steps 1a–1d (Rudy on flat ground; the layout, falls and the checkpoints; hearts, spikes, goblins and the stomp; the sword form), and the art went in during steps 2a (Rudy, with the 4 px outer outline), 2b (the layers, the ground and the spikes), 2c (the other props, the goblin, the hearts and the end card) and 2d (the title over the opening). Step 3 put in the audio: the six generated sound effects and the music loop on their own buses, with the music's dips under a hit, the pause and a death, its fade on the teleport circle, Esc to pause and M/N to mute. Step 4, the mushroom (a "should"), is cut. Step 5 verified it: [TEST-REPORT.md](TEST-REPORT.md), with my playtest, sound on and muted. The design before generation is tagged `design-v1` |
| Started from | An empty repository (not walker-jumpman and not my Assignment 1 project) |
| Engine | Godot 4.7.2.stable.official.ed1daf0bf, the standard build, with GDScript; the project is `game/` |
| Assistance | Claude Code. The human/AI split is recorded in [FRICTIONAL.md](FRICTIONAL.md) and [SOURCES.md](SOURCES.md) |
| Final film | *Walker Rudy, Wired In.* (Brutalist `godot-gamedev`, `walker` modifier; 9:56, 3840×2160), file `claude-liam-walker-rudy-gamedev.mp4`, SHA-256 `cb2f01dbe7f0788b5a8c9196b8168e2f2151e4be09aee4febee018a1165528a0`. The film names its source as `3b7aa1c`, the local commit ID; in the course repository that commit is `9871718`, with the same files. The MP4 is not in git; its beat sheet, capture logs and evidence are in [youtube/claude-liam-walker-rudy-gamedev/](youtube/claude-liam-walker-rudy-gamedev/). Course media: [claude-liam-walker-rudy-gamedev.mp4 on Google Drive](https://drive.google.com/file/d/1E_FuS_34ep_KN5FeWtA05CpvjM1pOXNl/view?usp=drive_link) |

## What the slice demonstrates

Level 1, Harvest Fields, as one Godot scene: Rudy runs and jumps across the fields from the title to the teleport circle, over spikes and two cliffs, past three goblins he can stomp, and through a sword-and-shield pickup that lets him cut them but is knocked away by the next hit. Three hearts; a waystone checkpoint; a fall costs a heart, and the last heart starts the level over. Every picture of Rudy, the level, the props, the goblin, the hearts and the end card is generated (Gemini); the six sound effects (Adobe Firefly, ElevenLabs) fire on the jump, the stomp, a hit, the teleport circle, the slash and the pickup; the music (Suno) loops under play, dips under a hit, the pause and a death, and fades out at the end.

Known limitations, in full in [TEST-REPORT.md](TEST-REPORT.md#known-limitations): one level; the mushroom monster, its spore and blocking are cut; four planned sounds were not made (a fall plays the hurt sound, and the waystone is silent); tested only on macOS.

## Run the slice

Open `game/project.godot` in Godot 4.7.2, or run it from the repository root (in a fresh clone, run the import line first):

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path game --import
/Applications/Godot.app/Contents/MacOS/Godot --path game
```

Controls: A/D or ←/→ to move (on the ground, a tap of the other direction turns Rudy on the spot; hold it to move); Space, W or ↑ to jump; J or X to slash, once Rudy has the sword; Enter on the title starts play, and on the end card plays the level again; Esc pauses and resumes play; M mutes the music and N the sound effects; F1 shows or hides the debug line, which is hidden at the start.

Checks, headless: `Godot --headless --path game --fixed-fps 60 res://tests/checks.tscn`. Screenshots for inspection (opens a window): `Godot --path game --resolution 1920x1080 --always-on-top res://tests/capture.tscn -- 1a 1b`, which writes to `evidence/<step>/`. Step 3's audio is recorded with Godot's movie maker: add `--write-movie <file>.avi` and name step `3`, then `python3 design/tools/plot_mix.py <file>.avi` measures the mix and draws `evidence/3/3-mix.png`. Step 5's comparison sheets: capture step `5`, then again with `--debug-collisions`, then `python3 design/tools/compare_sheets.py <commit>`.

## Design documents

- [CONCEPT.md](CONCEPT.md): the game on one page (design v1, tag `design-v1`, with dated revisions)
- [STORYBOARD.md](STORYBOARD.md): seven panels of the play experience (design v1, tag `design-v1`, with dated revisions; blockout pictures in `design/storyboard/`)
- [CHARACTER-SHEET.md](CHARACTER-SHEET.md): the contract for Rudy's generated frames (design v1, tag `design-v1`, with dated revisions; blockout images in `design/character/`)
- [CHANGE-BRIEF.md](CHANGE-BRIEF.md): the asset list, event-to-sound map, music behavior and predicted failures (design v1, tag `design-v1`, with dated revisions)
- [TEST-REPORT.md](TEST-REPORT.md): the checks, my playtests, the storyboard and character sheet against the slice, and what the predicted failures turned out to be
- [design/generation-prompts.md](design/generation-prompts.md): the prompt templates the generations started from
- [design/character/collision-r2.png](design/character/collision-r2.png): the collision shapes the slice uses, over all 16 game frames
- [design/tools/make_blockouts.py](design/tools/make_blockouts.py): draws the blockouts (code written by Claude; not a generative model)
- [ASSET-LOG.md](ASSET-LOG.md): every generation kept or seriously considered, with its prompt, outcome and reason
- [SOURCES.md](SOURCES.md): starting point, tools, generative models and their terms, and who did what
- [FRICTIONAL.md](FRICTIONAL.md): a dated log of the design decisions
