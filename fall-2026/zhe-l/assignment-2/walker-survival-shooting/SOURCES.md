# Sources

## Starting point
- Started from: an empty Godot 4 project, created by me in Godot 4.7.2-stable (Windows).

## Generative models
| Model | Developer | Version | Where it ran | License / terms | Used for |
|---|---|---|---|---|---|
| ChatGPT image generation | OpenAI | The exact image model version is not shown in the ChatGPT interface | ChatGPT, on a Plus plan provided through my student membership (I paid nothing) | OpenAI Terms of Use | Character reference drafts and the accepted turnaround |
| ChenkinNoob-XL | ChenkinNoob / ChenkinLab (fine-tune of NoobAI-XL, which builds on Illustrious-XL and SDXL) | V0.5 (`ChenkinNoob-XL-V0.5.safetensors`) | Locally, in ComfyUI on my own computer | fair-ai-public-license-1.0-sd with added terms, including a ban on commercial use. Fine for coursework; it would matter if the game were ever sold | Early character drafts (all rejected) |

## Tools
| Tool | Purpose | License |
|---|---|---|
| Claude Code (Claude Opus 5.5) | Organizing documents, translation, reading ComfyUI metadata, image conversion and thumbnails, asset log | Anthropic terms |
| ChatGPT (text) | Turning my design decisions into prompts, consistency rules, and production notes | OpenAI Terms of Use |
| ComfyUI | Local front end for the image model | GPL-3.0 |
| Pillow (Python) | Converting the accepted image to PNG and making rejection thumbnails | MIT-CMU (HPND) |
| Godot 4.7.2-stable | Engine | MIT |

## Collaborators / playtesters
None yet.

## Human / AI contributions
- **Me:** every design decision (direction, outfit, materials, holster position, modular equipment, which drafts to accept or reject), the storyboard, and the concept.
- **ChatGPT:** produced image drafts from my descriptions, helped turn my decisions into prompts and documentation, and drafted the English text of the character sheet and change brief from our conversation.
- **ChenkinNoob-XL (ComfyUI):** produced early drafts from prompts I ran locally.
- **Claude Code:** merged the ChatGPT material with my storyboard and concept, found the prompts and seeds in the ComfyUI output metadata, made the thumbnails, and wrote this log. Claude did not generate any image.

## Asset log
One row per generation that was kept or seriously considered. Rejected outputs are kept as thumbnails in `design/rejected/`. Storyboard images are exempt from this log (confirmed with the professor). ComfyUI output `ComfyUI_00010_` was a storyboard test, so it is not listed.

**About the ChatGPT rows:** the prompts were written inside a ChatGPT conversation and were not saved separately, so I cannot give the exact prompts or a seed. ChatGPT does not expose seeds. The ChatGPT images in this repository were saved from the copies I pasted into Claude Code (WebP, 1448 × 1086) and converted to PNG without other changes.

**About the ComfyUI rows:** the prompts, seeds, and settings were read back from the workflow that ComfyUI embeds in each output PNG. They are exact. The full prompt texts are in the appendix below.

| Asset ID | Model & version | Prompt / negative / seed / size / settings | Outcome + reason | Edits | Where used |
|---|---|---|---|---|---|
| CHAR-REF-00 (ComfyUI `00001`–`00009`, 2026-10-03) | ChenkinNoob-XL V0.5, local ComfyUI | Prompt P1 / negative N1 (appendix). Seeds 123456789, 997100846826920, 103334578739299, 309410215482627, 862291194226693, 7355608 (`00006`–`00009` are four identical re-runs of seed 7355608). 832 × 1216, 28 steps, CFG 5.5, euler_ancestral, normal scheduler | Rejected. Early single front-view exploration before the design existed (blonde or red hair, trousers or leggings instead of a skirt, gear built into the outfit). Some show the glossy, leggings-like lower body that led to design change 1 in `CHANGE-BRIEF.md`; my next prompts added "glossy fabric, shiny pants, latex, pvc …" to the negative prompt | None | `design/rejected/char-ref-00-comfyui-front-view-contact.png` |
| CHAR-REF-01 | ChatGPT image generation | Prompt not saved | Rejected. Plate carrier and pouches built into the character, a thigh holster, and decorative emblems. These led to design changes 3, 4, and 5 (holster to the right waist, no emblems, modular armor) | None | `design/rejected/char-ref-01-plate-carrier.png` |
| CHAR-REF-02 (ComfyUI `00011`–`00014`, 2026-10-06 to 10-07) | ChenkinNoob-XL V0.5, local ComfyUI | `00011`: prompt P2 / negative N2, seed 7355608. `00012`: prompt P3 / negative N3, seed 7355608. `00013` and `00014` (identical): P3 / N3, seed 5590904490. All 1664 × 1024, 28 steps, CFG 5.5, euler_ancestral, normal scheduler | Rejected; the results were far from what I wanted. `00011` came out with a 3D-render look rather than an anime design sheet, so I added "photorealistic, 3d render, cgi …" to the negative prompt (N3). `00012` and `00013` still built the plate carrier and thigh holsters into the character | None | `design/rejected/char-ref-02-comfyui-turnaround-contact.png` |
| CHAR-REF-03 | ChatGPT image generation | Prompt not saved | Rejected. From the back, the coat looks tucked into the skirt (design change 2); the holster sits on the belt outside the coat; cross emblems are still there | None | `design/rejected/char-ref-03-belt-outside-coat.png` |
| CHAR-REF-04 | ChatGPT image generation | Prompt not saved | Rejected / superseded. The coat construction is right, but there is no three-quarter view (design change 6) and there are still emblems and sheet decoration | None | `design/rejected/char-ref-04-no-three-quarter.png` |
| CHAR-TURN | ChatGPT image generation | Prompt not saved | Accepted. Front / three-quarter / side / back on one baseline, coat outside the skirt, holster hidden, matte materials, no emblems. Still open: no height bar yet; the X-shaped hair clip and choker are not decided (`CHARACTER-SHEET.md`, open decisions) | None (WebP → PNG conversion only) | `design/character/turnaround.png`; reference for every pose and the 3D model |

