# FRICTIONAL — honest log of the design thinking

**walker-ninja-TiantongZhang · Tiantong Zhang · started 2026-09-30**

A dated log of the design as it happens: what I was trying to make the player
see or hear, what I asked the model for, what came back, and what I decided.
Written the same day, not reconstructed at the end — the instructor's note says
a week of small daily entries beats a last-night reconstruction, and he is
right that it is also easier.

> **"I" is me. "Claude" is Claude. "the model" is whichever generative model
> produced the asset.** Assignment 2 scores those three apart, so they are
> never blended. Claude writes code, prompts and plans and organises these
> notes; it does not generate images or audio, and it does not write my
> judgement for me.

---

## 2026-09-30 — setting up, and the one thing that had to happen first

**Wanted:** to start generating music tonight, because the free daily credits
do not carry over and there are only four days left.

**What stopped me:** the rubric gives a point for the design being committed
**before** the first generation, and the whole provenance claim depends on that
ordering being checkable. Generating first and writing the concept after would
have cost that point in a way nothing later could repair — git timestamps show
the order.

**Decided:** commit `CONCEPT.md` v1 first, then generate. The concept does not
have to be final; the assignment says to retain the original and append
revisions, so v1 is a real specification rather than a placeholder, and the
three decisions that are genuinely mine are marked `[TZ DECIDE]` in it rather
than guessed at.

**Also decided: continue Assignment 1's game rather than start a new one.**
Four days is not enough to design a new game *and* generate for it. The
cyber-ninja build already has tested movement, a level, enemies and a
death/retry loop, which leaves the four days for design and generation — which
is what this assignment is actually about.

**One thing I get for free by doing it this way:** Assignment 1's death
reaction used a meme cat image and a laugh with no documented permission.
Assignment 2 requires generated audio anyway, so those two files were not
copied into this repository at all. They are replaced by documented
placeholders — a flat colour card and 3.42 s of silence — and will be replaced
again by generated assets. The placeholder audio is exactly 3.42 s because
`test_game.gd` asserts the reaction's remaining time, so the suite stays green
without weakening an assertion.

**Human / Claude / model:** I chose to continue the A1 game and to accept the
"design first, generate second" ordering. Claude set up the repository, read the
shipped game to draft `CONCEPT.md` from measured values rather than invention,
made the placeholders, and verified 79 + 14 checks still pass. No generative
model has been used yet.

**Still unresolved:** the three `[TZ DECIDE]` items — the art style, what the
music should make the player feel, and what the music does during the 0.55 s
retry. The first Suno prompt is blocked on the second one.

**Traceability:** commit `766cf15`, `CONCEPT.md` v1, `godot/assets/README.md`.

---

## 2026-10-01 — the music direction, and a contradiction it exposed in my own concept

**Wanted:** a music direction concrete enough to prompt with. Claude gave me
three directions, written as full prompts so I could hear the difference rather
than argue about adjectives: sparse and patient, driving and urgent, or cold
industrial ambient.

**Decided — driving.** My words:

> 我选的第二个，因为首先很激情，而且能衬托出紧张感调动玩家肾上腺素

*I chose the second one, because first it is passionate, and it can set off the
tension and get the player's adrenaline going.*

**What that exposed.** `CONCEPT.md` v1's audio direction said *"the game is
quiet and the hazards are sudden"*, and made the sound's whole job letting a
15-frame warning feel like enough time. **That line was Claude's draft, not my
decision** — Claude inferred "quiet" from the shipped game, which has almost no
audio at all, so it described an absence and called it an intention. My
intention is the opposite. The draft is what was wrong, and
`CONCEPT.md` revision 1.1 records that rather than quietly editing the
sentence.

**What it costs, which I am accepting on purpose.** Pillar 2 needs the trap's
rising sound to be *heard* at the trigger, and a 124 bpm bed with pulsing bass
and tight percussion competes for exactly that. So:

- `SFX-TRAP` now has to be designed **against** the music — a rising metallic
  sweep, distinguishable by moving pitch rather than by volume, because the
  music already owns the low end and the percussive transients. Judging it
  alone in Audacity is not a test of it.
