# Exam preparation guide: CSYE 7270: Building Virtual Environments

**Student-facing draft for instructor review.** Learn what the course's ideas mean, and how each differs from its neighbour, well enough to direct a coding agent working on a Godot game and to notice when a statement about the work is wrong. Use this guide for preparation, not as a prediction of examination questions. It adapts the supplied study guide's structure to the all-multiple-answer exam, with course-specific review and vocabulary.

## Start here: format and scoring

The current public format is **100 points: twenty multiple-answer questions × 5 points**. Each question has **five statements, A to E**; one to four of them are true. Each statement is true or false on its own and is worth **1 point**: you score a point for a true statement you checked and for a false statement you left blank. There are no case questions, no code to read and no shader code to write or change. Read each statement by itself: a strong word such as "always" often makes a statement false, but not every strong-sounding statement is false. See the [public exam overview](README.md) for the topic list and the exact marking rule.

Every practice exam covers the course's Chapters 0 to 14: Chapters 0, 3, 4, 7 and 14 have two questions each and every other chapter has one. Practise recognising what an idea means and how it differs from the one next to it, not memorizing editor menu locations.

## 1. What the evidence says

This guide's structure comes from the supplied study guide. The broad study principles below are useful, but the exact schedule is advice, not an experimentally validated recipe for this examination. Numerical effect sizes and precise optimal spacing claims from the source draft are not repeated because they have not been rechecked here against the original papers.

| Technique | Evidence and limitation | Application |
|---|---|---|
| Retrieval practice | Broad support for attempting to recall and then receiving corrective feedback [1,3]. It is not proof that every practice design transfers. | Answer before opening the key; explain the reason after checking. |
| Spacing | Distributed practice is well supported; useful gaps depend on the material and retention interval [1,2]. | Revisit difficult concepts on several days rather than one long session. |
| Interleaving | Benefits depend on the material and similarity of categories [4]. | Mix confusable terms after learning their basic distinctions. |
| Comparing cases | Comparing examples can support abstraction [5]. | State the deciding rule between two similar concepts, not just two definitions. |
| Worked examples | Helpful scaffolding, especially early; support should fade with understanding [6]. | Read the reasons in one public key, then attempt a practice exam independently. |
| Correcting confident errors | Feedback can correct high-confidence mistakes; correction may not persist without later retrieval [7]. | Record confidence and retest important errors after a delay. |
| Pretesting | A first attempt can direct later study [8]. | Try an unfamiliar public question before reading its explanation; low first scores are diagnostic. |
| Multiple true-false practice | Evaluates individual propositions and can reveal partial misconceptions [9]. | This is the whole exam. Judge each statement by its meaning, not by the pattern of other answers. |
| Short checklists | Results depend on the task and checklist; a checklist is not proof of correctness [10]. | Keep a short list of look-alike pairs as questions, then justify your conclusion. |
| Partner practice and timed writing | Practical advice rather than a validated treatment for this exam [11,12]. | Exchange error logs and explain each wrong statement to each other; rehearse the announced medium. |
| Sleep | Sleep habits correlate with performance; the cited study does not establish a causal guarantee [13]. | Protect a sustainable sleep schedule across preparation. |
| Writing about worries | Evidence is mixed, and the supplied draft relied on secondary reporting [14]. | Optional; do not substitute it for practice or support you already find useful. |

Targeted rereading is useful when it repairs a gap. The recommendation is not "never reread," but "do not mistake familiarity for being able to answer." Begin untimed if the idea is new; add timing once you can explain it.

## 2. Study plans

### Set the budget and record what you learn

The public exam overview suggests about 3 minutes per question: about 60 minutes of work for 20 questions. Confirm the actual examination duration with the instructor.

Allocate time from the actual examination instructions, not from a universal formula. Keep some checking time. One hard question should not prevent attempts at the rest. An unchecked box counts as "false", so decide every statement before time is up. Practise on paper if that is the announced format; confirm permitted materials with the instructor.

Keep an **error log** with: question and statement; your answer; confidence; corrected reasoning; the decisive word or qualifier; a short rule; next retest date. Keep a **pair list** of terms you confuse. Do not write only the answer letter: record why it is correct.

