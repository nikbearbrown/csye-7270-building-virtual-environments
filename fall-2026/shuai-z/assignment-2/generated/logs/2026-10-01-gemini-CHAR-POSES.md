# Generation log: Rudy's default-form poses, round 1 (Gemini, 2026-10-01)

I exported this chat from the Gemini app with the Voyager browser extension on 2026-10-01 at 17:35. The unmodified export is [2026-10-01-gemini-CHAR-POSES.export.md](2026-10-01-gemini-CHAR-POSES.export.md). I downloaded each full-size output from the chat afterwards (17:38–17:41) and numbered them 1–9 in turn order; those downloads are the files judged here, not the export's preview images.

- **Chat:** Gemini app, chat `87c157d4397cf98b` (a new chat, not the CHAR-REF chat), private to my account
- **Model and version:** the app reports image generation as Nano Banana, without an exact version. The chat model was Gemini 3.8 Flash
- **Account:** my personal Google account
- **Seed:** not available; the Gemini app does not expose one
- **Attached image, every turn:** CHAR-REF-07. The export's copy of the attachment is a 1024×571 preview; it differs from a downscaled `generated/accepted/CHAR-REF-07.jpg` by a mean of 1.7 levels (against 4.9 for CHAR-REF-06), so it is CHAR-REF-07
- **Requested size:** "Square image." Every download is a 2048×2048 JPEG
- **Times:** the exact time of each turn is TO FILL from Gemini Apps Activity

## Prompts

Every turn is the CHAR-REF-07 pose template from `design/generation-prompts.md` (prompts v2) with `[POSE]` replaced by that pose's line from the table, pasted unchanged. Claude checked all nine prompts in the export against the template character by character; all nine match. The template:

```text
Use the attached image as the exact character reference: draw the same boy, with the same proportions, face, center-parted light-brown hair with its strands and cowlick, green eyes, slate-grey robe with the large hood down and the thin pale trim along the hood edge, the front opening, the cuffs and the hem, brown belt and boots, colors and outline. Draw only one figure: the boy in side view facing right, [POSE]. Keep the same cel-shaded style, flat neutral lighting and the same plain, solid steel-blue background (#4F7CAA). Change nothing except the pose. Square image.
```

| Turn | ID | `[POSE]` |
|---|---|---|
| 1 | CHAR-IDLE-01 | standing relaxed, with his weight slightly forward and a cheerful look |
| 2 | CHAR-RUN-A-01 | running, contact pose: the front foot just touching the ground, the back leg stretched out behind him, body leaning forward, arms swinging opposite to the legs |
| 3 | CHAR-RUN-B-01 | running, passing pose: the supporting leg straight under his body, the other knee bent and lifted as it passes, body leaning forward |
| 4 | CHAR-RISE-01 | jumping upward: knees tucked, arms raised, hair and robe pulled downward by the upward motion |
| 5 | CHAR-FALL-01 | falling: legs stretched down, ready to land, arms out for balance, hair and robe lifted by the fall |
| 6 | CHAR-HURT-01 | hurt: recoiling from a hit coming from the right, leaning back, eyes squeezed shut, arms flung out |
| 7 | CHAR-DEFEAT-01 | defeated: sitting on the ground with his legs out, dizzy, eyes shut, a small sad smile |
| 8 | CHAR-RESPAWN-01 | getting back up: one knee on the ground, pushing himself up with a determined smile |
| 9 | CHAR-CELEBRATE-01 | celebrating: a small hop with one fist raised high and a big happy smile |

## What came back (Claude's first look; my decisions are in the last table)

Identity holds in all nine: the hair, cowlick, green eyes, the robe with its pale trim, the belt, the boots and the outline match CHAR-REF-07. Each check (`generated/checks/ID-check.png`) shows the frame at 160 px next to the blockout pose and the reference, on the wheat with the in-engine outline, in grayscale, and as a silhouette.

