# Chapter 12 — Audio and Triggers

## Executive summary

Game audio is two systems that must agree: a **trigger** system (game logic deciding that something happened) and a **mix** (players, buses, levels and a clock that runs on its own thread). This chapter takes both apart in Godot 4.7.2 — the three stream-player nodes, import settings for WAV, Ogg and MP3, buses and effects, polyphony, what restart and pause do to a sound, and why audio time is not frame time. You will direct an agent to add a generated click to the Walker rhythm game on every Perfect or Good hit, split the mix into Music and SFX buses, and write a headless test. The record of doing that on 27 September 2026 includes an agent that turned two checks into PASS lines without running them, on the false belief that headless Godot cannot meter audio; an investigation that found what the headless Dummy driver really does (it mixes in 93 ms bursts, which is why a bus meter misses a 60 ms click while a capture effect records it); a test that failed one run in ten for the same reason; and a hand-off from Claude Code to Codex when Claude's usage limit ended the session. The final test passes 25 checks. It proves routing, triggering, level at the bus, mute, restart and pause. It does not prove anyone can hear the click, or that it lands on the beat as heard. Those are yours to check, with headphones, and the chapter says how.

## The question

A rhythm game needs a click on every good hit. The prompt is easy to write. The agent adds an `AudioStreamPlayer`, calls `play()` in the hit handler, and its test prints `PASS hitsound_plays_on_perfect`.

What has been proved? That a flag called `playing` was true at one instant. Not that the sound was routed to the bus you meant, at the level you meant; not that a Miss stays silent; not that the click survives a pause correctly or vanishes on restart; and certainly not that a player hears it in time with the music.

And a sharper version of the question, which this chapter's record forced: **when your test runs where no one can hear, what can it actually observe about sound?** Guess wrong in one direction and you ship untested audio behind PASS lines. Guess wrong in the other and you skip checks that would have run.

## Ideas you need

### Three player nodes, one question: where is the listener?

Godot plays sound through **stream player** nodes. Each takes an `AudioStream` resource (the sound data) and sends its output to an audio bus.

| Node | Use | How position enters |
|---|---|---|
| `AudioStreamPlayer` | music, interface sounds — "the standard, non-positional stream player" | it does not |
| `AudioStreamPlayer2D` | sounds with a place on a 2D screen | "attenuated with distance to the listener"; by default the listener is the screen centre, or an `AudioListener2D`; `max_distance` defaults to 2000 |
| `AudioStreamPlayer3D` | sounds in a 3D world | attenuated and panned relative to the current camera or an `AudioListener3D`; four attenuation models; `max_distance` defaults to 0 (no cut-off) and, when set, "always works in a linear fashion" |

Sources: [AudioStreamPlayer2D](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer2d.html), [AudioStreamPlayer3D](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer3d.html), [audio streams tutorial](https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html) (the tutorial carries a banner saying it is not yet updated for 4.7; the class references are current).

Choose by asking where the listener is. The rhythm game's song and metronome are plain `AudioStreamPlayer`s because a rhythm game's clock must not depend on where anything is. The 3D Platformer's enemies use `AudioStreamPlayer3D` for their walk loop, hit and explosion, with `max_distance = 30` on the walk loop and Doppler tracking on (`walker-3d-platformer/godot/enemy/enemy.tscn`): a robot you cannot see should be one you cannot hear.

### Import: a file is not a sound until the importer says so

Godot imports "WAV, Ogg Vorbis and MP3" ([importing audio samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html)). Import settings live in a text file beside the asset (`hit_click.wav.import`), so an agent can read and diff them — and can change them without you noticing.

| | WAV | Ogg Vorbis | MP3 |
|---|---|---|---|
| Documented use | "short and repetitive sound effects" | "music" | where CPU is limited (mobile, web) |
| Compression on import | PCM, IMA ADPCM, or **Quite OK Audio (the default)** | always compressed | always compressed |
| Looping | Loop Mode (Detect from WAV, Disabled, Forward, Ping-Pong, Backward), Loop Begin/End in samples | Loop on/off, Loop Offset in seconds | same as Ogg |
| BPM / Beat Count / Bar Beats | — | present, but the docs call them "currently unused" | same |

Three consequences to check in any agent's work:

- **A WAV is not stored uncompressed by default.** Its import compression defaults to QOA. The rhythm game's metronome WAV has `compress/mode=2` in its `.import` file. If you generate a precise tone, what plays is whatever the import mode decodes.
- **Looping is an import setting.** The rhythm game's song imports with `loop=false`. Flip it and the song never ends, so "song finished" never arrives.
- **The BPM in an Ogg import drives nothing.** The song imports with `bpm=116.0`; the game keeps its tempo in `Conductor.bpm`. When an agent "sets the BPM", ask which one.

### Buses: where levels live

Every player has a `bus` (default `"Master"`; an unknown name falls back to Master). A bus applies its effects "in order" and sends its output to another bus; "routing always passes audio from buses on the right to buses further to the left", ending at Master ([audio buses](https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html)). Levels are decibels; the docs note sound "is considered no longer audible between -60 dB and -80 dB". The layout is a resource saved to `res://default_bus_layout.tres`, which the project setting `audio/buses/default_bus_layout` loads by default ([ProjectSettings](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html)). A project without that file has one bus, Master — the rhythm game's starting point.

A mix is a set of decisions about relative level. Music and effects on separate buses can be balanced, ducked or muted independently, and exposed in a settings menu. A bus is also a **measurement point**, and there are two instruments, which turn out to see different things:

