# CSYE 7270 Midterm Coach (v2.1): Claude Project and custom GPT

**v2.1 (2026-11-17).** For the Claude Project, use `CLAUDE-PROJECT-INSTRUCTIONS-v2.1.md` and upload `EXAM-CHEAT-SHEET.md` (both in this folder). v2.0 failed when the sheet wasn't uploaded; v2.1 says so plainly instead, and fixes the command clashes. What changed: `CHANGELOG-v2.1.md`. The custom-GPT instructions are still v2.0.

**Executive summary.** This is a midterm study tool, in two versions that behave the same way: a Claude Project and a custom GPT. Students can do three things with it:
1. **Help:** ask what's on the exam, get a topic explained, or have it make them a printable cheat sheet.
2. **Quiz:** get one question at a time; the answer appears only after they've answered.
3. **Exam:** get a full 20-question practice exam to print, with the key only when they ask.

Everything it knows about the exam comes from one file, `knowledge/EXAM-CHEAT-SHEET.md`, which is the full cheat sheet from Bear's slide walkthrough on 2026-11-13, with his 2026-11-15 PBR scope correction. It is Godot only, asks no code, and follows the real format: 20 multiple-answer questions, five statements each, one to four of them true. It replaces the old Unity/Unreal-era tutor GPT and the v1 coach prompt (`../CLAUDE-PROJECT-EXAM-COACH-PROMPT.md`, written for the retired case-question exam).

**Status:** draft for Bear. It has not been tried in a live Claude Project or GPT. Don't give it to students until the "For Bear" box in `../EXAM-CHEAT-SHEET-FULL.md` is settled (see Caveats).

## Files