- It becomes a predicted failure case for `CHANGE-BRIEF.md`: *the 15-frame
  warning is masked by the music, so the hazard reads as unfair with sound on
  although it is fair with sound off.* Checked by a human playtest of the trap
  section at full music level, because masking is perceptual and no automated
  count can see it.
- The muted-play requirement limits the damage either way: the trap is already
  fair on visuals alone (15 visible frames, 96 px of run-up), so the worst case
  is "the sound added nothing", not "the game became unfair".

**Human / Claude / model:** I chose the direction and the reason. Claude wrote
the three candidate prompts, spotted that my choice contradicted the audio
direction it had itself drafted, said so instead of letting both sentences
stand, and worked out what the choice does to `SFX-TRAP`. **No generative model
has been used yet** — see the open question below.

**Still unresolved:** whether I pick the art style before or after seeing the
first generated character; and what the music does during the 0.55 s retry,
which cannot be judged until the loop is actually playing in the game.

**Traceability:** `CONCEPT.md` revision 1.1, commit to follow.

---

## 2026-10-01 (later) — the first two generations, and one I did not spend

**Wanted:** to hear the difference between the three directions rather than
reason about adjectives, and to do it without burning downloads — Suno's free
plan allows 7 for the life of the account and they never reset.

**Asked:** Suno (version to confirm), the three prompts Claude wrote from
`CONCEPT.md`'s pillars, 35–40 s each so there is room to cut a loop at a bar
boundary. Asset log rows `MUS-A-01`, `MUS-B-01`, `MUS-C-00`.

**Got, and decided:**

- **A, sparse and patient** — generated, auditioned in the browser,
  **rejected**. It leaves the player room. That is exactly what I decided I did
  not want.
- **B, driving at 124 bpm** — generated, auditioned, **accepted as the
  direction**. 很激情，能衬托出紧张感调动玩家肾上腺素.
- **C, cold industrial ambient** — **never generated.** My words:
  *第三个从文字描述上就提不起我的兴趣* — the third one did not interest me from
  its written description alone.

**On not generating C.** I am recording this as a decision, not an omission.
The free daily credits do not carry over, so an unused one is lost — but a
generation I already know I will reject is not worth the ten minutes of
listening either. Reading the prompt and deciding it is not the game I am
making is the same judgement I would have made after hearing it, arrived at
earlier. Claude wrote the prompt; the decision not to spend it was mine.

**What is still only a direction, not an asset.** `MUS-B-01` is a 124 bpm
generation I liked in a browser. It is not yet a loop: it has to be cut at a
bar boundary, checked across at least three repetitions for a seam, and
exported as OGG. None of that has happened, so nothing is in the project yet
and the slice still has no music.

**Human / Claude / model:** Claude wrote the three candidate prompts from the
concept and kept the log. Suno produced A and B. I chose B, rejected A on
hearing it, and rejected C without generating it. Two of those three are
judgements only I could make.

**Still unresolved:** which Suno version this was and whether I downloaded B —
both marked **TO CONFIRM** in the asset log rather than guessed, because the
download counter and the rubric's "model and version" field are factual claims.
Also still open: the art style, and what the music does during the 0.55 s retry.

**Traceability:** `ASSET-LOG.md` rows `MUS-A-01` / `MUS-B-01` / `MUS-C-00`;
`CONCEPT.md` revision 1.1.

---

## 2026-10-01 (correction, same day) — it was eight tracks, not two

I sent Claude a screenshot of the Suno workspace, and it corrected three things
in the entry above. Appending rather than editing it, because the entry above
is what I actually told Claude and the correction is part of the record.

- **Eight tracks, not two.** Each direction was run four times. My "前两个"
  meant the first two *directions*, not two generations.
- **The model is `v6-mini`** for the four usable tracks. The other four came
  back tagged `V6 PREVIEW`, capped at **1:00** behind an "Upgrade for full
  song" button — unusable on the free tier whatever they sound like. I did not
  know that would happen when I started, and it halves the candidate pool.
- **Direction A's four prompts were all reworded** and none matches what Claude
  wrote. Direction B's four are Claude's prompt verbatim. Whether I edited A's
  or Suno's prompt enhancement expanded them, the screenshot does not settle,
  and Claude did not assert either way in the log.

