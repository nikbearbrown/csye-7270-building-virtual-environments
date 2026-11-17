# CSYE 7270 Midterm Coach: change log, v2.0 → v2.1 (2026-11-17)

**Summary.** The coach failed because the cheat sheet wasn't in the Project. The sheet already existed. All 62 of its slide citations match the decks, so none needed correcting. Its "Not on this exam" list gained the items the instructions already treat as off the exam. v2.1 adds a missing-sheet rule, resolves the nine command clashes listed in the spec, and fixes five more clashes found while checking. To use it: upload `knowledge/EXAM-CHEAT-SHEET.md` to the Project files and paste `CLAUDE-PROJECT-INSTRUCTIONS.md` into the Project instructions. Both files were corrected in place, at the same paths as before; there are no separate version files.

## Files
- **Instructions:** `glossary/exam-coach/CLAUDE-PROJECT-INSTRUCTIONS.md`, now v2.1, replacing v2.0 at the same path.
- **Sheet:** `glossary/exam-coach/knowledge/EXAM-CHEAT-SHEET.md`, corrected at the same path. It was never uploaded to the Project, which is why the coach failed.
- **Custom-GPT instructions:** `glossary/exam-coach/GPT-INSTRUCTIONS.md`, corrected the same way (see the end of this log).

## Sheet: slide citations
All 62 citations were checked against `glossary/decks/*.html` for deck number, deck name, slide number and slide title (the slide's heading). **62 of 62 match; none corrected.**

## Sheet: other changes
- "Not on this exam": added "Unity and Unreal: the course and the exam are Godot only". It was only implied, through "Decks 21 to 25".
- "Not on this exam": "The Godot shading language, GDScript, or any code" is now "Any code: GDScript, the Godot shading language, node class names, and built-in names (such as `COLOR` or `SCREEN_UV`)".
- "Not on this exam": game AI now names decks 19 and 20 by subject (perception, pathfinding and decisions).
- Already present, unchanged: detailed PBR parameters, maps and workflows; the PBR-based No-Bake system; game AI.

## Sheet against the instructions' fixed references
| Reference in the instructions | On the sheet? |
|---|---|
| Topic 14 includes PBR | Yes: "Materials, textures and PBR (general idea only)" |
| Topic 17 is rigs | Yes: sprite-based and rig-based animation, skin and skin weights |
| Topic 19 covers curves, timing and spacing | Yes |
| Topic 23 is state machines | Yes |
| Deck 15 slide 5 draws ease-in, ease-out, ease-in-out | Yes: "Easing from first principles", a progress-against-time curve; its notes give all three formulas |
| Deck 15 slide 6 shows timing and spacing | Yes: "Timing, spacing, frame rate and speed scale" |
| Deck 15 slide 11 is "Rig, rest pose and skinning weights" | Yes |
| Critical topics: sprite vs rig and skin; shaders; camera pan, tilt, roll | **Partly.** The sheet marks only topic 17 and the pan, tilt and roll part of topic 24 as critical, not shaders. **Instructions changed to match** (Mode 3 coverage). If shaders should be critical, mark topic 13 critical on the sheet and restore it. |

## Instruction changes (the ten asked for)
1. **Missing sheet:** new MISSING-SHEET RULE at the top of "Rules for everything you do". It gives a fixed reply (sheet not loaded; can't list topics, quiz or make an exam; ask Professor Bear) and allows nothing from memory. Only the help response (with that line added) and the pushback replies still work.
2. **"quiz":** a bare "quiz" now means "question" (Mode 2). "exam" and "test" are the full exam (Mode 3). "quiz me" stays Mode 2.
3. **"help":** one help response, the three modes and then the command list. Used on a new chat, on "help", and on any unknown single word.
4. **"topics" vs "What's on the exam?":** both list the 24 topics under the six parts. "topics" stops there. "What's on the exam?" adds the "Not on this exam" list and the offer to explain a topic or make a cheat sheet.
5. **"hint":** may restate the idea in other words, or define a scenario term in plain words from the sheet. May not name the topic, a deck or slide, the number of true statements, whether any statement is true, or rule a statement in or out. One per question. Doesn't change the score, but the tally marks it "(hint)". None for a full exam. With no open question, says so.
6. **"drill <topic>":** two questions numbered 1 and 2. The student answers both ("1: A, D / 2: B") or skips. Grading waits for both, then comes in one message: a score and a table per question, a total out of 10, and "Where to study" once.
7. **"another":** "type" is now defined as words-only or picture (in "The exam format"). "another" keeps the type and changes the topic and setting; picture topics are 17, 19 and 23. With no earlier question, it acts as "question".
8. **Pictures in the printable exam:** every drawing, in chat and in the exam, is a plain-text diagram in a fenced code block, at most 60 characters wide. It renders and prints from one markdown file, and sits under its question's scenario and above its statements. The SVG-in-a-separate-artifact instruction is gone.
9. **"key" with no exam:** checked in order. An open unanswered question gets "reply first or skip". Otherwise the exam key, if an exam was written. Otherwise "no practice exam yet", with an offer. For a single question, the Step 3 feedback is its key.
10. **Title:** v2.1.

## Other contradictions found and fixed
- **Answers read as commands:** "any unknown single word shows the help list" would have caught one-word answers such as "B" or "none". While a question is open, letters are now an answer, never a command.
- **"next" undefined:** Mode 2 listed "next" as a trigger, but the short commands didn't define it. It now means the same as "another".
- **"another" vs Mode 2:** Mode 2's own topic and type rules contradicted the short command. Mode 2 now defers to the short command for "another" and "next".
- **"case" in two places:** "case" is now a Mode 2 trigger as well as a short command, with the same behaviour (says there are no case questions, then gives one question).
- **Hints vs the answer-last rule:** the ANSWER-LAST RULE now names the requested hint as its only exception. Mode 2's "no hint" means no unrequested hint.
- **Category rule vs topic requests:** NEVER NAME THE CATEGORY now holds even when the student chose the topic (drill, "quiz me on rigs").
- **Full-exam answers:** there was no path for a student who sends their exam answers. Mode 3 now grades them against the key.
- **"cheat sheet" vs "cheatsheet":** both trigger the same Mode 1 behaviour, and "cheatsheet <topics>" limits it to those topics.
- **"explain" on an off-sheet topic:** it now follows the ON-THE-SHEET RULE.
- **Topic 4 marked "(picture questions)" on the sheet:** the coach can't draw the editor. The picture section now says so explicitly and keeps interface questions in words.

## Walk-through (v2.1 with EXAM-CHEAT-SHEET.md as the only Project file)
| Input | Rule that applies | Needs from the sheet | Result |
|---|---|---|---|
| help | Help response (Mode 1) | nothing | OK |
| topics | "topics" (Mode 1) | six part headings, 24 topic names | OK |
| question | Mode 2 | topics, Know lines, slides | OK |
| another | Short commands: another | the last question's type; picture topics 17, 19, 23 | OK |
| hint | Short commands: hint | Know line for a definition | OK |
| drill rigs | Short commands: drill | topic 17 | OK |
| drill unity | drill → "Not on this exam" | Unity line on the list | OK (line added this version) |
| exam / test | Mode 3 | six parts; critical marks on 17 and 24 | OK |
| quiz | Mode 2 (bare quiz = question) | as question | OK |
| key, with an exam | key step 2 | slides for "where to study" | OK |
| key, no exam | key step 3 | nothing | OK |
| key, question open | key step 1 | nothing | OK |
| cheatsheet | Mode 1 cheatsheet | Know lines, slides, OUT list | OK |
| case | Short commands: case → Mode 2 | as question | OK |
| unknown word ("banana") | Help response | nothing | OK |
| "what's on the exam?" | Mode 1 | 24 topics, OUT list | OK |
| "quiz me" | Mode 2 | as question | OK |
| "explain shaders" | Mode 1 explain | topic 13 Know line and slides | OK |
| any request, sheet missing | MISSING-SHEET RULE | nothing | OK; help still works, with the missing-sheet line added |

## Custom-GPT instructions (`GPT-INSTRUCTIONS.md`)
Rewritten to match, within the GPT's 8,000-character limit. It now has the missing-sheet rule, the merged help, a bare "quiz" as one question, "topics" vs "what's on the exam", the bounded hint, the drill answer format, "another"/"next" by question type, "key" in order, letters as answers, text-diagram pictures, and critical topics as on the sheet.

## Also corrected
- `glossary/EXAM-CHEAT-SHEET-FULL.md`, the source the knowledge sheet is built from: its "Not on this exam" list now matches the corrected sheet.

## Not changed
- No practice questions were written. No slides were changed.
