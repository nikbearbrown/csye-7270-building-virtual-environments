# Module 13 — Helpful links

## Executive summary

This page collects the reading, documentation, Walker project and tools behind Module 13. Open the Godot pages while you write your Predict answers and the benchmark prompt, and keep the engine-source link nearby for the day a Performance monitor surprises you.

## Read first

- [Chapter 13 — Profiling and Optimization](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/13-profiling-and-optimization.md) — the long reading: the full record of the agent runs, the ten-run measurements, and the Unity and Unreal comparison.
- [walker-2d-bullet-shower](https://github.com/nikbearbrown/walker-2d-bullet-shower) — the public Walker build (MIT) that you benchmark; read its README and FRICTIONAL.md before prompting.

## Godot documentation

- [General optimization](https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html) — the profile, find the bottleneck, optimize, repeat loop that the module follows.
- [CPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html) — why the profiler is started and stopped by hand, and how it distorts what it measures.
- [GPU optimization](https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html) — the costs a headless benchmark cannot see: draw calls, fill rate and the limits of mobile GPUs.
- [Optimization using Servers](https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html) — when skipping nodes pays off, and what you give up by doing it.
- [The Performance class](https://docs.godotengine.org/en/stable/classes/class_performance.html) — every monitor, including `TIME_PROCESS`, and `add_custom_monitor()` for your own counters.
- [The Profiler](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html) — how to start, stop and read the script profiler in the Debugger panel.
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) — `--headless`, `--script`, `--import` and the flags that decide what a headless timing means.

## Walker projects

- [walker-3d-graphics-settings](https://github.com/nikbearbrown/walker-3d-graphics-settings) — 17 headless assertions on render scale, field of view and image sliders, and a clear list of what stored settings do not prove.
- [walker-loading-threads](https://github.com/nikbearbrown/walker-loading-threads) — a reproduced threading race, its fix, and the stress runs that followed.
- [walker-misc-custom-logging](https://github.com/nikbearbrown/walker-misc-custom-logging) — a `Logger` registered with `OS.add_logger()`, the starting point for game analytics.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — the regular (not .NET) edition for GDScript; the recorded runs used 4.7.2.
- [Claude Code overview](https://code.claude.com/docs/en/overview) — the command-line agent you direct in every Build It step.
- [coreutils on Homebrew](https://formulae.brew.sh/formula/coreutils) — provides the `timeout` command that stock macOS lacks, which the Verify commands in this module use.

## Going deeper

- [`main/main.cpp` at tag 4.7.2-stable](https://github.com/godotengine/godot/blob/4.7.2-stable/main/main.cpp) — the engine source where `TIME_PROCESS` becomes a one-second maximum and the 6,900 µs sleep default lives.
- [Game Loop, in Game Programming Patterns](https://gameprogrammingpatterns.com/game-loop.html) — an engine-neutral account of fixed and variable time steps, the idea behind `--fixed-fps`.
- [Data Locality, in Game Programming Patterns](https://gameprogrammingpatterns.com/data-locality.html) — an engine-neutral explanation of how memory layout affects CPU speed; background reading, not something this module measured.
