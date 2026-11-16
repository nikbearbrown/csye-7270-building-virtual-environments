# Riot "So You Wanna Make Games??" Eps 1-9: terms for the terminology decks

## Executive summary

- Source: auto-captions of Riot Games' Eps 1-9 (Ep 10, game design, skipped as already covered). The captions run words together and misspell names, so any uncertain term is marked (uncertain).
- 171 distinct terms were pulled (counts per episode in the tables). 43 already appear in GLOSSARY-jargon-midterm.md (several only partially); 128 are new. Most "already in" hits are the animation, rig, particle, audio and 3D-asset sections.
- The glossary is engine- and implementation-heavy. The series is craft vocabulary (why art reads, how it is made), so the gaps are art principles, concept and character workflow, environment-art workflow, UI/UX and sound-design vocabulary.
- Four existing decks absorb many terms (Animation foundations, Particles, Audio and triggers, Textures and materials). Four NEW decks are proposed: Art principles and concept art, Character and environment art workflow, UI and UX design, Sound design.
- Glossary "Pitch" means a game sales pitch (Game design documents), so audio pitch is marked new, not matched. Glossary section names below are quoted exactly.

Meanings are paraphrased by me, not copied. "glossary: X" = the term (or a clear equivalent, noted in brackets) is in section X. "new" = absent.

---

## Ep 1 - Intro to Game Art (RqRoXLLwJ8g)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 1.1 | Clarity | The player can instantly tell what is going on: where to go, who is friend or foe, how healthy they are. | new |
| 1.2 | Satisfaction (responsive feedback) | The game answers each player action at once and makes success and failure feel good or bad. | new |
| 1.3 | Art style | The consistent look of a game: colour use, character design, how exaggerated shapes are. | new (glossary only has "Palette", 2D art and sound assets) |
| 1.4 | Pushed proportions | Deliberately exaggerated body or object shapes, as in a cartoon look. | new |
| 1.5 | Stylized versus realistic | A simplified or exaggerated look versus one that copies the real world. | new |
| 1.6 | Visual hierarchy | Arranging the picture so the most important things are seen first. | new |
| 1.7 | Contrast | Any difference (light, shape, colour, size, detail) used to pull the eye to one place. | new |
| 1.8 | Shape and size contrast | Using distinct shapes or sizes so one object stands out, or points toward danger or safety. | new |
| 1.9 | Colour and saturation contrast | Using strong colour or intensity differences so key things pop. | new |
| 1.10 | Silhouette | The outline of an object, which should be readable on its own. | glossary: Textures and materials |
| 1.11 | Focal point / area of focus | The spot in an image the artist wants the eye to land on. | new (glossary "Focal length" is a camera lens term, not this) |
| 1.12 | Areas of rest versus high detail | Leaving some regions plain so the busy regions read as important. | new |
| 1.13 | Atmospheric perspective | Faraway things lose detail and contrast, which adds depth and guides the eye. | new |

Ep 1 count: 13 terms; 1 in glossary, 12 new.

---

## Ep 2 - Concept Art (FqX-UMVTLHI)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 2.1 | Concept art | Early drawings and paintings that solve a design problem for the team, not finished pictures. | new |
| 2.2 | Constraint | A limit (setting, perspective, rules) that narrows what the artist should design. | new |
| 2.3 | Thematic constraint (lore, setting, tone) | A limit coming from the game's world and mood. | new |
| 2.4 | Perspective constraint (first person, third person, top down) | A limit from how the player's view frames the design. | new (glossary Camera section has no player-view modes) |
| 2.5 | Mechanics constraint | A limit from the game's rules and numbers, such as an ability or health total. | new |
| 2.6 | Reference | Collected real-world images and examples used for research. | new (glossary has only "Reference image" in Shader verification, a different meaning) |
| 2.7 | Mood board | A collection of reference images showing the intended theme and tone, shown to the team early. | new |
| 2.8 | Fillers (uncertain; captions say "fillers", probably short descriptor words on a mood board) | Short text labels placed on a mood board. | new (uncertain) |
| 2.9 | Ideation | Producing many quick ideas before choosing one. | new |
| 2.10 | Draw fast and loose | Sketching roughly to show the idea, not polish. | new |
| 2.11 | Two-tone sketching | Sketching with only two colours to avoid fussing over detail. | new |
| 2.12 | Closing doors | Narrowing ideas from broad to narrow by closing rejected options each round. | new |
| 2.13 | Iteration | Repeating a cycle of draft, feedback and change. | new |
| 2.14 | Grand reveal | Showing work late and all at once; the speakers advise against it. | new |
| 2.15 | Shape language | How the forms in a design express its personality or idea. | new |
| 2.16 | Target audience | The specific group a design is meant to excite. | new |
| 2.17 | Archetype | A familiar character type (for example a blade dancer) that a design builds on. | new |

