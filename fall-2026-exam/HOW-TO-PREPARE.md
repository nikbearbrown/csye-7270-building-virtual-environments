# How to prepare for the Fall 2026 exam

> **Draft, not signed off.** This guide summarises published studies on how people learn and prepare for tests. The sources are listed at the end, but the figures have not yet been checked against the original papers, and no study covers an exam exactly like this one. The plans are suggestions built on that research, not a proven schedule. Every technical term on the exam comes from the book text (the course chapters and lessons). Where your notes or any glossary differ from the example terms below, **the book text wins**: on a vocabulary exam, the course's definition is the answer, and a term the book does not use is not on the exam.

## Executive summary

The exam is **entirely multiple-answer**: 20 questions, 5 points each, 100 points. Each question has five statements; you decide whether each one is true or false on its own. It tests whether you know **what the course's ideas mean and how each differs from its nearest neighbour** (what a shader is, a material, a collider, a trigger, a sprite sheet, a rig, a state machine, a frame budget, MCP, a claim versus evidence). It does not ask you to read or write code. So preparing means: **practise in that exact format, with the answers hidden, and fix what you miss.**

The exam: fully on paper (no laptop, no phone; pen or pencil on the printed exam). 100 points: 20 multiple-answer questions, five statements each (A to E), each statement true or false on its own, 1 point per statement. A question has anywhere from one to four true statements. You score a point for a true statement you checked and for a false statement you left blank. The 20 questions cover the course's Chapters 0 to 14: Chapters 0, 3, 4, 7 and 14 have two questions each and every other chapter has one. See [README.md](README.md) for the topic list.

## Which practice file to open

Each practice exam has two files:

- **The exam** (`practice-exam-01.md`, `practice-exam-02.md`): the one to **practise from**. Questions only. Answer it cold, on paper, with no answers in sight.
- **The key, with the questions shown** (`practice-exam-01-KEY.md`, `practice-exam-02-KEY.md`): every question in full, with the true statements marked, a one-line reason under every statement, and the chapter passage the question follows. Open it after you finish, or use it to study.

The plans below say "study keyed answers" in the early days and "attempt cold" later. Use the key file for the first, and the exam file for the second.

## 1. What the evidence says

