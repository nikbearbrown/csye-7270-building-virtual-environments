Built the evidence without changing the flash implementation, `player.gd`, shader, or existing tests. Nothing was committed.

Added:

- [verify_flash_spec.gd](<scratch>/ch08/walker-jumpman-clawd/godot/tests/verify_flash_spec.gd)
- [flash_model.gd](<scratch>/ch08/walker-jumpman-clawd/godot/tests/flash_model.gd)
- [flash_bench.tscn](<scratch>/ch08/walker-jumpman-clawd/godot/tests/flash_bench.tscn)
- [flash_bench.gd](<scratch>/ch08/walker-jumpman-clawd/godot/tests/flash_bench.gd)
- [test_flash_bench.gd](<scratch>/ch08/walker-jumpman-clawd/godot/tests/test_flash_bench.gd)
- [BENCH.md](<scratch>/ch08/walker-jumpman-clawd/BENCH.md)
- Actual effort/results recorded in [FRICTIONAL.md](<scratch>/ch08/walker-jumpman-clawd/FRICTIONAL.md).

Timing results against HEAD:

```text
30 fps:
frames_in_failure=17
accumulated_game_time=0.566666666666667
first_flash=1.0
last_flash_before_retry=0.515151515151515
max_error=0.515151515151515
FAIL time-linear flash stays within tolerance
FAIL last failure frame flash <= 0.07
VERIFY_FLASH_SPEC failures=2
exit=1

60 fps:
frames_in_failure=34
accumulated_game_time=0.566666666666667
first_flash=1.0
last_flash_before_retry=0.0
max_error=0.0303030303030304
All checks PASS
VERIFY_FLASH_SPEC failures=0
exit=0

144 fps:
frames_in_failure=82
accumulated_game_time=0.570277777777777
first_flash=1.0
last_flash_before_retry=0.0
max_error=0.569191919191919
FAIL time-linear flash stays within tolerance
VERIFY_FLASH_SPEC failures=1
exit=1
```

The first failure-frame and first post-retry checks passed at all three rates.

CPU model output:

```text
FLASH_MODEL_COLORS:
{"body":{"0.0":"#dd775b","0.5":"#815653","1.0":"#25354a"},
 "eyes":{"0.0":"#000000","0.5":"#131b25","1.0":"#25354a"}}

body endpoints: PASS
eye endpoints: PASS
transparent alpha unchanged: PASS
FLASH_MODEL failures=0
```

Bench test output:

```text
Amount0 flash_amount=0.0: PASS
Amount05 flash_amount=0.5: PASS
Amount1 flash_amount=1.0: PASS
three distinct ShaderMaterials: PASS
uniform names ["flash_amount","flash_color"]: PASS
flash_amount type float: PASS
flash_color type Color: PASS
FLASH_BENCH_TEST failures=0
```

Regression tests also passed:

```text
WALKER TESTS: 25 checks / 0 failures
Keyboard: 9 checks / 0 failures
Clawd: 1950 checks / 0 failures
```

No `SHADER ERROR` appeared. Godot did emit local log-directory and macOS certificate warnings during headless runs; they did not affect the test results.