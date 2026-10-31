# LANGUAGE-NOTES — A5

2026-10-30

这里记录我对这几个 shader 的理解，以及能从代码和实验结果里找到的依据。行号都是按现在的文件写的，后面如果改了代码，还需要重新核对。火焰越界值的截图和 TIME/time_scale 的实测还没做，留到 Use It 阶段。

## A. StandardMaterial3D 生成文件的行号

这一步我用了 Godot 4.7.2，渲染器是 Forward+，驱动是 D3D12。没有逐个点击界面，而是用引擎脚本建了临时的 Node3D、MeshInstance3D 和 BoxMesh，给 StandardMaterial3D 绑上 albedo、roughness 和 GL normal 三张图，再打开 normal_enabled。

接着通过 EditorResourcePicker 调用编辑器本身的 Make Unique 和 Convert to ShaderMaterial，最后用 ResourceSaver.save 把生成的 Shader 存成 `shaders/standard_generated.gdshader`。临时场景没保存，原来的三个 shader 也没改。

文件共 48 行，SHA-256 为
`ca1c191c44fb614ae64a258fce3efbc13b77fdc82f480e98ac4582e30805650d`。

| 我要找的内容 | 在生成文件里的位置 |
|---|---|
| shader_type | `shaders/standard_generated.gdshader:3`：`shader_type spatial;` |
| render_mode | `shaders/standard_generated.gdshader:4`：`blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx`；使用正常光照。 |
| 检视器 Albedo 颜色 | `shaders/standard_generated.gdshader:6`：`uniform vec4 albedo : source_color;` |
| 检视器法线强度 | `shaders/standard_generated.gdshader:20`：`uniform float normal_scale : hint_range(-16.0, 16.0);` |
| albedo sampler 及其提示 | `shaders/standard_generated.gdshader:7`：`texture_albedo : source_color, filter_linear_mipmap, repeat_enable` |
| normal sampler 及其提示 | `shaders/standard_generated.gdshader:19`：`texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable`；没有 source_color。 |
| roughness sampler 及其提示 | `shaders/standard_generated.gdshader:14`：`texture_roughness : hint_roughness_r, filter_linear_mipmap, repeat_enable`；没有 source_color。 |
| ALBEDO | `shaders/standard_generated.gdshader:35`：`ALBEDO = albedo.rgb * albedo_tex.rgb;` |
| ROUGHNESS | `shaders/standard_generated.gdshader:43`：`ROUGHNESS = roughness_tex * roughness;` |
| NORMAL_MAP | `shaders/standard_generated.gdshader:46`：`NORMAL_MAP = texture(texture_normal, base_uv).rgb;` |
| NORMAL_MAP_DEPTH | `shaders/standard_generated.gdshader:47`：`NORMAL_MAP_DEPTH = normal_scale;` |

对照之后，我发现生成版本在第 27–29 行还写了 vertex()，用来处理 UV1 的缩放和偏移，而前面三个 shader 都只写了 fragment()。

还有一点是，生成代码里的 albedo、normal_scale 等 uniform 没有直接写默认值。这次转换时的值放在 ShaderMaterial 里，albedo_color 是白色，normal_scale 是 1.0。只保存 Shader，不会连材质绑的贴图和参数值一起保存。这份生成文件只是用来对照，没有接进游戏。

我检查了文件的解析和一次单独的 BoxMesh 渲染：Forward+ / D3D12 下能运行，没有 SHADER ERROR 或 SCRIPT ERROR。游戏里的场景和材质没有引用它，三张正式贴图的 `.import` 和原来三个 shader 的 SHA-256 也都没变。记录放在 `evidence/a5/step4/`，包括 `generation.json`、`validation.json`、两份日志和导出脚本的文本副本。

不过编辑器退出时仍有扫描中止、设置文件写入和资源释放错误，所以这里只能说这份 shader 的检查通过了，不能说整个工程已经无错误运行。

## B. 八个问题

### 1. shader_type 决定了什么？

我的理解是，shader_type 先告诉 Godot 这份 shader 用在哪一类渲染里，也决定了我能写哪些处理函数、用哪些内置变量和 render mode。

