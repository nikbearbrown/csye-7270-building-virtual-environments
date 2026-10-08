# Module 5 — Helpful links

## Executive summary

This page collects what to open while you work through Module 5: the companion chapter and its example record, the Godot manual pages behind the 3D interaction and the mobile, network and XR scoping, and the public Walker material for design documents. Walker's `/gdd` skill is not in public Walker `main` yet, so the Walker section links the public prompt and workflow document that exist today.

## Read first

- [Chapter 5 — The GDD and Virtual Worlds](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/05-the-gdd-and-virtual-worlds.md) — the long reading behind this lesson, including the full Unity and Unreal comparisons.
- [Worked-example record for Chapter 5](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/examples/05-the-gdd-and-virtual-worlds/README.md) — the recovered GDD, the checkpoint-pad criterion, the diffs, the tests and every prompt and log from the 27 September 2026 runs.

## Godot documentation

- [Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html) — open it for Godot's coordinate system and units when you write a quantity into an acceptance criterion.
- [Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html) — the node behind the checkpoint pad; check `body_entered` and `monitoring` here.
- [Marker3D](https://docs.godotengine.org/en/stable/classes/class_marker3d.html) — the position-hint node to name when a criterion needs a respawn point someone can inspect.
- [Using physics interpolation](https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/using_physics_interpolation.html) — why a teleport must reset interpolation, and what happens on screen if it does not.
- [Input examples](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html) — touch events and emulating touch from the mouse, for scoping a mobile target.
- [High-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html) — the MultiplayerAPI, ENet, and the advice to treat client input as untrusted, for scoping a networked target.
- [Setting up XR](https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html) — OpenXR, the node set an XR scene needs, and why initialization can fail, for scoping an XR target.

## Walker projects

All are public, and each Walker project keeps the upstream MIT license.

- [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer) — the build you recover a design from and extend with the checkpoint pad; open `tests/input_probe.gd` and `tests/feature_route.gd` for the probes.
- [Walker: prompts/zelda-gdd.md](https://github.com/nikbearbrown/walker/blob/main/prompts/zelda-gdd.md) — the public GDD prompt you can hand to an agent as plain instructions while `/gdd` is unpublished; it has no `reverse` spec.
- [Walker: docs/zelda-gdd-workflow.md](https://github.com/nikbearbrown/walker/blob/main/docs/zelda-gdd-workflow.md) — the workflow document for the GDD skill; the public copy still describes `/gdd` as a specification, so read it as a plan.
- [walker-mobile-multitouch-cubes](https://github.com/nikbearbrown/walker-mobile-multitouch-cubes) — a model of honest mobile scoping: synthetic touch verified, physical devices named as unverified.
- [walker-networking-multiplayer-bomber](https://github.com/nikbearbrown/walker-networking-multiplayer-bomber) — a model of networked scoping: two real processes on loopback verified, anything beyond loopback unverified.
- [walker-xr-openxr-character-centric-movement](https://github.com/nikbearbrown/walker-xr-openxr-character-centric-movement) — a model of XR scoping: import verified, headset behavior unverified.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — install the regular (not .NET) build; the chapter's runs used Godot 4.7.2.

## Going deeper

- [What are game mechanics? (Lostgarden)](https://lostgarden.home.blog/2006/10/24/what-are-game-mechanics/) — an essay proposing a working definition of game mechanics, carried over from the Spring 2026 course; open it when a mechanics section needs sharper vocabulary.
- [Game Design: Crash Course Games #19](https://youtu.be/TOQTZ6N_eVg) — a video introduction to game design, carried over from the Spring 2026 course's GDD reading list.
