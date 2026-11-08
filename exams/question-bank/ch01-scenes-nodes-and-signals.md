# Chapter 1: Scenes, nodes and signals

## MA-ch01.1

A Godot beginner is asked to define the basic terms of the engine. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An instance is a saved scene file stored on disk.
- [ ] B. The scene tree is the saved scene file that Godot loads at startup.
- [ ] C. A scene file is limited to a single node.
- [ ] D. A node is the basic building block of a scene, and its type decides what it can do.
- [ ] E. A scene is a saved arrangement of nodes in a tree that can be reused.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: An instance is the set of nodes created from a scene, not the file.
- B: The scene tree is the live hierarchy of nodes in the running game.
- C: A scene holds any number of nodes arranged in a tree.
- D: Godot builds everything from nodes, such as Sprite2D or Timer, and the type gives the abilities.
- E: A scene is a tree of nodes saved as a file that other scenes can reuse.

**Source:** Node, scene, instance, scene tree

## MA-ch01.2

A developer has a saved Character scene (body, sprite, collision shape) and wants a Magician that is mostly the same with one extra staff node. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Instancing and inheriting are two names for the same operation.
- [ ] B. Instancing places a scene as a node inside another scene and keeps it linked to its source file.
- [ ] C. An instanced scene appears as several unlinked top-level nodes.
- [ ] D. Adding the staff to a Magician that inherits from Character means editing the Character scene itself.
- [ ] E. Inheriting creates a new scene that extends a base scene, can add nodes of its own, and follows later changes to the base.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Instancing nests a scene inside another; inheriting builds a new scene on a base.
- B: An instance appears as one node and edits to the source scene reach it.
- C: An instance appears as one node, the root of the instanced scene, still linked to its file.
- D: An inherited scene can add the staff without changing the base.
- E: An inherited scene builds on a base scene and can extend it.

**Source:** Instancing versus inheriting a scene

## MA-ch01.3

A developer tells a coding agent: "Add ten enemies to the level." The agent duplicates the enemy's nodes ten times directly inside the level scene, and later the developer changes the enemy sprite. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Duplicated nodes are independent copies with no link to a shared enemy scene.
- [ ] B. "Instance the Enemy scene ten times in the level, at these positions" is a precise version of the instruction.
- [ ] C. Instancing one saved Enemy scene ten times lets an edit to that scene reach each instance.
- [ ] D. The word "add" does not say whether to duplicate nodes or to instance a scene, which leaves open a choice that affects maintenance.
- [ ] E. Instances of one scene share a single position because they share one scene file.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Plain duplicates are unlinked, so each needs the edit by hand.
- B: It names the term (instance), the scene and the placement.
- C: Instances stay linked to the scene file they came from.
- D: Duplicating and instancing give different results later, so the verb needs to be exact.
- E: Each instance has its own transform.

**Source:** Instancing a scene for repeated objects

## MA-ch01.4

A Main scene has a root Main with one child Player, and Player has one child Sprite. Each node has a script that prints a message from _enter_tree and from _ready. Check each statement that is true about the order of the callbacks. Each statement is worth 1 point (5 points total).

- [ ] A. In Main's _ready, the Player and Sprite have already been through their _ready.
- [ ] B. The _ready of a node is called after the _ready of its children.
- [ ] C. _ready is called before the node has entered the scene tree.
- [ ] D. The _enter_tree of Sprite is called before the _enter_tree of Player.
- [ ] E. The _enter_tree of a parent is called before the _enter_tree of its children.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Main is the last node to be ready.
- B: _ready goes from the leaves up, so children are ready first.
- C: _ready is called once the node and its children are in the tree.
- D: A child enters the tree after its parent.
- E: Entering the tree goes from the root down to the leaves.

**Source:** _enter_tree and _ready order

## MA-ch01.5

