# Engine vocabulary (Godot, Unity, Unreal)

## MA-vocab.1

Candidates for a game-programming job are asked what the words scene, level and map mean in the three big engines. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Unity, more than one scene can be open at the same time, which is called additive loading.
- [ ] B. In Unity, "scene" means a reusable object that is instanced many times, in the way a prefab is.
- [ ] C. A Godot scene can be a single weapon, a character or a whole level, so "scene" does not mean "one screen of the game".
- [ ] D. In Godot, "level" is a special engine type that is different from a scene.
- [ ] E. In Unreal, a level is a saved map that holds the Actors placed in one part of the world.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Additive loading opens a scene on top of the scenes already open, which is how levels are built from several parts.
- B: A Unity scene is a container of GameObjects for a level or screen; the reusable, instanced object is the prefab.
- C: A Godot scene is a saved tree of nodes of any size, which is why one mechanism serves small objects and whole levels.
- D: Godot has no separate level type; a level is a scene, usually one that instances smaller scenes.
- E: In Unreal the level (map) file stores the Actors placed in it.

**Source:** Scene, level and map

## MA-vocab.2

Engines package a reusable game object once and then place many copies of it. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Unreal, a Blueprint class is an asset that defines a custom Actor type, and each Actor placed in a level from it is an instance of that class.
- [ ] B. In Unity, a prefab is an asset that serves as a template, and each copy placed in a scene is a prefab instance linked to that asset.
- [ ] C. In Unity, a scene and a prefab are the same kind of asset, so loading a prefab replaces the current level.
- [ ] D. In Godot, a saved scene can be instantiated inside another scene, so one mechanism covers a whole level and a reusable object such as an enemy.
- [ ] E. In Unity, a prefab instance in a scene and the prefab asset are one object, so deleting the instance from the scene deletes the asset file.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: A Blueprint class is the definition; each placed copy is an instance of that class.
- B: The prefab asset is the template; instances in scenes are linked copies of it.
- C: Scenes and prefabs are different asset types; opening a prefab does not replace the level.
- D: In Godot a scene file is both the level format and the reusable-object format, and scenes nest.
- E: The instance is a separate object in the scene; removing it leaves the asset untouched.

**Source:** Instance, prefab and blueprint class

## MA-vocab.3

A developer working in a Godot project types to a coding agent: "Make the coin a prefab and spawn ten of them along the track." (Prefab is a Unity word.) Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A Godot scene plays the role a prefab plays in Unity, so the agent can read "prefab" as "a saved scene that is instanced".
- [ ] B. Spawning ten coins means making one coin node and ten references to it, so the ten share a single position.
- [ ] C. Instantiating the coin's loaded scene ten times gives ten separate node trees, each of which can be given a different position.
- [ ] D. Godot has a built-in prefab file type, and the agent has to create one before it can spawn a coin.
- [ ] E. After instantiate has been called, the coin runs in the game even if it has not been added as a child of a node.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: A saved Godot scene is the reusable template that Unity calls a prefab, so the word translates.
- B: Each instance is a separate node with its own position; references to one node would be the same object.
- C: Each call to instantiate produces a fresh, independent tree of nodes.
- D: Godot has no prefab file type; the scene file is the mechanism.
- E: An instance becomes part of the running game after it is added as a child in the scene tree.

**Source:** Translating engine words in an instruction

## MA-vocab.4

An enemy template (a Unity prefab, an Unreal Blueprint class or a Godot scene) is instanced 50 times in a level. On 3 instances the developer sets a different move speed on the instance itself. Later the developer changes the move speed default in the template. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An override is a value stored on the instance, and the new template default replaces it.
- [ ] B. Instances are unlinked copies made at placement time, so later edits to the template do not reach them.
- [ ] C. The instances whose speed was left at the template value follow the new default.
- [ ] D. The 3 instances with their own speed value keep it, because an override on an instance wins over the template's default.
- [ ] E. Adding a new child object or component to the template shows up in the instances without editing them one by one.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: An override is stored on the instance, so a change to the default does not replace it.
- B: Instances stay linked to the template in all three engines; that link lets edits flow to them.
- C: A property that is not overridden keeps following the template's value.
- D: The override is the instance-level value, and it wins over the default until it is reverted.
- E: Structural changes made to the template, such as an added child node or component, appear in its instances.

**Source:** Overrides on instances

## MA-vocab.5

