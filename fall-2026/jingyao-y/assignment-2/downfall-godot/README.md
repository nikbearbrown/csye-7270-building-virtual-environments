# Downfall — Assignment 2 (CSYE 7270): generated art, sound and music

**Author:** Yuan Jingya, with Claude Code assistance. **Engine:** Godot 4.7.2-stable (GL Compatibility), Windows 11.

**Project name:** `downfall-godot`, in the repository `coldfish432/GodotGame`. It does **not** start with `walker-`; the author kept the existing repository (see [SUBMISSION.md](SUBMISSION.md)).

**Started from:** the author's own earlier Downfall project (Unity prototype → Godot port). It did not start from walker-jumpman or Assignment 1.

## What the assignment slice demonstrates

The whole game is the playable slice:

- **Lappland's states:** idle, walk, three combo attacks, the sword wave and hurt, with 8-direction facing. All are swapped from generated sprite atlases.
- **Environments:** three generated field surfaces and prop groups, plus the generated Rhodes base.
- **Event sounds:** four generated warehouse event sounds on real `room_reveal.gd` signals. Two (lights on, lights off) are generated files; two (hatch, shelf) are counted but silent until generated.
- **Music:** a generated base loop and field loop, plus two stings with the predicted pause, death and extraction behaviour.
- **Mute:** a mute toggle.
- **Design docs:** [CONCEPT](CONCEPT.md), [STORYBOARD](STORYBOARD.md), [CHARACTER-SHEET](CHARACTER-SHEET.md), [CHANGE-BRIEF](CHANGE-BRIEF.md), [TEST-REPORT](TEST-REPORT.md), [FRICTIONAL](../FRICTIONAL.md), [SOURCES](SOURCES.md) (asset log), [SUBMISSION](SUBMISSION.md). The design docs are retrospective, and they say so.

## Run

Open this folder's `project.godot` in Godot 4.7.2 (the same game files are in https://github.com/coldfish432/GodotGame at `100dce3`), or run:

Open `project.godot` in Godot 4.7.2 and press F5 (main scene `game/main.tscn`), or run:

```powershell
& 'Godot_v4.7.2-stable_win64.exe' --path downfall-godot
```

## Controls

| Input | Action |
|---|---|
| Right-click | Move |
| Left-click | Attack (a full charge releases the sword wave) |
| Shift | Dodge |
| Q | Potion |
| E | Interact |
| I / C | Bag |
| R | Relics |
| M | Map |
| J | Contract |
| Esc | Pause / settings |

**Mute:** Esc → Settings (设置) → 静音 mutes all audio. Music and SFX have their own buses, but there is no separate toggle for each.

## Tests

```powershell
& 'downfall-godot	ests
un_all.ps1' -Visual
```

This includes `tests/test_audio.gd` (sound-trigger counts, loop points, pause/end behaviour) and `tests/test_relic_icons.gd`.

## Known limitations

- **Copyright:** the game uses the Arknights IP (character, setting, PRTS references), against the assignment's rights rule.
- **Design after generation:** the design came after much of the generation.
- **Character sheet:** 7 distinct poses, not 10.
- **Sounds:** the hatch and shelf sounds are not generated.
- **Mute:** there is no separate music/SFX mute.

See [TEST-REPORT.md](TEST-REPORT.md) §Honest limitations.

**Local-only files:** `../evidence/` and `music/` (raw MP3 downloads) live outside this repository; the docs say so where they reference them.

**Final film:** `claude-liam-downfall-gamedev.mp4` (4K, 6:23). The SHA-256 and link are in [SUBMISSION.md](SUBMISSION.md); its sources are in `youtube/claude-liam-downfall-gamedev/`.
