# CSYE 7270 Building Virtual Environments: Fall 2026 exam

## Executive summary

The Fall 2026 exam checks whether you can **direct and audit a coding agent in Godot** using the course's exact terms. It is worth 100 points: **7 case questions x 10 points = 70, plus 6 multiple-answer questions x 5 points = 30.** In each case an agent hands you a confident report with **one planted flaw**; you find it, name it with the right term, ask for evidence, and say what to do next. This folder holds two full **practice exams**, each with its answer key in a **separate file**. The practice exams are practice only: the real exam uses different cases and different questions.

## What the exam tests

Not memorised facts, and not writing style. It tests whether you can use the course's terms precisely enough to (1) tell an agent exactly what to do and (2) notice when an agent's report does not prove what it claims. "Claim versus evidence" is the habit behind every question.

## Format and time

| Part | What | Points | Suggested time |
|---|---|---:|---|
| A | 7 cases, 10 points each | 70 | about 6 to 7 minutes per case |
| B | 6 multiple-answer questions, 5 points each | 30 | about 2 minutes per question |
| | Total | 100 | |

## What a case looks like

Every case has the same parts:

1. **Scenario.** A designer, artist or producer with a goal. They may not read code.
2. **The instruction** a person gave the coding agent.
3. **The agent's output.** A short report, plan or diff summary. It sounds sure of itself and contains **one planted flaw** on a concept from the course. Agent outputs are **author-written for illustration**, not sampled runs.
4. **Four probes** (10 points in all): what is the flaw and its exact term (5); what one check would turn the agent's claim into evidence (2); what corrected instruction would you send the agent (2); how would you explain it to the designer in two plain sentences (1).

## Multiple-answer questions (Part B)

Each question has **five statements, A to E**. Each statement is **true or false on its own**, worth **1 point**. Check the ones you think are true. You score a point for a true statement you checked and for a false statement you left blank. Read each statement by itself: a strong word like "always" often makes a statement false, but not every strong-sounding statement is false.

## How cases are scored

| What earns points | Points |
|---|---:|
| Catches the flaw (you say what is actually wrong) | 3 |
| Uses the exact term for it | 2 |
| Asks for evidence (a check that can pass or fail and aims at the flaw) | 2 |
| Gives a fix or next step the agent could carry out | 2 |
| Keeps scope and plain language (does not over-claim; a non-expert could follow) | 1 |

- **If you miss the flaw, the case is capped at 5/10**, however good the rest sounds. Fluent jargon cannot buy points.
- **Grammar, spelling, length and polish earn nothing.** Short, rough English that names the real problem scores the same as polished prose.
- A correct idea written in another case's terms does not earn this case's term credit.

## How to practise

1. Do a practice exam **cold**: no notes, no key, about 100 minutes in all.
2. Only then open its `-KEY` file. For each case read the flaw, the terms that earn credit, the near-misses, and the sample answer, and compare with what you wrote. For Part B read the one-line reason for every statement.
3. Study what you missed, then do the second practice exam.

| File | What |
|---|---|
| [practice-exam-01.md](practice-exam-01.md) | 7 cases and 6 multiple-answer questions, no answers |
| [practice-exam-01-KEY.md](practice-exam-01-KEY.md) | answers and reasons for exam 01 |
| [practice-exam-02.md](practice-exam-02.md) | a second set; no case or question repeats from exam 01 |
| [practice-exam-02-KEY.md](practice-exam-02-KEY.md) | answers and reasons for exam 02 |

## What to study

- [Cheat sheet](https://github.com/nikbearbrown/interview-bank/tree/main/csye-7270-building-virtual-environments/ma-exams/CHEAT-SHEET.md)
- [Glossary of tested terms](https://github.com/nikbearbrown/interview-bank/tree/main/csye-7270-building-virtual-environments/ma-exams/GLOSSARY-jargon-midterm.md)
- [Question bank](https://github.com/nikbearbrown/interview-bank/tree/main/csye-7270-building-virtual-environments/ma-exams/question-bank/INDEX.md): 678 multiple-answer questions by chapter, with keys and reasons
- [More multiple-answer practice exams](https://github.com/nikbearbrown/interview-bank/tree/main/csye-7270-building-virtual-environments/ma-exams/practice-exams/) (exam-01 to exam-06, each with a separate `-KEY` file)

## Notes

- **Practice only.** These cases and questions are for practice. The real Fall 2026 exam uses different cases and different questions, so do not expect to see any of these on it.
- **Awaiting a game developer's check.** The keys for the physics and shader cases (the two clocks, collision layer and mask, alpha, sRGB decode, golden images) have not yet been verified by a game developer. If a key looks wrong to you on those, say so.
- **Draft.** The cases come from the draft case set and have not been signed off by the instructor.
- The names in scenarios are made up.