这三个文件第 1 行都写了 `shader_type spatial;`，因为它们处理的是三维场景里的表面，所以能在 fragment() 里写 ALBEDO、ROUGHNESS 这些输出。这里的 spatial 和 Forward+、D3D12 不是一回事，后两项分别是工程的渲染器和驱动。

代码：`shaders/burning_bottle_fire.gdshader:1`、`shaders/cargo_panel.gdshader:1`、
`shaders/hint_experiment.gdshader:1`。
依据：[Godot Introduction to shaders — Shader types](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shader-types)。

### 2. 写了哪些处理函数，各在什么时候运行？颜色那一行挪到 vertex() 会怎样？

这三个 shader 都只写了 fragment()：火焰在第 10 行，cargo 在第 16 行，hint 在第 8 行。它处理的是光栅化之后的片元，拿到的 UV 已经经过顶点之间的插值。它不是每个物体只跑一次，运行次数也不能直接按 CPU 的帧数来算。vertex() 则是处理网格顶点的；我没写的阶段由引擎完成。

火焰第 17 行直接给 ALBEDO 赋值，而 ALBEDO 是 fragment 阶段的输出，所以不能把整行直接搬进 vertex()。如果想提前算颜色，需要在 vertex() 里存到自定义变量，再通过 varying 传给 fragment()。

不过这里也要分清颜色和形状。颜色那条 mix 只用到了 uniform，同一个物体上算出来都一样，所以单独把这个计算提前，不会自动产生颜色渐变。火焰形状则依赖 UV，如果只在几个顶点算形状，再让中间的片元插值，就会和现在逐片元算出来的轮廓不同。

