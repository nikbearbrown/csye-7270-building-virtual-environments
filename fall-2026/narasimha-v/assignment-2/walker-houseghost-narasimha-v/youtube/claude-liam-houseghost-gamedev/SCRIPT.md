# HOUSEGHOST — Narasimha Reddy Valam

**Film script** · `godot-gamedev walker` · Narrator: Liam, Teardown register
**Engine:** Godot 4.7.2.stable · **Frame:** 3840×2160, 30 fps
**Capture:** `capture/run-01.mp4`, scripted-input, 19.97 s, SHA-256 in `CAPTURE.md`
**Source revision shown:** filled at render time from the submitted commit

Every claim below is drawn from the repository or from the recorded run. Where
something is unverified, the film says so on camera.

---

## Bookend 1 — Claude composer

*Visual: the composer, typing at reading speed. No narration.*

> Please use Walker to convert my game design document about HOUSEGHOST — a side-on
> Godot game where you play the ghost of a boy the world believes ran away, haunting
> the bedroom a new family has moved into. One key turns the world over: upright is
> the stripped room as it really is and you are the ghost; inverted is the room as he
> remembers it and he looks like a living boy. Touching the things that were his is
> the only way to be noticed, and every contact tears a day off the calendar toward
> the anniversary of the night he "ran". Build the Night 1 slice.

---

## Bookend 2 — Hesitant-writer summary

*Visual: plain text composing, one word corrected in place.*

> A single bedroom, two versions of it, and one verb. You walk, you jump, you turn
> the room over, you reach for something that was yours. Seven nights. Three relics.
> A child in the doorway who is the only ~~meter~~ **witness** the game has.

---

## B01 — The story, and the lie it opens inside

*Visual: the stripped room, the ghost drifting. Then the flip, live, from the capture.*

**Liam:** "A boy is missing from this house. The version everyone agreed on is that
he ran away — easier to believe than the alternative, and nobody looked very hard.
He did not run. You play him."

"A new family lives here now. His bedroom has been emptied and taped into boxes, and
there is a clean rectangle on the wallpaper where something of his used to stand. He
can still see the room as it was, and the game lets you see it too: press the key and
the light turns warm, the bed is made, his drawings go back up on the wall."

"That warm room is the comfortable version. It is also the lie. The stripped one is
what is actually there."

"He wants one thing. Not revenge, not escape — to be noticed by somebody, once,
before the anniversary of the night he supposedly left. There is a girl of about
eight in the doorway. She is the only person in this house who might still see him."

*Visual: storyboard panel 06, labelled **storyboard — a later night**.*

"And there is a man downstairs who checks the cellar door every night, and lays a
line of salt across it, for a reason nobody has asked him about."

*Back to gameplay.*

"What follows is the first night. Three relics, seven days on the calendar, one
room. The full game runs longer, the house gets less honest as it goes, and the
question of who the salt is for is not answered tonight. This is the opening of the
story, built to prove the thing works — not the whole of it."

---

## B02 — Three pillars, each with a decision attached

*Visual: three cards, each cutting to the engine moment that serves it.*

**The house is a witness.** Nothing is narrated. His lines sit in the level, in his
voice, where they mean something — a thought at a doorway, never an instruction.

**Being seen costs.** Recognition and the calendar are the same meter filling. Every
contact raises one and tears a day off the other.

**Nothing shown, everything implied.** The man never appears. A clean rectangle on
the wallpaper, where something of his used to stand, does.

**Liam:** "The third pillar disciplines the other two. The game does not show you the
thing it is about — it shows you the shape left behind."

---

## B03 — The decision that made the loop mean something

*Visual: a relic lighting, the contact landing at 12.88 s, the child turning.*

**Liam:** "An early version had a counter that said *things of his, found*, and a goal
that said *be seen*, and nothing in between. Collecting objects does not make a person
notice you. The loop ran, and it was arbitrary."

"What closed the gap was deciding what a relic actually is. These are the only things
left in the house that still move for him. Touch one and something moves in a room
where nothing should — and that is a thing a living person can notice."

"Her posture carries the result. She turns further toward the room with each relic,
until she is facing you with her eyes wide. The meter is a child, not a number, and
that was worth the extra art."

---

## B04 — Code, then result: the flip

```gdscript
func flip() -> void:
	if _flipping or _meters.ended:
		return
	_flipping = true
	is_inverted = not is_inverted
	world_flipped.emit(is_inverted)
	_audio.play("flip")
```

*Then the flip in the capture at 11.65 s.*

**Liam:** "State first, signal second, sound third. That order holds everywhere in
this project: audio is a consequence, never a cause. Mute it and nothing the game
does changes — which is why both mutes exist, and why the slice still reads with
every sound switched off. The nights, the relic lights and the girl's posture all
carry state visually."

"The guard on the first line is not decoration. Hold the key down and `_flipping`
refuses the second call, so one turn makes exactly one sound."

*Then: `up_direction = Vector2(0, -_gravity_dir)` in `player.gd`, followed by the boy
standing on the ceiling.*

---

## B05 — One asset, design to game

**Liam:** "The drawings came before the generating. Six storyboard panels, a character
sheet with the poses the game would actually use, a silhouette tested at the size it
appears on screen, a collision shape drawn over it, and a palette checked against the
room. That sheet is the specification every generated image had to meet — and several
did not."

1. **The sheet** — the silhouette at true size, 33×96 px, and the rule that governs
   every pose: the proportions do not change.
2. **The prompt** — verbatim, including the magenta backdrop, because asking a model
   for a transparent background returns a drawn checkerboard.
3. **The raw output** — untouched, on magenta.
4. **The edits** — chroma key with soft alpha and de-spill, `min(r, b) − g`, then the
   scaling.