A developer describes three callbacks of one Godot node. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. _process is called once per rendered frame.
- [ ] B. _physics_process is called at a fixed rate that does not follow the frame rate.
- [ ] C. _ready is called again on each frame.
- [ ] D. _process is called at the fixed physics rate.
- [ ] E. _ready is called once when the node and its children have entered the scene tree.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: The frame rate can change, and so can the number of _process calls per second.
- B: The physics step is fixed, so physics-driven movement uses this callback.
- C: _ready is called once per node unless it is requested again.
- D: The fixed rate belongs to _physics_process.
- E: One-time setup belongs in _ready.

**Source:** _ready, _process and _physics_process

## MA-ch01.6

A coding agent writes var label = $Label at the top of a script on a node with a child named Label. At startup the console says the node was not found, and label is null later. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A member initializer runs when the script instance is created, before the children are available.
- [ ] B. Godot finds a child by number and does not find it by name.
- [ ] C. Repeating the $Label lookup in _process each frame is the right fix for the null reference.
- [ ] D. _init is the constructor, and it runs when the object is created, before the node is in the tree.
- [ ] E. Marking the variable @onready defers its initialization until right before _ready.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: The children do not exist at that moment, so the lookup fails.
- B: A child is found by name or by path; the cause here is the timing.
- C: A lookup once at ready time is enough and a lookup each frame repeats work.
- D: Assigning children in _init has the same timing problem.
- E: @onready is the annotation for a variable that is assigned when the node is ready.

**Source:** @onready and the null child reference

## MA-ch01.7

Check each statement about GDScript and about how a script relates to a node. Each statement is worth 1 point (5 points total).

- [ ] A. The signal keyword declares a signal that other scripts can connect to.
- [ ] B. A script that begins with extends Node2D builds on that node type and can use its properties and methods.
- [ ] C. Python runs GDScript files inside the engine.
- [ ] D. Member variables belong to each script instance, so each node has its own copy.
- [ ] E. Attaching a script to one node gives the same behaviour to other nodes of the same type.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Declaring a signal makes it part of the node's interface.
- B: extends names the base type that the script is built on.
- C: GDScript looks like Python but has its own interpreter in the engine.
- D: Variables declared at the top of a script are per instance, not global.
- E: A script applies to the node it is attached to.

**Source:** GDScript and scripts on nodes

## MA-ch01.8

A coin script has @export var value: int = 1, and the coin scene is instanced three times in a level. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A value set in the Inspector is stored in the scene file.
- [ ] B. Each instance can carry its own exported value.
- [ ] C. A variable that is not exported is hidden from other scripts.
- [ ] D. @export makes the variable global, so one change reaches each instance.
- [ ] E. @export exposes the variable in the editor's Inspector.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Exported properties are saved with the scene.
- B: The script supplies the default and each instance can override it.
- C: Export concerns the editor, not access from code.
- D: Exported variables are still per-instance members.
- E: Export is about editor visibility.

**Source:** Exported variables

## MA-ch01.9

A developer tells a coding agent: "Let the designer tune run speed and jump height without touching code." Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A group stores numeric values for the nodes in it.
- [ ] B. An exported variable of a Resource type lets the designer pick the tuning file in the Inspector.
- [ ] C. A Resource is added to the scene tree as a child node.
- [ ] D. A constant at the top of a script can be edited in the Inspector.
- [ ] E. A custom Resource is a data container saved as a file that can be edited and shared.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: A group is a tag for finding nodes, not a place for values.
- B: An exported slot of a Resource type lets the file be assigned in the editor.
- C: A Resource is not a node and does not enter the scene tree.
- D: A constant is part of the script text and is not exposed.
- E: A custom Resource with exported fields is a data file.

**Source:** Exported variables and custom Resources

## MA-ch01.10

Three enemies point at the same saved EnemyStats Resource through an exported variable. During play, a script lowers stats.health on one enemy. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Runtime state such as current health is kept in the node, or the Resource is duplicated for each enemy.
- [ ] B. Changing the value in memory rewrites the saved file at once.
- [ ] C. A Resource is a data object, not a node.
- [ ] D. Loading the same resource path returns the same in-memory object, so the change is seen by each enemy.
- [ ] E. @export gives each enemy its own copy of the Resource.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Per-enemy state needs per-enemy storage.
- B: The file changes only if the game saves the resource.
- C: Resources are containers for data.
- D: A shared resource is shared state.
- E: Export exposes the slot; it does not copy.