A candidate is asked how objects get behaviour in each of the three engines. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Unreal, the base Actor Component type carries a transform and can be attached to other components in a hierarchy.
- [ ] B. In Unreal, an Actor can be placed in a level or spawned during play, and its location, rotation and scale come from its root component.
- [ ] C. In Godot, the idiom for giving one object several unrelated abilities is to attach several components to a single node, as with Unity's GameObjects.
- [ ] D. In Unity, a GameObject has a Transform, and rendering, physics and scripts are added to it as components.
- [ ] E. In Unity, a GameObject that holds scripts can exist without a Transform, because the Transform is added when something needs a position.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Transform and attachment belong to Scene Components; the plain Actor Component has no place in the world.
- B: An Unreal Actor has no transform of its own; it takes one from its root component.
- C: Godot builds behaviour by arranging nodes in a tree and instancing scenes; its nodes are not components in the Unity sense.
- D: A GameObject has a Transform, and other behaviour comes from components.
- E: A GameObject has a Transform from the moment it exists.

**Source:** Node, GameObject, Actor and component

## MA-vocab.6

Games label objects so that code can find or filter them, such as all enemies. Engines give those labels different rules. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Godot, a group is a collision rule that decides which objects touch each other, so joining a group changes what a node can hit.
- [ ] B. In Unity, a GameObject has one tag, so one object carries a single tag and not both "Enemy" and "Flying" at the same time.
- [ ] C. In Godot, a node can belong to several groups, and the scene tree can list a group's members or call a method on them.
- [ ] D. Adding a group or tag to an object helps code look it up; by itself it changes neither how the object looks nor how it moves.
- [ ] E. In Unity, a GameObject's tag and its layer are two names for the same property, so setting one sets the other.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Collision filtering uses layers and masks; groups are lookup labels.
- B: Unity gives a GameObject a single tag (and a single layer).
- C: Groups work like tags with many allowed per node, and the scene tree can query them.
- D: A lookup label has no built-in effect on rendering or physics.
- E: Tags and layers are separate properties; layers drive filtering such as rendering and physics, tags are for lookup.

**Source:** Groups, tags and layers

## MA-vocab.7

A designer wants a health bar to float 40 units above an enemy's head, follow the enemy as it walks and turns, and still be right when the enemy is scaled up to be a boss. The bar is made a child of the enemy. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A local position of (0, 0) places the child at the world origin.
- [ ] B. The bar's local position is measured relative to its parent, so a fixed local offset of 40 units up stays the same while the bar's world position changes as the enemy walks.
- [ ] C. When the parent is rotated, the engine rotates the child's local offset with it, so the bar swings around the enemy.
- [ ] D. When the parent is scaled up, the child's local offset is scaled with it, so the bar sits farther away unless scale inheritance is handled.
- [ ] E. World (global) space measures positions from the parent object's own origin.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A local position of (0, 0) is the parent's own origin, wherever the parent is in the world.
- B: A local position is stored relative to the parent and does not change when the parent moves.
- C: The world position is built from the chain of parent transforms, including rotation.
- D: Parent scale applies to the child's offset, so a boss at scale 2 puts the bar twice as far away.
- E: World space is measured from the world origin; local space is measured from the parent.

**Source:** Local versus world space

## MA-vocab.8

A developer tells a coding agent: "Raise the platform by 100 units." The agent edits position values in three engines. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Unreal, y is the up axis, so raising an Actor means increasing its y.
- [ ] B. In Unreal, positive z points up, so raising an Actor means increasing its z.
- [ ] C. In Unity the up axis is y, with positive y pointing up, so decreasing a GameObject's y raises it.
- [ ] D. In Godot's 2D space the y axis points down the screen, so raising a 2D node means decreasing its y position.
- [ ] E. Unity and Unreal use the same real-world length for one unit by default, so "100 units" is the same distance in both.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: Unreal's up axis is z, not y.
- B: Unreal is z-up, so increasing z raises the Actor.
- C: In Unity positive y is up, so decreasing y lowers the object.
- D: Godot 2D uses screen-style coordinates in which y grows downward.
- E: Unity treats a unit as a metre by convention, while Unreal treats a unit as a centimetre, so "100 units" differs.

**Source:** Up axis, y-down and units

## MA-vocab.9

