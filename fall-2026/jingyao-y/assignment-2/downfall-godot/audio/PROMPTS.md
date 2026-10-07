# Audio prompts — Gemini music generation

Every runtime audio file in `audio/` was generated with Gemini's music tool (the
"Music" mode in the Gemini app), downloaded as MP3 into `music/`, and cut by
`audio/tools/cut_audio.py`. The download always comes out at roughly one minute
whatever the prompt asks for, so each prompt asks for the wanted sound first.

Status of each prompt text:

- **confirmed**: the author pasted the exact text used back into the session.
- **as supplied**: the prompt as written for the author in the session; the
  author has not yet confirmed it was pasted unchanged.

## P-LIGHTS-ON → `music/开灯.mp3` → `audio/sfx/lights_on.wav` (as supplied)

```
Generate a sound effect, about 0.6 seconds long, no music, no voice.
A real large industrial warehouse: one row of big high-bay ceiling lights
being switched on. A heavy, loud wall-mounted breaker switch "KA-CHUNK",
immediately followed by the electric buzz and soft ballast hum of large
warehouse lamps powering up high above. Recorded inside a huge, empty
concrete warehouse with metal roof — the clunk has a short, natural
hollow echo off the concrete and steel (decaying within about 0.4 seconds).
Realistic, not sci-fi, not cartoonish. No background noise, no footsteps.
It will play 4 times, 0.45 seconds apart, one per row of lights, so each
hit must be a single clean switch-on.
```

## P-LIGHTS-OFF → `music/关灯.mp3` → `audio/sfx/lights_off.wav` (confirmed)

```
This is a single sound effect for a video game, NOT a song. No melody, no rhythm, no beat, no chords. Generate a sound effect, about 1 second long, no music, no voice.

The same huge empty concrete warehouse: the main breaker for all the

high-bay ceiling lights being switched off. One deep heavy "KA-CHUNK",

then the electric buzz of the big lamps fading out, with a short natural

hollow echo in the large hall. Realistic, not sci-fi. Silence by 1 second.
```

## P-BASE → `music/基地背景音乐.mp3` → `audio/music/base_loop.ogg` (as supplied)

```
Instrumental loop for the home base of a high-tech pharmaceutical
company aboard a giant mobile land-ship — a calm hub where operators
manage storage and prepare for missions.
- Exactly 100 BPM, 4/4, constant tempo, exactly 16 bars (38.4 seconds).
- Clean modern electronic with glitchy IDM textures: crisp light broken-beat
  electronic drums, a soft felt-piano motif, bright synth plucks,
  wide warm pads with gentle sidechain pumping, and small mechanical
  foley sounds used as rhythm (servo whirs, hydraulic hiss, relay clicks).
- Cool, industrial, high-tech, but warm and reassuring underneath;
  slightly melancholic, hopeful. Polished, not lo-fi, not dramatic.
- NO intro, NO outro, NO fade-in or fade-out, NO ending hit. The last bar
  must flow directly into the first bar for a seamless loop.
- No vocals. Medium-low energy, leave space for sound effects.
```

Measured result: not 100 BPM and not 16 bars. The file is 154 s, two passes of a
75.30 s section (sparse half, dense half) and a fade-out.

## P-MINE → `music/矿洞外勤音乐.mp3` → `audio/music/mine_loop.ogg` (as supplied)

```
Instrumental track for exploring a dark abandoned underground mine in a
sci-fi action game, between fights. Strict structure, exactly 96 BPM,
4/4, constant tempo, key of D minor, 24 bars total (60 seconds):

Bars 1–4 (INTRO, 10 s): starts from near silence — a low drone, distant
water drips and creaking mine timbers, then the sub-bass pulse enters.

Bars 5–20 (MAIN LOOP, 40 s): steady and tense. Pulsing low synth bass,
sparse metallic percussion that sounds like hammered pipes and chains
in a cavern, deep reverberant hits, distant industrial machinery, and a
quiet, lonely minor-key motif on a dark synth or bowed metal. Keep the
energy flat and even through all 16 bars, with no build-ups or drops,
so bar 20 can loop back into bar 5 seamlessly.

Bars 21–24 (ENDING, 10 s): the percussion drops out, the motif plays once
more slowly and resolves on a low D, a final deep resonant hit that rings
out and decays to silence.

No vocals. Medium-low energy, leave space for combat sound effects.
```

Measured result: E minor (not D minor), bar length 3.2 s (about 75 BPM, not 96).
Intro to about 11 s, main section to 51.6 s, then a short decay.

## P-EXTRACT → `music/撤离.mp3` → `audio/music/sting_extract.ogg` (as supplied)

```
A short instrumental music sting for a video game, NOT a full song.

It must start immediately at 0:00, with no silence or intro before it. It lasts about 6 seconds plus a natural reverb tail: a mission report screen after an operator has been safely extracted. Clean modern sci-fi electronic: a short rising melody on bright synth plucks and soft felt piano over a warm synth pad, landing on a warm, resolved major chord. Relieved, calm, quietly hopeful; not triumphant, no fanfare, no heavy drums. Let the final chord ring out and fade to silence by about 8 seconds.

After that, complete silence until the end. No vocals, no other music, no second section.
```

Measured result: 0.6 s of silence first, the sting to 6.28 s, then a different,
longer piece (not used).

## P-FAIL → `music/失败.mp3` → `audio/music/sting_fail.ogg` (as supplied)

```
A short instrumental music sting for a video game, NOT a full song.

It must start immediately at 0:00, with no silence or intro before it. It lasts about 6 seconds plus a natural reverb tail: a mission report screen after an operator has fallen in the field. Clean modern sci-fi electronic: a slow, lonely descending melody on a soft dark synth and a few muted piano notes over a low sustained pad, ending on an unresolved minor chord that fades away. Serious, heavy, sad, but not horror and not scary. No drums. Fade to silence by about 8 seconds.

After that, complete silence until the end. No vocals, no other music, no second section.
```

Measured result: the sting repeats; the first take is 12.0 s (longer than asked).

## Not generated yet

- P-HATCH (airlock floor hatch, `audio/sfx/hatch.wav`) and P-SHELF (rack rising,
  `audio/sfx/shelf.wav`). Both cues are wired and counted; they stay silent until
  the files exist.
