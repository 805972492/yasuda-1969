# data/ · 事实表

这些 CSV 是整理稿的机器可读版，全部来自 `docs/` 里登记过的来源（S 编号见 `docs/02`）。`null`／空串表示**未核得**，不是 0。

| 文件 | 内容 | 出处 |
|---|---|---|
| `timeline.csv` | 构内分钟级事件 70 条（1/17—1/20），字段：相对分钟／日期／时刻／事件／经纬度／可信度／S 编号／类别 | 主要 S1，辅 S34 |
| `jan1_14_s1.csv` | 1/1—1/14 的前史 47 条（同 S1 逐日） | S1 |
| `units.csv` | 双方 16 个编组：阵营／位置／兵力／任务／经纬度／装备／补给／士气（后三项标推定） | S1、S34 |
| `buildings.csv` | 47 栋建筑的当日角色与当日事件（轮廓来自 OSM） | OSM + S1 |
| `casualties.csv` | 21 行伤亡与逮捕口径对照（警察负伤 653、学生重伤 76、検挙 633/983 等） | 国会会議録、S34、S35 |
| `persons.csv` | 14 位人物的身份、1969 年位置、关键事实、证据类型 | 综合 |
| `factions.csv` | 20 个派系：系统、上部团体、据点、人数口径 | 综合 |
| `impact.csv` | 12 条「他地／他校 → 本乡」的影响 | S1 |
| `tokyo_ops.csv` | 全城 108 条事件（1/15—1/29）：地点、类别、经纬度、坐标可信度 | S1 |
| `reconstruction_1969.csv` | 1969 年构内配置复原 9 项（现存／已拆／后建） | S1、淡青、东大新闻 |
| `key_buildings.geojson`<br>`key_buildings.json`<br>`osm_points.geojson` | OSM 提取的建筑多边形与点位 | © OpenStreetMap contributors，**ODbL 1.0** |

## 坐标

WGS84。校园内点位精度约 10 m（OSM 轮廓），史料推定项标 `推定` 并给误差圈。1969 年的建筑配置以 `docs/10` 的说明为准：**不是 1969 年测绘图**。

## ODbL

`*.geojson` 与 `key_buildings.json` 属 OSM 衍生数据库，按 ODbL 1.0 提供：可复制、分发、修改，但需保留「© OpenStreetMap contributors」署名，且衍生库须同样以 ODbL 共享。文字与 CSV 事实表按 CC BY 4.0（见根目录 `LICENSE-docs`）。