**Zero downloads.** All eight auditioned in the browser. The counter is still
0 of 7.

**What I notice looking at the eight together.** Direction A got four
different wordings — one of them (`MUS-A-02`) even asked for a "driving urgent
pulse" at 85 BPM, so it was already drifting toward B — and still lost.
Direction B won on the first wording, unchanged. Rewriting the prompt did not
rescue a direction that was wrong for the game. The decision that mattered was
which feeling the score should carry, and that is not a prompt-engineering
problem.

**Traceability:** `design/rejected/2026-10-01-suno-library.png`, `ASSET-LOG.md`
rows `MUS-A-01`…`MUS-C-00`.

---

## 2026-10-01 — the art style: pixel art

**Wanted:** a style decision concrete enough to prompt a character reference
with tomorrow.

**Decided: pixel art** (option (b) of the three in `CONCEPT.md` v1).

**Why, in my words:** the flat option would have been safest but the generated
frames would end up looking like the code-drawn ones they are replacing, and
that is a weak thing to put in the film. Painted was already ruled out in v1 —
at 18 × 28 the texture is mush. Pixel art is the only one whose constraints are
the same as the game's.

**What I am accepting by choosing it:** the texture import filter has to be set
to nearest or every frame blurs, and the palette is not free — the character
still has to read against both the cream sky and the dark slate platforms, so
v1's palette section is a constraint the generated art inherits rather than a
suggestion.

**One thing I am carrying over from the audio.** The assignment says to
generate one reference image and derive every pose from it, because consistency
comes from the reference and not from repeating the prompt. Direction A's four
rewordings just demonstrated that in audio: changing the sentence did not change
the outcome. I expect the same to be true of the character, so I am not planning
to prompt ten poses independently.

**Human / Claude / model:** the style choice and the reasoning are mine. Claude
laid out the three options with their costs in v1 and recorded this decision as
revision 1.2. No image has been generated yet.

**Still unresolved:** what the music does during the 0.55 s retry — still not
judgeable until the loop is actually in the game.

**Traceability:** `CONCEPT.md` revision 1.2.

---

## 2026-10-03 — the two specs, written late, and said so

**Wanted:** the character sheet and the change brief, in that order, before
anything else is generated.

**The ordering problem, stated plainly.** The music was generated on 10-01.
`CHARACTER-SHEET.md` and `CHANGE-BRIEF.md` were written on 10-03. So the music
ran ahead of its specification and there is no way to make that not true. What
I am not doing is dating the files 09-30 and pretending otherwise — the
repository's commit history would contradict it anyway, and a log that can be
checked against git and lose is worth less than no log. For the art and the
sound effects the order is the right way round, and that is the part I can still
control.

**The deadline moved to Wednesday 10-07**, which is four days. That is the
reason the character sheet splits its poses into eight required and three
optional instead of listing eleven as if they were equally likely to happen.
The optional three are the slack, and they are named as the first thing to drop
rather than discovered as a shortfall at the end.

**What came out of actually measuring the game instead of describing it.**
Three things I did not know this morning:

1. **The character is almost invisible against the platforms it stands on.**
   Plate `#1f3a6e` against platform `#25354a` is 1.12:1 — not low contrast, the
   same brightness. The visor is the exact mirror: 8.50:1 on slate, 1.32:1
   against the cream sky. The scarf is the only colour on the sheet above 2.5:1
   against both, at 2.89:1. So the scarf is not decoration, it is the
   silhouette, and the sheet now makes it mandatory and unoccluded in every
   pose. I had been treating it as the character's flourish.

2. **The sword must not be generated.** The swung blade is drawn from the same
   pivot, angle and reach the kill hitbox is built from, on purpose, so what you
   see and what kills you cannot drift apart. A static image of the blade would
   quietly sever that. So the generated sprite is body-and-scarf only and the
   code keeps drawing the sword over it — which also drops the frame from
   56 × 56 to 32 × 32.

3. **There is no death pose.** On death the player is disabled and the sprite
   freezes on whatever frame it was on, for 0.55 s. I had assumed the reaction
   covered this; the reaction is an overlay at the session level and the
   character does nothing. That is new wiring, not a texture swap, and it is why
   the death pose is in the required eight while the celebration is not.

