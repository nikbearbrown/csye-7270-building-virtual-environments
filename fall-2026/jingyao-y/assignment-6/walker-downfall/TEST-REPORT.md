# TEST-REPORT.md — Assignment 6

Machine: Windows 11, Godot 4.7.2-stable (official) console build, Forward+ / D3D12.
Every run goes through `scripts/run-test.sh`; the mode is given with each result.

## Headless facts probe

`./scripts/run-test.sh a6_probe_headless.gd 60` → `logs/a6_probe_headless_60fps.log`
(agent, 2026-11-07). Headless reports `forward_plus` / `d3d12` with an empty
adapter name (dummy renderer). Every class, property and enum CHANGE-BRIEF.md
names exists in 4.7.2. `CPUParticles3D` has no `amount_ratio`;
`ParticlesMaterial` and `scale_random` do not exist; `initial_velocity` and
`scale` exist as Vector2 compatibility properties that set the min/max pair.
A one-shot `GPUParticles3D` reads `emitting == false` from frame 1 and never
emits `finished` headlessly.

## Baseline (before any A6 code)

See the sections below once the runs finish.
