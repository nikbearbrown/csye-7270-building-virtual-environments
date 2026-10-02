# SOURCES — walker-houseghost-narasimha-v

## Started from

- An empty Godot 4 project (no template code).
- The world-inversion verb is carried forward as an idea from my Assignment 1 game, `walker-jumpman-narasimha-v` (my own work); no code, scenes, or assets are reused.
- Course context: `nikbearbrown/csye-7270-building-virtual-environments`, Assignment 2.

## Collaborators and tools

- **Claude Code (Fable 5):** code, documents, prompts, plans, and the hand-coded character concept sketch cards. Does not generate images or audio; its code-drawn sketches are labeled design artifacts and do not count toward the generative-asset requirement.
- **Me (Narasimha Reddy Valam):** all design decisions, rejections, edits, and playtests — the devil's-advocate exchanges are logged in `../FRICTIONAL.md`.

## Generative models (planned; rows added with first use)

| Model | Version / where run | License / terms | Used for |
|---|---|---|---|
| Gemini image generation | TBD at first use (model name + date, gemini.google.com) | Google Terms of Service (output usage per Google's generative-AI terms) | character + environment art |
| ChatGPT image generation | TBD at first use (model name + date, chatgpt.com) | OpenAI Terms of Use | character + environment art |
| Suno (free tier) | TBD at first use | Suno free-tier terms (non-commercial; attribution; 7 lifetime downloads) | music loop |
| SFX tool (ElevenLabs free tier or local Stable Audio Open) | TBD | TBD at first use | four event sounds |

Neither Gemini nor ChatGPT exposes seeds; reproducibility is kept as: exact prompt text, model and version, date, and screenshots of accepted and rejected outputs (rejects as thumbnails).

## Asset log

One row per generation kept or seriously considered. Neither Gemini nor ChatGPT exposes seeds, so the prompt text, model, and date are the reproduction record. Full-size keepers go in `design/character/`; rejects are kept as small screenshots in `design/character/rejects/`.

| Asset ID | Model + version | Prompt + settings | Outcome | Edits | Where used |
|---|---|---|---|---|---|
| CHAR-REF-01 | Gemini (Flash image generation), gemini.google.com, 2026-10-02 | "A character reference sheet for a 2D video game, hand-painted storybook illustration style… boy about ten… school picture day: collared off-white shirt buttoned one button wrong, small dark red clip-on tie pulled loose, grey shorts with grass stains… four views… flat solid magenta background (#FF00FF)" — four-view turnaround, School Picture Boy design | **Rejected** — technically competent (consistent four views, clean magenta) but the character is warm and cute, with no unease whatsoever; it reads as a children's-book boy, not the main character of a horror game. Also too tidy to carry any story. | None | `design/character/rejects/CHAR-REF-01-gemini-storybook-schoolboy.jpg` |
| CHAR-REF-01b | Gemini (Flash image generation), gemini.google.com, 2026-10-02 | Follow-up on CHAR-REF-01, my instruction verbatim: "i want more details and realistic" | **Rejected** — "realistic" was read as photoreal 3D: a CGI/stock-photo child whose facial detail turns to mud at 96 px (sheet rule: "detail that disappears at game size is not detail"). The flat magenta also degraded into a lit pink studio backdrop with floor shadows, which would halo during matting. Lesson recorded in FRICTIONAL: for a 2D game sprite, ask for readable shapes, not realism. | None | Screenshot only (not downloaded) |
| CHAR-REF-02 | Gemini (Flash image generation), gemini.google.com, 2026-10-02 | Follow-up on CHAR-REF-01b: "Using this exact character… make a version of him as a faded old school photograph. Desaturated sepia and cold grey tones, soft paper grain… legs fade away into thin pale mist below the knees. No shadow beneath him." | **Rejected** — inherited the photoreal problem; mist read as stage smoke rather than dissolution; tie stayed loose when the GHOST state specifies it straight; grass stains lost. Judged against CHARACTER-SHEET two-state rule. | None | Screenshot only (not downloaded) |
| CHAR-REF-03 | Gemini (Flash image generation), gemini.google.com, 2026-10-02 | Rewritten for style: "2D hand-drawn horror video game. Stylized illustration with flat colours, bold simple shapes, clean readable silhouette, limited muted palette. Not photorealistic, not 3D, not anime… boy about nine… hand-knitted dark green sweater slightly too big, one sleeve unravelling… bare feet… four views… pure flat magenta #FF00FF" | **Rejected (style accepted, character rejected)** — art style, flat magenta, and four-view consistency were all correct and became the production style. Character failed the brief: read as a calm 14-year-old, neutral face, tidy sweater, no unease. Diagnosis: horror was left to the model instead of being specified in the design. | None | `design/character/rejects/CHAR-REF-03-gemini-flat-style-too-old.jpg` — style basis for CHAR-REF-04 |
| CHAR-REF-04 | ChatGPT image generation, chatgpt.com, 2026-10-02 | Same style block plus explicit horror design: "child proportions: large head roughly one third of total height… pale grey-white skin, dark circles, eyes slightly too large and too dark with very small pupils… straight black hair hanging flat over the forehead… In every view, including the side and back views, his head is turned to face the viewer." | **Candidate, revision requested** — eyes, ragged oversized sweater, four-view consistency and flat magenta all good; ChatGPT held the design better than Gemini. Still reads 12–13 rather than 8 (legs too long, head too small), and the clothes are tattered without being evidence of anything. | Pending | `design/character/rejects/CHAR-REF-04-chatgpt-ragged-sweater-candidate.jpg` — superseded by CHAR-REF-05 |
| CHAR-REF-05 | ChatGPT image generation, chatgpt.com, 2026-10-02 | Image-to-image on CHAR-REF-04: keep face/eyes/hair/style/views/background; change (1) proportions to a clear eight-year-old — head ≈1/3 height, shorter legs; (2) clothing — sweater soaked dark and heavy from the chest down with a visible wet line, badly unravelling hem and cuffs, child's dungaree overall with one strap unbuckled, trousers caked with dry grey dust at the knees, bare dusty feet. No blood or gore. | **Candidate, revision requested** — all three evidence details landed (wet line across the chest, grey dust on knees and soles, badly unravelling cuffs) and child proportions improved. Four views consistent, magenta flat. Judged still short on dread: hair and face are too tidy for the design, and the dungarees read as costume rather than evidence at small size. | Pending | Revision CHAR-REF-06 |