**Human / Claude / model:** the two documents were drafted by Claude from
measurements of my build; every number in them names the file and lines it came
from, and I spot-checked the line references. The three findings above are
Claude's, found by reading the code rather than by asking me. The decisions they
feed — eight required poses, scarf mandatory, sword stays code-drawn, tuning
frozen — I am accepting, and the reason I am accepting the frozen tuning is that
the assignment compares the slice before and after its assets, so moving a
gameplay number at the same time would measure two things and prove neither.

**Still unresolved:** which generator to use for the art and the sound effects.
It has to record a seed, which Suno could not, and that is the one requirement I
am treating as non-negotiable after the music turned out to be unreproducible.

**Traceability:** `CHARACTER-SHEET.md`, `CHANGE-BRIEF.md` revision 2.0.0.

---

## 2026-10-04 — the music cannot be downloaded, and the counter I kept was fiction

**What happened.** I went to download the finalist and Suno says the download
allowance is already used up. I have not downloaded anything for this project.

**Why.** Suno changed its free plan on 2026-09-03 to seven downloads **for the
life of the account**, and applied it **retroactively**. Anything I ever
downloaded on that account — long before this course — is counted. The account
was not clean on the day the project started, and I never checked that it was.

**The part that is mine to own.** `ASSET-LOG.md` has carried a hand-maintained
counter reading "0 used, 7 remaining" since the first entry. That number was
never verified against the account; it was an assumption written in the
confident format of a measurement. A table with two numbers in it looks like a
fact, which is exactly why it went unchallenged for three days. **The counter
is left standing in the file with the correction above it**, because deleting it
would hide the one interesting thing here: the log was wrong in the direction of
making the project look safer than it was.

**What is actually lost, stated precisely.** Eight generations, a decided music
direction judged by ear, and a written argument for why direction B beat
direction A on the first wording while A lost over four. All of that is still on
the record and still counts. What is lost is **one audio file**. The design work
survives the tool; that distinction is worth noticing, and it is an argument for
keeping the reasoning in the log rather than only the asset.

**What this does not change.** `CONCEPT.md` revision 1.1 — driving, around
124 bpm, the score supplies the pressure — stands. It was a decision about the
game, not about a vendor. The replacement loop is judged against the same
revision, which is what a written direction is *for*.

**What it does change.** The "prefer a seeded tool" requirement, which
`CHARACTER-SHEET.md` section 8 and `ASSET-LOG.md` both already carried as a
preference for the art and the sound effects, is now **binding on the music
too**. The reason has gone from "the log would be nicer" to "the file has to be
mine once it is generated". Those are different arguments and the second is the
stronger one.

**Human / Claude / model:** I hit the wall. Claude checked what actually changed
at Suno rather than guessing, found the 2026-09-03 retroactive change, and
corrected the log the same day by appending rather than rewriting. Which
generator replaces it is mine to decide; the shortlist and the reasons are
Claude's.

**Traceability:** `ASSET-LOG.md` correction dated 2026-10-04.

---

## 2026-10-04 — a dungeon, and the contrast table I got backwards

**Wanted:** the game to look like a dungeon instead of a bright outdoor slope.

**Decided: a dungeon**, and it went into the build the same day.

**The part worth writing down is not the decision, it is what the decision
exposed.** `CHARACTER-SHEET.md` section 3 opened with "the body is effectively
invisible against the platforms it stands on", quoting 1.12:1, and I built a
whole rule set on it — the scarf is mandatory, the outline is non-negotiable.
The arithmetic was right. **The claim about the game was wrong.**

Platforms here sit at y 320 and are 64 tall. The character's body is 28 px
above its feet. Standing on the floor it occupies 292–320; the platform
occupies 320–384. **They never touch.** The character's background is the
backdrop, essentially always, and against the cream sky that was 10.03:1. The
crisis I wrote a specification around almost never happened.

I only found it because the dungeon forced the question *what is actually
behind the character* — which is the question that should have come before the
table, not two days after it. A number measured correctly and a claim about the
game are different things, and a table makes the second look like the first.
The sentence stays in the file with the correction under it.

