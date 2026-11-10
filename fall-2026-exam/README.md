# CSYE 7270 Building Virtual Environments: Fall 2026 exam

## Executive summary

The Fall 2026 exam is **entirely multiple-answer** and tests the **high-level concepts of the whole course**: what a shader is, what a material is, how a collider differs from a trigger, how a sprite sheet differs from a rig, what a state machine is for, what a frame budget is, and how an agent's claim differs from evidence. It is worth 100 points: **20 questions x 5 points.** There are no cases, no code to read and no shader code to write or change. This folder holds two full **practice exams**, each with its answer key in a **separate file**. The practice exams are practice only: the real exam uses different questions.

## What the exam tests

Whether you know what the course's ideas mean and how they differ from their near neighbours, so that you can tell an AI coding agent or a teammate exactly what you want and notice when a report does not prove what it claims. It does not test memorised facts, code, menu paths or writing style.

## Format and time

| What | Points | Suggested time |
|---|---:|---|
| 20 multiple-answer questions, 5 points each | 100 | about 3 minutes per question, about 60 minutes in all |

Each question has **five statements, A to E**, and **anywhere from one to four of them can be true**. Each statement is **true or false on its own**, worth **1 point**. Check the ones you think are true. You score a point for a true statement you checked and for a false statement you left blank. Read each statement by itself: a strong word like "always" often makes a statement false, but not every strong-sounding statement is false.

## What the exam covers

Every practice exam has one question on each of these topics, so each one is a sample of the whole course. The exam is about Godot only, and every question follows the course chapters: each answer key names the chapter passage the question follows.

| # | Topic |
|---:|---|
| 1 | Chapter 0: Checking an agent's report against evidence |
| 2 | Chapter 0: Working safely with an agent (instruction files, permissions, headless runs) |
| 3 | Chapter 1: Walker, Godot projects and how a game updates |
| 4 | Chapter 2: Game art and sound (pixel art, asset requests, loops) |
| 5 | Chapter 3: 3D assets from Blender to Godot |
| 6 | Chapter 3: Driving Blender with an agent (MCP and scripts) |
| 7 | Chapter 4: Nodes, scenes, signals and groups |
| 8 | Chapter 4: Collision (colliders, triggers, layers and masks) |
| 9 | Chapter 5: Game design documents and requirements |
| 10 | Chapter 6: Shaders |
| 11 | Chapter 7: Materials (material, shader, texture) |
| 12 | Chapter 7: Textures (colour, data and normal maps) |
| 13 | Chapter 8: Checking a shader |
| 14 | Chapter 9: Particle effects |
| 15 | Chapter 10: Animation foundations (sprite sheets, rigs, keyframes, inverse kinematics) |
| 16 | Chapter 11: State machines and blending |
| 17 | Chapter 12: Audio and triggers |
| 18 | Chapter 13: Profiling and optimization |
| 19 | Chapter 14: How game characters decide (state machines, behavior trees) |
| 20 | Chapter 14: Generating levels (seed, noise, checking) |

Chapter 15 (the final project) is not examined.

## How to practise

1. Do a practice exam **cold**: no notes, no key, no phone, no laptop; paper and pen or pencil; about 60 minutes.
2. Only then open its `-KEY` file. For every statement you got wrong, read the one-line reason and then the course chapter named by the topic.
3. Study what you missed, then do the second practice exam.

| File | What |
|---|---|
| [practice-exam-01.md](practice-exam-01.md) | 20 multiple-answer questions, no answers |
| [practice-exam-01-KEY.md](practice-exam-01-KEY.md) | answers and a reason for every statement |
| [practice-exam-02.md](practice-exam-02.md) | a second exam; no question repeats from exam 01 |
| [practice-exam-02-KEY.md](practice-exam-02-KEY.md) | answers and a reason for every statement |

## How to prepare

- [HOW-TO-PREPARE.md](HOW-TO-PREPARE.md): a study guide for this exam: what the research says, a 14-day and a 3-day plan, how to learn each idea and how to practise the multiple-answer questions, and the common mistakes.
- [EXAM-PREP-GUIDE.md](EXAM-PREP-GUIDE.md): a shorter preparation guide for the same exam, with course-specific review pairs and the same plans.

## What to study

- The course chapters ([chapters](../chapters/README.md)) and lessons ([modules](../modules/README.md)). Every question follows a passage in the chapters, and each answer key names the passage.
- The two practice exams above: after you finish one, read the reason under every statement you got wrong.

The older question bank, cheat sheet and glossary in the `interview-bank` repository were written for an earlier version of this exam and cover other engines and code that this exam does not, so they are not needed.

## Notes

- **Practice only.** The real Fall 2026 exam uses different questions, so do not expect to see any of these on it.
- **Awaiting a game developer's check.** The keys for the physics, shader, material, audio and animation questions have not yet been verified by a game developer. If a key looks wrong to you on those, say so.
- **Draft.** The questions were written from the course chapters (and checked against the chapter text by an AI reader, which is not a substitute for the instructor) and have not been signed off by the instructor.
- **No case questions.** An earlier draft of this exam used seven case questions. That format is no longer used and the old case set has been removed from the repository.
