# CHANGE-BRIEF.md — Assignment 5: burning-bottle fire shader

## What the code does today (facts, checked 2026-10-30)

- 燃烧瓶投掷者 (`thrower`) lobs a bottle; its fire lasts `fire_time` 3.0 s
  (`game/enemy_attacks.gd:34`), 0 when the thrower is silenced
  (`entities/enemy.gd:1200`). Throwers spawn in the city region
  (`game/enemy_attacks.gd:163`).
- The bottle lands after 0.6 s (`entities/molotov.gd:8`) and calls
  `game.spawn_hazard(at, radius, 0.0, fire_time, …)` (`entities/molotov.gd:67`,
  `game/game_manager.gd:794`): a `GroundHazard` with `fuse` 0 and `lasting` 3.0.
- `GroundHazard` counts `lasting` down by the physics delta in
  `_physics_process`, only while `game.simulation_active()` is true
  (`entities/ground_hazard.gd:62`, `game/game_manager.gd:386`), hits every
  0.5 s, and frees itself when `lasting` reaches 0.
- The fire on the ground today is a `Decal` with a code-made circle texture
  (`entities/ground_hazard.gd:31`). A Decal takes textures, not a shader, so
  it stays as the scorch, and the new flames go on a new mesh.
- The same class also draws the slug burst and a boss's last rite (`fuse` > 0,
  `lasting` 0: `entities/enemy.gd:1443`, `entities/boss.gd:347`). Those are
  not burning fires.
- Renderer: `project.godot` sets no `rendering_method`; the Windows driver is
  D3D12 (`project.godot:27`). The field's `Environment` is made in
  `game/game_manager.gd:6501` and sets no tonemap or glow there. Confirm in a
  running game before predicting pixels.

2026-10-30 运行核验补充：上面最后一条只描述初始化，不能推导进入城区后的设置。
`apply_scene_look(false)` 会换成 `field_environment()`，后者从
`base_environment()` 创建环境（`game/game_manager.gd` 的同名函数）。实际城区运行值为
`renderer=forward_plus`、`driver=d3d12`、`tonemap_mode=3`（ACES）、
`tonemap_exposure=1.0`，glow、fog、adjustment、SSAO、SSIL 均开启。
第 7 节记录了单独用于像素预测的临时校准设置和实测背景。

## The state

- What it communicates, and why the player needs it: 传达“这片地面仍会造成周期伤害，以及还剩多少燃烧时间”。玩家据此决定绕行还是等待；亮黄火焰逐渐转成暗红余烬并减弱，消失才表示这堆火的持续伤害结束。暗淡不表示已安全。
- Name of the state: `fire_patch_burning`，成立条件为 `fuse <= 0.0 && lasting > 0.0`。当前投掷瓶火堆生成即成立；虫子爆炸和 Boss last rite 的 `lasting == 0`，不属于该状态。
- Script and variable that hold it: `entities/ground_hazard.gd` 的 `fuse`、`lasting`；`game.simulation_active()` 决定倒计时是否推进。未来显示驱动在有效火堆生成、第一次物理倒计时之前缓存该实例的初始 `lasting` 为 `initial_lasting`，之后只读状态并写材质：`fire_remaining = clamp(lasting / initial_lasting, 0.0, 1.0)`。不硬编码分母 3.0，因此未来改变 `fire_time` 仍能归一化。初始值不大于 0 的危险区不创建火焰，也不做除法。

## Effect specification

### The shader

- Path: `res://shaders/burning_bottle_fire.gdshader`（本次只约定路径，不创建 shader）。
- `shader_type`: `spatial`，火焰是三维场景中 `MeshInstance3D` 的材质。
- `render_mode`: `unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled`。

`unshaded` 使火色不依赖灯光；`blend_add` 在线性空间把火光加到背景上；
`cull_disabled` 防止观察角度变化时面片背面消失；`depth_draw_never` 避免透明面片写深度；
`shadows_disabled` 和 `fog_disabled` 避免接收阴影、雾的衰减。
另外把 mesh 的 `cast_shadow` 设为 OFF（`shadows_disabled` 本身不禁止投影），
保留正常深度测试，让实体墙壁仍可遮挡火焰。

显示结构：每个有效火堆增加一个朝向相机的面片，宽 `2 * radius`、高 `1.6 * radius`，
底部在地面上方 0.04 世界单位；与原有 Decal 共存。无贴图采样、无 `sampler2D`。