**And then it became true.** The dungeon wall takes the backdrop from 10.03:1
to **1.60:1**. Worse than the number I had been calling the crisis, and now it
happens constantly.

**So the fix had to come with the setting, not after it.** Three things, all
measured before anything was drawn:

1. **The rim inverts.** The outline was `shade` — 14.12:1 on a cream sky,
   **1.14:1** on a dungeon wall. It becomes `steel_edge`: 7.31:1 against the
   wall and 4.57:1 against the body it outlines. It was already one of the
   eight colours, so the dungeon cost no new colour at all.
2. **The floor reads from its lit top edge.** The stone body is 1.43:1 against
   the wall — the floor would be invisible, which is a fairness bug under
   pillar 2, not a style complaint. The 4 px cap goes teal → torchlit warm,
   6.96:1.
3. **The background is made the quietest thing on screen** — mortar 1.18:1,
   arches 1.10:1. Strong contrast is spent only on what the player touches.

**What the screenshots caught that I could not.** The first torch glow was four
nested translucent discs. Rendered, that is visible ring banding — it looks
cheap. Sixteen discs is smooth. Nothing in the source said so. Second time this
project that rendering and *looking* beat reasoning about the code.

**The timing was luck, and I should say so.** This cost almost nothing because
**no environment art had been generated yet**. Two days later it would have
thrown the environment assets away. That is an argument for the order the
assignment asks for — specs before generation — and I only half followed it
with the music.

**What I am not pretending.** Revision 2.0.0 of the brief said the before/after
comparison would isolate the assets, because every gameplay number was frozen.
The numbers *are* still frozen — 79 checks pass unchanged. But the setting
moved, so the comparison is no longer "same game, new art". The film has to say
that out loud instead of letting a dungeon be mistaken for what generation did.

**Human / Claude / model:** the setting is mine. Claude researched the genre,
found the contrast inversion before anything was drawn, caught its own earlier
overstatement, wrote the code, and verified it with the suite and with rendered
frames rather than by assertion. The reference games I was shown — and the rule
that none of their names may appear in a prompt — are the assignment's rule,
followed.

**Still unresolved:** what the music does during the 0.55 s retry. Unchanged
since 1.1. The loop is in the project now but nothing plays it yet.

**Traceability:** `CONCEPT.md` revision 1.3, `CHANGE-BRIEF.md` revision 2.1.0,
`CHARACTER-SHEET.md` section 3b and its correction, `evidence/screens/`.

---

## 2026-10-04 (later) — the music is in the game, and two things that looked like bugs

**Wanted:** the loop actually playing, and a mute key, so the seam can be judged
by ear in the place it will be heard instead of in Audacity.

**Both done.** Music on its own bus, mute on `0`, eighty-seven checks passing.

**The line that took the most thought is one `if`.** `restart_attempt()` runs
on *every* death. Calling `music.play()` there restarts the loop at bar 1 every
0.55 s, which is worse than silence. The guard has to resume, not restart.

**And the guard was still wrong, which only probing found.**
`AudioStreamPlayer.playing` reports **false** while `stream_paused` is true. So
`if not music.playing: music.play()` did the right thing for an ordinary death
and the wrong thing for *pause → R*: the track jumped back to the top. I would
not have found that by reading the code, because the code reads correctly. I
found it by printing what the engine actually reports in each state before
writing the assertions. The case is a named regression check now.

**The second thing was not a bug at all, and I spent ten minutes on it.**
Re-running the screen captures produced three of six frames and exited cleanly
— exactly what a regression from the music change would look like, and I went
looking for it there. It was `--quit-after`: it counts **process iterations**,
not physics ticks, and a windowed run renders uncapped, so six thousand
"frames" can burn in nine seconds while only about four hundred fifty physics
ticks have happened. The headless run completing is what isolated it.

Worth writing down because the mistake was not technical. I had just changed
the audio, so when something broke I looked at the audio. The thing that
actually settled it was running the *same script* in a different mode and
getting a different answer, which is a question about the harness, not about
the feature.