Ep 2 count: 17 terms; 0 in glossary, 17 new (Iteration relates loosely to "Prototype" and "Playtest" in Game design documents, but is not defined there).

---

## Ep 3 - Character Art (PfpE5dNTWeI)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 3.1 | Character artist | Person who models, textures and sometimes designs the characters. | new |
| 3.2 | Iconic elements | The few features that make a character recognizable even when tiny on screen. | new |
| 3.3 | Proxy model | A rough block-out model used to check proportions and silhouette early. | new |
| 3.4 | Readability | How well a character can be understood in the game's real view. | new |
| 3.5 | 3D model / polygon mesh | Points joined by lines into faces that form the object's surface. | glossary: 3D assets and Blender [Vertex, Edge, Face] |
| 3.6 | Vertex | A corner point of a mesh. | glossary: 3D assets and Blender |
| 3.7 | High-poly sculpt | A very detailed model made by digital sculpting. | new |
| 3.8 | Digital sculpting | Shaping a model like clay in software such as ZBrush. | new |
| 3.9 | Low-poly mesh | A cheap, simplified version of the sculpt that the engine can run. | new (glossary has "Triangle count..." and LOD in 3D assets and Blender, not this term) |
| 3.10 | UV map | A flat 2D layout of the model's surface used to place textures. | glossary: 3D assets and Blender |
| 3.11 | Unwrapping | Cutting a model open and laying its surface flat. | glossary: 3D assets and Blender |
| 3.12 | Texture baking | Transferring the high-poly detail into an image for the low-poly mesh. | new (glossary has "Baked lighting" in Textures and materials, which is a different bake) |
| 3.13 | Texture painting | Painting colour directly onto the flattened UV image. | new |
| 3.14 | Shader | A small program that decides how a surface looks. | glossary: Shader foundations (also Shaders and materials) |
| 3.15 | Shader inputs (colour, transparency, metallic) | Settings on a shader that change the surface. | glossary: Shaders and materials [Metallic, Albedo, Transparency in 2D art] |
| 3.16 | Texture map | An image plugged into a shader input. | glossary: Textures and materials [Colour texture, Texture] |
| 3.17 | Normal map | A texture that fakes small bumps in the lighting without extra geometry. | glossary: Shaders and materials (also Textures and materials) |
| 3.18 | Height map | A greyscale texture saying how far parts stick out. | glossary: Textures and materials |
| 3.19 | Anatomy | Knowing the bones and muscles so a sculpt is believable and can be animated. | new |
| 3.20 | Neutral pose | The default standing pose a model is built in. | new (uncertain wording; captions say "neutral pose") |

Ep 3 count: 20 terms; 9 in glossary (3.5, 3.6, 3.10, 3.11, 3.14, 3.15, 3.16, 3.17, 3.18), 11 new.

---

## Ep 4 - Environment Art (37LVhP15zGw)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 4.1 | Environment art | Building the world: terrain, props and set pieces. | new |
| 4.2 | Prioritization | Choosing which assets deserve the most effort. | new |
| 4.3 | Block-out | A rough level built from grey boxes that fixes obstacles, paths and enemy entries. | new (glossary Level design in Game design documents is the discipline only) |
| 4.4 | Rough-out / art pass | Replacing the boxes with first-draft art. | new |
| 4.5 | Playtest | Watching real people play to find problems. | glossary: Game design documents |
| 4.6 | Paint-over | Painting directly on a screenshot to suggest changes. | new |
| 4.7 | Gameplay constraint | A rule the environment must serve, such as a boundary or a climbable ledge. | new |
| 4.8 | Gameplay-critical information in the world | Setting art that also tells the player what they can do. | new |
| 4.9 | Establishing composition | The opening view of a level that shows the player where they are. | new |
| 4.10 | Lighting (focal lighting, spot light, shadow) | Using light and dark to guide the eye and set mood. | glossary: Textures and materials [Baked lighting; light/shadow in Shader foundations] (partial) |
| 4.11 | Post-processing effects | Full-screen image adjustments added at the end. | new |
| 4.12 | Environmental storytelling | Layout and props that show history, climate or culture. | new |
| 4.13 | Scale cues | Familiar objects (chairs, doors, stairs) that make sizes believable. | new |
| 4.14 | Poly count | The number of polygons in a model, kept low for speed. | glossary: 3D assets and Blender [Triangle count versus face count versus vertex count] |
| 4.15 | Modular kit | Reusable building chunks that combine into many different places. | new |
| 4.16 | Reuse of models and textures | Repeating assets to save time and memory. | glossary: Profiling and optimization [Texture compression, Texture atlas in 2D art and sound assets] (partial) |
| 4.17 | Wear and tear | Small signs of use (worn edges, grime) that make props feel lived in. | new |

