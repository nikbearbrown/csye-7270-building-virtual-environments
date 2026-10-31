# Rebuild the A5 film

Use the delivered A5 project and the local Brutalist toolkit. Preserve existing films and source. Set PYTHONUTF8=1 and use the interpreter with kokoro-onnx installed. Never publish.

1. Review TEST-REPORT and the measurement JSON files. Recheck shader hashes and code line ranges.
2. Run tools/a5/build_film.py author only for a new build; it resets the authored sheet. Do not overwrite an already measured sheet accidentally.
3. Generate audio with runtime/scripts/generate_audio_kokoro.py REEL. Use the existing am_onyx voice. Run tools/a5/attach_outro.py to bind the shipped channel jingle and its full duration; never synthesize over it.
4. Run tools/a5/make_film_media.py against the retained captures. Re-record native 4K gameplay if missing. Do not upscale recorded gameplay or retime actions.
5. Render a pilot using runtime/scripts/remotion_scenes.py REEL --only B04, inspect it, then render remaining established scenes with that wrapper.
6. Run tools/a5/brand_data_beats.py after rendering B18/B19, then write records with tools/a5/write_film_records.py, then tools/a5/build_film.py ledger. Run art godot-gamedev --check REEL --game PROJECT.
7. Run art final REEL --height 2160 --fps 30 --out REEL/exports/landscape. Retain normal audio, paperwork, frame and source gates.
8. Inspect the actual master at 2 fps plus each beat near 15/50/85 percent, including source at reading size, motion order, audio and the silent regular outro. Record defects and fixes in _qc/REPORT.md. Do not call a probe alone visual QC.
9. Refresh the source inventory after final artifacts are created and rerun the game-development checker. Verify the exported file's SHA-256 against its receipt. Keep the previous films and failed-attempt records.
