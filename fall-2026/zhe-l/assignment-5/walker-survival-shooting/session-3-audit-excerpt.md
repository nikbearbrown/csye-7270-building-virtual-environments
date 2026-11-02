# Session 3 (material audit) — labelled excerpt

**What this is:** an excerpt of the Claude Code session that ran the audit prompt (`prompt-3.txt`) and wrote `godot/MATERIALS.md` and `godot/tests/test_materials.gd`. The full transcript (`.jsonl`, about 1.5 MB, with my local paths and the agent's replies in Chinese) is kept on my computer and not posted, because the assignment asks for a labelled excerpt when a transcript is over about 1 MB.

**How it was run:** `claude -p` from Claude's shell fails to authenticate on this machine (recorded in FRICTIONAL for Assignment 5), so, as for session 1, I pasted the prompt into a fresh interactive Claude Code desktop session (model Claude Opus 5.5) started in my working folder on 2026-11-01 (times below are UTC, 2026-11-02 02:33–02:41). In that folder the Godot project is `project-survival-shooting/` (here `godot/`); the prompt says so.

**Final state (the check the assignment asks for after every agent session):** the session ended normally with its own wrap-up (not a turn limit). No tool result in the transcript is an error or a permission denial. After the session, `git diff --stat` on the shaders folder and on `scripts/run-test.sh` printed nothing (checked by my main Claude session before the audit was committed).

## Tool calls, in order (paths shown relative to the working folder)

| Time (UTC) | Tool | What it did (the agent's own description, or the file) |
|---|---|---|
| 02:33:37 | update_plan | Plan: read, write MATERIALS.md, write the test, run it |
| 02:33:38 | Bash | Inspect repo layout and test runner |
| 02:33:41 | Bash | Read CHANGE-BRIEF 2026-11-01 revision |
| 02:33:44 | Read | `submission-a5/CHANGE-BRIEF.md` |
| 02:33:47 | Bash | Read both shaders and list resources |
| 02:33:50 | Bash | Read materials, import files and attribution |
| 02:33:54 | Bash | Read hint scene, crate imports, normal check |
| 02:34:22 | Bash | Read project settings and base scene lights |
| 02:34:23 | Grep | Search the project for the texture, shader and material names |
| 02:34:26 | Bash | Read base scene head/tail and test style |
| 02:34:35 | Bash | Check assignment Step 3/4 notes and prior logs |
| 02:34:38 | Read | `submission-a5/ASSIGNMENT.md` (the assignment text, Step 3–4) |
| 02:34:56 | Bash | See how existing test checks uniforms and hints |
| 02:34:58 | Bash | Read existing test entry and helpers |
| 02:35:02 | Bash | Read A5 agent CLAUDE.md with headless facts |
| 02:36:05 | Bash | Check language pattern of A5 working docs |
| 02:36:41 | update_plan | — |
| 02:38:09 | Write | `project-survival-shooting/tests/test_materials.gd` |
| 02:38:13 | Bash | Run material test headlessly at 60 fps (`./scripts/run-test.sh test_materials.gd 60`) |
| 02:38:50 | Bash | Fix range compare, pin formats, rerun test |
| 02:39:01 | Read | `project-survival-shooting/tests/test_materials.gd` |
| 02:39:05 | Edit | `project-survival-shooting/tests/test_materials.gd` |
| 02:39:41 | update_plan | — |
| 02:40:48 | Write | `project-survival-shooting/MATERIALS.md` |
| 02:40:54 | Bash | Final test run and check changed files |
| 02:41:02 | wrap_up | End of the session |

The agent wrote only the two files it was asked for. It changed its own test once after the first run: see its report below.

## The agent's final report (translated from Chinese; not edited otherwise)

> The audit is written and the test has run: 169 PASS, 0 FAIL at 60 fps, exit code 0. No `.gdshader`, material, scene or `.import` file was changed, and nothing was committed.
>
> **Two new files**
> - MATERIALS.md: one row per material, one row per sampler (with the import settings and the measured format after import), plus lights and environment, findings and attribution. Written in Chinese following the working folder's rules, to be translated on upload.
> - test_materials.gd: Chinese comments, sectioned by the project's rules. It checks: the sampler hints (read from the source text); each uniform's type, group and range from `get_shader_uniform_list(true)`; the shader defaults and the two constants (read from the source); which values the four materials store and which textures they bind; the 6 `.import` files (read with `ConfigFile`); Use External in both `.glb.import` files; after instancing `base.tscn` and `hint_experiment.tscn`, the materials actually on the surfaces, the lights and the environment; normal maps: decode the source files and print `curl_ratio` under both conventions.
>
> **Run result (excerpt; full log in `logs/test_materials_60fps.log`)**
> ```
>   PASS  crate_wear.gdshader: rust_albedo hints are source_color, filter_linear_mipmap, repeat_enable (...)
>   PASS  both crate materials reference the same shader (res://shaders/crate_wear.gdshader)
>   PASS  crate_long.glb.import: use_external/path uid://cedrurswxh5f2 resolves to res://assets/furniture/materials/crate_long_wear.tres (...)
>   PASS  base.tscn: crate_long paint-surface normals all axis-aligned (72 normals, 0 off-axis)
>   PASS  base.tscn: tonemap is Linear (got 0)
>   PASS  Metal041C_1K-PNG_Displacement.png: imported get_image() format is 0 (got 0)
>   INFO  curl_ratio Metal041C_1K-PNG_NormalGL.png directx=false: 0.1991
>   INFO  curl_ratio Metal041C_1K-PNG_NormalGL.png directx=true : 1.8009
>   INFO  curl_ratio Metal041C_1K-PNG_NormalDX.png directx=false: 1.8009
>   INFO  curl_ratio Metal041C_1K-PNG_NormalDX.png directx=true : 0.1991
> == ALL PASS: 0 failure(s) ==
> exit=0
> ```
>
> The first run had 1 FAIL, caused by the test itself, not the materials: the minimum of the `texture_scale` range, 0.1, reads back as the text `0.10000000149012` once stored as a 32-bit float, and I had compared it as text. After changing it to a numeric comparison, everything passes.
>
> **Main findings (evidence lines in section 4 of MATERIALS.md)**
> 1. Neither scene writes tonemap, exposure, glow or fog. Linear, exposure 1.0 and all-off are the `Environment` defaults. CHANGE-BRIEF line 239 says these values are "set". The runtime values are right, and the test pins them.
> 2. Roughness and NormalGL are imported but no material uses them yet; the Step 4 material that uses them does not exist yet.
> 3. Nobody reads the NormalDX import result. The normal-map check reads the source PNG, so it also cannot check NormalGL as imported (measured: imported as the two-channel `FORMAT_RGTC_RG`).
> 4. The shader never writes `METALLIC`, so the "silver metal scratches" of CHANGE-BRIEF line 158 will show as non-metal grey. The plan says nothing about metallic; this is yours to decide.
> 5. The two materials store only two values each; the other three use the shader defaults. The 0.85 and 0.1 stored by the small crate equal the defaults.
>
> Also checked and consistent with the plan: after import every normal points along an axis; Displacement is already 8-bit (`FORMAT_L8`) when the PNG is decoded; the wear is "rust in low places first".
>
> **What a headless test cannot prove**
> - The colours on screen: the hint experiment's 64/128/192 predictions, the look of the rust, the lighting must be judged from captures.
> - Whether the shader really compiles on D3D12.
> - Whether the GPU really decodes sRGB, and whether the sampler hints work on screen.
> - A curl near 0 only says there is a surface behind the map, not that it is the right one.
> - This run used the existing `.godot/` cache. The assignment's next step is to clear the cache, reimport and run again, and to do the mutation that deletes `source_color`.
>
> Please note when reviewing: the enum names in MATERIALS.md (`compress/mode` 2 = VRAM Compressed, `Image.Format` 17 = DXT1, 21 = RGTC_RG, and so on) were written from memory and not looked up in the engine this time; please check each one. The numbers themselves were all measured in this run.

The review that followed (enum names and format constants checked against the engine, the renderer evidence corrected, one unmeasured row deleted, finding 4 decided as a known limitation) is the separate commit after the unedited audit.