代码：`shaders/burning_bottle_fire.gdshader:10`、`:11`、`:14`、`:17`；
`shaders/cargo_panel.gdshader:16`；`shaders/hint_experiment.gdshader:8`。
依据：[Godot Introduction to shaders — Processor functions](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html#shaders-in-godot)。

### 3. 读了哪三个内置变量、写了哪两个？哪些是只读的？

我按代码数了一遍，这三份 shader 实际只读取了两种内置变量：UV 和 TIME。题目提示里的第 11、13、15 行是三个读取位置，里面有重复使用同一个变量的情况：

| 代码位置 | 读取内容 | 在当前阶段能否改写 |
|---|---|---|
| `shaders/burning_bottle_fire.gdshader:11` | UV | fragment 的输入，只读 |
| `shaders/burning_bottle_fire.gdshader:13` | UV、TIME | 都只读 |
| `shaders/burning_bottle_fire.gdshader:15` | TIME | 全局时间输入，只读 |

火焰写的两个输出是 ALBEDO（第 17 行）和 ALPHA（第 18 行）。cargo 另外还写了 ROUGHNESS（第 19 行）、NORMAL_MAP（第 20 行）和 NORMAL_MAP_DEPTH（第 21 行）。这些是在设置片元的输出，没有改 UV 或 TIME。

fire_remaining 和 tint_color 是我声明的 uniform，不算内置变量；p、shape 只是函数里的局部变量，也不能算进去。

代码：`shaders/burning_bottle_fire.gdshader:17`、`:18`；
`shaders/cargo_panel.gdshader:19`、`:20`、`:21`。
依据：[Godot Spatial shaders — Built-ins](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html#built-ins)。

### 4. 每种提示只影响检视器，还是也改变 shader 收到的值？

| 提示 | 我用到的位置 | 我的理解 |
|---|---|---|
| source_color | `shaders/hint_experiment.gdshader:4`；`shaders/cargo_panel.gdshader:3`、`:9` | 颜色 uniform 对应颜色控件；颜色 sampler 使用 sRGB 颜色语义，在本实验的 Forward+ 路径解码为线性颜色，实际影响采样值。 |
| hint_range | `shaders/cargo_panel.gdshader:8`、`:12`、`:13` | 给检视器提供范围和步长；不会替代码赋值执行 clamp。 |
| hint_normal | `shaders/cargo_panel.gdshader:5` | 标记法线贴图用途，可参与引擎的法线纹理处理；不把它当 sRGB 颜色解码，也不自动把 DX 的 Y 方向变成 GL。向 NORMAL_MAP 写入编码值后，内置法线路径负责解释和重建。 |
| filter_nearest / filter_linear_mipmap | `shaders/hint_experiment.gdshader:4`、`:5`；`shaders/cargo_panel.gdshader:3` | 改变 GPU 的纹理过滤；前者取最近 texel，后者线性过滤并使用 mipmap。不是单纯更换检视器控件。 |
| repeat_disable / repeat_enable | 同上 | 改变超出 0–1 的 UV 的采样寻址；本实验禁用重复，cargo 开启重复以支持 uv_scale>1。 |

我对照了 `evidence/a5/hint-experiment/measurement.json` 里的真实渲染结果。这次记录用的是 Godot 4.7.2、Forward+、D3D12，显卡是 AMD Radeon(TM) 610M，tonemap 为 Linear、exposure 为 1，后处理关闭。

| 文件灰度 | 带 source_color：预测 / 实测 RGB | 无 source_color：预测 / 实测 RGB |
|---|---|---|
| 64 | 64 / (64,64,64) | 137 / (137,137,137) |
| 128 | 128 / (128,128,128) | 188 / (188,188,188) |
| 192 | 192 / (192,192,192) | 225 / (225,225,225) |

六个位置的 within_2 都是 true，中心像素的值也正好等于预测。我看了同目录的 hint-experiment.png，下排没有 source_color 的三个色块确实比上排亮。

表里的 RGB 是从测量记录里读的，不是我看截图估出来的，这次写笔记时也没有重新跑截图。我的理解是，带提示的路径先解码，再在输出时编码，所以回到了文件原来的灰度；不带提示的路径少了前面的解码，直接编码输出后就变亮了。

依据：[Godot Shading language — Uniform hints](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-hints)。

### 5. hint_range 会不会 clamp 代码设的值？

不会。我在 `logs/a5_probe_headless_60fps.log:9` 看到的记录是
`FACT hint_range value set 2.0 from code, read back: 2.0`。

设成 2.0，读回来还是 2.0，说明 hint_range 没有自动把材质参数截到 1.0。不过这个测试是 headless 的，只能说明参数的存取结果，不能说明屏幕上会显示什么颜色。

火焰第 4 行的提示范围虽然是 0–1，但第 17 行的 mix 没写 clamp，第 18 行算 alpha 时才明确写了 clamp。正常驱动也在 `entities/fire_flame.gd:43` 把状态比例限制在 0–1。

所以我需要分开看两件事：材质里能不能存下 2.0，以及 shader 拿到 2.0 后怎么算。brief 第 6 题预测中心 A 会显示 (210,255,67)，这张越界值截图还没核验，目前仍然只是预测。

代码：`shaders/burning_bottle_fire.gdshader:4`、`:17`、`:18`。

### 6. 生成的 shader 哪一行让 albedo 按颜色采样、法线按数据采样？自己的 shader 对应哪行？

我在生成文件第 7 行找到了 `texture_albedo`，它带 source_color，所以按颜色处理。第 19 行的 `texture_normal` 带的是 hint_roughness_normal，没有 source_color，所以不会把法线当 sRGB 颜色解码。第 34、35 行采样并组合 albedo，第 46 行把法线交给 NORMAL_MAP，第 47 行设置法线强度。

我的 cargo 对应的是第 3 行 albedo_tex 和第 5 行 normal_tex。前者有 source_color，后者有 hint_normal，没有 source_color。第 18 行把颜色样本乘 tint_color.rgb，再写进 ALBEDO；第 20 行把法线样本直接交给 NORMAL_MAP，没有自己写 `*2-1`，也没有直接写 NORMAL。

这里两个文件的法线提示名称并不一样：生成的是 hint_roughness_normal，cargo 用的是 hint_normal。对这道题来说，共同点是它们都没有把法线图标成 source_color。

代码：`shaders/standard_generated.gdshader:7`、`:19`、`:34`、`:35`、`:46`、`:47`；
`shaders/cargo_panel.gdshader:3`、`:5`、`:18`、`:20`。

### 7. 为什么 fragment() 读不到相邻像素正在算的值？游戏状态怎么传进来？

我的理解是，每个片元都在算自己的结果，不能假定旁边的片元已经算完，也没有一个变量可以直接读到它正在写的 ALBEDO。texture() 读的是提供给 shader 的纹理，不是旁边片元这一次计算的结果。如果要做需要周围像素的效果，就得先把结果画进纹理，再在后面的渲染步骤里采样。

游戏状态是从 CPU 这边通过 uniform 传进去的。火焰第 4 行声明了 fire_remaining，第 17、18 行用它控制颜色和 alpha。驱动 `entities/fire_flame.gd` 在第 24 行记下初始 lasting，第 34 行给每堆火建自己的材质，第 36 行先设成 1.0。之后第 43 行用 set_shader_parameter 写入 clamp 后的 lasting/initial_lasting；暂停时会在第 42 行跳过更新。

这样几堆火可以共用同一个 Shader，但各自保留自己的材质值。shader 只负责显示，不会回头改伤害和燃烧时间。

代码：`shaders/burning_bottle_fire.gdshader:4`、`:17`、`:18`。
依据：[Godot Introduction to shaders — Parallel execution](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html)。

### 8. Godot 着色语言提供了哪两样普通 GLSL 没有或需要自己接起来的东西？

我这次用得最直接的两样是颜色提示和检视器参数。

第一样是 source_color。cargo 第 3 行加上它之后，引擎就知道这个 sampler 读的是颜色图。提示实验的第 4、5 行和第 9 行也用同一张 PNG 测出了区别。普通 GLSL 应用当然也能做 sRGB 采样，但通常需要应用自己设置纹理格式和绑定，不是直接在 uniform 后面写一个 source_color 就能接好。

第二样是 group_uniforms 和 hint_range。cargo 第 7、11、14 行把参数分成 Surface 和 Response，第 8、12、13 行给滑块设置范围和步长。普通 GLSL 的 uniform 声明不会自动生成这些检视器控件，还需要应用自己写界面。

另外，火焰第 13、15 行用到的 TIME 也是 Godot 提供的。普通 GLSL 没有一个自动跟着游戏走的标准 TIME，一般需要应用自己传时间。但我这里还没有完成 TIME 和 time_scale 关系的真实渲染测试，这部分仍要按 R5 单独记录。

代码：`shaders/cargo_panel.gdshader:3`、`:7`、`:8`、`:11`、`:12`、`:13`、`:14`；
`shaders/hint_experiment.gdshader:4`、`:5`、`:9`；`shaders/burning_bottle_fire.gdshader:13`。
依据：[Godot Shading language — Uniform groups](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniform-groups)。


rg: D:\CSYE 7370\csye-7270-course\fall-2026\jingyao-y\assignment-5\walker-downfall\LANGUAGE-NOTES.md: 系统找不到指定的文件。 (os error 2)
LANGUAGE-NOTES.md:34:我检查了文件的解析和一次单独的 BoxMesh 渲染：Forward+ / D3D12 下能运行，没有 SHADER ERROR 或 SCRIPT ERROR。游戏里的场景和材质没有引用它，三张正式贴图的 `.import` 和原来三个 shader 的 SHA-256 也都没变。记录放在 `evidence/a5/step4/`，包括 `generation.json`、`validation.json`、两份日志和导出脚本的文本副本。
evidence/a5/step4\export_standard_material.gd.txt:5:const EVIDENCE := "res://evidence/a5/step4/"
evidence/a5/step4\export_standard_material.gd.txt:123:	var file := FileAccess.open(EVIDENCE + "generation.json", FileAccess.WRITE)
?? evidence/a5/step4/
Name                            Length
----                            ------
before-hashes.json                 734
export_standard_material.gd.txt   4694
export.log                        2969
generation.json                   2903
render-validation.log              813
validation.json                   1651