| Uniform | Type | Hint | Default | Set by |
|---|---|---|---|---|
| fire_remaining | float | `hint_range(0.0, 1.0, 0.01)` | `1.0` | driver, from the state |
| hot_color | vec4 | `source_color` | `vec4(1.0, 1.0, 0.0, 1.0)` | material default（不改） |
| ember_color | vec4 | `source_color` | `vec4(1.0, 0.0, 0.0, 1.0)` | material default（不改） |
| intensity | float | `hint_range(0.0, 1.0, 0.01)` | `0.6` | material default（不改） |
| flicker_amount | float | `hint_range(0.0, 0.2, 0.01)` | `0.08` | material default；受控截图显式设 `0.0` |

数值 hint 用于检视器，不代替驱动中的 clamp。颜色的 RGB 按 `source_color` 的颜色语义处理，
alpha 不作 sRGB 解码；本方案两种默认颜色的 RGB 只有 0 和 1，解码前后数值相同。

### The colour line

```glsl
ALBEDO = mix(ember_color.rgb, hot_color.rgb, fire_remaining) * intensity;
```

后续 shader 必须逐字使用上面这条颜色语句。它给出线性火色；透明度另由形状和剩余比例决定。
为固定可计算的形状，约定中间量如下（这里只写数学定义，不是已实现的 shader）：

- `p = 2 * UV - 1`；先令 `p.x *= 1 + 1.5 * max(-p.y, 0)`，使顶部收窄。
- 再令 `p.x += flicker_amount * sin(8 * UV.y + 7 * TIME) * (1 - UV.y)`，使上部摆动
  （Godot 的 UV.y 在面片顶部为 0、底部为 1，所以用 `1 - UV.y` 让顶部摆幅最大、底部不动）。
- `shape = clamp(1 - dot(p, p), 0, 1)`；`flicker = 1 + flicker_amount * sin(11 * TIME)`。
- `ALPHA = clamp(shape * clamp(fire_remaining, 0, 1) * flicker, 0, 1)`。

颜色 uniform 的 alpha 不参与上述计算；截图只改 `flicker_amount=0`，不临时替换颜色那一行。

### Observable rules

| # | Rule | Value / answer |
|---|---|---|
| R1 | Uniform value when the state begins | 生成时立即为 `1.0`，不加点燃渐亮，避免已经有伤害却看不清。材质首次可见前完成赋值。 |
| R2 | Uniform value when the state ends | 正常倒计时跨过 0 的最后一次物理更新中，释放前读到 `0.0`；ALPHA 也为 0，随后节点及其显示子节点释放。最后一个实际显示的非零帧可以略早于该终止样本。 |
| R3 | Duration of any change, in seconds (tolerance: one frame period); same game time at 30, 60, 144 fps | 标准火堆在 3.0 游戏秒内由 1 线性降到 0；`t=1.5` 时为 0.5。无额外渐亮或结束后的渐灭。30/60/144 三档的时长容差分别为 ±0.033333/±0.016667/±0.006944 游戏秒，测试配置见下文。 |
| R4 | State begins again mid-transition: restart, extend or ignore | 对原实例为 ignore；新瓶落地生成新实例，从 1 开始。旧火不重启、不延长，重叠火堆各自计时；加法混合的画面叠亮属于预期。 |
| R5 | Scaled or unscaled time under `Engine.time_scale`; behaviour while paused | 跟随受 time_scale 缩放的物理 delta。time_scale=0.5/1/2 时约用 6/3/1.5 墙钟秒，仍为 3 游戏秒。`simulation_active()==false` 时 lasting 与 fire_remaining 冻结；普通菜单暂停时 TIME 仍走，允许火苗摆动、闪烁，但寿命颜色不推进。预测（未实测）：shader 的 TIME 是否随 `Engine.time_scale` 变慢或在 0 时停止，在 Use It 中实测后记录。 |
| R6 | Uniform value if the state ends before a transition finishes | 撤离、换层、清除火堆时立即随节点消失；不补播渐灭、不为结束动画延长危险区。释放前值可能仍为例如 0.7，释放后无“当前值”可读取。新实例重新缓存初始时长并从 1 开始。 |
| R7 | Several instances: how each gets its own value | 每堆火 `ShaderMaterial.new()`，共享 Shader 资源但不共享材质实例。A 在 t=0 出生、B 在 t=1.0 出生，在 t=1.5 时应分别为 0.5 和 5/6；同时检查材质实例 ID 不同。 |

物理时序约定：初始化在 hazard 首次倒计时之前完成；hazard 的物理更新先执行，
显示驱动随后读 `lasting` 并赋值（`process_physics_priority`，数值越大越后执行；
hazard/driver 为 0/10）。观察器按作业要求在 `_process()` 中采样，`process_priority=100`，
排在同一帧所有其他 `_process()` 之后；另在 `_physics_process()` 中以
`process_physics_priority=100` 记录终止样本，保证在 `queue_free()` 的延迟删除前取到。
这些是未来驱动和测试的验收约束，目前没有运行它们。