A developer tells a coding agent: "Move the player to where I click." In a 2D game the click arrives as a position inside the viewport, and the camera may be moved or zoomed. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The raw click position is a screen (viewport) coordinate, and the agent can treat it as the same thing as a world coordinate.
- [ ] B. When the camera is panned or zoomed, the same screen position corresponds to a different world position.
- [ ] C. Screen coordinates are measured in the viewport, usually from its top-left corner, while world coordinates locate a point in the game world.
- [ ] D. A precise instruction asks the agent to convert the click from screen coordinates to world coordinates through the camera, then move the player to that world position.
- [ ] E. The camera has no role in relating screen space to world space.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Screen and world coordinates are different spaces, and a conversion is needed.
- B: The camera defines the mapping, so moving or zooming it changes which world point sits under a screen position.
- C: Screen space belongs to the display, and world space belongs to the game world.
- D: Naming both spaces and the conversion removes a guess that would put the player in the wrong place.
- E: The camera is what relates the two spaces.

**Source:** Screen space versus world space

## MA-vocab.10

Check each statement about frames, ticks and delta time. Each statement is worth 1 point (5 points total).

- [ ] A. A tick is one update step of a subsystem such as physics, while a frame is one pass of the main loop ending in a rendered image, so the counts can differ.
- [ ] B. In Godot, the delta passed to the physics callback follows the fixed physics rate, so it does not stretch when a rendered frame takes longer than usual.
- [ ] C. Frame rate is the number of fixed physics steps that run each second, which is why the two numbers match.
- [ ] D. The delta passed to a per-frame callback is a fixed 1/60 s, because 60 frames per second is the standard rate games are built for.
- [ ] E. Delta time is the time elapsed since the previous call of the update callback, usually measured in seconds.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: Physics ticks and rendered frames are counted separately and need not be equal.
- B: Godot's physics callback runs at a fixed rate, and its delta follows that rate.
- C: Frame rate counts rendered frames per second; the fixed-step rate is a separate setting.
- D: The per-frame delta varies with how long each frame took on that machine.
- E: Delta is the elapsed time between consecutive calls, which lets movement scale with real time.

**Source:** Frame, tick and delta time

## MA-vocab.11

A developer asks a coding agent: "Make the enemy move right 5 pixels every frame." The agent writes position.x += 5 in the per-frame update function, and the game is tested on a 60 Hz screen and a 144 Hz screen. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Delta time is the count of frames drawn in the last second.
- [ ] B. position.x += 5 is movement per frame, so the enemy covers more distance per second when more frames are drawn each second.
- [ ] C. Movement of 5 pixels per frame is frame-rate independent, so the enemy looks the same speed at 60 and at 144 frames per second.
- [ ] D. Asking for "move right at 300 pixels per second" and writing position.x += 300 * delta gives the same on-screen speed at 60 and at 144 frames per second.
- [ ] E. Multiplying a step by delta changes its unit from "per frame" to "per second", so the number 5 may need to be raised to keep the old speed.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Delta time is a duration in seconds, not a count of frames.
- B: A fixed step per frame makes speed depend on the number of frames per second.
- C: A per-frame step is the textbook example of movement that is not frame-rate independent.
- D: A rate in units per second scaled by the time per frame covers the same distance per second at any frame rate.
- E: With delta, the number is a rate per second, so a per-frame value needs converting.

**Source:** Frame-rate independence

## MA-vocab.12

An interviewer asks why movement that involves the physics engine belongs in the fixed-step callback (Unity's FixedUpdate, Godot's _physics_process) and not in the per-frame callback (Update, _process). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Putting movement in the fixed-step callback makes the on-screen frame rate constant.
- [ ] B. In Godot, the physics callback is the right place for cosmetic effects such as a flickering light, because it runs more often than the per-frame callback.
- [ ] C. The physics engine advances the world in fixed-size steps, so forces and velocities applied in the callback tied to that step line up with the simulation.
- [ ] D. Gravity, forces and body movement belong in the fixed-step loop, while camera smoothing and UI animation belong in the per-frame loop.
- [ ] E. Physics driven by the variable per-frame delta depends on how fast the machine renders, so the same input can give different jump arcs on different machines.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Frame rate depends on rendering and load; the fixed step only decouples physics from it.
- B: The physics callback runs at its own fixed rate, which can be lower or higher than the frame rate; cosmetic effects belong in the per-frame callback.
- C: Fixed-size steps keep the simulation's time unit constant.
- D: Visual smoothing follows the rendered frames, while physics follows the fixed step.
- E: A varying step makes collisions and jump heights less repeatable between machines.

