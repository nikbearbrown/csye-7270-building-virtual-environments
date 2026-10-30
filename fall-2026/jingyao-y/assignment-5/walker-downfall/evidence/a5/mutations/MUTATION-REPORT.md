# Fire shader mutation checks — 2026-10-30

课程提交基准：`7e562a4`。本次未提交、未推送。

课程目录是提交切片，没有 `project.godot`；实际执行位置为
`D:/CSYE 7370/downfall-godot`。开始前核对课程切片与运行工程的 shader、
FireFlame、GroundHazard、新测试和包装脚本，五个文件的 SHA-256 全部一致。

执行人：两次 shader 变异和恢复都由学生本人手工改动 shader；agent 没有编辑
`shaders/` 下的任何文件，只负责跑测试、核对哈希和整理本报告。

四轮均通过未经修改的包装脚本运行，参数保持一致：

```bash
GODOT='D:/CSYE 7370/Godot_v4.7.2-stable_win64_console.exe' TEST_TIMEOUT=120 ./scripts/run-test.sh test_fire_shader.gd 60
```

| Run | 只对运行副本施加的临时改动 | 包装脚本退出码 | 测试结果 |
|---|---|---|---|
| baseline-before | 无 | 0 | 89 checks, 0 failures |
| missing-semicolon | 删除 ALBEDO 颜色语句末尾的一个分号 | 1 | 89 checks, 7 failures；`SHADER ERROR: Expected a ';'.` |
| renamed-uniform | 仅在 shader 内把声明和全部使用处的 `fire_remaining` 改为 `fire_remaining_mutated` | 1 | 89 checks, 5 failures；uniform 名称断言等失败 |
| baseline-restored | 恢复原始字节 | 0 | 89 checks, 0 failures |

改名变异没有 SHADER ERROR 或 SCRIPT ERROR：语法仍有效，uniform 列表报告
`fire_remaining_mutated`，测试报告 `FAIL uniform fire_remaining exists`。
驱动、测试未改名。这证明接口断言能捕获未知参数名仍可被材质存取的情况。
两种变异均完整跑到测试结果行，并非依靠超时作为成功证据。

每次变异后均在 finally 中恢复原 shader。最终 SHA-256：

```text
7b65af5605af47a0ffb7caf32c138974bade9137f37c15a6577e9d0aa74ba410
```

运行副本与课程切片的 shader 逐字节相同；运行副本的全部现有 `.gd` 测试、
驱动、GroundHazard 和包装脚本在本次操作前后的哈希一致。
逐文件哈希及退出码见 `summary.json`。四份同名 `.log` 保留真实包装脚本输出；
两份 `.diff` 记录精确变异；`shader.original.txt` 保留原始字节。

最初一次沙箱内尝试无法启动 Git Bash：创建 signal pipe 被拒绝（Win32 error 5，
进程退出码 3221225794）。这不是 shader 测试结果；那次启动失败记录单独保存在
`sandbox-launch-failure/`。获准在沙箱外执行后，才得到上表的有效结果。

## R1 核查意见

认可区分“生成物理步”与“第一次帧观察器采样”的解释，但应追加带日期的 brief 修订，
不能把宽容差说成原文已经明确允许。建议修订文字：

> R1 的生成时值仍严格为 1.0；在 time_scale=1、60 Hz 物理下，第一次
> `_process()` 观察器采样之前可能已运行后续物理步，允许该采样值与 1.0 的差
> 不超过 `(1 / 渲染帧率) / initial_lasting` 加浮点误差。30 fps 的既有日志为
> 0.994444，对应 `1 - (1/60)/3`。该容差不放宽生成物理步的 1.0 断言。

这里核查了已有 30 fps 日志和测试代码；本次新跑的四轮都是 60 fps。
当前测试标签称“first frame it is drawn”，但 headless 只能证明 `_process()`
采样值，不能证明 GPU 首次实际显示的像素。视觉首帧仍需有渲染器的截图或影片。
本次未修改 brief；以上文字供后续修订使用。

这两项变异检查不证明火焰颜色、形状、亮度、首个实际显示帧或全游戏回归通过。
未重复运行 73 个旧测试。