**Source:** Shared resources

## MA-ch01.11

A Door node has a child Lock, and the Lock should tell the Door when it has been picked. Check each statement that is true about the usual advice "call down, signal up". Each statement is worth 1 point (5 points total).

- [ ] A. A shared ancestor can connect or mediate between sibling scenes.
- [ ] B. A parent can call a method on a child it owns.
- [ ] C. A Lock that emits an unlocked signal can be reused where there is no Door.
- [ ] D. A Lock that calls get_parent().open() is tightly coupled to the layout of the tree above it.
- [ ] E. Sibling scenes should hold direct references to each other.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: An ancestor that knows both siblings can wire them.
- B: Calls go down to children that the parent knows.
- C: The emitter does not need to know what listens.
- D: Coupling is a dependency on structure that is not guaranteed.
- E: Direct sibling references tie scenes together.

**Source:** Call down, signal up; coupling

## MA-ch01.12

A script declares signal health_changed(new_value) and emits it from several places. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emitting calls the connected functions and passes them the arguments.
- [ ] B. A deferred connection runs its function at the end of the frame instead of at once.
- [ ] C. Emitting a signal with no connected function raises an error.
- [ ] D. By default connected functions run at the end of the frame.
- [ ] E. Connecting in the editor's Signals dock and with connect in code both make a connection.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Emit sends the arguments to each connected function.
- B: Deferred mode postpones the call.
- C: A signal without listeners calls nothing.
- D: The default is immediate; deferred is the option that waits.
- E: The dock and code are two ways to make the same kind of link.

**Source:** Signal mechanics

## MA-ch01.13

A coding agent builds player controls from the instruction "Make Space jump and A and D move." Check each statement that is true about input terms. Each statement is worth 1 point (5 points total).

- [ ] A. An input action names an intent, such as jump, and maps to bindings in the Input Map.
- [ ] B. is_action_just_pressed is true on the frame the press began, and is_action_pressed is true while it is held.
- [ ] C. A binding by physical key stays at one keyboard position on other layouts, and a binding by printed character follows the character.
- [ ] D. An action holds one input event.
- [ ] E. Reading the Space key directly is as flexible as using an action.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Code asks about the action and not about a key.
- B: Just pressed and pressed are different tests.
- C: Physical bindings suit WASD-style controls.
- D: An action can group several events, such as a key and a gamepad button.
- E: A hard-coded key cannot be rebound without editing code.

**Source:** Input actions

## MA-ch01.14

A pause menu of Control nodes opens over gameplay. Check each statement that is true about input callbacks. Each statement is worth 1 point (5 points total).

- [ ] A. Polling Input.is_action_pressed in _process is blocked while a menu is open.
- [ ] B. _input is called before the GUI processes the event.
- [ ] C. Marking an event as handled stops it from reaching later nodes.
- [ ] D. _unhandled_input is called before _input.
- [ ] E. _unhandled_input gets events that no earlier callback or Control consumed.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Polling reads the current state of the action.
- B: _input can see events before a button uses them.
- C: Handled events stop propagating.
- D: _input comes first, and _unhandled_input gets what is left.
- E: Gameplay code there ignores a click that a button consumed.

**Source:** Input callbacks and the GUI

## MA-ch01.15

A level has twelve guard nodes in several scenes, and an alarm must put them on alert. A developer proposes a group named guards. Check each statement that is true about groups. Each statement is worth 1 point (5 points total).

- [ ] A. Using a group means the alarm code keeps a list of guard references by hand.
- [ ] B. A group is a name tag, and adding a node to it does not change its parent.
- [ ] C. A group is a node type.
- [ ] D. A node can belong to more than one group.
- [ ] E. One call on the scene tree can call a method on each member of a group.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Avoiding a hand-kept list is the purpose of a group.
- B: The nodes stay where they are in the tree.
- C: A group is a label, not a type of node.
- D: A guard can also be in an enemies group.
- E: A group call addresses the members together.

