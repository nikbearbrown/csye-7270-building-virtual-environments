# CSYE 7270 terminology glossary

Every term in every deck in `decks/`, with its meaning and a tag: **in the book text** (the chapters use and explain it), **in the glossary** (a row in `interview-bank/.../GLOSSARY-jargon-midterm.md`), **editor or docs** (defined by the engine's editor or documentation), **outside source**, or **video only** (only from the course videos). Generated from the decks by `make_glossary.js`; edit the decks, not this file.

## Decks

| Deck | Slides | Terms |
|---|---|---|
| [2D art and sound assets in the engine](decks/Terms%20-%202D%20art%20and%20sound%20assets.html) | 16 | 34 |
| [Terms: Camera](decks/Terms%20-%20Camera.html) | 19 | 20 |
| [Game design A: what a game is](decks/Terms%20-%20Game%20design%20A.html) | 14 | 22 |
| [Game design B: choices and challenge](decks/Terms%20-%20Game%20design%20B.html) | 14 | 19 |
| [Game design C: pacing and guidance](decks/Terms%20-%20Game%20design%20C.html) | 15 | 19 |
| [Godot: the editor, scenes, nodes, signals and movement](decks/Terms%20-%20Godot%20editor%20and%20scenes.html) | 16 | 34 |
| [Walker and the toolchain](decks/Terms%20-%20Walker%20and%20the%20toolchain.html) | 14 | 26 |

Total: 7 decks, 174 term entries.

---

## 2D art and sound assets in the engine

[Open the deck](decks/Terms%20-%202D%20art%20and%20sound%20assets.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Resolution | Width and height in pixels. | in the glossary |
| Viewport | The area the game draws into, set in Project Settings; the window scales it. | editor or docs |
| Aspect ratio | Width divided by height. | in the glossary |
| Uniform vs non-uniform | Same factor on both axes versus different factors that distort. | in the glossary |
| Texel | One pixel of a texture. | in the glossary |
| Nearest vs linear | Nearest reads one texel and keeps hard edges; linear blends four and smooths. | in the book text |
| Integer scaling | Scaling by whole numbers so pixel art stays crisp. | in the glossary |
| Sprite sheet | One image of many frames in a grid. | in the book text |
| Texture atlas | Many small images packed into one big texture; a frame is a region of it. | in the book text |
| SpriteFrames | A Godot resource of named animations: frames, speed and a loop flag. | in the book text |
| Frame rate | Frames shown per second. | in the book text |
| Alpha channel | The extra channel storing opacity. | in the glossary |
| Transparent background | Cut the background to alpha 0; ask for a solid colour, not for transparent. | in the book text |
| PNG vs JPEG | Lossless with alpha versus lossy without alpha. | in the book text |
| Fringe (halo) | The halo of edge colour left around a cutout; fix_alpha_border removes it. | in the book text |
| Import settings | Per-asset options controlling how the engine converts it, kept in the .import file. | in the book text |
| Lossless vs lossy | Exact reconstruction versus smaller files with lost detail. | in the glossary |
| Mipmaps | Pre-shrunk copies of a texture used when drawn small; about 33% more memory. | in the book text |
| Silhouette | The outline of an object; it should still read when filled black at game size. | in the book text |
| Readability | How well a character can be understood in the game's real view. | video only |
| Collider | Shape used for contact tests; separate from the art and sized from the body. | in the book text |
| PCM | Uncompressed digital audio samples. | in the glossary |
| Sample rate | Audio samples per second. | in the glossary |
| Nyquist limit | The highest frequency a sample rate can hold: half the rate. | in the glossary |
| Procedural synthesis | Sound made by a formula evaluated sample by sample, with no file and no model. | in the book text |
| WAV vs Ogg Vorbis | WAV for short effects; Ogg Vorbis for music, speech and long sounds. | in the book text |
| Loop point | Where a looping sound jumps back to; WAV has begin and end, Ogg only a start offset. | in the book text |
| One-shot | Plays once and stops. | in the glossary |
| AudioStreamPlayer | Godot node that plays sound with no position. | in the book text |
| Polyphony | How many copies of a sound can play at once; Godot's default is 1. | in the book text |
| Bus | A channel that sounds are routed through for shared volume and effects. | in the book text |
| Decibel | Logarithmic loudness unit. | in the glossary |
| Headroom | Spare level left below the maximum. | in the glossary |
| Clipping | Distortion when a signal exceeds the maximum level. | in the glossary |

## Terms: Camera

[Open the deck](decks/Terms%20-%20Camera.html) · 19 slides · 20 terms

| Term | Meaning | Tag |
|---|---|---|
| Pan | Turn left or right on the spot; position unchanged. | in the glossary |
| Tilt | Turn up or down on the spot; position unchanged. | in the glossary |
| Roll | Spin around the viewing direction; the horizon tips. | in the glossary |
| Dolly | Move the camera forward or backward along its view direction. | in the glossary |
| Dolly in / dolly out (also dolly in/out) | Move the camera toward / away from the subject. Dolly in moves toward the subject, dolly out moves away. | in the glossary |
| Truck | Move the camera left or right, still facing the same way. | in the glossary |
| Pedestal | Move the camera straight up or down, still facing the same way. | in the glossary |
| Zoom | Change the lens (field of view or focal length); the camera does not move. | in the glossary |
| Dolly versus zoom | A dolly changes parallax (near and far shift against each other); a zoom only magnifies. | in the glossary |
| Parallax | Nearer things shift more than farther things when the viewpoint moves. | in the glossary |
| Focal length | Lens strength in millimetres; longer means narrower view and more magnification. | in the glossary |
| Orbit | Move around a subject on a curved path while keeping it framed. | in the glossary |
| Follow camera | Tracks a moving target, usually with smoothing. | in the glossary |
| Smoothing (damping) (also smoothing/damping) | Spreads the camera's catch-up over time so it trails slightly. Same idea under both names: the camera eases toward its target instead of snapping. | in the glossary |
| Deadzone | Screen region where the target can move without the camera moving. | in the glossary |
| Look-ahead | Shifts framing toward the direction of travel. | in the glossary |
| Screen shake | Brief, fading random offset of the camera for impact. | in the glossary |
| Camera limits | Clamps that keep the view inside the level. | in the glossary |
| Field of view (FOV) | The lens angle; wider shows more. | in the glossary |
| Perspective / orthographic | Distant things shrink / size does not depend on distance. | in the glossary |

## Game design A: what a game is

[Open the deck](decks/Terms%20-%20Game%20design%20A.html) · 14 slides · 22 terms

| Term | Meaning | Tag |
|---|---|---|
| Game | An activity that has all four: a goal, opposition, decisions and rules. | video only |
| Goal | The objective the player works toward. | in the glossary |
| Opposition | Obstacles the player must overcome; it makes a game fun and can frustrate. | video only |
| Decisions | The ways the player can get past the opposition. | video only |
| Rules | The framework that limits and governs the whole experience. | video only |
| House rules | Rules a group changes for its own table; they change how the game plays. | video only |
| Mechanic | A rule-governed action in the game. | in the book text |
| Player verb | An action the player can take: jump, shoot, build. | in the glossary |
| Core mechanic | The action players do over and over again. | video only |
| Core loop | The repeated moment-to-moment cycle the player enjoys. | in the glossary |
| Thematic feel | Mechanics alone can set the tone: what a thing does tells the player what it is. | video only |
| Movement pattern | How a character moves gives it personality: a hop is a frog, a wave is a snake. | video only |
| Types of fun (also Eight Kinds of Fun (Marc LeBlanc)) | "Fun" is too vague. Name the kind: fantasy, thrill, fellowship, mastery, exploration, creativity. | video only |
| Target experience | The one specific experience everyone on the team aims at. | video only |
| Appeal | The pull to keep playing; it differs by game and by player. | video only |
| Art, design, engineering | They depend on each other; results are best when all three aim at the same target. | video only |
| Space | The look, sound, lighting and physical setting; it shapes what fits in the game. | video only |
| Components | The objects in the space that players use or meet: characters, weapons, vehicles. | video only |
| Prototype | A simplified version made first to test whether the idea has appeal. | video only |
| Play testing | Letting players challenge the design so it can be revisited and improved. | video only |
| Clear progress | The player can see how close they are to the goal. | video only |
| Climactic arc | Difficulty and tension build toward the goal's resolution. | video only |

## Game design B: choices and challenge

[Open the deck](decks/Terms%20-%20Game%20design%20B.html) · 14 slides · 19 terms

| Term | Meaning | Tag |
|---|---|---|
| Meaningful play | The player acts and the game responds in a way that matters. | in the glossary |
| Descriptive play | The player acts and sees the game respond: the bola hits, the ice shatters. | in the glossary |
| Evaluative play | The player steps back and asks why this action matters to the whole game. | in the glossary |
| Meaningful choice | A choice that changes what happens and that the player has to think about. | in the glossary |
| Agency (autonomy) | The player takes control of how the game is played. | in the glossary |
| Risk versus reward | A harder or riskier action pays more, and the player weighs the factors. | in the glossary |
| Trade-off | Give up one thing to get another. | in the glossary |
| Persistence | The player lives with the consequences of a choice for a set time. | in the glossary |
| Situational choice | The same choice is better or worse depending on the situation the player is in. | in the glossary |
| Unit differentiation (also orthogonal unit differentiation) | Each enemy type does something different, which forces the player to prioritise. | in the glossary |
| Personalisation | Players build their own play style from the decisions they make. | in the glossary |
| Frustration | Some is part of challenge; it has to be the kind the player can learn from. | in the glossary |
| Difficulty | How hard the opposition is; it is separate from fairness. | in the glossary |
| Fairness | Clear expectations and consistent design, so the player can learn from failing. | in the glossary |
| Luck and skill | Luck: chance decides. Skill: the player's ability decides. Games mix the two. | in the glossary |
| Balance | Every advantage has a disadvantage; no role starts with an unfair edge. | in the glossary |
| Rock-paper-scissors | Each option beats one and loses to another, so no option wins everywhere. | in the glossary |
| Downtime | Time a player waits with nothing to do. | in the glossary |
| Probability | The odds of each result; extra rolls change them. | in the glossary |

## Game design C: pacing and guidance

[Open the deck](decks/Terms%20-%20Game%20design%20C.html) · 15 slides · 19 terms

| Term | Meaning | Tag |
|---|---|---|
| Three pillars | A game rests on the player's role, communication and appeal. | in the glossary |
| Player purpose | What the player does and why; the player, not the game, drives it forward. | in the glossary |
| Communication | Showing the player the goal and how to reach it, with clues in the environment. | in the glossary |
| Guiding the focus | Making clear what the player should concentrate on. | in the glossary |
| Linear and nonlinear | Straight from start to end, or with alternate choices along the way. | in the glossary |
| Side quest | A detour from the main storyline. | in the glossary |
| Level design | Planning and building the spaces the player moves through. | in the glossary |
| Teaching through levels | The first level lets the player try each skill, with no text. | in the glossary |
| Design the middle first | Build the engaging middle levels, then the opening levels that lead there. | in the glossary |
| Anticipation | Prepare the player for what comes next, such as a wind-up before an attack. | in the glossary |
| Build-up | A sequence that raises tension toward an event: sound, sparks, camera shake. | in the glossary |
| Logical events | Events behave sensibly and meet the player's unspoken expectations. | in the glossary |
| Consistent rules | Even where physics is bent, it is bent the same way every time. | in the glossary |
| Games can cheat | Hidden help the player does not notice, such as enemies told not to turn around. | in the glossary |
| Dynamic | Many things happening at once, so play stays fresh. | in the glossary |
| Progression | A natural rise in challenge; do not over-stimulate or under-stimulate. | in the glossary |
| Pacing | Alternating intense and calm moments. | in the glossary |
| Waves | A group of enemies sent together: many weak ones or a few strong ones. | in the glossary |
| Spacing | Open areas to admire, or tight ones that feel claustrophobic; leave room for AI. | in the glossary |

## Godot: the editor, scenes, nodes, signals and movement

[Open the deck](decks/Terms%20-%20Godot%20editor%20and%20scenes.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Scene dock, Remote tab | Lists the scene's nodes; the Remote tab lists the running game's. | in the book text |
| FileSystem dock | Lists every file in the project, under res://. | editor or docs |
| Inspector | The editor panel for viewing and editing properties. | in the glossary |
| Node dock | Shows the selected node's signals and groups. | editor or docs |
| 2D, 3D and Script views | Tabs along the top: 2D and 3D edit scenes, Script edits code. | editor or docs |
| Output and Debugger | Bottom panels: Output shows printed text, Debugger shows errors. | editor or docs |
| Project Settings | Project-wide values: physics rate, layer names, input actions, autoloads. | in the book text |
| Run and Play buttons | Run Project (F5) starts the main scene; Run Current Scene starts the open one. | editor or docs |
| Project | A folder with a project.godot file at its root; res:// means that folder. | in the book text |
| Scene | A saved, reusable tree of nodes: a level, a character, a menu. | in the book text |
| Node | The smallest building block: one object doing one job. | in the book text |
| Script | Attaches behaviour to a node; GDScript here. | in the book text |
| Scene tree | The live hierarchy of nodes in a running game. | in the book text |
| Instance | One live copy of a saved scene; a change on one instance overrides the template. | in the book text |
| _process | Runs once per rendered frame; the rate varies by machine. | in the book text |
| _physics_process | Runs at a fixed rate, 60 times a second by default. | in the book text |
| Input action | A named intent such as jump, bound to keys or buttons. | in the book text |
| Just-pressed vs held | Just-pressed is true only on the tick a press began; held stays true while down. | in the book text |
| Polling | Asking every tick whether something has happened. | in the book text |
| Event-driven | Code runs only when something announces that it happened. | in the glossary |
| Signal | A named event a node emits; other nodes connect to it. | in the book text |
| Group | A named tag on nodes; one call reaches every node in it. | in the book text |
| Autoload | A script or scene kept loaded across scene changes. | in the book text |
| Resource | A typed data container nodes share, made by extending Resource. | in the book text |
| Export preset, template | A preset is the recipe for one platform; the template is the prebuilt engine it packs your data into. | in the book text |
| Area2D | Detects overlaps and can emit signals; never blocks or pushes. | in the book text |
| StaticBody2D | Not moved by physics; others collide with it. | in the book text |
| RigidBody2D | Simulated physics: you set forces or velocity, the engine moves it. | in the book text |
| CharacterBody2D | Moved by your code; move_and_slide() slides it along what it hits. | in the book text |
| Collision shape | The geometry physics uses, separate from the drawn sprite. | in the book text |
| Collision layer | Where an object is: the layers it appears in. | in the book text |
| Collision mask | What an object scans: it detects B only if B is in a layer it scans. | in the book text |
| Bitmask | A number whose bits switch layers on or off; layer n has the value 2^(n−1). | in the book text |
| Area snapshot | An Area's overlap list is updated once per physics step, so it can be a tick old. | in the book text |

## Walker and the toolchain

[Open the deck](decks/Terms%20-%20Walker%20and%20the%20toolchain.html) · 14 slides · 26 terms

| Term | Meaning | Tag |
|---|---|---|
| Walker | The working method and its files: brief, build, playtest, inspect, revise, export. | in the book text |
| Repository | A project folder with its full version history. | in the book text |
| Commit | A saved snapshot in version history. | in the book text |
| Diff | The exact lines that changed between two versions. | in the book text |
| CLI and shell | You drive a program by typing commands; the shell (zsh, bash) reads them. | in the book text |
| Flag | An option on a command, such as --headless. | in the book text |
| Headless | Running with no window or display. | in the book text |
| Exit code | A number a program returns; 0 means success. | in the book text |
| Timeout | A limit after which a run is stopped. | in the book text |
| Hang | A run that never finishes. | in the book text |
| Import | Convert a source file into the form the engine uses. | in the book text |
| Cache | Stored results reused to save time, which can also go stale. | in the book text |
| Permission prompt | A question asking you to approve an action. | in the book text |
| Allow rule | A saved permission letting a command run without asking. | in the book text |
| Sandbox | A restricted environment where mistakes cannot reach the rest of the machine. | in the book text |
| Instruction file | A standing file of project rules the agent reads, such as CLAUDE.md or AGENTS.md. | in the book text |
| Spec | A written description of what must be built. | in the glossary |
| Checkable instruction | An instruction written so a check can pass or fail. | in the glossary |
| Claim versus evidence | A claim says what happened; evidence is proof that it did. | in the book text |
| Regression test | A test that guards a behaviour that worked before. | in the book text |
| Deterministic | The same inputs always give the same result. | in the book text |
| Flaky | Passes sometimes and fails sometimes with no change. | in the glossary |
| Game time | The simulation's clock, as opposed to the wall clock. | in the glossary |
| Fixed frame rate | Rendering locked to a set number of frames a second so runs match. | in the book text |
| Pinned time step | A constant step length forced on the simulation. | in the book text |
| Text versus binary scene | Readable scene files diff cleanly; opaque ones do not. | in the book text |

---

## Alphabetical index

| Term | Deck | Meaning |
|---|---|---|
| _physics_process | Godot: the editor, scenes, nodes, signals and movement | Runs at a fixed rate, 60 times a second by default. |
| _process | Godot: the editor, scenes, nodes, signals and movement | Runs once per rendered frame; the rate varies by machine. |
| 2D, 3D and Script views | Godot: the editor, scenes, nodes, signals and movement | Tabs along the top: 2D and 3D edit scenes, Script edits code. |
| Agency (autonomy) | Game design B: choices and challenge | The player takes control of how the game is played. |
| Allow rule | Walker and the toolchain | A saved permission letting a command run without asking. |
| Alpha channel | 2D art and sound assets in the engine | The extra channel storing opacity. |
| Anticipation | Game design C: pacing and guidance | Prepare the player for what comes next, such as a wind-up before an attack. |
| Appeal | Game design A: what a game is | The pull to keep playing; it differs by game and by player. |
| Area snapshot | Godot: the editor, scenes, nodes, signals and movement | An Area's overlap list is updated once per physics step, so it can be a tick old. |
| Area2D | Godot: the editor, scenes, nodes, signals and movement | Detects overlaps and can emit signals; never blocks or pushes. |
| Art, design, engineering | Game design A: what a game is | They depend on each other; results are best when all three aim at the same target. |
| Aspect ratio | 2D art and sound assets in the engine | Width divided by height. |
| AudioStreamPlayer | 2D art and sound assets in the engine | Godot node that plays sound with no position. |
| Autoload | Godot: the editor, scenes, nodes, signals and movement | A script or scene kept loaded across scene changes. |
| Balance | Game design B: choices and challenge | Every advantage has a disadvantage; no role starts with an unfair edge. |
| Bitmask | Godot: the editor, scenes, nodes, signals and movement | A number whose bits switch layers on or off; layer n has the value 2^(n−1). |
| Build-up | Game design C: pacing and guidance | A sequence that raises tension toward an event: sound, sparks, camera shake. |
| Bus | 2D art and sound assets in the engine | A channel that sounds are routed through for shared volume and effects. |
| Cache | Walker and the toolchain | Stored results reused to save time, which can also go stale. |
| Camera limits | Terms: Camera | Clamps that keep the view inside the level. |
| CharacterBody2D | Godot: the editor, scenes, nodes, signals and movement | Moved by your code; move_and_slide() slides it along what it hits. |
| Checkable instruction | Walker and the toolchain | An instruction written so a check can pass or fail. |
| Claim versus evidence | Walker and the toolchain | A claim says what happened; evidence is proof that it did. |
| Clear progress | Game design A: what a game is | The player can see how close they are to the goal. |
| CLI and shell | Walker and the toolchain | You drive a program by typing commands; the shell (zsh, bash) reads them. |
| Climactic arc | Game design A: what a game is | Difficulty and tension build toward the goal's resolution. |
| Clipping | 2D art and sound assets in the engine | Distortion when a signal exceeds the maximum level. |
| Collider | 2D art and sound assets in the engine | Shape used for contact tests; separate from the art and sized from the body. |
| Collision layer | Godot: the editor, scenes, nodes, signals and movement | Where an object is: the layers it appears in. |
| Collision mask | Godot: the editor, scenes, nodes, signals and movement | What an object scans: it detects B only if B is in a layer it scans. |
| Collision shape | Godot: the editor, scenes, nodes, signals and movement | The geometry physics uses, separate from the drawn sprite. |
| Commit | Walker and the toolchain | A saved snapshot in version history. |
| Communication | Game design C: pacing and guidance | Showing the player the goal and how to reach it, with clues in the environment. |
| Components | Game design A: what a game is | The objects in the space that players use or meet: characters, weapons, vehicles. |
| Consistent rules | Game design C: pacing and guidance | Even where physics is bent, it is bent the same way every time. |
| Core loop | Game design A: what a game is | The repeated moment-to-moment cycle the player enjoys. |
| Core mechanic | Game design A: what a game is | The action players do over and over again. |
| Deadzone | Terms: Camera | Screen region where the target can move without the camera moving. |
| Decibel | 2D art and sound assets in the engine | Logarithmic loudness unit. |
| Decisions | Game design A: what a game is | The ways the player can get past the opposition. |
| Descriptive play | Game design B: choices and challenge | The player acts and sees the game respond: the bola hits, the ice shatters. |
| Design the middle first | Game design C: pacing and guidance | Build the engaging middle levels, then the opening levels that lead there. |
| Deterministic | Walker and the toolchain | The same inputs always give the same result. |
| Diff | Walker and the toolchain | The exact lines that changed between two versions. |
| Difficulty | Game design B: choices and challenge | How hard the opposition is; it is separate from fairness. |
| Dolly | Terms: Camera | Move the camera forward or backward along its view direction. |
| Dolly in / dolly out | Terms: Camera | Move the camera toward / away from the subject. Dolly in moves toward the subject, dolly out moves away. |
| Dolly versus zoom | Terms: Camera | A dolly changes parallax (near and far shift against each other); a zoom only magnifies. |
| Downtime | Game design B: choices and challenge | Time a player waits with nothing to do. |
| Dynamic | Game design C: pacing and guidance | Many things happening at once, so play stays fresh. |
| Evaluative play | Game design B: choices and challenge | The player steps back and asks why this action matters to the whole game. |
| Event-driven | Godot: the editor, scenes, nodes, signals and movement | Code runs only when something announces that it happened. |
| Exit code | Walker and the toolchain | A number a program returns; 0 means success. |
| Export preset, template | Godot: the editor, scenes, nodes, signals and movement | A preset is the recipe for one platform; the template is the prebuilt engine it packs your data into. |
| Fairness | Game design B: choices and challenge | Clear expectations and consistent design, so the player can learn from failing. |
| Field of view (FOV) | Terms: Camera | The lens angle; wider shows more. |
| FileSystem dock | Godot: the editor, scenes, nodes, signals and movement | Lists every file in the project, under res://. |
| Fixed frame rate | Walker and the toolchain | Rendering locked to a set number of frames a second so runs match. |
| Flag | Walker and the toolchain | An option on a command, such as --headless. |
| Flaky | Walker and the toolchain | Passes sometimes and fails sometimes with no change. |
| Focal length | Terms: Camera | Lens strength in millimetres; longer means narrower view and more magnification. |
| Follow camera | Terms: Camera | Tracks a moving target, usually with smoothing. |
| Frame rate | 2D art and sound assets in the engine | Frames shown per second. |
| Fringe (halo) | 2D art and sound assets in the engine | The halo of edge colour left around a cutout; fix_alpha_border removes it. |
| Frustration | Game design B: choices and challenge | Some is part of challenge; it has to be the kind the player can learn from. |
| Game | Game design A: what a game is | An activity that has all four: a goal, opposition, decisions and rules. |
| Game time | Walker and the toolchain | The simulation's clock, as opposed to the wall clock. |
| Games can cheat | Game design C: pacing and guidance | Hidden help the player does not notice, such as enemies told not to turn around. |
| Goal | Game design A: what a game is | The objective the player works toward. |
| Group | Godot: the editor, scenes, nodes, signals and movement | A named tag on nodes; one call reaches every node in it. |
| Guiding the focus | Game design C: pacing and guidance | Making clear what the player should concentrate on. |
| Hang | Walker and the toolchain | A run that never finishes. |
| Headless | Walker and the toolchain | Running with no window or display. |
| Headroom | 2D art and sound assets in the engine | Spare level left below the maximum. |
| House rules | Game design A: what a game is | Rules a group changes for its own table; they change how the game plays. |
| Import | Walker and the toolchain | Convert a source file into the form the engine uses. |
| Import settings | 2D art and sound assets in the engine | Per-asset options controlling how the engine converts it, kept in the .import file. |
| Input action | Godot: the editor, scenes, nodes, signals and movement | A named intent such as jump, bound to keys or buttons. |
| Inspector | Godot: the editor, scenes, nodes, signals and movement | The editor panel for viewing and editing properties. |
| Instance | Godot: the editor, scenes, nodes, signals and movement | One live copy of a saved scene; a change on one instance overrides the template. |
| Instruction file | Walker and the toolchain | A standing file of project rules the agent reads, such as CLAUDE.md or AGENTS.md. |
| Integer scaling | 2D art and sound assets in the engine | Scaling by whole numbers so pixel art stays crisp. |
| Just-pressed vs held | Godot: the editor, scenes, nodes, signals and movement | Just-pressed is true only on the tick a press began; held stays true while down. |
| Level design | Game design C: pacing and guidance | Planning and building the spaces the player moves through. |
| Linear and nonlinear | Game design C: pacing and guidance | Straight from start to end, or with alternate choices along the way. |
| Logical events | Game design C: pacing and guidance | Events behave sensibly and meet the player's unspoken expectations. |
| Look-ahead | Terms: Camera | Shifts framing toward the direction of travel. |
| Loop point | 2D art and sound assets in the engine | Where a looping sound jumps back to; WAV has begin and end, Ogg only a start offset. |
| Lossless vs lossy | 2D art and sound assets in the engine | Exact reconstruction versus smaller files with lost detail. |
| Luck and skill | Game design B: choices and challenge | Luck: chance decides. Skill: the player's ability decides. Games mix the two. |
| Meaningful choice | Game design B: choices and challenge | A choice that changes what happens and that the player has to think about. |
| Meaningful play | Game design B: choices and challenge | The player acts and the game responds in a way that matters. |
| Mechanic | Game design A: what a game is | A rule-governed action in the game. |
| Mipmaps | 2D art and sound assets in the engine | Pre-shrunk copies of a texture used when drawn small; about 33% more memory. |
| Movement pattern | Game design A: what a game is | How a character moves gives it personality: a hop is a frog, a wave is a snake. |
| Nearest vs linear | 2D art and sound assets in the engine | Nearest reads one texel and keeps hard edges; linear blends four and smooths. |
| Node | Godot: the editor, scenes, nodes, signals and movement | The smallest building block: one object doing one job. |
| Node dock | Godot: the editor, scenes, nodes, signals and movement | Shows the selected node's signals and groups. |
| Nyquist limit | 2D art and sound assets in the engine | The highest frequency a sample rate can hold: half the rate. |
| One-shot | 2D art and sound assets in the engine | Plays once and stops. |
| Opposition | Game design A: what a game is | Obstacles the player must overcome; it makes a game fun and can frustrate. |
| Orbit | Terms: Camera | Move around a subject on a curved path while keeping it framed. |
| Output and Debugger | Godot: the editor, scenes, nodes, signals and movement | Bottom panels: Output shows printed text, Debugger shows errors. |
| Pacing | Game design C: pacing and guidance | Alternating intense and calm moments. |
| Pan | Terms: Camera | Turn left or right on the spot; position unchanged. |
| Parallax | Terms: Camera | Nearer things shift more than farther things when the viewpoint moves. |
| PCM | 2D art and sound assets in the engine | Uncompressed digital audio samples. |
| Pedestal | Terms: Camera | Move the camera straight up or down, still facing the same way. |
| Permission prompt | Walker and the toolchain | A question asking you to approve an action. |
| Persistence | Game design B: choices and challenge | The player lives with the consequences of a choice for a set time. |
| Personalisation | Game design B: choices and challenge | Players build their own play style from the decisions they make. |
| Perspective / orthographic | Terms: Camera | Distant things shrink / size does not depend on distance. |
| Pinned time step | Walker and the toolchain | A constant step length forced on the simulation. |
| Play testing | Game design A: what a game is | Letting players challenge the design so it can be revisited and improved. |
| Player purpose | Game design C: pacing and guidance | What the player does and why; the player, not the game, drives it forward. |
| Player verb | Game design A: what a game is | An action the player can take: jump, shoot, build. |
| PNG vs JPEG | 2D art and sound assets in the engine | Lossless with alpha versus lossy without alpha. |
| Polling | Godot: the editor, scenes, nodes, signals and movement | Asking every tick whether something has happened. |
| Polyphony | 2D art and sound assets in the engine | How many copies of a sound can play at once; Godot's default is 1. |
| Probability | Game design B: choices and challenge | The odds of each result; extra rolls change them. |
| Procedural synthesis | 2D art and sound assets in the engine | Sound made by a formula evaluated sample by sample, with no file and no model. |
| Progression | Game design C: pacing and guidance | A natural rise in challenge; do not over-stimulate or under-stimulate. |
| Project | Godot: the editor, scenes, nodes, signals and movement | A folder with a project.godot file at its root; res:// means that folder. |
| Project Settings | Godot: the editor, scenes, nodes, signals and movement | Project-wide values: physics rate, layer names, input actions, autoloads. |
| Prototype | Game design A: what a game is | A simplified version made first to test whether the idea has appeal. |
| Readability | 2D art and sound assets in the engine | How well a character can be understood in the game's real view. |
| Regression test | Walker and the toolchain | A test that guards a behaviour that worked before. |
| Repository | Walker and the toolchain | A project folder with its full version history. |
| Resolution | 2D art and sound assets in the engine | Width and height in pixels. |
| Resource | Godot: the editor, scenes, nodes, signals and movement | A typed data container nodes share, made by extending Resource. |
| RigidBody2D | Godot: the editor, scenes, nodes, signals and movement | Simulated physics: you set forces or velocity, the engine moves it. |
| Risk versus reward | Game design B: choices and challenge | A harder or riskier action pays more, and the player weighs the factors. |
| Rock-paper-scissors | Game design B: choices and challenge | Each option beats one and loses to another, so no option wins everywhere. |
| Roll | Terms: Camera | Spin around the viewing direction; the horizon tips. |
| Rules | Game design A: what a game is | The framework that limits and governs the whole experience. |
| Run and Play buttons | Godot: the editor, scenes, nodes, signals and movement | Run Project (F5) starts the main scene; Run Current Scene starts the open one. |
| Sample rate | 2D art and sound assets in the engine | Audio samples per second. |
| Sandbox | Walker and the toolchain | A restricted environment where mistakes cannot reach the rest of the machine. |
| Scene | Godot: the editor, scenes, nodes, signals and movement | A saved, reusable tree of nodes: a level, a character, a menu. |
| Scene dock, Remote tab | Godot: the editor, scenes, nodes, signals and movement | Lists the scene's nodes; the Remote tab lists the running game's. |
| Scene tree | Godot: the editor, scenes, nodes, signals and movement | The live hierarchy of nodes in a running game. |
| Screen shake | Terms: Camera | Brief, fading random offset of the camera for impact. |
| Script | Godot: the editor, scenes, nodes, signals and movement | Attaches behaviour to a node; GDScript here. |
| Side quest | Game design C: pacing and guidance | A detour from the main storyline. |
| Signal | Godot: the editor, scenes, nodes, signals and movement | A named event a node emits; other nodes connect to it. |
| Silhouette | 2D art and sound assets in the engine | The outline of an object; it should still read when filled black at game size. |
| Situational choice | Game design B: choices and challenge | The same choice is better or worse depending on the situation the player is in. |
| Smoothing (damping) | Terms: Camera | Spreads the camera's catch-up over time so it trails slightly. Same idea under both names: the camera eases toward its target instead of snapping. |
| Space | Game design A: what a game is | The look, sound, lighting and physical setting; it shapes what fits in the game. |
| Spacing | Game design C: pacing and guidance | Open areas to admire, or tight ones that feel claustrophobic; leave room for AI. |
| Spec | Walker and the toolchain | A written description of what must be built. |
| Sprite sheet | 2D art and sound assets in the engine | One image of many frames in a grid. |
| SpriteFrames | 2D art and sound assets in the engine | A Godot resource of named animations: frames, speed and a loop flag. |
| StaticBody2D | Godot: the editor, scenes, nodes, signals and movement | Not moved by physics; others collide with it. |
| Target experience | Game design A: what a game is | The one specific experience everyone on the team aims at. |
| Teaching through levels | Game design C: pacing and guidance | The first level lets the player try each skill, with no text. |
| Texel | 2D art and sound assets in the engine | One pixel of a texture. |
| Text versus binary scene | Walker and the toolchain | Readable scene files diff cleanly; opaque ones do not. |
| Texture atlas | 2D art and sound assets in the engine | Many small images packed into one big texture; a frame is a region of it. |
| Thematic feel | Game design A: what a game is | Mechanics alone can set the tone: what a thing does tells the player what it is. |
| Three pillars | Game design C: pacing and guidance | A game rests on the player's role, communication and appeal. |
| Tilt | Terms: Camera | Turn up or down on the spot; position unchanged. |
| Timeout | Walker and the toolchain | A limit after which a run is stopped. |
| Trade-off | Game design B: choices and challenge | Give up one thing to get another. |
| Transparent background | 2D art and sound assets in the engine | Cut the background to alpha 0; ask for a solid colour, not for transparent. |
| Truck | Terms: Camera | Move the camera left or right, still facing the same way. |
| Types of fun | Game design A: what a game is | "Fun" is too vague. Name the kind: fantasy, thrill, fellowship, mastery, exploration, creativity. |
| Uniform vs non-uniform | 2D art and sound assets in the engine | Same factor on both axes versus different factors that distort. |
| Unit differentiation | Game design B: choices and challenge | Each enemy type does something different, which forces the player to prioritise. |
| Viewport | 2D art and sound assets in the engine | The area the game draws into, set in Project Settings; the window scales it. |
| Walker | Walker and the toolchain | The working method and its files: brief, build, playtest, inspect, revise, export. |
| WAV vs Ogg Vorbis | 2D art and sound assets in the engine | WAV for short effects; Ogg Vorbis for music, speech and long sounds. |
| Waves | Game design C: pacing and guidance | A group of enemies sent together: many weak ones or a few strong ones. |
| Zoom | Terms: Camera | Change the lens (field of view or focal length); the camera does not move. |
