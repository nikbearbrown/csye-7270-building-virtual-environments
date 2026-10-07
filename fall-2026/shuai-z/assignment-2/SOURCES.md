# SOURCES — walker-rudy

Credits, tools, generative models and their terms, and who did what. This file is updated as the work goes on; the generation records are in ASSET-LOG.md and the dated record in FRICTIONAL.md.

## Starting point

An empty repository, created on 2026-09-30. There is no starter code and no starter art: not walker-jumpman, and not my Assignment 1 project.

## People

- **Shuai Zhang (me):** design decisions, prompts, generation runs, choosing and rejecting outputs.
- No other collaborators or playtesters.

## Tools

| Tool | Version | Used for |
|---|---|---|
| Claude Code (desktop app), model Claude Opus 5.5 | — | Design questions and drafts; the documents; the blockout, check and contact-sheet scripts; the Godot code in `game/` |
| Python 3 with Pillow, NumPy, SciPy and Matplotlib | Pillow 10.4.0, NumPy 2.1.3, SciPy 1.15.3, Matplotlib 3.10.0 | `design/tools/make_blockouts.py`, `check_against_sheet.py`, `contact_sheet.py`, `matte_sprites.py`, which makes Rudy's game frames from the accepted originals (background removal, scaling, placement), `prepare_env.py`, which makes the Level 1 layers (keying, tiling, scaling, the soil below the ground), `prepare_props.py`, which makes the props and the goblin's frames, `prepare_sfx.py`, which makes the game's sound effects from the accepted takes (cutting, fades, mono, peak level), `prepare_music.py`, which cuts the music loop from the accepted take, `check_readability.py`, which re-measures Rudy's contrast on the generated Level 1, `plot_mix.py`, which measures the game's recorded mix for step 3 and draws it, and `compare_sheets.py`, which puts the step 5 screenshots beside the storyboard and the character sheet |
| Voyager browser extension | — | Exporting the Gemini chats into `generated/logs/` |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build | The game, in `game/`, written in GDScript; started on 2026-10-01 as a greybox with code-drawn placeholders. Its movie maker (`--write-movie`) recorded the step 3 evidence, the game's own mix |
| OBS Studio | 32.2.2 | Recording Suno's browser playback of MUS-LOOP-01 as an MP4, kept locally |
| Audacity | 4.0.0 | Cutting the silence from the start and end of that recording, and exporting it as a mono OGG |
| Brutalist toolkit (`brutalist.art`), skill `godot-gamedev` with the `walker` modifier | checkout `22264a3` | The film: its beat-sheet contract, Remotion scenes, narration wrapper, compiler and quality gates. Details in `youtube/claude-liam-walker-rudy-gamedev/SOURCES.md` |
| Kokoro-82M through kokoro-onnx, voice `am_onyx` ("Liam") | local model `kokoro-v1.0.onnx` | The film's narration, run locally and free; a synthetic voice, not a clone of anyone |
| Remotion | the toolkit's `runtime/remotion` | The film's title, editor-reconstruction, design-board, verdict and outro scenes |
| FFmpeg and vorbis-tools | FFmpeg 9.0.2; oggenc 1.4.3 with libvorbis 1.3.7 | Decoding and loudness measurement in the audio scripts; encoding the music loop and the step 3 mix; cutting and mixing the film |

## Generative models

| Model | Version | Where it ran | Terms | Assets |
|---|---|---|---|---|
| Gemini app image generation, which the app reports as Nano Banana | The exact image-model version is not shown. The chat model was Gemini 3.8 Flash | Gemini app, hosted by Google, on my personal Google account, on a paid plan | Google Terms of Service and the [Generative AI Additional Terms of Service](https://policies.google.com/terms/generative-ai). The page fetched on 2026-10-01 says it was last modified 2023-08-09. It forbids using the service to develop machine-learning models, requires following the Generative AI Prohibited Use Policy, and does not say who owns generated content | CHAR-REF-01 to CHAR-REF-07; the default-form poses CHAR-IDLE-01 to CHAR-CELEBRATE-01; the sword form CHAR-SWORD-IDLE-01 to CHAR-SWORD-FALL-01; the Level 1 environment (ENV-SKY-CASTLE, ENV-FIELDS, ENV-GROUND); the props, the goblin, the end card and UI-HEART |
| Adobe Firefly, Generate sound effects | The page shows no model name; the takes' Content Credentials name `Adobe Firefly GenSoundFX 2`, Firefly version 1.2 | Firefly web app, hosted by Adobe, on Adobe's free plan | Adobe General Terms of Use and Generative AI User Guidelines; details in ASSET-LOG.md. Outputs may be used commercially unless a beta feature says otherwise; Content Credentials must not be removed to mislead, so the game files keep their link | SFX-JUMP-01 to SFX-JUMP-04 |
| ElevenLabs sound effects | The free account's default model; the files do not name it. ElevenLabs lists one sound-effects model, `eleven_text_to_sound_v2` | ElevenLabs web app, hosted by ElevenLabs, on the free plan | ElevenLabs Terms of Service (last updated 2026-03-31): I keep the rights in my output, for non-commercial use only. Anything I publish with these sounds must have "elevenlabs.io" or "11.ai" in its title; details in ASSET-LOG.md | SFX-STOMP, SFX-HURT, SFX-PORTAL, SFX-SLASH and SFX-PICKUP, four takes each |
| Suno | v6 mini, as Suno showed it | Suno web app, hosted by Suno, on the free plan | Suno Terms of Service (effective 2026-09-03): free-plan output is for personal, non-commercial use only, and Suno keeps the rights in it; no attribution is required. Details in ASSET-LOG.md | MUS-LOOP-01 |
| ChatGPT image generation | Chat model GPT-5.6 Sol at high reasoning; the image model was ChatGPT's default, not named in the chat | ChatGPT, hosted by OpenAI, on my account, on a paid plan | OpenAI [Terms of Use](https://openai.com/policies/terms-of-use/), effective 2026-01-01, fetched 2026-10-02. As between me and OpenAI, I own the output, and OpenAI assigns me any rights it has in it; output may not be unique. OpenAI may use content to improve its services, and I can opt out of its use for training; details in ASSET-LOG.md | CHAR-SWORD-RUN-B-02 to -04, all rejected |

## Resemblance to an existing character

Rudy's name and look resemble Rudeus "Rudy" Greyrat from *Mushoku Tensei: Jobless Reincarnation*: light-brown hair, a grey hooded mage robe, and a young mage in a medieval other world. Claude pointed this out on 2026-10-01.

- No prompt names that character or that work.
- From 2026-10-01 the prompts do not name Rudy either; they say "the boy".
- For now, I have not changed his signature features.

## Human / AI contributions

The dated record is FRICTIONAL.md. In short:
- the design decisions are mine;
- Claude drafted the documents and prompts and wrote the scripts;
- the images in the game come from Gemini (three rejected run frames came from ChatGPT), and the sound effects from Adobe Firefly (SFX-JUMP) and ElevenLabs (from SFX-STOMP on), and the music from Suno;
- I chose and rejected the outputs.
- The film: Claude wrote its beat sheet, the narration, the capture driver and the build tools, and ran the captures, the builds and the quality checks; Kokoro voiced the narration. I watched and listened to the whole final film and found no problem, accepted the Liam narration, kept the slice's own audio in it as the assignment requires, put it on Google Drive where it opens without signing in, and chose not to publish it on YouTube, since the assignment does not require it.
- Gemini and ChatGPT ran on paid plans; Firefly, ElevenLabs and Suno on free plans. The assignment needs no paid service.
