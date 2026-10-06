# Module 12 — Audio and Triggers

CSYE 7270 · Fall 2026 · Week 12

## Executive summary

Game audio is two systems that must agree: a trigger system, where game logic decides that something happened, and a mix, made of players, buses, levels and a clock that runs on its own thread. This module takes both apart in Godot 4.7.2 and separates what a terminal can test from what only your ears can. You will direct Claude Code to add a generated click to the Walker rhythm game on every Perfect or Good hit, split the mix into Music and SFX buses, and write a headless test. On 27 September 2026 that exercise produced an agent that printed two PASS lines for checks it had not run, a test that failed one run in ten, and a finding about what headless Godot can actually observe. The final test passes 25 checks and proves routing, triggering, level at the bus, mute, restart and pause. It does not prove that anyone can hear the click or that it lands on the beat as heard. Those are HUMAN CHECKs, made with headphones.

## The question

A rhythm game needs a click on every good hit. The prompt is easy to write. The agent adds an `AudioStreamPlayer`, calls `play()` in the hit handler, and its test prints `PASS hitsound_plays_on_perfect`.

What has been proved? That a flag called `playing` was true at one instant. Not that the sound reached the bus you meant at the level you meant, not that a Miss stays silent, not that the click behaves on pause and restart, and certainly not that a player hears it in time with the music.

The record forced a sharper question: when your test runs where no one can hear, what can it observe about sound? Guess wrong one way and you ship untested audio behind PASS lines. Guess wrong the other way and you skip checks that would have run.

## The ideas

### Three player nodes, one question: where is the listener?

`AudioStreamPlayer` is the non-positional player, for music and interface sounds. [`AudioStreamPlayer2D`](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer2d.html) attenuates with distance to the listener (the screen centre, or an `AudioListener2D`), and its `max_distance` defaults to 2000. [`AudioStreamPlayer3D`](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer3d.html) attenuates and pans relative to the current camera or an `AudioListener3D`; its `max_distance` defaults to 0, meaning no cut-off. Choose by asking where the listener is. The rhythm game's song and metronome are plain players because a rhythm game's clock must not depend on where anything is. The 3D platformer's enemies use `AudioStreamPlayer3D` with `max_distance = 30` on the walk loop: a robot you cannot see should be one you cannot hear.

### Import: a file is not a sound until the importer says so

Godot imports WAV, Ogg Vorbis and MP3 ([importing audio samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html)): WAV for short, repetitive effects, Ogg for music. Settings live in a text file beside the asset, `hit_click.wav.import`, so an agent can read, diff and change them without you noticing. Three consequences:

- **A WAV is not stored uncompressed by default.** Import compression defaults to Quite OK Audio; the rhythm game's metronome has `compress/mode=2`. What plays is what the import mode decodes.
- **Looping is an import setting.** The song imports with `loop=false`. Flip it and "song finished" never arrives.
- **The BPM in an Ogg import drives nothing.** The docs call it "currently unused". The song imports with `bpm=116.0`, but the game keeps its tempo in `Conductor.bpm`. When an agent "sets the BPM", ask which one.

**Sources.** The old course's Audio page pointed to Freesound for sounds and Audacity for editing, and its Mini-Assignment 3 asked for music tracks, effects and an ambient loop, sorted into categories, with the AI tools used and each asset's intended use documented. Three things still hold: sort sounds by role, because the roles become buses; document every asset's source and intended use; treat a loop as a file with real loop settings. Freesound's FAQ says uploaders choose among Creative Commons licences (CC0, Attribution, Attribution NonCommercial), so the licence belongs to the sound: copy it into `SOURCES.md`. Module 2 covers generating audio; this week's syllabus note is "Disclose sources; verify actual playback."

### Buses: where levels live, and two instruments

Every player has a `bus`, default `Master`. A bus applies its effects in order and sends its output to another bus, ending at Master ([audio buses](https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html)). Levels are decibels. The layout is a resource saved as `res://default_bus_layout.tres`, which a project loads by default; a project without it has one bus, Master, the rhythm game's starting point. Music and effects on separate buses can be balanced, ducked or muted independently.

