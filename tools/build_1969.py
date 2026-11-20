# -*- coding: utf-8 -*-
"""1969 年本郷構内 地形復元図 + 安田講堂立面分層示意图 生成器（標準ライブラリのみ）"""
import csv, json, os, io

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
MAP = os.path.join(HERE, "map")

# ---------------------------------------------------------------- 1969 要素表
# 類別: retain=1969存在・現在も同じ場所に現存 / lost=1969存在・現存せず / post=1969年には無かった
# 確度: A=史料に明記 / B=建物史で年が判明・位置は現況から推定 / C=位置推定
ROWS = [
    dict(name="安田講堂（大講堂）", cat="retain", built="1925", lat=35.713428, lon=139.762297,
         evid="S13/S14・東大新聞 2025-11-06・東大 FOCUS", conf="A",
         note="地上5階・地下1階＋時計塔（6〜9階）。3階以上が台地上、1・2階が崖下。1969 当時の収容 3階961席＋4階777席＝1,738席。"),
    dict(name="旧理学部1号館（数学物理学教室）", cat="lost", built="1926（4階は1965増築）", lat=35.71347, lon=139.76275,
         evid="都市徘徊blog 2022-08-16（建物史）・理学部旧1号館特設ページ", conf="C",
         note="安田講堂の東（裏）の崖下。L字→ロ字、1969 には 4 階まで。1994 西棟・2003 中央棟・2013 東棟の3期で解体。位置は現・理学部1号館の敷地と重なると推定。"),
    dict(name="安田講堂前広場（中央食堂は地下・1976年造成）", cat="post", built="1976", lat=35.71342, lon=139.76204,
         evid="東大新聞 2025-11-06（中央食堂は1976年、講堂前を掘削して地下に造成）", conf="B",
         note="1969 年は地上の広場。現在の中央食堂は地下施設で、地上はやはり広場。"),
    dict(name="御殿下グラウンド（記念館は1983着工・1989完成）", cat="post", built="1989", lat=35.71222, lon=139.76328,
         evid="東大埋蔵文化財調査室・御殿下記念館公式（平成元年1月完成）", conf="B",
         note="1969 年は屋外グラウンド（崖下）。1/18 15:30 に機動隊がここ側から講堂背面へ突入した。"),
    dict(name="山上会館（現建物は1983着工・創立百年記念事業）", cat="post", built="1989", lat=35.712082, lon=139.762709,
         evid="東大埋蔵文化財調査室（1983年に御殿下記念館・山上会館の建設開始）", conf="B",
         note="1969 年に現在の建物はない（旧施設の内容は未確認）。"),
    dict(name="本部棟（1979年完成。1969 の本部機能は安田講堂内）", cat="post", built="1979", lat=35.71305, lon=139.76085,
         evid="東大新聞 2025-11-06（79年の本部棟完成に伴い総長室が移転）", conf="C",
         note="1969 年は総長室・本部事務が安田講堂 1・2 階にあった。本部棟の位置は現況からの推定。"),
]

# 轮廓按史料方位推定的三处（OSM 无多边形）：用矩形示意，虚线 + 低透明度
RECTS = [
    dict(name="工学部列品館（1969 要塞・現存）", cat="retain", built="1925", lat=35.71395, lon=139.76035,
         w=42, h=30, evid="S22 文化遺産オンライン・S1 紛争日誌（1/18 8:50—13:00）", conf="C",
         note="正門左手奥（北側），今工学部本部。RC 3階建・建築面積766㎡・1996/1998 登録有形文化財。"
              "1/14 16:00 社学同 ML 派约50人占拠要塞化；1/18 08:50 起排除，火炎放射器抵抗，"
              "11:00 装甲車破垒，2・3・4階起火，13:00 过屋上突入 32 人被捕（女3・重傷2）。"),
    dict(name="法文2号館（1969 革マル据点）", cat="lost", built="不明", lat=35.71300, lon=139.76060,
         w=38, h=24, evid="S1 紛争日誌（1/18 09:20）・S24 米田証言", conf="C",
         note="1969 年存在、现在 OSM 无同名多边形（疑似改建或合并）。按法文1号館东北的相对位置推定。"
              "1/18 09:20 革マル系 14 人据守，3・4階から投石，屋上で全員逮捕（米田说 12 人）。"),
    dict(name="理学部化学新館（1969 反帝学評据点）", cat="unknown", built="不明", lat=35.71360, lon=139.76340,
         w=32, h=22, evid="S1 紛争日誌（1/15 11:20）", conf="C",
         note="1969 年确实存在（1/15 11:20 反帝学評约50人在此构筑街垒并抽重油）。"
              "现址对应建筑与拆除时间未确认，故按「未确认」处理。"),
]