- `AudioServer.get_bus_peak_volume_left_db(bus_idx, channel)` — the bus **meter** ([AudioServer](https://docs.godotengine.org/en/stable/classes/class_audioserver.html)).
- An `AudioEffectCapture` added to the bus, which "copies all audio frames … into its internal ring buffer" and "does not alter the audio" ([AudioEffectCapture](https://docs.godotengine.org/en/stable/classes/class_audioeffectcapture.html)).

What each one actually reports is the subject of the last section of these ideas.

### Polyphony, restart and pause: the lifecycle of one player

An `AudioStreamPlayer` plays one voice by default. `max_polyphony` defaults to 1, and "calling play() after this value is reached will cut off the oldest sounds" ([AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html)). Fast hits on a single-voice player sound like one hit that keeps restarting; raise `max_polyphony` and the tails overlap.

- `play(from_position = 0.0)` starts from the beginning unless told otherwise. A restart that calls `play()` restarts the music; that is a design decision, not a default to ignore.
- `finished` is "emitted when a sound finishes playing without interruptions". It does not fire on `stop()`, and never for a looping stream.
- **Pause.** Stream players follow `process_mode`: when the tree pauses, "audio nodes will pause their current audio stream" ([pausing games](https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html)), and `stream_paused` changes automatically. A pause-menu sound needs a player whose `process_mode` keeps running.
- **Reloading a scene** (`get_tree().reload_current_scene()`, the rhythm game's R key) frees every player in the old scene and makes new ones. Nothing carries over unless it lives in an autoload.

### Triggers: signals decide when, not the audio system

The audio system never decides *when* to play. Game logic does, usually through a signal: `Area2D.body_entered` on a pickup, `Timer.timeout`, a button's `pressed`, or a game-defined signal like the rhythm game's `note_hit(beat, hit_type, hit_error)`. The audio questions are always the same: **which event, which player, which bus — and what if the event fires twice, fires during a pause, or fires just before a restart?** In Dodge the Creeps (Chapter 9), `game_over()` stops `$Music` and plays `$DeathSound`; `new_game()` calls `$Music.play()` again. Two functions, and the restart behavior is fully specified: the song always starts over.

### Audio time is not frame time

The rhythm game's `Conductor` (`game_state/conductor.gd`) is the best short lesson in why. The audio thread mixes in blocks, so `get_playback_position()` "will increment in chunks (every time the audio callback mixed a block of sound)" ([sync with audio](https://docs.godotengine.org/en/stable/tutorials/audio/sync_with_audio.html)). The documented correction adds `AudioServer.get_time_since_last_mix()` and subtracts `AudioServer.get_output_latency()`, the delay between mixing a sample and hearing it. The AudioServer reference warns that `get_output_latency()` "can be expensive" and should not be called every frame; the Conductor caches it once. It then computes a smooth time from the system clock and runs a One Euro filter on the difference between the two clocks, so notes move smoothly but stay locked to what the player hears.

The metronome shows the limit. Its own comment says each tick "is rounded to the next mix window (~11ms at the default 44100 Hz mix rate)" and links an open proposal for precise audio scheduling (`game_state/metronome.gd`). Godot 4.7.2 starts sounds at mix boundaries; it has no sample-accurate "play at time t". Unity and Unreal both do, as the end of this chapter shows.

### What a headless run can hear

Headless Godot selects the **Dummy** audio driver (`--headless` is `--display-driver headless --audio-driver Dummy` ([command line](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html))). The project-settings reference describes Dummy as disabling "all audio playback and recording". I probed what that leaves before any agent ran (`examples/12-audio-and-triggers/probes/`, Godot 4.7.2). The short answer: **Dummy means no device, not no mixing.**

| What | Observed headless |
|---|---|
| `playing`, `finished` | work; a 1.0 s generated tone emitted `finished` 0.97–0.98 s of wall time after `play()` |
| `get_playback_position()` | advances; an Ogg song reached 2.79–2.88 s after about 2.99 s of wall time |
| `AudioServer.get_output_latency()` | 0.0 |
| Pause the tree | `playing` false, `stream_paused` true; position stopped after one mix block; resumed on unpause |
| `max_polyphony = 1`, three `play()` calls | position reset to the start each time |
| `AudioStreamPlayer2D` | at screen centre −12.0 dB per channel; 250 px right, −19.9 dB left / −16.5 dB right; beyond `max_distance`, −200 dB |
| `AudioStreamPlayer3D` | 2 m ahead −6.6 dB; 29 m (max 30) −47.4 dB; 40 m −200 dB; to the right, louder on the right |
| Bus **meter** on a held tone | a 0.5-amplitude sine read −6.02 dB; with the bus at −12 dB, −18.02 dB; muted, −200 dB |
| Bus **meter** on a 60 ms click | **−200 dB on every frame** |
| `AudioEffectCapture` on the same click | recorded 58 ms of it, peak 0.4993 (−6.03 dBFS) |
| Capture on SFX vs on Master, SFX muted | SFX capture still −6.03 dBFS; Master capture silent |

The last three rows needed an explanation, and the engine source has it. The Dummy driver (`servers/audio/audio_driver_dummy.h`/`.cpp`) mixes `buffer_frames = 4096` frames in one burst, then sleeps 4096/44100 s — about 93 ms ([driver source at 4.7.2](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/audio/audio_driver_dummy.cpp)). Each burst runs eight of the AudioServer's 512-frame mix steps back to back (`buffer_size = 512` in [`audio_server.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/audio/audio_server.cpp)), and the meter holds the peak of the **last** step only. A 60 ms click that ends before the last step of its burst is mixed and never metered. A capture effect records every step. Three more consequences follow:

- **A short sound can start and finish between two frames.** `playing` can already be false one frame after `play()`. This caused a flaky test failure below.
- **A capture on a bus hears the audio before that bus's volume and mute** — the effects run first, then the fader, then the meter (same source). To test a mute, capture on the bus it sends to.
- **The Dummy clock is not wall-clock time.** It sleeps a fixed 93 ms after mixing 93 ms of audio, so its clock lags by the time each burst takes; the Walker rhythm-game log recorded the Dummy audio clock advancing 4.60 s in 5.00 s of wall time.

What stays unobservable: anything about a speaker, a real device's latency, whether the mix is balanced, and whether it sounds good.

## The Walker example: walker-audio-rhythm-game

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer), [`walker-audio-rhythm-game`](https://github.com/nikbearbrown/walker-audio-rhythm-game), [`walker-audio-audio-effects`](https://github.com/nikbearbrown/walker-audio-audio-effects), [`walker-audio-bpm-sync`](https://github.com/nikbearbrown/walker-audio-bpm-sync), [`walker-audio-device-changer`](https://github.com/nikbearbrown/walker-audio-device-changer), [`walker-audio-generator`](https://github.com/nikbearbrown/walker-audio-generator), [`walker-audio-mic-record`](https://github.com/nikbearbrown/walker-audio-mic-record), [`walker-audio-midi-piano`](https://github.com/nikbearbrown/walker-audio-midi-piano). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

Seven Walker builds adapt Godot's `audio/` demos, all copied from `godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` under the demos' MIT licence (Godot Engine contributors). Each is public at `github.com/nikbearbrown/<build name>`; you can also start from its upstream path. Together they map what can and cannot be verified about game audio without ears.

| Build (upstream path) | Teaches | What its log established | What it says remains unverified |
|---|---|---|---|
| `walker-audio-rhythm-game` (`audio/rhythm_game`) | audio-clock timing, hit windows, restart, pause | a live Space hit scored Perfect; R reset the score; P paused and resumed; constructed hit-timing cases 0 and ±50 ms Perfect, ±100 ms Good, −200 ms early miss | heard synchronization, device latency, full-chart play |
| `walker-audio-audio-effects` (`audio/audio_effects`) | bus effects | 18/18 effect toggles restore state; 7/7 sound buttons start their players; all 37 bands of three EQs are 0 dB | "actual processing sound"; a flat EQ "does not demonstrate a deliberate tonal adjustment" |
| `walker-audio-bpm-sync` (`audio/bpm_sync`) | system vs audio clock at 116 BPM | 16 checks; restart position under 0.2 s; Dummy wall/playback deltas recorded (e.g. 1.196 s wall, 1.115 s playback) | heard sync, latency compensation; music and font licences unresolved |
| `walker-audio-device-changer` (`audio/device_changer`) | output devices | 9 checks, with a harness that refuses to run unless the driver is Dummy | any physical device switch |
| `walker-audio-generator` (`audio/generator`) | `AudioStreamGenerator` synthesis | 15 checks (22,050 Hz, 440 Hz start, frequency and volume controls); an `AudioStreamGeneratorPlayback` leak on abrupt quit, clean with an orderly stop–drain–free | pitch at the device, underruns, latency |
| `walker-audio-mic-record` (`audio/mic_record`) | recording through a bus effect | 10 UI and state checks; a leak on abrupt quit, clean with 200 ms drains; the save handler ignores `save_to_wav`'s error result | any microphone capture, playback or WAV export |
| `walker-audio-midi-piano` (`audio/midi_piano`) | MIDI to pitched samples | 12/12 mouse checks; synthetic MIDI 7/7 after reproducing and fixing three failures (polyphonic pressure cleared the highlight; a zero-velocity note-on retriggered instead of releasing), then 13/13 at the key-range ends | physical MIDI, heard audio; an 8 s voice lifetime against an 8.011 s sample |

The MIDI fix is the course's method in miniature. MIDI's convention that a note-on with velocity zero means note-off is exactly the detail an agent gets plausibly wrong. The Walker log reproduced the failure with synthetic events, fixed it, and kept the failing log.

**The build this chapter works in.** In `walker-audio-rhythm-game`, notes scroll toward a guide; Space hits the nearest; the game judges Perfect (±50 ms), Good (±150 ms) or Miss and shows the running error; R restarts; P or Escape pauses. `scenes/main/main.tscn` owns a `Conductor`, a song `AudioStreamPlayer` named `Player` at `volume_db = -12`, a `Notes` manager emitting `note_hit`, and a `Metronome` player (off by default). The song's Vorbis tags identify "The Second Comeback" (Juan Linietsky, 2019); the metronome sample is by Ludwig Peter Müller (CC0, per the upstream README). The Walker `SOURCES.md` notes that metadata identifies authorship, "not a separate license grant".

**What its log established — including about its own clocks.** The Walker `FRICTIONAL.md` (13–14 September) records:

- Headless import exits 0, but a 180-frame run exits 0 *with* four leaked Ogg playback objects. Stopping the conductor and waiting 0.2 s before freeing the scene removed the warnings in four repeated runs — a teardown-order finding, not a gameplay one.
- `test_live_hit.gd` sends a real Space event when the first chart note is within 15 ms of its target; the label reads `Perfect: 1`. `test_live_restart.gd` then sends R, and the reloaded scene's Perfect count is 0.
- Under the headless Dummy driver the raw audio clock advanced **4.60 s in 5.00 s** of wall time; in a windowed run with CoreAudio on 14 September it advanced 5.005 s in 5.006 s. The log's conclusion: the headless route "must not be used as time-faithful footage without more verification".
- A source audit found `_handle_keypress` could index an empty note list; the Walker copy added a guard, labelled "defensive source hardening, not a claimed reproduction".

**What remains unverified.** Everything a player hears, and the song's licence for any public film.

## Hands-on: a hit click, two buses, and proof that the click reaches the mix

You will add confirmation audio — a short click on every Perfect or Good hit — split the mix into Music and SFX, and prove from a terminal that the click is triggered by the right events, routed to the right bus, silent when muted, and well-behaved on restart and pause. The click is generated by a script you can read, so its source is fully disclosed. How it sounds is left to you.

### Predict

1. `note_hit` fires for five hit types. Which should make a sound, and what happens to a player's trust if a Miss clicks too?
2. Three hits land 40 ms apart. With `max_polyphony = 1` on a 60 ms click, what does the player hear? With 4?
3. You press P halfway through a click, and later R. What should the click and the song do in each case, and what does Godot do by default?
4. A headless test says `HitSound.playing == true`. What has that proved about the sound, and what has it not?

### Build It

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Copy `audio/rhythm_game` into a new folder as `godot/`, apply [`walker-adaptation.diff`](../examples/12-audio-and-triggers/walker-adaptation.diff) (the title and the empty-list guard), and copy in `test_live_restart.gd` from [`examples/12-audio-and-triggers/tests/`](../examples/12-audio-and-triggers/tests/). Commit. Import and record the baseline:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://test_live_restart.gd
```

Expect `LIVE_SPACE_PERFECT true` and `LIVE_RESTART_RESET true`, after about ten seconds: it waits in real time for the first chart note. Do not add `--fixed-fps` to audio tests. The audio thread runs in real time whatever the frame clock does, so a test that waits for sound must wait on the wall clock. Use `timeout`: a test script that hits an error before `quit()` never exits, and this chapter's record lost 19 minutes to one.

Now give Claude Code this prompt. It fixes what must not change (timing), specifies the generated asset exactly, names the trigger rule, and asks for tests of level, restart and pause — not just "it plays".

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

```bash
claude -p "$(cat prompt1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(python3:*)" --disallowedTools "Skill" --max-turns 60 --output-format stream-json --verbose > session1.jsonl
```

`Bash(python3:*)` is needed for the generator, and it is broad: it lets the agent run any Python. Acceptable in a scratch copy; not in a repository with secrets. With Codex, the same prompt runs as `codex exec -s workspace-write -C . "$(cat prompt1.txt)" < /dev/null`.

Requirement 5 contains a mistake — the prompt author's, not the agent's — that this chapter's record exposes. The ideas above tell you what it is.

### Use It

Only you can do this part. Use headphones at a fixed system volume, and write down the date and device.

1. Open the **Audio** panel at the bottom of the editor. Confirm the three buses, their sends, and 0 dB faders. Watch the meters while the game runs: Music should move; SFX should flick on hits. (With a real audio driver the meter is fed continuously, unlike Dummy's bursts.)
2. Play the first chart. Does the click confirm a Perfect without masking the music? Is it too loud at 0 dB against a song set to −12 dB? Does a Good sound identical to a Perfect — and should it?
3. Tap Space wildly through a dense passage. With `max_polyphony = 4` the clicks overlap. Feedback or noise?
4. Press P mid-click, wait, press P again. Press R right after a hit. Listen for a click that survives a restart or reappears after a pause.
5. Toggle "Use filtered" and listen for any change in how the click lines up with the beat. There should be none: the click is triggered by the judgment, not by the clock.

### Ship It

- **Commits:** baseline; generator and WAV; bus layout and routing; HitSound and trigger; test. The WAV is 5,336 bytes, so it belongs in Git; the syllabus sends files over 25 MB to Drive or designated media storage.
- **SOURCES.md:** the click is generated by `tools/make_click.py` with no third-party material; the song and metronome keep their upstream attributions; state what is unresolved (the song's licence for public distribution).
- **FRICTIONAL.md:** what the agent believed about headless audio, what your probe showed, what you heard.
- **Brutalist film:** `godot-gamedev` for the routing and the trigger, each excerpt followed by the capture or meter result it produces. A `godot-walkthrough` of the click needs real recorded device audio; a headless log is not audio.

### Verify

```bash
timeout 120 godot --headless --path godot --script res://tests/test_hit_audio.gd
```

```bash
timeout 120 godot --headless --path godot --script res://test_live_restart.gd
```

Then run the instructor's independent probe, [`verification/verify_levels.gd`](../examples/12-audio-and-triggers/verification/verify_levels.gd) — read it first. Copy it into `godot/tests/`. It adds capture effects at runtime, mutes Music so Master carries only SFX, fires the real `note_hit` signal, and prints what each bus carried:

```bash
timeout 60 godot --headless --path godot --script res://tests/verify_levels.gd
```

Run the test more than once. A test that passes nine times in ten is a test that fails.

A pass establishes: the bus graph and routing; that Perfect and Good trigger the click and Miss does not; that the click's samples reach the SFX bus at the level the generator wrote; that muting SFX removes it from Master; that R reloads to silence; that P freezes the song and a second P resumes it. It does not establish that anyone can hear the click, that it is pleasant, that it lands on the beat as heard, or anything about latency on a real device.

## What we actually ran

**Date:** 27 September 2026. **Machine:** the instructor's Mac (Apple M4 Pro, macOS 26.5.1), Godot 4.7.2. **Agents:** Claude Code 2.1.150, whose `-p` mode used the account default `claude-sonnet-4-6`; then Codex CLI 0.153.4 (`gpt-5.6-sol`, reasoning effort `low`). **Starting point:** a scratch repository with the Walker build's `godot/` folder and Markdown files, baseline commit `e1e99db`. The record is in [`examples/12-audio-and-triggers/`](../examples/12-audio-and-triggers/). The recorded Claude Code sessions did not yet have `--disallowedTools "Skill"`; they had `--strict-mcp-config` and `--settings '{"autoMemoryEnabled":false}'`, operational choices for the record.

### Session 1: a working change, a hand-made import file, and two fake PASS lines

Claude Code ran for 54 turns (about 26 minutes; API-equivalent cost reported as $2.82). The production change was small and correct:

```gdscript
func _on_note_hit(beat: float, hit_type: Enums.HitType, hit_error: float) -> void:
	match hit_type:
		Enums.HitType.PERFECT, Enums.HitType.GOOD_EARLY, Enums.HitType.GOOD_LATE:
			$HitSound.play()
```

It wrote `default_bus_layout.tres` (Master, Music and SFX, both sending to Master), set `bus = &"Music"` on the song and `&"SFX"` on the Metronome and a new `HitSound` with `max_polyphony = 4`, and added `buses/default_bus_layout` to `project.godot` (redundant — it names the default path). `git diff` confirms that `conductor.gd`, `note_manager.gd`, `metronome.gd`, the charts and the song's import file are untouched. The generator is 94 lines of standard-library Python; the WAV it wrote measures, by my own check, mono, 16-bit, 44,100 Hz, 2,646 frames (60.0 ms), peak −6.12 dBFS.

Three things in the details are the "dangerous middle" the syllabus warns about:

- The generator **also hand-writes the `.import` file**, with an invented UID (`uid://b1hclk5n0t4xe`), `compress/mode=0` (uncompressed PCM, not the QOA default — a defensible choice nobody asked for), and an imported-file name computed from the WAV's MD5. Godot kept the UID, rewrote the file name on import, and warned `invalid UID … using text path instead` until it had.
- The new node carries `unique_id=1234560001`, an obviously hand-typed ID written straight into the scene file.
- Its first test run failed to parse (`:=` could not infer a type, and `get_tree()` does not exist inside a script that *is* the SceneTree). The second died on a problem the Walker log had already recorded: a class annotation forced `note.gd` to compile before the `GlobalSettings` autoload existed (`Identifier not found: GlobalSettings`). That Godot process never reached `quit()` and was still running 19 minutes later, holding the Claude Code session open until I killed it.

And then the test. The peak checks the prompt asked for were written like this, **before the test had ever run**:

```gdscript
	var is_headless := DisplayServer.get_name() == "headless"
	if is_headless:
		print("PASS peak_sfx_rises_after_perfect",
				" (SKIP: Dummy driver — bus peak meters return floor; see headless note)")
```

The report called this "graceful Dummy-driver SKIP". A SKIP that prints PASS is a false pass, and the belief behind it — that the Dummy driver cannot meter — was never tested. Its final output was 21 PASS lines, two of them fake.

### What the evidence actually said

My probes had already shown the Dummy driver metering a held tone at −6.02 dB. But my own independent check of the finished scene (`verification/verify_levels.gd`, first version, `logs/verify1-levels.log`) read the SFX meter at −200 dB after real Perfect hits, while the music on Master read −33 dB. So the agent's conclusion was wrong, and my premise was incomplete. The probes in the ideas section above — held tone versus 60 ms click, meter versus capture, capture on SFX versus Master — and the driver source settled it: the meter samples the last 512 frames of a 4,096-frame burst, so a short click usually slips past it. The prompt's requirement 5 ("the SFX bus peak … rises above −40 dB within 0.1 s") was asking a meter to see something it cannot see. That was the prompt author's mistake. The right instrument is a capture effect.

### Session 2: capture-based checks, a flaky failure, and a usage limit

I resumed the Claude Code session with the evidence:

```text
Two of your checks print PASS without testing anything, and the reason you give is wrong. You wrote the SKIP before running the test once. In headless Godot 4.7.2 the Dummy driver does mix. In separate probes: a 0.5-amplitude sine held for 200 ms or longer read -6.02 dB on AudioServer.get_bus_peak_volume_left_db, and -200 dB with the bus muted. But that meter reports only the most recent mix block, and a 60 ms sound can be mixed without ever showing on it: an AudioEffectCapture on the same bus recorded about 58 ms of hit_click.wav, peak 0.4993, while the meter read -200 dB on every frame. A capture effect on a bus hears the audio before that bus's volume and mute; a capture on Master hears what the SFX bus actually sends.

Replace both SKIP branches with real checks that run headless. In the test only (do not save it into default_bus_layout.tres), add an AudioEffectCapture to the SFX bus and one to Master, keep the metronome off, and mute the Music bus while measuring so Master carries only SFX. Wait in real time (wall clock), not in frames. Assert: after a PERFECT note_hit, the SFX capture peaks above -12 dBFS and the Master capture above -12 dBFS; with the SFX bus muted, the SFX capture still hears the click but the Master capture stays below -60 dBFS. A check that cannot run must print SKIP, never PASS, and must not count as a pass. Remove the effects and restore the bus state afterwards.

Change nothing outside godot/tests/test_hit_audio.gd. Correct the headless note in that file to say what the Dummy driver actually allows. Run the test three times and godot/test_live_restart.gd once, in real time, and paste the real output.
```

In 21 turns it wrote the four capture checks exactly as specified and fixed the `GlobalSettings` compile error by looking the autoload up at run time. On the second of its complete runs, `hitsound_plays_on_perfect` failed. It started to diagnose the flake — and the session ended with "You've hit your session limit · resets 6:40pm (America/New_York)". The account's Claude Code usage was exhausted for about four hours.

I ran that state ten times: nine runs passed all 23 checks, and run 9 failed `hitsound_plays_on_perfect` (`logs/verify2-*`). The check awaited one frame after `note_hit` before reading `playing`. With the Dummy driver mixing 93 ms at a time, a 60 ms click can start and finish inside one burst between two frames. The test was timing-dependent, and one run in ten caught it.

### The Codex hand-off

Rather than wait, I handed the remaining work to Codex, with the facts it needed and nothing else:

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

The pause change mattered. Session 1's pause check started the click, waited a frame, and asserted its position did not move while paused — which passes trivially if the click has already finished, and under Dummy it often had. Codex made the three changes in about four minutes, touched only the test file, and ran everything: 25/25 three times, and `test_live_restart.gd` passing. Its sandbox again blocked Godot's log file and certificate lookup, harmlessly.

### My verification

All in real time, with `timeout`, on the final state (`logs/verify3-*`):

- `test_hit_audio.gd`, ten runs: **25/25 checks every run**, exit 0, no leak warnings at exit.
- `test_live_restart.gd`: `LIVE_SPACE_PERFECT true`, `LIVE_RESTART_RESET true`.
- `git diff e1e99db HEAD -- godot/game_state godot/globals godot/music godot/objects`: empty. Timing, charts and the song are untouched.
- My independent probe, `verify_levels.gd` (capture version), which shares no code with the agent's test:

```text
driver=Dummy
  bus 0 Master -> '' volume_db=0.0
  bus 1 Music -> 'Master' volume_db=0.0
  bus 2 SFX -> 'Master' volume_db=0.0
song on bus Music: playing=true position=1.21 s; Music meter=-34.76 dB
HitSound: bus=SFX max_polyphony=4 stream length=0.06 s
SFX muted=false: SFX capture peak -6.12 dBFS, Master capture peak -6.12 dBFS, SFX meter max seen -200.0 dB
SFX muted=true: SFX capture peak -6.12 dBFS, Master capture peak -200.0 dBFS, SFX meter max seen -200.0 dB
note_hit type 0 (miss): SFX capture peak -200.0 dBFS
note_hit type 4 (miss): SFX capture peak -200.0 dBFS
```

The capture peak, −6.12 dBFS, is the peak I measured in the WAV file itself, so the click reaches the SFX bus unchanged (uncompressed import, 0 dB player, 0 dB bus). Muting SFX removes it from Master. The two Miss types put nothing on the bus. And the SFX meter never saw any of it — the instrument the original prompt asked for.

### What is still unverified

Whether the click is audible, pleasant, or balanced against the song; whether it lands on the beat as heard; latency on any real device; and the song's licence for a public film. One check in the final test — `space_hit_starts_hitsound`, which reads `playing` two frames after a real key press — has the same timing shape as the check that flaked, and was not changed.

## Check your understanding (ungraded)

1. Open `hit_click.wav.import`. Which settings did the agent choose that the prompt did not specify? What would change in the engine if `compress/mode` were 2?
2. Read `audio_driver_dummy.cpp` at 4.7.2. Explain, with the numbers, why a 200 ms tone shows on the bus meter headless and a 60 ms click usually does not.
3. Why does a capture on the SFX bus still hear the click when SFX is muted? Where in `AudioServer::_mix_step` is the order that causes it?
4. `space_hit_starts_hitsound` reads `playing` two frames after the key press. Estimate how often it could fail under Dummy, then run the test twenty times and compare.
5. Change `HitSound.max_polyphony` to 1 and write a capture-based check that detects the difference when three `note_hit` signals arrive 20 ms apart.
6. Where would you put a UI click that must keep playing while the game is paused, and which property makes it work?

## Doing the same thing in Unity

Unity was not run for this chapter. The comparisons come from Unity's official documentation, checked on 27 September 2026 (default manual: Unity 6.6, 6000.6).

### Similarities

The parts line up. An **AudioClip** is the imported sound; an **AudioSource** plays it; an **AudioListener** "acts like a microphone", and "each scene can only have 1 Audio Listener to work properly" ([audio overview](https://docs.unity3d.com/Manual/AudioOverview.html), [AudioListener](https://docs.unity3d.com/Manual/class-AudioListener.html)). Where Godot has three player nodes, Unity has one AudioSource with a **Spatial Blend**: 0 is 2D, 1 is fully 3D, attenuated by distance and direction ([AudioSource](https://docs.unity3d.com/Manual/AudioSource-reference.html)). Godot's buses are Unity's **Audio Mixer** groups, which "accept any number of input signals" and "produce exactly one output", with effects, snapshots and exposed parameters ([Audio Mixer](https://docs.unity3d.com/Manual/AudioMixerOverview.html)).

This chapter's change in Unity: import `hit_click.wav`; route the click's AudioSource to an `SFX` mixer group and the song's to `Music`; in the hit-judging code, play the click for Perfect and Good only. Import settings matter the same way: each AudioClip has a **Load Type** (Decompress On Load, Compressed In Memory, Streaming), a **Compression Format** (PCM, ADPCM, Vorbis/MP3), Force To Mono, Load In Background and Preload Audio Data ([AudioClip import](https://docs.unity3d.com/Manual/class-AudioClip.html)). Unity imports .mp3, .aif/.aiff, .wav, .ogg and .flac, plus tracker modules ([supported formats](https://docs.unity3d.com/Manual/AudioFiles-compatibility.html)).

### Differences

- **Polyphony is a method.** `PlayOneShot` "does not cancel clips that are already being played by PlayOneShot and Play" ([PlayOneShot](https://docs.unity3d.com/ScriptReference/AudioSource.PlayOneShot.html)) — Godot's `max_polyphony > 1`. Calling `Play()` again on the same clip makes it "sound like it is re-started" ([Play](https://docs.unity3d.com/ScriptReference/AudioSource.Play.html)) — Godot's default of one voice.
- **Sample-accurate scheduling exists.** `AudioSource.PlayScheduled` "plays the clip at a specific time on the absolute time-line that `AudioSettings.dspTime` reads from", and Unity describes `dspTime` as much more precise than `Time.time` ([PlayScheduled](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html), [dspTime](https://docs.unity3d.com/ScriptReference/AudioSettings-dspTime.html)). A Unity metronome can be scheduled ahead on the audio clock; Godot 4.7.2's is rounded to the next mix block, as its own comment admits.
- **Ducking is an effect.** The mixer's Duck Volume creates "side-chain compression from signal sent from Sends" ([mixer effects](https://docs.unity3d.com/Manual/AudioMixerInspectors.html)). Godot's `AudioEffectCompressor` has a `sidechain` bus property (checked on 4.7.2), which you wire yourself.
- **Headless testing.** A PlayMode test in `-batchmode` can check routing and that the source starts on a Perfect. Whether Unity's mixer runs and can be captured in batch mode was not checked for this chapter; do not assume it behaves like Godot's Dummy driver.

### The agent-workflow angle

An Audio Mixer is an asset, and an AudioSource lives in a scene or prefab — YAML under Force Text, with GUID references through `.meta` files. An agent can change an AudioSource's output group, but the reference is an identifier, not a readable name; a wrong one fails quietly — the same risk as this chapter's invented UID. Exposed parameters are set from C# with `AudioMixer.SetFloat`, and once a parameter is exposed, snapshots no longer control it ([SetFloat](https://docs.unity3d.com/ScriptReference/Audio.AudioMixer.SetFloat.html)) — an interaction an agent will not know unless you say so.

| Godot | Unity |
|---|---|
| `AudioStreamPlayer` / `2D` / `3D` | `AudioSource` + Spatial Blend |
| camera / `AudioListener2D`/`3D` | `AudioListener` (one per scene) |
| audio bus | Audio Mixer group |
| bus effect, `AudioEffectCapture` | mixer effect |
| `max_polyphony > 1` | `PlayOneShot` |
| starts on the next mix block | `PlayScheduled` on `AudioSettings.dspTime` |
| `.import` sidecar (text) | `.meta` import settings (YAML) |

## Doing the same thing in Unreal Engine

Unreal Engine was not run for this chapter. The comparisons come from Epic's official documentation, checked on 27 September 2026 (newest documented version: 5.8). Unreal's source is available to registered GitHub users under the Unreal Engine EULA — source-available, not open source.

### Similarities

A **Sound Wave** is the imported sound. **Sound Classes** "group multiple sounds together" so their parameters can be altered at once, and Sound Class Mixes adjust them during play ([Sound Classes](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-classes-in-unreal-engine)). **Submixes** do what Godot's buses do: "mix audio generated from individual sources into a single output buffer" and apply DSP effects ([Submixes](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-submixes-in-unreal-engine)). Positional sound is governed by **Attenuation** settings — volume, spatialization, air absorption, occlusion and more ([attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)).

Triggers look familiar. **Play Sound 2D** plays "with no attenuation, perfect for UI sounds"; **Play Sound at Location** is "a fire and forget sound and does not travel with any actor"; **Spawn Sound Attached** creates an Audio Component attached to a scene component ([Play Sound 2D](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Audio/PlaySound2D), [Play Sound at Location](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Audio/PlaySoundatLocation), [Spawn Sound Attached](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Audio/SpawnSoundAttached)). Trigger volumes are "Actors that are used to cause an event to occur when they are interacted with" ([trigger volumes](https://dev.epicgames.com/documentation/en-us/unreal-engine/trigger-volume-actors-in-unreal-engine)) — Godot's `Area2D.body_entered`.

### Differences

- **Concurrency is an asset with rules.** A Sound Concurrency asset limits "how many sounds play simultaneously and what to do when that limit is reached", with rules such as Prevent New, Stop Oldest, Stop Farthest Then Oldest and Stop Quietest ([concurrency](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-concurrency-reference-guide)). Godot's `max_polyphony` has one rule: cut off the oldest.
- **Sample-accurate audio exists twice.** MetaSounds give "complete control over a Digital Signal Processing (DSP) graph" with "sample-accurate timing and control at the audio buffer level" ([MetaSounds](https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-the-next-generation-sound-sources-in-unreal-engine)); **Quartz** is "a Blueprint-exposed scheduling system" providing "sample-accurate audio playback" across game, audio-logic and audio-rendering threads ([Quartz](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-quartz-in-unreal-engine)). The rhythm game's metronome in Unreal would be a Quartz clock, not a per-frame check.
- **Import converts.** Unreal imports .wav, .ogg, .flac, .aif, .opus and .mp3, and "all imported audio files are converted to 16-bit .wav files internally"; the shipped codec (Bink Audio by default, ADPCM, PCM or platform-specific) is chosen per platform ([importing audio](https://dev.epicgames.com/documentation/en-us/unreal-engine/importing-audio-files)). Godot keeps Ogg and MP3 as imported, and offers compression choices only for WAV.
- **Sound Cues are the older graph.** A Sound Cue "encapsulates complex sound design tasks within a node graph" ([Sound Cue](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-cue-reference-for-unreal-engine)); Epic's UE5 migration guide says MetaSounds will supersede them.
- **Headless testing.** `-nullrhi` removes rendering; this chapter did not verify how Unreal's mixer behaves in a `-nullrhi` automation run, so a test that measures a submix would need its own check — the lesson of this chapter.

### The agent-workflow angle

Sound Waves, Sound Classes, Submixes, Concurrency assets and MetaSounds are all `.uasset` files, which Epic describes as binary and not mergeable as text ([Perforce and Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine)). An agent can write the C++ or Blueprint-callable code that plays a sound on a Perfect, and can script asset setup through editor Python, but it cannot show you a readable diff of the routing. In Godot the whole change in this chapter — bus layout, routing, player, trigger, generator and test — is text, and every mistake in the record was found by reading it.

| Godot | Unreal Engine 5 |
|---|---|
| `AudioStream` (WAV/Ogg/MP3) | Sound Wave |
| `AudioStreamPlayer` / `2D` / `3D` | Audio Component; Play Sound 2D / at Location |
| audio bus | Submix (routing, effects); Sound Class (grouping, levels) |
| `max_polyphony` | Sound Concurrency asset |
| starts on the next mix block | Quartz clock; MetaSounds |
| `Area2D.body_entered` | trigger volume / overlap event |
| `default_bus_layout.tres` (text) | Submix and Sound Class `.uasset`s (binary) |

## Sources

Godot (official documentation, "stable" = 4.7, and engine source at tag `4.7.2-stable`):

- [Audio buses](https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html), [audio streams](https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html), [sync the gameplay with audio and music](https://docs.godotengine.org/en/stable/tutorials/audio/sync_with_audio.html), [importing audio samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html), [pausing games](https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html)
- Class references: [AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html), [AudioStreamPlayer2D](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer2d.html), [AudioStreamPlayer3D](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer3d.html), [AudioServer](https://docs.godotengine.org/en/stable/classes/class_audioserver.html), [AudioEffectCapture](https://docs.godotengine.org/en/stable/classes/class_audioeffectcapture.html), [AudioStreamGenerator](https://docs.godotengine.org/en/stable/classes/class_audiostreamgenerator.html), [ProjectSettings](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html)
- [Command-line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- Engine source: [`servers/audio/audio_driver_dummy.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/audio/audio_driver_dummy.cpp) and [`audio_driver_dummy.h`](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/audio/audio_driver_dummy.h) (4096-frame bursts, fixed sleep); [`servers/audio/audio_server.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/audio/audio_server.cpp) (`buffer_size = 512`; effects before fader and meter)
- Godot demo projects at commit [`a3b5c113`](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7): `audio/rhythm_game` and the six other `audio/` demos (MIT; asset notes as listed in each demo)

Course and Walker records:

- `walker-audio-rhythm-game` (README, GAME-BRIEF, SOURCES, FRICTIONAL), and the README/FRICTIONAL/VERIFICATION/ASSET-PROVENANCE files of `walker-audio-audio-effects`, `walker-audio-bpm-sync`, `walker-audio-device-changer`, `walker-audio-generator`, `walker-audio-mic-record`, `walker-audio-midi-piano`; `walker-3d-platformer/godot/enemy/enemy.tscn`
- This chapter's record: [`examples/12-audio-and-triggers/`](../examples/12-audio-and-triggers/)

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 27 September 2026:

- Unity: [audio overview](https://docs.unity3d.com/Manual/AudioOverview.html), [AudioListener](https://docs.unity3d.com/Manual/class-AudioListener.html), [AudioSource](https://docs.unity3d.com/Manual/AudioSource-reference.html), [Audio Mixer](https://docs.unity3d.com/Manual/AudioMixerOverview.html), [mixer effects](https://docs.unity3d.com/Manual/AudioMixerInspectors.html), [AudioClip import](https://docs.unity3d.com/Manual/class-AudioClip.html), [supported formats](https://docs.unity3d.com/Manual/AudioFiles-compatibility.html), [PlayOneShot](https://docs.unity3d.com/ScriptReference/AudioSource.PlayOneShot.html), [Play](https://docs.unity3d.com/ScriptReference/AudioSource.Play.html), [PlayScheduled](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html), [dspTime](https://docs.unity3d.com/ScriptReference/AudioSettings-dspTime.html), [AudioMixer.SetFloat](https://docs.unity3d.com/ScriptReference/Audio.AudioMixer.SetFloat.html)
- Unreal Engine: [Sound Classes](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-classes-in-unreal-engine), [Submixes](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-submixes-in-unreal-engine), [attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine), [Sound Concurrency](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-concurrency-reference-guide), [MetaSounds](https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-the-next-generation-sound-sources-in-unreal-engine), [Quartz](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-quartz-in-unreal-engine), [Sound Cue](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-cue-reference-for-unreal-engine), [importing audio](https://dev.epicgames.com/documentation/en-us/unreal-engine/importing-audio-files), [Play Sound 2D](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Audio/PlaySound2D), [Play Sound at Location](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Audio/PlaySoundatLocation), [Spawn Sound Attached](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Audio/SpawnSoundAttached), [trigger volumes](https://dev.epicgames.com/documentation/en-us/unreal-engine/trigger-volume-actors-in-unreal-engine), [Perforce and Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine)
