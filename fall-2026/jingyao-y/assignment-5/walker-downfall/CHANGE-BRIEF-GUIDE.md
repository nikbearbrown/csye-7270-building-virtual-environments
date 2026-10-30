# CHANGE-BRIEF.md 填写指南（每个 TODO 要做什么）

> 由 Claude Code 写于 2026-10-30，给学生本人看。这里只讲“每一项要决定什么、
> 去哪里找依据、怎么算、容易错在哪”，不给答案：颜色那一行、规则取值、所有
> 预测数字和题目回答都由你自己写进 `CHANGE-BRIEF.md`。
> 填完、提交 `CHANGE-BRIEF.md` 之后，才开始写任何 shader，也才发第一条 prompt。

建议顺序：先填 1–3（状态、shader、颜色那一行），再填 4–6（规则、边界、证据），
然后做 7–8 的手算，最后填 9–11。第 9 节（贴图材质）可以先只填计划，贴图还没下载也没关系。

---

## 1. The state（状态）

**What it communicates, and why the player needs it**
- 写一两句：这堆火对玩家意味着什么。提示：火每 0.5 秒伤害一次，玩家要判断
  “现在能不能踩过去、还要等多久”。效果要传达的就是这个信息。
- 不要写成“让火好看”，要写成玩家据此做什么决定。

**Name of the state**
- 给状态起一个名字，后面规则、测试、影片都用这个名字，比如 “fire patch burning”。
- 要说清楚它的成立条件。代码里火堆燃烧阶段是 `fuse <= 0` 且 `lasting > 0`
  （`entities/ground_hazard.gd:62`）。虫子爆炸和 Boss 技能也用同一个类，但它们
  `lasting` 是 0，不算“燃烧中”，你的条件要把它们排除。

**Script and variable that hold it**
- 写 `entities/ground_hazard.gd` 的哪个变量。
- 决定一件事：uniform 是 0–1 的比例时，分母从哪来？`GroundHazard` 没有存
  “一开始烧多久”，只有不断减少的 `lasting`。可以规定驱动在火堆生成时记下初始值，
  也可以直接用常数 3.0（`game/enemy_attacks.gd:34`）。各有利弊：用常数，
  别的投掷者改了 `fire_time` 就会错。把你的选择写下来。

## 2. The shader（shader 本身）

**Path**
- 这个仓库本身就是 Godot 工程，所以作业里的 `godot/shaders/` 在这里对应
  `res://shaders/`（仓库根目录下的 `shaders/` 文件夹，现在还不存在）。起一个说明用途的文件名。

**shader_type**
- 火焰面片是 3D 场景里的 MeshInstance3D，所以只能是 `spatial`。写上选它的理由。

**render_mode**
逐个决定要不要，并写一句理由：
- `unshaded`：不受场景光照影响，ALBEDO 直接就是输出色。不用它的话，像素预测要把灯光也算进去，基本算不了。
- `blend_add`：颜色加在背景上，适合火和光，越叠越亮。不用的话是普通透明混合（`blend_mix`），两种混合的手算公式不同（见第 7 节）。
- `cull_disabled`：面片背面也画。面片如果始终正对相机可以不要。
- `depth_draw_never`：透明物体一般不写深度，免得挡住后面的火苗。
- `shadows_disabled`、`fog_disabled`：火不该被阴影或雾压暗。

## 3. Uniform 表

要求：至少两个 uniform，每个都要写类型、hint 和默认值；其中一个必须是驱动按状态设置的 float；不能有任何 `sampler2D`。

逐列怎么填：
- **Uniform**：名字。驱动和测试都要靠这个名字，起好就别改（第 2 步的改名变异测试就是测这个）。
- **Type**：`float`、`vec4` 等。
- **Hint**：浮点数用 `hint_range(最小, 最大)` 或 `hint_range(最小, 最大, 步长)`；
  颜色用 `source_color`。想清楚每个 hint 是只影响检视器，还是也会改变 shader 收到的值。
  `source_color` 属于后者：shader 拿到的是解码成线性之后的值。
- **Default**：默认值。headless 测试会从源码文本里读这个值，所以表里写的必须和你 shader 里写的完全一致。
- **Set by**：写 “driver, from the state”，或 “material default（不改）”。

