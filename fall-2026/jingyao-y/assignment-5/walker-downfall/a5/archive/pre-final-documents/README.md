# Downfall — Assignment 2 (CSYE 7270): generated art, sound and music

**Author:** Yuan Jingya, with Claude Code assistance. **Engine:** Godot 4.7.2-stable (GL Compatibility), Windows 11.

**Project name:** `downfall-godot`, in the repository `coldfish432/GodotGame`. It does **not** start with `walker-`; the author kept the existing repository (see [SUBMISSION.md](SUBMISSION.md)).

**Started from:** the author's own earlier Downfall project (Unity prototype → Godot port). It did not start from walker-jumpman or Assignment 1.

## What the assignment slice demonstrates

The whole game is the playable slice:

- **Lappland's states:** idle, walk, three combo attacks, the sword wave and hurt, with 8-direction facing. All are swapped from generated sprite atlases.
- **Environments:** three generated field surfaces and prop groups, plus the generated Rhodes base.
- **Event sounds:** four generated warehouse event sounds on real `room_reveal.gd` signals. Two (lights on, lights off) are generated files; two (hatch, shelf) are counted but silent until generated.
- **Music:** a generated base loop and field loop, plus two stings with the predicted pause, death and extraction behaviour.
- **Mute:** a mute toggle.
- **Design docs:** [CONCEPT](CONCEPT.md), [STORYBOARD](STORYBOARD.md), [CHARACTER-SHEET](CHARACTER-SHEET.md), [CHANGE-BRIEF](CHANGE-BRIEF.md), [TEST-REPORT](TEST-REPORT.md), [FRICTIONAL](FRICTIONAL.md), [SOURCES](SOURCES.md) (asset log), [SUBMISSION](SUBMISSION.md). The design docs are retrospective, and they say so.

## Run

Open `project.godot` in Godot 4.7.2 and press F5 (main scene `game/main.tscn`), or run:

```powershell
& 'Godot_v4.7.2-stable_win64.exe' --path downfall-godot
```

## Controls

| Input | Action |
|---|---|
| Right-click | Move |
| Left-click | Attack (a full charge releases the sword wave) |
| Shift | Dodge |
| Q | Potion |
| E | Interact |
| I / C | Bag |
| R | Relics |
| M | Map |
| J | Contract |
| Esc | Pause / settings |

**Mute:** Esc → Settings (设置) → 静音 mutes all audio. Music and SFX have their own buses, but there is no separate toggle for each.

## Tests

```powershell
& 'downfall-godot	ests
un_all.ps1' -Visual
```

This includes `tests/test_audio.gd` (sound-trigger counts, loop points, pause/end behaviour) and `tests/test_relic_icons.gd`.

## Known limitations

- **Copyright:** the game uses the Arknights IP (character, setting, PRTS references), against the assignment's rights rule.
- **Design after generation:** the design came after much of the generation.
- **Character sheet:** 7 distinct poses, not 10.
- **Sounds:** the hatch and shelf sounds are not generated.
- **Mute:** there is no separate music/SFX mute.

See [TEST-REPORT.md](TEST-REPORT.md) §Honest limitations.

**Local-only files:** `../evidence/` and `music/` (raw MP3 downloads) live outside this repository; the docs say so where they reference them.

**Final film:** https://youtu.be/n6yPUyUQEaM · `claude-liam-downfall-gamedev.mp4` (4K, 6:23). The SHA-256 is in [SUBMISSION.md](SUBMISSION.md).

---

# Downfall · 外勤合同首版

设计依据：`策划案_v1_0.md`、`拉普兰德攻击动作与特效设计案.md` v3，以及 `敌人攻击动画与预警设计案.md` v2 的已拍板规则。实现三个首发地区；雷姆必拓和叙拉古仍属于后续扩展。

## 运行

用 Godot 4.7.2 打开 `project.godot`，按 F5 运行主场景 `game/main.tscn`，从罗德岛选择合同。

```powershell
& 'D:\CSYE 7370\Godot_v4.7.2-stable_win64.exe' --path 'D:\CSYE 7370\downfall-godot'
```

