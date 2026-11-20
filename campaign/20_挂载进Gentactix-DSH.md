# 20 · 把安田讲堂挂进已安装的 Gentactix-DSH

日期：2026-11-20　目标：让「安田讲堂攻防战」出现在 `E:\Gentactix-DSH` 界面的**战役列表**里，和台儿庄那批并列，而不是只能单开 HTML。

## 一、结果

- 后端 `/api/missions`：20 → **21**，新增 `YS01-local-v1`（安田讲堂攻防战-1969.01.18至1969.01.19，profile=delay，30 分钟/回合，deadline 6 回合）。
- 后端 `/api/battles`：45 → **46**，新增「安田讲堂攻防战 1969.01.18至1969.01.19 · 建议 30分钟/回合」。
- 启动页「战役资料库 **46**」，列表末位即 #46 安田讲堂攻防战；选中后「初始态势」下拉里出现「可重放局部教学 · 迟滞」。
- 实测：建会话 → `/init`（红方 3 个编组、蓝方 3 个编组、turn 0 active）→ `/next`（turn 1，progress 1，report 正常）。

## 二、新增文件

| 路径 | 作用 |
|---|---|
| `data/yasuda/scenarios.json` | 编辑源（schema v2，与抗日战争/长征同构） |
| `data/yasuda/sources.json` | 来源登记 S1…S46 |
| `data/yasuda/{timeline,forces,figures,verification_gaps}.csv`、`INDEX.md` | 由渲染器生成 |
| `gentactix/yasuda_anchors.json` | 14 个地名锚点（含 uncertainty_km、source_url） |
| `corpus/安田讲堂攻防战-1969.01.18至1969.01.19.md` | 史料卡（30 KB，按 `##` 切片给 RAG） |
| `adjudication/安田讲堂攻防战-1969.01.18至1969.01.19.md` | 几何参数卡（geo-5 七参数） |
| `tools/render_yasuda.py` | 渲染器（复用 `tools/render_long_march.py` 的骨架，`--check` 可校验） |

## 三、改动的上游文件（4 处，都很小）

| 文件 | 改动 | 原因 |
|---|---|---|
| `tools/render_missions.py` | 新增 `yasuda_mission()`，`render()` 末尾拼上；打印条数改为动态 | missions.json 是生成物，不能手改，否则 `test_generated_catalog_current` 失败 |
| `gentactix/rag.py` | `series` 增加 `"安田讲堂攻防战-": "安田讲堂/"` | 原来只有三个系列会走「必要章节注入」，单战役会被 early-return，`test_pinned_rules_all_twenty` 拿不到「争议与待考」 |
| `tools/render_long_march.py` | ① `data_dir.relative_to(ROOT).as_posix()`；② 锚点表支持无 GeoNames ID | ① 原写法在 Windows 输出反斜杠，导致 `verify_anti_japanese_war` / `verify_long_march` 的 `--check` **在本机本来就会失败**（文件是 Linux 生成的）；② 安田锚点没有 GeoNames ID |
| `verify_missions.py`、`verify_mission_backend.py` | 断言 20 → 21 | 目录确实多了一条 |

`gentactix/missions.json` 由 `python tools/render_missions.py` 重新生成（21 条，含新条目），未手改。

## 四、安田讲堂这条想定怎么设的

- 红方＝讲堂守备队（1 层 40 人、2 层 30 人、法学部研究室 130 人），蓝方＝机动队（正门 1000、赤门 1000、装甲放水 120）。
- `profile=delay`：守住截止回合、红方至少两个编组有人员、蓝方未进入 exit 600 m 内。exit 放御茶之水站前（约 1.6 km），这样在 0.5 km 的校园尺度上也能判定。
- `map_center`＝讲堂（35.713428, 139.762297），`map_radius_km=0.8`；`geometry` 用本包那套校园尺度七参数（contact 0.05 / control 0.04 / encircle 0.3 / retreat 0.4 / sealed 0.85·0.5 / terrain 1.35）。
- 所有人数、库存、钟点都写进 `assumptions`：教学假设，不是史实部署。

## 五、验证记录（本机）

| 检查 | 结果 |
|---|---|
| `python tools/render_missions.py --check` | 21 条一致 |
| `python tools/render_yasuda.py --check` | 一致 |
| `verify_missions.py` | 13 tests OK |
| `verify_mission_backend.py` | 4 tests OK |
| `verify_desktop_backend.py` | 33 tests OK |
| `verify_app_integration.py` | 23/23 |
| `verify_anchors.py` | 380 PASS / 0 FAIL |
| `verify_anti_japanese_war.py` / `verify_long_march.py` | OK（顺带修好了本机路径分隔符导致的假失败） |
| `verify_all.py` | **32/33**；唯一失败是 `verify_model_settings` 的 `st_mode==0o600`，Windows 下 chmod 语义不同，属既有环境问题，与本次改动无关 |
| API 实测 | `/api/missions`=21、`/api/battles`=46、建会话→init→next 全部 200 |

## 六、怎么自己复核 / 回滚

复核：

```
cd E:\Gentactix-DSH
.\.venv\Scripts\python.exe tools\render_missions.py --check
.\.venv\Scripts\python.exe verify_missions.py
.\.venv\Scripts\python.exe verify_mission_backend.py
.\.venv\Scripts\python.exe verify_desktop_backend.py
```

回滚（只删安田这一条）：

1. `tools/render_missions.py` 里去掉 `result.append(yasuda_mission())`，重跑生成器；
2. `gentactix/rag.py` 的 `series` 去掉安田那项；
3. 删 `data/yasuda/`、`corpus/安田讲堂…md`、`adjudication/安田讲堂…md`、`gentactix/yasuda_anchors.json`、`tools/render_yasuda.py`；
4. 两个 verifier 的 21 改回 20。

## 七、注意

- 战役列表按 `battle` 字符串精确匹配来联动「初始态势」下拉；安田的 `battle` 必须与 `adjudication` 文件名、`anchors.campaigns` 键、`scenarios.json` 的 `name` 完全一致（本包已对齐，改动时四处要一起改）。
- 前端 `dist` 不用重建：列表是运行时从 `/api/missions`、`/api/battles` 拉的。
- 后端已重启到 8700，静态页 8711；用 `E:\Gentactix-DSH\启动GenTactix-DSH.bat` 启动即可复现。
