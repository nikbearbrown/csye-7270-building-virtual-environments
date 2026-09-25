# Blueprint — Course vision

Status: proposed for Professor Brown's review. No human approval is implied.

## One reader

A Northeastern CSYE 7270 graduate student who has programmed in a language such as Python but may never have shipped a game. The course assumes access to Claude Code, as specified by the instructor; tool access is checked before graded work. Students do not need prior Unity, Unreal, C#, Blender, or Godot experience.

## Capability at the end

The student can turn a bounded game brief into a reproducible Godot experience, use a coding agent without surrendering design judgment, integrate attributable assets, test important invariants, and explain what the project actually does. Evidence includes a playable project, design decisions, source history, playtest observations, and an honest account of human and AI contributions.

## Central argument

Agentic game development is the practice of making intent testable, directing implementation in small steps, and confronting the result in play—not the practice of accepting plausible generated code.

## The course's two complementary loops

**Learning:** Predict → Build It → Use It → Ship It → Verify.

**Walker production:** Game brief → Build → Playtest → Inspect → Revise → Export.

Students predict before delegating; run and play each change; ship a reproducible source version; then verify the submitted version from a clean start. Verification is also repeated throughout development, not postponed until the final step. Export readiness is a separate claim from source readiness.

## Opening sequence fixed by the instructor

1. **Walker + Godot:** inspect and run walker-jumpman; replace its main character's visual identity without silently changing its physics; extend the actual playable level; retain tests and document a human playtest.
2. **Prompting game art:** use an available image tool such as Gemini, ChatGPT, or Midjourney to develop assets against technical constraints, then judge them inside Godot. Walker prompting assistants are planned support, not a dependency falsely represented as installed today.
3. **Prompting Blender through MCP:** supervise a small modeling task, inspect the geometry and materials, export a portable asset, and validate it in Godot. Use the selected community integration's documentation, not unverified installation claims in a video transcript.

## Remaining scope

Retain the original course's substantive systems: GDDs, scene architecture, 2D and 3D environments, collision and physics, shaders and materials, particles, animation, audio, game AI, procedural content, profiling, analytics, networking, mobile/web deployment, and an appropriately scoped XR introduction. Replace separate Unity/Unreal onboarding blocks with a coherent Godot progression. GDD work begins with a short change brief in Module 1 and becomes more detailed as project decisions accumulate.

The book and course are not limited to a 2D platformer. That familiar starter reduces the first week's setup burden; subsequent work explicitly introduces 3D assets and environments.

## Position among existing learning resources

These are comparisons of teaching approaches, not required purchases:

- [Godot's first 2D game tutorial](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/index.html) provides a first engine project. This course instead begins by inspecting and changing a supplied playable project, with agent delegation and regression evidence made explicit.
- [GDQuest's Learn GDScript From Zero](https://gdquest.github.io/learn-gdscript/) offers programming practice. Here programming literacy supports supervising and explaining a real project; it does not replace runtime inspection.
- [Godot's first 3D game tutorial](https://docs.godotengine.org/en/stable/getting_started/first_3d_game/index.html) supplies a useful 3D learning reference. This course adds a source-to-runtime asset pipeline, constrained prompting, provenance, and a sustained design/verification record.

## Human / AI boundary

AI can propose designs, explain source, implement authorized changes, prepare candidate assets, run mechanical checks, and summarize results. Humans determine intent, acceptable scope, artistic direction, playability, fairness, accessibility, permissions, and release decisions. Neither an AI assertion nor a passing headless test substitutes for a human having played the build.

## First release boundary

The requested deliverables are the syllabus, Module 1 (with its one-to-one Chapter 1), and a new IMSCC. The original Spring 2026 export remains untouched. Do not import its old Unity/Unreal assignments, quizzes, binaries, student records, or unrelated book files into the new package. Later modules appear as a syllabus roadmap until authored; they must not appear as completed learning materials.

## Instructor-confirmed course settings

- **Term: Fall 2026.** Confirmed by Professor Brown on September 10, 2026.
- **Late penalty: 10% per day.** Confirmed by Professor Brown on September 10, 2026; replaces the conflicting 5% daily provision in the supplied syllabus.
- **Assignment proportions: 60 / 10 / 10 / 20 percent.** Assignment-specific implementation or explanation / Frictional / GitHub version matching Canvas / Relative Quartile. For a 25-point explainer this is 15 / 2.5 / 2.5 / 5, with the 15 explanation points divided 6 / 4 / 3 / 2 as supplied by the instructor. The [assessment policy](prerequisites/assessment-policy.md) and [explainer rubric](assignments/rubrics/25-point-explainer.md) preserve the criteria, the full-group comparative review, and responsibility for explaining AI-assisted work.
- **Assignment cadence and value: one every 10 days, 100 points each.** Modules and chapters correspond one-to-one; graded assignment timing is separate. The 25-point rubric is a proportional example, not a scheduled assignment.
- **Required Godot explainer:** each assignment includes a rendered film made using the appropriate Brutalist Godot skill. Implementation and explanation share the 60-point category; Frictional / GitHub matching Canvas / Relative Quartile remain 10 / 10 / 20. The [course AI policy](prerequisites/ai-policy.md), [video guide](prerequisites/brutalist-godot-explainers.md), and [100-point framework](assignments/rubrics/100-point-assignment.md) record these directions and link Professor Brown's AI-policy video.

## Decisions to resolve before student release

- Blueprint review procedure: whether to pause at each planning gate or prepare all three requested deliverables together as clearly labeled review drafts.

The university boilerplate will be preserved from the instructor's supplied syllabus. Changes to course software, pedagogy, assignments, and engine-specific examples will be explicit. Formal book approval gates remain unsigned until the human reviews them.