| Technique | What the research found | Strength | What it means for this exam |
|---|---|---|---|
| Practice testing (self-quizzing) | One of only two techniques rated "high utility" in a major review of ten study techniques. Works best with corrective feedback. Rereading, highlighting and summarizing were rated low. [1] | Strong | Do practice exams and cards. Stop rereading notes. Check against the key right after each attempt. |
| Spaced practice | The other "high utility" technique [1]. For a test one week away, the best gap between study sessions was about 20-40% of that week; a gap that is too short hurts more than one that is too long. [2] | Strong (mostly facts) | Revisit each topic every 3-5 days across 14 days (the guide's extrapolation from [2]). Cramming throws this away. |
| Transfer from practice tests | Practice testing transfers to new questions (average d about 0.40), mainly when practice and exam answers overlap, practice involves elaboration, and you got most practice items right. Transfer is weakest when cue and answer are swapped (practise term -> definition, get tested definition -> term). [3] | Moderate | Practise in the exam's own format. Drill terms in both directions. Get accurate first, then fast. |
| Interleaving (mixing problem types) | Moderate average benefit (g = 0.42), larger when the categories look alike. For word-based materials, blocking actually won (g = -0.39). [4] | Moderate, conditional | Mix questions from different chapters, and inside a cluster mix look-alike terms (collider and trigger, sprite sheet and rig). Do not expect shuffling a bare word list to help: interleave by applying terms to scenarios. |
| Comparing cases side by side | Comparison activities beat other case formats (d about 0.50). Stating the principle after the comparison helped. [5] | Moderate | Study look-alike terms as pairs, then write the rule that separates them. Caveat: the strongest condition in that review was finding similarities, so evidence for contrasting confusable terms is indirect. |
| Worked examples | Help beginners; the advantage fades or reverses as skill grows (expertise reversal). Removing worked steps gradually works better than fixed examples. [6] | Strong for early learning | Read the key's reasons in the first days only. Then attempt cold and use the key to check. |
| Learning from errors | Errors made with high confidence are corrected more readily after feedback (hypercorrection). Feedback must show the correct answer. Some confident errors come back after a delay. [7] | Moderate-strong (mostly lab, general-knowledge questions) | Rate your confidence on every practice statement. Re-test confident errors 2-3 days later. |
| Pretesting | Attempting questions before studying can help as much as testing after. [8] | Promising, not settled | Try a practice exam cold before reading the key or the chapter. |
| Multiple true-false format | This format exposes "mixed" understanding: students who accept the correct statement and also a wrong one. Single-answer multiple choice hides this. [9] | Moderate (assessment research) | This is the whole exam. Judge each statement on its own. There is no fixed number of true statements. |
| Short checklists of look-alikes | Mixed. One controlled study found a generic checklist no better than unguided reading, while reading aimed at specific defect classes found 35% more. Other small studies favour checklists or find no difference. [10] | Weak / mixed | Keep a short list of look-alike pairs phrased as questions ("does it block, or only report?"). Not a long generic list. |
| Practising with partners | Career-centre guidance on case interviews: practise with partners to find weaknesses, then drill those weaknesses. [11] | Practitioner advice, not research | Swap your error logs with a classmate and explain to each other why each wrong statement is wrong. |
| Timed handwritten exams | Teaching-centre guidance: budget time by points, read all questions first, move on when time is up. [12] | Practitioner advice | Every statement is worth the same. Decide the ones you are sure of first and come back to the rest. An unchecked box counts as "false", so decide every statement before time is up. |
| Sleep | In one course (88 students, wearable trackers), sleep over the prior week and month correlated with grades; sleep on the single night before a test did not. [13] | Correlational, one course | Protect sleep across all 14 days. Do not trade sleep for study. |
| Writing about worries before the exam | A 2011 study found benefits for anxious students. A later large replication reported no effect (confirmed only through a secondary source). [14] | Mixed | Optional. Do not rely on it. |

Where the evidence is weak. Most of this research uses facts, word lists, maths problems or general-knowledge questions. No studies were found of exams like this one (decide five statements about each of twenty ideas from one course). The checklist evidence is mixed and comes from small studies. Timed-exam and partner-practice advice is practitioner guidance, not experiments. The plan is well founded on how to practise and less certain on exam-specific tactics.

## 2. Study plans

Set your time budget first.
- Minutes per question = (exam minutes - 10) / 20
- Example: a 60-minute exam gives 2.5 minutes per question, with 10 minutes spare.
- Check the real length of the exam with the instructor and use that. Use your numbers in every timed drill.

Keep two logs from Day 1.
- Error log: question, statement, your answer, your confidence (sure / unsure / guess), correct answer, the word or fact that decided it, one-line rule.
- Pair list: every pair of terms you confused, plus pairs that sit near each other in the chapters.

Five clusters to review, used in the plans below:
1. Toolchain, working with an agent, and checking its claims (Chapter 0).
2. Walker and Godot projects, game art and sound, and 3D assets with Blender (Chapters 1 to 3).
3. Nodes, scenes and collision; design documents; shader foundations (Chapters 4 to 6).
4. Materials and textures, checking a shader, and particles (Chapters 7 to 9).
5. Animation, state machines, audio, performance and game AI (Chapters 10 to 14).

### 14-day plan (Day 14 = day before the exam)
| Day | What to do | Time | Why |
|---|---|---|---|
| 1 | Practice exam 01, cold, by hand, timed. Mark it with the key. Start both logs. | 1.5-2 h | Pretest; shows your gaps; sets a baseline. |
| 2 | Build term cards from the chapters' own wording and the pair list. Read the key's reasons for every statement you missed and say why the tempting wrong one fails. Cluster 1: re-read, then say each idea in one sentence without notes. | 75 min | Worked examples while the format is new. |
| 3 | Cards in both directions (25 min). Cluster 2 and 3: for each chapter, write what each term means and how it differs from its nearest neighbour; check the chapter. | 75 min | Moving from examples to solo work. |
| 4 | Cover the key of practice exam 01 and re-answer only its questions on clusters 1 to 3, with your Day 1 answers hidden. Mark and log. | 75 min | Retrieval in exam format. |
| 5 | Re-attempt every confident error from Days 1-4. Rewrite each rule until it would stop you from making the same mistake. | 60 min | Hypercorrection. |
| 6 | Clusters 4 and 5, then re-answer practice exam 01's questions on clusters 4 and 5, shuffled, with the key covered. | 75 min | Interleaving where categories are easy to confuse. |
| 7 | Rest, or 20 minutes of cards. | 0-20 min | Spacing gap. |
| 8 | Practice exam 02, full, timed, by hand. Mark it. | 1.5-2 h | Spaced retrieval; measures progress. |
| 9 | Work the error log: for each miss, write why the wrong answer tempted you and the rule that would have stopped you. Re-test Day 1 confident errors. | 60 min | Delayed re-test; confident errors can return. |
| 10 | Write three questions of your own, each on a different chapter: five statements, with some true and some plausible but false. Swap with a classmate if you can and mark each other; explain every statement aloud. | 75 min | Thinking like the exam author; partner feedback. (The guide's suggestion; not directly tested.) |
| 11 | Swap the questions you wrote on Day 10 with a classmate and answer theirs, timed with your per-question minutes. Then review every miss. | 75 min | Speed once accuracy is solid. |
| 12 | Full rehearsal: practice exam 01 again (it is 11 days since you first saw it), under exact timing. | 1.5-2 h | Full rehearsal. |
| 13 | Cards only for terms missed twice. Re-read the two chapters where you lost most statements. | 45 min | Targeted and light. |
| 14 | Ten cards and one chapter's pair list. Pack pens and pencils. Sleep. Nothing new. | 30 min | Protect sleep; avoid late confusion. |
Avoid reusing a practice exam within 4 days, or you will be recognizing answers rather than retrieving them.

### 3-day crash version
You lose most of the spacing benefit. Make up for it by testing, never by rereading.
| Day | What to do | Time | Why |
|---|---|---|---|
| 1 | Practice exam 01, timed, by hand. Mark it. Build a pair list from misses only; make cards in both directions. Read the key's reasons for the chapters you missed most. | 3 h | Diagnose, then worked examples on your gaps only. |
| 2 | Cards (30 min). Re-answer practice exam 01's questions on your two weakest clusters, key covered, marked. In the evening, re-attempt Day 1 confident errors. | 3 h | Retrieval with feedback; a same-day gap. |
| 3 | Practice exam 02, timed. Review only confident errors and your weakest chapters. Stop by early evening and sleep. | 2.5 h | Final rehearsal; protect sleep. |
| Exam morning | Ten cards. | 15 min | Warm-up only. |

## 3. Learn each idea: say it, contrast it, test it

The exam asks whether you know what an idea means and how it differs from the idea next to it. For each term in each chapter, write four lines on a card:

1. **What it is**, in one sentence, in the chapter's wording.
2. **Its nearest neighbour** and the one question that tells them apart.
3. **One example and one non-example.**
4. **What you would say to an agent or teammate** that uses the exact word (for example "an area that reports overlap and does not block", not "a coin collider").

Drills, always by hand and timed:
- **Term sprint:** 10 terms, 60 seconds each: say what it is and how it differs from its neighbour.
- **Scenario to term:** read a description and name the exact term for it (the reverse of a definition card).
- **Wrong-word spotting:** read a sentence a person might send to an AI tool and say which word is wrong and what they meant.
- **Say it to the agent:** rewrite a vague request ("make it faster") using the exact terms.

## 4. Multiple-answer routine

### Learn look-alike terms in pairs
For each pair, make one card with: each term's one-line definition, in the chapter's wording; the deciding question: the one thing that tells them apart; one example of each.

Example pairs. Every term below is used and explained in the book text; where the chapter's wording differs, the chapter wins. Each pair names the chapter to reread. This is a study aid, not a list of what will be asked.
| Pair | Deciding question | Chapter |
|---|---|---|
| Claim / evidence | Is it the agent's report, or a result you checked yourself? | 0 |
| Instruction file / permission | Is it standing knowledge the agent starts each session with, or a rule about which commands it may run? | 0 |
| Headless run / looking at the screen | Does it check game state and numbers, or what a person sees and hears? | 0, 8 |
| Per-frame update / fixed-rate physics update | Does it run once per drawn frame, or at a fixed rate? | 1, 4 |
| Nearest / smooth texture filter | Does a pixel stay a hard block, or do neighbouring pixels blend? | 2 |
| Collision shape / the picture | Is it the shape the physics engine uses, or what the player sees? Nothing ties them together. | 3, 4 |
| Script / MCP connection | Is it a saved file you can rerun, or a live conversation with an open program? | 3 |
| Node / scene / instance | Is it one job, a saved tree of nodes, or one use of a saved scene? | 4 |
| Signal / group | Is it a message that something happened, or a tag used to call many nodes? | 4 |
| Collider / trigger | Does it block, or only report an overlap? | 4 |
| Collision layer / collision mask | Is it what this object is, or what this object looks for? | 4 |
| Design document / brief | Is it the detailed record builders and testers work from, or the short statement of the idea? | 5 |
| Texture / material / shader | Is it image data, a bundle of settings and textures, or the program that draws? | 6, 7 |
| Vertex part / pixel part of a shader | Does it run once per corner (position), or once per covered pixel (colour)? | 6 |
| Colour texture / data texture | Is it display colour, or a number used as stored? | 7 |
| Albedo / normal map | Is it the base colour of the surface, or a per-pixel direction used for lighting? | 7 |
| Compile check / looking at the drawn result | Does it show that the code is valid, or that the picture is right? | 8 |
| Burst / continuous effect | Are the particles born all at once, or at a steady pace? | 9 |
| Sprite sheet / rig | Does the animation change which image is shown, or move bones that the parts follow? | 10 |
| Keyframe / interpolation | Is it a value stored at a time, or the rule that fills in between? | 10 |
| State machine / blend space | Is exactly one state active with transitions between them, or are clips mixed by a continuous value? | 11 |
| Bus / positional sound | Is it a channel for a group of sounds, or a sound with a place in the world? | 12 |
| Frame time / FPS / frame budget | Is it milliseconds per frame, frames per second, or the longest allowed frame time? | 13 |
| CPU-bound / GPU-bound | Does game logic and draw preparation set the frame length, or drawing work? | 13 |
| State machine / behavior tree | Is one state active with transitions, or are children tried in priority order from a root? | 14 |
| Seed / noise | Does it make a level repeatable, or give smoothly varying values? | 14 |

Make cards in both directions: definition -> term, and term -> "which description fits?" Practice in one direction transfers poorly to the other [3]. Shuffle within a cluster of similar terms, not across unrelated ones [4].

### Judge each statement alone
1. Cover the other four statements.
2. Find the word that carries the meaning: usually the technical term or a qualifier ("always", "only", "guarantees", "never").
3. Ask: is this term the correct name for exactly what is described? Common traps are:
   - **swapped definitions:** the right two terms with their meanings exchanged;
   - **the right term with the wrong condition:** true in one setting, stated as true everywhere;
   - **a near-synonym swapped in:** "fragment" for "pixel", "normals" for "normal map";
   - **a qualifier that makes the statement too strong.** A strong word often makes a statement false, but not always: check the meaning, not the word.
4. Mark it and move on. Do not count how many you have marked true; there is no quota (one to four are true).
5. For "spot the wrong word in this prompt", first write in the margin what the person meant, then check whether the word matches.
6. Decide every statement. An unchecked box counts as "false".

### Review wrong answers
For every missed statement, log the deciding word and a one-line rule (for example, "a trigger reports overlap; it does not block"). Star the confident errors and re-test them 2-3 days later [7]. Always review with the correct answer in front of you; practice with corrective feedback works best [1].

## 5. Common mistakes and fixes
| Mistake | Fix |
|---|---|
| Rereading notes and highlighting as the main study method. | Replace with practice tests and cards [1]. |
| Knowing the word but not what separates it from its neighbour. | Write the deciding question for every pair. |
| Marking the answer you recognise rather than the one you can explain. | Say why the nearest wrong statement is false. |
| Judging statements against each other, or assuming one true statement per question. | Judge each alone; no quota [9]. |
| Treating "always", "only" and "never" as automatically false. | Check the meaning; some strong-sounding statements are true. |
| Answering from another engine or from general games experience instead of from what the course teaches. | The exam is about Godot and follows the course text; where your experience differs, the course text wins. |
| Practising only on screen. | Every timed drill on paper. |
| Spending the whole sitting on early questions and leaving boxes undecided. | Fixed minutes per question; an undecided box counts as "false" [12]. |
| Repeating one practice exam until you remember the answers. | Leave at least 4 days; use a fresh mixed set. |
| Trading sleep for late study. | Keep sleep steady across the two weeks [13]. |

## 6. Sources
Numbers match the citations above. Where the guide relied on a summary rather than the paper itself, it says so.
1. Dunlosky, Rawson, Marsh, Nathan & Willingham (2013). Improving students' learning with effective learning techniques. Psychological Science in the Public Interest, 14(1). DOI 10.1177/1529100612453266. Read via the APS press release and a summary table (texasldcenter.org/?p=346).
2. Cepeda, Vul, Rohrer, Wixted & Pashler (2008). Spacing effects in learning: a temporal ridgeline of optimal retention. Psychological Science, 19(11). https://pubmed.ncbi.nlm.nih.gov/19076480/ . The "too short is worse than too long" point comes from York University's press release.
3. Pan & Rickard (2018). Transfer of test-enhanced learning: meta-analytic review and synthesis. Psychological Bulletin, 144(7). https://sc-pan.github.io/pdf/PR_2018.pdf
4. Brunmair & Richter (2019). Similarity matters: a meta-analysis of interleaved learning and its moderators. Psychological Bulletin, 145(11). https://pubmed.ncbi.nlm.nih.gov/31556629/
5. Alfieri, Nokes-Malach & Schunn (2013). Learning through case comparisons: a meta-analytic review. Educational Psychologist, 48(2).
6. Kalyuga, "Expertise reversal effect and its instructional implications" (Chartered College of Teaching). Salden, Aleven, Schwonke & Renkl (2010), The expertise reversal effect and worked examples in tutored problem solving, Instructional Science.
7. Butterfield & Metcalfe (2006). The correction of errors committed with high confidence. Metacognition and Learning. Review of learning from errors, Psychonomic Bulletin & Review (2021). Griffiths & Higham, "Beyond hypercorrection".
8. Pan & Sana (2021). Pretesting versus posttesting. Journal of Experimental Psychology: Applied. (The guide saw the pretesting result in a database summary, not in the full paper; provisional.)
9. Multiple-true-false vs multiple-choice questions (2019), International Journal of STEM Education. https://dx.doi.org/10.1186/s40594-019-0169-0
10. University of Maryland Experimental Software Engineering Group, reading techniques for fault detection. Akinola & Osofisan (2009), arXiv 0909.4260. Oladele & Adedayo, LAUJET. (About finding defects in code and documents; the transfer to this exam is indirect.)
11. Boston University Questrom, consulting case resources. Penn Career Services, case interview guide. (Practitioner guidance on practising with partners.)
12. University of Texas at Austin learning center, "Written Tests". Kansas State Counseling Services, "Suggestions for Taking Essay Tests". (Practitioner guidance on time budgeting.)
13. Okano, Kaczmarzyk, Dave, Gabrieli & Grossman (2019). Sleep quality, duration, and consistency are associated with better academic performance in college students. npj Science of Learning.
14. Ramirez & Beilock (2011), Science. The failed replication (Camerer et al., 2018) was seen only in lecture slides. Check the original before relying on it.