| ID | Against the prompt and the sheet |
|---|---|
| CHAR-IDLE-01 | Matches: side view, relaxed, a slight smile. At 160 px the chin and head-top lines fall where the reference's do |
| CHAR-RUN-A-01 | Matches: front foot reaching to the ground, back leg stretched out, forward lean, arms opposite to the legs |
| CHAR-RUN-B-01 | **Partly.** The stride is shorter and the back foot is raised, but it is not a passing pose: no leg is straight under the body and no knee is lifted forward. Next to RUN-A it may read as a two-frame run anyway; that needs testing in the engine |
| CHAR-RISE-01 | Mostly: knees tucked, upward. Only one arm is raised (a fist), so it is close to the celebrate pose, and the hair and robe are not visibly pulled down |
| CHAR-FALL-01 | **Partly.** Legs down, one arm out, hair and hood lifted. The robe opens from the belt down and shows the trousers, which is the split hem I rejected in CHAR-REF-06 |
| CHAR-HURT-01 | **Does not match.** Eyes squeezed shut and arms flung out, but he leans forward, head ahead of his feet, toward the hit. It reads as a dive, not a recoil |
| CHAR-DEFEAT-01 | Matches: sitting, legs out, eyes shut, a small smile. It has a soft cast shadow under him, which the sheet forbids; the matte has to remove it |
| CHAR-RESPAWN-01 | Matches: one knee down, a hand on the ground, a determined smile |
| CHAR-CELEBRATE-01 | **Partly.** Fist raised, big smile, feet off the ground, but he is drawn in a three-quarter view toward the viewer, not in side view like the other frames |

Two things that affect every frame:

- **Scale differs between images.** The standing figure in CHAR-IDLE-01 is 1902 px tall; the seated one in CHAR-DEFEAT-01 is 1756 px, so Gemini zoomed in on the sitting pose. The check tool scales each figure to 160 px tall, which is right for standing poses but blows up the crouched and seated ones (RISE, DEFEAT, RESPAWN have oversized heads in their 160 px rows). The game frames have to be scaled by head size instead, so that Rudy's head is the same size in every frame.
- **Background:** Gemini drew it as about `#526F8F`, not the requested `#4F7CAA`, the same as in CHAR-REF-07 (`#4F6D8F`). The color key still separates it cleanly.

## Where each output is kept

| ID | Download | Size | SHA-256 (first 12) | Kept in git as |
|---|---|---|---|---|
| CHAR-IDLE-01 | `1.jpeg` | 2048×2048 | fa16eb76210e | accepted: `generated/accepted/CHAR-IDLE-01.jpg` |
| CHAR-RUN-A-01 | `2.jpeg` | 2048×2048 | cb37962297ee | accepted: `generated/accepted/CHAR-RUN-A-01.jpg` |
| CHAR-RUN-B-01 | `3.jpeg` | 2048×2048 | 76998e5aeb9f | rejected, to be redone: thumbnail in `generated/rejected/CHAR-HURT-RUN-B-01.png` |
| CHAR-RISE-01 | `4.jpeg` | 2048×2048 | 714dfc116eab | accepted: `generated/accepted/CHAR-RISE-01.jpg` |
| CHAR-FALL-01 | `5.jpeg` | 2048×2048 | 098fff47a2ba | accepted: `generated/accepted/CHAR-FALL-01.jpg` |
| CHAR-HURT-01 | `6.jpeg` | 2048×2048 | b847e4ad935a | rejected, to be redone: thumbnail in `generated/rejected/CHAR-HURT-RUN-B-01.png` |
| CHAR-DEFEAT-01 | `7.jpeg` | 2048×2048 | efe82e639653 | accepted: `generated/accepted/CHAR-DEFEAT-01.jpg` |
| CHAR-RESPAWN-01 | `8.jpeg` | 2048×2048 | 8e39a3150bc4 | accepted: `generated/accepted/CHAR-RESPAWN-01.jpg` |
| CHAR-CELEBRATE-01 | `9.jpeg` | 2048×2048 | 1e5a4df691ad | accepted: `generated/accepted/CHAR-CELEBRATE-01.jpg` |

The export's own image files (`assets/img-*.jpg`) are previews and are not kept; three of the nine outputs (turns 1, 7 and 8) appear in the export only as Gemini links.
