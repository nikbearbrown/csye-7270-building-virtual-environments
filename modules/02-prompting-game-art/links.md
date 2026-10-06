# Module 2 — Helpful links

## Executive summary

These are the pages to open while you work through Module 2: the companion chapter and its run records, the official Godot documentation behind each import setting, the public Walker projects, and the tools you need installed. Open the Godot pages when a setting in an `.import` file or a node surprises you, and the Walker pages when you need a starting repository.

## Read first

- [Chapter 2 — Prompting Game Art (and Sound) Against the Engine](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/02-prompting-game-art.md) — the long reading behind this lesson, with the Unity and Unreal comparisons and every source.
- [Chapter 2 worked-example record](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/main/examples/02-prompting-game-art) — the exact prompts, logs, diffs and agent transcripts from the 27 September 2026 runs, plus the independent check scripts you copy in Verify.

## Godot documentation

- [Import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html) — open it to see how the `.import` sidecar, the `.godot/imported/` cache and version control fit together, and which files to commit.
- [Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html) — open it when a sprite looks soft or a texture setting seems to have no effect; it says where filter and repeat modes live in Godot 4.
- [ResourceImporterTexture](https://docs.godotengine.org/en/stable/classes/class_resourceimportertexture.html) — the reference for every texture import parameter, including `compress/mode`, `mipmaps/generate` and `process/fix_alpha_border`.
- [Importing audio samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html) — open it before you import sound or music: WAV versus Ogg Vorbis, loop modes and loop points.
- [2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) — `AnimatedSprite2D` with `SpriteFrames`, and `Sprite2D` with `AnimationPlayer`, for turning a sheet into frames.
- [CanvasItem](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html) — the class that owns `texture_filter`; check it when you set Nearest on a sprite node.
- [AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html) — `play()` and `max_polyphony`, for debugging a double-trigger or a cut-off sound.

## Walker projects

- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) — the practice project in this module: Clawd drawn in code, 18 animations, no image or audio files, and the `.gitignore` that hides `audio/`.
- [walker-jumpman](https://github.com/nikbearbrown/walker-jumpman) — the course starter Clawd was forked from; its `.gitignore` also hides `*.wav`.
- [walker-audio-generator](https://github.com/nikbearbrown/walker-audio-generator) — procedural sine-wave audio with no sound files, for seeing the difference between synthesis and a generative model.

## Tools

- [Godot Engine downloads](https://godotengine.org/download/) — install the regular edition, not the .NET one; the chapter's runs used Godot 4.7.2.
- [GNU coreutils on Homebrew](https://formulae.brew.sh/formula/coreutils) — on macOS this provides the `timeout` command that stops a hung headless test.
- [Audacity](https://www.audacityteam.org/) — a free audio editor from the old course page, for trimming silence from the front of a sound effect and cutting a music loop at a bar boundary.

## Going deeper

- [U.S. Copyright Office, Copyright and Artificial Intelligence, Part 2: Copyrightability (January 2025)](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf) — the report behind the provenance advice: when AI output is protected and why prompts alone do not count.
- [AudioCraft on GitHub](https://github.com/facebookresearch/audiocraft) — Meta's open audio generation repository; read its license statement for the difference between its code terms and its model-weight terms before you use any open model.