| File | What it is | Where it goes |
|---|---|---|
| `CLAUDE-PROJECT-INSTRUCTIONS-v2.1.md` | **Current.** The full instructions for the Claude Project | Project → custom instructions (paste the whole file) |
| `EXAM-CHEAT-SHEET.md` | **Current.** The exam sheet the coach reads: 24 topics, slides, and the "Not on this exam" list | Upload to the Project files (and to the GPT's Knowledge) |
| `CHANGELOG-v2.1.md` | What changed from v2.0, and the check of every command | Reading only |
| `CLAUDE-PROJECT-INSTRUCTIONS.md` | v2.0, superseded by v2.1 | Project → custom instructions (paste the whole file) |
| `GPT-INSTRUCTIONS.md` | The same rules, shortened to fit a GPT (under the 8,000-character instruction limit) | GPT → Configure → Instructions (paste the whole file) |
| `knowledge/EXAM-CHEAT-SHEET.md` | The 24 exam topics, each with what to know and the deck, slide number and slide title, plus the "Not on this exam" list. This is the student version: no "For Bear" box, and plain slide titles instead of links. | Upload to both, as Project knowledge and GPT Knowledge |

## Set up the Claude Project
1. claude.ai → Projects → Create project. Name: "CSYE 7270 Midterm Coach". Description: "Practice for the CSYE 7270 midterm: what's on it, one question at a time, or a full printable practice exam."
2. Set custom instructions: paste all of `CLAUDE-PROJECT-INSTRUCTIONS-v2.1.md`.
3. Add knowledge: upload `EXAM-CHEAT-SHEET.md` (this folder). Without it the coach can't work, and v2.1 says so.
4. Share it with the class (Team or Enterprise plan), or have students build their own from these three files.
5. Test it: start a chat and type "help", then "quiz me on rigs", then "make me a full exam".

## Set up the custom GPT
1. ChatGPT → Explore GPTs → Create → Configure.
2. Name: "CSYE 7270 Midterm Coach". Description: as above.
3. Instructions: paste all of `GPT-INSTRUCTIONS.md`.
4. Knowledge: upload `EXAM-CHEAT-SHEET.md` (this folder).
5. Capabilities: turn on **Code Interpreter** (it draws the picture questions). Image generation and web browsing can stay off.
6. Conversation starters: "What's on the midterm?" · "Quiz me on animation" · "Make me a cheat sheet" · "Give me a full practice exam".
7. Share as "Anyone with the link".

## What changed from the old tutor GPT
| Old GPT (Unity/Unreal era) | Now |
|---|---|
| 25% Unity, 25% Unreal, 25% vocabulary, 25% general | Godot only; topics come only from the cheat sheet |
| Code snippets (for example `OnCollisionEnter`) | No code at all, ideas in plain words |
| Weekly quizzes, 15-20 question midterm, 25-30 question final | One midterm: 20 questions × 5 statements, one to four true, 100 points |
| Answers hidden unless asked | Kept: in quiz mode the answer comes only after the student answers |
| Reasoning for all five options in a table | Kept: the feedback table covers all five statements |
| Category never revealed | Kept: the topic shows only in the feedback ("Where to study") |
| Scenario-based | Kept |
| Not in the old GPT | Cheat-sheet mode, a printable full exam with a separate key, picture questions (curves, timing and spacing, rig, state machine), and every answer points to the deck, slide and title |

## Dry run (2026-11-13)
A separate agent followed `CLAUDE-PROJECT-INSTRUCTIONS.md` and the knowledge file through a scripted chat: hi → quiz on rigs → answer → surprise picture question → skip → "quiz me on PBR" → full exam → key. Every rule held:
- The answer came only after the student answered or skipped, and no question named its topic.
- Under the scope at that time, PBR was turned down as "not on this exam", with two nearby topics offered instead. This result is historical and is superseded by Bear's 2026-11-15 correction below.
- Every slide it cited is a real deck, slide number and title.
- The full exam covered all six parts, with two drawn picture questions (a rig with no jaw, finger or cape bones, and an ease-in curve) and true counts mixed: four questions with 1 true, six with 2, six with 3, four with 4.

Two weak spots, now fixed in both instruction files: one question tested GDD section position numbers ("Risks is fifteenth"), and one scenario gave away its own statement ("third-person game"). The keys were checked by the same kind of model that wrote them, not by a game developer. It has not been run inside a real Claude Project or GPT.

## PBR scope correction (2026-11-15)
Bear confirmed that students should know what PBR is and why it matters, but have not used a PBR-based No-Bake system. Topic 14 now includes the general definition and importance of PBR. Detailed PBR parameters, maps and implementation workflows, and the No-Bake system, remain outside the exam. Both coach prompts and the full/student cheat sheets carry this boundary. The topic count stays 24.

Retest both coaches: "quiz me on PBR" must offer a general concept question without revealing the answer; a request for detailed PBR or the No-Bake system must be redirected as outside this exam. This revision has been checked for source consistency, not tested in a live Claude Project or GPT.

## Caveats
- **Unconfirmed readings.** The cheat sheet carries six remaining readings that Bear hasn't confirmed (the PBR item is now confirmed) (the "For Bear" box in `../EXAM-CHEAT-SHEET-FULL.md`). Two of them are camera topics with no slide yet (shot sizes, first vs third person), so the coach can only cite the nearest slide for those.
- **Picture questions are drawn by the AI.** Claude draws them as SVG; the GPT draws them with Code Interpreter. Either can draw something that doesn't match its own statements. The instructions tell it to check, but students should report a picture that looks wrong. Neither version can draw the Godot or Blender editor, so interface questions are in words.
- **Rebuild the knowledge file when the sheet changes.** `knowledge/EXAM-CHEAT-SHEET.md` is generated from `../EXAM-CHEAT-SHEET-FULL.md`: drop the "For Bear" section, and turn each slide link into "Deck NN Name, slide N, "Title"" using the title from the deck. If the full sheet changes, regenerate this file and upload it again to both tools.
- **Source publication approved by Bear (2026-11-16).** The course repo is public. These practice-coach files contain no live exam questions. The draft-scope and live-testing caveats above still apply.