可以考虑的 uniform 类型（选几个，名字自己起）：
- 驱动的 0–1 值（燃烧进度或剩余比例）；
- 两种颜色，比如刚点燃时的热色和快灭时的余烬色，都用 `source_color`；
- 闪烁幅度：截图时要能把它设成 0，否则 `TIME` 一直在变，同一个像素每帧都不同；
- 整体亮度或强度。

## 4. The colour line（颜色那一行）

- 写在 `fragment()` 里，**一条语句**，改变颜色（写 `ALBEDO`，或者在 `blend_add` 下写 `ALBEDO` 和 `ALPHA` 之一，取决于你怎么设计）。
- 它必须包含驱动的那个 uniform，否则状态不会影响颜色。
- 它必须能手算：只用 uniform、常数，以及你在同一个 shader 里先算好、并在第 7 节说清楚取值的中间量（比如火焰形状值）。`TIME` 可以出现在形状和闪烁里，但手算的像素要选在闪烁设成 0 时取值确定的位置。
- 常见的形式是 `mix(甲, 乙, 驱动值)`：驱动值为 0 时等于甲，为 1 时等于乙。用什么当甲和乙、要不要再乘一个形状或强度，由你决定。
- 写好后，shader 必须**逐字**用这一行。以后要改，先在本文件的 Revisions 里加一条带日期的修订，再改 shader。

## 5. Observable rules（R1–R7）

每条写一个可以测量的答案。代码里已知的事实见 `CHANGE-BRIEF.md` 开头。

- **R1 状态开始时的值**：火堆刚生成那一帧，uniform 是多少？想想是直接跳到某个值，还是有一个点燃的渐亮过程。如果有，写出渐亮用几秒。
- **R2 状态结束时的值**：`lasting` 降到 0 时火堆节点会被释放（`entities/ground_hazard.gd:78`），所以“结束时的值”指的是释放前最后一帧测到的值。写出你预期的数。
- **R3 时长与容差**：火烧 3.0 秒（游戏时间）。容差是一个帧周期：30 fps 是 1/30 秒，60 fps 是 1/60，144 fps 是 1/144。要写明三种帧率下测到的游戏时间都应该相同。如果有渐亮或渐灭，也要分别写出它们的秒数。
- **R4 中途再次触发**：同一个火堆不会被重新点燃，新扔的瓶子会生成**新的**火堆。所以对一个火堆来说答案是 restart、extend 还是 ignore？还要考虑两个火堆重叠时，各自的值会不会互相影响。
- **R5 时间缩放与暂停**：`lasting` 每个物理帧减去 delta，而物理 delta 会受 `Engine.time_scale` 影响，所以是缩放时间还是不缩放时间？打开菜单时 `simulation_active()` 为假，`lasting` 不减，uniform 会怎样？另外注意：`TIME` 在暂停时**照样走**，所以火苗还会跳，只是颜色不变。决定这样是否可以接受，并写下来。
- **R6 过渡没完成状态就结束了**：比如火还在渐亮时玩家撤离或换层，火堆被释放。写出这时会怎样（节点和材质一起消失，没有残留值），以及有没有可能出现“下一层的火一出生就带着上一层的值”。
- **R7 多个实例**：每个火堆怎么拿到自己的值。二选一：每个火堆 `new` 一个自己的 `ShaderMaterial`（或者 `duplicate()` 一份），或者 shader 里用 `instance uniform`，再用 `set_instance_shader_parameter()` 设值。写明选哪个，以及测试怎么证明两个火堆的值不同。

## 6. Boundaries 与 Evidence split

**Boundaries**：列出不能变的东西，越具体越好：
- 伤害数值、0.5 秒一跳的间隔、3 秒时长、火圈半径；
- 地上的 Decal（继续当烧痕，不改）；
- 虫子爆炸和 Boss 技能的预警圈（不能长出火苗）；
- 投掷者的攻击时序、瓶子飞行时间、所有现有测试的期望值；
- 驱动只读 `lasting`，不写任何游戏状态。

**Evidence split**：R1–R7 每条写“headless 测试”还是“肉眼”，以及怎么做：
- 能用数字验证的（值、时长、各实例独立、暂停冻结、时间缩放）→ headless：一个 `process_priority` 很高的节点每帧读取 uniform，在 30、60、144 fps 下各跑一次，驱动走真实流程（让投掷者真的扔瓶子）。
- 关于“看起来对不对”的（颜色、火苗形状、亮度、和背景的对比）→ 肉眼，要写明用哪张截图、跟哪张预测表对比。
- headless 用的是假的渲染器，什么都不画，所以任何关于画面的结论都不能写成 headless。

