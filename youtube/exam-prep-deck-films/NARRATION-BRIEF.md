# Narration brief: one terminology deck becomes one narrated film

You are writing the spoken script for ONE film in the YouTube playlist **Building Virtual Environments, Exam Prep** (course CSYE 7270, Building Virtual Environments, Professor Nik Bear Brown: making games with Godot, Blender and an AI coding agent). The film plays a terminology slide deck, animation by animation, while a narrator named Liam explains what is on screen. You write the words Liam says. You do not render anything and you do not edit the deck.

Everything lives under
`/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/` (called COURSE below). FILMS = `COURSE/youtube/exam-prep-deck-films`. Your deck number NN, the deck file and the reference files are given in your task.

## What you are given

- `FILMS/extract/NN/deck.json`: every slide and every click-step of the deck. For each step: `new_texts` (the words that step adds to the picture), `all_texts` (all words on the picture after the step), `anim_ms`, and `still` (a 1920x1080 picture of the slide after the step). Each slide also has `title`, `eyebrow` (its group), `evidence` (the badge: Computed, Simulation, Illustrative data, Conceptual illustration), `notes` (the deck author's speaker note), `source`, and `picture` (a plain description of the drawing).
- `FILMS/extract/NN/stills/sSS-kK.jpg`: the stills. **Look at them** (Read tool): at least the last step of every slide, and any step whose words alone do not tell you what the picture shows. You must know what the viewer is looking at to explain it. Two limits of the extract: `new_texts` is a plain difference of the words on screen, so a word that was already printed is not listed again (use the still to see what a step really adds, for example on a checklist that prints every line at step one and then marks them one by one); and a still is the END of a step, so for a step that means something only in motion (a value edited, dots merging) read its render function to know what moves. Numbers that appear only mid-animation are not in `all_texts` and are not spoken.
- The deck itself (path in your task). The term dictionary is the `var T = {...}` object; each `renderXxx(el, k, anim)` function draws one slide, and `k` is the step. Read the render function when a still is unclear.
- The reference files named in your task (course chapters, the course glossary, source notes). Use them to understand a term the slide states too briefly, and for what the course's own game, Walker, actually contains. Chapter files may contain unresolved merge-conflict markers; ignore them. **Never open anything in a folder named `4TAs`.**

## What the film is

One slide = a short run of beats. **One click-step = one beat = one narration.** When a beat starts, the step's animation plays (about half a second to several seconds), then the picture holds while Liam finishes. The deck's opening title slide (slide index 0, no steps) and its red section slides (no steps) are not narrated.

So you write one narration for every `(slide, step)` pair in `deck.json` where the slide has steps. Nothing is skipped and nothing is merged.

## Who is speaking, and how

- **Liam, in for Professor Bear.** Liam is a stand-in narrator. He refers to the professor in the third person as "Professor Bear" and never claims to be him. He rarely needs to mention him at all.
- **Register: plain, direct, calm.** Short sentences written for the ear. No hype, no cheerleading, no rhetorical flourishes, no "let's dive in". A student should be able to repeat the sentence in an exam answer.
- **Explain, do not read.** The slide already shows the term and a one-line meaning. Liam says what the term means in plain words, points at the picture ("the red box", "the ball on the left", "the bar on the right"), and where it helps says how to tell the term from its look-alike (the TELL THESE APART box). Do not recite the slide's definition line word for word.
- **Say the exact term.** Each beat names the term or terms that step adds, spelled exactly as on the slide, at least once. Exams reward the exact term.
- **The first step of each slide** starts with a few words that say what the picture is, so the viewer is oriented.
- **Self-contained.** The viewer may have read nothing and watched nothing else. Never say: this chapter, the chapter, the book, the deck, slide, click, "as we saw", last or next video, or any chapter, episode or video number. Do not name the source videos, books or manuals the slide cites; teach the term as the course's term. If a term leans on another idea, say that idea in a clause.
- **Honest about the numbers.** If the slide's badge is Illustrative data or Simulation, do not present its numbers as measurements of a real game. Say "in this made-up example" or "in this simulated run" once per slide where numbers are spoken. If the deck's notes say something is illustrative, unconfirmed, drawn from documentation only, or that an engine was not run for the course, respect that: never claim more than the note does.
- **No new facts.** No study, product, studio, person, date or number that is not on the slide, in its note, or in the reference files. A plain everyday rewording of the idea is fine.
- **Exam talk.** You may say that the exact term matters. Never say or imply that a particular term will be on an exam, and never describe an exam.

## Abstract first, then an example, for every term

Professor Bear's rule for these films: "Once you say something abstractly, then give it an example." It is fine for the film to be long.

- **Every term gets one.** For each beat that introduces a term (a step whose `new_texts` add a term entry), the beat first says what the term means, then ends with one concrete example, introduced with "For example," or "Picture ...". A beat that adds two terms gives one short example for each, or one example that shows both.
- **From making a game.** Draw examples from the course's own work: the Walker game and games like it (a player character, a platform, a coin, a hazard, an enemy that patrols, a goal, a level, a sprite sheet, a jump, a camera, a sound, a menu, a playtest), and the work of building them with Godot, Blender and an AI coding agent (a scene file, a test run from the command line, an instruction to the agent, a model exported from Blender, a shader on a sprite). Use the reference files to keep Walker details true. If the picture on screen already is a concrete case of the term, point at it and add one sentence that carries it to a game a student might build.
- **Concrete** means a specific situation a student can picture: a thing in a game, a file, a decision, a tool doing a particular thing. "A coin that plays a sound when the player touches it" is concrete; "an object in some game" is not.
- **True to the term.** The example must be a real instance of the term as the slide entry and the reference files define it, and must not fit the slide's look-alike (its TELL THESE APART box) or a neighbouring term better than the term itself. This is the most important rule: a vivid example of the wrong term teaches the wrong answer.
- **Vary them.** Do not reuse the same situation for every term.
- **No invented facts in examples.** No numbers in an example unless that exact figure is on the slide at that step. No named commercial games, studios or people unless they are on the slide or in the reference files. A plain made-up situation is fine.
- Beats on the map slide (the first slide with steps), the look-alike pairs, "Say it exactly" and the closing checklist do not need an example unless a term in them would otherwise be left abstract.

**Length:** a term beat is 45 to 85 words. A map, pairs, say-it-exactly or checklist beat is 20 to 50 words. A step that adds no term but shows a further idea about one (an override, a comparison) is treated as a term beat, with an example. Never under 16 or over 90 (the checker fails those). Counting what is drawn ("three boxes", "the fourth group") is fine and needs no entry in `figures`; `figures` is for values printed on the slide.

## Writing for a text-to-speech voice (Kokoro)

- **Spell every number as words**: "ninety-nine percent", "zero point six", "nine hundred sixty pixels per second squared". No bare digits anywhere in any narration field.
- **Only speak numbers that are on the slide at that step.** For each beat list them in `figures` exactly as they appear on the slide (a substring of one of the step's `all_texts`), for example `"figures": ["0.81 s", "960 px/s²"]`. The checker verifies each one is on the slide. If you round, still list the slide's figure. A beat that speaks no number has `"figures": []`.
- **Engine names keep their spelling.** A class or node name that the deck prints somewhere may be written exactly as printed, digits included: `Area2D`, `CharacterBody2D`, `Sprite2D`, `AnimationPlayer`, `GPUParticles2D`. The voice reads these correctly. This is the only place a digit may appear.
- **Code and file names are said in words.** No underscores, brackets, slashes or dots inside a name. Write "move and slide" for `move_and_slide()` (the checker allows the word there), "the physics process function" for `_physics_process`, "the player scene file" or "a file ending in dot t s c n" for `player.tscn`, "the res prefix, written res, colon, slash, slash" for `res://`. Units in words: pixels, seconds, decibels, hertz, frames per second.
- **No symbols**: none of `( ) [ ] | = % $ + / * < > _ # @ &` and no arrows or long dashes. Write "does not equal", "divided by", "to the power of".
- **Acronyms**: write them as on the slide (GDD, UV, PBR, MCP, VFX, HUD). The first time one is spoken, give its expansion in the same breath ("GDD, the game design document"); the standard expansion of a standard acronym is allowed even where the slide does not print it.
- **Check the voice.** Run `python3 FILMS/tools/say.py "IK" "glTF" "A star"` on every acronym, engine name and unusual word you use; it prints how the voice will read each one. If a reading is wrong (an acronym read as a word, as with IK or AABB; the letter A read as "uh"), find a plain respelling that the tool reads correctly ("I K", "ay star") and add it to `say_as`: `{"term": "IK", "say": "I K"}`. The narration keeps the normal spelling; only the voice changes. A `say_as` term must start and end with a letter or digit. Godot is already handled; do not add it.
- Avoid words the voice reads two ways: past-tense "read" (write "looked at" or "saw"), "lead" (the metal or the verb), "live", "tear", "wind", "minute" as an adjective, "close" as an adjective next to a verb use, "bass", "bow", "content". Prefer the unambiguous word.
- Commas, full stops and question marks only. No semicolons, and no colons inside narration beats except in the checks where the pattern below shows them.
- A single capital letter used as a name ("Pad A", "point A") is read as the article unless it ends its clause. Put it right before a comma or a full stop.

## The other pieces you write

1. `opening_summary` (8 to 40 words, one or two sentences). It is spoken on the title card right after the playlist name and the film title, so do not repeat either. Say what the film covers and why that is useful. Numbers as words.
2. `opening_description` (at most 52 characters): the short line printed on the title card under the title. Digits are fine here. Example: "34 terms for the Godot editor, scenes and signals."
3. `idea`: the second beat, where a writer types a sentence a newcomer believes and corrects one phrase of it.
   - `narration` (35 to 70 words) must begin exactly `Hallo. This is Liam, in for Bear.` Then the mistaken framing, the correction, and one sentence on what the film does about it (it goes through the terms, each one shown). Do not repeat the playlist or the title.
   - For a film of many terms, the main point can be the deck's lead look-alike pair, stated as a correction.
   - `text`: what the writer types, at most two lines (`\n`) and 70 characters. `triggerWords`: the phrase that gets deleted, verbatim inside `text`, no closing punctuation. `replacementWords`: what replaces it, no closing punctuation. After the swap the sentence must be true and must be the film's main point. Example: text `An Area2D\nblocks the player.`, triggerWords `blocks the player`, replacementWords `only reports the overlap`.
4. `recap_lines`: exactly six bare sentences (4 to 16 words, at most 84 characters each), in the deck's order, each restating one thing the film established. Nothing new. Numbers as words.
5. `your_turn`: a prompt the viewer can paste into Claude to practise this film's terms without the deck in front of them.
   - `command` (35 to 75 words): spoken aloud in full, so it obeys every voice rule above. It should make the viewer USE the terms, for example ask for short game-making cases one at a time where the viewer must name the exact term and say why its look-alike is wrong, with the answer withheld until they reply. Name six to ten of the film's terms inside the prompt.
   - `checks`: exactly two lines, each starting `Check: `, at most 78 characters, that the viewer uses to judge the result.
   - `segment`: a Title Case label of at most 40 characters, for example `Name The Term, Defend It`.

## Output

Write `FILMS/extract/NN/narration.json`:

```json
{
  "deck": "NN",
  "opening_summary": "...",
  "opening_description": "...",
  "idea": {"narration": "Hallo. This is Liam, in for Bear. ...", "text": "...", "triggerWords": "...", "replacementWords": "..."},
  "beats": [
    {"slide": 1, "step": 1, "narration": "...", "figures": []},
    {"slide": 1, "step": 2, "narration": "...", "figures": ["34"]}
  ],
  "recap_lines": ["...", "...", "...", "...", "...", "..."],
  "your_turn": {"segment": "...", "command": "...", "checks": ["Check: ...", "Check: ..."]},
  "say_as": [{"term": "IK", "say": "I K"}],
  "deck_problems": ["anything on a slide that looks wrong: a number that does not add up, a typo, a term defined two ways"]
}
```

Then run the checker and fix until it prints PASS:

```
python3 FILMS/tools/check_narration.py FILMS/extract/NN
```

Before you finish, reread every beat once against its still: does the sentence describe what is actually on screen at that step (not a later step), is the example a true instance of the term, and would it sound right spoken aloud?

Write only `narration.json`. Do not edit the deck, the extract, the tools or anything else, and do not create, delete, commit or publish anything. Your final message: PASS or FAIL from the checker, the body word count it printed, the `say_as` entries you added, and the `deck_problems` you found (or "none").
