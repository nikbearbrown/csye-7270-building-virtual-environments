# Research brief: "Making games through conducting AI" (CSYE 7270 lecture film 1)

Read-only research. Sources read: info-7375-conducting-ai (README, COURSE, SYLLABUS, AGENTS, ch.00 intro, ch.1-15, ch.97 fundamental themes, ch.98 Appendix A), info-7375-irreducibly-human (README, SYLLABUS, ch.00, ch.1-8, ch.97, lesson 15), info-7375-computational-skepticism-for-ai (README, SYLLABUS, reading-map, ch.1, _expanded-four-moves, ch.8 opening, lessons 8-9), skepticism-ai (README, ABOUT, ls).

Path prefix used below (written out in full each time, as asked):
/Users/bear/Documents/CoWork/bear-textbooks/books/

Labels: [BOOK] = the book says it. INFERRED = my reading, the books do not say it. [BOOK-HEDGE] = the book itself flags the claim as contested/low-evidence.

---------------------------------------------------------------------------
## 0. Three things to know before using any of this

1. **None of the three books mentions game design, playtesting, fun, game feel, Godot, or Unity.** A grep for "game", "gameplay", "playtest", "godot", "unity" across the Conducting AI and Irreducibly Human chapters finds only: "Game of 24" (a test problem, ch.2:35), a football "game" (ch.12:3-7), a ballpark "game" (IH ch.7:7), and "skin in the game". Every game-making claim in the film is therefore INFERRED from a general principle. The closest the books come: the Brutalist section (creative production, motion/video design, not games) and Appendix A (software built with an agent at the command line, which is exactly the Claude Code situation).
2. **Several of the "irreducibly human" claims are the books' own arguments, not established findings, and the course layer says so.** /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-conducting-ai/AGENTS.md:7 "Treat philosophical impossibility claims as arguments rather than established empirical limits." Ch.2:59 calls the structural claim "a wager, not a theorem [Contested]". The film should say "the work the human must do" and avoid "AI can never do X".
3. **The ideas are repeated across the books.** Ch.97 "Fundamental Themes" is the same file in Conducting AI, Irreducibly Human and Computational Skepticism (495 lines each). The five capacities are named identically in Conducting AI (ch.4-13) and Computational Skepticism ch.1:152-180. Cite one source, not three.

---------------------------------------------------------------------------
## 1. The core claims of each book, in plain words

### 1A. Conducting AI  (/Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-conducting-ai/)

Course shell: README.md, COURSE.md (15 lessons, one per chapter), SYLLABUS.md. The five-stage rhythm is "Predict → Build It → Use It → Ship It → Verify" (COURSE.md:3). The book is "the narrative reading edition" (README.md:7). Assignment 8-10 build the Supervisory Analysis (SYLLABUS.md:35).

**Ch.1 The Conductorless Orchestra** (/Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-conducting-ai/chapters/01-the-conductorless-orchestra.md)
- Five professionals each use an AI tool as intended and each ships a confident, wrong output (lines 7-15). What was missing in all five: "no human operation engaged to determine whether the confident output was grounded in the specific reality at hand" (line 33).
- The missing thing is the **conductor**: plays no instrument, and does four things: holds the whole performance in mind, hears the wrong note before the score confirms it, chooses which piece is worth performing, decides how it is interpreted (lines 39-51). Those four plus the prior judgment become the five capacities (line 53).
- Cruel inversion (line 81): the property that made the output dangerous is the property that made it convincing (fluency). Figure 1.2 (line 83).
- Accountability (line 87): the human signs, the model faces no sanction, so verification cannot be handed back to the tool.
- "Gardnerian Gap" (lines 55-65): a catalogue of abilities names no director of them. The book itself marks Gardner's theory [Contested] (line 59): do not put Gardner on screen as support.

**Ch.2 The Solve-Verify Asymmetry** (.../chapters/02-the-solve-verify-asymmetry.md), exactly what it claims:
- The claim (blockquote, line 7): solving and verifying are different cognitive operations; AI automates the first; the second stays human "not because today's models are weak, but because verification requires something statistical pattern-matching does not contain"; because faster solving makes more output to verify, "the gap deepens as capability scales rather than closing."
- Misconception it attacks (line 11): "verifying is just solving again, more carefully".
- Evidence ladder: (a) P vs NP as an analogy only, explicitly bounded twice (open conjecture; LLMs are not worst-case exact algorithms) (lines 17-23); (b) the real argument: a model verifies by sampling from the same distribution that produced the error (lines 31-35), backed by Stechly/Valmeekam/Kambhampati self-critique results [Medium]; (c) what verification needs is grounding in specific domain reality, which lives outside the distribution (line 37).
- Two channels picture (line 45): SOLVE channel widens, VERIFY gate stays human-sized. Figure 2.1 (line 47).
- Removes both a comfort ("next model will check itself") and a threat ("you'll be a rubber stamp") (lines 51-57). Verification is where accountability attaches.
- Honest counter-case (lines 61-71): reasoning models and tool use do verify more. The book's answer: grounding comes from the tool the model was pointed at, selected by a human; "The conductor's job moves up a level" (line 69).
- Worked example (lines 73-77): the lawyer's re-prompt asked the solver to solve the checking question and got more likely-looking text.

**Ch.3 Three Levels of AI Usage** (.../chapters/03-three-levels-of-ai-usage.md)
- Taxonomy is "my own teaching framework" (line 19), a re-cut of Sheridan-Verplank 1978 / Parasuraman-Sheridan-Wickens 2000.
- Level I copy editor: bounded task, output inspectable at a glance (line 21). Level II research assistant: correctness lives outside the interaction, you must go consult sources (line 23). Level III supercollaborator: output shapes the problem itself, so you must supervise the framing (line 25). Table at lines 31-35.
- The danger is a **gap** between level of work and level of supervision, not any level (line 29). Not a ladder of virtue.
- Parasuraman & Manzey 2010: automation complacency and automation bias; found in experts as much as novices; not overcome by practice or warnings (lines 41-45). Shneiderman: automation and human control are separate axes (line 49).
- Priya's Tuesday (lines 5-13, map at 59-65).

