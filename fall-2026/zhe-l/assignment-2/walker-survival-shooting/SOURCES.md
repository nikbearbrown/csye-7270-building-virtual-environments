# Sources

## Starting point
- Started from: an empty Godot 4 project, created by me in Godot 4.7.2-stable (Windows).

## Generative models
| Model | Developer | Version | Where it ran | License / terms | Used for |
|---|---|---|---|---|---|
| ChatGPT image generation | OpenAI | The exact image model version is not shown in the ChatGPT interface | ChatGPT, on a Plus plan provided through my student membership (I paid nothing) | OpenAI Terms of Use | Character reference drafts, the accepted turnaround, the extra character views (2026-10-09), and the tablet reference images (2026-10-08) |
| ChenkinNoob-XL | ChenkinNoob / ChenkinLab (fine-tune of NoobAI-XL, which builds on Illustrious-XL and SDXL) | V0.5 (`ChenkinNoob-XL-V0.5.safetensors`) | Locally, in ComfyUI on my own computer | fair-ai-public-license-1.0-sd with added terms, including a ban on commercial use. Fine for coursework; it would matter if the game were ever sold | Early character drafts (all rejected) |
| Claude Code | Anthropic | Claude Opus 5.5 (`claude-opus-5-5`) | Claude Code desktop app; writes Blender Python through the Blender MCP and Godot scene files directly | Anthropic terms | Builds 3D assets in code from basic shapes: the test chair and the subway base greybox (the professor confirmed these count as generated assets) |
| Stable Audio 3 Small SFX | Stability AI (UK) | `stable_audio_3_small_sfx.safetensors` (model card base model: `stabilityai/stable-audio-3-small-sfx-base`), with the text encoder `t5gemma_b_b_ul2.safetensors` | Locally, in ComfyUI 0.38.0 on my own computer | Stability AI Community License (free for research and non-commercial use; commercial use needs registration and is limited to under US $1M annual revenue). The bundled T5Gemma text encoder is under the Gemma Terms of Use | Terminal UI sound effects (SFX-TERMINAL-*) |

## Tools
| Tool | Purpose | License |
|---|---|---|
| Claude Code (Claude Opus 5.5) | Organizing documents, translation, reading ComfyUI metadata, image conversion and thumbnails, asset log | Anthropic terms |
| ChatGPT (text) | Turning my design decisions into prompts, consistency rules, and production notes; for the sound effects, explaining sound-design styles and terms, and converting the prompts I wrote into phrasing the local audio model understands more easily | OpenAI Terms of Use |
| ComfyUI 0.38.0 | Local front end for the image model and the audio model | GPL-3.0 |
| FFmpeg / ffprobe | Used by Claude to read the workflow ComfyUI embeds in each output FLAC (prompts, seeds, settings) | LGPL / GPL |
| Pillow (Python) | Converting the accepted image to PNG and making rejection thumbnails | MIT-CMU (HPND) |
| Godot 4.7.2-stable | Engine | MIT |

## Collaborators / playtesters
None yet.

