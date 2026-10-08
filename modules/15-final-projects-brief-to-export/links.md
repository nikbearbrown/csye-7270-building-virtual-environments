# Module 15 — Helpful links

## Executive summary

This page collects the reading, documentation, projects and tools behind the capstone module on reproducing, saving and exporting a Godot game. Open it when you prepare your clean-clone run, decide whether to install export templates, or plan the two final films.

## Read first

- [Chapter 15 — Final Projects: From Brief to Export](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/15-final-projects-brief-to-export.md) — the long reading behind this module: the full worked example, real output, and the Unity and Unreal comparisons.
- [Worked-example record for Chapter 15](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/main/examples/15-final-projects-brief-to-export) — both prompts, the agent's transcripts, the reviewer's checks and every log, for reproducing the run or checking a number.
- [Required Brutalist Godot explainers](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/prerequisites/brutalist-godot-explainers.md) — which film skill proves which claim, and what belongs in GitHub versus media storage.

## Godot documentation

- [Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html) — export presets, templates, resource filters, and which export files are safe to commit.
- [Exporting for the Web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html) — the WebGL 2.0 and Compatibility renderer limits, and how to serve and test a Web export.
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) — the flags used here: `--headless`, `--import`, `--fixed-fps` and the export options.
- [File paths in Godot projects](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html) — where `res://` and `user://` point on each operating system.
- [Saving games](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html) — JSON or binary save files, the types JSON cannot hold, and a note pointing to `ConfigFile` for settings.
- [FileAccess](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html) — how opening fails, when data is flushed, and the warning about deserializing objects.

## Walker projects

- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) — the Week 15 example: the brief-to-export documents, the three baseline test scripts and `scripts/clawd-build.cjs`.
- [walker-loading-serialization](https://github.com/nikbearbrown/walker-loading-serialization) — JSON and `ConfigFile` saves with 28 negative and 42 validator checks; the validate-before-you-change-state lesson.
- [walker-gui-accessibility](https://github.com/nikbearbrown/walker-gui-accessibility) — focus, accessible names, a live region and a custom accessible list, with a README that states what headless tests cannot verify.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — the regular, non-.NET editor; its export templates are a separate, large download whose installation is your decision.
- [Brutalist](https://github.com/nikbearbrown/brutalist.art) — the course-provided checkout holds the `godot-walkthrough` and `godot-gdd` film skills; request the update if your copy lacks one.
- [Node.js downloads](https://nodejs.org/en/download) — needed to run `scripts/clawd-build.cjs`, the project's own invariant check.
- [Homebrew coreutils](https://formulae.brew.sh/formula/coreutils) — on macOS, the package that provides the `timeout` command used to wrap every headless test run.

## Going deeper

- [Godot 4.5 release notes](https://godotengine.org/releases/4.5/) — where screen reader support through AccessKit arrived, described by Godot as experimental.
- [Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/) — a reference of basic, intermediate and advanced guidelines for not excluding players, useful when deciding what "accessible" means for your menu.