**Source:** Update loop versus fixed-step loop

## MA-vocab.13

A game's fixed-step callback is set to a constant rate, and rendering is not capped. When a frame takes long, the engine runs extra fixed steps to catch up. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. After a frame that lasted several times the step length, the engine runs several fixed steps to catch up.
- [ ] B. When frames are shorter than the step length, some rendered frames run no fixed step.
- [ ] C. When the frame rate rises, the length of the fixed step shrinks so that each step lines up with one frame.
- [ ] D. Each catch-up call of the fixed-step callback receives the delta of the whole long frame.
- [ ] E. The fixed-step callback runs once per rendered frame, so the two loops alternate one to one.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: The engine accumulates elapsed time and spends it in whole fixed steps.
- B: On short frames the accumulated time has not yet reached a full step.
- C: The step length is a setting and does not change with the frame rate.
- D: Each call receives the constant step length; several calls together cover the long frame.
- E: The two loops run at independent rates, so they do not alternate one to one.

**Source:** Fixed-step catch-up

## MA-vocab.14

A scene holds 2000 enemies, and each runs a per-frame update that checks whether the player is near. A developer asks an agent to cut that cost. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Reacting to an event costs more per frame than polling for idle objects.
- [ ] B. Switching off the per-frame callback on idle enemies removes their polling cost until they are switched back on.
- [ ] C. Event-driven code runs when something happens, so idle objects add nothing per frame.
- [ ] D. Polling checks a condition on each update even when nothing has changed, so its cost grows with the number of objects.
- [ ] E. Polling and event-driven are two names for the same technique.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: An event has no per-frame cost for idle objects.
- B: An object without a per-frame callback pays nothing for it.
- C: Events invoke code at the moment of change.
- D: Polling repeats the same check at the update rate whether or not the answer changed.
- E: Polling asks again and again; an event is pushed when the change occurs.

**Source:** Polling versus event-driven cost

## MA-vocab.15

Most engines give an object a hook that runs once when it is ready to be used (Godot's _ready, Unity's Start, Unreal's BeginPlay) and a hook that runs repeatedly (Godot's _process, Unity's Update, Unreal's Tick). Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A hook that runs one time is unsuitable for starting a looping timer, because the hook does not repeat.
- [ ] B. In Godot, _ready is called again each time a node is removed from the scene tree and added back.
- [ ] C. A per-frame hook is the right place to build the player's starting inventory, because it keeps retrying until it succeeds.
- [ ] D. In Godot, children's _ready callbacks run before the parent's, so the parent can rely on its children being set up.
- [ ] E. In Unity, Start is called before the script's first frame update, and when the script instance is enabled.

**Key:** A=F B=F C=F D=T E=T

**Why:**

- A: A once-only hook can start a repeating process; it starts it once.
- B: _ready is called once per node unless it is explicitly requested again.
- C: Setup in a per-frame hook repeats each frame or needs a guard flag; setup belongs in the once-only hook.
- D: Children are ready first, then the parent.
- E: Start runs before the first frame update for an enabled script.

**Source:** Start hook versus per-frame hook

## MA-vocab.16

Godot calls it a signal, Unity programmers use C# events or UnityEvent, and Unreal has delegates and Event Dispatchers. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Signals, events and delegates hold the message in a queue until each listener checks it once per frame.
- [ ] B. In Godot, emitting a signal that nothing is connected to is not an error; it calls nothing.
- [ ] C. In the three engines, the code that announces an event does not need to name the objects that react to it.
- [ ] D. In Godot, a listener can connect to a signal on a node it has a reference to; a parent and child relationship is not required.
- [ ] E. A callback is a function that a listener hands over so the announcing object can call it when the event happens.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Listeners are called by the announcer when the event happens; a Godot signal calls connected functions immediately unless deferring is requested.
- B: An empty list of listeners is legal; emitting then does nothing.
- C: Listeners register themselves, so the announcer stays unaware of who is listening.
- D: A connection links a signal to a callable on any object; the tree layout does not restrict it.
- E: The callback is the function passed to the signal, event or delegate.

**Source:** Signal, event, delegate and callback

## MA-vocab.17