**`[TZ DECIDE]` #3 is finally answerable.** Since revision 1.1 I have been
deferring "what does the music do during the 0.55 s retry" on the grounds that
it cannot be judged until the loop is audible in the game. It is audible now,
and it is implemented the simplest way: **it keeps playing.** Ducking is a
bus-level change and should be made against something heard rather than
imagined. That decision is now mine to make with my ears, not on paper.

**Still owed, and it is mine:** the listen. `CHANGE-BRIEF.md` C4 says play the
loop three times and listen at the seam before it goes near the project, and
the file went in first. The seam measured at the 10th percentile of the track's
own frame-to-frame change, which is a strong number, but a number is not an ear.

**Human / Claude / model:** Claude wrote the wiring, the tests and the
documents, found the `stream_paused` bug by probing the engine rather than
trusting the API's name, and corrected its own misdiagnosis of the capture
script. The retry behaviour, the loop choice and the seam are mine to judge.

**Traceability:** `CHANGE-BRIEF.md` revision 2.2.0, `ASSET-LOG.md` 2026-10-04,
`evidence/screens/10-muted.png`.

---

## 2026-10-05 — the character got a body, and the rim had to stop being an outline

**Wanted:** the same purple-scarf ninja, but finer, with the head, torso and
four limbs tellable apart.

**Done.** Head with a neck, a chest that tapers into a darker abdomen, two
arms in three parts each, two legs in three parts each, gauntlets and boots.

**The first thing I learned is that it had no arms at all.** The shipped figure
was a helm, a torso, two shoulder triangles and two leg stubs. It read as a
person at 18 × 28, which was enough for Assignment 1 and stops being enough the
moment the character is the subject of a pose sheet.

**The first attempt failed, and it failed arithmetically.** I added limbs and
kept the rim as it was — 1 px grown on all four sides. Rendered, the figure was
**grey pipework with a hint of navy down the middle**. The reason is a
subtraction I had not done: an all-sides rim costs a part 2 px of width, so a
3 px arm keeps 1 px of armour and a 4 px leg keeps 2. The three-value scheme
meant to separate near limb from far limb had nowhere to happen. Nothing in the
source said this. I only saw it in the contact sheet.

**The fix was to stop thinking of the rim as an outline.** It is now
directional — 1 px toward the back and 1 px up, nothing on the front or the
underside. That costs **zero** width, and it is more honest about the setting
anyway: in a dungeon the light comes from a torch above and behind, not from
everywhere. And because `x` is measured forward and gets mirrored, the rim
stays on the same side of the body when the character turns around, which is
what a light source does and what an outline does not.

**The second bug was a sign.** `y` is negative upward, so lifting a leg has to
*subtract*. I added. The boot went to y +0.8 — below the feet line, into the
floor — and the shin's height computed as `3.2 - tuck` = 0.6 px. The jump frame
rendered as a glitch. Also found by looking.

**The two pixels that did the most work** are the neck. Without them the helm is
just the top of the torso, and no amount of detail inside the head fixes it.

**One structural thing I am glad I did.** The body is a parts list now, and the
rim pass and the paint pass walk the **same array**. The old code listed eight
shapes twice, once for each pass, with nothing stopping the copies drifting. It
was fine because one person wrote both lists in one sitting; it was not fine as
a thing to keep editing.

**What this says about my test suite, and I would rather write it down than
have it noticed for me.** Eighty-seven checks pass and both of this revision's
bugs sailed through all of them, because **every check in the suite is about
behaviour** — where the hitbox is, whether the trap is drawn, whether an enemy
is at its live position. **Nothing asserts what the player looks like.** The
honest answer is not to add a pixel-diff of the player, which would fail on
every intentional art change and get deleted within a week. The honest answer
is that the character captures plus the contact sheet **are** the check, and
they need a human to look at them. That is a weaker guarantee than the rest of
the suite and the film should not pretend otherwise.

**Human / Claude / model:** the brief is mine — keep the purple scarf, make it
finer, separate the limbs. Claude did the geometry, found the rim arithmetic
and the sign error by rendering and looking rather than by reasoning, and wrote
the documents. No generated art is involved: this is still original vector
drawing in code, which is also why it could be iterated three times in an hour.