## Human / AI contributions
- **Me:** every design decision (direction, outfit, materials, holster position, modular equipment, which drafts to accept or reject), the storyboard, and the concept.
- **ChatGPT:** produced image drafts from my descriptions, helped turn my decisions into prompts and documentation, and drafted the English text of the character sheet and change brief from our conversation.
- **ChenkinNoob-XL (ComfyUI):** produced early drafts from prompts I ran locally.
- **Sound effects (2026-10-09):** I built and operated the local Stable Audio 3 Small SFX workflow in ComfyUI, entered and adjusted the prompts and generation settings, generated multiple candidates, listened to the outputs, and made every accept/reject decision. I decided the sound language of the terminal: short electronic tones with radio-static / squelch texture, a lower, rounder cursor tone, and a short, higher error beep. I wrote the prompts; ChatGPT converted my wording into phrasing the local model understands more easily, and I used it to learn the relevant sound-design styles and terms (for example radio squelch, filtered radio static, RF interference). Stable Audio 3 Small SFX generated all the audio.
- **Claude Code (sound effects):** read the exact prompts, seeds, and settings back from the metadata of every ComfyUI audio output, matched the accepted files to their original outputs by checksum, and wrote the SFX rows of this log. Claude did not generate or edit any audio.
- **Claude Code:** merged the ChatGPT material with my storyboard and concept, found the prompts and seeds in the ComfyUI output metadata, made the thumbnails, and wrote this log. Claude did not generate any image; Claude did build 3D assets in code (see the ENV rows in the asset log).

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
| CHAR-TURN | ChatGPT image generation | Prompt not saved | Accepted. Front / three-quarter / side / back on one baseline, coat outside the skirt, holster hidden, matte materials, no emblems. Still open: no height bar yet. The X-shaped hair clip stays; the choker does not fit the design (`CHARACTER-SHEET.md`, revision history) | None to the image (WebP → PNG conversion only). The choker will be removed when the 3D model is built | `design/character/turnaround.png`; reference for every pose and the 3D model |
| TABLET-REF-01 to TABLET-REF-04 (2026-10-08) | ChatGPT image generation | Prompt not saved | Accepted as design references for the rugged military tablet (PROP-TABLET) | None to the images | `design/pad/tablet-ref-01.png` to `tablet-ref-04.png` (renamed from the ChatGPT download names, in time order: 20:36:53, 20:36:54, 20:36:55, 20:38:37); reference for PROP-TABLET |
| CHAR-VIEW-01 (2026-10-09) | ChatGPT image generation | Prompt not saved | Accepted as references: separate full-body views of the main character (front, back, left side, right side, three-quarter), 793 × 1983 | None to the images | `design/character/character-front.png`, `character-back.png`, `character-side.png`, `character-side-right.png`, `character-three-quarter.png`; reference for the 3D model |
| CHAR-VIEW-APOSE-01 (2026-10-09) | ChatGPT image generation | Prompt not saved | Accepted as references: A-pose versions of the front, back, left side, and right side views, 948 × 1659 | None to the images | `design/character/character-front-Apose.png`, `character-back-Apose.png`, `character-side-Apose.png`, `character-side-right-Apose.png`; reference for the 3D model |
| ENV-SEAT-TEST-01 (`test_chair.glb`, 2026-10-07) | Claude Code (Claude Opus 5.5) + Blender via the Blender MCP | Prompt: my request in Claude Code to test the Blender workflow with a simple low-poly chair (not saved verbatim). Built by Claude in Blender Python from basic shapes, exported as GLB. About 0.44 × 0.9 × 0.42 m | Kept for testing. It shows the Blender → Godot route works; the final start-menu seat is still undecided (chair, sofa, or something else) | None | `godot/assets/furniture/test_chair.glb`; placed against the back wall in `base.tscn` (panels 1–2) |
| ENV-BASE-01 (`base.tscn`, 2026-10-08) | Claude Code (Claude Opus 5.5), writing the Godot scene file | Prompt (my words, 2026-10-08, typed in Chinese; English translation): "Never mind, you build it for me. Remember to write the changes into the md files; so far you have already generated a bench with AI. Generate the terrain too. I have already done a little, so you should only need to do some more" (earlier I had asked for four walls, a ceiling, a floor, and a staircase). Godot CSG: room 16 × 10 m, interior height 3 m; 6 steps of 0.2 m × 0.3 m up to a 1.2 m platform; invisible sloped collision box over the steps; two OmniLight3D (color 0.78/0.86/1.0, energy 1.5, range 8); dark cool ambient light | Accepted as the greybox. I built the floor and the left and right walls myself; Claude added the front and back walls, the ceiling, the stairs, the lights, and a preview camera. A headless raycast confirmed the ramp matches the step edges | None yet | `godot/base.tscn` (panels 1–4) |

