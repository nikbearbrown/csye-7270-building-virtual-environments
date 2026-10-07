# Generation log: SFX-HURT, SFX-PORTAL, SFX-SLASH and SFX-PICKUP (ElevenLabs, 2026-10-03)

Four prompts in ElevenLabs' sound effects, four takes each, made the same way as SFX-STOMP ([log](2026-10-03-elevenlabs-SFX-STOMP.md)).

- **Model and version:** the default model on my free ElevenLabs account, as for SFX-STOMP. The files carry no model name (only an `encoder` tag, Lavf59.27.100); ElevenLabs lists one sound-effects model, `eleven_text_to_sound_v2`
- **Account:** ElevenLabs free plan
- **Time:** the file names carry Unix timestamps from 2026-10-04 02:16:06 to 02:24:42 UTC, the evening of 2026-10-03 in my time zone; probably when the files were saved
- **Seed and other settings:** not recorded. The lengths, the same for all four takes of a sound, suggest a duration setting: 0.480 s for the hurt and slash, 2.000 s for the portal, 0.800 s for the pickup
- **Output:** WAV, 48 kHz, 16-bit stereo
- **Prompts:** the shared block and each sound's line from `design/generation-prompts.md`, assumed unchanged; the file names start with the prompt's first words. They are not repeated here
- **Files:** the downloads were named `A_single_short_sound_#1` to `#4` in a folder per sound; they are saved as `SFX-<ID>-01` to `-04` in that order

## Takes

Measured by Claude: the peak level and its time, and when each take rises above and falls below 40 dB under its peak. "Mono" is the correlation of the two channels; 1 means they are the same.

| Take | Peak | Audible | Mono | Outcome |
|---|---|---|---|---|
| SFX-HURT-01 | −2.8 dBFS at 45 ms | 0–156 ms | 0.999 | **accepted:** "很像人物受伤后发出的叫声" [it sounds a lot like the cry a character makes when hurt] |
| SFX-HURT-02 | −7.1 dBFS at 12 ms | 0–454 ms | 0.997 | not chosen |
| SFX-HURT-03 | −1.3 dBFS at 99 ms | 63–480 ms | 0.999 | not chosen |
| SFX-HURT-04 | −21.5 dBFS at 4 ms | 0–480 ms | −0.867 | not chosen |
| SFX-PORTAL-01 | 0.0 dBFS at 17 ms | 0–835 ms | 0.643 | not chosen |
| SFX-PORTAL-02 | −1.6 dBFS at 525 ms | 0–2000 ms | 0.987 | **accepted:** "有那种被传送阵传送走的感觉" [it feels like being carried away by the teleport circle] |
| SFX-PORTAL-03 | 0.0 dBFS at 245 ms | 0–1406 ms | 0.486 | not chosen |
| SFX-PORTAL-04 | 0.0 dBFS at 269 ms | 0–1334 ms | 0.456 | not chosen |
| SFX-SLASH-01 | −40.7 dBFS at 480 ms | 0–480 ms | 0.608 | not chosen (almost silent) |
| SFX-SLASH-02 | −0.2 dBFS at 10 ms | 0–134 ms | 0.917 | not chosen |
| SFX-SLASH-03 | 0.0 dBFS at 224 ms | 76–398 ms | 0.495 | **accepted:** "有那种挥动剑时风发出的声音" [it has the sound of the wind when a sword is swung] |
| SFX-SLASH-04 | −1.4 dBFS at 99 ms | 0–232 ms | 0.166 | not chosen |
| SFX-PICKUP-01 | −0.6 dBFS at 131 ms | 0–270 ms | 0.264 | not chosen |
| SFX-PICKUP-02 | 0.0 dBFS at 180 ms | 0–799 ms | 0.779 | **accepted:** "有金属碰撞发出的声音" [it has the sound of metal striking metal] |
| SFX-PICKUP-03 | −2.6 dBFS at 2 ms | 0–326 ms | 0.994 | not chosen |
| SFX-PICKUP-04 | −10.3 dBFS at 15 ms | 0–164 ms | 0.991 | not chosen |

## Notes on the accepted takes

- **SFX-HURT-01** sounds like a cry, although the prompt asked for no voice and CONCEPT.md asked for a non-vocal hurt cue. I chose it for that, and CONCEPT.md was revised to keep it.
- **SFX-PORTAL-02** and **SFX-PICKUP-02** end in a short click in their last 40 ms and 10 ms; the game files are cut before it.
- **SFX-SLASH-03** has 8 samples at full scale (clipped) around its peak, and its channels differ more than the others': the mono mix is 1.3 dB quieter than the stereo take. The mix is normalized afterwards.
- In the game files, the hurt and the portal are about 4 dB louder than the jump and the stomp (loudest 100 ms: hurt −9.7, portal −10.5, slash −12.5, pickup −12.6, stomp −13.5, jump −14.0 dBFS RMS). The balance between the sounds is set in build step 3.