## 7. Controlled inputs and predicted values（手算像素）

**Lighting/tonemap**
- 用了 `unshaded` 就不受灯光影响，但输出仍要经过 tonemap。
- 现在野外的 Environment 是在 `game/game_manager.gd:6501` 里新建的，代码里没设 tonemap 和 glow，按 Godot 默认应该是 Linear、glow 关。但这只是读代码得出的推断：要在运行中的游戏里打印 `world_environment.environment.tonemap_mode` 和 `glow_enabled` 确认，并把你确认的方法写下来。
- 如果不是 Linear，就写明截图时怎么临时改成 Linear、曝光 1.0。

**Background**
- 火是叠在城区地面上的。先在火面片隐藏时截一张图，**量出**背景像素的值，再拿它来算。不要猜。

**Uniform values**
- 选三个驱动值，比如两端加中间。截图时闪烁幅度设成 0。

**Pixel 表**
- 选至少两个像素，而且要选在“形状值”能确定的位置：比如火焰正中形状值为 1 的地方，和光晕上你能用公式算出形状值的地方。写清楚每个像素在面片上的 UV 位置、在截图里的坐标。

**Working（手算步骤）**
1. 把 8 位值除以 255，得到 0–1 的 sRGB 值。
2. 用 `source_color` 的颜色 uniform，shader 收到的是**解码**后的线性值。
   解码公式：`x ≤ 0.04045` 时为 `x / 12.92`，否则为 `((x + 0.055) / 1.055)^2.4`。
   检视器里的颜色和你写在 shader 里的默认值都要这样换算。
3. 用你的颜色那一行在线性空间里算出火焰颜色。
4. 和背景合成（背景也先解码成线性值）：
   - `blend_add`：结果 = 背景 + 火焰颜色 × ALPHA，每个通道超过 1 的部分截掉；
   - `blend_mix`：结果 = 背景 × (1 − ALPHA) + 火焰颜色 × ALPHA。
5. Linear tonemap、曝光 1.0 时，0–1 之间的值保持不变。
6. 用作业给的 `encode()` 编码回 sRGB，乘 255，四舍五入，就是预测的 8 位值。
每一步都写出数字，评分要求“手算”，计算过程就是证据。

**Contrast ratio**（如果效果改变了和背景的对比度）
- 相对亮度 L = 0.2126 R + 0.7152 G + 0.0722 B，其中 R、G、B 用**线性**值。
- 对比度 = (较亮的 L + 0.05) / (较暗的 L + 0.05)。分别算出三个驱动值下火焰中心对背景的对比度。

## 8. Hint experiment predictions（提示实验预测）

- 每个色带都按同一条流程推：文件里的 8 位值 → 采样器读出来的值 → 写进 ALBEDO 的值 → 输出时编码 → 屏幕上显示的 8 位值。
- 带 `source_color` 的采样器：读出来的值是把文件值当 sRGB **解码**后的线性值。
- 不带 `source_color` 的采样器：读出来的就是文件值除以 255，不做任何转换。
- 输出时，引擎对每个结果都做一次 `encode()`。
- 两个四边形都用 `unshaded`，tonemap 是 Linear、曝光 1.0，所以中间没有其他变化。
- 三个色带 × 两个四边形，6 个数都要手算出来，并写出计算过程。
- “哪个四边形显示的值和文件一样”：看哪条路径上解码和编码正好抵消。
- 渲染器是 Forward+，这些预测成立。如果改用 Compatibility，要先测量再解释。

## 9. Material plan（第二个 shader：读贴图的材质）

**Object, scene, lighting**
- 选一个 3D 物件和所在场景，比如基地里的一个货箱或地板。写明在什么光照下评判：哪盏灯、环境光，以及评判法线和粗糙度贴图时要关掉 SSAO 之类会混淆的效果（基地环境开了 SSAO、SSIL、glow、雾，见 `game/game_manager.gd:6537`）。

**贴图表**，每张贴图一行：
- **Role**：颜色、粗糙度、法线，或者遮罩。
- **Source**：Poly Haven 的具体材质页面网址。法线贴图要写明用的是 `_nor_gl`（Godot 要的是 OpenGL 约定）。另外，校准 curl 检查时还需要同一材质的 `_nor_dx`。
- **What its numbers mean**：
  - 颜色贴图：sRGB 编码的颜色；
  - 粗糙度贴图：0 光滑到 1 粗糙，按线性存储；
  - 法线贴图：把 -1 到 1 的方向分量打包成 0 到 1，绿色通道的朝向取决于 GL 还是 DX 约定。
