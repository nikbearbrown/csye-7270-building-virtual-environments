# Scenes and Instances in Godot

## BOPEN · Opening

CSYE seventy-two seventy, Building Virtual Environments. Scenes and Instances in Godot. Build reusable objects with clear scene boundaries.

## BIDEA · Opening

Hallo. This is Liam, in for Bear. If scene means level to you, Godot's structure seems larger than it is. Start with a door: one reusable object whose parts have clear jobs.

## BDEFS · Opening

Node. One capability in a tree. Tree. A parent-child arrangement. Instance. A live copy of a definition. Resource. Data that nodes can share.

## BACT1 · A Scene Is an Object

A Scene Is an Object.

## BS01 · A Scene Is an Object

A scene can be a door, a character, or a whole level. Nodes supply capabilities. Saving their arrangement lets us reuse the object without rebuilding every part. Think of the scene as a reusable object boundary, not a synonym for level.

## B03 · A Scene Is an Object

A scene is a reusable node tree, usually saved as a text scene file. One root owns this small example. A complete level, a player, a coin, and a menu can each be scenes.

## B04 · A Scene Is an Object

Node itself has no position. Two D and three D spatial nodes provide transforms. Here a child keeps its local offset when its parent moves. Top-level settings and different node types can change that relationship.

## BS02 · A Scene Is an Object

Our door combines a visible panel, a solid body, and an approach area. Each collision shape belongs directly to the object it describes. This tree is derived from the saved door scene; the door owns the behavior of the assembly.

## BACT2 · Reuse Without Surprises

Reuse Without Surprises.

## B05 · Reuse Without Surprises

PackedScene holds a saved definition. Instantiate creates a live copy. These two copies have different positions, while resources inside them may still be shared. Independent nodes do not automatically mean independent materials or shapes.

## BS03 · Reuse Without Surprises

The locked property is exported so each door instance can start with a different setting. Is open is runtime state. Both belong to the door script. The level can configure the public setting without reaching through the scene to manipulate private children.

## B18 · Reuse Without Surprises

Two nodes can share the same Shape resource. Resize that shared resource and both boundaries change. Duplicate the resource when you need one independent boundary. This is resource ownership, separate from whether the nodes were instanced separately.

## B06 · Reuse Without Surprises

A level has a player and coins: composition. An inherited scene specializes a base scene: a variant relationship. Prefer exported settings over repeatedly exposing editable children. Reuse should preserve a clear boundary around the object.

## BACT3 · Connect Clear Boundaries

Connect Clear Boundaries.

## B07 · Connect Clear Boundaries

Let the level connect a coin's collected signal to the score update. The coin reports what happened without locating a distant parent. Unique names help inside a scene; persistent state can live in an autoload.

## BS04 · Connect Clear Boundaries

The level creates two doors and connects the first door's approach signal. The door reports an actor; the level decides what that means for the level. No hard-coded chain of parent lookups is needed to find the recipient.

## B08 · Connect Clear Boundaries

A question block remembers whether it was used, so give it a small scene and an explicit state. Animate its visual child for a cosmetic bump. If the solid surface must push something, use an animatable body.

## BS05 · Connect Clear Boundaries

A fresh door starts closed. Opening one instance changes that instance's state and shape; it does not open its neighbor. If a door must remain unlocked across level changes, store that progression outside the disposable instance and restore it deliberately.

## BACT4 · Verify the Composition

Verify the Composition.

## B09 · Verify the Composition

Keep actors, blocks, levels, interface, and layer definitions organized by responsibility. Test scenes in isolation. When editing text scenes, preserve resource references and existing identifiers; letting the engine save a PackedScene avoids hand-copying node identifiers.

## B02 · Verify the Composition

This lab ran in Godot four point seven point two. Match your documentation and project settings to the installed engine. A saved version is reproducible context; calling something the latest release is a claim that soon expires.

## B53 · Verify the Composition

Before an agent extends reference code, inspect the seed for old APIs, scaled collision nodes, hard-coded parent paths, and movement outside physics callbacks. Static searches are leads. A clean search does not prove behavior, and we have not audited an unseen course game.

## B52 · Verify the Composition

Write the engine version, scene boundaries, named layers, movement callback, and test commands into the repository conventions. These are project policies, not universal laws. Require the agent to report what ran and what still needs a playtest.

## B54 · Verify the Composition

Use the documentation matching your engine, beginning with nodes and scenes, physics introduction, and the character-body reference. Keep the runnable lab beside those pages. Predict an outcome, run one controlled test, and use the evidence to revise your explanation.

## BVDT · Closing

Let's recap with Claude. For CSYE seventy-two seventy, Building Virtual Environments. A scene packages nodes into a reusable object. Instance settings and shared resources have different ownership. Signals keep communication at explicit object boundaries. A small fixture makes composition testable.

## BHTF · Closing

Help me build a reusable Godot four door scene with a visible panel, a solid body, and an approach area. Export a locked setting. Instantiate two doors with different settings, connect an approach signal in the level, and test that opening one leaves the other closed. State which resources are shared and which state must persist outside a scene.

## BOUT · Closing

Scenes and Instances in Godot. At Nik Bear Brown.