R3 的三档测试都经 `scripts/run-test.sh <test>.gd 30|60|144` 运行，即 `--fixed-fps` 固定渲染帧率，
`Engine.time_scale=1.0`，物理保持项目的 60 Hz，不改 `physics_ticks_per_second`，
测的就是发布配置。uniform 只在物理步更新，起点和终点都落在物理步上；`_process()`
观察器在每个物理步之后的第一帧看到变化，起止两端各晚不到一个渲染帧，所以测得的
时长与 3.0 游戏秒之差小于一个渲染帧周期，即 R3 的容差。中点按离散时刻采样，值另允许
一个物理步除以初始时长的误差（见下）。

### Boundaries

- 不改伤害公式、瓶子直接伤害、火焰 tick 伤害和敌我伤害规则；保留 `GroundHazard.TICK=0.5`、当前首 tick 时机、3.0 秒标准寿命和半径 1.3。
- 不改碰撞、移动、输入、敌人状态机、攻击前摇/恢复、瓶子 0.6 秒飞行、沉默导致 `fire_time=0` 的规则和现有测试期望值。
- 原有 Decal 的纹理、颜色、地面投射和生命周期保持原样，继续承担地面烧痕；新 mesh 只负责火苗。
- `lasting=0` 的虫子爆炸和 Boss 预警不创建火焰；已有 `Warning`、爆炸 VFX、其他对象和场景照明不改。
- 驱动只读 `fuse`、`lasting`、初始时长和暂停状态，不回写游戏状态，不触发伤害，不调用新的计时器决定危险区寿命。
- 受控截图只在一次性运行中复制 Environment 并关闭后处理，结束后恢复；不能把校准设置保存成游戏默认值。

### Evidence split

| Rule | Headless test or eyes | How |
|---|---|---|
| R1 | Headless test + eyes | 走真实 thrower 攻击 → Molotov 落地 → spawn_hazard 流程，观察初始 uniform=1；肉眼检查落地立即可见。 |
| R2 | Headless test + eyes | 晚执行的物理观察器记录释放前终止值为 0、节点随后不存在；肉眼检查火苗消失，不能用 headless 声称已经渲染透明。 |
| R3 | Headless test + eyes | 每档通过真实落瓶流程，以 delta 累计游戏秒，采样整条 1→0 曲线、1.5 秒中点和 3 秒终点；另录三种渲染帧率下的游戏画面。 |
| R4 | Headless test + eyes | 真实落两瓶，相隔 1 秒；核对旧实例出生时间、剩余值不被改写，新实例从 1 开始；肉眼看重叠区叠亮及一堆先灭。 |
| R5 | Headless test + eyes | 分支设 time_scale=0.5、1、2，核对墙钟/游戏秒；打开使 simulation_active 为假的菜单，跨 30 个物理步断言 lasting 和 uniform 不变，关闭后续算；另核对打开正在搜刮的 inventory 仍继续计时。肉眼确认普通暂停时摆动可以继续。 |
| R6 | Headless test + eyes | 剩余比例约 0.7 时通过清层/撤离流程销毁，等延迟删除后断言 hazard、mesh 不存在；新建下一堆读到 1。肉眼检查无悬空火焰残留。 |
| R7 | Headless test + eyes | 双实例材质 ID 不同，在共同采样时刻各读到独立比例；更改 A 的材质值不改变 B。肉眼检查各自熄灭。 |

数值误差：比例比较允许 `1e-5` 浮点误差；按离散时刻采样的中点另允许一物理步除以初始时长。
所有拟议测试、变异测试、火焰截图和影片均待 shader/驱动实现后执行。
颜色、形状、背景对比要用下面的预测表与有渲染器的截图核对，headless 的假渲染器不能证明这些。

## Controlled inputs and predicted values

- Lighting/tonemap for these captures, and how it is fixed: 已用 Godot 4.7.2 的真实 Forward+ / D3D12 运行城区，读取 `game.world_environment.environment`，结果见前文核验。用于计算时复制当前 Environment，显式设置 Linear（`tonemap_mode=0`）、exposure=1.0，关闭 glow、fog、volumetric fog、adjustment、SSAO、SSIL、SSR，并隐藏 outline pass；保留原场景灯光。火材质用 unshaded。退出恢复原 Environment，未修改生产脚本。
- Background colour(s) behind the flame: 2026-10-30 已截图测量，并非猜测。原生 1280×720 PNG，左上角为 (0,0)：A=(640,420) 的 RGB8 为 **(58,58,67)**；B=(704,420) 为 **(59,58,67)**。采样区域无 UI、无火焰，隐藏玩家及危险区以隔离底图。本底图用于面片的单独校准；完整实战火堆还含 Decal，需另拍实战图，不能直接套这组背景。
- Uniform values: `fire_remaining=1.0, 0.5, 0.0`；`hot_color`、`ember_color`、`intensity=0.6` 使用表中默认值；`flicker_amount=0.0`，消除 TIME 对形状和闪烁的影响。