Ep 4 count: 17 terms; 4 in glossary (4.5, 4.10, 4.14, 4.16; two of them partial), 13 new.

---

## Ep 5 - Technical Art (kr7XYXMM7-U)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 5.1 | Technical artist | Person bridging art and code, speeding up how art gets into the game. | new |
| 5.2 | Rigging | Giving a model a skeleton so it can move. | glossary: Animation [Rig] |
| 5.3 | Skeleton and bones | A hierarchy of joints placed inside a mesh. | glossary: Animation [Skeleton, Bone] |
| 5.4 | Weight painting | Painting how much each bone pulls on each part of the mesh. | glossary: Animation [Bone weights, Skinning weights] (the paint step itself is new) |
| 5.5 | Mesh deformation | The mesh bending as bones move. | glossary: Animation foundations [Skinning] |
| 5.6 | Rig controls | Handles that move many bones at once, like puppet strings. | new |
| 5.7 | Foot planting / leg follow | Rig behaviour that keeps a foot fixed on the ground or switches which part leads. | glossary: Animation [IK] (partial) |
| 5.8 | Custom tool | A small plug-in or script made to save artists' time. | glossary: Toolchain [Add-on in 3D assets and Blender] (partial) |
| 5.9 | Implementation steps | The cleanup (names, settings, splitting files) an asset needs before it works in-game. | new |
| 5.10 | Exporter | A tool that sends an asset out of an art program for the game. | glossary: Engine vocabulary [Export, Import] (partial) |
| 5.11 | Game development pipeline | The flow of files from person to person until they reach the game. | new (glossary "Pipeline" in Profiling and optimization is a different sense: render stages) |
| 5.12 | Version control | Software that records every file version and who changed it, and warns of clashes. | glossary: Toolchain [Repository, Commit, Diff; the phrase "version control" itself is not defined] (partial) |
| 5.13 | Naming conventions | Agreed rules for file names. | new |
| 5.14 | Folder structure | The agreed way files are organized in directories. | new |
| 5.15 | Mass renaming | A tool that renames many files at once. | new |
| 5.16 | Vertex colour | Colour stored on each vertex, here used to blend textures or paint terrain. | new |
| 5.17 | Shader parameters | The adjustable inputs of a shader. | glossary: Shader foundations [Uniform] |
| 5.18 | Toon (tuned) shading | A shader trick that flattens the lighting to give a cartoon look. | new (uncertain; captions say "tuned shaded", likely toon-shaded) |
| 5.19 | Simulation | Using maths to mimic physical behaviour of cloth, hair, water and similar. | glossary: Game movement and collision [Rigid body] (partial; cloth, hair, fluids are new) |
| 5.20 | Ragdoll | A body that collapses under physics instead of playing an animation. | new |
| 5.21 | Context switching | Jumping between very different requests during the day. | new |

Ep 5 count: 21 terms; 10 in glossary (5.2, 5.3, 5.4, 5.5, 5.7, 5.8, 5.10, 5.12, 5.17, 5.19; several partial), 11 new.

---

