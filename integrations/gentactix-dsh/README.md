# 并入 Gentactix-DSH（可选）

目标：让「安田讲堂攻防战」出现在 `Gentactix-DSH` 界面的战役列表里，和台儿庄那批并列；也可以只把本包当独立数据用。

目录里给了**新增文件**和**上游改动 diff**，不含上游代码本体（上游是 MIT，请自行 clone）。

## 一、需要放进上游的文件

| 本目录 | 放到上游 | 说明 |
|---|---|---|
| `data/yasuda/` | `data/yasuda/` | 编辑源：scenarios / sources / 4 张 CSV / INDEX |
| `gentactix/yasuda_anchors.json` | `gentactix/yasuda_anchors.json` | 14 个地名锚点 |
| `corpus/…安田….md` | `corpus/` | 史料卡，RAG 按 `##` 切片 |
| `adjudication/…安田….md` | `adjudication/` | geo-5 七参数 |
| `tools/render_yasuda.py` | `tools/` | 渲染器，`--check` 可校验 |

## 二、需要改的上游文件

见 `diffs/`，逐条是 unified diff，可直接 `git apply` 试：

| diff | 改动 | 为什么 |
|---|---|---|
| `rag.py.diff` | `series` 增加 `"安田讲堂攻防战-": "安田讲堂/"` | 原逻辑只给三个系列注入「必要章节」；单战役会被 early-return，拿不到《争议与待考》等必读段 |
| `render_missions.py.diff` | 新增 `yasuda_mission()`，拼到 `render()` 末尾 | `missions.json` 是生成物，手改会被 `test_generated_catalog_current` 判失败 |
| `render_long_march.py.diff` | ① 路径改 `as_posix()`；② 锚点允许没有 GeoNames ID | ① 原写法在 Windows 输出反斜杠，会让 `--check` 假失败；② 安田锚点没有 GeoNames |
| `verify_missions.py.diff`、`verify_mission_backend.py.diff` | 断言 20 → 21 | 目录确实多了一条 |

改完跑生成器，不要手改 JSON：

```bash
python tools/render_yasuda.py
python tools/render_missions.py          # 重新生成 gentactix/missions.json（21 条）
```

## 三、安装后的样子

- `GET /api/missions` → 21 条，新增 `YS01-local-v1`，profile=`delay`，30 分钟/回合，deadline 6。
- `GET /api/battles` → 46 条，新增「安田讲堂攻防战-1969.01.18至1969.01.19 · 建议 30分钟/回合」。
- 界面：启动页「战役资料库 46」→ 选它 → 「初始态势」选「可重放局部教学 · 迟滞」→ 创建。

初始态势：红方＝讲堂守备队（1 层 40 / 2 层 30 / 法学部研究室 130），蓝方＝机动队（正门 1000 / 赤门 1000 / 装甲放水 120）。目标：守满 6 回合、红方至少两个编组有人员、蓝方未进到御茶之水站前 600 m 内。

## 四、验证

```bash
python tools/render_missions.py --check
python tools/render_yasuda.py --check
python verify_missions.py
python verify_mission_backend.py
python verify_desktop_backend.py
python verify_app_integration.py
python verify_anchors.py
```

本机实测：`verify_missions` 13 tests OK、`verify_mission_backend` 4 tests OK、`verify_desktop_backend` 33 tests OK、`verify_app_integration` 23/23、`verify_anchors` 380 PASS。

## 五、回滚

1. `tools/render_missions.py` 去掉 `result.append(yasuda_mission())`，重跑生成器；
2. `gentactix/rag.py` 的 `series` 去掉安田那项；
3. 删掉本目录放进去的 5 组文件；
4. 两个 verifier 的 21 改回 20。

## 六、一个坑

`battle` 字符串是主键：`data/yasuda/scenarios.json` 的 `name`、`adjudication/` 文件名、`anchors.campaigns` 的键、missions 的 `battle` 必须**完全一致**。改一处就要四处同改，否则列表里点了没反应。