5. **In engine** — the eight-frame cycle running in the capture.

**Liam, over step four:** "Getting the frames to one size failed three times. Height
failed, because a crouch is shorter than a stand. Shoulder width failed, because
raised arms move the shoulders. Head width failed on the rising pose, where the
topmost pixels are not his head — they are his hands. Body area worked. Every obvious
measure of *the same size* turned out to be a property of the pose rather than of the
boy."

*Visual tail: the rejected takes as thumbnails.*

**Liam:** "The takes that lost are kept. One was turned down because the boy carried
less detail than the sheet specifies. Another because a lamp had drifted from the room
established two panels earlier — which only becomes visible once the earlier panels
exist to disagree with."

---

## B06 — Code, then result: what the mix was hiding

*Visual: the `LEVELS` table before and after. Two captures of the same walk.*

**Liam:** "A pass over the mix found the problem was not the levels that were set. It
was the ones that were never set. Three sounds — the footsteps, the ghost's drift and
the fall — were missing from this table, so they played at full level, while the
comment directly above it claimed footsteps were deliberately quiet."

"Matched peaks are not matched loudness. The footstep sample is dense where the story
sounds are spiky, so at equal peaks the steps sat five decibels above the flip. The
loudest sound in the game was the one that fires most often, and nothing had chosen
that."

---

## B07 — The events, in real play

*On-screen label: **scripted-input capture***

**Liam:** "Nine sounds carry this slice. Four are the spine: turning the world over, a
contact landing, a day tearing off the calendar, and falling out of the world. Each
fires from a signal the game emits after it has already changed state, and each fires
once — holding the key or mashing it does not stack them."

---

## B08 — The slice, unnarrated

*On-screen label: **slice audio, unnarrated**. No voice, no music bed.*

**Liam, before it begins:** "Twelve seconds with nothing over it. Two scores, one for
each version of the room, sharing a key and a tempo so the flip crosses between them
without a lurch. Listen for what happens after the contact."

*Capture, 11.0 s → 19.5 s with the room tone before it: the flip, the music ducking,
the music box answering, the paper tear, and the hush.*

**Liam, after:** "The silence is deliberate. It is the only moment in the slice where
the game stops making noise on purpose, because being noticed should not sound like a
reward."

---

## B09 — Code, then result: the loop that would not have looped

```gdscript
if stream is AudioStreamOggVorbis:
	stream.loop = true
```

**Liam:** "The music ships as Ogg Vorbis. Converting the files was not the whole job —
Godot's Ogg importer defaults loop to false, and Ogg and WAV spell looping
differently. Swap the extensions alone and the score plays once and stops.
Twenty-two megabytes became one point two, and the loop is set in code, because an
import setting does not survive a reimport reliably."

---

## B10 — What the tests cannot do

*Visual: thirteen checks passing. Then stills of things that were broken while they passed.*

**Liam:** "Thirteen automated checks, zero failures. They count each sound against each
event, under rapid repeats and held input, and they confirm that muting changes no
game state."

"They were also green through every real fault this game had. Green while the player
could not move, because a race between two tween signals depended on frame timing the
checks never exercise. Green while three sounds fired and could not be heard. Green
while a clean clone printed load errors."

"Passing tests and a broken game are not a contradiction — they measure different
things. Everything that mattered was found by a person playing it, with the sound on
and then with all of it off, or by running the project the way a stranger receives it:
cloned fresh, from scratch."

---

## Verdict

**Built and shown tonight:** two character states, both versions of the room, three
relics, seven nights, gravity inversion, nine sound events, two music loops, separate
mutes, contextual cues, and a girl whose posture is the recognition meter.

**What tonight does not do yet:** the house only gets less honest in later nights, so
the hallway that rearranges itself and the cellar door are drawn and not built. Three
poses on the character sheet are specified and ungenerated, because the slice never
calls for them. A player who skips the opening can take a moment to work out what the
game wants of them — the cues beside each relic are the answer to that, and they have
not been tried on a fresh player yet.

**Liam:** "HOUSEGHOST is designed, built and verified by Narasimha Reddy Valam. The
game is his — the story, the inversion, the seven nights, the decision that a child's
posture should carry the meter instead of a number. He generated every image, every
sound effect and both music loops, judged each one against his own character sheet and
storyboard, and threw out the ones that missed. He played it with the sound on, and
then with all of it off, to prove it still reads."

"Claude Code was the tool at the keyboard — GDScript, the processing scripts, the
documentation. Every design decision in this film came from him."

**Models:** ChatGPT's image model — the character art, both rooms, the relics, and the
six storyboard panels. Suno v6-mini — both music loops, non-commercial terms with
attribution. ElevenLabs Sound Effects — the event sounds.

**Liam:** "Gemini was tried first for the character and did not make it in. The boy it
returned read as a storybook schoolchild rather than the one the sheet describes, and a
later attempt read too old. Those takes are kept. A model that was evaluated and
dropped is part of the record too."

**Next:** the hallway that corrects itself. It is the first moment the memory — the
player's safe world — lies to them, and it is where the second night begins.

---

## Your Turn

**Liam reads:**

> Please use Walker to add a relic that can only be reached by falling upward through
> a ceiling gap, and predict what it does to the night count before you run it.

**Liam:** "Write the prediction down first, then run it. If the calendar disagrees with
you, the interesting thing is not the bug — it is the distance between what you
expected and what the engine did."

Liam signs off here.

---

## Outro — locked

`ClaudeTitleOutro`. Exact title, @NikBearBrown, one slug-seeded crisp mascot, no
subline. Liam re-reads the title, then "At Nik Bear Brown". No jingle, no game audio,
no narration over the final card.