左键攻击目标、点地面走过去；右键闪避（可改键）；Q 药瓶；E 与附近装置/深入入口/撤离点交互；I 背包；B 将背包最后一件移入安全袋。

背包中点选物品，选择装备、转移或丢弃；点选空格可重新放置选中物品，不能旋转。三选一、背包及路线菜单暂停战斗。右上方地图：白点为角色，橙色强化，金色点金，蓝色深入，绿色撤离。

## 已接入

- 拉普兰德双剑三段连斩、幼狼之牙蓄力剑气、五方向70帧战斗动画及闪避残影。剑气仅随武器词缀获得，三次命中蓄满、下一刀释放；详见 `拉普兰德攻击实现记录.md`（含测试及截图路径）。

- 7 种普通敌人的四帧攻击与重新烘焙的待机帧；普通物理攻击不显示地面预警，靠姿势、武器朝向、闪点和各自音效读招。扇形劈砍、真实扑咬/突刺、单箭/三箭扇射、冰斧冲击和跟瞄后锁定的狙击已接入。见 `敌人攻击实现记录.md`。

- 罗德岛接单、仓库、装备准备、投保、交付、死亡回收、再次出发，仓库及资金持久化。
- 矿区、街区废墟、冻土林线的地形、敌人职责比例、掉落构成和专属物品不同。
- 三地使用连续地形围出半线性主路、收窄口、战斗空地和奖励岔路；矿区矿轨、街区折向道路、雪原谷道由同一地形轮廓约束画面、碰撞、导航和小地图。见 `地图场景改造.md`。
- 单向区段推进；三个风险与收益不同的去向；深入与撤离为不同地点。
- 局内藏品系统（`局内构筑与数值策划案_v1_0.md`）：94 件集成战略藏品，名字与原效果取自 PRTS，效果转译到本作并按量级调整数值；没有体系或套装加成。来源为强化装置、战斗缴获（首领必掉，精英 5%，普通敌人 0.8%）、密室藏品，每区段最多 3 件；三选一尽量跨三类藏品，按地区倾向加权，可花待交付报酬刷新。自带伤害的攻击效果（横扫、多道剑气、灼烧、爆裂、荆棘等）在 9 件特殊装备上（`game/special_gear.gd`，获取方式待定，暂为 5% 掉落）。
- 明日方舟量级数值：拉普兰德生命 2400 / 攻击 600 / 法术攻击 360 / 防御 200 / 法抗 10 / 攻速 100；物理伤害减防御、法术伤害按法抗（保底 10%），剑气为法术伤害，精英重击为法术攻击。装备效能换算成攻击、生命、防御、法攻，词缀扩展到攻击、法攻、防御、法抗、暴击。飘字与敌人血条显示实际伤害。
- 武器、防具、饰品；三档稀有度，最多两条随机词缀。双剑三段连斩、幼狼之牙剑气词缀、回血、药瓶、带前摇的三类敌人。
- 补给箱、强化装置和点金装置各有两名守卫：进入据点范围整组触发，远离后返回各自站位。**触发范围不作任何显示**——地面不画圈，小地图也不标，靠观察守卫和地形自己判断多近算近；可读危险的要求针对的是攻击前摇，不是哨兵的容忍距离。普通敌人需要距离和视线感知，追出出生区域或丢失目标后归位。见 `守卫与敌人感知.md`。
- 10×6 背包、2×2 安全袋，可在仓管台扩容到 12×8 与 3×3；点金可指定已装备或容器内装备；阵亡结算去重；保险真实随机成功/失败。
- 背包界面（`装备与背包界面调研.md` 第六节）：拖拽、对比差值提示、战力、稀有度边框、点金/保险/安全袋角标、价值与阵亡预览、自动整理、词缀三档与 Alt 范围、拾取过滤与 Alt 地面名称、仓库搜索与一键存回材料。
- 每个区段另有一份按深度写定的配置（`FieldCatalog.DEPTH_PROFILE`），在地区基准之上叠加敌人数、精英数与掉落加成；深度无上限，表按 6 循环，循环长度是固定撤离间隔的整数倍，因而每个撤离段都落在同一条写定的条目上。
- 机关密室：每段布置 4 个机关，全部触发后开启密室与三个封印宝箱。矿区由两名普通敌人守卫，两名全部击败才解封；城区、雪原仍是一名精英守卫。矿区所有精英名额暂时改成普通敌人，源石虫作为普通敌人成群出现。
- 战争迷雾只作用于小地图：没走过的地形不画，装置、密室、机关与撤离信标在靠近发现之前不出现在图上，发现后永久保留。3D 画面不做遮蔽或变暗，保持前摇动作、武器指向及精英危险区的可读性。每进入新区段重置。见 `game/field_fog.gd`。
- 警戒值随着深入和交战上升，直接显示敌方伤害增幅。没有经验等级或永久构筑成长。
- 9 个敌人像素造型、12 个场景物件和 3 种地面纹理；沿用已有拉普兰德八方向行走素材。见 `art/field/来源.md`。
- 场景采用统一像素地表、路缘碎屑和共用基座的物件组合：矿区矿岩与支架、街区残墙与店面、雪原树丛与冻岩。物件按地表网格落地，近景控制遮挡。见 `场景美术重构_v2.md`。
- 合成提示音、受击反馈、7 种敌人的专属短音效；精英保留红色危险圈。弩箭撞墙碎裂，高速弹使用连续碰撞检查。

