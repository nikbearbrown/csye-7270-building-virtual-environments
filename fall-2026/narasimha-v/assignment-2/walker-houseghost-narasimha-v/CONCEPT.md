# HOUSEGHOST — Concept

**Project:** `walker-houseghost-narasimha-v` · CSYE 7270 Assignment 2 · Narasimha Reddy Valam
**Started from:** an empty Godot 4 project. The world-inversion verb is carried forward as an idea from my Assignment 1 game (walker-jumpman-narasimha-v); no code or assets are reused.

## The game in two sentences

You are the ghost of a boy the world believes ran away, haunting the house a new family has just moved into. By flipping between the house as they see it (upright, bare, theirs) and the house as you remember it (upside down, lamplit, yours), you reach across to be seen — but every contact tears a day off the calendar toward the anniversary of the night you "ran," and the only adult who believes in ghosts is the man who made you one.

## Core loop

**Revision 2026-10-06 — the flip, as built.** The camera never rotates. Pressing flip reverses gravity: the boy falls upward and stands on the ceiling, and the world changes what it is showing.

- **Normal — the comfortable lie.** He looks like a living boy, and the room is warm, lamplit and lived in. This is how he still sees himself and how he remembers the house.
- **Inverted — what is actually there.** He becomes the ghost, and the room becomes the stripped, boxed-up bedroom the new family moved into.

**The action:** walk and jump through the house, flipping between the two worlds to get past what blocks you. Furniture the memory has is solid only while normal; clutter the emptied house has is solid only while inverted. A stack you cannot pass on the floor is clear along the ceiling, and a stack hanging from the ceiling sends you back down — so the route alternates between the two truths.

**The decision each time:** at the music box, a gentle touch or a loud one. Gentle is slow and safe; loud is faster recognition but costs more days and wakes the house.

**The risk:** every contact tears days off the calendar toward the anniversary. The night ends either because the child finally sees you, or because the anniversary arrives first.

## Design pillars

1. **The flip is the fear.** Horror lives only in the inverted world; the upright world carries unease, never scares. The dread should peak the moment before the player flips, not after.
   *Honored by:* the flip sound — a held breath and a reversed room-tone swell — is the scariest sound in the game, scarier than anything in the inverted world itself.
2. **Nothing shown, everything implied.** No gore, no monster closeups. The father is frightening because he salts a threshold and passes the potatoes.
   *Honored by:* the father's sprite never faces the camera in Night 1; the Hollow appears only in peripheral framing, never centered.
3. **Being seen costs the truth's arrival.** Progress and danger are the same meter. The player should never get recognition for free.
   *Honored by:* the calendar-tear sound plays inside the warm contact chime — the reward and the cost are one audio event.
4. **The house is a witness.** Every room tells the story if the player looks; the environment is the narrative device, not dialogue.
   *Honored by:* the memory-house's wrong rooms visibly "correct" themselves — the art itself is the plot.

## Art direction

Soft-painted 2D interiors with heavy, honest shadow: the upright house in dim desaturated blues and movers'-cardboard browns (a home that isn't one yet), the inverted memory-house in deep amber lamplight against near-black (a home preserved in the moment it ended). The ghost is the palette bridge: cold blue-white and translucent in the upright world, solid and warmly lit in the inverted one — he only looks alive in the world that is gone. Reference notes in words: late-autumn dusk light through thin curtains; tungsten bulbs and wood grain; frost crystals on single-pane glass; VHS-era domestic objects (a music box, a wall calendar, a corded phone).

## Audio direction

The player should feel like an intruder in their own home: quiet, held-breath, listening.

**Revision 2026-10-06 — two tracks, one per world.** The original direction gave the inverted world a lullaby and left the upright world near-silent. Hearing it built, the silence read as unfinished rather than tense, so each world now owns a piece of music and the flip cuts between them.

- **Upright, where he is dead and unseen:** a tense, driving arpeggiated synth score. Cold and glassy, propulsive but restrained, with a percussive pulse built from the house's own sounds — a ticking clock, a dripping tap, a floorboard creak, a muffled heartbeat. The tension comes from repetition, never from volume.
- **Inverted, where he was alive:** a music-box lullaby over an organic polyrhythmic groove — hand drums, shakers, rim clicks, a syncopated sub-bass. Warm and moving on the surface, grieving underneath. The remembered room has a pulse because it is the world he was alive in; the dead room does not get one.

Both share key and tempo, so the flip cuts straight from one to the other with no musical lurch: the two worlds sound like one piece of music turning over. The cut is deliberate rather than a crossfade, because the abruptness is what makes the flip feel like crossing a threshold.

Music never plays in both worlds at once. On the slice's ending the current track fades once, cleanly — the only clean musical resolution in the slice, reserved for endings. M mutes music and N mutes effects, independently, and neither changes anything the game does.

## The name

The boy is nameless everywhere — menus, UI, documents, dialogue. His name exists in the game only as a relic scratched under a floorboard in the memory-house, and the child speaking it aloud is what completes "being seen." Erasing him was the crime; naming him is the win condition. (Hidden answer recorded in the character sheet; it never appears in the slice.)

## Generation plan

Art comes from Gemini and ChatGPT image generation (free/institutional access, no paid APIs). Neither exposes seeds, so reproducibility is kept by logging the exact prompt, model and version, date, and screenshots of every attempt in the asset log. Character consistency comes from one approved reference image of the ghost, re-uploaded with each pose request. Backgrounds are prompted flat magenta and removed locally, never prompted "transparent." Music: Suno free tier (7 lifetime downloads — rejects are logged by screenshot, only finalists downloaded). SFX: a no-download-cap tool (ElevenLabs free credits or a local model), trimmed and looped in Audacity, delivered as OGG/WAV.

## Scope note

Assignment 2 proves Night 1 only, as a slice: one room and hallway in both world-states, the flip, one kind and one scary contact, the calendar/frost meter, one wrong-room correction, a glimpse of the father checking the cellar door. The five-act twist ladder (memory corrections, the father's history, the family's identity, the Hollow's identity, the testimony ending) is the semester plan and is deliberately not spoiled in the slice.
