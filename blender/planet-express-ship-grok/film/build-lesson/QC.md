# QC: Build the Planet Express Ship in Blender, from Images

Checked 2026-10-21 on the film source (no film rendered).

| Check | Result |
|---|---|
| Every image in the beat sheet exists in the published gallery | pass |
| Side, top, front and rear views all used | pass |
| Brutalist opening, recap, Your Turn, credit card, spoken outro present | pass |
| Outro speaks the exact title then "At Nik Bear Brown", 1.0 s silent tail, no music (OUTRO-LOCK) | pass |
| Narrator named only as the Liam voice; no voice settings in any file | pass |
| No subtitles, captions or .srt | pass |
| Every claim maps to an image and region (SHOTLIST.md) | pass |
| Stats labelled as reported by the README | pass |
| Human verdict shown as pending where it is pending | pass |

**Not performed (film-stage checks):** narration audio generation and measurement, frame inspection, crop accuracy, label legibility, listening for speech-to-image sync. These need the rendered film, which Professor Bear makes with his own tools. The 19 beat durations are word-count estimates (about 5.5 min total); the measured narration replaces them.

**Lesson checks:** no prompt or code was run in a fresh Blender scene for this lesson, so every checkpoint is labelled *proposed*, and the lesson is not called tested or learner-tested. The starter prompt needs no hidden local paths or original files: it names only published gallery images.
