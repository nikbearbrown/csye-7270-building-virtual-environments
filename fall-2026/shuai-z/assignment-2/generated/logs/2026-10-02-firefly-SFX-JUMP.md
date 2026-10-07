# Generation log: SFX-JUMP (Adobe Firefly, 2026-10-02)

One prompt in Adobe Firefly's Generate sound effects, which gave four takes. I downloaded all four and noted the prompt in a text file beside them.

- **Model and version:** the Firefly page shows no model name. Each take's Content Credentials do: the WAV's XMP chunk links to a manifest on `cai-manifests.adobe.com`, which Claude fetched on 2026-10-02. For take 04 it names the software agent `Adobe Firefly GenSoundFX 2`, the operation `audio_text2sfx` and `com.adobe.firefly.version` 1.2, and it is signed by Adobe Firefly C2PA. The manifests of takes 01–03 were not fetched.
- **Account:** Adobe's free plan, with no paid subscription
- **Time:** take 04's manifest says it was created at 2026-10-03 00:20:12 UTC, which is the evening of 2026-10-02 in my time zone
- **Seed:** not available
- **Output:** four WAV files, each 1.000 s, 48 kHz, 16-bit stereo; the two channels are almost identical (correlation 0.999 on take 04)
- **Manifests:** take 01 `urn-c2pa-fcd91a99-06a2-420c-bc35-458ebaa46f45-adobe`, 02 `urn-c2pa-410f403c-a080-41a4-b7aa-e1b700e0ea30-adobe`, 03 `urn-c2pa-2791d53f-60be-49a1-81d9-9209a6ba1d06-adobe`, 04 `urn-c2pa-9ac809e8-7c73-4143-8d25-7f59cbd99662-adobe`

## Prompt

The shared block and the SFX-JUMP line from `design/generation-prompts.md`, joined with one space and unchanged; Claude compared them character by character.

```text
A single short sound effect for a cozy 2D fantasy platformer. Soft, warm and rounded rather than harsh or loud. Clean and close, dry with almost no reverb, no music, no voice, no background noise, no other sounds. A quick, light jump: a soft upward whoosh of air with a little flutter of a cloth robe. Gentle and springy, not cartoonish.
```

## Takes

Measured by Claude: the peak level, and when each take rises above and falls below 40 dB under its own peak.

| Take | Peak | Audible from | Audible to | Outcome |
|---|---|---|---|---|
| SFX-JUMP-01 | −9.6 dBFS | 117 ms | 674 ms | not chosen |
| SFX-JUMP-02 | −14.8 dBFS | 223 ms | 630 ms | not chosen |
| SFX-JUMP-03 | −15.2 dBFS | 88 ms | 777 ms | not chosen |
| SFX-JUMP-04 | −6.7 dBFS | 122 ms | 476 ms | **accepted:** "足够明显，能听得出主角起跳了，声音也不怪" [it is clear enough: you can hear him take off, and it doesn't sound strange] |

Take 04 swells from about 210 ms to its peak at 320 ms. Before 210 ms it is more than 30 dB under the peak. The game file starts there, so the peak comes about 0.11 s after the jump key, while Rudy rises.