### Fourteen-day plan

These are adjustable study sessions, not required workloads. Include breaks and adapt around other commitments.

| Day | Work | Suggested duration |
|---|---|---|
| 1 | Attempt public practice 01 cold; then check it and start both logs. | Exam-length sitting plus review |
| 2 | Review cluster 1 below; make two-direction term cards; read the key's reasons for what you missed. | 60–75 min |
| 3 | Review clusters 2 and 3; for each term, write what it is and how it differs from its nearest neighbour. | 60–75 min |
| 4 | Cover the key of practice 01 and re-answer only its questions on clusters 1 to 3. | 60–75 min |
| 5 | Retest confident errors; rewrite each rule until it would stop the mistake. | 45–60 min |
| 6 | Review clusters 4–5; then mix questions from different chapters. | 60–75 min |
| 7 | Rest or brief spaced retrieval from the pair list. | 0–20 min |
| 8 | Attempt public practice 02 cold, then check every statement. | Exam-length sitting plus review |
| 9 | Revisit the oldest errors. Explain why the tempting alternative is not supported. | 45–60 min |
| 10 | Write three five-statement questions from public lessons, each with some true and some plausible false statements. Exchange with a peer and explain every statement. | 60–75 min |
| 11 | Answer a classmate's Day 10 questions, timed. Review every miss. | 60–75 min |
| 12 | Full rehearsal using practice 01 again (it is 11 days since you first saw it) or a fresh mixed set; do not assume a third full practice paper exists. | Exam-length sitting plus review |
| 13 | Retest the most consequential remaining errors and explain one idea aloud. | 30–45 min |
| 14 | Light retrieval, check logistics, and protect sleep. | 20–30 min |

Course-specific clusters:
1. Toolchain, working with an agent, and checking its claims (Chapter 0).
2. Walker and Godot projects, game art and sound, and 3D assets with Blender (Chapters 1 to 3).
3. Nodes, scenes and collision; design documents; shader foundations (Chapters 4 to 6).
4. Materials and textures, checking a shader, and particles (Chapters 7 to 9).
5. Animation, state machines, audio, performance and game AI (Chapters 10 to 14).

When repeating a question, explain the reasoning before recalling the answer. A familiar score is not evidence that you can transfer the concept to a new scenario.

### Three-day version

| Day | Work |
|---|---|
| 1 | Diagnose with practice 01. Review the two weakest clusters and make cards only for important gaps. |
| 2 | Re-answer practice 01's questions on your weakest clusters with the key covered; inspect feedback; retest earlier mistakes after a break. |
| 3 | Rehearse with practice 02, review remaining gaps, and stop intensive work early enough to rest. |

Short preparation cannot reproduce two weeks of spacing. Focus on accurate reasoning and targeted reading rather than memorizing complete answers.

## 3. Learn each idea: say it, contrast it, test it

For each term you meet in a chapter, write on a card:

1. **What it is**, in one sentence, in the course's wording.
2. **Its nearest neighbour**, and the one question that tells them apart.
3. **An example and a non-example** of your own.
4. **How you would say it to an agent or teammate**: the exact word, not a vague one. "An area that reports overlap and does not block" says more than "a coin collider".

Short drills:

- **Definition drill:** pick a term, say what it is and how it differs from its neighbour in one minute.
- **Scenario drill:** read a description and name the exact term for it.
- **Wrong-word drill:** read a sentence a person might send to an AI tool, find the word that does not fit, and say what they meant.
- **Rewrite drill:** turn a vague request into one that uses the exact terms.

For practical study, predict a visible result, run a disposable project, compare it with your prediction, then explain what the test does and does not show. Do not change a real project merely to rehearse. Use the engine version specified in class.

If a public key appears technically wrong, record the disputed wording and your reasoning, then ask the instructor. Do not memorize a contradiction simply because it is in a key. This guide does not replace grading policy.

### Claim versus evidence