**Source:** Groups

## MA-ch01.16

A project registers a script as an autoload and a developer inspects the live scene tree during play. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An autoload is added after the main scene has finished loading.
- [ ] B. An autoload is freed and recreated when the current scene is replaced.
- [ ] C. A script has no way to refer to an autoload by the name it was registered with.
- [ ] D. An autoload node is a child of the root, added before the main scene is loaded.
- [ ] E. An autoload is safe to remove with queue_free at runtime.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: Autoloads are loaded before the main scene.
- B: An autoload persists across scene changes.
- C: A GDScript can use the registered name.
- D: Autoloads come first, with the current scene added after them.
- E: Freeing an autoload at runtime can crash the engine.

**Source:** Autoloads

## MA-ch01.17

A script calls get_node("UI/Panel/ScoreLabel") inside _process, so the lookup runs on each frame. Check each statement that is true about node paths. Each statement is worth 1 point (5 points total).

- [ ] A. A hard-coded path keeps working after a node on that path is renamed.
- [ ] B. get_node on a path that leads nowhere returns an empty node and reports no error.
- [ ] C. Storing the reference in a variable once the node is ready avoids repeating the lookup.
- [ ] D. A relative path starts at the calling node, and an absolute path starts at the root with a slash.
- [ ] E. A unique name set on a node lets %Name reach it from within its scene, wherever it sits.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Paths break when a node on the path is renamed or moved.
- B: An invalid path gives an error and a null result.
- C: Caching the reference is the usual practice.
- D: The leading slash marks an absolute path.
- E: A unique name is a lookup that does not depend on position.

**Source:** Node paths and unique names

## MA-ch01.18

A bullet node must be removed when it hits a wall. Check each statement that is true about freeing nodes. Each statement is worth 1 point (5 points total).

- [ ] A. queue_free queues the node for deletion at the end of the current frame.
- [ ] B. free deletes the object at once, so older references to it become invalid.
- [ ] C. Freeing a node leaves its children behind in the tree.
- [ ] D. Calling queue_free twice on one node is an error.
- [ ] E. After queue_free the node's other callbacks stop in the same frame.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: The node can still be accessed until then.
- B: Immediate deletion can leave dangling references.
- C: Freeing a node also frees its children.
- D: Repeating queue_free is safe.
- E: Deletion happens at the end of the frame.

**Source:** queue_free and free

## MA-ch01.19

A developer tells an agent: "Spawn a bullet when the player fires." Check each statement that is true about the terms in a precise version. Each statement is worth 1 point (5 points total).

- [ ] A. A bullet added under the level root moves in the player's local space.
- [ ] B. A PackedScene is a loaded scene resource that can be instantiated.
- [ ] C. Instantiating creates nodes that are not in the scene tree until they are added as a child of a node that is.
- [ ] D. A child inherits its parent's transform, so a bullet added under the player moves with the player.
- [ ] E. An instance that was not added to the tree still runs its _ready.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Under the level root, the bullet moves in the level's space.
- B: A PackedScene is the loaded form of a scene file.
- C: add_child is the step that puts the nodes in the tree.
- D: Transforms are inherited down the hierarchy.
- E: Callbacks run when the node enters the tree.

**Source:** Instantiate, add_child, transform

## MA-ch01.20

A coin script runs get_parent().get_parent().add_score(10), and it breaks in a level with a different tree layout. Check each statement that is true about the terms in the redesign. Each statement is worth 1 point (5 points total).

- [ ] A. To emit a signal is to register a function that will be called.
- [ ] B. A coin that emits a collected signal does not need to know who listens.
- [ ] C. A script that reaches two parents up is tightly coupled to the layout of the tree.
- [ ] D. Connecting a function to a signal can be done in the editor or in code.
- [ ] E. Signals carry information down the tree and calls carry it up.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Emit sends the signal and connect registers the function.
- B: The emitter is decoupled from its listeners.
- C: The script works only where the ancestors are arranged as expected.
- D: Both ways make a connection.
- E: The usual advice is the other way round: call down, signal up.