def rect(lat, lon, w_m, h_m):
    import math
    dlat = (h_m / 2) / 111320.0
    dlon = (w_m / 2) / (111320.0 * math.cos(math.radians(lat)))
    ring = [[lon - dlon, lat - dlat], [lon + dlon, lat - dlat],
            [lon + dlon, lat + dlat], [lon - dlon, lat + dlat],
            [lon - dlon, lat - dlat]]
    return {"type": "Polygon", "coordinates": [ring]}

# 現代建物（OSM）— 1969 年の存否が未確認のものは灰色点線で「未確認」表示
GEO = json.load(open(os.path.join(DATA, "key_buildings.geojson"), encoding="utf-8"))
CERTAIN_1969 = {"安田講堂", "法文1号館", "法学部3号館", "法学部4号館", "工学部1号館",
                "東京大学総合図書館", "文学部3号館", "赤門", "東京大学教育学研究科・教育学部",
                "医学部総合中央館", "医学部3号館", "工学部11号館", "工学部5号館"}
TREES = {"銀杏並木", "三四郎池", "赤門通り", "三四郎坂", "医学部前広場", "工学部前広場",
         "御殿下グラウンド"}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def write_csv():
    p = os.path.join(DATA, "reconstruction_1969.csv")
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["名称", "类别", "竣工年", "纬度", "经度", "可信度", "出处", "说明"])
        for r in ROWS + RECTS:
            w.writerow([r["name"], r["cat"], r["built"], r["lat"], r["lon"], r["conf"], r["evid"], r["note"]])
    return p
from elev_svg import SVG

