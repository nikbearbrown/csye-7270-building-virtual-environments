# Second-pass check of one film's narration

A narrated film is being made from ONE terminology slide deck for the course CSYE 7270, Building Virtual Environments (making games with Godot, Blender and an AI coding agent). Another writer wrote the narration. Students will study from it, so a wrong definition or a wrong example does real harm. You are the independent second reader: check every spoken sentence against the slide and the reference files, and correct what is wrong. You did not write it; do not assume it is right.

COURSE = `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments`. FILMS = `COURSE/youtube/exam-prep-deck-films`. Your deck number NN, the deck file and the reference files are in your task. Never open a folder named `4TAs`.

## Read first

1. `FILMS/NARRATION-BRIEF.md`: the rules the narration had to follow (how the film works, the voice rules, the example rule, the output format).
2. `FILMS/extract/NN/narration.json`: the narration under review.
3. `FILMS/extract/NN/deck.json`: for every slide and click-step, `new_texts` (what the step adds), `all_texts` (everything on screen after it), the slide's `notes`, `evidence` badge and `picture`.
4. The stills `FILMS/extract/NN/stills/sSS-kK.jpg` (Read tool). Look at one whenever the words alone do not settle what is on screen.
5. The reference files, for what a term means in this course and what the Walker game really contains. Chapter files may have merge-conflict markers; ignore them.

## What to check, beat by beat

For every body beat `(slide, step)`:

- **True to the slide.** Every number, label and relationship spoken is on the slide at that step. Nothing is said about a later step's content as if it were visible now.
- **True to the course.** The term means what the slide entry and the reference files say it means. Watch for a definition that has drifted into a neighbouring term (the decks exist because these terms are easy to confuse), a direction reversed (which object scans which, which stage runs first, which way a value moves), a cause and effect swapped, "always" where the source says "can", or a general claim the source makes only for one engine or one case.
- **The example is a true instance.** Each term's example must be a real case of that term, and must not fit the slide's TELL THESE APART look-alike or a neighbouring term in the same deck better. A vivid example of the wrong term teaches the wrong answer. Check any direction in it. It must invent no numbers (only figures on the slide at that step), and no named commercial games, studios or people that are not on the slide or in the reference files. What it says about Walker must match the reference files.
- **Honest about evidence.** Numbers from a slide badged Illustrative data or Simulation are not presented as measurements of a real game. Scope limits in the slide's `notes` (illustrative values, a title to confirm, documentation only, an engine not run for the course) are respected.
- **Engine facts.** Where the narration states how Godot, Blender, Unity or Unreal behaves, it says no more than the slide, its note and the reference files support.
- **Brief rules.** No "this chapter", "the book", "slide", "click", no chapter, episode or video numbers, no source video or book named. Nothing says or implies a term will be on an exam.

Also check `opening_summary`, `idea` (after the swap, is the sentence true and is it this film's point?), the six `recap_lines` (each must restate something the body said; nothing new), `your_turn` (the terms it names are terms this film teaches), and each `say_as` entry (run `python3 FILMS/tools/say.py "<term>" "<say>"`: the respelling must read as the term should be spoken).

## What to do about a problem

Fix it in `narration.json` yourself, changing as little as possible: one sentence, one number, one word. **Do not rewrite for style, rhythm or taste**, and do not swap a good example for one you prefer. A beat that is correct and merely plain stays as it is. Keep every voice rule (numbers as words, no symbols, the `figures` list still accurate) and keep the checker passing:

```
python3 FILMS/tools/check_narration.py FILMS/extract/NN
```

If you cannot tell whether something is right (the slide and the reference files disagree, or neither settles it), do not guess: leave the beat, and list it under `unresolved`.

## Output

Write `FILMS/extract/NN/verify.json`:

```json
{
  "deck": "NN",
  "beats_checked": 50,
  "corrections": [
    {"slide": 4, "step": 2, "was": "the full old narration", "now": "the full new narration", "why": "one sentence: what was wrong and what settles it (slide text or reference passage)"}
  ],
  "bookend_corrections": [{"field": "recap_lines[3]", "was": "...", "now": "...", "why": "..."}],
  "unresolved": ["slide 9 step 3: the slide says X, the chapter says Y; narration follows the slide"]
}
```

Empty lists are a fine result if the narration holds up; do not manufacture corrections. Then, only if the checker prints PASS, create the empty file `FILMS/extract/NN/READY`.

Write only `narration.json`, `verify.json` and `READY`. Do not edit the deck, the extract, the tools or anything else, and do not delete, commit or publish anything. Your final message: the checker's last line, the number of corrections, and each correction and unresolved item in one line.