**Source:** Emit, connect, coupling

## MA-ch01.21

An agent moves a node with position.x += 5 in _process and loads a settings file in _process. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The fixed-step callback suits physics-driven movement.
- [ ] B. delta is the time since the previous frame or tick.
- [ ] C. Loading a settings file once is one-time setup that belongs in _process.
- [ ] D. Adding a fixed amount in _process makes speed depend on the frame rate.
- [ ] E. Multiplying a per-second speed by delta gives movement that is independent of the frame rate.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: A constant step gives stable physics.
- B: Delta is the length of the last step.
- C: One-time setup belongs in _ready.
- D: More frames per second means more distance per second.
- E: Scaling by delta ties movement to real time.

**Source:** Delta, frame-rate independence

## MA-ch01.22

A designer wants enemy stats in a shared Resource with exported fields. Check each statement that is true about when values arrive. Each statement is worth 1 point (5 points total).

- [ ] A. A Resource slot shared by several enemies holds separate copies automatically.
- [ ] B. _ready fails to read the values that were set in the Inspector.
- [ ] C. Exported values are assigned after _init has run and before _ready.
- [ ] D. A custom Resource extends the Resource type and is saved as a file.
- [ ] E. _init sees the values that were set in the Inspector.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Users of one loaded resource share one object.
- B: _ready can read the designer's values.
- C: Editor values are applied between construction and ready.
- D: A custom Resource is a data file defined by a script.
- E: _init sees only the defaults from the script.

**Source:** Export timing, custom Resource

## MA-ch01.23

Players on an AZERTY keyboard say WASD movement feels wrong, and clicking Resume on a pause menu also fires a shot. The agent read key labels directly and handled the mouse in _input. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A binding by printed label keeps the same key positions on other layouts.
- [ ] B. Handling fire in _unhandled_input receives just the events that no Control consumed.
- [ ] C. A binding by physical key position keeps the WASD hand shape on other layouts.
- [ ] D. Handling fire in _input lets the gameplay code see a click that the Resume button also uses.
- [ ] E. A precise instruction can leave out which callback handles the mouse event.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A labelled binding follows the character to a new position.
- B: _unhandled_input is for gameplay events left after the GUI.
- C: Physical bindings refer to location.
- D: _input comes before the GUI.
- E: The callback decides the order, so a precise instruction names it.

**Source:** Physical versus labelled keys, input callbacks

## MA-ch01.24

A game needs an alarm that reaches the guards, a score that survives a scene change, and a door that opens when its lock child is picked. Check each statement that is true about choosing a mechanism. Each statement is worth 1 point (5 points total).

- [ ] A. A score kept in a node of the level scene survives the change to a game-over scene.
- [ ] B. A signal lets a child announce an event without knowing its parent.
- [ ] C. An autoload is a node that persists across scene changes, which suits a score.
- [ ] D. A misspelled group name raises an error at the call.
- [ ] E. A group addresses many nodes by a shared tag.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Nodes of the level are freed with the level.
- B: The child stays reusable.
- C: An autoload is not freed with the scene.
- D: A misspelled group name silently matches nothing.
- E: A call on the group reaches each member.

**Source:** Group, autoload or signal

## MA-ch01.25

An agent summarised Godot behaviour in several claims. Check each statement that is a correct claim. Each statement is worth 1 point (5 points total).

- [ ] A. queue_free removes the node at the end of the frame, and the node can be used until then.
- [ ] B. _ready is called once for a node unless it is requested again.
- [ ] C. @export var speed stores one value in the script that the instances share.
- [ ] D. Emitting a signal with no listeners raises an error.
- [ ] E. An autoload is recreated when the current scene is replaced.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Deletion is deferred to the end of the frame.
- B: _ready follows the node entering the tree.
- C: Each instance can carry its own exported value.
- D: An emit without connections calls nothing.
- E: An autoload persists.

**Source:** Checking claims about Godot behaviour