**Traceability:** `CONCEPT.md` revision 1.4, `CHANGE-BRIEF.md` revision 2.3.0,
`CHARACTER-SHEET.md` section 3c, `evidence/screens/char-contact-sheet.png`.

---

## 2026-10-05 (later) — a body on the floor, and four sounds I did not generate

**Wanted:** both of the two things still blocking the slice — a death pose, and
sound effects.

**Got one of them properly and one of them honestly.**

### The death pose

Flat, face down, head the way it was going, as I drew it on sheet frame 7. The
thing that surprised me is how little it took: **the whole pose rests on the
visor being a band along the BOTTOM of the helm.** Put it on the side and the
character is asleep. Put it underneath and it is face down in the floor. One
inversion.

The other half of why it works is that it is **the only pose in the game wider
than it is tall** — about 26 × 9 against 18 × 28 standing. At the size this
game draws at, that is worth more than any amount of detail, because you can
tell it apart without reading a single pixel.

### The sound effects, and what I am not going to pretend about them

**I did not generate them.** They are synthesised by arithmetic in a script —
closed-form waveforms and one seeded noise array. **They do not satisfy the
assignment's "generate sound" requirement and nothing in this repository claims
they do**: `ASSET-LOG.md` opens its sound section with that sentence and
`godot/assets/README.md` has a "Generated?" column that reads *no* four times.

**Why I did it anyway.** Revision 1.1 of CONCEPT made a prediction back on
10-01 — that a 124 bpm bed with pulsing bass would drown the trap's 15-frame
warning — and CHANGE-BRIEF turned it into the only check in this project that
cannot be automated, because masking is perceptual. **And it cannot be run
against silence.** So the choice was: wait for a generator and run the check
once at the end, or put something audible in now and run the check twice, with
the second run comparable to the first. The second is better and it is not
close.

The replacement is file-for-file. No trigger, no assertion, no level and no
balance changes when the generated versions land.

### The one sound that had a brief to answer

`SFX-TRAP` is not a guess. Revision 1.1 did not only predict the masking, it
specified the fix in advance: **a moving pitch, which percussion does not
have**, so the warning is told apart by motion rather than by volume. So it is
a rising sweep, 420 → 2100 Hz, with partials at inharmonic ratios so it reads
as struck metal rather than as a note the score could swallow, and its
amplitude **rises** instead of decaying, because the hazard is still arriving.
0.260 s, which is 15.6 frames — the sound lasts exactly as long as the warning.

Writing the prediction down four days ago is the only reason that sound has a
design instead of a vibe.

### The thing I am most pleased about is a number

`sfx_log` records which effect fired on which tick. The trap check now reads:
**warning at tick 24 with the player at x 1064.6, death at tick 59, lead 35
ticks** against a 15-tick rise. The fairness argument of the whole slice —
*you were told before it could kill you* — is in the suite as an integer
instead of in a paragraph as a claim. That is the first audio assertion here
that would catch a real design mistake rather than a missing file.

### A claim I had to walk back within the hour

The synthesis script's first docstring said the OGGs were byte-reproducible.
They are not: an Ogg page header carries a stream serial number ffmpeg picks at
random, with no flag to pin it. I checked instead of arguing — decoded both
runs to raw PCM and compared — and all four match byte for byte. So the
reproducible thing is the waveform and an OGG hash fingerprints one encode. The
corrected wording and the exact commands are in the script.

Small, but it is the same mistake as the download counter: a confident sentence
about reproducibility that nobody had tested.

**Human / Claude / model:** the death pose is my drawing, implemented by Claude.
The sound-effect *design* for the trap is CONCEPT revision 1.1, which was my
decision about the music and Claude's working-out of what it cost. The
synthesis, the wiring, the eight tests and the documents are Claude's, and so
is the decision to label the audio as not-generated rather than let it pass.
Running an actual generator is mine and still outstanding.

**Traceability:** `CHANGE-BRIEF.md` revision 2.4.0, `ASSET-LOG.md` sound-effects
section, `scripts/synth_placeholder_sfx.py`, `godot/assets/README.md`,
`evidence/screens/02-failure.png`.
