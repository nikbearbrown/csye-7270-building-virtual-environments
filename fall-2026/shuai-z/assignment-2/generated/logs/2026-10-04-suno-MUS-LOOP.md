# Generation log: MUS-LOOP (Suno, 2026-10-04)

One song from Suno, recorded from the browser and cut into the Level 1 loop.

- **Model and version:** Suno v6 mini, as Suno showed it
- **Account:** Suno's free plan, with its default settings
- **Prompt:** the first MUS-LOOP prompt in `design/generation-prompts.md`, the one for a tool with a style field, as I said:

```text
instrumental folk, medieval countryside, warm and unhurried adventure, plucked lute, wooden recorder, fiddle, frame drum, gently bouncing, 104 BPM, D mixolydian, no vocals
```

- **Instrumental switch:** left at Suno's default; I do not know whether it was on. The song has no vocals
- **Why I kept it (my words):** "我觉得他有中世纪的异域风，而且听起来比较轻松愉悦" [I feel it has a medieval, exotic flavor, and it sounds fairly relaxed and cheerful]
- **Seed:** not available

## How the file was made

I did not download the song from Suno. I played it in the browser on Suno's site and recorded it with OBS 32.2.2 as an MP4. The MP4 stays on my computer and is not in the repository (course rule: no MP4 in git).

In Audacity 4.0.0 I cut the silence from the start and the end of the recording and exported it on purpose as a mono OGG: `walker-rudy.ogg`, exported on 2026-10-04 at 15:14 local time, 176.2 s, 48 kHz, mono, Vorbis at about 96 kbit/s. That file is the accepted take, `generated/accepted/MUS-LOOP-01.ogg`, unchanged.

The audio was compressed more than once on the way: by Suno's player stream, by OBS's encoder and by the Audacity export; the game file adds a fourth encoding. It is mono because of my export, not because of Suno.

## What Claude measured

- **Tempo:** 104.99 BPM, from the autocorrelation of an onset envelope. The beat grid stays within 6 ms of the song up to 120 s and drifts after that (+14 ms by 120–140 s, +234 ms by 160–176 s), so the loop is taken before 120 s.
- **Key:** the strongest pitch classes are D, A, B, E, F♯, G and C♯: D major, not the D mixolydian the prompt asked for (mixolydian would have C instead of C♯).
- **Structure:** comparing the harmony (pitch-class profile) of every beat with every other beat, the song repeats most clearly every 24 bars (mean similarity 0.44; 4 bars 0.38, 16 bars 0.31, 32 bars 0.27). The best 24-bar seam starts on beat 94 of the grid, at 53.919 s, with a similarity of 0.89 across the 8 beats after the seam and 0.81 across the 8 before it. The best 16-, 20- and 32-bar seams scored 0.55, 0.61 and 0.47.
- **Seam:** the end, 24 bars later, was moved 5.1 ms off the grid to 108.787 s, where the 2 s of waveform after it best match the 2 s after the start (correlation 0.42; the two repeats are played differently, so they are not identical).

## The loop

Made by `design/tools/prepare_music.py`:

- samples 2,588,126 to 5,221,757 of the take decoded at 48 kHz: 2,633,631 samples, 54.867 s, 24 bars;
- the beat after the end (0.5715 s) is crossfaded, at equal power, into the loop's first beat. The loop's last sample is then followed directly by the sample that followed it in the song, so the seam is continuous: in the decoded game file the step from the last sample to the first is 0.0006, under the median step between neighbouring samples, 0.0056;
- the level: the target was −16 LUFS, but the peak would then pass −1 dBFS, so the gain stops at −0.6 dB, with the peak at −1.0 dBFS and the loudness at −19.2 LUFS. No limiter was used;
- encoded with oggenc 1.4.3 (vorbis-tools, libvorbis 1.3.7) at quality 6: `game/systems/audio/music/MUS-LOOP.ogg`, mono, 48 kHz, 653 KB. The decoded file has exactly 2,633,631 samples;
- in Godot the import setting Loop is on, with the loop offset at 0. A headless check loads it with `loop` true and a length of 54.867 s.

## Listening

Before the loop was encoded, I listened to two previews that Claude rendered from the same cut: 10 s before and after the seam, and the whole loop three times in a row (2 min 45 s, seams at 0:54.9 and 1:49.7). My words: "接缝听不出来" [I can't hear the seam].