One of the cross-course topics is how a report about a piece of work differs from a result you have checked. For each kind of check, practise saying what it shows and what it does not: a clean compile shows the files load, not that the behaviour is right; an agent's "all tests pass" is a claim until you rerun the test yourself; a test that compares a value with the one it just set cannot fail. Ask of any statement: what would have to be true for this to be evidence, and what would the check miss?

## 4. Multiple-answer routine: use the terms precisely

For each pair, make a card with a definition, deciding question, original example and non-example. Practise both directions: term to explanation, and scenario to term. Start with these review distinctions, then extend them using the instructor's glossary.

| Terms | Deciding distinction |
|---|---|
| Claim / evidence | Is it the agent's report, or a result you checked yourself? |
| Instruction file / permission | Is it standing knowledge the agent starts each session with, or a rule about which commands it may run? |
| Collision shape / the picture | Is it the shape the physics engine uses, or what the player sees? Nothing ties them together. |
| Script / MCP connection | Is it a saved file you can rerun, or a live conversation with an open program? |
| Node / scene / instance | Is it one job, a saved tree of nodes, or one use of a saved scene? |
| Signal / group | Is it a message that something happened, or a tag used to call many nodes? |
| Collider / trigger | Does it block, or only report an overlap? |
| Collision layer / collision mask | Is it what this object is, or what this object looks for? |
| Texture / material / shader | Is it image data, a bundle of settings and textures, or the program that draws? |
| Vertex part / pixel part of a shader | Does it run once per corner (position), or once per covered pixel (colour)? |
| Colour texture / data texture | Is it display colour, or a number used as stored? |
| Sprite sheet / rig | Does the animation change which image is shown, or move bones that the parts follow? |
| Keyframe / interpolation | Is it a value stored at a time, or the rule that fills in between? |
| State machine / blend space | Is exactly one state active with transitions between them, or are clips mixed by a continuous value? |
| Bus / positional sound | Is it a channel for a group of sounds, or a sound with a place in the world? |
| Frame time / FPS / frame budget | Is it milliseconds per frame, frames per second, or the longest allowed frame time? |
| CPU-bound / GPU-bound | Does game logic and draw preparation set the frame length, or drawing work? |
| State machine / behavior tree | Is one state active with transitions, or are children tried in priority order from a root? |

These are study aids, not a complete syllabus or a claim that these particular terms will appear. Prefer the course's explicitly stated usage, but ask about a factual conflict or a term whose meaning varies across fields.

### Judge each statement independently

1. Identify the claim and its qualifiers.
2. Work out whether the stated conditions are enough. For a number, verify the denominator, units and assumptions.
3. Look for the usual traps: two terms with their meanings swapped, the right term with the wrong condition (true in one setting, stated as true in all), a near-synonym swapped in, and a qualifier that makes the statement too strong.
4. Use a counterexample when evaluating a universal claim. "Always" is not automatically false, and a cautious-sounding sentence is not automatically true.
5. Mark the statement according to its meaning and the printed marking instructions, not a guessed answer pattern. Do not count how many you have marked true; there is no quota.
6. During review, explain why the nearest wrong alternative fails. Retest high-confidence errors later.

The published rules score each of the five statements separately: correctly checked true and correctly left-blank false statements each earn one point. Follow the actual examination's instructions if revised.

## 5. Common mistakes and fixes

| Mistake | Better practice |
|---|---|
| Remembering the answer rather than the idea | Explain an unfamiliar example and a counterexample. |
| Knowing a word but not what separates it from its neighbour | Write the deciding question for every pair. |
| Marking the statement you recognise rather than the one you can explain | Say why the nearest wrong statement is false. |
| Assuming one true statement per question, or judging statements against each other | Judge each alone; one to four are true. |
| Treating "always", "only" or "never" as automatically false | Check the meaning; some strong-sounding statements are true. |
| Answering from another engine or from general games experience instead of from what the course teaches | The exam is about Godot and follows the course text; where your experience differs, the course text wins. |
| Treating completion as verification | Identify the observable result and the appropriate source of evidence. |
| Using an AI answer as proof of understanding | Attempt cold first, then critique help against public sources. |
| Spending the whole sitting on early questions | Use the announced timing; an undecided box counts as "false". |
| Treating a study schedule as an exam rule | Check the instructor's current announcements, accommodations and examination sheet. |

