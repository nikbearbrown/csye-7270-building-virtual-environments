# LANGUAGE-NOTES — A5

核对日期：2026-10-30。行号以当前工作区文件为准；后续改动文件后应重新核对。
八题的代码与现有实验记录已核对。编辑器生成文件及其行号对照尚未完成，Step 4 尚未全部完成。

## A. StandardMaterial3D 生成文件的行号

`shaders/standard_generated.gdshader` 当前不存在。Windows 控制连接返回
`Computer Use native pipe is unavailable`，因此没有执行编辑器里的 Make Unique、
Convert to ShaderMaterial、Save As，也没有创建或保存临时场景。

必须在实际导出后补齐以下对照；目前没有生成文件可以支持这些行号或 uniform 名称：

| 生成文件中需要定位的内容 | 当前状态 |
|---|---|
| shader_type、render_mode | 尚无生成源码可引用 |
| 检视器 Albedo 颜色所对应的 uniform | 尚无生成源码可引用 |
| 检视器法线强度所对应的 uniform | 尚无生成源码可引用 |
| albedo sampler 及其提示 | 尚无生成源码可引用 |
| normal sampler 及其提示 | 尚无生成源码可引用 |
| ALBEDO、ROUGHNESS、NORMAL_MAP 赋值 | 尚无生成源码可引用 |

导出后还应核对：解析是否成功；游戏资源是否引用了它；三张正式贴图的 `.import`
是否与导出前逐字节一致。当前未运行编辑器，不能把这些写成已经通过。

## B. 八个问题

### 1. shader_type 决定了什么？

它选择 shader 所属的渲染接口，决定可以使用哪些处理函数、内置变量和 render mode。
三个文件第 1 行都是 `shader_type spatial;`，因此面向三维表面，可在 fragment 中写
ALBEDO、ROUGHNESS 等表面输出。它不等于选择 Forward+ 或 D3D12，后两者属于工程渲染器与驱动。

代码：`shaders/burning_bottle_fire.gdshader:1`、`shaders/cargo_panel.gdshader:1`、
`shaders/hint_experiment.gdshader:1`。
依据：[Godot Introduction to shaders — Shader types](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shader-types)。

### 2. 写了哪些处理函数，各在什么时候运行？颜色那一行挪到 vertex() 会怎样？

三个文件都只自定义 fragment()：火焰第 10 行、cargo 第 16 行、hint 第 8 行。
它在光栅化后的片元上计算；片元带有从顶点阶段插值得到的 UV。不是一整个物体只运行一次，
也不能把它的次数简单等同于 CPU 帧数。vertex() 则处理网格顶点；未自定义的阶段由引擎完成。

火焰第 17 行直接写的是 fragment 阶段的 ALBEDO 输出。把整条赋值原样放入 vertex()
会使用该阶段不可用的输出，不能这样搬。如果只是先在 vertex() 计算一个自定义颜色，
再用 varying 传给 fragment()，语法上可以另行实现。这里的 mix 表达式只依赖 uniform，
同一物体各顶点算出的颜色相同，因此仅把这部分计算提前并不会自然产生渐变。
但依赖 UV 的火焰形状若改成只在少数顶点计算，再插值到片元，就不能保持原来的非线性轮廓。

代码：`shaders/burning_bottle_fire.gdshader:10`、`:11`、`:14`、`:17`；
`shaders/cargo_panel.gdshader:16`；`shaders/hint_experiment.gdshader:8`。
依据：[Godot Introduction to shaders — Processor functions](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shaders-in-godot)。

### 3. 读了哪三个内置变量、写了哪两个？哪些是只读的？

按实际源码，三份 shader 只显式读取了两种不同的内置变量：UV 和 TIME。
题目提示的火焰第 11、13、15 行是三个读取位置，不是三种变量：

