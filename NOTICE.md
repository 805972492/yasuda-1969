# NOTICE · 第三方来源与许可

本仓库的文字与数据表由整理者撰写，但依据以下公开史料与作品。**本仓库不转载它们的全文、扫描件或整本电子书**，只做摘录、事实整理与链接。涉及引文的条目均标注 S 编号，编号表见 `docs/02_史料清单与可信度评估.md`。

## 一、一手史料与官方统计

| 来源 | 权利人 | 本仓库的用法 |
|---|---|---|
| 東京大学「紛争日誌 その4」（1969-01-01 至 03-26，翻刻）<br>https://www.u-tokyo.ac.jp/content/400261559.pdf | 東京大学文書館 | 只摘录逐日条目、时刻与人数，注明行号与日期；不转载 PDF 或整份翻刻 |
| 東京大学文書館紀要 第37号（2019）「紛争日誌 その1」解題<br>https://www.u-tokyo.ac.jp/content/400141850.pdf | 東京大学文書館 | 只引用其资料群编号与体例说明 |
| 第61回国会 会議録（1969）<br>https://kokkai.ndl.go.jp/ | 国立国会図書館 | 引用答辩原文与数字，注明会议、日期与议员名 |
| 犯罪白書 昭和44年版（第一編第五章二）<br>https://hakusyo1.moj.go.jp/jp/10/nfm/n_10_2_1_5_2_0.html | 法務省 | 引用统计数值并注明「44-05-20 現在」等口径；不转载页面扫描件 |
| 東大新聞 2025-11-06「安田講堂竣工100周年」<br>https://www.todaishimbun.org/yasuda100hekiga_20251106/ | 東京大学新聞社 | 引用建筑与座席数据 |
| 文化遺産オンライン「東京大学工学部列品館」<br>https://online.bunka.go.jp/heritages/detail/185550 | 文化庁 | 引用登録有形文化財信息 |
| 東京大学 FOCUS／淡青 等校内刊物 | 東京大学 | 引用校园图与建筑沿革，不转载图片 |

## 二、当事者回忆与研究著作（只摘引，不转载）

| 作品 | 权利人 | 本仓库的用法 |
|---|---|---|
| 島泰三『安田講堂 1968—1969』（中文译本） | 作者／译者／出版者 | 引用页码定位（`L####`）与短句，用于层内配置、人数口径、心理描写 |
| 小熊英二『1968』上下（中文译本） | 作者／译者／出版者 | 引用页码定位与短句，用于世代背景、派系结构、日共语汇 |
| 『日本共産党の六十五年』等党方叙述 | 出版者 | 经民间研究站二次引述，标为 C 级 |

**本仓库不包含**上述两本中译本的 EPUB、全文抽取文本或大段译文。需要复核的读者请自行购买或借阅原书，再按 `docs` 中的 `L####` 定位。

## 三、报道引用

日経（2019-01-17）、産経「警視庁150年」（2024-07-14）、共同通信写真档案、NHK 节目表等，只引用标题、日期与数字，并标为二次引述（C 级）。NHK 节目表截图不随仓库发布。

## 四、地图数据

- **OpenStreetMap**：`data/key_buildings.geojson`、`data/osm_points.geojson` 与 `maps/` 中的建筑轮廓由 OSM 数据提取。
  © OpenStreetMap contributors，许可 **ODbL 1.0**（https://www.openstreetmap.org/copyright）。
  这些衍生库按 ODbL 提供；如再分发，请保留署名并以 ODbL 共享。
- **国土地理院**：地图与截图使用地理院タイル（https://maps.gsi.go.jp/development/ichiran.html），
  截图注明「出典：国土地理院」。底图版权不归本仓库，不在 CC BY 4.0 范围内。
- 1969 年的校园配置为**按史料方位推定**，不是 1969 年测绘图；误差说明见 `docs/10_1969年地形复原图说明.md`。

## 五、软件

本项目的推演包**基于 [pystrategylab/Gentactix](https://github.com/pystrategylab/Gentactix) 扩展**，并按 [snow-wind-001/Gentactix-DSH](https://github.com/snow-wind-001/Gentactix-DSH) 的数据结构组织；感谢原作者开源。

上游版权声明（MIT，随本仓库保留）：

```
MIT License

Copyright (c) 2026 pystrategylab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- 本仓库不包含上游代码本体；`integrations/gentactix-dsh/` 只提供新增文件与最小 diff。
- 本仓库自己的代码同样以 MIT 发布（`LICENSE`），文档与数据表以 CC BY 4.0 发布（`LICENSE-docs`）；两者都不改变上游的 MIT 条件。
- **Leaflet 1.9.4**（BSD-2-Clause）与 **leaflet-polylinedecorator**（MIT）经 CDN 引入，未随仓库分发。
- 演示页面的结算逻辑为本仓库自行编写，不是 Gentactix-DSH 上游代码。

## 六、截图

`screenshots/` 下的图片是本仓库自制界面的截图，按 CC BY 4.0 提供；但其中卫星影像来自国土地理院、矢量底图来自 OpenStreetMap，**这两部分仍归各自权利人**，转发时请一并保留署名。