可复现输入与证据（相对仓库根目录）：

- 测量脚本：`evidence/a5/change-brief-2026-10-30/measure_background.gd`；实际数值：同目录 `measurement.json`；原始日志：`capture.log`；无火底图：`city-background.png`。这些文件原本生成在仓库外的 `../evidence/change-brief-2026-10-30/`，复制进仓库后内容不变；脚本里的输出路径仍写死为原位置。
- `persist_sessions=false`，`fixed_map_seed=2026`，真实 `start_contract("city")`，打开 `capture` modal 冻结模拟。玩家定位到 `main_path[0]+(0,8)` 的可行走点，实际为 `(0,0.7,-14)`。
- camera.size=24；实际相机原点 `(0,16.70052,-23.99917)`，basis X=`(-1,0,0)`、Y=`(0,0.529999,0.847998)`、Z=`(0,0.847998,-0.529999)`。截图直接读取 root viewport，未缩放、未做图像调色。
- 后续校准面片朝向相机，投影为 256×256 像素，中心对齐像素中心 `(640.5,420.5)`；A 的 UV=(0.5,0.5)，B 的 UV=(0.75,0.5)。校准时将面片放在这两个地面像素前方，保持正常深度测试并确认未被遮挡。其余对象、相机和底图设置与测量一致。
- 校准输出预定命名 `fire-r1.png`、`fire-r05.png`、`fire-r0.png`；这些火焰图目前尚未生成。r=0 在专用校准夹具中保留面片来量像素；实战中节点会释放，两者都应恢复到对应底图值。

本次日志有 `user://` 日志和着色器缓存写入错误（包括场景加载调用栈），但已正常退出并保存 PNG 和测量 JSON；这次采样不能作为无错误运行或全游戏回归通过的证据。

| Pixel | r=1.0 | r=0.5 | r=0.0 |
|---|---|---|---|
| A：中心 UV=(0.5,0.5)，截图 (640,420)，shape=1 | (210,210,67) | (158,121,67) | (58,58,67) |
| B：UV=(0.75,0.5)，截图 (704,420)，shape=0.75 | (186,186,67) | (142,110,67) | (59,58,67) |

Working (by hand):

1. 8 位 sRGB 归一化：`58/255=0.227450980`，`59/255=0.231372549`，`67/255=0.262745098`。
2. 解码 `D(x)=x/12.92`（x≤0.04045），否则 `D(x)=((x+0.055)/1.055)^2.4`。例如 `D(58/255)=((0.227450980+0.055)/1.055)^2.4=0.042311411`。其余为 `D(59/255)=0.043735029`、`D(67/255)=0.056128490`。因此线性背景 A=`(0.042311411,0.042311411,0.056128490)`，B=`(0.043735029,0.042311411,0.056128490)`。
3. source_color 的两种默认值逐通道解码：`D(0)=0`、`D(1)=((1+0.055)/1.055)^2.4=1`；所以 ember=`(1,0,0)`、hot=`(1,1,0)`。颜色那一行为 `C(r)=[(1-r)*(1,0,0)+r*(1,1,0)]*0.6=(0.6,0.6*r,0)`。r=1/0.5/0 时分别为 `(0.6,0.6,0)`、`(0.6,0.3,0)`、`(0.6,0,0)`。
4. flicker_amount=0 时 flicker=1。A 有 p=(0,0)，shape=`1-0=1`；B 有 p=(0.5,0)，shape=`1-0.5²=0.75`，顶部收窄系数都是 1。故 `alpha_A=r`，`alpha_B=0.75*r`。
5. 加法合成 `O=min(Bg+C*alpha,1)`（逐通道）；下表六种输入均未超过 1。Linear tonemap、exposure=1 保持这些线性值。

| Pixel / r | C × alpha（线性） | Bg + C × alpha（线性） | 编码后 ×255，取整前 | 四舍五入 RGB8 |
|---|---|---|---|---|
| A / 1 | (0.6,0.6,0) | (0.642311411,0.642311411,0.056128490) | (209.685648,209.685648,67) | (210,210,67) |
| A / 0.5 | (0.3,0.15,0) | (0.342311411,0.192311411,0.056128490) | (158.083194,121.325982,67) | (158,121,67) |
| A / 0 | (0,0,0) | (0.042311411,0.042311411,0.056128490) | (58,58,67) | (58,58,67) |
| B / 1 | (0.45,0.45,0) | (0.493735029,0.492311411,0.056128490) | (186.459952,186.218886,67) | (186,186,67) |
| B / 0.5 | (0.225,0.1125,0) | (0.268735029,0.154811411,0.056128490) | (141.575536,109.629676,67) | (142,110,67) |
| B / 0 | (0,0,0) | (0.043735029,0.042311411,0.056128490) | (59,58,67) | (59,58,67) |