def build():
    feats = []
    for f in GEO["features"]:
        nm = (f["properties"].get("name") or "").strip()
        if not nm:
            continue
        if nm in TREES:
            kind = "tree"
        elif nm == "安田講堂":
            kind = "hall"
        elif nm in CERTAIN_1969:
            kind = "retain"
        else:
            kind = "unknown"
        feats.append(dict(kind=kind, name=nm, geom=f["geometry"]))
    for r in ROWS:
        if r["cat"] == "lost":
            feats.append(dict(kind="lost", name=r["name"], lat=r["lat"], lon=r["lon"],
                              conf=r["conf"], note=r["note"], evid=r["evid"], built=r["built"]))
        elif r["cat"] == "post":
            feats.append(dict(kind="post", name=r["name"], lat=r["lat"], lon=r["lon"],
                              conf=r["conf"], note=r["note"], evid=r["evid"], built=r["built"]))

    for r in RECTS:
        feats.append(dict(kind=r["cat"], name=r["name"], geom=rect(r["lat"], r["lon"], r["w"], r["h"]),
                          approx=True, conf=r["conf"], note=r["note"], evid=r["evid"], built=r["built"]))

    rows_html = "".join(
        f"<tr><td>{esc(r['name'])}</td><td>{r['built']}</td><td>{r['conf']}</td>"
        f"<td>{esc(r['evid'])}</td></tr>" for r in ROWS + RECTS)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>安田讲堂 1969 地形复原图 + 立面分层示意</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
 *{{box-sizing:border-box}}
 body{{margin:0;background:#0a0e14;color:#dbe4ee;font-family:"Microsoft YaHei",system-ui,sans-serif;display:flex;flex-direction:column;height:100vh}}
 header{{padding:8px 14px;background:#111a24;border-bottom:1px solid #22303f;display:flex;gap:18px;align-items:center;flex-wrap:wrap}}
 header h1{{font-size:15px;margin:0;font-weight:600;letter-spacing:.5px}}
 .lg{{display:flex;gap:12px;font-size:11px;align-items:center;flex-wrap:wrap}}
 .sw{{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:4px;vertical-align:-1px}}
 label.tg{{font-size:11.5px;cursor:pointer;color:#9db0c4}}
 main{{flex:1;display:flex;min-height:0}}
 #map{{flex:1;min-width:0}}
 aside{{width:430px;min-width:430px;background:#0d151e;border-left:1px solid #22303f;overflow:auto}}
 .tabs{{display:flex;border-bottom:1px solid #22303f;position:sticky;top:0;background:#0d151e;z-index:5}}
 .tabs button{{flex:1;padding:9px;background:none;border:0;color:#7f93a8;font-size:12.5px;cursor:pointer;border-bottom:2px solid transparent}}
 .tabs button.on{{color:#e8f1fa;border-bottom-color:#e0a75a}}
 .pane{{display:none;padding:12px}} .pane.on{{display:block}}
 table{{width:100%;border-collapse:collapse;font-size:11px}}
 td,th{{border-bottom:1px solid #1e2b38;padding:4px 3px;text-align:left;vertical-align:top}}
 th{{color:#8fa6bc;font-weight:500}}
 .note{{font-size:11.5px;color:#93a7bc;line-height:1.65}}
 .note b{{color:#d9c08a}}
 .leaflet-popup-content{{font-size:12px;line-height:1.6;margin:8px 10px;color:#1b2430}}
 .leaflet-popup-content b{{color:#8a5b12}}
 .tag{{display:inline-block;font-size:10px;padding:1px 5px;border-radius:3px;margin-right:4px}}
</style></head><body>
<header>
  <h1>安田讲堂 1969 地形复原图</h1>
  <div class="lg">
    <span><i class="sw" style="background:#2f7f5e"></i>1969 已有·现存</span>
    <span><i class="sw" style="background:#c0563b"></i>1969 已有·已拆除</span>
    <span><i class="sw" style="background:#c9a227"></i>1969 时尚无</span>
    <span><i class="sw" style="background:#3a4a5c"></i>今存·1969 未确认</span>
    <span><i class="sw" style="background:#4f8fd0"></i>地形/树木</span>
  </div>
  <label class="tg"><input type="checkbox" id="tBase" checked> 现代建物轮廓</label>
  <label class="tg"><input type="checkbox" id="tOld" checked> 1969 要素</label>
</header>
<main>
  <div id="map"></div>
  <aside>
    <div class="tabs">
      <button class="on" data-p="p1">立面分层示意</button>
      <button data-p="p2">要素与依据</button>
      <button data-p="p3">怎么用</button>
    </div>
    <div class="pane on" id="p1">{SVG}
      <div class="note" style="margin-top:10px">
        <b>为什么正面在 3 楼</b>：安田讲堂建在本乡台地东端的崖地上。台地一侧（西，正门与银杏并木方向）地面就在 3 楼，因此正门入口在 3 楼；崖下（东，御殿下グラウンド方向）露出 1、2 楼。3 楼与 1 楼高差约 6 米。
      </div>
    </div>
    <div class="pane" id="p2">
      <table><tr><th>要素</th><th>年</th><th>可信度</th><th>出处</th></tr>{rows_html}</table>
      <p class="note" style="margin-top:10px">
        可信度：<b>A</b> 一手史料/官方说明明确记载；<b>B</b> 建物史或校方文章给出年份，位置按现况推定；<b>C</b> 位置为推定（图中以虚线圈或虚线表示）。
      </p>
    </div>
    <div class="pane" id="p3">
      <p class="note">
        <b>1.</b> 灰蓝色底图是现代 OSM 建物轮廓，只作为“对齐参照”。绿色＝1969 年已存在且现存；红色＝1969 年存在、后来拆了（图中只有旧理学部 1 号馆一项有据可查，用虚线圈标推定范围）；黄色＝1969 年还没有。<br>
        <b>2.</b> 推演时请把“黄色”四项从 1969 年的战场里去掉：中央食堂（1976）、本体栋（1979）、御殿下纪念馆与山上会馆（1989）。也就是说<b> 1969 年 1 月，讲堂前的广场就是一片空地，讲堂 1、2 楼里挤着本部事务与总长室</b>。<br>
        <b>3.</b> 黄圈“未确认”不代表 1969 年不存在，只表示我没有找到它的竣工年；请勿据此下结论。<br>
        <b>4.</b> 底图瓦片来自国土地理院（需联网）。建筑轮廓 © OpenStreetMap contributors（ODbL）。
      </p>
    </div>
  </aside>
</main>
<script>
const FEATS = {json.dumps(feats, ensure_ascii=False)};
const COLORS = {{retain:'#2f7f5e', lost:'#c0563b', post:'#c9a227', unknown:'#3a4a5c', tree:'#4f8fd0', hall:'#e08a3c'}};
const map = L.map('map', {{zoomControl:true}}).setView([35.7128,139.7618], 17);
const gsi = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{{z}}/{{x}}/{{y}}.jpg',
  {{maxZoom:19, attribution:'国土地理院 シームレス写真'}}).addTo(map);
const gstd = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/std/{{z}}/{{x}}/{{y}}.png',
  {{maxZoom:18, attribution:'国土地理院 標準地図'}});
L.control.layers({{'卫星照片':gsi,'标准地图':gstd}}, null, {{position:'topleft'}}).addTo(map);

const baseLayer = L.layerGroup().addTo(map);
const oldLayer = L.layerGroup().addTo(map);

const NOTE = {{
 'retain':'1969 年存在，且今天还在原址。',
 'lost':'1969 年存在，后来被拆除。',
 'post':'1969 年 1 月还没有这座建筑。',
 'unknown':'今天存在；1969 年的情况未确认（不作推断）。'
}};

function style(f) {{
  const c = COLORS[f.kind] || '#3a4a5c';
  const dash = f.approx ? '5 3' : (f.kind === 'unknown' ? '4 4' : (f.kind === 'tree' ? '2 4' : null));
  const fo = f.approx ? 0.22 : (f.kind==='hall'?0.55:(f.kind==='unknown'?0.10:0.42));
  return {{color:c, weight:f.kind==='hall'?2.5:(f.approx?2:1.4), fillColor:c,
           fillOpacity:fo, dashArray:dash}};
}}

FEATS.forEach(f => {{
  if (f.geom) {{
    const isBase = (f.kind === 'unknown' && !f.approx);
    const layer = L.geoJSON(f.geom, {{
      style: style(f),
      onEachFeature: (ft, lay) => lay.bindPopup(
        `<b>${{f.name}}</b><br>${{NOTE[f.kind]||''}}` +
        (f.approx ? '<br><i>轮廓为推定矩形</i>' : '') +
        (f.built ? `<br>竣工：${{f.built}}` : '') +
        (f.conf ? `<br>可信度：${{f.conf}}` : '') +
        (f.note ? `<br>${{f.note}}` : '') +
        (f.evid ? `<br><span style="color:#666">出处：${{f.evid}}</span>` : ''))
    }});
    (isBase ? baseLayer : oldLayer).addLayer(layer);
  }} else if (f.lat) {{
    const mk = L.circle([f.lat, f.lon], {{
      radius: 42, color: COLORS[f.kind], weight: 2, dashArray: '6 4',
      fillColor: COLORS[f.kind], fillOpacity: 0.18
    }}).addTo(oldLayer);
    mk.bindPopup(`<b>${{f.name}}</b><br>竣工：${{f.built||'—'}}<br>
      可信度：${{f.conf}}<br><b>位置为推定范围</b><br>${{f.note}}<br>
      <span style="color:#666">出处：${{f.evid}}</span>`);
    mk.bindTooltip(f.name, {{direction:'top'}});
  }}
}});

document.getElementById('tBase').onchange = e =>
  e.target.checked ? map.addLayer(baseLayer) : map.removeLayer(baseLayer);
document.getElementById('tOld').onchange = e =>
  e.target.checked ? map.addLayer(oldLayer) : map.removeLayer(oldLayer);

document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => {{
  document.querySelectorAll('.tabs button').forEach(x => x.classList.remove('on'));
  document.querySelectorAll('.pane').forEach(x => x.classList.remove('on'));
  b.classList.add('on');
  document.getElementById(b.dataset.p).classList.add('on');
}});
</script></body></html>"""
    p = os.path.join(MAP, "1969地形复原图.html")
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
    return p

if __name__ == "__main__":
    print("csv:", write_csv())
    p = build()
    print("html:", p, os.path.getsize(p), "bytes")
