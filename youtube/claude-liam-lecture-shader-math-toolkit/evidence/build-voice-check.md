# Voice check (faster-whisper small)

**What this is.** Automatic transcription of each beat's Kokoro audio against `narration.py`; a rough ear, not a replacement for Bear's.

**Found.** 47 beats; 4 below 0.85 similarity (listed with transcripts). Pronunciation dictionary untouched.

| beat | similarity |
|---|---|
| BOPEN | 1.00 |
| BIDEA | 0.99 |
| BDEFS | 1.00 |
| B01 | 1.00 |
| B02 | 0.93 |
| B03 | 1.00 |
| B04 | 1.00 |
| B05 | 0.97 |
| B06 | 0.98 |
| B07 | 1.00 |
| B08 | 0.99 |
| B09 | 1.00 |
| B10 | 1.00 |
| B11 | 0.87 |
| B12 | 0.43 |
| B13 | 1.00 |
| B14 | 0.83 |
| B15 | 1.00 |
| B16 | 0.98 |
| B17 | 0.94 |
| B18 | 1.00 |
| B19 | 0.85 |
| B20 | 0.97 |
| B21 | 1.00 |
| B22 | 0.87 |
| B23 | 0.99 |
| B24 | 0.91 |
| B25 | 0.83 |
| B26 | 1.00 |
| B27 | 0.88 |
| B28 | 1.00 |
| B29 | 0.91 |
| B30 | 0.96 |
| B31 | 1.00 |
| B32 | 0.93 |
| B33 | 0.99 |
| B34 | 0.99 |
| B35 | 0.95 |
| B36 | 1.00 |
| B37 | 0.99 |
| B38 | 1.00 |
| B39 | 1.00 |
| B40 | 1.00 |
| B41 | 1.00 |
| BVDT | 1.00 |
| BHTF | 1.00 |
| BOUT | 0.99 |

## Low beats (read the transcript, then LISTEN)

### B12 (0.43)
- spoken text: The docs spell out the formula. Squeeze the input between the edges into zero to one, call that t, and return three t squared minus two t cubed. They also warn that a first edge at or above the second gives undefined results.
- heard: The docs spell out the formula. Squeeze the input between the edges into 0 to 1, call that T, and return 3T squared minus 2T cubed. They also warn their first edge at or above the second gives undefined results.

### B14 (0.83)
- spoken text: Mix slides between two values. Give it a start, an end, and a weight. Weight zero returns the start, one returns the end, one half lands halfway. It does not pin the weight: a weight of two overshoots the end, so clamp it first.
- heard: Mix slides between two values, give it a start, an end, and a wait. Wait 0 returns the start, 1 returns the end, 1 half lands halfway. It does not pin the wait. A wait of 2 overshoots the end, so clamp it first.

### B19 (0.85)
- spoken text: Fract keeps only what comes after the decimal point. Two point seven five becomes point seven five. Multiply the ramp by four first, and fract gives four ramps in a row, each starting over at zero.
- heard: Frack keeps only what comes after the decimal point. 2.75 becomes 0.75. Multiply the ramp by 4 first, and Frack gives 4 ramps in a row, each starting over at zero.

### B25 (0.83)
- spoken text: One trap. In a shader, mod of minus point two five and one is point seven five: it follows floor. G D script's F mod keeps the sign and says minus point two five. F pos mod matches the shader. Check which one you wrote.
- heard: One trap in a shader mod of minus 0.25 and 1 is 0.75, it follows floor, gd scripts fmod keeps the sign and says minus 0.25, fposs mod matches the shader, check which one you wrote.
