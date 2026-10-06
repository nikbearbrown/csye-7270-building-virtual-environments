# Module 0 — Helpful links

## Executive summary

This page lists what to open while you set up the toolchain and run the walker-pong example: the companion chapter and its run record, the Godot pages behind the command-line options, the repositories, the installers, and the agent documentation. Open the Tools links first, then the rest as a step in the lesson sends you to them.

## Read first

- [Chapter 0: The Toolchain](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md) — the long reading behind this module, with the full timing experiment and the Unity and Unreal comparisons.
- [Chapter 0 worked-example record](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/main/examples/00-the-toolchain) — the diffs, readable transcripts, `PROMPTS.md` and verification logs from the 27 September 2026 runs.

## Godot documentation

- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) — what `--headless`, `--path`, `--script`, `--import` and `--check-only` do, and how to put `godot` on your `PATH`.
- [Idle and physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html) — why `delta` is in seconds, and the background for the frames-are-not-seconds trap.
- [SceneTree class](https://docs.godotengine.org/en/stable/classes/class_scenetree.html) — the class a headless test script extends, so `godot --script` can run it as the whole program.
- [TSCN file format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html) — how to read a `.tscn` scene as text, the way an agent does.
- [Version control systems](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html) — what to commit and why `.godot/` stays out of Git.

## Walker projects

- [walker-pong](https://github.com/nikbearbrown/walker-pong) — the game for this module's score task: its `AGENTS.md`, `tests/input_route.gd`, and MIT license with upstream attribution.
- [Walker framework](https://github.com/nikbearbrown/walker) — the README and `publish.sh` behind the instruction files; its bundled Godot guide targets C#/.NET, which this course does not use.
- [Godot demo projects, `2d/pong` at the adapted commit](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/2d/pong) — the upstream demo that walker-pong adapts, for comparing against the original.

## Tools

- [Godot 4.7.2 download](https://godotengine.org/download/archive/4.7.2-stable/) — the regular (non-.NET) editor version the course numbers were recorded on.
- [Claude Code setup](https://code.claude.com/docs/en/setup) — install, `claude --version`, and sign-in; it states which account types include Claude Code.
- [Codex CLI](https://developers.openai.com/codex/cli) — the optional second agent's installation and sign-in pages.
- [Git downloads](https://git-scm.com/downloads) — the fourth tool, needed before the first `git clone`.

## Going deeper

- [Claude Code: how Claude remembers your project](https://code.claude.com/docs/en/memory) — `CLAUDE.md` versus `AGENTS.md`, and the version from which `AGENTS.md` is read directly.
- [Claude Code: permission modes](https://code.claude.com/docs/en/permission-modes) — what runs without asking in each mode, for choosing how narrow to be.
- [Codex: AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) — how Codex finds and combines instruction files from the Git root down.
- [Godot 4.7.2 source: `core/os/os.cpp`](https://github.com/godotengine/godot/blob/4.7.2-stable/core/os/os.cpp) — `OS::add_frame_delay`, where headless Godot's sleep between frames comes from.
