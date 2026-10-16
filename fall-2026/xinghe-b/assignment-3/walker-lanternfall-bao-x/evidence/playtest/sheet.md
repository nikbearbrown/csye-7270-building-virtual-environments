# Playtest sheet — filled in by Bao

Two full runs from a fresh launch (`./walker-lanternfall.command`). Tick what you saw or heard, and write what you noticed in your own words — these notes go straight into TEST-REPORT.md and FRICTIONAL.md.

- **Run A — sound on.** Date/time: ______  Result (won / lost at m:ss): ______  Level reached: ___  Took Sunflare? ___
- **Run B — press M on the title screen, play fully muted.** Date/time: ______  Result: ______  Level: ___  Sunflare? ___

## Controls and states (both runs)

| Check | A | B | Notes |
|---|---|---|---|
| Enter / A starts; WASD / arrows / stick move; diagonal speed feels the same | | | |
| Courier faces the way you move; moving up/down keeps the last facing | | | |
| You can see idle, walking (two frames), cast, hurt, level-up, defeat or victory | | | |
| Level-up pauses the field; 1 / 2 / 3 (or d-pad + A) pick a card | | | |
| Esc / P pauses and resumes; R restarts from anywhere | | | |
| F3 shows the hurtbox; does it feel fair where you get hit? | | | |

## Sound (run A)

| Check | Heard once per event? | Notes |
|---|---|---|
| SFX-01 enemy dies (dense waves: does it machine-gun?) | | |
| SFX-02 gem collected | | |
| SFX-03 you get hit | | |
| SFX-04 level up | | |
| SFX-05 Sunflare evolution | | |
| SFX-06a lose stinger / SFX-06b win stinger | | |
| Tap a direction key fast 10 times, then hold it 5 s: any sound from input alone? | | |
| Music loop point (every 20 s): click, gap or tempo jump? | | |
| Pause: music muffled and quieter, then back to normal? | | |
| Level-up: music dips while choosing? | | |
| After Sunflare: the brighter layer fades in? | | |
| Lose: music fades out, then the stinger. Press R during the fade: music restarts cleanly? | | |
| M / 9 / 0: all / music / effects mute, and the HUD shows it | | |

## Without sound (run B)

| Question | Answer |
|---|---|
| Could you tell when you were hit? | |
| Could you tell when you levelled up and when you evolved? | |
| Could you see the fog-wraiths on the cobbles? (measured contrast 0.03 — the lowest) | |
| Is the courier big enough to track? | |
| Anything you only understood with sound on? | |

## Open questions for you to decide

1. Wraith visibility: keep, or brighten its colours?
2. Courier size: keep 32 px frames, or show it larger?
3. Hurtbox: keep r = 10 (now reaches the lower half of the lamp) or shrink to about 7?
4. Difficulty: did you reach Sunflare inside 3 minutes? Too easy / too hard?

## One thing to change and re-test

Pick one problem from above → what we changed → play again → did it fix it? (This is the required observe → change → re-verify loop.)