A developer wants the health bar (HUD) to redraw when the player takes damage. The requirements for the coding agent are that the player's code does not need to know the HUD exists and the HUD does not check the player every frame. A statement is true when the request it quotes meets both requirements. Each statement is worth 1 point (5 points total).

- [ ] A. "Have the player emit a health-changed signal, and have the HUD connect to it and redraw in the handler."
- [ ] B. "Give the player a reference to the HUD and have the player call the HUD's redraw function when it takes damage."
- [ ] C. "In the HUD's per-frame update function, read the player's health and redraw if it changed."
- [ ] D. "Store health in a global variable that the player writes and the HUD reads in its per-frame update function."
- [ ] E. "Have the HUD declare a signal, and have the player connect to it and emit it whenever health changes."

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: The player announces the change and the HUD listens, so neither requirement is broken.
- B: A direct call needs the player to hold a reference to the HUD, which breaks the first requirement.
- C: Reading the health in a per-frame update is polling, which breaks the second requirement.
- D: The HUD still polls the shared value, which breaks the second requirement.
- E: The player would have to reference the HUD to connect to its signal, which breaks the first requirement.

**Source:** Signals versus polling and direct calls

## MA-vocab.18

A Unity script subscribes one of its methods to a C# event on a long-lived manager object. The script's GameObject is later destroyed without the script unsubscribing. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Event systems keep weak references to subscribers, so a long-lived emitter drops a destroyed subscriber without an unsubscribe call.
- [ ] B. The usual remedy is symmetrical: subscribe when the object is enabled and unsubscribe when it is disabled or destroyed.
- [ ] C. The engine queues the event until the next frame, by which time the destroyed object has been cleaned up and no error follows.
- [ ] D. The manager's list of subscribers still holds the destroyed script's method, so the next time the event is raised a call can be made on an object that no longer exists.
- [ ] E. In Godot, when a node whose method is connected to a signal is freed, the engine removes that connection.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: A C# event holds a normal reference to each subscriber, so a missing unsubscribe causes stale calls.
- B: Pairing subscribe and unsubscribe with enable and disable (or destroy) is the standard discipline.
- C: A C# event calls its subscribers in the line that raises it; nothing is queued.
- D: A stale subscription stays in the list and is called on the next raise.
- E: Godot removes the connections of a freed object.

**Source:** Event lifetime and unsubscribing

## MA-vocab.19

A studio interview asks why engines offer input actions instead of letting game code read raw keys. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Unity's Input System actions, Unreal's Enhanced Input actions and Godot's Input Map actions are three engine-specific forms of the same idea.
- [ ] B. Polling and an event callback are the same thing: both push a message to the code when the input occurs.
- [ ] C. Hard-coding a check for the Space key in the movement code is the preferred way to support rebinding.
- [ ] D. Because game code asks about the action, a player can rebind the key without game code changing.
- [ ] E. An input action is a named intent, such as "jump", mapped to one or more physical inputs like a keyboard key or a gamepad button.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Each engine maps named actions to bindings under different names and tools.
- B: Polling reads state when asked; an event callback is pushed to the code when the input happens.
- C: A hard-coded key defeats rebinding and ties the code to one device.
- D: Rebinding changes the mapping, not the code that reads the action.
- E: The action is the game-level meaning, and bindings tie it to devices.

**Source:** Input action versus raw key

## MA-vocab.20

A designer wants jumping to happen once per button press and running to continue while a button is held. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A just-pressed query stays true for the whole time the button is held.
- [ ] B. A just-pressed query is true on the frame or tick the press began, which fits a one-shot jump.
- [ ] C. A precise version defines an action named jump bound to the Space key and a gamepad button, reacts once per press, and defines a separate run action read as a held state.
- [ ] D. "Jump when the player presses space" is a precise instruction, because it names the key.
- [ ] E. A held-state query, true for as long as the button is down, fits the run control.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: That describes a held state; just-pressed is true on a single frame or tick.
- B: A just-pressed query fires once per press.
- C: It names the action, the bindings and the query type for each control.
- D: It hard-codes one key and one device, and does not say whether holding repeats the jump.
- E: Running continues while the input is down, so a held state fits.

**Source:** Just-pressed versus held; precise input instruction

## MA-vocab.21

