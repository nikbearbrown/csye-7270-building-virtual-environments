# Module 12 — Helpful links

## Executive summary

This page collects the reading, the official Godot audio documentation, the public Walker projects and the tools behind Module 12. Open it while you build the click and the bus layout, and again when you decide what a headless run can and cannot tell you about sound.

## Read first

- [Chapter 12 — Audio and Triggers](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/12-audio-and-triggers.md) — the long reading behind this module: the full record of the 27 September 2026 runs, the headless audio probes and the Unity and Unreal comparisons.

## Godot documentation

- [Audio buses](https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html) — how buses, effects and sends route sound to Master, and how decibel levels work.
- [Audio streams](https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html) — the three stream-player nodes and how 2D and 3D sound is positioned; its banner says it is not yet updated for 4.7, and the class references are current.
- [Sync the gameplay with audio and music](https://docs.godotengine.org/en/stable/tutorials/audio/sync_with_audio.html) — why audio time is not frame time, and the documented latency correction.
- [Importing audio samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html) — WAV, Ogg Vorbis and MP3 import settings: compression, loop mode and loop points.
- [Pausing games](https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html) — how `process_mode` decides which nodes, audio players included, pause with the tree.
- [AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html) — `max_polyphony`, `play()`, `bus` and `stream_paused`, the properties the tests read.
- [AudioServer](https://docs.godotengine.org/en/stable/classes/class_audioserver.html) — the bus meter, latency and mix-time calls the chapter's tests and probes use.
- [AudioEffectCapture](https://docs.godotengine.org/en/stable/classes/class_audioeffectcapture.html) — the effect that records every frame on a bus, and so sees a short click the meter misses.

## Walker projects

- [walker-audio-rhythm-game](https://github.com/nikbearbrown/walker-audio-rhythm-game) — the build you modify: the Conductor, the Metronome, the `note_hit` signal and its live-input tests.
- [walker-audio-audio-effects](https://github.com/nikbearbrown/walker-audio-audio-effects) — bus effects, and what an 18 of 18 toggle check does and does not show.
- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer) — positional 3D sound: `AudioStreamPlayer3D` on the enemies, in `godot/enemy/enemy.tscn`.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — the regular (non-.NET) build; the recorded runs used 4.7.2.
- [Claude Code documentation](https://code.claude.com/docs/en/overview) — install and run Claude Code, the agent the lesson's prompts are written for.
- [Audacity](https://www.audacityteam.org/) — the free audio editor from the old course's Audio page, for trimming and inspecting a sound before you import it.

## Going deeper

- [audio_driver_dummy.cpp at 4.7.2-stable](https://github.com/godotengine/godot/blob/4.7.2-stable/servers/audio/audio_driver_dummy.cpp) — the engine source behind the 4,096-frame bursts and the 93 ms sleep that explain what headless audio can see.
- [Freesound](https://freesound.org/) — carried over from the old course's Audio page; a collaborative sound database where each sound has its own Creative Commons licence, so read the licence per sound.
- [So You Wanna Make Games?? | Episode 8: Sound Design](https://youtu.be/KcorIwJscFA) — a sound-design episode carried over from the old course's Audio page.