6. 输出编码为 `E(x)=12.92*x`（x≤0.0031308），否则 `E(x)=1.055*x^(1/2.4)-0.055`。例如 A/r=0.5 红通道：`255*(1.055*0.342311411^(1/2.4)-0.055)=158.083194→158`；绿通道同理为 `121.325982→121`。其余通道逐项代入，结果已列在表中。

未来截图允许每通道 ±2 个 8 位级别（底图量化、浮点和读回误差）；超过容差先复查渲染器、后处理、UV 对齐和混合方式，不事后修改预测冒充符合。

Contrast ratio against the background:

使用未取整的线性值，`L=0.2126R+0.7152G+0.0722B`。
中心背景 `Lbg=0.2126*0.042311411+0.7152*0.042311411+0.0722*0.056128490=0.043309004`。
火焰中心的合成亮度为 `Lout=Lbg+0.12756*r+0.42912*r²`：

| r | Lout | (Lout + 0.05) / (Lbg + 0.05) |
|---|---|---|
| 1 | 0.599989004 | 0.649989004 / 0.093309004 = **6.965984:1** |
| 0.5 | 0.214369004 | 0.264369004 / 0.093309004 = **2.833264:1** |
| 0 | 0.043309004 | 0.093309004 / 0.093309004 = **1:1** |

这组对比度只预测受控底图下的中心像素，不作为文字可读性合规结论，也不代表实战 ACES/glow 下的比值。

## Hint experiment predictions

3×1 PNG, greys 64, 128, 192; unshaded quads; Linear tonemap, exposure 1.0.

| Band | Stored | Quad with `source_color` | Quad without |
|---|---|---|---|
| 1 | 64 | 64 | 137 |
| 2 | 128 | 128 | 188 |
| 3 | 192 | 192 | 225 |

Working:

两个空间面片均设不透明、unshaded、ALBEDO=采样 RGB，使用同一个原始 3×1 PNG；
采样指定 `filter_nearest, repeat_disable`，无 mipmap，禁止有损压缩；在各 texel 中心测量。
仅颜色提示不同，使用 Forward+、Linear、exposure=1，关闭上一节列出的后处理。
以下每个灰度标量代表 RGB 三通道：

| Stored | 文件值 /255 | 有 source_color：采样→ALBEDO（D） | 输出 E(D) ×255 | 无 source_color：采样→ALBEDO | 输出 E(文件值/255) ×255 |
|---|---|---|---|---|---|
| 64 | 0.250980392 | ((0.250980392+0.055)/1.055)^2.4 = 0.051269458 | 0.250980392×255 = 64 | 0.250980392 | (1.055×0.250980392^(1/2.4)−0.055)×255 = 137.206602 → **137** |
| 128 | 0.501960784 | ((0.501960784+0.055)/1.055)^2.4 = 0.215860500 | 0.501960784×255 = 128 | 0.501960784 | (1.055×0.501960784^(1/2.4)−0.055)×255 = 187.844970 → **188** |
| 192 | 0.752941176 | ((0.752941176+0.055)/1.055)^2.4 = 0.527115126 | 0.752941176×255 = 192 | 0.752941176 | (1.055×0.752941176^(1/2.4)−0.055)×255 = 224.999862 → **225** |

有 hint 的输出也逐项用同一 E 公式，例如 `E(0.051269458)=1.055*0.051269458^(1/2.4)-0.055=0.250980392`。
无 hint 时没有前面的 D，线性输出又经过 E，因此明显变亮。此表为预测，提示实验还未实施。

