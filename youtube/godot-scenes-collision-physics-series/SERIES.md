# Godot objects and interaction — lecture series

CSYE 7270 Building Virtual Environments. Liam in for Bear, local Kokoro am_onyx, @NikBearBrown. The user explicitly requested multiple films and asked for a trigger/collider distinction; that overrides the lecture skill's default one-film treatment of the source.

The earlier combined lecture is preserved as source material. These four films are independent learning units, each with its own opening, prerequisite terms, four acts, recap, exercise, outro, narration, scenes, evidence and render handoff. No video numbers will appear in viewer-facing material. Order below is a teaching recommendation, not a numbered series contract.

| Film | Question answered | Worked example | Exit check |
|---|---|---|---|
| Scenes and Instances in Godot | How do I compose a reusable game object? | Reusable door and independent instances | Two instances work without hard-coded external paths. |
| Collision Shapes, Layers, and Masks in Godot | Where is the boundary and which pairs interact? | Player, wall, coin and tile floor | Explain a permitted and an excluded interaction. |
| Triggers and Colliders in Godot | When should contact block movement, and when should it notify code? | One door with a solid body and an approach area | Sensor detects without blocking; solid body blocks until deliberately opened. |
| Character Motion and Rigid-Body Physics in Godot | Does gameplay code or the solver calculate the movement? | Designed jump, crate and debris | Measured jump tolerance and impulse response; separate presentation from simulation. |

## Dependency and overlap policy

Teach scenes first, then shape/filtering fundamentals, then triggers as a focused application, then motion and simulation. The trigger film can also stand alone: it redefines shapes, bodies, areas, and mask direction briefly. Physics reintroduces body ownership and ticks; it does not repeat the whole scene or layer lecture. Repeated short prerequisites are intentional. No film says the viewer must have watched another.

The door is a recurring example: composition in Scenes, physical boundary/filtering in Collision, two independent mechanisms in Triggers. The physics film uses the same test-room context but focuses on a player and movable prop, where simulation is actually relevant.

## Collider versus trigger

Collider is commonly used for contact geometry or a solid collision boundary. Trigger is overlap detection without solid blocking. Both use collision geometry. In Godot a CollisionShape2D/3D supplies geometry to a physics body or an Area2D/3D; the owning collision object supplies the role. They are not competing shape resources. A solid collision can also be reported to code; an area can also influence gravity/damping. Detection and response are separate choices.

## Source coverage

The entire supplied research/overview is distributed across these films. Version chronology, optional Scene Paint/AwaitTweener conveniences and unverified third-party determinism recommendations remain companion context rather than narration. Source-provided conventions are treated as recommendations, not instructions to edit a reference game's repository. The old combined package and its original claims review remain unchanged.
