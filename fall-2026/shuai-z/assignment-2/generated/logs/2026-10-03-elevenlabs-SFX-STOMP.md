# Generation log: SFX-STOMP (ElevenLabs, 2026-10-03)

One prompt in ElevenLabs' sound effects, which gave four takes. From this sound on I use ElevenLabs instead of Adobe Firefly.

- **Model and version:** the default model on my free ElevenLabs account. The WAV files carry no model name or provenance data (only an `encoder` tag, Lavf59.27.100). ElevenLabs' model list, fetched by Claude on 2026-10-03, gives one sound-effects model, `eleven_text_to_sound_v2`, so that is the most likely model, but the app did not confirm it
- **Account:** ElevenLabs free plan
- **Time:** the file names carry Unix timestamps of 2026-10-03 20:18:07–20:18:14 UTC, probably when the files were saved
- **Seed and other settings:** not recorded
- **Output:** four WAV files, each 0.480 s, 48 kHz, 16-bit stereo; the two channels are almost identical

## Prompt

The shared block and the SFX-STOMP line from `design/generation-prompts.md`, unchanged, as I said; the file names start with the prompt's first words.

```text
A single short sound effect for a cozy 2D fantasy platformer. Soft, warm and rounded rather than harsh or loud. Clean and close, dry with almost no reverb, no music, no voice, no background noise, no other sounds. A padded stomp: a soft, cushioned thump of small boots landing on top of a small creature, with a tiny squishy pop. Satisfying but gentle, no crunch, no bones.
```

## Takes

The downloads were named `A_single_short_sound_#1` to `#4`; they are saved as SFX-STOMP-01 to -04 in that order. Measured by Claude: the peak level and its time, and when each take falls below 40 dB under its peak.

| Take | Peak | Audible to | Outcome |
|---|---|---|---|
| SFX-STOMP-01 | −27.4 dBFS at 63 ms | 480 ms | not chosen |
| SFX-STOMP-02 | −1.1 dBFS at 2 ms | 289 ms | **accepted:** "有踩踏感" [it feels like a stomp] |
| SFX-STOMP-03 | −7.3 dBFS at 27 ms | 208 ms | not chosen |
| SFX-STOMP-04 | −26.8 dBFS at 25 ms | 353 ms | not chosen |

Take 02 has no silence at the start: its first sample is already at 41% of full scale, which would click, so the game file fades in over 3 ms. After 190 ms it is more than 33 dB under its loudest 10 ms.