Which quad shows the file's values unchanged, and why: **有 source_color 的四边形**。
它先把文件的 sRGB 解码为线性，显示前再编码回 sRGB，`E(D(x))=x`，两次变换抵消。
不能把未带 hint 的原始数值当作已经解码的线性颜色。
依据：[Godot Shading language — source_color](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#using-source-color)。

## Material plan (textured shader)

- Object, scene, and the lighting it is judged under: 计划在独立 `res://tests/material_review.tscn` 放置两块有 UV、tangent 的 `BoxMesh` 金属货箱面板，A/B 并排，尺寸和相机一致，之后才考虑接入基地货箱。评判光用一盏白色 DirectionalLight3D（rotation_degrees=(-35,-30,0)，energy=1.0）和固定中性环境光 Color(1,1,1)、energy=0.2；环境为 Linear、exposure=1，关闭 SSAO、SSIL、SSR、glow、fog、调色和 outline。法线/粗糙度校准时不换灯，避免把后处理误当成表面变化。该场景、shader、材质和贴图本次均只立计划。

游戏内放置：两份材质也放进游戏本身的 3D 场景，即罗德岛基地，用在基地里的两只货箱上
（`world/base_map.gd:90` 的 `crate` 模型），一只用 A、一只用 B，并排或同一房间内，
在基地原有灯光下作“In play”检查。Interface sweep、法线/粗糙度判定和并排对照截图仍在上面的
独立夹具里做，因为基地环境开着 SSAO、SSIL、glow 和雾（`base_environment()`），会和表面变化混淆。
导入贴图后先确认 crate 模型的 UV 能承接这套贴图；不合适时改用基地里其他有 UV 的箱体，
并在 Revisions 里记下换成了哪个对象。

计划 shader 路径 `res://shaders/cargo_panel.gdshader`，`shader_type spatial`，
不使用 unshaded，保留正常 PBR 光照以观察粗糙度与法线。图源统一选用
[Poly Haven — Rusty Metal Sheet](https://polyhaven.com/a/rusty_metal_sheet)，CC0，1K，
优先取 PNG 版本；下载时记录实际文件名与哈希。GL/DX 两份法线使用相同分辨率与文件格式。

| Texture | Role | Source | What its numbers mean | Colour or data | compress/mode | compress/normal_map | mipmaps/generate |
|---|---|---|---|---|---|---|---|
| `rusty_metal_sheet_diff_1k` | 漫反射/基色 | [材质页](https://polyhaven.com/a/rusty_metal_sheet)，Diffuse | 8 位 sRGB 编码表面颜色；不是线性数据 | colour；sampler 加 `source_color` | 0（Lossless） | 2（Disable） | true |
| `rusty_metal_sheet_rough_1k` | 粗糙度 | [材质页](https://polyhaven.com/a/rusty_metal_sheet)，Rough | 0 光滑、1 粗糙的线性标量，读取 R 通道 | data；不加 `source_color` | 0（Lossless） | 2（Disable） | true |
| `rusty_metal_sheet_nor_gl_1k` | 正式切线空间法线 | [材质页](https://polyhaven.com/a/rusty_metal_sheet)，Normal (OpenGL) | RGB 打包方向分量；OpenGL 的 +Y 绿色约定，用于 NORMAL_MAP | data；`hint_normal`，无 `source_color` | 2（VRAM Compressed） | 1（Enable） | true |
| `rusty_metal_sheet_nor_dx_1k` | 只供 curl 校准对照 | [材质页](https://polyhaven.com/a/rusty_metal_sheet)，Normal (DirectX) | 与 GL 绿色方向相反；同一位置应约为 Gdx=1−Ggl，不作为正式材质法线 | data；对照 sampler 用 `hint_normal`，无 `source_color` | 2（VRAM Compressed） | 1（Enable） | true |

表内是计划设置，不是假称已读取不存在的 `.import`。后续下载后逐张设定、重导入，
从实际 `.import` 的 `[params]` 回读 `compress/mode`、`compress/normal_map`、
`mipmaps/generate` 再确认；禁用会覆盖这些值的自动检测。
GL 正式导入 `process/normal_map_invert_y=false`；DX 反向对照也先保持 false，
仅在单独“修正 DX”分支切为 true，并重导入，预期匹配 GL。
法线压缩可能只保留 RG，shader 交给 NORMAL_MAP 的内置路径重建 Z，不能依赖压缩后的蓝通道。
依据：[Godot Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)。

| Uniform | Type | Hint | Range | Default | Group | Expected change across its range |
|---|---|---|---|---|---|---|
| uv_scale | float | `hint_range(0.25, 8.0, 0.25)` | 0.25–8.0 | `1.0` | Surface | 三张图用同一组 UV；数值越大重复越多，同一面板上的纹理细节越小，不能只缩放颜色图。 |
| tint_color | vec4 | `source_color` | RGB 分量 0–1 | `vec4(1.0, 1.0, 1.0, 1.0)` | Surface | 基色逐通道乘 tint.rgb；黑色趋黑、白色保留原基色，单通道增大对应色变强，alpha 不用于透明。 |
| roughness_scale | float | `hint_range(0.0, 2.0, 0.05)` | 0–2 | `1.0` | Response | `ROUGHNESS=clamp(texture_R*roughness_scale,0,1)`；0 为锐利反光，增大后高光变宽、变弱。 |
| normal_strength | float | `hint_range(0.0, 2.0, 0.05)` | 0–2 | `1.0` | Response | 设 NORMAL_MAP_DEPTH；0 为平面，1 为图源强度，2 加强凹凸光照，不移动轮廓。 |

对应 `group_uniforms Surface;` 和 `group_uniforms Response;`，声明完成后用
`group_uniforms;` 结束组。三张正式 sampler 单独命名为 `albedo_tex`、`roughness_tex`、
`normal_tex`，均用一致的 repeat/filter 设置；DX sampler 只在校准夹具中使用。
Interface sweep 对四个非贴图 uniform 分别截最小值、默认值、最大值，其他值固定。
颜色 sweep 用黑、白及单独 RGB 分量端点检查，不把颜色控件误当单一标量滑块。

- What differs between the two materials, and why: 两个独立 ShaderMaterial 共用 `cargo_panel.gdshader` 和同一套贴图。A=`cargo_panel_mild.tres`：uv_scale=1、tint_color=(1,1,1,1)、roughness_scale=0.65、normal_strength=0.35，表示较平整、较光亮的面板。B=`cargo_panel_weathered.tres`：uv_scale=1、tint_color=(0.8,0.7,0.6,1)、roughness_scale=1.35、normal_strength=1.2，表示更暗、更粗糙、凹凸更强的旧面板。至少三个参数不同，符合两材质要求；图源本来就有锈斑，A 不宣称是无锈新钢板。

## Predicted failure cases

| # | Failure | Check that catches it |
|---|---|---|
| F1 | 所有火堆误共用 ShaderMaterial，一堆火重置其他火的值 | R7 双实例 ID 与异龄比例断言，另外改单实例值并读取另一实例。 |
| F2 | 把虫子/Boss 的瞬时危险区也画成火，或零时长除法 | 分别走 slug/boss 真实创建路径并构造 fuse>0、lasting=0 边界，断言无火焰 mesh/驱动、原 Warning 仍在；沉默投掷者落瓶后无火堆。 |
| F3 | 按帧数计时造成不同物理频率下持续时间不同 | R3 三档真实流程、累计 delta 与中点/终点断言；180 帧版本会暴露为 6/3/1.25 秒。 |
| F4 | 忽略 time_scale 或菜单暂停，视觉寿命与伤害不一致 | R5 时间缩放分支与 simulation_active 假值分支，逐步比较 lasting/initial_lasting 和材质值。 |
| F5 | uniform 被改名但 set_shader_parameter 没有明显报错 | 从 Shader 的 get_shader_uniform_list() 断言存在 float fire_remaining，并读源码核对默认值；变异测试仅改 shader 中该名字，原驱动和测试不改，预期失败后恢复。 |
| F6 | 颜色图漏 source_color 或数据图误加 source_color | 材质静态测试逐 sampler 核对 hint；变异测试删除 albedo_tex 的 source_color，必须失败；提示实验实测应由 64/128/192 变为 137/188/225。 |
| F7 | 沿用实际城区 ACES/glow，却把 Linear 公式的偏差当 shader 错误 | 截图前记录运行 renderer、Environment、exposure、后处理；设置不符则判受控输入不成立，先重拍背景。 |
| F8 | DX 法线当作 GL 导致凹凸/绿色方向反转 | 同光照 curl 对照 GL、原始 DX、Invert Y 修正 DX，后者应接近 GL；检查正式材质绑定 _nor_gl。 |

## Questions

1. **Which renderer does `project.godot` name, and what does it rule out?** 文件没有显式写 rendering_method，只指定 Windows 的 `d3d12` 驱动（`project.godot:27`）；桌面缺省是 Forward+，本次运行也确认为 forward_plus/d3d12。D3D12 是图形驱动而不是第四种 renderer。作业列出的限制是：Decal 和 compute shader 需要 Forward+ 或 Mobile；VoxelGI、SDFGI、SSIL 在 Mobile 和 Compatibility 下不可用。Forward+ 不排除其中任何一项。这对本项目是实际约束：火堆的地面烧痕是 Decal（`entities/ground_hazard.gd:31`），基地环境开着 SSIL（`game/game_manager.gd:6550`，`base_environment()` 里的 `e.ssil_enabled = true`）。换成 Compatibility 会两样都失去，换成 Mobile 会失去 SSIL。颜色管线的预测也只在 Forward+/Mobile 下成立。依据：[Godot Overview of renderers](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)。
2. **What colour arrives in `fragment()` before you change it, and what would the tempting alternative give you?** 本例是 spatial，不存在 canvas_item 自动把默认纹理颜色乘入 COLOR 的语义。fragment 收到的 COLOR 是从 vertex 阶段传来的插值顶点颜色；普通 QuadMesh 未提供顶点色时为白色。直接 `ALBEDO=COLOR.rgb` 会得到白色自发亮面片（本例 unshaded），不会自动得到火焰或贴图颜色。`texture(albedo_tex,UV).rgb` 才是显式纹理采样，颜色 sampler 还需 source_color；无纹理火 shader 不使用它。依据：[Godot Spatial shaders — built-ins](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#built-ins)。
3. **Spatial: what does `ALBEDO` hold if you never write it, and what does `COLOR` hold?** ALBEDO 默认是白色 vec3(1.0)；它是输出，不是自动采好的颜色贴图。COLOR 是顶点颜色传入 fragment 的值；当前 QuadMesh 无自定义顶点色，所以为 vec4(1.0)。两者不自动等价，必须显式写 ALBEDO 才能使用所需的颜色。依据：同上 Spatial shaders 的 ALBEDO 与 COLOR 条目。
4. **How long would a frame-counting version last at 30, 60 and 144 fps?** 按 60 fps 的 3 秒定为 `N=3*60=180` 帧，若每渲染帧减 1，则 30 fps 为 `180/30=6.0 s`、60 fps 为 `180/60=3.0 s`、144 fps 为 `180/144=1.25 s`。若错误计数发生在物理回调，则应把分母换成物理频率，不能把显示 fps 当物理频率。
5. **Which resource holds the uniform's default, which its current value, and what happens if two objects share the material?** 默认声明存于 Shader 源码；ShaderMaterial 保存该材质的当前覆盖值，未覆盖时回退到 Shader 默认值。两个 mesh 共享同一个 ShaderMaterial 时，set_shader_parameter 改的是同一份覆盖值，两个对象一起改变；本计划 R7 共享 Shader、各自 new 材质，所以寿命比例独立。依据：[Godot ShaderMaterial](https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html)。
6. **Does `hint_range` clamp a value the driver sets from code? (Predict now.)** 预测不会；它约束检视器控件，不会自动替代码 clamp。实现后在独立校准材质上用代码设 fire_remaining=2.0，先停驱动覆盖，再断言 get_shader_parameter 返回 2.0，并截图对照。颜色那一行没有 clamp，mix 外插为 `(0.6,1.2,0)`；ALPHA 的显式 clamp 仍给 1，A 点预测 RGB8=(210,255,67)，区别于 r=1 的 (210,210,67)。这是越界实验，正常驱动仍把状态比例 clamp 到 [0,1]。现在是预测，尚未声称通过实测。依据：[Godot Shading language — Uniform hints](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-hints)。

## Revisions

- 2026-10-30：初次填写状态、接口、颜色语句、R1–R7、证据划分、全部像素/提示实验预测、材质计划、失败案例和六题答案。实测当前城区使用 ACES/glow 等效果，补充真实运行值及临时 Linear 校准背景，修正只看初始化代码会得到的推断。新增测量证据位于仓库外的 `../evidence/change-brief-2026-10-30/`；本次未创建任何作业 shader、驱动或测试。材质下载/导入、shader 实测和后续测试仍是后续实施阶段的工作。
- 2026-10-30（提交前审查，Claude Code 按学生要求直接修改）：摆动项改为乘 `(1 - UV.y)`，与“上部摆动”的说明一致（受控截图 flicker_amount=0，预测数字不受影响）；R5 中“time_scale=0 时 TIME 停止”改为待实测的预测；R3 改为经 `scripts/run-test.sh --fixed-fps 30/60/144`、物理保持 60 Hz 测量，不再改 `physics_ticks_per_second`，观察器改为 `_process()` 高优先级采样加物理回调终止样本；证据路径改为仓库内 `evidence/a5/change-brief-2026-10-30/` 的副本；第 1 题改为对照作业列出的限制并联系本项目的 Decal 与 SSIL；材质计划增加基地货箱的游戏内放置；文档链接由 latest 改为 stable。
- 2026-10-30（实现前修订 R3，学生决定，Claude Code 执笔）：原 R3 写“3.0 游戏秒内由 1 线性降到 0”。实算发现，`lasting = 3.0` 每个物理步减去 `1/60`（双精度）要减 181 次才 ≤ 0（第 180 次后余 `+5.6e-15`），所以现有游戏里一堆火实际持续 **181 个物理步 = 3.016667 游戏秒**。这是现有计时行为，不在本次修改范围内。R3 改为：火焰从生成时的 1.0 起，在 `lasting` 第一次 ≤ 0 的那个物理步读到 0.0；60 Hz 物理下为 181 步、3.016667 游戏秒，在 30、60、144 fps 下相同，时长容差为该档一个渲染帧周期（1/30、1/60、1/144 秒）；t = 1.5 游戏秒时仍为 0.5（另允许一个物理步除以初始时长的误差）；每一步都满足 `fire_remaining = clamp(lasting / initial_lasting, 0, 1)`。R5 的 time_scale 分支同理按“第一次 ≤ 0 的物理步”计（0.5 时 361 步、2 时 91 步），游戏秒累计约为 3.0 加不到一个缩放物理步。原 R3 文字保留在上方表中不改。