- **Colour or data**：只有颜色贴图加 `source_color`，其余都按数据读。法线贴图用 `hint_normal`。
- **Import settings**：三项都要明确设定，不要留在 Detect：
  - `compress/mode`：0 Lossless、1 Lossy、2 VRAM Compressed、3 VRAM Uncompressed、4 Basis Universal；
  - `compress/normal_map`：0 Detect、1 Enable、2 Disable；
  - `mipmaps/generate`：true 或 false。
  设完后重新导入，打开 `.import` 文件确认数值，再写进表里。这几个编号要以你那份 `.import` 文件和 Godot 4.7 的文档为准。

**Uniform 表**
- 至少 4 个**非贴图** uniform，每个都要有 hint 和默认值，分到至少两个 `group_uniforms` 组里。
- 每个写清楚：从最小值到最大值，画面上预期会怎么变。之后的 Interface sweep 就是逐条去验证这一列。
- 可以考虑的方向：UV 缩放、色调、粗糙度倍数、法线强度、遮罩阈值。

**两个材质的区别**
- 至少有两个值不同，或者用了不同的贴图。要写出**为什么**这样分，比如一个是新货箱、一个是锈蚀旧箱。

## 10. Predicted failure cases（至少 3 条）

每条写“会出什么错”和“用什么检查抓到”。可以从这些候选里挑，也可以自己想：
- 所有火堆共用一个材质，一堆火的颜色出现在每一堆火上 → 测试同时生成两个火堆，分别读值。
- 虫子爆炸或 Boss 技能的预警圈也长出了火苗 → 测试生成一个 `fuse` 大于 0、`lasting` 为 0 的危险区，断言它没有火焰节点。
- 用帧数而不是 delta 计时，导致 144 fps 下火变短 → 在三种帧率下测量游戏时间。
- `Engine.time_scale` 变了，时长也跟着变（或者该变的时候没变）→ 加一个改了 time_scale 的测试分支。
- uniform 被悄悄改了名，`set_shader_parameter` 不报错 → `get_shader_uniform_list()` 名字断言，再做改名变异测试。
- 数据贴图误加了 `source_color` → 材质测试从源码文本里读 hint，再做删除 `source_color` 的变异测试。

## 11. Questions（6 道题）

每题自己回答，并写出依据：
1. **渲染器**：看 `project.godot`。没有写 `rendering_method` 时，默认是什么？Godot 文档里写了每种渲染器分别不支持什么，对照作业给的那句话来答。
2. **fragment 开始时收到的颜色**：查 Godot 文档 “Spatial shaders” 页里 fragment 内置变量的默认值。这一题主要考 canvas_item 的 `COLOR` 和 `texture(TEXTURE, UV)` 的区别；你用的是 spatial，就说明 spatial 里对应的是什么。
3. **ALBEDO 不写时是什么，COLOR 是什么**：同一页文档。`COLOR` 来自哪里（顶点颜色）？你的 QuadMesh 有顶点颜色吗？
4. **按帧计数的版本能持续多久**：假设有人写成“烧 N 帧”，而 N 是按 60 fps 定的，那么 30 fps 和 144 fps 下各是几秒？自己算。
5. **默认值存在哪，当前值存在哪，两个物件共用材质会怎样**：默认值在 Shader 资源（源码）里，当前值在 ShaderMaterial 里。用你自己的话写，并联系 R7。
6. **hint_range 会不会截断代码设的值**：先写下你的预测。之后 Use It 时，用代码把它设成 2.0 截图，再回来对照，判断预测对不对。

---

## 填完之后的顺序

1. 提交 `CHANGE-BRIEF.md`（只有你填写的内容）。
2. 让 Claude Code 按 prompt-1 起草 `CLAUDE.md`，原样提交一次，审查修改后再单独提交一次。
3. 你手写第一个 shader，单独提交。
4. 让 Claude Code 写驱动和测试（先出计划，你批准后再动手）；之后做两次变异测试。
5. 第二个 shader、两个材质、提示实验、材质审计、`LANGUAGE-NOTES.md`，按作业顺序继续。
