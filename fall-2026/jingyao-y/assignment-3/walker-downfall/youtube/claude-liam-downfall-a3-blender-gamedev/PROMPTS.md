# PROMPTS.md

## Film narration

All narration is written in `tools/build_sheet.py`. Kokoro (`am_onyx`) generated it locally via `runtime/scripts/generate_audio_kokoro.py`, at a cost of $0.00.

## Reconstructed prompts on screen

- **B00 (cold open):** a reconstructed Walker ask, labelled "illustrative, not a transcript". The author's real instructions to Claude were in Chinese and much longer.
- **B19 (Your Turn):** a prompt the viewer can paste. It is not a record of anything sent.

## Asset "prompts"

No image or 3D generator was used, so the assets have no generation prompts. Every Blender step is the code itself, in `tools/blender/build_*.py`.