### Final self-check

Can you say what each idea in each chapter is, name its nearest neighbour, and say what separates them? Can you explain a mistaken true/false choice without looking at its key? If not, return to the relevant lesson and practise that idea rather than rereading everything.

## 6. Sources and course resources

### Use the public course materials

- [Exam overview](README.md).
- [Practice exam 01](practice-exam-01.md) and [practice exam 02](practice-exam-02.md). Open each matching key only after attempting the student file.
- [Chapter map](../chapters/README.md) and [modules](../modules/README.md).
- This document is an **exam preparation guide**, not a specification of the exam. The older question bank, cheat sheet and glossary in the `interview-bank` repository were written for an earlier version of the exam; they cover other engines and code that this exam does not.

This guide uses the public overview as of 9 November 2026. It does not reproduce private examination questions, solutions, topic allocations or answer patterns. The instructor's current examination sheet controls scope, duration and permitted materials.

### Research behind the preparation structure

These references come from the supplied study-guide draft. They support general study principles, not a guarantee of a score or the exact schedule above. The original papers and all links have not been independently revalidated in this adaptation; secondary-source limitations are retained. Quantitative claims from the draft have deliberately been omitted.

1. Dunlosky et al. (2013), *Improving Students' Learning With Effective Learning Techniques*. DOI: [10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266). Broad review of study strategies.
2. Cepeda et al. (2008), *Spacing effects in learning*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/19076480/).
3. Pan & Rickard (2018), *Transfer of test-enhanced learning*. [Author PDF](https://sc-pan.github.io/pdf/PR_2018.pdf).
4. Brunmair & Richter (2019), *Similarity matters: a meta-analysis of interleaved learning*. [PubMed](https://pubmed.ncbi.nlm.nih.gov/31556629/).
5. Alfieri, Nokes-Malach & Schunn (2013), *Learning through case comparisons*. [Author PDF](https://www.lrdc.pitt.edu/Schunn/papers/ContrastingCasesMeta-AlfieriEtAl2013.pdf).
6. Salden et al. (2010), *The expertise reversal effect and worked examples in tutored problem solving*. [Research record](https://researchportal.hw.ac.uk/en/publications/the-expertise-reversal-effect-and-worked-examples-in-tutored-prob/).
7. Butterfield & Metcalfe (2006), *The correction of errors committed with high confidence*. [Article copy](https://core.ac.uk/download/357328401.pdf). Revisit corrections; immediate feedback is not permanent mastery.
8. Pan & Sana (2021), *Pretesting versus posttesting*. [Author PDF](https://sc-pan.github.io/pdf/PS_2021.pdf). The supplied draft relied on a summary rather than full-paper inspection.
9. Research comparing multiple-true-false and multiple-choice formats (2019), *International Journal of STEM Education*. [DOI](https://doi.org/10.1186/s40594-019-0169-0).
10. University of Maryland Experimental Software Engineering Group, [reading techniques for fault detection](https://www.cs.umd.edu/projects/SoftEng/ESEG/topics/rtfault2.html). About finding defects in code and documents; transfer to this exam is indirect.
11. Penn Career Services, [case interview guide](https://careerservices.upenn.edu/resources/case-interview-guide/). Practitioner guidance on practising with partners, not experimental evidence for this exam.
12. Kansas State Counseling Services, [suggestions for taking essay tests](https://www.k-state.edu/counseling/resources/self_help/suggestionsfortakingessaytests.html). Practitioner guidance on time budgeting.
13. Okano et al. (2019), *Sleep quality, duration, and consistency are associated with better academic performance in college students*. [MIT record](https://dspace.mit.edu/handle/1721.1/127257). Observational evidence.
14. Ramirez & Beilock (2011), expressive writing before tests, via [a research news summary](https://www.sciencedaily.com/releases/2011/01/110113141605.htm). The supplied draft also reports a replication concern through secondary material; no recommendation here depends on this finding.
