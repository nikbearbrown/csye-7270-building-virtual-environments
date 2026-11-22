# Evidence-led commentary

| Artifact + range | Visible observation | Interpretation / limit | Next experiment |
|---|---|---|---|
| capture/npc_in_game 40–370 (B04, B06) | Closure changes cell every 10 frames, no hitch at the wrap | Matches the key spacing (1/3 s); one fixture run | Five-wrap seam check by the user (done in the game: "All fine") |
| capture/npc_in_game 400–760 (B10) | the three squad figures do not all breathe together | The seek-once rule works on this floor; two of three phases coincide (S7: 1/3, 1/3, 2/3) | Seed with more spread if visible in step |
| logs/a7_mutations (B08) | m1–m3 exit 1 with the right line; m4 passes | The read-back catches a misnamed track the engine would play silently | — |
| r0 frames 27/29/49/50 + wave_dodges log (B12) | sprite ↔ rig swap at the phase edges | One authority over the sprite's visible; no blank frame seen | — |
| test_wave_state_machine log (B14) | clip position = state time every tick, both rates | Clocks agree headlessly; says nothing about the look | — |
| capture/rig_turntable (B16) | wind-up, sweep, settle over 20 frames | Motion is small at 1× zoom; the lean is 2–3 px | Larger lean on the f6 key, prediction first |
| r0 strip (B18) | boundaries 29/37/41/50; the click's big hit flash on 29 | Claude's reading only: the startup may read as "already hit"; the user kept r0 | A readable wind-up (the Your Turn) |
| capture/wave_dodges (B20) | startup dodge keeps the charge; active/recovery dodges after the wave | The edge rule holds in one scripted run | Human play with stuns and death mid-release |

Observations are separated from source explanations. No claim about fun, fairness or accessibility follows from these captures.