## 首版调参及明确取舍

这些是实现参数，不修改策划案硬规则：固定撤离每 3 段一次，随机撤离每段 20%；保险每件 15 资金、回收率 60%；路线提高警戒 6/12/20。核心表在 `game/field_catalog.gd`。

原矿在安全袋内仍持续造成污染伤害；安全袋保护物品归属，不隔绝污染。作业内拾得的报酬仅撤离后入账。交付仓库物品换取资金。以上细则可在试玩后调整。

存档位于 Godot 的 `user://field_contract_v1.json`，写入时保留 `.bak`。中断游戏按阵亡处理最近一次物资快照：点金、安全袋、带入装备保险仍按同一规则结算，不恢复未完成区段。物资变动后保存，保险随机状态一并保存，已结算再次加载不重复回收。测试禁用正式存档，存档测试使用独立文件。

## 验证

2026-09-30 敌人攻击实现后，分批运行全部套件共 **357 项检查、0 失败**，其中
敌人专项 88 项；另生成 31 张引擎截图，并核对闪点实际渲染。汇总见上级
`evidence/enemy-validation.json`，详细范围及复现方式见 `敌人攻击实现记录.md`。

```powershell
& 'D:\CSYE 7370\downfall-godot\tests\run_all.ps1' -Visual
```

`test_v1.gd` 覆盖新规则和存档；movement/combat/relics/ai_driver 保留适用的旧回归；`test_ui_v1.gd` 在真实渲染窗口中向 Godot 输入系统发送鼠标和按键事件；`capture_v1.gd` 输出引擎截图到上级 `evidence`。旧的固定增益/共用出口/立即重开测试已归档为 `tests/legacy/*.gd.txt`，由 v1 套件替代。

`test_layout.gd` 检查三个地区各 20 个种子的可达性及守卫站位；`test_terrain.gd` 实际驱动角色从入口走到终点、敌人绕掩体追击、地形阻挡射线，并检查移除装饰后的道路功能。`test_guards.gd` 覆盖守卫整组触发、归位、再次触发和死亡清理，以及普通敌人的感知、遮挡、追击范围和取消攻击。`capture_terrain.gd` 输出正常镜头道路、战斗区、俯视总览和纯地形截图；`capture_guards.gd` 输出驻防、警戒、返回和归位截图。2026-09-27 回归合计 172 项检查通过，日志在上级 `evidence/guards-regression.log`。

测试不等于真人体验验收。普通敌人使用侧面四帧攻击，反向水平翻转；精英仍沿用原有造型及预警。地图仍是程序生成原型，数值、长期重复游玩和真人体验目标需要试玩调优。后续扩展两地未开放。
