# TEST-REPORT — walker-rudy

> 2026-10-04, build step 5. Written by Claude Code from the runs below and from FRICTIONAL.md. My own playtest is quoted in my words, with Claude's translation; nothing in it is written for me.

| | |
|---|---|
| Source tested | Commit `9871718` ("Step 5: verify the slice; my playtest; the debug line hidden"): the fresh-copy run, the checks and the screenshots in `evidence/5/`. My playtest was at `10c0c2e` ("Step 3: the audio"); the only change to the game since is the debug line, hidden at the start |
| Commit IDs | Commit IDs refer to the course repository. The project was developed in a local repository and moved there with its history; each listed commit has the same files as the local one that was tested |
| Engine | Godot 4.7.2.stable.official.ed1daf0bf, the standard build, GL Compatibility renderer |
| Machine | macOS 15.1 (24B83), Apple M3 |
| Run on | 2026-10-04 |

## Summary

| Check (the assignment's) | Result | Evidence |
|---|---|---|
| Startup and controls | A fresh clone of `9871718` imports with no errors, passes every check, and runs windowed with no errors. Every file the game names by a `res://` path is in git. My playtest by hand: no problem reported | [Startup and controls](#1-startup-and-controls) |
| Character against the sheet | Every game pose, facing right and left, beside its sheet pose, with the collision shapes. Differences and collision mismatches listed | `evidence/5/5-character-vs-sheet-default.jpg`, `5-character-vs-sheet-sword.jpg` |
| Storyboard against the slice | All seven panels beside the same moment in the game. Panel 4's mushroom, spore and block are not in the slice (cut) | `evidence/5/5-storyboard-vs-slice.jpg` |
| Sound events | The four required events (jump, stomp, hurt, portal) and the other two (slash, pickup): one sound per occurrence in the checks, including mashed and held keys and two events in one tick. My playtest: the sound effects "were all clear", and mashing and holding the jump and slash keys gave one sound each time | [Sound events](#4-sound-events) |
| Music | Pause and end behave as predicted, checked and measured in the game's recorded mix. The seam: inaudible in the previews, and in my playtest over at least three repetitions "the BGM was fine too" | [Music](#5-music) |
| Muted play | Muting changes nothing in play (checked). My playtest muted: "I found no problems either" | [Muted play](#6-muted-play) |
| Automated check | 141 checks, all passing, with the command below | [Automated check](#7-automated-check) |

## 1. Startup and controls

From a fresh copy, as a reviewer would get it (`git clone` of the local repository into a new folder, so nothing ignored by git, such as `_raw/` or the `.godot/` cache, comes along), first at `10c0c2e` and again at `9871718`:

```bash
git clone <repository> fresh && cd fresh
/Applications/Godot.app/Contents/MacOS/Godot --headless --path game --import
/Applications/Godot.app/Contents/MacOS/Godot --headless --path game --fixed-fps 60 res://tests/checks.tscn
/Applications/Godot.app/Contents/MacOS/Godot --path game --quit-after 600
```

- **Import:** exit code 0 at both commits; no error, warning or missing-resource line.
- **Checks:** exit code 0; all 139 checks at `10c0c2e`, and all 141 at `9871718`, passed.
- **Windowed run:** the game opened on the title and ran 600 frames; exit code 0 at both commits, and no error or warning in the output.
- **Every used asset is present:** the 75 `res://` paths named in the game's scenes, resources, shaders, scripts and `project.godot` are all tracked in git. Step 5 adds this as a check, so every later run repeats it (it passed in the fresh clone of `9871718`); with `props.json` moved away as a test, it fails.
- This was a local clone. On 2026-10-07 the same three commands were run again on a fresh `git clone` from GitHub, branch `shuai-z/assignment-2` of my fork of the course repository, at `5865362`, in `fall-2026/shuai-z/assignment-2/`: import exit code 0 with no error, warning or missing-resource line; all 141 checks passed, exit code 0; the windowed run exited 0 with no error or warning. `game/` there is the same tree as at `9871718` (git tree `96db935`); the commits since change only documents.

Controls, as README.md lists them: A/D or ←/→ to move; Space, W or ↑ to jump; J or X to slash with the sword; Enter to start and to play again; Esc to pause; M and N to mute the music and the sound effects; F1 to show or hide the debug line. The checks drive every state change through the same input actions (`Input.action_press`): running, turning on the spot, jumping, the pickup, the slash, the stomp, the hits, the falls, the waystone, the teleport circle, the end card, the title, the pause and the mutes.

My playtest (see [My playtests](#my-playtests)) reported no problem.

## 2. Character against the sheet

`evidence/5/5-character-vs-sheet-default.jpg` (nine poses) and `5-character-vs-sheet-sword.jpg` (six): each game pose as CHARACTER-SHEET.md draws it (the blockout in `design/character/poses.png`), beside the in-engine crop facing right and facing left, and the same two crops with Debug → Visible Collision Shapes on. The crops are from capture step 5 in the final Level 1 (the full-size files are in `evidence/5/`).

Against the sheet:
- **Every pose the controller picks is shown**, in both directions: the nine default-form poses (sheet #2–#10) and the six sword-form poses (#11, #12, and #3–#6 with the props). The turnaround (#1) is a reference, not a game pose.
- **Not in the slice:** the block pose (#13), cut with the mushroom (step 4, see CHANGE-BRIEF.md). Its frame is generated and loaded, but nothing shows it.
- **Facing left is a runtime flip**, as the sheet says, so facing left the sword and shield change hands. Every pose flips; the respawn is only ever seen facing right, because he always gets back up facing right.
- **Differences from the blockouts, all accepted earlier:** about 3.4 heads instead of 2.5, and the pale trim on the robe (CHARACTER-SHEET.md, revision 2); CHAR-HURT thrown almost flat, with gold motifs on the trim (HURT-02, accepted 2026-10-01); the two run frames keep the same leg behind (accepted 2026-10-02, after the ChatGPT redo failed); CHAR-CELEBRATE in three-quarter view; the falling pose leaps forward, so a jump in place keeps the rising pose (revision 3).

Against the collision shape (the 40 × 136 px capsule, drawn over all 16 frames in `design/character/collision-r2.png`, CHARACTER-SHEET.md revision 4):
- **Standing and running:** the capsule stays on his torso, with its bottom on his soles on the ground line, in both forms and both directions.
- **In the air:** the robe, the arms, the sword and the shield reach outside the capsule. That is the design: only the capsule is hit, so a hit that grazes his hair, his sword or his shield misses.
- **CHAR-HURT, CHAR-DEFEAT and CHAR-RESPAWN** lie or kneel outside the capsule. In those states he is invulnerable or cannot be touched, so the mismatch never decides a hit.
- **The faint square in front of him** is the sword's hitbox, drawn even while it is off; it is live only 0.03–0.18 s into a slash, which the slash crops show.

## 3. Storyboard against the slice

`evidence/5/5-storyboard-vs-slice.jpg`: each storyboard blockout (`design/storyboard/`) beside the same moment in the game, full screen (`evidence/5/5-panel-1.jpg` to `5-panel-7.jpg`, capture step 5). The debug line is hidden, as it is at the start since my playtest; F1 shows it.

| Panel | In the slice | Differences, and why |
|---|---|---|
| 1. First sight | Yes | As planned: the start of Level 1 with "Walker Rudy" (named in step 2d), "Level 1 · Harvest Fields" and "Press Enter to start"; the hearts appear when play starts. The first spikes and a goblin are already in view at the right |
| 2. Core action | Yes, as two moves | The jump over the spikes and the stomp are two moves: the goblin's patrol starts 435 px after the spikes, and a running jump covers about 390 px. The screenshot is the top of the jump over the spikes with the goblin ahead. At the top of a running jump he already shows CHAR-FALL (CHARACTER-SHEET.md, revision 3) |
| 3. Success | Yes, in the gameplay shot | The panel is a design view (close-up, low angle), and says that in play it happens in the medium gameplay shot; the screenshot is that shot, just after the pickup, in the sword form. The pickup disappears at once instead of its glow fading |
| 4. Failure | Partly | **Not covered:** the mushroom monster, its spore from behind, the block pose and SFX-SPORE, all cut (step 4). The failure in the slice is walking into a goblin or onto the spikes: the gear flies off, the hearts stay at three, he shows CHAR-HURT, flashes and is knocked back, and the camera shakes; SFX-HURT plays and the music dips |
| 5. Recovery | Yes, with the revised rules | Since the step 1c playtest a fall costs a heart instead of being instant death with the hearts refilled, so he gets back up with two; the sound is SFX-HURT instead of the cut SFX-FALL (CHANGE-BRIEF.md revisions, 2026-10-02). The lit waystone shows its halo, added after the step 2c playtest |
| 6. The end | Yes | As planned: CHAR-CELEBRATE, the column of light (deep gold since the step 2c playtest) and the camera pulled back to 0.8; the music fades out under SFX-PORTAL |
| 7. Level complete | Yes | As planned: "Level complete" and "Press Enter to play again" over ENV-ENDCARD; silent |

Panels the slice does not cover: none as a whole. Within panels: panel 4's attack from behind (the mushroom, the spore, the block), and panel 3's close-up camera.

## 4. Sound events

Each event's sound plays from the code that represents the event, through `Sfx.play(id)`; the event-to-sound map and its guards are in CHANGE-BRIEF.md. Checked headless by counting `Sfx.play` calls per ID against what the checks saw happen:

| Event (assignment role) | Sound | Checks (all passing) |
|---|---|---|
| Jump (action) | SFX-JUMP | a tap: one jump, one sound; holding the key: one jump, none on landing; a press in the air: no jump, no sound; mashing for 160 ticks: one sound per takeoff, each on the tick he leaves the ground |
| Stomp (success) | SFX-STOMP | landing on a goblin: one sound, no hit; on two goblins in the same tick: two sounds; coming down on a defeated goblin again: no more; a full-speed fall from the top of a jump: still one stomp, not a hit; a sword cut: no stomp sound |
| Hurt (failure) | SFX-HURT | the spikes: one sound per heart; the spikes and a goblin at once: one sound; standing on the spikes: the next sound only after the invulnerability; the gear knocked away: one sound; a fall: one sound at the kill line, though he stays below it |
| Teleport circle (completion) | SFX-PORTAL | one sound; stepping on again: no more |
| Slash | SFX-SLASH | no sword: nothing; a tap: one swing, one sound; holding the key: one; mashing for 2 s: one sound per swing, and no swing starts during another |
| Pickup | SFX-PICKUP | one sound; crossing the place again: no more |

In the game's own mix (step 3, recorded with Godot's movie maker and measured by `design/tools/plot_mix.py`; `evidence/3/3-mix.png`): each of seven sounds in a scripted run starts on its event's frame and plays within 0.01 dB of its file.

By ear, in my playtest with sound on, mashing and holding the jump and slash keys among the rest: "我已经试玩过了，开声音时音效都清晰的，bgm也没问题；静音时也没发现问题" [I have played it. With sound on, the sound effects were all clear, and the BGM was fine too; muted, I found no problems either].

## 5. Music

- **The seam:** MUS-LOOP is 24 bars cut at bar lines, with the beat after the end crossfaded into the first beat (`design/tools/prepare_music.py`; ASSET-LOG.md). Of the previews, three repetitions and the seam with 10 s on each side, I said: "I can't hear the seam" (2026-10-04). Godot imports it with Loop on; a check confirms the loop flag and its length, 54.867 s. In my playtest, over at least three repetitions in the game (about three minutes): "the BGM was fine too".
- **Pause and end, as predicted** (CHANGE-BRIEF.md, music behavior, and its revision for step 3). Checked headless, and measured in the recorded mix, where the music's gain matched what the game asked for to 0.01 dB:

| Moment | Predicted | Checked | Measured in the mix |
|---|---|---|---|
| Title | starts under the title, plays on into play | starts once; Enter does not start it again | — |
| Hit | dips 6 dB for about 0.6 s | −6 dB, back at full level 0.72 s after the hit, with the 0.15 s ramp | −6.00 dB |
| Pause | drops 12 dB, keeps its place | −12 dB while paused; the sound effects pause | −12.00 dB |
| Death and respawn | dips 9 dB, never restarts | −9 dB through the fade and the respawn, for a fall and for a start-over; not restarted | −9.00 dB |
| Teleport circle | fades out over about 1.5 s | stopped after 1.52 s | the fade, then digital silence |
| End card | silent | not playing | digital silence |

## 6. Muted play

- **Muting changes nothing in play:** with both buses muted, the scripted route from the opening to the teleport circle takes the same 733 ticks, ends at the same x to 0.001 px, and makes the same sound calls as unmuted (a check).
- **Each sound has a visual twin** (predicted failure 6):

| Sound | What shows without it |
|---|---|
| SFX-JUMP | he leaves the ground in CHAR-RISE |
| SFX-STOMP | the goblin's squashed frame, then it vanishes; he bounces up |
| SFX-HURT | CHAR-HURT, the knockback, the flash, the camera shake, and a heart emptying or the gear flying off |
| SFX-PORTAL | the column of light, CHAR-CELEBRATE, the camera pulling back |
| SFX-SLASH | CHAR-SWORD-SLASH with its trail; a goblin in reach is squashed |
| SFX-PICKUP | the pickup vanishes and he is in the sword form |
| (no sound) waystone | it lights, with a ring of light and a pulsing halo |

In my playtest, muted: "I found no problems either".

## 7. Automated check

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path game --fixed-fps 60 res://tests/checks.tscn
```

Result on 2026-10-04: `all checks passed`, 141 `PASS` lines, exit code 0. Each check prints one line; the script exits with code 1 if any fails. What they cover, by build step, is at the top of `game/tests/checks.gd`. The sound checks are the ones listed under [Sound events](#4-sound-events). The headless audio driver never mixes, so the checks read what the players were told to do; the end of the output reports the audio streams still registered with the audio server as leaked, which is that driver, not the game.

Where a rule changed, its checks changed with it, and FRICTIONAL.md records it: for example the jump in place after the step 2a playtest, and in step 3 the fall's sound (fall → hurt) and the waystone's (checkpoint → none), after the 2026-10-02 decision to keep six sounds. Several checks were shown to fail on purpose: the cliff window with the old jump (step 1b), the frame check with CHAR-RUN-B pointed at CHAR-RUN-A's frame (step 2a), the jump-sound checks with the sound moved to the key press (step 3), and the asset check with a file moved away (step 5).

## Predicted failures, and what happened

From CHANGE-BRIEF.md, "Predicted failure cases and how they will be checked":

1. **Generated poses drift from the reference.** It happened, in part. The overlays at game size (`generated/checks/`, `design/tools/check_against_sheet.py`) found HURT-01 leaning toward the hit instead of recoiling, and RUN-B-01 not a passing pose, so both were redone; CHAR-RISE and CHAR-SWORD-RISE about 12% too large against CHAR-IDLE's face, corrected by hand to ×0.88; and the reference at about 3.4 heads instead of 2.5, which I kept (CHARACTER-SHEET.md, revision 2).
2. **Rudy disappears against the wheat.** The fills do blend, as predicted: his hair against the generated wheat is 1.71. The outer outline carries him at 11.13, and in colour and in grayscale he reads in both forms over the wheat and the sky (`evidence/2b/2b-readability.png`). No change was needed.
3. **A sound fires twice on one event.** Not found: see [Sound events](#4-sound-events).
4. **The music loop clicks or leaves a gap.** Not heard: not in the previews, and in my playtest, over at least three repetitions, "the BGM was fine too". The loop was moved to 24 bars because the song repeats every 24, and its end 5.1 ms off the beat grid, where the waveform best matches the start.
5. **Art and collision disagree.** Checked in collision screenshots in `evidence/2a/` to `evidence/5/`, and by checks: the ground art's walk line and all four cliff faces are within 1 px of the collision; the goblin's 40 × 118 px box and the spikes' box fit their art; Rudy's capsule as in [Character against the sheet](#2-character-against-the-sheet). The poses outside the capsule are in states where he cannot be hit.
6. **The slice is unreadable with sound muted.** Not found: every sound has a visual twin ([Muted play](#6-muted-play)), and muted "I found no problems either".

## Inspect and revise

Each of these began with something I saw, heard or measured, and changed an asset, a prompt, a loop point or the game. The details are in FRICTIONAL.md, under the headings named.

| Observation | Revision | Record |
|---|---|---|
| CHAR-REF-02 covered in ornate patterns, CHAR-REF-03 too plain | a prompt asking for edge trim only, matched in every view; CHAR-REF-07 accepted | "Rudy's reference, round 2: accepted"; `f9f3d07` |
| HURT-01 leans toward the hit; RUN-B-01 is not a passing pose | both redone with new edit prompts; HURT-02 and RUN-B-02 accepted | "HURT and RUN-B redone"; `7e74814` |
| The rising frames 12% too large when overlaid on the idle face | scale ×0.88 by hand in `matte_sprites.py` | "Rudy's game frames: matting, scale and placement"; `e019959` |
| My step 1a playtest: the run too slow, the jump slow, turning not crisp | faster run and jump, turning on the spot | "Step 1a playtests"; `2608528` |
| My step 1b playtest: the cliffs too tight | a higher jump; a check measuring the takeoff window | "Step 1b playtest"; `46ba347` |
| My step 1c playtest: a fall should cost a heart | the fall rules, and their checks | "Step 1c playtests"; `ebfdab3` |
| My step 2a playtest: the run frames keep the same leg behind | a run redo prompt; ChatGPT's three outputs rejected; both frames kept | "The run redo is dropped"; `4d3bad1` |
| My step 2b playtest: the spikes do not stand out | the generated spikes brought forward, with the outline, moved between the wheat tufts | "Step 2b playtest: the spikes stand out"; `f8c4ae0` |
| My step 2c playtest: the pickup small, the save not shown, the light too pale | a larger pickup, the waystone's halo and ring, a deep-gold column of light | "Step 2c playtest"; `22d8086` |
| The generated song repeats every 24 bars, not 16 or 32 | a 24-bar loop, its end moved 5.1 ms to match the waveform | "The music loop"; `af98d88` |

## My playtests

- **Earlier, during the build:** steps 1a, 1b, 1c, 2a, 2b, 2c and 2d, each on my Mac; what I found is in FRICTIONAL.md and the table above.
- **The finished slice, sound on, then muted:** on 2026-10-04, on my Mac, at `10c0c2e`. "我已经试玩过了，开声音时音效都清晰的，bgm也没问题；静音时也没发现问题" [I have played it. With sound on, the sound effects were all clear, and the BGM was fine too; muted, I found no problems either].
- **Asked by Claude afterwards:** whether I had heard at least three repetitions of the loop in the game, and mashed and held the jump and slash keys. My answer: I did both.
- **What changed after it:** the debug line is hidden at the start (F1 shows it). Claude suggested it; the decision is mine, and I gave no further reason.

No one else has played or listened to the slice.

## Known limitations

- **One level**, about 30 seconds at full speed (12.2 s on the checks' straight route).
- **The mushroom is cut:** the mushroom monster, its spore, blocking with the shield, CHAR-SWORD-BLOCK in play, SFX-SPORE and SFX-BLOCK. Panel 4's failure comes from a goblin or the spikes instead.
- **Four planned sounds were not made:** SFX-FALL (a fall plays SFX-HURT), SFX-CHECKPOINT (the waystone lights silently), SFX-SPORE and SFX-BLOCK.
- **Art kept as it is:** the two run frames keep the same leg behind; CHAR-HURT is thrown almost flat; Rudy is about 3.4 heads, not the sheet's 2.5.
- **The mix** was set from measured loudness and not changed after my playtest, which found the sounds clear and the music fine; no one else has listened to it.
- **The debug line** (F1) does not update while the game is paused.
- **Mute has no on-screen cue:** M and N mute the music and the sound effects, but only the debug line (hidden by default) shows it, and no in-game text names the keys; README.md does. Adding one would change `game/` after the film's source revision, so it is left for later.
- **Tested only on macOS** (15.1, Apple M3); no Windows or Linux run.
- **The checks cannot hear:** headless, they check what the audio players were told to do; what is heard was measured once, in the movie-maker recording of step 3.
- **Terms:** ElevenLabs' and Suno's free plans allow only non-commercial use, Suno keeps the rights in the music, and anything published with the ElevenLabs sounds needs "elevenlabs.io" or "11.ai" in its title (SOURCES.md).