**Ch.4-5 Capacity 1, Plausibility Auditing** (.../chapters/04-plausibility-auditing-part-1.md, 05-plausibility-auditing-part-2.md)
- Auditing is not verification. It runs BEFORE any source is consulted and decides (1) whether a source needs consulting at all and (2) what verification should look for (ch.4:17-22). Runs on your own domain model, not an external source. Table at ch.4:32-37.
- Foundation: "Statistical likelihood across a training corpus is not a grounded model of how a domain works" (ch.4:53). Chollet/ARC used as evidence the gap reconstitutes itself (ch.4:45-51).
- Two mechanisms (ch.4:57-63; the book says this split is "a pedagogical scaffold of this course", not an established taxonomy): domain-grounded pattern recognition ("this does not match the shape of any case I know") and anomaly detection against a mental model (a violated constraint).
- Audit-first protocol (ch.5:23-33): render verdict, name the target, name the mechanism, all before any lookup. Five outputs A-E (ch.5:11-19): renal-dose discharge summary, real case cited for wrong holding, R-squared 0.97 churn model (leakage tell), routing plan that sends a 53-foot trailer to a stop that cannot take it, a unit-consistent load calc that may still be ungrounded. Output E is the "indeterminate" verdict (ch.5:47).
- Calibrated trust (Lee & See 2004), misuse vs disuse (ch.5:63).

**Ch.6-7 Capacity 2, Problem Formulation** (.../chapters/06-problem-formulation-part-1.md, 07-problem-formulation-part-2.md)
- AI optimizes toward "the common and the likely"; the human reframes toward "the salient and the important", and must do it BEFORE engaging the tool (ch.6:13). The solve-verify asymmetry at the level of problems is a "formulate-versus-optimize asymmetry": AI optimizes a given formulation flawlessly, only a human can decide the formulation was wrong (ch.6:23).
- Problem and solution co-evolve (Dorst & Cross), so handing over the problem forfeits the standard you would judge the answer against: "an abdication, not a delegation" (ch.6:39). Schön: problems are constructed from problematic situations (ch.6:41). Darke's "primary generator": you cannot start without an anchor; surface it, do not purge it (ch.6:45-49). Semmelweis is the worked case (ch.6:3-13, 59-67).
- Ch.7: the **distinctness test** (ch.7:17): "Would these two formulations require different solutions even to test?" Three reworded support-ticket framings are one framing (ch.7:3-9); genuinely distinct framings disagree about what counts as success (ch.7:27). Also "Type III error": exactly right about the wrong problem (ch.7:53) and a values decision inside every formulation (ch.7:89).