### Prompt appendix (ComfyUI)

**P1** (CHAR-REF-00)
```text
masterpiece, best quality, newest, high resolution, aesthetic, excellent, year 2026,
1girl, solo, full body, standing, neutral pose, front view, looking at viewer,
anime character design, tactical female character, modern tactical outfit,
black tactical vest, plate carrier, utility pouches, combat belt, fitted combat uniform,
layered clothing, gloves, knee pads, boots,
clean silhouette, clear clothing construction, functional gear,
plain light background, studio lighting, character concept art, game character design
```

**N1**
```text
nsfw, worst quality, old, early, low quality, lowres, signature, username, logo,
bad hands, mutated hands, extra fingers, missing fingers,
blurry, text, watermark, cropped, multiple people, background clutter
```

**P2** (CHAR-REF-02, `00011`)
```text
anime character design sheet, character turnaround, same girl, consistent appearance, full body, clean presentation, concept art, game character design, production reference sheet, plain light gray background, flat studio lighting, clear silhouette, practical design, matte materials, realistic fabric rendering, non-glossy surfaces, non-reflective clothing, subdued dark color palette, dark navy, charcoal black, cool gray accents

young anime female, calm and composed expression, feminine but short hairstyle, dark navy blue short bob haircut, chin-length bob, straight blunt bangs, hime cut, soft side locks framing the face, blue-gray eyes

school tactical outfit, dark pleated skirt, matte black opaque tights, 80D+ opaque tights, thick matte black tights, long sleeve school-style top, school uniform inspired inner layer, dark outer jacket or dark school outerwear, lightweight but thick plate carrier, compact but thick ballistic vest, substantial chest rig thickness, front magazine pouches on the chest, additional small side pouches on the vest, side utility pouches, side medical pouch, tactical belt, large rear-left utility pouch on the belt, dedicated tactical tablet pouch integrated into the large rear-left pouch area, right-side pistol magazine pouches on the belt, right thigh holster, black tactical ankle boots, practical tactical equipment, tactical straps and buckles, believable load-bearing gear, functional outfit
front view, side view, back view, three full-body views of the same character, character turnaround sheet, front side back layout, aligned standing poses, neutral standing pose, arms relaxed naturally, easy-to-read design sheet layout
```

**N2**
```text
glossy fabric, shiny fabric, reflective clothing, wet look, latex, pvc, leather leggings, leather pants, rubber, plastic-like material, metallic cloth, skintight clothing, bodysuit, catsuit, yoga pants, leggings, overly glossy tights, transparent tights, skin-tight pants, fetishwear, exaggerated shine, cheap AI look, overdesigned details, random accessories, inconsistent outfit, inconsistent face, inconsistent hair, extra pouches in random places, broken gear layout, unrealistic materials, bad anatomy, extra fingers, missing fingers, malformed hands, distorted legs, deformed skirt, bad boots, text, watermark, logo, cropped body, multiple different characters, messy background, dramatic cinematic lighting, strong rim light, overexposed highlights
```

**P3** (CHAR-REF-02, `00012`–`00014`)
```text
anime character design sheet, character turnaround, production reference sheet, concept art, 2D illustration, polished anime concept illustration, clean lineart, soft cel shading, matte rendering, muted dark palette, subdued colors, dark navy, charcoal black, cool gray accents, plain light gray background, flat studio lighting, clear silhouette, readable outfit design, orthographic presentation, outfit breakdown, design clarity, elegant layout, full body character sheet

same girl, consistent appearance, calm and composed expression, blue-gray eyes, feminine short hairstyle, dark navy blue short bob haircut, chin-length bob, straight blunt bangs, hime cut, soft side locks framing the face

school tactical outfit, dark pleated skirt, matte black opaque tights, 80D+ opaque tights, thick matte black tights, school-inspired long sleeve top, dark outerwear, compact but thick plate carrier, substantial ballistic vest thickness, front magazine pouches, additional side utility pouches, side medical pouch, tactical belt, large rear-left utility pouch, dedicated tactical tablet pouch, right-side pistol magazine pouches, right thigh holster, black tactical ankle boots, practical tactical equipment, believable load-bearing gear, functional outfit, dark school tactical aesthetic
front view, side view, back view, three full-body views of the same character, front side back layout, aligned standing poses, neutral standing pose, arms relaxed naturally, easy-to-read design sheet layout, character turnaround sheet
```

**N3**
```text
photorealistic, realistic, hyperrealistic, 3d render, cgi, game render, unreal engine, octane render, plastic skin, rubbery skin, mannequin, doll-like face, waxy shading, glossy fabric, shiny fabric, reflective tights, wet look, latex, pvc, leather leggings, overly glossy tights, transparent tights, skin-tight bodysuit, catsuit, fetishwear, overly rendered skin, strong specular highlights, harsh rim light, cinematic bloom, overly dramatic lighting, excessive realism, random extra accessories, broken gear layout, bad anatomy, extra fingers, missing fingers, distorted hands, malformed legs, deformed skirt, text, watermark, logo, messy background
```