| SFX-TERMINAL-POWER-ON-V01 (ComfyUI audio `00001`–`00015`, 2026-10-09) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A1 / negative A1 (audio appendix). 8 steps, CFG 1.0, lcm sampler, simple scheduler. 5.0 s: seed 5590904490 (`00001` batch 1; `00002`–`00005` batch 2), seed 77853657847881 (`00006`–`00007`). 1.0 s, batch 2: seeds 259122829178303, 509266827886360, 927952609724058, 757154208632985 (`00008`–`00015`) | Rejected. Too sharp and explosive, like an electronic transient; it lacked the clear single confirmation beep and the military communications texture I wanted | None | Not used |
| SFX-TERMINAL-POWER-ON-V02 (`00016`–`00033`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A2 / negative A2 (`00016`–`00031`); A3 = the same positive with an empty negative (`00032`–`00033`). 12 steps, CFG 1.0, lcm, simple, batch 2. 1.0 s: seeds 235893070620272, 577646660658064. 1.5 s: seeds 996386811226278, 944620719990344, 235530507217038, 571837257118318, 208013081214778, 1145141919810; A3 seed 651287091042509. `00028`–`00033` were saved as MP3 (kept out of git) | Rejected. These were rerolls (new seeds or slightly different length settings); none of them gave a result I was satisfied with. After this I changed the design to one clear single beep layered with short radio static | None | Not used |
| SFX-TERMINAL-POWER-ON-V03 (`00034`–`00043`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A4 / negative A4. 12 steps, CFG 1.0, lcm, simple, batch 2. Seed 488893752963761 at 1.5 s (`00034`–`00035`, MP3); seed 1145141919810 at 1.5 s, 2.1 s, 2.5 s, 2.3 s (`00036`–`00043`) | **Accepted: `00042`** (seed 1145141919810, 2.3 s). The clear single beep combined with short radio-static / squelch texture matched the rugged military-terminal sound I wanted. The other outputs in this group were rerolls: I changed the seed or the length only to get new variations. The prompt fixes the sound at about 1 second, so the rest of each file is silence and the length setting does not change the sound itself | None. `00042` was copied and renamed; it is byte-identical to the ComfyUI output (checked by MD5). Not yet converted to OGG | `design/sfx_sound/sfx_power_on.flac`; planned for the game as OGG |
| SFX-TERMINAL-POWER-OFF-V01 (`00044`–`00045`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A5 / negative A5 (the power-on prompt plus a descending shutdown tone, a relay-like cutoff click, and a fading noise tail; "rising startup tone" and "positive confirmation chime" added to the negative). Seed 1145141919810, 2.3 s, 12 steps, CFG 1.0, lcm, simple, batch 2 | **Accepted: `00044`**. It stays in the same sound family as power-on. Nothing special about the choice: I was satisfied with it when I listened. `00045` was not chosen | None (byte-identical copy). Not yet converted to OGG | `design/sfx_sound/sfx_power_off.flac`; planned for the game as OGG |
| SFX-TERMINAL-CURSOR-V01 (`00046`–`00051`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A6 / negative A6 (a single beep around 1 kHz). 1.0 s, 12 steps, CFG 1.0, lcm, simple, batch 2. Seeds 1145141919810, 1145141919811, 942603389476194 | Rejected. Too sharp. I changed the cursor toward a lower, rounder "doo" tone | None | Not used |
| SFX-TERMINAL-CURSOR-V02 (`00052`–`00069`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A7 (main tone 500–600 Hz, `00052`–`00067`) and A8 (300–400 Hz, `00068`–`00069`); negative A7 for both. 12 steps, CFG 1.0, lcm, simple, batch 2. A7: seed 305189683949811 at 1.0 s; 738136524913167 at 1.1 s; 1145141919810 at 1.1, 1.5, 2.0, 1.0 s; 7355608 at 1.0 s (twice). A8: seed 7355608 at 1.0 s | Rejected. These were rerolls (new seeds or slightly different length settings); none of them gave a result I was satisfied with. I lowered the target frequency step by step | None | Not used |
| SFX-TERMINAL-CURSOR-V03 (`00070`–`00073`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A9 (main tone 100–200 Hz, `00070`–`00071`) and A10 (700–800 Hz, `00072`–`00073`); negative A7. Seed 7355608, 1.0 s, 12 steps, CFG 1.0, lcm, simple, batch 2 | **Accepted: `00070`** (A9). A low, short, rounded navigation tone. A10 (700–800 Hz) did not sound much different, so I did not use it | None (byte-identical copy). Not yet converted to OGG | `design/sfx_sound/sfx_botton_press.flac`; planned for the game as OGG |
| SFX-TERMINAL-ERROR-V01 (`00074`–`00075`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A11 / negative A11 (a 400–500 Hz buzzer; the prompt included "controlled amplitude flutter"). Seed 7355608, 1.0 s, 12 steps, CFG 1.0, lcm, simple, batch 2 | Rejected. Multiple repeated / tremolo-like tones instead of one sound | None | Not used |
| SFX-TERMINAL-ERROR-V02 (`00076`–`00077`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A12 / negative A12 (one steady unmodulated tone, 400–500 Hz; tremolo, flutter, and pulsing added to the negative). Seed 7355608, 1.0 s, same settings | Rejected. It still had modulation and was too low-pitched | None | Not used |
| SFX-TERMINAL-ERROR-V03 (`00078`–`00081`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A13 / negative A13 (one steady tone at 1100–1300 Hz with radio static only before and after the tone). Seed 7355608, 1.4 s (`00078`–`00079`) and 1.0 s (`00080`–`00081`), same settings | Rejected. These were rerolls (new seeds or slightly different length settings); none of them gave a result I was satisfied with. | None | Not used |
| SFX-TERMINAL-ERROR-V04 (`00082`–`00101`) | Stable Audio 3 Small SFX, local ComfyUI | Prompt A14 / negative A14 (a short "di" beep at 1500–1800 Hz, `00082`–`00099`); A15 = A14 without the radio-static lines (`00100`–`00101`, negative A14). 12 steps, CFG 1.0, lcm, simple, batch 2. A14: seed 7355608 at 1.0 s and 2.0 s; 285761072807263, 904440903178430, 862408537462408 at 2.0 s; 1006023025527340 and 1145141919810 at 2.3 s; 1145141919810 at 1.0 s. A15: seed 1145141919810, 1.0 s | Rejected. These were rerolls (new seeds or slightly different length settings); none of them gave a result I was satisfied with. | None | Not used |
| SFX-TERMINAL-ERROR-V05 (`00102`–`00127`) | Stable Audio 3 Small SFX, local ComfyUI | Shortened prompts A16–A22 (most descriptors removed). A16: negative A14; A17, A18: empty negative; A19–A21: a negative prompt I typed in Chinese (meaning "no multiple sounds, generate only one sound"), in A20 also put in the positive; A22: "only one "doo" sound". 12 steps, CFG 1.0, lcm, simple, batch 2. Seeds: 1145141919810 at 1.0 s (`00102`–`00109`); 587941498300204, 215261150479133 at 1.0 s; 88724730495980, 678896230871315, 257384963511168, 448773839510089, 470401036591599, 798649151585538, 738089384662078 at 1.5 s | Rejected. These were rerolls (new seeds or slightly different length settings); none of them gave a result I was satisfied with. | None | Not used |
| SFX-TERMINAL-ERROR-V06 (`00128`–`00155`) | Stable Audio 3 Small SFX, local ComfyUI | Short prompts A23–A29: "only one "di" sound", "sound should be sharp" (written "shape" in A23–A28), with negative "too much noise" / "too many noise" / "not too many noise" or empty; A28–A29 drop "rugged". 12 steps, CFG 1.0, lcm, simple, batch 2. Seeds: 466319066964929, 279049298745973, 970110798572635 at 1.5 s; 18306444387625 at 1.0 s; 834953178313426 at 1.5 s; 410128869009758 at 1.5 s and 1.0 s; 912311214866240 at 1.0 s; 907642672243603 at 1.0, 1.6, 1.2 s | Rejected. These were rerolls (new seeds or slightly different length settings); none of them gave a result I was satisfied with. | None | Not used |
| SFX-TERMINAL-ERROR-V07 (`00156`–`00161`) | Stable Audio 3 Small SFX, local ComfyUI | Prompts A30 ("tones go high to low") and A31 ("frequency go high to low"), negative "too much noise". Seed 907642672243603, 1.2 s, 12 steps, CFG 1.0, lcm, simple, batch 2 | Current direction, not final: a single, short, higher-pitched "di" with no modulation. No output chosen yet | None | Not used yet |

**About the SFX rows:** the prompts, seeds, and settings were read back from the workflow that ComfyUI embeds in each output FLAC/MP3, so they are exact. Each run used batch size 2 and saved two files, which share one seed. Many runs inside one row are rerolls: I kept the prompt and changed the seed, or changed the length setting slightly, to get new variations. Because the prompt states the sound's duration, the extra length is silence at the end of the file. The full prompt texts are in the audio appendix at the end of this file. I listened to every output; the rejected audio stays in my local ComfyUI output folder and is not uploaded (audio has no thumbnail).
**Reproducibility check:** when I heard a result I was satisfied with, I ran the same prompt and seed again to check that the model gives the same output. The decoded audio is identical in these re-runs (checked by Claude with an MD5 of the decoded audio; the file bytes differ only in the embedded metadata): `00002`/`00004`, `00003`/`00005`, `00064`/`00066`, `00065`/`00067`, `00084`/`00086`, `00085`/`00087`, `00106`/`00108`, `00107`/`00109`, `00144`/`00146`, `00145`/`00147`, `00156`/`00160`, `00157`/`00161`.
**Negative prompts had no effect (found by Claude afterwards):** outputs that differ only in the negative prompt came out identical: `00102` (A16, negative A14) = `00104` (A17, empty negative), and `00138` = `00140` = `00142` (A25, A26, A27: "not too many noise" / "too many noise" / "too much noise"). Every audio run used CFG 1.0, and at CFG 1.0 ComfyUI's sampler does not use the negative prompt, so none of the audio negative prompts in this log changed the output. Only the positive prompt, seed, and length did.

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

### Audio prompt appendix (Stable Audio 3 Small SFX, ComfyUI)
A3 has the same positive prompt as A2. A19–A21 contain a negative prompt I typed in Chinese; it is given below in English translation.

**A1** — positive
```text
short tactical electronic device power-on sound effect,
rugged military handheld computer booting up,
two brief digital confirmation beeps followed by a rising electronic activation tone,
dry narrow-band synthesized sound,
subtle low-frequency electrical pulse,
slightly gritty retro-digital texture,
compact utilitarian interface sound,
precise and restrained,
late 20th century military electronics aesthetic,
duration about 1 second,
single isolated sound effect
```
Negative
```text
music, song, melody, rhythm, beat, drums, bassline,
ambient music, background music,
cinematic soundtrack, trailer sound,
orchestral, musical chord,
long drone, sustained tone,
huge sci-fi whoosh, laser gun,
magic sound, fantasy sound,
smartphone notification,
cute UI sound, arcade sound,
reverb, echo, ambience,
speech, voice, vocals,
multiple repeated sounds,
long sound effect
```

**A2** — positive
```text
short military handheld terminal power-on sound effect,
compact electronic startup sequence,
soft low electronic pulse followed by two quiet digital initialization tones,
gentle rising system activation sound,
warm mid-frequency electronic body,
subtle low-frequency hum,
restrained retro-digital texture,
small rugged computer speaker,
controlled and functional,
soft attack,
smooth transient,
short decay,
no sudden impact,
no harsh high frequencies,
single isolated sound effect,
duration about 1 second
```
Negative
```text
harsh, sharp, piercing, screeching, shrill,
high-pitched alarm, loud beep,
explosive transient, impact sound,
electrical spark, glitch burst,
distortion burst, clipping,
laser, weapon sound,
siren, warning alarm,
cinematic boom, trailer sound,
music, melody, rhythm, beat,
reverb, echo,
voice, speech, vocals
```

**A3** — positive
```text
short military handheld terminal power-on sound effect,
compact electronic startup sequence,
soft low electronic pulse followed by two quiet digital initialization tones,
gentle rising system activation sound,
warm mid-frequency electronic body,
subtle low-frequency hum,
restrained retro-digital texture,
small rugged computer speaker,
controlled and functional,
soft attack,
smooth transient,
short decay,
no sudden impact,
no harsh high frequencies,
single isolated sound effect,
duration about 1 second
```
Negative: (empty)

**A4** — positive
```text
short rugged military handheld terminal power-on sound effect,
one clear electronic confirmation beep,
distinct single mid-pitched beep around 900 Hz,
the beep is layered with a brief filtered radio static burst,
subtle radio squelch,
short RF interference texture,
tiny digital chatter and electrical noise,
gritty communications equipment texture,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,
dry and compact,
utilitarian late-20th-century military electronics,
brief electronic startup tail after the beep,
controlled and restrained,
single isolated sound effect,
duration about 1 second
```
Negative
```text
piercing beep, shrill tone, very high pitch,
screech, harsh alarm, siren,
explosive transient, impact,
laser, sci-fi weapon,
clean smartphone notification,
cute UI sound, arcade sound,
pure sine wave,
smooth pristine digital tone,
music, melody, chord, rhythm, beat,
cinematic boom, cinematic whoosh,
long drone, long sustained tone,
heavy distortion, clipping,
reverb, echo,
voice, speech, vocals
```

**A5** — positive
```text
short rugged military handheld terminal power-off sound effect,
one clear electronic confirmation beep,
distinct single mid-pitched beep around 850 Hz,
the beep has a subtle downward pitch movement,
layered with a brief filtered military radio static burst,
short radio squelch,
subtle RF interference texture,
tiny digital chatter and electrical noise,
gritty communications equipment texture,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

after the beep, a short descending electronic shutdown tone,
the sound loses energy and falls downward,
brief power-disconnect sensation,
tiny relay-like cutoff click near the end,
short crackling digital noise tail fading into silence,

dry and compact,
utilitarian late-20th-century military electronics,
controlled and restrained,
single isolated sound effect,
duration about 1 second
```
Negative
```text
piercing beep, shrill tone, very high pitch,
screech, harsh alarm, siren,
rising startup tone,
positive confirmation chime,
explosive transient, impact,
laser, sci-fi weapon,
clean smartphone notification,
cute UI sound, arcade sound,
pure sine wave,
smooth pristine digital tone,
music, melody, chord, rhythm, beat,
cinematic boom, cinematic whoosh,
long drone, long sustained tone,
heavy distortion, clipping,
large reverb, echo,
voice, speech, vocals
```

**A6** — positive
```text
ultra-short rugged military handheld terminal cursor sound effect,
one clear compact electronic navigation beep,
distinct single mid-high pitched beep around 1 kHz,
very short duration,
fast attack and fast decay,

the beep is layered with a tiny filtered radio static burst,
brief radio squelch texture,
subtle RF interference,
tiny digital chatter,
gritty communications equipment noise,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

precise and functional,
dry and compact,
restrained late-20th-century military electronics aesthetic,
single isolated interface sound,
no sustained tail,
duration about 0.1 second
```
Negative
```text
long beep, sustained tone,
multiple beeps, repeated beeps,
piercing, shrill, screeching,
alarm, siren, warning buzzer,
large startup sound, shutdown sound,
explosive transient,
laser, sci-fi weapon,
smartphone notification,
cute UI sound,
arcade sound,
coin sound,
keyboard click,
mouse click,
music, melody, rhythm, beat,
cinematic sound,
reverb, echo,
voice, speech, vocals
```

**A7** — positive
```text
ultra-short rugged military handheld terminal cursor sound effect,
one compact low-mid electronic navigation tone,
a rounded short "doo" style confirmation sound,
main tone centered around 500 to 600 Hz,
soft attack and short decay,
warm low-mid electronic body,
subtle low-frequency weight,

the tone is layered with a tiny filtered radio static burst,
brief dark radio squelch texture,
subtle RF interference,
very small amount of digital chatter,
gritty communications equipment texture,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

dark, restrained, compact and functional,
not bright,
not sharp,
single isolated interface sound,
duration about 0.12 seconds
```
Negative
```text
high-pitched beep,
bright beep,
sharp chirp,
piercing tone,
shrill sound,
thin electronic tone,
1 kHz beep,
high frequency,
strong upper harmonics,
screech,
alarm,
siren,
warning buzzer,
multiple beeps,
repeated beeps,
long sustained tone,
smartphone notification,
cute UI sound,
arcade sound,
laser,
music,
melody,
rhythm,
reverb,
echo,
voice,
speech,
vocals
```

**A8** — positive
```text
ultra-short rugged military handheld terminal cursor sound effect,
one compact low-mid electronic navigation tone,
a rounded short "doo" style confirmation sound,
main tone centered around 300 to 400 Hz,
soft attack and short decay,
warm low-mid electronic body,
subtle low-frequency weight,

the tone is layered with a tiny filtered radio static burst,
brief dark radio squelch texture,
subtle RF interference,
very small amount of digital chatter,
gritty communications equipment texture,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

dark, restrained, compact and functional,
not bright,
not sharp,
single isolated interface sound,
duration about 0.12 seconds
```
Negative: same as A7

**A9** — positive
```text
ultra-short rugged military handheld terminal cursor sound effect,
one compact low-mid electronic navigation tone,
a rounded short "doo" style confirmation sound,
main tone centered around 100 to 200 Hz,
soft attack and short decay,
warm low-mid electronic body,
subtle low-frequency weight,

the tone is layered with a tiny filtered radio static burst,
brief dark radio squelch texture,
subtle RF interference,
very small amount of digital chatter,
gritty communications equipment texture,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

dark, restrained, compact and functional,
not bright,
not sharp,
single isolated interface sound,
duration about 0.12 seconds
```
Negative: same as A7

**A10** — positive
```text
ultra-short rugged military handheld terminal cursor sound effect,
one compact low-mid electronic navigation tone,
a rounded short "doo" style confirmation sound,
main tone centered around 700 to 800 Hz,
soft attack and short decay,
warm low-mid electronic body,
subtle low-frequency weight,

the tone is layered with a tiny filtered radio static burst,
brief dark radio squelch texture,
subtle RF interference,
very small amount of digital chatter,
gritty communications equipment texture,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

dark, restrained, compact and functional,
not bright,
not sharp,
single isolated interface sound,
duration about 0.12 seconds
```
Negative: same as A7

**A11** — positive
```text
short rugged military handheld terminal error buzzer,
single low-mid electronic rejection tone,
dark compact buzzer centered around 400 to 500 Hz,
slightly descending pitch,
rough rounded electronic waveform,
subtle odd harmonics,
brief electromechanical buzzer texture,
controlled amplitude flutter,

layered with a short filtered military radio static burst,
dark radio squelch,
subtle RF interference,
tiny digital chatter,
gritty communications equipment noise,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

clear invalid-operation feedback,
firm and unpleasant but not piercing,
dry, compact and utilitarian,
restrained late-20th-century military electronics aesthetic,
single isolated sound effect,
duration about 0.3 seconds
```
Negative
```text
high-pitched buzzer,
sharp beep,
bright tone,
piercing alarm,
shrill sound,
screech,
siren,
emergency alarm,
multiple beeps,
repeating warning,
smartphone notification,
cute UI sound,
arcade sound,
laser,
cinematic warning,
explosion,
huge impact,
pure sine wave,
smooth clean digital tone,
music,
melody,
rhythm,
beat,
long sustained tone,
heavy distortion,
clipping,
large reverb,
echo,
voice,
speech,
vocals
```

**A12** — positive
```text
short rugged military handheld terminal error sound,
ONE single continuous low-mid electronic rejection tone,
only one sound event,
steady unmodulated tone,
no pulsing,
no repetition,
no tremolo,
no flutter,

dark compact buzzer centered around 400 to 500 Hz,
slightly descending pitch,
rounded rough electronic waveform,
subtle odd harmonics,
firm and controlled,

layered with a very subtle filtered military radio static texture,
dark radio squelch texture,
subtle RF interference,
gritty communications equipment character,
small military field radio speaker,
slightly lo-fi narrow-band electronics,

clear invalid-operation feedback,
dry, compact and utilitarian,
single isolated sound effect,
duration about 0.25 seconds
```
Negative
```text
multiple beeps,
repeated beeps,
repeating buzzer,
pulsing tone,
tremolo,
flutter,
vibrato,
stuttering,
rapid pulses,
oscillating volume,
alternating tones,
two-tone alarm,
warbling,
siren,

high-pitched buzzer,
sharp beep,
bright tone,
piercing alarm,
shrill sound,
screech,
smartphone notification,
arcade sound,
music,
melody,
rhythm,
beat,
long sustained tone,
heavy distortion,
reverb,
echo,
voice,
speech,
vocals
```

**A13** — positive
```text
short rugged military terminal error sound effect,

ONE single attention-getting electronic error tone,
exactly one tone event,
single steady tone around 1100 to 1300 Hz,
bright and sharp,
clear high-mid frequency warning tone,
short and immediate,
stable pitch from beginning to end,
constant tone character,
clean fast attack,
short clean decay,

no pitch movement,
no modulation,
no pulsing,

a tiny burst of filtered military radio static immediately before the tone,
a very short radio noise tail immediately after the tone,
the radio texture must NOT overlap heavily with the main tone,

small rugged communications device speaker,
slightly lo-fi narrow-band military electronics,
dry and compact,
utilitarian tactical equipment,
clear invalid-operation feedback,
single isolated sound effect,
duration about 0.2 seconds
```
Negative
```text
tremolo,
vibrato,
flutter,
warble,
wobble,
pulsing,
amplitude modulation,
frequency modulation,
pitch modulation,
pitch sweep,
descending pitch,
rising pitch,
detuned layers,
beating frequencies,

multiple beeps,
repeated beeps,
double beep,
triple beep,
stuttering,
rapid pulses,
repeating alarm,
oscillating tone,
two-tone alarm,
siren,

low pitched tone,
deep buzzer,
bass tone,
soft confirmation sound,

music,
melody,
rhythm,
beat,
arcade sound,
smartphone notification,
cinematic impact,
reverb,
echo,
voice,
speech,
vocals
```

**A14** — positive
```text
short rugged military handheld terminal error sound effect,

ONE single clear electronic error beep,
exactly one short tone event,
bright high-mid frequency beep,
main tone around 1500 to 1800 Hz,
clean sharp "di" style electronic tone,
short fast attack,
short clean decay,
stable pitch,
no pitch movement,
no modulation,
no pulsing,
no repetition,

a tiny filtered military radio static burst immediately before the beep,
very subtle short radio noise tail after the beep,
gritty communications equipment texture,
small military field radio speaker character,
slightly lo-fi narrow-band electronics,

attention-getting but controlled,
clear invalid-operation feedback,
dry and compact,
single isolated sound effect,
duration about 0.12 seconds
```
Negative
```text
low pitched tone,
deep tone,
deep buzzer,
rounded "doo" sound,
bass-heavy sound,

tremolo,
vibrato,
flutter,
warble,
wobble,
pulsing,
amplitude modulation,
frequency modulation,
pitch sweep,
detuned layers,
beating frequencies,

multiple beeps,
repeated beeps,
double beep,
triple beep,
stuttering,
repeating alarm,
two-tone alarm,
siren,

extremely piercing screech,
harsh clipping,
laser,
arcade sound,
smartphone melody,
music,
melody,
rhythm,
beat,
reverb,
echo,
voice,
speech,
vocals
```

**A15** — positive
```text
short rugged military handheld terminal error sound effect,

ONE single clear electronic error beep,
exactly one short tone event,
bright high-mid frequency beep,
main tone around 1500 to 1800 Hz,
clean sharp "di" style electronic tone,
short fast attack,
short clean decay,
stable pitch,
no pitch movement,
no modulation,
no pulsing,
no repetition,


attention-getting but controlled,
clear invalid-operation feedback,
dry and compact,
single isolated sound effect,
duration about 0.12 seconds
```
Negative: same as A14

**A16** — positive
```text
short rugged military handheld terminal error sound effect,



attention-getting but controlled,
clear invalid-operation feedback,
dry and compact,
single isolated sound effect,
duration about 0.12 seconds
```
Negative: same as A14

**A17** — positive
```text
short rugged military handheld terminal error sound effect,



attention-getting but controlled,
clear invalid-operation feedback,
dry and compact,
single isolated sound effect,
duration about 0.12 seconds
```
Negative: (empty)

**A18** — positive
```text
short rugged military handheld terminal error sound effect,

duration about 0.12 seconds
```
Negative: (empty)

**A19** — positive
```text
short rugged military handheld terminal error sound effect,

duration about 0.12 seconds
```
Negative
```text
[typed in Chinese; English translation] no multiple sounds, generate only one sound
```

**A20** — positive
```text
short rugged military handheld terminal error sound effect,
[typed in Chinese; English translation] no multiple sounds, generate only one sound
duration about 0.12 seconds
```
Negative: same as A19

**A21** — positive
```text
short rugged military handheld terminal error sound effect,
```
Negative: same as A19

**A22** — positive
```text
short rugged military handheld terminal error sound effect,
only one "doo" sound
```
Negative
```text
only one "doo"
```

**A23** — positive
```text
short rugged military handheld terminal error sound effect,
only one "dii" sound
sound should be shape
```
Negative: (empty)

**A24** — positive
```text
short rugged military handheld terminal error sound effect,
only one "di" sound
sound should be shape
```
Negative: (empty)

**A25** — positive
```text
short rugged military handheld terminal error sound effect,
only one "di" sound
sound should be shape
```
Negative
```text
not too many noise
```

**A26** — positive
```text
short rugged military handheld terminal error sound effect,
only one "di" sound
sound should be shape
```
Negative
```text
too many noise
```

**A27** — positive
```text
short rugged military handheld terminal error sound effect,
only one "di" sound
sound should be shape
```
Negative
```text
too much noise
```

**A28** — positive
```text
short military handheld terminal error sound effect,
only one "di" sound
sound should be shape
```
Negative: same as A27

**A29** — positive
```text
short military handheld terminal error sound effect,
only one "di" sound
sound should be sharp
```
Negative: same as A27

**A30** — positive
```text
short military handheld terminal error sound effect,tones go high to low
only one "di" sound
sound should be sharp
```
Negative: same as A27

**A31** — positive
```text
short military handheld terminal error sound effect,frequency go high to low
only one "di" sound
sound should be sharp
```
Negative: same as A27