Developers use "asset" and "resource" loosely. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. In Godot, a Resource and a Node are interchangeable: both can be placed in the scene tree and both receive the per-frame callback.
- [ ] B. A Godot Resource is a data container that does nothing on its own; nodes use resources to do their work.
- [ ] C. In Godot, loading the same resource path twice returns two independent copies, so changing one does not affect the other.
- [ ] D. An asset, in the everyday sense, is a file in the project folder such as a PNG, a WAV or a mesh, which the engine imports before using it.
- [ ] E. Unity's ScriptableObject and Unreal's Data Asset fill a similar role: a data asset that many objects can read, independent of an object in a level.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Nodes live in the scene tree and get per-frame callbacks; a resource is data.
- B: A Resource is data; behaviour comes from nodes.
- C: Loading a resource that is already in memory returns the same copy.
- D: Source files are imported by the editor, and the engine uses the imported form at runtime.
- E: Both are data assets that exist independently of objects in a level, though they are not identical features.

**Source:** Asset versus resource

## MA-vocab.22

A game keeps the player's inventory in one globally reachable object: a singleton in Unity, an autoload in Godot, or an object held by the persistent Game Instance in Unreal. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Such an object is useful because it outlives a single scene or level, so what it stores survives scene changes.
- [ ] B. Registering a script as an autoload makes the engine refuse to create a second copy of it, which makes it a true singleton.
- [ ] C. In Godot, replacing the current scene frees the autoload nodes too, and they are recreated for the new scene.
- [ ] D. In Unity, an object survives a scene load when it is explicitly marked to be kept, for example with DontDestroyOnLoad.
- [ ] E. Because code can reach it from anywhere, a function that quietly reads the global is harder to test alone than one handed the inventory as a parameter.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Lifetime beyond the current scene is the reason to put shared state in such an object.
- B: An autoload is still an ordinary node that could be instanced again; the engine does not enforce a single copy.
- C: Autoloads stay loaded whichever scene is running.
- D: Unity destroys the objects of the replaced scene unless they are marked to survive.
- E: A hidden dependency on a global makes a function depend on state its signature does not show.

**Source:** Singleton and autoload

## MA-vocab.23

A developer asks a coding agent for "a global score counter" in a Godot game that has a title scene, a level scene and a game-over scene. The agent puts the counter in a script on the root node of the level scene, and the score reads zero on the game-over scene. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Passing the score to the next scene as the scenes are switched is a way to avoid a global.
- [ ] B. Registering the script as an autoload would keep it alive from startup through each scene change.
- [ ] C. The score variable was freed along with the level scene's nodes when the game switched scenes.
- [ ] D. Marking the variable with @export keeps its value when the game switches scenes.
- [ ] E. The cause is that GDScript resets number variables to zero when a new scene is loaded.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: The vague word "global" hid a design choice; handing the value on is a legitimate alternative.
- B: An autoload is a node placed under the root before the main scene and kept through scene changes.
- C: A variable lives as long as the node it belongs to, and the level scene's nodes were removed.
- D: @export exposes a variable to the editor; it does not extend its lifetime.
- E: GDScript does not reset variables; the object holding the variable was removed.

**Source:** Say "autoload", not "global"

## MA-vocab.24

Check each statement about the editor, a running game and a built (exported or packaged) game. Each statement is worth 1 point (5 points total).

- [ ] A. Producing a standalone game is a separate step from running it in the editor, and engines name that step export, build or package.
- [ ] B. Code written to extend the editor, such as Unity code in the UnityEditor namespace, is absent from a built player.
- [ ] C. A game that runs correctly from the editor runs the same in a built version, so testing the build adds little.
- [ ] D. In Godot, export templates, the prebuilt runtime for each target platform, have to be installed before a project can be exported.
- [ ] E. In Unity, edits made to scene objects in Play mode are kept when Play mode stops.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Running in the editor and producing a standalone game are different steps with engine-specific names.
- B: Editor-only code does not exist in the player.
- C: Builds can differ from editor runs in included files, platform settings and performance.
- D: Export templates supply the runtime for each target platform.
- E: Changes made in Play mode are discarded when it ends.

**Source:** Editor, runtime and build

## MA-vocab.25

A developer tells a coding agent: "Ship the game to my tester." The agent starts the project from the command line, sees it run, and reports it is done. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The tester needs the editor installed to open an exported game.
- [ ] B. A precise instruction names the export (or build, or package) step and the target platform, and asks for the built artifact to be launched and checked.
- [ ] C. "Ship" is the engines' own name for the export step, so the instruction is precise.
- [ ] D. Running the project from the command line produces a standalone file the tester can open without the engine.
- [ ] E. An export includes the files its settings select, so a file that loads in the editor can be missing from the build.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: A built game is meant to run without the editor.
- B: Naming the step, platform and check removes the guesses.
- C: Engines say export, build or package; "ship" leaves the step and the target open.
- D: Running a project launches it with the engine and creates no standalone game.
- E: The editor reads the project folder directly, while an export contains selected files.