A bus is also a measurement point, and Godot offers two instruments. `AudioServer.get_bus_peak_volume_left_db` reads the bus **meter**. An `AudioEffectCapture` added to the bus "copies all audio frames" into a ring buffer and does not alter the audio ([AudioEffectCapture](https://docs.godotengine.org/en/stable/classes/class_audioeffectcapture.html)). They see different things, as the last idea explains.

### One player's lifecycle, and the triggers that drive it

An `AudioStreamPlayer` plays one voice by default: `max_polyphony` is 1, and calling `play()` past that limit "will cut off the oldest sounds" ([AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html)). Fast hits on one voice sound like one hit that keeps restarting; raise the limit and the tails overlap. `play()` starts from the beginning, so a restart that calls it restarts the music: a design decision, not a default. When the tree pauses, audio nodes pause their streams, following `process_mode` ([pausing games](https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html)), so a pause-menu sound needs a player whose `process_mode` keeps running. Reloading a scene frees every player and creates new ones; nothing carries over unless it lives in an autoload.

The audio system never decides when to play. Game logic does, usually through a signal: `Area2D.body_entered`, `Timer.timeout`, a button's `pressed`, or a game-defined signal like the rhythm game's `note_hit(beat, hit_type, hit_error)`. The audio questions never change: which event, which player, which bus, and what if the event fires twice, during a pause, or just before a restart?

### Audio time is not frame time

The audio thread mixes in blocks, so `get_playback_position()` increments in chunks ([sync with audio](https://docs.godotengine.org/en/stable/tutorials/audio/sync_with_audio.html)). The documented correction adds `AudioServer.get_time_since_last_mix()` and subtracts `AudioServer.get_output_latency()`, the delay before a mixed sample is heard. The rhythm game's `Conductor` caches that latency once, since the docs warn the call can be expensive, and filters the difference between the system and audio clocks. The metronome shows the limit: its own comment says each tick "is rounded to the next mix window (~11ms at the default 44100 Hz mix rate)". Godot 4.7.2 starts sounds at mix boundaries and has no sample-accurate "play at time t". Unity and Unreal do, as the comparison below notes.

### What a headless run can hear

`--headless` selects the **Dummy** audio driver, which the project-settings reference describes as disabling "all audio playback and recording". The instructor probed what that leaves before any agent ran. The short answer: Dummy means no device, not no mixing.

| What | Observed headless |
|---|---|
| `playing`, `finished`, playback position | They work; `get_output_latency()` returns 0.0 |
| Bus meter on a held 0.5-amplitude tone | −6.02 dB; with the bus at −12 dB, −18.02 dB; muted, −200 dB |
| Bus meter on a 60 ms click | **−200 dB on every frame** |
| `AudioEffectCapture` on the same click | Recorded 58 ms of it, peak 0.4993 (−6.03 dBFS) |
| Capture on SFX and on Master, SFX muted | SFX capture still −6.03 dBFS; Master capture silent |

The engine source explains the last rows. The Dummy driver ([source at 4.7.2](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/audio/audio_driver_dummy.cpp)) mixes 4,096 frames in one burst, then sleeps about 93 ms. Each burst runs eight 512-frame mix steps back to back, and the meter holds the peak of the **last** step only. A 60 ms click that ends before the last step is mixed and never metered; a capture records every step. Three consequences follow. A short sound can start and finish between two frames, so `playing` can be false one frame after `play()`. A capture on a bus hears the audio before that bus's volume and mute, so test a mute by capturing on the bus it sends to. And the Dummy clock is not wall time. What stays unobservable: any speaker, any real device's latency, whether the mix is balanced, and whether it sounds good.

## The Walker example: walker-audio-rhythm-game

[`walker-audio-rhythm-game`](https://github.com/nikbearbrown/walker-audio-rhythm-game) is a public Walker adaptation of Godot's `audio/rhythm_game` demo (commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, MIT, kept by the Walker copy). Space hits the nearest note; the game judges Perfect (±50 ms), Good (±150 ms) or Miss; R restarts; P or Escape pauses. `scenes/main/main.tscn` owns a `Conductor`, a song `AudioStreamPlayer` named `Player` at `volume_db = -12`, a `Notes` manager emitting `note_hit`, and a `Metronome` player, off by default. The song's Vorbis tags identify "The Second Comeback" (Juan Linietsky, 2019); the metronome sample is by Ludwig Peter Müller (CC0). The Walker `SOURCES.md` notes that metadata identifies authorship, "not a separate license grant".

**What its log established.** A 180-frame headless run exits 0 with four leaked Ogg playback objects; stopping the conductor and waiting 0.2 s before freeing the scene removed them. `test_live_hit.gd` sends a real Space event when the first chart note is within 15 ms of its target, and the label reads `Perfect: 1`; `test_live_restart.gd` then sends R, and the reloaded scene's Perfect count is 0. Under the Dummy driver the audio clock advanced 4.60 s in 5.00 s of wall time, against 5.005 s in 5.006 s in a windowed CoreAudio run, so the log concludes the headless route "must not be used as time-faithful footage without more verification". **What remains unverified:** everything a player hears, and the song's licence for any public film.

Six sibling builds adapt the other `audio/` demos, each with a log that states its own limits. In [`walker-audio-audio-effects`](https://github.com/nikbearbrown/walker-audio-audio-effects), 18 of 18 effect toggles restore state, yet a flat EQ "does not demonstrate a deliberate tonal adjustment". In [`walker-audio-midi-piano`](https://github.com/nikbearbrown/walker-audio-midi-piano), a MIDI note-on with velocity zero means note-off, a detail an agent gets plausibly wrong; its log reproduced three failures, fixed them, and kept the failing log.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Answer in writing before you delegate anything.

1. `note_hit` fires for five hit types. Which should make a sound, and what happens to a player's trust if a Miss clicks too?
2. Three hits land 40 ms apart. With `max_polyphony = 1` on a 60 ms click, what does the player hear? With 4?
3. You press P halfway through a click, and later R. What should the click and the song do in each case, and what does Godot do by default?
4. A headless test says `HitSound.playing == true`. What has that proved about the sound, and what has it not?

### 2. Build It

Start from the upstream demo, as the chapter's reproduction does; the recorded run itself started from the Walker build's `godot/` folder. The public Walker repository holds the same project and is the quicker start; then check that `godot/test_live_restart.gd` is present.

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Copy `audio/rhythm_game` into a new folder as `godot/`, apply [`walker-adaptation.diff`](../../examples/12-audio-and-triggers/walker-adaptation.diff) (the title and an empty-list guard), copy in [`test_live_restart.gd`](../../examples/12-audio-and-triggers/tests/test_live_restart.gd), and commit. Then import and record the baseline:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://test_live_restart.gd
```

Expect `LIVE_SPACE_PERFECT true` and `LIVE_RESTART_RESET true` after about ten seconds: the test waits in real time for the first chart note. Do not add `--fixed-fps` to audio tests: the audio thread runs in real time, so a test that waits for sound must wait on the wall clock. Keep `timeout` (on macOS it comes from Homebrew's `coreutils`; see [Chapter 0](../../chapters/00-the-toolchain.md)): a script that errors before `quit()` never exits, and the record lost 19 minutes to one.

The prompt below fixes what must not change (timing), specifies the generated asset exactly, names the trigger rule, and asks for tests of level, restart and pause, not just "it plays". It also contains a mistake, the prompt author's rather than the agent's: one requirement asks an instrument to see something it cannot. Find it, and write down why, before you send the prompt as it was run.

```text
You are working in a copy of walker-audio-rhythm-game, a Godot 4.7.2 GDScript rhythm game in godot/. Inspect before editing: read godot/project.godot, godot/scenes/main/main.tscn, godot/scenes/main/main.gd, godot/scenes/main/pause_handler.gd, godot/game_state/conductor.gd, godot/game_state/metronome.gd, godot/game_state/note_manager.gd and godot/test_live_restart.gd.

Goal: a short click confirms every Perfect or Good hit, and the mix is split into Music and SFX buses. Timing must not change.

Requirements
1. Generate the click yourself; do not download audio or call any paid service. Write tools/make_click.py (Python 3 standard library only) that writes godot/sfx/hit_click.wav: mono, 16-bit PCM, 44100 Hz, 60 ms, a 1500 Hz sine with an exponential decay, peak at -6 dBFS. Run it. Add a SOURCES.md entry saying the file is generated by that script and contains no third-party material.
2. Create godot/default_bus_layout.tres with buses Master, Music and SFX; Music and SFX send to Master. Route the song player (the AudioStreamPlayer named Player) to Music, and the Metronome and a new HitSound player to SFX.
3. Add an AudioStreamPlayer named HitSound to main.tscn using hit_click.wav, with max_polyphony 4. Play it from the existing note_hit handler in main.gd for PERFECT, GOOD_EARLY and GOOD_LATE only; never for MISS_EARLY or MISS_LATE.
4. Do not edit conductor.gd, note_manager.gd, metronome.gd, the charts, the hit windows or the song's import settings.
5. Add godot/tests/test_hit_audio.gd (extends SceneTree), runnable with
   godot --headless --path godot --script res://tests/test_hit_audio.gd
   It loads the real main scene and asserts: the three buses exist and Music and SFX send to Master; Player is on Music, Metronome and HitSound on SFX; emitting the Notes node's real note_hit signal with PERFECT or GOOD starts HitSound and with MISS does not; within 0.1 s of a Perfect the SFX bus peak (AudioServer.get_bus_peak_volume_left_db) rises above -40 dB, and with the SFX bus muted it stays at the floor; a real Space key press on the first chart note scores a hit and starts HitSound (reuse the approach in test_live_restart.gd); pressing R reloads the scene with HitSound silent and the song position under 1 s; pressing P pauses the tree and HitSound does not advance while paused. Stop the players and wait 0.2 s before freeing the scene (FRICTIONAL.md explains the Ogg teardown warning). Print one PASS or FAIL line per check and quit(1) on any failure.
6. Run the new test and godot/test_live_restart.gd headlessly and paste their real output. Headless Godot uses the Dummy audio driver: say what the test can and cannot establish about what a player hears.
```

Save it as `prompt1.txt` and run it from the repository root with Claude Code:

```bash
claude -p "$(cat prompt1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(python3:*)" --disallowedTools "Skill" --max-turns 60 --output-format stream-json --verbose > session1.jsonl
```

`Bash(python3:*)` is needed for the generator, and it is broad: it lets the agent run any Python. That is acceptable in a scratch copy, not in a repository with secrets. With Codex, the optional alternative:

```bash
codex exec -s workspace-write -C . "$(cat prompt1.txt)" < /dev/null
```

**Follow-up prompts from the record.** Send these only if your own checks show the same failures. First, if the agent printed PASS for a check it skipped (the record resumed the same Claude Code session; its `PROMPTS.md` has the command):

```text
Two of your checks print PASS without testing anything, and the reason you give is wrong. You wrote the SKIP before running the test once. In headless Godot 4.7.2 the Dummy driver does mix. In separate probes: a 0.5-amplitude sine held for 200 ms or longer read -6.02 dB on AudioServer.get_bus_peak_volume_left_db, and -200 dB with the bus muted. But that meter reports only the most recent mix block, and a 60 ms sound can be mixed without ever showing on it: an AudioEffectCapture on the same bus recorded about 58 ms of hit_click.wav, peak 0.4993, while the meter read -200 dB on every frame. A capture effect on a bus hears the audio before that bus's volume and mute; a capture on Master hears what the SFX bus actually sends.

Replace both SKIP branches with real checks that run headless. In the test only (do not save it into default_bus_layout.tres), add an AudioEffectCapture to the SFX bus and one to Master, keep the metronome off, and mute the Music bus while measuring so Master carries only SFX. Wait in real time (wall clock), not in frames. Assert: after a PERFECT note_hit, the SFX capture peaks above -12 dBFS and the Master capture above -12 dBFS; with the SFX bus muted, the SFX capture still hears the click but the Master capture stays below -60 dBFS. A check that cannot run must print SKIP, never PASS, and must not count as a pass. Remove the effects and restore the bus state afterwards.

Change nothing outside godot/tests/test_hit_audio.gd. Correct the headless note in that file to say what the Dummy driver actually allows. Run the test three times and godot/test_live_restart.gd once, in real time, and paste the real output.
```

Second, if a trigger check fails one run in ten or the pause check can pass without testing anything (in the record, Claude Code's usage limit ended the session here and Codex took over, given only the facts it needed):

```text
Work in this Godot 4.7.2 project. Edit only godot/tests/test_hit_audio.gd. A previous agent (Claude Code) was part-way through fixing it when its usage limit ended the session.

Facts from the Godot 4.7.2 source and from probes on this machine:
- The Dummy audio driver (servers/audio/audio_driver_dummy.h/.cpp) mixes buffer_frames = 4096 frames in one burst, then sleeps 4096/44100 s (about 93 ms). Each burst runs eight 512-frame AudioServer mix steps back to back.
- AudioServer.get_bus_peak_volume_left_db reports only the last 512-frame step of the latest burst, so a 60 ms click can be fully mixed without ever showing on the meter.
- A 60 ms sound can therefore start and finish inside one burst between two frames: HitSound.playing can already be false one frame after play(). One run of this test failed hitsound_plays_on_perfect for that reason.

Make three changes:
1. Trigger checks: read HitSound.playing immediately after each note_hit.emit(), before any await, and say why in a comment. Keep the MISS checks.
2. Pause check: hitsound_frozen_while_paused can pass without testing anything, because the click may already have ended. Test the pause on the song player instead (it is long): after P, its playback position must not advance by more than 0.02 s over 0.3 s of wall-clock time, and it must advance again after a second P. Name the checks for what they test.
3. Correct the headless note at the end of the file using only the facts above; delete the claims that the Dummy driver mixes 512-sample blocks at about 86 mixes per second and that 60 ms clips stay playing for hundreds of frames.

Then run it three times with: godot --headless --path godot --script res://tests/test_hit_audio.gd
and once: godot --headless --path godot --script res://test_live_restart.gd
Run them in real time (no --fixed-fps). Paste the real output. Do not weaken any other check.
```

### 3. Use It

Only you can do this part. Use headphones at a fixed system volume, and write down the date and device. Every item is a **HUMAN CHECK**.

1. Open the **Audio** panel at the bottom of the editor. Confirm the three buses, their sends and 0 dB faders. Watch the meters while the game runs: Music should move, SFX should flick on hits. A real audio driver feeds the meter continuously, unlike Dummy's bursts.
2. Play the first chart. Does the click confirm a Perfect without masking the music? Is it too loud at 0 dB against a song set to −12 dB? Does a Good sound identical to a Perfect, and should it?
3. Tap Space wildly through a dense passage. With `max_polyphony = 4` the clicks overlap. Is that feedback or noise?
4. Press P mid-click, wait, press P again. Press R right after a hit. Listen for a click that survives a restart or reappears after a pause.
5. Toggle "Use filtered" and listen for any change in how the click lines up with the beat. There should be none: the judgment triggers the click, not the clock.

### 4. Ship It

Commit in order: baseline; generator and WAV; bus layout and routing; `HitSound` and trigger; test. The WAV is 5,336 bytes, so it belongs in Git; MP3 and MP4 files and anything over 25 MB go to the course's designated media storage. Run `git status` before committing audio: the public rhythm-game repository ignores `*.wav` except under `godot/`, and [Chapter 2](../../chapters/02-prompting-game-art.md) records a starter whose `.gitignore` hid an audio folder.

In `SOURCES.md`, state that the click is generated by `tools/make_click.py` with no third-party material, that the song and metronome keep their upstream attributions, and what is unresolved: the song's licence for public distribution. In `FRICTIONAL.md`, record what the agent believed about headless audio, what your probe showed, and what you heard. The Brutalist skill that fits is `godot-gamedev`, showing the routing and the trigger, each excerpt followed by the capture or meter result it produces. A `godot-walkthrough` of the click needs real recorded device audio; a headless log is not audio.

### 5. Verify

```bash
timeout 120 godot --headless --path godot --script res://tests/test_hit_audio.gd
```

```bash
timeout 120 godot --headless --path godot --script res://test_live_restart.gd
```

Then run the instructor's independent probe, [`verify_levels.gd`](../../examples/12-audio-and-triggers/verification/verify_levels.gd). Read it, copy it into `godot/tests/`, and run it. It adds capture effects at runtime, mutes Music so Master carries only SFX, fires the real `note_hit` signal, and prints what each bus carried:

```bash
timeout 60 godot --headless --path godot --script res://tests/verify_levels.gd
```

Run the test more than once: a test that passes nine times in ten is a test that fails. In the record, ten runs of the final test passed 25 of 25 each, and the probe measured the click at −6.12 dBFS on both the SFX bus and Master, matching the WAV's own peak.

| Question | Headless check (a pass establishes this) | HUMAN CHECK (a pass does not) |
|---|---|---|
| Which events click? | Perfect and Good start `HitSound`; Miss does not | Whether the click reads as confirmation |
| Which bus, what level? | Routing graph; capture peak equals the WAV's peak | Whether it is balanced against the song |
| Does mute work? | Master capture silent with SFX muted | Whether it sounds right |
| Restart and pause? | R reloads to silence; P freezes the song and a second P resumes it | A click surviving a restart in your ears |
| Timing? | Constructed hit-timing cases in the Walker log | Whether it lands on the beat as heard; device latency |

A passing run says nothing in the right-hand column. Nobody can hear the click from a terminal.

## What the agents got wrong

In the recorded run, Claude Code 2.1.150 (default model `claude-sonnet-4-6`) and then Codex CLI 0.153.4 left four mistakes worth studying.

**Two PASS lines for checks that never ran.** Before the test had run once, the agent wrote `PASS peak_sfx_rises_after_perfect (SKIP: Dummy driver ...)` on the belief that headless Godot cannot meter audio. A SKIP that prints PASS is a false pass, and the belief was untested: a held tone does meter headless. The instructor's independent probe caught it, reading the SFX meter at −200 dB after real hits while music on Master read −33 dB.

**A prompt that asked an instrument to see what it cannot.** That probe also showed the instructor's premise was incomplete: the meter misses a 60 ms click because it holds only the last mix step of each 93 ms burst. Requirement 5 asked the meter to rise within 0.1 s of a Perfect. The mistake was the prompt author's; the right instrument is a capture effect.

**A hand-written import file and invented IDs.** The generator also wrote the `.import` file itself, with an invented UID, `compress/mode=0` (nobody asked for it) and a file name computed from the WAV's MD5, and the agent put a hand-typed `unique_id=1234560001` into the scene. Godot kept the UID, rewrote the file name, and warned about an invalid UID until it had. This is the dangerous middle: read everything the agent generated, not only what you requested.

**A flaky trigger check and a pause check that could not fail.** `hitsound_plays_on_perfect` failed once in ten runs because a 60 ms click can start and finish inside one burst between two frames, and the pause check could pass because the click had already ended. Codex read `playing` immediately after `emit()` and moved the pause test to the long song player. One check, `space_hit_starts_hitsound`, still reads `playing` two frames after a key press and was not changed.

## If you know Unity or Unreal

Unity and Unreal were not run for this module; the comparisons come from their official documentation, checked on 27 September 2026.

| Godot 4.7.2 | Unity 6.6 | Unreal Engine 5.8 |
|---|---|---|
| `AudioStreamPlayer` / `2D` / `3D` | `AudioSource` + Spatial Blend | Audio Component; Play Sound 2D or at Location |
| Audio bus | Audio Mixer group | Submix (routing, effects); Sound Class (grouping) |
| `max_polyphony` above 1 | `PlayOneShot` | Sound Concurrency asset |
| Starts on the next mix block | `PlayScheduled` on `AudioSettings.dspTime` | Quartz clock; MetaSounds |
| `.import` sidecar (text) | `.meta` import settings (YAML) | Sound Wave `.uasset` (binary) |
| `default_bus_layout.tres` (text) | Audio Mixer asset, referenced by GUID | Submix and Sound Class `.uasset` (binary) |

Both engines offer sample-accurate scheduling that Godot 4.7.2 lacks, so a metronome there can be scheduled ahead on the audio clock instead of being rounded to a mix block. For an agent workflow the difference is readability: in Godot the whole change (bus layout, routing, player, trigger, generator and test) is text, and every mistake in the record was found by reading it. Unity references are GUIDs, and Unreal's routing is binary. Whether either engine's mixer can be captured in batch mode was not checked. See [Chapter 12](../../chapters/12-audio-and-triggers.md) for the full comparison.

## Practice assessment (ungraded)

Answer in your own words, then check the source. The Canvas practice quiz for this module covers related ground in multiple choice. Do not paste Claude's explanation as proof of your understanding; ask it to question you, then check the source yourself.

1. Explain, with the numbers, why a 200 ms tone shows on the bus meter headless while a 60 ms click usually does not.
2. Why does a capture on the SFX bus still hear the click when SFX is muted? Where would you put a capture to test the mute?
3. Where would you put a UI click that must keep playing while the game is paused, and which property makes it work?
4. Set `HitSound.max_polyphony` to 1 and describe a capture-based check that detects the difference when three `note_hit` signals arrive 20 ms apart.

## The next step

This module opens Assignment 9, "Sound That Provably Plays, and a Frame You Can Afford." It finishes with Module 13, profiling and optimization, and is due about Day 90 (Canvas dates govern); its page sets the exact task and the required `godot-gamedev` film. This lesson adds no graded deliverable. The long reading is the companion chapter, [Chapter 12 — Audio and Triggers](../../chapters/12-audio-and-triggers.md).