| 代码位置 | 读取内容 | 在当前阶段能否改写 |
|---|---|---|
| `shaders/burning_bottle_fire.gdshader:11` | UV | fragment 的输入，只读 |
| `shaders/burning_bottle_fire.gdshader:13` | UV、TIME | 都只读 |
| `shaders/burning_bottle_fire.gdshader:15` | TIME | 全局时间输入，只读 |

火焰明确写出的两个内置输出是 ALBEDO（第 17 行）和 ALPHA（第 18 行）。
cargo 还写 ROUGHNESS（第 19 行）、NORMAL_MAP（第 20 行）、NORMAL_MAP_DEPTH（第 21 行）。
这些是片元阶段的输出，不是对输入 UV/TIME 的修改。fire_remaining、tint_color 等是自己声明的
uniform，不属于内置变量；局部变量 p、shape 也不属于内置变量。

代码：`shaders/burning_bottle_fire.gdshader:17`、`:18`；
`shaders/cargo_panel.gdshader:19`、`:20`、`:21`。
依据：[Godot Spatial shaders — Built-ins](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#built-ins)。

### 4. 每种提示只影响检视器，还是也改变 shader 收到的值？

| 提示 | 当前代码 | 作用 |
|---|---|---|
| source_color | `shaders/hint_experiment.gdshader:4`；`shaders/cargo_panel.gdshader:3`、`:9` | 颜色 uniform 对应颜色控件；颜色 sampler 使用 sRGB 颜色语义，在本实验的 Forward+ 路径解码为线性颜色，实际影响采样值。 |
| hint_range | `shaders/cargo_panel.gdshader:8`、`:12`、`:13` | 给检视器提供范围和步长；不会替代码赋值执行 clamp。 |
| hint_normal | `shaders/cargo_panel.gdshader:5` | 标记法线贴图用途，可参与引擎的法线纹理处理；不把它当 sRGB 颜色解码，也不自动把 DX 的 Y 方向变成 GL。向 NORMAL_MAP 写入编码值后，内置法线路径负责解释和重建。 |
| filter_nearest / filter_linear_mipmap | `shaders/hint_experiment.gdshader:4`、`:5`；`shaders/cargo_panel.gdshader:3` | 改变 GPU 的纹理过滤；前者取最近 texel，后者线性过滤并使用 mipmap。不是单纯更换检视器控件。 |
| repeat_disable / repeat_enable | 同上 | 改变超出 0–1 的 UV 的采样寻址；本实验禁用重复，cargo 开启重复以支持 uv_scale>1。 |

现有真实渲染记录为 `evidence/a5/hint-experiment/measurement.json`：
Godot 4.7.2、Forward+、D3D12，适配器 AMD Radeon(TM) 610M；Linear、exposure=1，记录中的后处理关闭。

| 文件灰度 | 带 source_color：预测 / 实测 RGB | 无 source_color：预测 / 实测 RGB |
|---|---|---|
| 64 | 64 / (64,64,64) | 137 / (137,137,137) |
| 128 | 128 / (128,128,128) | 188 / (188,188,188) |
| 192 | 192 / (192,192,192) | 225 / (225,225,225) |

六处记录的 within_2 均为 true，而且中心样本恰好等于预测。
已查看同目录 hint-experiment.png：下排无提示路径比上排明显更亮。
具体 RGB 数值取自测量记录，不是靠肉眼估出的；本次没有重跑捕获脚本。
带提示路径先解码、输出时再编码，恢复原灰度；原值路径少了解码，直接编码显示后变亮。

依据：[Godot Shading language — Uniform hints](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-hints)。

### 5. hint_range 会不会 clamp 代码设的值？

不会。`logs/a5_probe_headless_60fps.log:9` 的实际记录是
`FACT hint_range value set 2.0 from code, read back: 2.0`。
这证明材质参数存取没有因 hint_range 把 2.0 截为 1.0；headless 记录不能证明 GPU 显示的颜色。

火焰第 4 行虽然提示范围是 0–1，但第 17 行 mix 没有 clamp；第 18 行的 alpha 计算则显式 clamp。
正常驱动另外在 `entities/fire_flame.gd:43` 对状态比例显式 clamp。
因此“代码设 2.0 的材质读回值”和“某条 shader 表达式如何处理 2.0”是两个问题。
brief 第 6 题对有渲染器实验的预测仍是中心 A=(210,255,67)，该火焰越界截图尚未核验，不能写成实测。

代码：`shaders/burning_bottle_fire.gdshader:4`、`:17`、`:18`。

### 6. 生成的 shader 哪一行让 albedo 按颜色采样、法线按数据采样？自己的 shader 对应哪行？

生成文件尚未导出，无法给出其中的实际 sampler 名称和行号；这个问题的生成文件部分尚未完成。

当前 cargo 对应的代码可以确定：第 3 行 albedo_tex 带 source_color；第 5 行 normal_tex 带
hint_normal 且没有 source_color。第 18 行把颜色样本乘 tint_color.rgb 后写入 ALBEDO；
第 20 行把编码后的法线样本原样交给 NORMAL_MAP，不手动做 `*2-1`，也不直接写 NORMAL。
生成文件导出后应逐条对照这些用途，而不是假定两个文件会使用相同的 uniform 名称。

代码：`shaders/cargo_panel.gdshader:3`、`:5`、`:18`、`:20`。

### 7. 为什么 fragment() 读不到相邻像素正在算的值？游戏状态怎么传进来？

每个片元调用有自己的局部计算，不能依赖相邻调用谁先结束，也没有在此 shader 中声明
可读取相邻调用当前 ALBEDO 的共享存储。texture() 能读取已提供的纹理输入，不等于读取
旁边片元正在写的结果。需要邻域效果时，应明确安排一个先产出纹理、后采样的渲染步骤。

游戏状态由 CPU 上的驱动通过材质 uniform 传入。火焰第 4 行声明 fire_remaining，
第 17、18 行使用它。`entities/fire_flame.gd:24` 缓存初始 lasting，
第 34 行为每堆火 new 一个材质，第 36 行先写 1.0，第 43 行在物理更新后调用
set_shader_parameter，把 clamped lasting/initial_lasting 写进去；第 42 行在暂停时跳过更新。
各堆火共享 Shader 源码，各自持有材质值，shader 不反过来修改伤害或寿命。

代码：`shaders/burning_bottle_fire.gdshader:4`、`:17`、`:18`。
依据：[Godot Introduction to shaders — Parallel execution](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html)。

### 8. Godot 着色语言提供了哪两样普通 GLSL 没有或需要自己接起来的东西？

第一样是材质输入和颜色语义的直接绑定：在 cargo 第 3 行写 source_color，便能让引擎按颜色纹理
处理该 sampler；提示实验第 4、5 行及第 9 行用相同 PNG 展示了有无该提示的实际差别。
普通 GLSL 应用也能通过 sRGB 纹理格式等方式实现这种采样，但需要应用侧设置资源格式与绑定，
不是普通 GLSL 自带名为 source_color 的 uniform 提示。

第二样是与引擎检视器直接相连的参数界面：cargo 第 7、11、14 行的 group_uniforms
建立并关闭 Surface/Response 分组，第 8、12、13 行的 hint_range 给出控件范围和步长。
GLSL uniform 声明本身不会自动给应用创建这些分组和滑块；应用需要另写编辑器界面。

另一个本例使用的引擎输入是火焰第 13、15 行的 TIME。普通 GLSL 没有一个自动随游戏运行的
标准 TIME 变量；应用通常自行提供时间 uniform。这里不据此断言该版本 TIME 与 time_scale
的实际关系，R5 的有渲染器测量仍应单独记录。

代码：`shaders/cargo_panel.gdshader:3`、`:7`、`:8`、`:11`、`:12`、`:13`、`:14`；
`shaders/hint_experiment.gdshader:4`、`:5`、`:9`；`shaders/burning_bottle_fire.gdshader:13`。
依据：[Godot Shading language — Uniform groups](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-groups)。