**Source:** Ship, run and export

## MA-vocab.26

A developer gives a coding agent this instruction: "Add a global thing so the enemies chase the player every frame at speed 4." Check each statement that is true about the wording. Each statement is worth 1 point (5 points total).

- [ ] A. "Each frame" is precise, because it fixes how fast the enemies move on screen.
- [ ] B. A better version asks for movement toward the player at a stated rate in units per second, with the step scaled by delta in the per-frame callback.
- [ ] C. "Speed 4" has no unit and no time base, so it could mean 4 units per frame or 4 per second.
- [ ] D. "Global thing" does not say whether the object is a script on a level node, a manager node or an autoload that survives scene changes.
- [ ] E. Replacing "global thing" with "global variable" makes the location and lifetime precise.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A per-frame step makes speed depend on the frame rate.
- B: A rate per second scaled by delta is frame-rate independent.
- C: A number without unit and time base leaves the real speed to the agent.
- D: The location and lifetime of shared state change what happens at a scene change.
- E: "Global variable" is as vague about location and lifetime as "global thing".

**Source:** Vague request rewrite: frame-rate independence and global state

## MA-vocab.27

A level contains 30 copies of a crate. The designer wants the crates in one corner to be heavier, and wants every crate to play a new sound when hit. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The 30 crates are unrelated hand-made copies that share a name.
- [ ] B. Adding the sound to the template once gives it to the 30 instances without editing them one by one.
- [ ] C. Changing the weight on the corner instances alone creates an override, a value stored on the instance rather than in the template.
- [ ] D. If the template's default weight is changed later, the overridden crates keep their own weight until the override is reverted.
- [ ] E. To make the corner crates heavier, the designer edits the template's weight.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Instances are linked to one template and are not unrelated copies.
- B: A change to the template reaches its linked instances.
- C: An override is the instance-level value.
- D: Overrides persist until they are reverted, while the other instances follow the default.
- E: Editing the template would make every crate heavier, not just the corner ones.

**Source:** Template, instance and override

## MA-vocab.28

A developer who knows Unity starts working on Godot and Unreal projects. Check each statement that is true about how Unity terms map to the other engines. Each statement is worth 1 point (5 points total).

- [ ] A. A C# event corresponds to a Godot autoload.
- [ ] B. A Godot scene does the work of both a Unity scene and a Unity prefab.
- [ ] C. An agent told to "do it the Unity way" in Godot can add components to a node in the same way as to a GameObject.
- [ ] D. Unity's ScriptableObject corresponds roughly to a Godot Resource and to an Unreal Data Asset.
- [ ] E. Unity's FixedUpdate corresponds roughly to Godot's physics callback.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: A C# event matches a Godot signal or an Unreal delegate; an autoload matches a singleton.
- B: A Godot scene is both the level format and the reusable-object format.
- C: Godot nodes are not Unity components, so a literal translation builds something Godot does not use.
- D: All three are data assets independent of objects in a level.
- E: Both run at a fixed rate for physics work.

**Source:** Cross-engine vocabulary mapping

## MA-vocab.29

A game has a player, a HUD, an audio manager and an achievement system, and the four have to react when the player picks up a coin. A junior developer makes the coin script call each of the four directly. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A direct call is the better choice when a parent commands a child it owns, or when a return value is needed.
- [ ] B. A redesign has the coin emit a "coin collected" signal, and each system connects its own callback.
- [ ] C. Events suit asking another object for an answer, because they return a value to the emitter.
- [ ] D. Direct calls couple the coin to the four systems: it needs a reference to each and changes when a system is added or removed.
- [ ] E. With signals, the emitter has to name its listeners when it emits.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: A direct call fits a single known target and a needed return value.
- B: The emitter announces what happened and each listener registers itself.
- C: Events announce what already happened; they are not a way to ask for an answer.
- D: A direct call ties the caller to its target.
- E: Listeners register themselves, so the emitter does not name them.

**Source:** Signal, event and delegate versus direct call