**Ch.8-9 Capacity 3, Tool Orchestration** (.../chapters/08-tool-orchestration-part-1.md, 09-tool-orchestration-part-2.md)
- Five-layer capability stack (author's teaching device, not an industry standard, ch.8:9): generation, structured extraction, RAG, multi-step reasoning, agentic execution. As you climb, autonomy rises and verifiability falls; agentic layer has "error compounding" (ch.8:13-23, table 25-31).
- Rule: "Select the lowest-on-the-stack capability that the step actually requires" (ch.8:47). Value ETV "easier to verify", an extension of Thomas & Hunt's ETC (ch.8:51). Route exact work (arithmetic, lookups) out of the stochastic model entirely (ch.8:53).
- Ch.9: the unit of risk is the **handoff**, not the tool (ch.9:11-19). Document at each seam: what is passed, what it is trusted to be, how trust was earned. Cross-audit works "only to the degree that the two tools fail differently" (ch.9:25); sibling models give false agreement. Audit a generative claim with a non-generative tool (code, retrieval, schema) (ch.9:35-40).
- **Laundering** (author's coinage): an unverified output gains false authority as it passes through clean downstream steps; "Polish is not provenance" (ch.9:46-50). Consultant's $4.2 billion deck (ch.9:3-7). Pronovost ICU checklist as the evidence for explicit handoffs (ch.9 Wayback box, lines 66-72).

**Ch.10-11 Capacity 4, Interpretive Judgment** (.../chapters/10-interpretive-judgment-part-1.md, 11-interpretive-judgment-part-2.md)
- Suchman's three legitimacies, transposed by the author onto AI output (ch.10:15): pragmatic (serves audience self-interest; AI supplies this readily), moral (is it the right thing here; AI describes but cannot stand behind), cognitive (comprehensible, taken for granted; AI "counterfeits it", ch.10:19). Table ch.10:25-29.
- Worked example: one accurate cost-optimized recommendation is legitimate at the finance committee and morally illegitimate at the bedside (ch.10:55-65). "The notes are the model's, the meaning is supplied."
- Ch.11: Memo A (AI analysis, "thin") to Memo B (yours, "thick"; Ryle/Geertz eyelid example, ch.11:3). Memo B must separate: what the AI produced / what I add / why trust (cognitive) / why right here (moral) / signed recommendation (ch.11:19-27). "Memo B equals Memo A plus a signature" is theater (ch.11:13). Thin/thick audit (ch.11:37-41). Signing is the act no model performs (ch.11:49).

**Ch.12-13 Capacity 5, Executive Integration** (.../chapters/12-executive-integration-part-1.md, 13-executive-integration-part-2.md)
- Integration is the management of the relationship among the other four, not a fifth stage (ch.12:11-17). Sequencing ("do A, finish A, do B ...") vs integration ("when working on C makes A wrong, stop and re-open A") (ch.12:17).
- **Re-engagement trigger** = an event, not an attitude: "here, while doing X, I noticed something that made Y unsafe, and so I went back to Y" (ch.12:31-35).
- "Four right answers, one wrong performance" (ch.12:43-59): forecast, cost, public-comment, equity tools each correct; the assembled transit-site recommendation is wrong. Composite, flagged "not a documented incident". Lesson: "if each part is correct, the whole may still be wrong" (ch.12:59). Conway's Law reading of the seam.
- The head/hand/heart/spirit "Weave" is a mnemonic the book rates [Low] and calls weakest on "spirit" (ch.12:37-41): do not put it on screen as a finding.
- Ch.13: the Supervisory Analysis, 2,500-4,000 words, six recommended sections (the book itself marks section labels as "editorial recommendation", with `[author to confirm ...]` flags still in the text, ch.13:19 and 36) plus a required Re-engagement Log (ch.13:38-46).

**Ch.14-15** (.../chapters/14-the-dress-rehearsal.md, 15-the-plausibility-audit.md): peer critique, then Claude as adversarial auditor; the student judges each finding genuine vs false positive; the **Gap Account** names a failure the auditor could not detect. Distinguishes "contingent miss" (a better auditor fixes it) from "structural blind spot" (ch.15:45-49). Grounds: correlated failure ("the same AI writes the implementation and the tests", ch.15:51-55) and three archetypes: situated moral legitimacy, tacit domain anomaly, accountability asymmetry (ch.15:67-77). LLM-judge biases and attack rates (ch.15:25-31).

**Appendix A, The Pragmatic Conductor** (.../chapters/98-appendix-pragmatic-conductor.md) is the chapter that speaks most directly to Claude Code. Thomas & Hunt's advice sorted three ways (lines 21-27): (1) now mechanical, delegate it; (2) now more human, not less ("the Gru Part": choosing the problem, deciding what good enough means, estimating, finding real constraints); (3) now inverted (three items, A.10 lines 323-333). Every entry is tagged [PA][PF][TO][IJ][EI] with a **gate** (a testable condition before output moves on). Key entries: tracer bullet / vertical slice that runs (line 104); prototype is disposable (109); an agent reads your codebase as its style guide (44); single constraints file (CLAUDE.md) (A.1 "Communicate"); "Good enough" must be stated in the prompt (A.1); context drift, check `git diff --stat` (A.1 "boiled frogs"); programming by coincidence (A.7, line 224); tests-from-the-same-agent problem and a ranked list of test independence (A.7, lines 249-267); requirements pit and "find the box" (A.8, 273-300); cargo-cult repos and the saboteur branch (A.9, 300-322); worked 9-step Boondoggle Score for a discount rule (lines 335-359).

**Ch.97 Fundamental Themes** (.../chapters/97-fundamental-themes.md) is where the "division of labor" and "boondoggling" ideas live:
- One sentence (line 8); Frictional (16-30); phase gate = "the specific point at which AI processing stops and human work begins" (38); Humans + AI taxonomy (57-69).
- Division of Labor (lines 195-207): AI does Tier 1 tasks; humans do Tiers 4-7.
- Brutalist argument (312-388): "maximally informed, minimally autonomous, by design" (324); three governing files CLAUDE.md / DESIGN.md / PROJECT.md (328-340); "Refusal Behavior" (340); technical layer vs creative layer (346-356); what the artist keeps (360-372).
- Boondoggling (394-467): conducting Claude through a build; Boondoggle Score has a Minion Part (exact prompts for Claude) and a Gru Part (human actions, each labeled PA/PF/TO/IJ/EI) with a testable handoff condition between every step (412-426). Claude is right for scaffolding, docs from a complete outline, tests from documented criteria, format transforms, boilerplate; the human is right for "whether the problem being solved is the right problem", plausibility, accountability, integration, "when to stop" (434-436).

### 1B. Irreducibly Human  (/Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-irreducibly-human/)

- Course description: SYLLABUS.md:5-7 "investigate the division of work between people and AI"; README.md:5 "AI does the computing, drafting, and candidate generation it can usefully contribute. Humans practice the underlying mechanisms, evaluate evidence, maintain real relationships, and own authorized decisions." Fifteen lessons from seven tiers (README.md table, lines 13-29). SYLLABUS.md:7 explicitly says the taxonomy and its "strongest capability and philosophical claims are not conclusions students must accept to earn credit".
- ch.00-introduction.md is generic placeholder text (it never names the tiers); the real argument starts at ch.1. Use chapters/08-conclusion.md and chapters/97-fundamental-themes.md for the overview.
- **The seven tiers** (conclusion, /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-irreducibly-human/chapters/08-conclusion.md:15-19, the clearest one-paragraph map; figure caption line 21 bands them deprioritize / supervise / protect):
  1. Pattern & Association (ch.1): machine wins, "deprioritize on purpose"; human added to a superior machine can make things worse (Nielsen, "if AI > human, then AI + human < AI", conditional, [Medium], ch.1:17); "Prediction is cheap; judgment is scarce" (Agrawal/Gans/Goldfarb, ch.1:29-33).
  2. Embodied & Sensorimotor (ch.2): Moravec's paradox; the boundary is physical; unstructured world.
  3. Social & Personal (ch.3): "the simulacrum problem": convincing performance is not the capacity; gap is ontological.
  4. Metacognitive & Supervisory (ch.4): the machine cannot reliably report its own uncertainty ("Type 2" metacognitive sensitivity), so the human carries it; verdict "supervise" (ch.4:13-17, 63-65). Plausibility auditing named as the skill no curriculum teaches (ch.4:51-61), including its failure conditions (outside your domain knowledge, fluency taken as accuracy, "volume trap").
  5. Causal & Counterfactual (ch.5): prediction is not identification; readmission model "right about everything and wrong about what to do" (ch.5:7-15, composite flagged [verify]).
  6. Collective & Distributed (ch.6): "invisible groupthink" (label rated [Low], ch.6:15); homogenization and "algorithmic monoculture" (ch.6:64-72).
  7. Existential & Wisdom (ch.7): "reckoning is not judgment" (Brian Cantwell Smith, 2019); a self with something at stake, accountability, asking the question that wasn't asked (ch.7:49-65). The book marks this its "argued thesis" [Contested] (ch.7:51).
  NOTE: ch.97 omits a Tier 3 section (it jumps from Tier 2 at line 93 to Tier 4 at line 101). The tier list in ch.97 is therefore six sections plus the taxonomy header; use ch.08 for the full seven.
- **Division-of-labor principle** (ch.97:195-207): AI does Tier 1 work (generate structure, retrieve, adjust complexity, estimate once identification is set, format); humans do Tiers 4-7 (audit plausibility, formulate the problem, identify causal structure, hold positions under disagreement, institutional judgment, know what question is worth asking, be accountable). "The gate is at the boundary between what AI can do (Tier 1) and what requires human cognition (Tiers 4-7)" (ch.97:207). Hinge condition that must be on screen: "deprioritization is not deletion" and "you cannot audit what you do not know" (ch.1:63-67; conclusion line 37): keep the fundamentals to the level required to evaluate the machine.
- **Recursive capstone** (conclusion lines 25-31): knowing which tier you are in is itself a high-tier capacity, so the machine cannot run that audit for you.
- **Lesson 15** (/Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-irreducibly-human/lessons/15-division-of-labor-capstone/README.md): student builds and defends a division of labor. The per-lesson template is "**AI should** draft, compute, implement, and challenge the candidate. **Human should** practice the mechanism, verify the evidence, maintain actual relationships, and own the final handoff." (lines 44-46). Record the real split in CONTRIBUTIONS.md: what you did, what Claude contributed, what you accepted, changed, or rejected (line 48). Assessment answer (line 36): "Specific recorded AI assistance and human practice, interpretation, relationships, and authorized decisions tied to the actual artifact."

### 1C. Computational Skepticism for AI  (/Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-computational-skepticism-for-ai/)

- What it asks of a student: SYLLABUS.md:7 "interrogate AI outputs by building the mechanisms used to check them"; outcomes at lines 17-24 (turn a plausible claim into a prediction, assumption and falsification test; implement calibration/data-audit/robustness/group-metric checks; distinguish explanation vs association vs causal claims vs evidence of actual system state; design testable delegation contracts and approvals tied to a specific action; communicate with uncertainty; honest effort log). Course map = README.md lines 11-27 (15 lessons: toolkit, probability, data provenance, robustness, explanations, bias, fairness, agent outcomes, handoffs, visualization, uncertainty, accountability, limits, build-and-break studio, capstone).
- Load-bearing ideas (ch.1, /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-computational-skepticism-for-ai/chapters/01-the-skeptics-toolkit.md):
  - Skepticism is "a method", "a set of moves you can perform on a claim", not a disposition (line 37). It is "the discipline of knowing how you formed" beliefs (line 41). Hardest to do "when the output looks right" (line 43).
  - Four moves: Descartes = radical doubt as an inspection protocol ("what would have to be true for this to be wrong?" produces a checklist, lines 49-55); Hume = limits of induction (line 60); Popper = falsifiability, specify what a wrong answer looks like BEFORE reading the output (line 202); Kant/Plato ("the slice") = artifact vs world: "What is the artifact, and what is the world, and what is the relationship between them?" (line 115). Compact lineage in chapters/_expanded-four-moves.md (Descartes, Hume, Popper, Plato's Cave).
  - Verification cost: "producing the output is cheap, verifying is expensive" (lines 132-144, the same asymmetry as Conducting AI ch.2 in different words). "The answer is *never* 'automate the verification' ... design the system so that the verification a human can perform tells you what you need to know" (line 144).
  - Five Supervisory Capacities, same five (lines 152-180, table 170-176).
  - Fluency trap: fluency boosts confidence in the output and then confidence in your own evaluation (line 186-192).
  - Skepticism as team practice: put the moves in the workflow, not in one tired person (lines 210-224).
- Agent chapter (ch.8) and lesson 8 are the closest to game-making with Claude Code: a "false success report that nothing caught" (ch.8:15); lesson 8 builds an outcome checker that "inspects state independently of narration" (lessons/08-agent-outcomes-and-traces/README.md:5-9, 36). Lesson 9: a handoff needs "an acceptance condition someone can check" and a schema-valid packet can still be substantively unacceptable (lessons/09-delegation-and-handoffs/README.md).
- Editorial warnings you must respect: /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-computational-skepticism-for-ai/docs/reading-map.md:13 chapter 1 contains literal git merge-conflict markers (`<<<<<<< HEAD` / `>>>>>>> d78899b` pairs at ch.1 lines 51-55, 121-125 and 377-446); lines 11-17 say some manuscripts "make universal claims about AI's inability to verify ... Treat these as arguments to test against their scope and counterexamples, not empirical laws"; and "External tools can contribute useful verification."

### 1D. skepticism-ai/  (/Users/bear/Documents/CoWork/bear-textbooks/books/skepticism-ai/)
What it is: the *publication/working tree* behind skepticism.ai, not a finished textbook. Its README.md is the stock book-scaffold template (structure, build, "Computational Skepticism", Author Nik Bear Brown, Started 2026-05-30, Status Draft). chapters/ holds only 00-frontmatter, 02-chapter-01.md (779 bytes, a placeholder: "Replace this placeholder with your content"), 97-fundamental-themes.md (the shared file) and 99-back-matter. ABOUT.MD says the same. The real content is in youtube/ (about 20 `claude-liam-*` essay-reels such as report-is-not-the-world, what-would-prove-this-wrong, good-at-the-shadows, why-seventeen; with SAVE-STATE.md and cli-ideas.md), pantry/, papers/, lectures/. Do not cite skepticism-ai/chapters as a source.

---------------------------------------------------------------------------
## 2. Verbatim quotes worth putting on screen (12; each under 25 words; markdown asterisks removed, otherwise character-for-character)

Verified by a script that matched each string to its file/line (italics markers stripped only where noted).

1. "The tools play better than ever. The podium is empty." (10 words)
   /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-conducting-ai/chapters/01-the-conductorless-orchestra.md:51
2. "You can hand a machine the task. You cannot hand it the consequence" (13 words; sentence continues "and so you cannot hand it the verification that the consequence demands")
   .../info-7375-conducting-ai/chapters/01-the-conductorless-orchestra.md:87
3. "Plausibility was not incidental to the failure; it was the mechanism of the failure." (14)
   .../info-7375-conducting-ai/chapters/01-the-conductorless-orchestra.md:81
4. "Solving a problem and verifying a solution are different cognitive operations. AI automates the first." (15; a blockquote that continues)
   .../info-7375-conducting-ai/chapters/02-the-solve-verify-asymmetry.md:7
5. "More water through the wide channel does not widen the gate." (11)
   .../info-7375-conducting-ai/chapters/02-the-solve-verify-asymmetry.md:45
6. "The risk was never the level. The risk is always the gap." (12; original has italic "gap")
   .../info-7375-conducting-ai/chapters/03-three-levels-of-ai-usage.md:29
7. "handing problem definition to a model is an abdication, not a delegation." (12; original italicizes the last phrase)
   .../info-7375-conducting-ai/chapters/06-problem-formulation-part-1.md:39
8. "The AI will optimize a given formulation flawlessly. Only a human can decide that the formulation itself was wrong." (19)
   .../info-7375-conducting-ai/chapters/06-problem-formulation-part-1.md:23
9. "if each part is correct, the whole may still be wrong." (11)  [original bolds the clause]
   .../info-7375-conducting-ai/chapters/12-executive-integration-part-1.md:59
10. "When the same agent writes the implementation and the tests, the tests encode the same misunderstanding as the code." (19; bold in original)
    .../info-7375-conducting-ai/chapters/98-appendix-pragmatic-conductor.md:251
11. "The AI handles the technical execution. The human keeps the creative judgment." (12)
    .../info-7375-conducting-ai/chapters/97-fundamental-themes.md:324   (same file also in the other two books)
12. "you cannot audit what you do not know." (8; italic in original)
    .../info-7375-irreducibly-human/chapters/01-tier-1-pattern-and-association.md:65

Spares, all verified (swap in as needed):
- "Fluency stops being evidence." (ch.98 line 331, bold) and "An agent never questions the box." (ch.98:287, bold) and "Volume is not progress. A vertical slice that runs is." (ch.98:104) and "A test suite that passes when you deliberately break the code is a coconut." (ch.98:305) and "if you could not have written it, you cannot audit it" (ch.98:60), all in .../info-7375-conducting-ai/chapters/98-appendix-pragmatic-conductor.md.
- "Nine steps. Two of them are the agent's. The other seven are the reason the two are safe." (ch.98:359).
- "The dangerous zone in AI-assisted software builds is not where Claude fails visibly. It is where Claude succeeds fluently at the wrong task." is 24 words across lines 432: use only "It is where Claude succeeds fluently at the wrong task." (10 words, ch.97:432).
- "Anyone can use Claude Code. Boondogglers conduct it." (ch.97:467 and 479). Bear's own tagline; fine on screen for his own film.
- "Deprioritization is not deletion." (IH ch.08-conclusion.md:37) and "human cognitive value in the age of the machine is not uniform. It is tiered." (IH 08-conclusion.md:19).
- "A success statement records what was said; the state records what the action actually changed." (.../info-7375-computational-skepticism-for-ai/lessons/08-agent-outcomes-and-traces/README.md:36). Best single line for "Claude said it's done".
- "What is the artifact, and what is the world, and what is the relationship between them?" (.../info-7375-computational-skepticism-for-ai/chapters/01-the-skeptics-toolkit.md:115; italic in original.)
- "the primary enemy of skepticism is not laziness. It is confidence." (same file:43).
- "The output cost a fraction of a cent. The verification costs an hour of senior labor." (same file:138).
- The Semmelweis/Wiener/Einstein-Infeld lines in the books are themselves quotations of third parties; avoid putting them on screen as the books' words.

---------------------------------------------------------------------------
## 3. Best concrete examples/stories a film could reuse

Each: what it is, where, what it shows, and how it reuses for a game film.

1. **The conductorless orchestra / the podium is empty.** ch.1:39-51. Shows: AI augmented every instrument; nobody augmented the conductor; the conductor's whole contribution is supervisory. Reuse: the thesis image for the whole film. INFERRED mapping: in a game build, Claude Code is a section of virtuosos; the human is the one who holds the whole game in mind.
2. **The lawyer who re-prompted (Room one).** ch.1:7 and ch.2:75-77. Shows the sharpest asymmetry beat: asked to verify, the same source confirmed itself. Reuse: INFERRED: asking Claude "does this scene actually run / is this method real?" and trusting its yes. Real-world, documented: Mata v. Avianca, 6 fake cases, $5,000 sanction.
3. **The package that does not exist (Room two, "slopsquatting").** ch.1:9 and Appendix A.7 "Stay safe out there": "no `install` runs on a package name that came only from a model" (ch.98:264). Shows: fluent, idiomatic, executable and false. Reuse: nearest to game-dev: a plugin/addon name or an engine API call that does not exist. (A Godot-specific "method does not exist in this engine version" is INFERRED; the books do not mention it.)
4. **Priya's Tuesday.** ch.3:5-13, map at 59-65. 9:15 rename variables (glance is correct), 11:40 compare RFCs (glance is too light, the token-lifetime figure was never checked), 3:20 architecture proposal (the highest-stakes, problem-shaping output got the same four-second glance). "Nothing in Priya's Tuesday looks like negligence." Shows: supervision stayed flat while usage climbed three levels. Reuse: map a game-dev day to the same three levels: format GDScript / read the engine docs / let Claude propose the game's architecture or mechanic. (Game mapping INFERRED; the three-level structure is the book's.)
5. **Semmelweis.** ch.6:3-13, 59-67. Two clinics, ~10% vs <4% mortality; the modal framings ("noise" or "sicker patients") vs the salient one ("what do the doctors do that the midwives do not?"). Handwashing from April 1847 18.3% to June 2.2%. Book's own cautions: he lacked germ theory, was rejected, died in an asylum; "a correct, salient reframe can precede a correct mechanism" (ch.6:11). Shows: the AI would have optimized the tractable framing. Reuse: "what is this game actually about?" is the question the model will not ask; the film can say a design question is a formulation, and Claude will optimize any formulation you hand it.
6. **Five outputs, audit them cold (clinical dose, real case/wrong holding, R-squared 0.97, 53-foot trailer, flawless load calc).** ch.5:11-19, 39-55. Shows: how an expert "hears" a wrong note before checking. The trailer and the too-good R-squared are the most visual. Reuse: INFERRED: a physics number that is internally consistent but wrong for the game (a jump height that clears the level geometry; an enemy that fits no level), the "implausible fit" tell.
7. **One accurate output, two rooms (cost-optimized pathway at the finance committee vs the bedside).** ch.10:55-65. Shows: the same correct output is legitimate in one setting, not in another; "the notes are the model's, the meaning is supplied." Reuse: INFERRED: the same correct mechanic is right or wrong depending on the player and the game's intent.
8. **Four right answers, one wrong performance (transit facility).** ch.12:43-59, flagged a composite not an incident. Shows: locally correct, globally wrong; the un-fired re-engagement trigger. Reuse (INFERRED): movement, camera, collision and level tools each pass; the game does not work together. Caution: tell viewers it is illustrative, as the book does.
9. **Quarterback: four skills, one fourth quarter.** ch.12:3-9. Shows: holding all four at once is its own capacity. Visual and short.
10. **The consultant's $4.2 billion deck, "laundering".** ch.9:3-7, 46-56. A made-up number passes through extraction and formatting and ends up reading as audited. Shows: polish is not provenance. Reuse: INFERRED: a polished playable build that hides an unverified assumption.
11. **Checklist with Pronovost.** ch.9 Wayback box (lines 66-72). Real NEJM 2006: ~100 Michigan ICUs, five-item central-line checklist, infection rate to a median of zero in ~3 months. Book is careful: proof is Pronovost's, the popularization is Gawande's. Shows: explicit handoffs catch steps competent people skip under load.
12. **The nine-step Boondoggle Score for a discount rule.** ch.98:335-359. Two Minion steps (tracer bullet, implementation) + a Saboteur prompt; seven human steps (interrogate the requirement, find the box, write the contract, write the tests from the contract, audit the diff, re-engagement check, sign). Closest thing in the books to a literal "what the human does / what Claude does" ledger for building with Claude Code. Reuse: adapt the structure; do not claim the books wrote a game version. This also matches the cc-explainer CONDUCT/HUMAN beat vocabulary.
13. **Ash and "you broke my toy" (agent said done; state said otherwise).** CS ch.1:11-15 and ch.8:5-15. Agent reported the email deleted and the account secured; the data was still on the server. Shows: the false success report; lesson 8's checker. Strongest story for "Claude says the game builds and runs". (See fact-check flag on Ash in section 5.)
14. **Epic Sepsis Model.** CS ch.1:5 (and the opening of the book). Validated by the vendor's own metrics, missed ~2 of 3 sepsis cases on external validation of 27,697 patients, alerted on 18% of all hospitalized patients. Shows: "By every measure its builders chose, it had succeeded." Reuse: a game that passes every test its builder wrote.
15. **Knight Capital, Aug 1 2012.** CS chapters/_expanded-four-moves.md:11 (also in ch.1 inside a conflict block). 7 of 8 servers updated, reused flag bit woke dead code; ~45 minutes, ~$440 million. Shows: "deployment succeeded" is not "the system is doing what we intend". Reuse: shipping a build.
16. **Brutalist: AI removes the technical barrier, human keeps the creative judgment.** ch.97:344-372. The most direct statement of the film's thesis as applied to a creative domain, in Bear's own words, and it ends "whether the work is good" (line 368).
17. **The hospital's four-minute radiologist (Tier 1) and the dental segmentation reallocation.** IH ch.1:3-9. Shows: same move, opposite outcomes; what matters is what the human does with the recovered capacity. Good bridge for "what Claude takes off your plate and what you spend it on".
18. **The Tigers-game lemonade (Ratté).** IH ch.7:3-13. Every official correctly applied the rule; nobody asked whether the rule served its purpose in this case. Shows: judgment vs reckoning. Likely too heavy for a game film.

---------------------------------------------------------------------------
## 4. Honest map: making games with an AI that writes the code

Everything in the "applies" column is INFERRED application of a book's principle; the books themselves say nothing about games.

### What the human must judge (the books' vocabulary -> game work)
| Human job | Book anchor | Game-making reading (INFERRED) |
|---|---|---|
| Decide what the game is for and what question it answers | Problem formulation: "abdication, not a delegation" (ch.6:39); "find the box" and the requirements pit (ch.98 A.8); formulate-vs-optimize (ch.6:23) | Design intent, the game's core loop, the audience, the constraint that is real vs assumed. This is the strongest, best-supported mapping. The film's own Walker GDD/README practice fits the "Communicate" rule (one constraints file the agent reads, A.1). |
| Hear that something is wrong before running the checker | Plausibility auditing: the "wrong note" (ch.4:28); anomaly detection against a held model (ch.4:61) | "This enemy cannot be dodged", "that jump is not possible", an implausibly perfect number. Needs you to know the domain: "you cannot audit what you do not know" (IH ch.1:65). So a student must understand game basics to the level needed to evaluate, which is a teaching claim the books make ("deprioritization is not deletion"). |
| Judge whether it is fun, feels right, means what you intended | Interpretive judgment: pragmatic vs moral vs cognitive legitimacy; thin vs thick (ch.10-11); Brutalist "whether the work is good" (ch.97:368) | Feel, fun, tone and meaning are exactly "supplied by an interpreter who knows the context" (ch.10:3). This is the FIT, but it is an extension: the books' examples are institutional (hospital, client), not aesthetic experience. Say "taste and intent are the human's", do not say the books prove an AI cannot assess fun. |
| Playtest with real players / check the world, not the report | CS: "What is the artifact, what is the world, what is the relationship?" (CS ch.1:115); lesson 8 "A success statement records what was said; the state records what the action actually changed." | The artifact is the code and Claude's "it works"; the world is a person holding a controller, or at least the game actually running. Map = good, but note the books never mention playtesting, and the lesson-8 checker is a state-checker for agent actions, not a fun-test. |
| Own the decision / sign the commit | Memo B signature (ch.11:49); A.1 "Take responsibility": the agent wrote it "works even less well, because you approved the diff" | Accountability for what ships. Direct fit. |
| Notice when the work has moved | Re-engagement trigger (ch.12:31); context drift via `git diff --stat` (A.1 "boiled frogs") | When a playtest finding reopens the design, go back; log it. Direct fit. |
| Hold the whole game in mind | Executive integration; "four right answers, one wrong performance" (ch.12:43-59) | Systems that each pass but do not cohere (INFERRED). |

### What the AI does (the books' vocabulary)
Tier 1 / "Minion Part": scaffolding from a complete spec, boilerplate, tests from documented acceptance criteria, format/data transforms, variants of a specified pattern, drafting docs from a complete outline (ch.97:434), renaming/extract-method/apply patches (ch.98:25 "now mechanical"), enumerating candidate edge cases (ch.98 A.8: "good at generating candidates. It cannot tell you which ones matter here"). INFERRED game versions: GDScript, scene/node wiring, placeholder assets, repetitive variants, running headless checks.

### Principles from Appendix A that transfer cleanly to a Claude Code + Godot workflow (INFERRED application of the book's rules)
- Tracer bullet first: one thin vertical slice that runs end to end before any feature generation (ch.98:104-107). This is the book's "hard gate".
- Throwaway prototypes stay throwaway: branch deleted or re-derived, "never promoted silently" (ch.98:109-112).
- Tests (or checks) must not come from the same generation as the code (ch.98:251-267, ranked independence list) and the saboteur check (introduce a defect, confirm the suite catches it) (ch.98:305-312). Applicable to any automated check you ask Claude to write; "a coconut" test suite is a real trap.
- Agent treats your codebase as its style guide, so one tolerated bad pattern propagates (ch.98:44).
- Volume is not progress (ch.98:104).
- "Fluency stops being evidence" (ch.98:331): clean idiomatic code no longer signals a competent author.
- Context in one file the agent reads (CLAUDE.md/AGENTS.md), no constraint stated in two places (ch.98 A.1 "Communicate"). Fits the Brutalist three-files idea (ch.97:328-340).

### Which would be a STRETCH, or should be avoided
1. P vs NP (ch.2:17-23): the book itself says it is only an analogy and "if you ever hear someone say 'P vs NP proves AI can't verify itself', they have overreached" (line 23). Leave it out or cite as bounded.
2. "AI can never verify / can never be fun / can never be creative." The books say "wager", "argued thesis", "[Contested]" (ch.2:59, IH ch.7:51). Also the books concede tool-using reasoning models verify more (ch.2:61-71), and the course layer says external tools can verify (CS reading-map line 15). A game film with Claude running the game itself, taking screenshots, running headless tests is consistent with the books: the grounding comes from the tool, and a human chose it. Say "Claude can run checks; a human decides which checks matter and whether the result is what was intended."
3. Tier 2 (embodied) is about robot dexterity, Moravec's paradox, surgeons' hands (IH ch.2). It is NOT about game feel. Linking the player's hands to "feel" is INFERRED. Safer to leave it out.
4. Tier 3 (social/personal): about simulated empathy and relationships, not NPC dialogue. Leave out.
5. Tier 5 (causal), Tier 6 (collective), Tier 7 (wisdom): the ethical/causal examples are all clinical, legal, civic. Possible INFERRED links: Tier 6 homogenization to "AI-made games converge on the same look" (IH ch.6:64-72, rated high for the mechanism in general, not shown for games); Tier 7 "knowing what question to ask" as design vision. Mark as extrapolation if used.
6. Gardner / multiple intelligences, head-hand-heart-spirit weave (ch.12:37-41), the five-layer capability stack as an "industry standard" (ch.8:9 says it is not), the three levels as "a published model" (ch.3:19 says it is not): do not present these as researched frameworks.
7. Quantitative productivity or "56% wage premium" (ch.97:241), Bastani 48%/17pt, Kosmyna EEG (see section 5): not relevant to a game film and partly flagged low-evidence.
8. Do not state that Bear's course "teaches" the five capacities as graded items. The Conducting AI SYLLABUS says the Supervisory Analysis is the capstone; CSYE 7270 is a different course (INFERRED; I did not read its materials).

### Film-structure suggestion that stays inside the books (INFERRED)
Open on the empty podium; show Level I/II/III mapped to three Claude Code moments; give the solve-verify asymmetry in one sentence plus the "report vs world" line; then a two-column ledger HUMAN / CLAUDE using the Boondoggle Score vocabulary (PF design intent, PA hear the wrong note, TO choose the check, IJ taste and meaning, EI hold the whole, sign) with Claude's column limited to what the books list as Tier 1. Close on Wiener's hammock or "Deprioritization is not deletion". (Memory rule for this folder: bookloop/lecture films should be self-contained and not name the books unless the film is for an INFO 7375 course; CSYE 7270 is not one. That is from Bear's saved notes, not these books.)

---------------------------------------------------------------------------
## 5. Numbers, dates and facts a film would need to check

Conducting AI /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-conducting-ai/chapters/
- ch.1:7 Mata v. Avianca: six non-existent cases (Varghese v. China Southern, Martinez v. Delta, Shaboon v. EgyptAir named); sanction "$5,000 under Rule 11" for Schwartz "and his co-counsel"; Schwartz "three decades of practice". Citation in ch.1:109: 678 F. Supp. 3d 443 (S.D.N.Y. 2023). Verify who was sanctioned and the date (book gives no date in ch.1; IH ch.4:3 says "spring of 2023").
- ch.1:9 slopsquatting: "roughly 19-22% of packages suggested ... nonexistent"; "~30% of prompts produce at least one hallucinated package"; coinage credited to Seth Larson in the source list (ch.1:110). Verify against the primary study.
- ch.1:11 physician chatbot red-team "5-13% ... potentially unsafe" (source list: 5% Claude to 13% GPT-4o/Llama, data Sep-Dec 2024, arXiv:2507.18905).
- ch.1:13 Deloitte Australia: "roughly A$440,000 (about US$290,000)", refund of final installment, Azure OpenAI, reported October 2025 (Fortune, The Register).
- ch.1:57 Gardner Frames of Mind 1983, seven intelligences.
- ch.2:17 Cook 1971 and Levin; ch.2:25 Turing Award 1982; STOC '71 pp.151-158.
- ch.2:35 Stechly/Valmeekam/Kambhampati arXiv:2402.08115 (ICLR 2025); GPT-4 on Game of 24, graph coloring, STRIPS.
- ch.3: Sheridan & Verplank 1978; Parasuraman, Sheridan & Wickens 2000; Parasuraman & Manzey 2010 *Human Factors* 52(3):381-410; Shneiderman 2020/2022; Engelbart 1962. The de-skilling figures are explicitly [Low] "need checking" (ch.3:47).
- ch.4:3-7 GPT-4 bar exam: "roughly the 90th percentile" (March 2023); Martinez 2024: ~69th percentile of all takers, ~63rd first-time, ~48th among passers, ~15th on essays [Contested]. ch.4:49 ARC: o3 Dec 2024, 75.7% (public limit) and 87.5% (high compute); ARC-AGI-2 launched March 2025; non-expert humans over 60% average; late-2025 best verified commercial "high-30s", Gemini-3-based refinement "about 54%"; book says "check the current ARC Prize technical report before quoting any single figure". Date-sensitive: re-verify at publication.
- ch.5:61-63 Mosier & Skitka; Lee & See 2004 calibrated trust. A single study on transparency vs confidence displays [Medium].
- ch.6:5-9 Semmelweis: First Clinic "averaged around ten percent and reached above eighteen percent in the worst months"; Second Clinic "under four percent"; handwashing in "May 1847" with chlorinated lime; mortality "18.3 percent in April 1847 to 2.2 percent that June". The "worst months above 18%" and the exact monthly figures should be checked against Semmelweis's own tables; the book does not give a primary citation here. Died in an asylum (ch.6:11).
- ch.6:75 Einstein & Infeld, *The Evolution of Physics*, 1938, p.92 (book insists on citing both authors).
- ch.8: Thomas & Hunt ETC; McIlroy: pipe 1973, philosophy 1978 (book distinguishes the two dates). A 98.7% vs 82.3% valid-JSON figure is flagged "single-benchmark, illustrative" (ch.8:17). Vendor "agents embedded by mid-2026" forecast flagged [Low] (ch.8:23).
- ch.9: Pronovost NEJM 355(26):2725-2732 (Dec 2006), ~100 Michigan ICUs, five-item checklist, median to zero within ~3 months; Johns Hopkins "~11% toward zero" is via Gawande [Medium]. LLM-judge "rating roulette" 2025 study [Medium].
- ch.10: Suchman 1995 *Academy of Management Review* 20(3):571-610.
- ch.12: Norman & Shallice 1980; Conway 1968; Follett 1924/1925; Pestalozzi head-heart-hands (mnemonic [Low]).
- ch.13: Supervisory Analysis 2,500-4,000 words (ch.13:9); Simon 1962.
- ch.15:27-31: prompt-injection attack success "low-double-digits to ~74%" and ">30%" (cited as a range, [High] that the vulnerability exists); position bias "more than ten percentage points". Dreyfus 1972/1979/1992.
- ch.97 (same file in all three books): PwC 2025 Global AI Jobs Barometer: 56% wage premium (doubled from 25%), jobs requiring AI skills +7.5% while postings -11.3% (line 241); Bastani: AI users scored 48% higher in practice and 17 percentage points lower on the unassisted exam (line 24); Kosmyna EEG "up to 55% reduction in functional brain connectivity" (line 26). **Internal inconsistency:** ch.97 states the Kosmyna figure as plain fact, while IH ch.1:53 rates the same study [Low/preprint], N=54 then 18 completing, not peer-reviewed. Do not use the 55% on screen without checking the primary source.

Irreducibly Human /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-irreducibly-human/chapters/
- ch.1: Nielsen "if AI > human, then AI + human < AI" (late 2025, [Medium]; he also forecasts override-malpractice "in a few more years", which the book treats as a prediction, not present law); dental segmentation 15-18 minutes manual [Medium]; WEF Future of Jobs 2025 "39% of core skills to change by 2030".
- ch.2: Moravec 1988 *Mind Children*; hand "commonly modeled as 27 degrees of freedom" (22 and 26 also appear); reflex ~10 ms vs VLA up to ~500 ms; GR00T N1, Helix 7-9 Hz and 200 Hz; Brooks "beyond 2036". Dated robotics claims; book says "treat the door as a dated illustration".
- ch.3: UCSD three-party Turing test, GPT-4.5 judged human 73% with persona, ~36% without (arXiv:2503.23674).
- ch.4: ABA Formal Opinion 512, July 29, 2024; Lee et al. *PNAS Nexus* 4(5):pgaf133 (2025); sanction amounts "should be spot-checked" (ch.4:7).
- ch.5: readmission-model story is a composite, tagged [verify: a citable named deployment].
- ch.7: Ratté / Mike's Hard Lemonade, Comerica Park, April 2008; Smith 2019 *The Promise of Artificial Intelligence*.

Computational Skepticism /Users/bear/Documents/CoWork/bear-textbooks/books/info-7375-computational-skepticism-for-ai/
- ch.1:5 Epic Sepsis Model: Wong et al. JAMA Internal Medicine 181(8), 2021; 27,697 patients; missed "roughly two of every three"; alerts on 18% of hospitalized patients.
- ch.1 / _expanded-four-moves.md:11 Knight Capital, Aug 1 2012: 8 servers (7 updated), "Power Peg" code from 2003, ~45 minutes, 4+ million trades, 154 stocks, ~$440 million (SEC 2013). Note the text differs between versions: ch.1 (conflict block) says "absorbed by a competitor within months", the _expanded file says "ceased to exist as an independent company by year's end". Verify.
- _expanded-four-moves.md:19 Zillow Offers: ~7,000 homes, shut down November 2021, write-down "more than half a billion dollars", ~a quarter of staff; Google Flu Trends Aug 2011-Sep 2013; DeGrave, Janizek & Lee 2021 *Nature Machine Intelligence*.
- Ash / *Agents of Chaos* (Shapira et al., arXiv:2602.20021, 2026), ch.1:7 and ch.8:5-15. **Fact-check flag:** the book describes Ash as "a security researcher" who "gave an autonomous AI agent privileged access" and later "discovered" the email was still there. Bear's saved note on the INFO 7375 CS lectures says in the paper "'Ash' is the agent, not a researcher". The two conflict; check the paper before saying who Ash is on screen.
- Source-text defects: ch.1 contains literal merge-conflict markers (`<<<<<<< HEAD`, `>>>>>>> d78899b`) with two competing versions of the Knight Capital and DeGrave passages (reading-map.md:13 confirms). Quote from the _expanded-four-moves.md version or from text outside the conflict blocks. Two ch.9 files, two ch.10, two ch.13 duplicates exist; reading-map.md:9 says which are assigned (09 delegation, 10 visualization, 12 accountability, 13 limits).

General source-text hazards for any on-screen quote
- Conducting AI ch.13 still has `[author to confirm ...]` markers (ch.13 lines 19, 36; line 116 has an `[Editor...]` note); several claims carry evidence tags like [High]/[Medium]/[Low]/[Contested]; quote the text without tags but honour them (a [Low] claim should not be stated flatly).
- Many "stories" are composites and say so (ch.1 Room five, ch.12 transit, IH ch.5 readmission, CS ch.1 swollen-leg woman, CS ch.13 clinical opener). A film must not present them as documented incidents.
- Files are drafts for hand-rewrite in places (CS ch.8 line 1 comment: "Rough draft for hand-rewrite").
