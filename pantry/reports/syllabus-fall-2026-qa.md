# Fall 2026 Word syllabus QA

Completed September 10, 2026, following the instructor's explicit DOCX edit request.

- Final file: `../../CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx`
- Final SHA-256: `64fb24154c9dfa285fee02bd01695cd495c2a8ffa96b02247a7b0f01ad614e9b`
- Original backup: `../backups/CSYE_7270_Virtual_Environments_and_Real-Time_3D.before-fall-2026.docx`
- Original SHA-256: `69302c6f256e569f2c138a9054ac91a331d2e503c9edffbd0b38231edfeed5cc`

## Preservation checks

The migration changes only `word/document.xml` and its hyperlink relationships. All other ZIP members, including styles, fonts, embedded fonts, numbering, theme, and settings, remain byte-identical. Section size and margins are unchanged. The red Calibri title, heading hierarchy, body styling, bullets, rules, and table widths follow the original.

The original Collaboration Policy through the final university resource sections, and the final course letter-grade policy, match their original XML after excluding only `keepNext` pagination flags. These flags prevent stranded headings and a split grade table; they do not change policy text or typography. The weekly schedule retains its five-column structure and row spacing, with left-aligned text and repeating headers for readability. Assignment quartile scores retain the source's 5 / 10 / 15 / 20 mapping.

The document contains no administrative “not supplied” placeholder, Spring 2026 date, former 5% penalty, weekly-assignment cadence, or Unreal Reels requirement. No exact assignment dates or new section number were invented. Both daily late-penalty mentions are 10%.

## Content checks

Confirmed Fall 2026; Walker/Godot/GDScript; Week 1 main-character change and playable-level extension; Week 2 prompted game art; Week 3 community Blender MCP; one chapter per module; incremental releases; both learning/build sequences; 100-point assignments every 10 days; 60 + 10 + 10 + 20 = 100; required Brutalist Godot explainers; Frictional; human/AI attribution; matching GitHub/Canvas revisions; film-as-code storage; and the clean clickable Professor Bear AI-policy video URL.

Brutalist explainers remain within the 60-point implementation/explanation category. Public YouTube publication and a second aspect ratio are not assumed. Planned Walker art assistants are not represented as installed commands.

## Render and package validation

- Bundled document Python and LibreOffice runtime; canonical `render_docx.py`.
- Original: 19 Letter pages. Revised: 21 Letter pages, all nonempty.
- Visually inspected pages 1–21 at original resolution. Pages 1–4 of the final render are byte-identical to the reviewed second render; pages 5–21 were inspected from the final render.
- Checked headings, table continuation, clipping, font fidelity, line wrapping, hyperlinks, and policy sections.
- ZIP CRC validation passed. Every referenced external hyperlink ID resolves; the AI-policy URL is exactly `https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz`.
- The installed final file matches the visually reviewed candidate's SHA-256.

Internal page renders are in `/tmp/csye7270-syllabus-PmRFnzey/final-review/`; they are QA intermediates, not additional deliverables. The edit script is `../../scripts/update_syllabus_docx.py`; rerun it only against the preserved original to produce a separate candidate.

This is an agent's mechanical/content/render QA record, not a human book-gate signature. The original Canvas IMSCC was not changed or imported.
