# HOUSEGHOST — Concept

**Project:** `walker-houseghost-narasimha-v` · CSYE 7270 Assignment 2 · Narasimha Reddy Valam
**Started from:** an empty Godot 4 project. The world-inversion verb is carried forward as an idea from my Assignment 1 game (walker-jumpman-narasimha-v); no code or assets are reused.

## The game in two sentences

You are the ghost of a boy the world believes ran away, haunting the house a new family has just moved into. By flipping between the house as they see it (upright, bare, theirs) and the house as you remember it (upside down, lamplit, yours), you reach across to be seen — but every contact tears a day off the calendar toward the anniversary of the night you "ran," and the only adult who believes in ghosts is the man who made you one.

## Core loop

**The action:** flip into the inverted memory-house, find something true (a relic, a route, a memory), flip back, and spend it on a contact — a touch the living can notice.
**The decision each time:** kind contact or scary contact. Scary is fast (recognition jumps) but alerts the father and feeds the Hollow. Kind is slow and safe.
**The risk:** every contact tears a calendar day. The anniversary arrives whether you are ready or not, and the frost that comes with it eats the memory-rooms you still need.

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

The player should feel like an intruder in their own home: quiet, held-breath, listening. Upright world: near-silence — house settling, a clock, the family's muffled life through walls. Inverted world: a music-box lullaby loop, warm but slightly worn, as if played too many times. The lullaby de-tunes a little each time a calendar day tears away — the soundtrack itself is the doom meter. Music never plays in both worlds at once; the flip hard-cuts the mix, which makes the flip feel like crossing a real threshold. On pause: all audio ducks to silence except the clock. On the slice's fail state (the Hollow touches you): the lullaby stops mid-phrase and does not resume until the player flips upright. On the slice's end: the lullaby completes its phrase once, cleanly, then stops — the only clean resolution in the game's audio, reserved for endings.

## The name

The boy is nameless everywhere — menus, UI, documents, dialogue. His name exists in the game only as a relic scratched under a floorboard in the memory-house, and the child speaking it aloud is what completes "being seen." Erasing him was the crime; naming him is the win condition. (Hidden answer recorded in the character sheet; it never appears in the slice.)

## Generation plan

Art comes from Gemini and ChatGPT image generation (free/institutional access, no paid APIs). Neither exposes seeds, so reproducibility is kept by logging the exact prompt, model and version, date, and screenshots of every attempt in the asset log. Character consistency comes from one approved reference image of the ghost, re-uploaded with each pose request. Backgrounds are prompted flat magenta and removed locally, never prompted "transparent." Music: Suno free tier (7 lifetime downloads — rejects are logged by screenshot, only finalists downloaded). SFX: a no-download-cap tool (ElevenLabs free credits or a local model), trimmed and looped in Audacity, delivered as OGG/WAV.

## Scope note

Assignment 2 proves Night 1 only, as a slice: one room and hallway in both world-states, the flip, one kind and one scary contact, the calendar/frost meter, one wrong-room correction, a glimpse of the father checking the cellar door. The five-act twist ladder (memory corrections, the father's history, the family's identity, the Hollow's identity, the testimony ending) is the semester plan and is deliberately not spoiled in the slice.