## Ep 6 - Character Animation (VmNUAX2V8JQ)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 6.1 | 12 principles of animation | The classic set of animation rules from Thomas and Johnston's book. | new |
| 6.2 | Anticipation | A short wind-up that tells the player an action is coming. | new (glossary has "Startup" frames in Animation and interaction, close but different) |
| 6.3 | Believable motion and physics | Movement that stays consistent so players can predict results. | new |
| 6.4 | Character personality in motion | Making an action show who this specific character is. | new |
| 6.5 | Acting it out (video reference) | Filming yourself doing the action to plan the animation. | new |
| 6.6 | Pose | A single held body position; animation is a series of them. | glossary: Animation foundations [Pose], plus Keyframe in Animation |
| 6.7 | Line of action | An imagined curve through the body that gives a pose one clear direction. | new |
| 6.8 | Weight distribution / centre of gravity | Where the balance falls, shown by whether it sits over the feet. | new |
| 6.9 | Stance | How the feet and body are set, used to sell weight. | new |
| 6.10 | Key storytelling poses | The main poses plotted on a timeline before filling in between. | glossary: Animation [Keyframe] (partial) |
| 6.11 | Timeline | The time axis that holds the keys. | glossary: Animation foundations |
| 6.12 | Spacing | How far the object moves between successive frames. | new |
| 6.13 | Ease (ease in, ease out) | Slowing toward a stop (or speeding from rest) so motion feels weighted. | glossary: Animation [Easing] |
| 6.14 | Squash and stretch | Compressing on impact and elongating at speed to show elasticity and inertia. | new |
| 6.15 | Ball bounce | The standard beginner exercise for timing and spacing. | new |
| 6.16 | Inertia / elasticity | The sense that a body resists changes in speed and springs back. | new |
| 6.17 | Animation blending | Mixing several animations together as one result. | glossary: Animation [Blend tree] |
| 6.18 | State machine | The tool that chooses which animations play under which conditions. | glossary: Animation [State machine, Transition] |
| 6.19 | Motion reference | Footage or studies of real movement. | new |
| 6.20 | Straight-ahead versus pose-to-pose (uncertain; transcript only hints at it) | Animating frame after frame in order versus planning key poses first. | new (uncertain) |

Ep 6 count: 20 terms; 6 in glossary (6.6, 6.10 partial, 6.11, 6.13, 6.17, 6.18), 14 new.

---

## Ep 7 - Game VFX (3QKK2o5rWSQ)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 7.1 | VFX (visual effects) | Sparks, magic, smoke, splashes and similar visual extras. | new (as an abbreviation) |
| 7.2 | Real-time effect | An effect drawn live every frame, so it must be cheap, unlike film renders. | new |
| 7.3 | Particle system | An emitter plus the rules for what it spawns. | glossary: Particles |
| 7.4 | Emitter | The invisible spawn point of a particle system. | glossary: Particles |
| 7.5 | Sprite | A flat image fired by an emitter. | glossary: 2D art and sound assets |
| 7.6 | Camera-facing card | A flat quad that always turns toward the viewer. | glossary: Particles [Billboard] |
| 7.7 | Mesh effect | A 3D shape (such as half a sphere) used inside an effect. | glossary: Particles [Mesh particle] |
| 7.8 | Trail / ribbon | A strip that follows a moving object, textured to look like a tail. | new |
| 7.9 | Scrolling texture | A texture slid across a surface to suggest motion. | new |
| 7.10 | Primary, secondary and tertiary reads | The order the eye notices an effect's parts. | new |
| 7.11 | Glow texture | A soft bright image used to make a head or core pop. | new |
| 7.12 | Restraint (effect contrast) | Keeping most effects modest so important ones stand out. | new |
| 7.13 | Shape language (effects) | Using the same shapes for the same meaning across a game. | new |
| 7.14 | Colour coding | Colours that signal team, damage type or tone. | new |
| 7.15 | Analogous colours | Neighbouring hues, used to tie an effect to its caster. | new |
| 7.16 | Timing / speed curve of an effect | Varying how fast an effect grows and slows, instead of linear change. | glossary: Animation [Easing] (partial) |
| 7.17 | Gravity and collision in particles | Particles pulled down and bouncing off objects. | glossary: Particles [Gravity (particles)] |
| 7.18 | Real-time VFX communication of gameplay | An effect's job is telling the player what happened. | new |

Ep 7 count: 18 terms; 7 in glossary (7.3, 7.4, 7.5, 7.6, 7.7, 7.16 partial, 7.17), 11 new.

---

