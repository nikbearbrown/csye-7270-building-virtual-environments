# Canvas delivery — Fall 2026

## Executive summary

**What this is.** How the rebuilt CSYE 7270 course gets into Canvas. One command turns the course's Markdown and JSON sources into an importable Canvas package (16 modules, 38 pages, 10 assignments, 16 ungraded practice quizzes, the syllabus, and a 10%-per-day late policy), and into one HTML fragment per page for pasting by hand.

**Why read it.** It tells you how to build the package, how to import it into a Canvas course, what to check afterwards, and, most important, what has **not** been verified: the package has never been imported into a live Canvas, because nothing here has access to one.

**What it decided.** Everything imports **unpublished**, so nothing reaches students until you publish it. No due dates are set; the assignments say "Day 10, 20, … 100" and Canvas dates are yours to set. An assignment that covers two modules is listed in both. The old Spring 2026 export is not imported: no media, no Unity or Unreal items, no old quizzes, no student data. [`OLD-TO-NEW.md`](OLD-TO-NEW.md) says where every old item went.

**What it did not do.** It did not touch Canvas, and it did not push anything to GitHub. Chapter and example links in the pages point at the course repository on GitHub and return 404 until `chapters/` and `examples/` are pushed.

---

## Build

From the course root (needs Python 3 and pandoc):

```bash
python3 scripts/build_course.py
```

It writes two things, both ignored by git:

| Output | What it is |
|---|---|
| `canvas/package/csye7270-fall-2026-godot-walker.imscc` | The importable Canvas package. |
| `canvas/paste/*.html` | One HTML fragment per page and assignment, for the manual-paste route. |

Two options: `--state published` imports everything published instead of unpublished, and `--partial` skips sources that do not exist yet (for testing while writing). The script ends with an integrity check: every XML file is well-formed and every reference in the manifest and module list resolves. That proves the package is internally consistent. It does not prove Canvas accepts it.

`python3 scripts/check_course.py` checks the sources first: heading order, word counts, quiz keys and shape, links, and that each assignment's 60-point table sums to 60.

## Import into Canvas

Try a sandbox course first. In the destination course, follow Canvas's [import guide](https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-import-a-Canvas-course-export-package/ta-p/795): **Settings → Import Content into this Course → Content Type: Canvas Course Export Package →** choose the `.imscc` file **→ All content → Import**. Canvas warns that an import can overwrite some course settings, so use a course you can throw away until you have checked it.

## What is in the package

| Part | Count | Notes |
|---|---|---|
| Modules | 16 | Module 0 (Start Here) plus Modules 1–15, in order. Each has Lecture, Practice, Assignment (where one applies) and Links headers, the layout of the old course. |
| Pages | 38 | One lecture page per module (two for Module 14), a Helpful-links page per module, and Module 0's course map, AI policy, grading, framework and explainer pages. |
| Assignments | 10 | 100 points each, file upload plus text entry, in one "Assignments" group. No due dates. |
| Practice quizzes | 16 | Six multiple-choice questions each, unlimited attempts, correct answers and feedback shown. Ungraded. Answer order shuffles. |
| Syllabus | 1 | Converted from the revised Fall 2026 Word syllabus (images dropped). |
| Late policy | 1 | 10% per day, as in the syllabus. |

## Check after importing

1. **Modules:** 16 modules, in order, each item in the right header. Quizzes should be inside their modules (see the first limit below).
2. **Assignments:** 10 assignments of 100 points. Set the due dates (Day 10, 20, … 100 from the first class day), then confirm the submission types suit you.
3. **Syllabus tab:** it reads correctly and the schedule table survived the conversion.
4. **Late policy:** Grades → Settings shows 10% per day.
5. **A page from each module,** on a phone-width window: tables and code blocks should scroll or wrap rather than run off the screen.
6. **Publish** modules, pages, quizzes and assignments when you are satisfied. They arrive unpublished.

## Limits you should know about

- **Never imported into a live Canvas.** The XML follows the dialect of the old Canvas export, but only a real import shows what Canvas accepts or silently drops.
- **Quizzes in modules is the least certain part.** Their module items use the content type `Quizzes::Quiz`, written from knowledge of Canvas's exporter, not from the old export, which had no quizzes inside modules. If a quiz does not land in its module, add it by hand; the quiz itself is imported either way.
- **Chapter and example links 404 until the course repository is pushed.** The list of every link rewritten to the repository is in `canvas/package/repo-links.txt` after a build.
- **No dates anywhere.** That is deliberate; Canvas dates are the instructor's.

## Manual paste, if you prefer

Each fragment in `canvas/paste/` is a Canvas-safe HTML body: open the page or assignment in Canvas, switch the editor to HTML, and paste. `page-…` files are pages; `assignment-…` files are assignment descriptions. Set the assignment to 100 points and enable file upload and text entry yourself. The fragments carry no scripts, images or local file links.

The three fragments in this folder's top level (`01-module-1-…html` and so on) come from an earlier script, `scripts/build-canvas-pastes.cjs`. They are superseded by `canvas/paste/` and left in place.

## Related

- [`OLD-TO-NEW.md`](OLD-TO-NEW.md): what became of every old module, page, assignment and quiz.
- [`../modules/README.md`](../modules/README.md): the module index.
- [`../pantry/course-build-spec.md`](../pantry/course-build-spec.md): the file formats the builder reads.