## Ep 8 - Sound Design (KcorIwJscFA)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 8.1 | Gameplay cue | A sound that tells you something is ready, damaged or spotted. | glossary: Audio and triggers [Cue] (different sense: a named sound event) |
| 8.2 | Audio feedback | Sound confirming a player's choices. | new |
| 8.3 | Emotional driver / mood through sound | Sound used to set the atmosphere of a scene. | new |
| 8.4 | Frequency | How fast a vibration repeats; sets pitch. | new |
| 8.5 | Pitch | How high or low a sound seems. | new (glossary "Pitch" is a game pitch, Game design documents) |
| 8.6 | Frequency band | A slice of the frequency range. | new |
| 8.7 | Sound envelope | The shape of a sound's loudness from start to end. | new |
| 8.8 | Waveform | The drawn shape of the sound. | new |
| 8.9 | ADSR (attack, decay, sustain, release) | Four stages of a sound's envelope: rise, drop, hold, fade. | new |
| 8.10 | Attack | Time to go from silence to the loudest point. | new (glossary "Attack" is a combat-timing term in Animation and interaction) |
| 8.11 | Decay | Drop after the peak. | new |
| 8.12 | Sustain | The level held for most of the sound. | new |
| 8.13 | Release | The fade-out at the end. | new (glossary "Release" is returning to a pool, Profiling) |
| 8.14 | Dynamics | The overall loudness behaviour of a sound over time. | new |
| 8.15 | Attenuation | Loudness falling as you move away from the source. | glossary: Audio and triggers |
| 8.16 | Attenuation curve | The curve describing how loudness changes with distance. | glossary: Audio and triggers [Falloff] |
| 8.17 | Equalization (EQ) | Boosting or cutting chosen frequencies. | new |
| 8.18 | Reverb | The echo of a space from sound bouncing off surfaces. | glossary: Audio and triggers |
| 8.19 | Attaching sounds to game events | Wiring a sound or music change to something happening in the game. | glossary: Audio and triggers [Cue, Trigger in Game movement and collision] (partial) |
| 8.20 | Sound library | A collection of recorded sounds to reuse. | new |
| 8.21 | Foley | Sounds recorded by hand with props. | new |
| 8.22 | Foley prop | An object made to produce a needed sound. | new |
| 8.23 | Dialogue | Spoken lines triggered by events. | new |
| 8.24 | Background music switching | Changing the music when the situation changes. | new |

Ep 8 count: 24 terms; 5 in glossary (8.1 and 8.19 partial; 8.15, 8.16, 8.18), 19 new.

---

## Ep 9 - User Interface Design (sc3h5JXtIzw)

| # | Term | Plain meaning | Glossary |
|---|------|---------------|----------|
| 9.1 | User interface (UI) | The visible elements a player uses to interact with the game. | new (the abbreviation appears in many entries but is never defined) |
| 9.2 | User experience (UX) | How information is organized and reached, and the path a player takes. | new |
| 9.3 | Information architecture | Where each piece of information lives and how you reach it. | new |
| 9.4 | UX flow / player journey | The route a player takes through the interface. | new |
| 9.5 | Visual design | Presenting complex information so it is simple and clear. | new |
| 9.6 | Audience (platform, genre) | Who is using the UI and where (PC, mobile, console; genre needs). | new |
| 9.7 | HUD (overlay) | Information drawn on top of the gameplay view. | new |
| 9.8 | Menus and screens (map, inventory, skill tree, character select) | The non-HUD UI screens. | new |
| 9.9 | Minimal UI | Showing little UI because the game needs little real-time info. | new |
| 9.10 | Ecosystem consistency | All UI sharing rules for colour, effect and position. | new |
| 9.11 | Thematic (UI theme) | The creative idea behind a UI's look. | new |
| 9.12 | Typography | The choice and use of lettering. | new |
| 9.13 | Iconography | The set of icons and how they look. | new |
| 9.14 | Layout | Arrangement of elements on screen. | new (glossary "UV map" mentions a flat layout, a different sense) |
| 9.15 | Proximity | Elements placed near each other read as related. | new |
| 9.16 | Motion graphics (mograph) | Animation of UI that makes the message felt. | new |
| 9.17 | UI motion goals (responsiveness, intention, awareness, consistency, physical intuition) | The five aims listed for UI animation. | new |
| 9.18 | Responsiveness | Interactions feel fast and fluid. | new |
| 9.19 | Parallax motion | Layers shifting at different speeds for depth. | glossary: Camera [Parallax] |
| 9.20 | Physical intuition | UI motion that follows believable forces, such as friction. | new |
| 9.21 | Pain point | A spot where a player gets stuck or annoyed, which design aims to fix. | new |

Ep 9 count: 21 terms; 1 in glossary (9.19), 20 new.

---

## Totals

| Episode | Terms | In glossary | New |
|---|---|---|---|
| Ep 1 Intro to Game Art | 13 | 1 | 12 |
| Ep 2 Concept Art | 17 | 0 | 17 |
| Ep 3 Character Art | 20 | 9 | 11 |
| Ep 4 Environment Art | 17 | 4 | 13 |
| Ep 5 Technical Art | 21 | 10 | 11 |
| Ep 6 Character Animation | 20 | 6 | 14 |
| Ep 7 Game VFX | 18 | 7 | 11 |
| Ep 8 Sound Design | 24 | 5 | 19 |
| Ep 9 User Interface Design | 21 | 1 | 20 |
| Total | 171 | 43 | 128 |

("In glossary" includes partial matches, flagged in the tables.)

---

## Episode-to-deck map

| Episode | Existing deck(s) that should take its terms | Terms that go there |
|---|---|---|
| Ep 1 Intro to Game Art | Textures and materials | silhouette |
| | (none else fits) | clarity, hierarchy, contrast etc. go to NEW deck A |
| Ep 2 Concept Art | (none) | all go to NEW deck A |
| Ep 3 Character Art | 3D assets and Blender; Textures and materials; Shaders and materials; Shader foundations | mesh, vertex, UV map, unwrapping, low-poly; texture map, normal map, height map; shader and inputs. High-poly, sculpting, proxy, baking go to NEW deck B |
| Ep 4 Environment Art | 3D assets and Blender; Game design documents; Profiling and optimization; Textures and materials | poly count, modular reuse, playtest, lighting. Block-out, scale cues, storytelling go to NEW deck B |
| Ep 5 Technical Art | Animation; Animation foundations; Toolchain; Engine vocabulary; Shader foundations; Collision and physics | rig, skeleton, weights, skinning, IK, version control, export, shader parameters, simulation. Pipeline, naming, vertex colour, rig controls, ragdoll go to NEW deck B (or Toolchain) |
| Ep 6 Character Animation | Animation foundations; Animation; Animation and interaction | pose, ease, blending, state machine, keyframe, timeline; also anticipation, squash and stretch, spacing, line of action, centre of gravity as additions to Animation foundations |
| Ep 7 Game VFX | Particles; Shaders and materials | particle system, emitter, billboard, mesh particle, gravity, timing and easing; effect-specific read order, shape language, colour coding as additions to Particles |
| Ep 8 Sound Design | Audio and triggers; 2D art and sound assets | attenuation, falloff, reverb, cue, events; envelope, ADSR, EQ, frequency, Foley go to NEW deck C or an extension of Audio and triggers |
| Ep 9 User Interface Design | Camera (parallax only) | parallax; everything else goes to NEW deck D |

---

## New decks proposed

1. Art principles and concept art (NEW deck A): clarity, satisfaction, art style, visual hierarchy, contrast types, focal point, areas of rest, atmospheric perspective, constraints, mood board, ideation, closing doors, iteration, shape language, target audience (Eps 1 and 2; about 30 terms).
2. Character and environment art workflow (NEW deck B): proxy model, high-poly sculpt, low-poly mesh, texture baking, texture painting, anatomy, block-out, scale cues, modular kit, environmental storytelling, post-processing, wear and tear, pipeline, naming conventions, rig controls, vertex colour (Eps 3, 4 and 5, about 25 terms).
3. Sound design (NEW deck C): frequency, pitch, envelope, ADSR, dynamics, EQ, Foley, sound library, audio feedback, mood through sound (Ep 8; about 14 terms). Alternative: fold into Audio and triggers if that deck has room.
4. UI and UX design (NEW deck D): UI, UX, information architecture, flow, visual design, HUD, minimal UI, ecosystem consistency, typography, iconography, layout, proximity, mograph, UI motion goals, responsiveness, physical intuition, pain point (Ep 9; about 20 terms). The glossary has no UI section at all.

## Honest caveats

- Captions are garbled in places: "rigging" appears as "ringing", "sustain/release" runs together, "Tune shading" is probably toon shading, "fillers" is probably a short label on a mood board. These are marked (uncertain).
- Several terms are tagged "partial" because the glossary has a related but different entry (for example Pitch, Attack, Release, Cue, Pipeline). Count them as new if the deck must define the art sense.
- The speakers explain some terms only by example (line of action, spacing, ease). Meanings above are mine, written from what they showed.
