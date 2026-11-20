# -*- coding: utf-8 -*-
"""安田讲堂攻防战 战役包生成器（Gentactix-DSH 结构 v2）。

输出：
  data/yasuda_battle/{scenarios.json,sources.json,timeline.csv,forces.csv,figures.csv,verification_gaps.csv,INDEX.md,README.md}
  corpus/安田讲堂攻防战-1969.01.18至1969.01.19.md
  adjudication/安田讲堂攻防战-1969.01.18至1969.01.19.md
  gentactix/yasuda_anchors.json
  推演展示_安田讲堂.html   （把 pack 内联进模板，双击即可玩）
"""
from __future__ import annotations

import csv
import io
import json
import os
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT
DATA = os.path.join(OUT, "data", "yasuda_battle")
CORPUS = os.path.join(OUT, "corpus")
ADJ = os.path.join(OUT, "adjudication")
GENT = os.path.join(OUT, "gentactix")

BATTLE = "安田讲堂攻防战-1969.01.18至1969.01.19"
SCEN_ID = "YS01"
SCHEMA_VERSION = 2

CHECKED = "2026-11-20"

# --------------------------------------------------------------------------
# 来源
# --------------------------------------------------------------------------
SOURCES = {
    "S1": {
        "title": "東京大学「紛争日誌 その4」（1969年1月1日—3月26日）",
        "publisher": "东京大学文书馆（翻刻）",
        "url": "https://www.u-tokyo.ac.jp/content/400261559.pdf",
        "evidence_type": "一手日志（当日记录、翻刻）",
        "supports": "逐日分钟级记录：入构时刻、各馆解除、逮捕人数、神田联动、发布与交涉",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S34": {
        "title": "島泰三『安田講堂 1968—1969』（中文译本）",
        "publisher": "当事者回忆录",
        "url": "",
        "evidence_type": "当事者回忆",
        "supports": "馆内分层配置、馆内生活、恐惧与秩序、逮捕 397 人、伤情 76 重伤",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S35": {
        "title": "小熊英二『1968』上下（中文译本）",
        "publisher": "研究著作",
        "url": "",
        "evidence_type": "研究综述（引大量访谈与统计）",
        "supports": "世代与阶层结构、派系构成、日共与民青的定性语汇、逮捕 983 说",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S41": {
        "title": "犯罪白書 昭和44年版 第一編第五章二",
        "publisher": "法務省",
        "url": "https://hakusyo1.moj.go.jp/jp/10/nfm/n_10_2_1_5_2_0.html",
        "evidence_type": "官方统计（检察阶段）",
        "supports": "东大事件受理 984 人、起訴 1,776、勾留认容率 98.0%",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S43": {
        "title": "東京大学文書館紀要 第37号（「紛争日誌 その1」解題）",
        "publisher": "东京大学文书馆",
        "url": "https://www.u-tokyo.ac.jp/content/400141850.pdf",
        "evidence_type": "史料解题",
        "supports": "資料群 A–G 与底本关系、翻刻取舍原则",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S2": {
        "title": "第61回国会 会議録（1969年）安田講堂事件関連答弁",
        "publisher": "国立国会图书馆 国会会议録检索システム",
        "url": "https://kokkai.ndl.go.jp/",
        "evidence_type": "国会答辩（官方记录）",
        "supports": "警察側负伤 653（入院 37）、燃烧瓶 500 本、起訴 509、物件損害 4.5 億圆",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S3": {
        "title": "最高裁刑事局 学生運動関係事件の処理状況（二次引述）",
        "publisher": "最高裁判所事務总局（經二次引述）",
        "url": "",
        "evidence_type": "司法統計（二次引述）",
        "supports": "起訴 607 人、一審有罪 590 人（实刑 147 人）",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S27": {
        "title": "日経「東大安田講堂攻防から50年」（2019-01-17）等報纸报道",
        "publisher": "日本经济新闻 等",
        "url": "https://www.nikkei.com/article/DGKKZO40105530X10C19A1EAC000/",
        "evidence_type": "报紙报道（二次引述）",
        "supports": "机动队約 8,500 人、逮捕約 630 人、催泪弹 1 万发·96 台车两、入試中止",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
    "S46": {
        "title": "NHKクロニクル 1969年1月18日・19日 総合テレビ番組表",
        "publisher": "NHK",
        "url": "https://www.nhk.or.jp/archives/chronicle/",
        "evidence_type": "播出记录（用户提供截图）",
        "supports": "两日节目表；无独立「现场直播」，有特别节目与新闻焦点",
        "accessed": "2026-11-20",
        "original_archive_examined": False,
    },
}

# --------------------------------------------------------------------------
# 编成（坐标 WGS84；凡标推定者见 note）
# --------------------------------------------------------------------------
FORCES = [
    # 攻方
    dict(side="机动队", unit="第1·第2机动队（工学部方面）", desc="06:50 自农学部正门入构，过陆桥向工学部；责任区为工学部1·2·7·8号馆与列品馆方面。", n=1000, lat=35.71380, lng=139.76000, conf="推定", src=["S1"]),
    dict(side="机动队", unit="第3·第4机动队（龙冈门·池之端门）", desc="07:03 自龙冈门与池之端门入构，责任区医学部方面与构内东南。", n=1000, lat=35.71180, lng=139.76400, conf="推定", src=["S1"]),
    dict(side="机动队", unit="第5·第6机动队（赤门）", desc="07:05 自赤门入构，责任区法学部·文学部·经济学部方面。", n=1000, lat=35.71059, lng=139.76036, conf="A", src=["S1"]),
    dict(side="机动队", unit="第7·第8机动队（正门·讲堂正面）", desc="正门方面待机与正面攻略；13:20 本格攻击、15:20 正面攻击。", n=1000, lat=35.71294, lng=139.75966, conf="A", src=["S1"]),
    dict(side="机动队", unit="装甲车·放水车队", desc="放水车10数台（09:00）、装甲车以11:00 破列品馆路障、烟幕与催泪弹支援。", n=120, lat=35.71300, lng=139.76090, conf="推定", src=["S1", "S34"]),
    dict(side="机动队", unit="直升机（侦察·催泪液）", desc="08:00 上空投催泪弹、14:35 铁桶催泪液、次日 09:00 风压支援。", n=2, nunit="架", lat=35.71343, lng=139.76230, conf="推定", src=["S1"]),
    dict(side="机动队", unit="私服·搜查班", desc="500 人（S1）；17:50 明大学生会馆突入救出即其行动。", n=500, lat=35.71250, lng=139.76100, conf="推定", src=["S1"]),
    dict(side="机动队", unit="神田增派（东大→神田 900 人）", desc="13:30 自东大抽调 900 人赴神田，与既存部队合计 2,000 人阻止学生流向警视厅（自 8,000 人中抽出，不另加于总数）。", n=900, lat=35.69900, lng=139.76430, conf="B", src=["S1"]),
    # 守方（馆内分层按 S34；人数标「未詳」者按史料不填）
    dict(side="全共斗", unit="安田讲堂 1层（大讲堂下层）", desc="本乡本科生部队 40 人，文科·理科两分队守四处楼梯；对党派部队无指挥权。", n=40, lat=35.713428, lng=139.762297, conf="A", src=["S34"], floor=1),
    dict(side="中核派", unit="安田讲堂 2层（中核派＋全斗联·青医联）", desc="二层约 30 人为中核派·全斗联·青医联混成，自 17 日夜由中核派守卫，12:15 前后被捕 20 余名；另有自三层支援二层街垒的部署（S34 引岛泰三）。", n=30, lat=35.713428, lng=139.762300, conf="A", src=["S34", "S1"], floor=2),
    dict(side="反帝学评", unit="安田讲堂 5层（左）", desc="解放派据 5 层左侧；16:30 与社学同分别在 5 层南侧屋顶与 6 层阳台。人数史料未给。", n=None, lat=35.713430, lng=139.762290, conf="A", src=["S34", "S1"], floor=5),
    dict(side="社学同", unit="安田讲堂 5层（右）", desc="社学同据 5 层右侧；16:30 在 6 层阳台唱国际歌。人数史料未给。", n=None, lat=35.713432, lng=139.762294, conf="A", src=["S34", "S1"], floor=5),
    dict(side="中核派", unit="安田讲堂 6层·钟楼", desc="中核派在 6 层中央与钟楼；17:45 钟楼屋顶最后数人。人数史料未给。", n=None, lat=35.713428, lng=139.762310, conf="推定", src=["S34", "S1"], floor=6),
    dict(side="中核派", unit="法学部研究室（法研）", desc="15 日 09:30 中核派＋四托洛約 130 人入；18 日 11:40 突入 3 层、屋顶浇汽油，15:35 屋顶 121 人被捕。", n=130, lat=35.71270, lng=139.76030, conf="推定", src=["S1"]),
    dict(side="社学同 ML派", unit="工学部列品馆", desc="14 日 16:00 占据要塞化；18 日 08:50 排除开始、火焰喷射器、11:00 装甲车破路障、13:00 过后屋顶 32 人（女 3·重伤 2）。", n=50, lat=35.71395, lng=139.76035, conf="A", src=["S1", "S34"]),
    dict(side="革马派", unit="法文2号馆", desc="18 日 09:20 前后 14 人在 3·4 层投石，屋顶全员被捕。", n=14, lat=35.71300, lng=139.76060, conf="推定", src=["S1"]),
    dict(side="全共斗", unit="医学部中央馆（塔屋）", desc="16 人在塔屋抵抗至 08:30 全员被捕。", n=16, lat=35.71080, lng=139.76326, conf="A", src=["S1"]),
    dict(side="反帝学评", unit="理学部1号馆（封锁·馆内无人）", desc="1/15 16:00 反帝学评主力约 150 人侵入；1/17 12:00 再封锁；18 日 07:10 机动队到着时馆内无人（1/9 事件见证至 11:30）。", n=0, lat=35.71370, lng=139.76298, conf="A", src=["S1"]),
    # 第三方
    dict(side="民青", unit="医学部本馆（守备）", desc="18 日 19:50 共斗約 200 攻、民青約 200 自 2 楼阳台放水投石；19:30 前后仍在守。", n=200, lat=35.71080, lng=139.76180, conf="推定", src=["S1"]),
]

# --- 地域与据点（多战区：本乡 / 神田 / 驹场）---
for _f in FORCES:
    _f.setdefault("zone", "神田" if "神田" in _f["unit"] else "本乡")

FORCES += [
    dict(side="全共斗", sect="全共斗", unit="神田街垒队（御茶之水·明大通）", desc="19 日 09:00 过夜约 800 人行动开始，御茶之水站与明大通一带筑 10 处街垒；12:50 拦停都电。", n=800, lat=35.69950, lng=139.76400, conf="B", src=["S1"], zone="神田"),
    dict(side="全共斗", sect="明大共斗", unit="明大骏河台（过夜队）", desc="明大学生会馆与骏河台校舍为神田方面据点；18 日 09:35 自此处出发袭御茶之水站前派出所。", n=300, lat=35.69780, lng=139.76210, conf="B", src=["S1"], zone="神田"),
    dict(side="全共斗", sect="全共斗", unit="驹场第8本馆队", desc="驹场第 8 本馆长期被封锁；15 日民青来攻时馆内约 100 人。", n=100, lat=35.65940, lng=139.68470, conf="B", src=["S1"], zone="驹场"),
    dict(side="全共斗", sect="全共斗", unit="本乡增援（日大·他大）", desc="15–17 日陆续入构的支援部队（日大共斗 40、他大数百）；可投入本乡任何据点。", n=450, lat=35.71260, lng=139.76090, conf="推定", src=["S1"], zone="本乡"),
    dict(side="民青", sect="民青", unit="教育学部（民青据点）", desc="1/9 教育学部有民青武装约 3,000 人；1/10 秩父宮集会由民青主导；1/14 19:57 千人示威自此出发。", n=300, lat=35.71099, lng=139.76100, conf="推定", src=["S1"], zone="本乡"),
    dict(side="民青", sect="民青", unit="第2食堂（民青据点）", desc="1/1 15:00 民青约 180 人向第二食堂示威；1/10 0:30 示威后分散入第 2 食堂等据点。", n=150, lat=35.71366, lng=139.76441, conf="推定", src=["S1"], zone="本乡"),
    dict(side="民青", sect="民青", unit="驹场第1·2本馆（民青）", desc="12 日 20:30 驹场民青＋班级联合战术占据学生会馆·1 号馆并夺回第 1·2 本馆。", n=300, lat=35.66050, lng=139.68520, conf="B", src=["S1"], zone="驹场"),
    dict(side="机动队", unit="御茶之水站前派出所（守备）", desc="18 日 09:35 被 150 人袭击破玻璃；19 日 12:50 前后再被占据·放火。", n=40, lat=35.69900, lng=139.76480, conf="B", src=["S1"], zone="神田"),
]

ZONES = [
    dict(id="本乡", name="本乡构内", lat=35.71290, lng=139.76180, zoom=17),
    dict(id="神田", name="神田·御茶之水", lat=35.69870, lng=139.76420, zoom=16),
    dict(id="驹场", name="驹场", lat=35.66020, lng=139.68510, zoom=16),
]

SITES = [
    dict(id="kanda_barricade", name="神田街垒（10 处）", lat=35.69930, lng=139.76420, zone="神田", holder="全共斗", str=800, barrier=80),
    dict(id="meidai", name="明大骏河台", lat=35.69780, lng=139.76210, zone="神田", holder="全共斗", str=300, barrier=60),
    dict(id="ochano_police", name="御茶之水站前派出所", lat=35.69900, lng=139.76480, zone="神田", holder="机动队", str=40, barrier=40),
    dict(id="komaba_hachi", name="驹场第8本馆", lat=35.65940, lng=139.68470, zone="驹场", holder="全共斗", str=100, barrier=60),
    dict(id="komaba_honkan", name="驹场第1·2本馆", lat=35.66050, lng=139.68520, zone="驹场", holder="民青", str=300, barrier=50),
    dict(id="dai2shokudo", name="第2食堂", lat=35.71366, lng=139.76441, zone="本乡", holder="民青", str=150, barrier=40),
]

FLOORS0 = {
    "1": dict(holder="全共斗", sect="全共斗", mix="", n=40, b=70, note="本乡本科生部队 40 人，守四处楼梯（S34）"),
    "2": dict(holder="中核派", sect="中核派", mix="全斗联·青医联", n=30, b=80, note="二层约 30 人为中核派＋全斗联＋青医联混成，12:15 被捕 20 余名（S34）"),
    "3": dict(holder="全共斗", sect="全共斗", mix="", n=None, b=80, note="大讲堂 961 席层；3 层为台地面"),
    "4": dict(holder="全共斗", sect="全共斗", mix="", n=None, b=70, note="大讲堂上部 777 席；便殿·总长应接室"),
    "5": dict(holder="反帝学评", sect="反帝学评", mix="社学同（右半）", n=None, b=70, note="5 层南侧屋顶＝反帝学评、6 层阳台＝社学同（S1 16:30）"),
    "6": dict(holder="中核派", sect="中核派", mix="", n=None, b=60, note="钟楼；全馆最后失守处（17:27／17:45）"),
}

BUILDINGS = [
    dict(id="yasuda_hall", name="安田讲堂", lat=35.713428, lng=139.762297, zone="本乡", holder="全共斗", str=397, barrier=100, floors=True, note="馆内 397 人（S34 逮捕数）"),
    dict(id="reppinkan", name="工学部列品馆", lat=35.71395, lng=139.76035, zone="本乡", holder="社学同 ML派", str=50, barrier=80, note="1/15 16:00 占据；1/18 08:50 排除"),
    dict(id="houbou_ken", name="法学部研究室（法研）", lat=35.71270, lng=139.76030, zone="本乡", holder="中核派", str=130, barrier=70, note="15:35 屋顶突入时 121 人被捕（S1）"),
    dict(id="houbun2", name="法文2号馆", lat=35.71300, lng=139.76060, zone="本乡", holder="革马派", str=14, barrier=60, note="1/18 09:00 屋顶全员 14 人被捕"),
    dict(id="igaku_c", name="医学部综合中央馆", lat=35.710798, lng=139.76326, zone="本乡", holder="全共斗", str=16, barrier=40, note="16 人塔屋抵抗至 08:30"),
    dict(id="igaku_h", name="医学部本馆", lat=35.71080, lng=139.76180, zone="本乡", holder="民青", str=200, barrier=60, note="民青 200 人守备；1/18 未被攻"),
    dict(id="kogakubu1", name="工学部1号馆", lat=35.714231, lng=139.76006, zone="本乡", holder="反帝学评", str=None, barrier=30, note="1/12 15:00 反帝学评系再封锁工学部 1·2·7·8 号馆与列品馆（S1）；1/18 07:00 责任教官见证下解除，馆内无人，以不退去罪逮 1 人"),
    dict(id="kyoiku", name="教育学部", lat=35.710989, lng=139.76100, zone="本乡", holder="民青", str=300, barrier=50, note="民青据点（兵力为推定）；1/18 08:15 太田学部长应待→09:15 令状→机动队約 100 人一巡→11:20 验证終了，无人被捕，押收胶合板盾 18 等"),
    dict(id="rigaku1", name="理学部1号馆", lat=35.71370, lng=139.76298, zone="本乡", holder="反帝学评", str=None, barrier=10, note="1/15 16:00 反帝学评主力約 150 人侵入；1/17 10:00 社学同約 50 人退去入大讲堂、12:00 再封锁；1/18 07:10 机动队到着·07:20 破门，馆内无人"),
] + SITES

# --------------------------------------------------------------------------
# 时间轴（分钟自 1969-01-18 00:00 起算；h 为时:分）
def ev(minute, date, label, text, src, status="published_account", prec="小时", group="", variant=""):
    return dict(minute=minute, date=date, time_label=label, precision=prec, event=text,
                sources=src, evidence_status=status, variant_group=group, variant=variant)

EVENTS = [
    # ---- 1/18 ----
    ev(390, "1969-01-18", "06:30", "警视厅依大学正式要請，在本富士署设总合警备本部；第1—第8机动队及各方面部队 8,000 人、私服 500 人，合计 8,500 人。", ["S1"]),
    ev(390, "1969-01-18", "06:30", "施设部设备課切断占据中及周边建筑的送电（06:45 停水）。", ["S1"]),
    ev(410, "1969-01-18", "06:50", "第1·第2机动队自农学部正门入构，过陆桥向工学部。", ["S1"]),
    ev(423, "1969-01-18", "07:03", "部队自龙冈门、池之端门入构。", ["S1"]),
    ev(425, "1969-01-18", "07:05", "部队自赤门入构。", ["S1"]),
    ev(430, "1969-01-18", "07:10", "机动队抵理学部1号馆；馆内无人，1/9 见证验证至 11:30。", ["S1"]),
    ev(432, "1969-01-18", "07:12", "弥生门路障撤去。", ["S1"]),
    ev(440, "1969-01-18", "07:20", "医学部1号馆（学生5人逮捕）与3号馆解除；中央馆塔屋 16 人抵抗。", ["S1"]),
    ev(500, "1969-01-18", "08:20", "医学部中央馆塔屋 16 人全员逮捕（約 08:30）。", ["S1"]),
    ev(480, "1969-01-18", "08:00", "对大讲堂形成包围；各所发射催泪弹，直升机上空投弹。", ["S1"]),
    ev(530, "1969-01-18", "08:50", "工学部列品馆排除开始：社学同 ML 派以投石、燃烧瓶、瓦斯管自制火焰喷射器抵抗。", ["S1"]),
    ev(540, "1969-01-18", "09:00", "放水车 10 数台向大讲堂放水。", ["S1"]),
    ev(545, "1969-01-18", "09:15", "教育学部解除（09:15 令状、机动队約 100 人一巡、11:20 验证終了）。", ["S1"]),
    ev(540, "1969-01-18", "09:00", "法学部研究室排除开始（中核派·四托洛）。", ["S1"]),
    ev(660, "1969-01-18", "11:00", "装甲车破壞列品馆路障，部队自后门与法文1号馆突入、制压 1 楼。", ["S1"]),
    ev(520, "1969-01-18", "08:40", "列品馆 2·3·4 楼起火，消防车出动（时刻按 11:39 前后报導并列）。", ["S1", "S34"], status="source_conflict", prec="时段"),
    ev(700, "1969-01-18", "11:40", "法学部研究室突入 3 楼；学生在屋顶浇汽油纵火。", ["S1"]),
    ev(780, "1969-01-18", "13:00", "列品馆屋顶突入，逮捕 32 人（女 3、重伤 2）；学生喊「瓦斯弹直击伤及学友，停止攻击，无条件投降」。", ["S1"]),
    ev(810, "1969-01-18", "13:30", "神田：逃入明大·中大的学生增至約 1,500 人，喊「攻击警视厅」；自东大抽调机动队 900 人，合計 2,000 人阻止。", ["S1"]),
    ev(800, "1969-01-18", "13:20", "对大讲堂本格攻击开始；装甲车接近庶務部入口，被燃烧瓶点燃。", ["S1"]),
    ev(875, "1969-01-18", "14:35", "直升机散布铁桶催泪液。", ["S1"]),
    ev(920, "1969-01-18", "15:20", "正面攻击。", ["S1"]),
    ev(930, "1969-01-18", "15:30", "背面 2 處約 50 人突入。", ["S1"]),
    ev(935, "1969-01-18", "15:35", "法学部研究室屋顶突入，逮捕 121 人（中核派·四托洛）。", ["S1"]),
    ev(970, "1969-01-18", "16:10", "大讲堂 2 楼被侵入。", ["S1"]),
    ev(980, "1969-01-18", "16:20", "电锯破门。", ["S1"]),
    ev(1050, "1969-01-18", "17:30", "警备本部下令中止，部队退去（S34 作 17:10 中止、17:19 广播重开）。", ["S1", "S34"], status="source_conflict"),
    ev(1140, "1969-01-18", "19:00", "放水车配置，断续放水至翌朝。", ["S1"]),
    ev(1290, "1969-01-18", "21:30", "加藤总长代行发表声明：退去期限延至 20 日 10 时。", ["S1"]),
    ev(1439, "1969-01-18", "23:59", "本乡构内逮捕 273 人（S1 日末统计，无具体时刻，此处置于日末）。", ["S1"], prec="日"),
    # ---- 1/19 ----
    ev(1800, "1969-01-19", "06:00", "机动队在大讲堂周边重新集结。", ["S1"]),
    ev(1860, "1969-01-19", "07:00", "放水再开；部队自南北突入。", ["S1"]),
    ev(1980, "1969-01-19", "09:00", "放水达 5 楼；直升机风压支援；装甲车接近；木造隧道施设。", ["S1"]),
    ev(2000, "1969-01-19", "09:20", "各层楼梯街垒加固；部队以绳索·电动电钻·切割机拆除。", ["S1"]),
    ev(1980, "1969-01-19", "09:00", "神田：过夜约 800 人行动开始，御茶之水站与明大通一帶构筑 10 處街垒。", ["S1"]),
    ev(2160, "1969-01-19", "12:00", "2 楼 20 数人被捕（一說 12:15）。", ["S1", "S34"], status="source_conflict"),
    ev(2215, "1969-01-19", "12:55", "3 楼学生部付近被制压。", ["S1"]),
    ev(2210, "1969-01-19", "12:50", "神田：御茶之水橋都电被拦停、一时占据；本乡2丁目冲突。", ["S1"]),
    ev(2270, "1969-01-19", "13:50", "南側 2→3 楼楼梯激战。", ["S1"]),
    ev(2325, "1969-01-19", "14:45", "3 楼街垒撤去；15 时頃馆内 200 人以上被捕。", ["S1"]),
    ev(2355, "1969-01-19", "15:35", "4→5 楼；北側屋顶抵抗約 10 分鐘停止。", ["S1"]),
    ev(2370, "1969-01-19", "15:50", "守备队全部被捕（S34；S1 作 15:00 过后 200 人以上、15:35 推进）。", ["S34", "S1"], status="source_conflict"),
    ev(2430, "1969-01-19", "16:30", "5 楼南側屋顶＝反帝学评、6 楼阳台＝社学同；唱国际歌、反帝学评領袖演说。", ["S1"]),
    ev(2487, "1969-01-19", "17:27", "钟楼突入。", ["S1"]),
    ev(2500, "1969-01-19", "17:40", "南側屋顶与 6 楼阳台 60 人逮捕。", ["S1"]),
    ev(2505, "1969-01-19", "17:45", "钟楼屋顶共产同数人被捕——最后一人。", ["S1"]),
    ev(2580, "1969-01-19", "19:00", "公安部验证至 21:00：押收 25 件 901 点、敷石等 14 袋、无炸药。", ["S1"]),
    ev(2580, "1969-01-19", "19:00", "神田：本乡2·3丁目两次冲突（18:42—20:00）、街垒至 22 时撤除；至夜间 75 人逮捕。", ["S1"]),
    # ---- 收束 ----
    ev(2880, "1969-01-20", "10:00", "退去期限（18 日 21:30 声明）。", ["S1"]),
    ev(2970, "1969-01-20", "11:30", "佐藤首相·坂田文相一行自龙冈门来学約 1 小时，加藤案内视察安田讲堂、法研。", ["S1"]),
    ev(2970, "1969-01-20", "11:30", "文部省与东大会談，入試中止最終决定（S27 二传说，C 级）。", ["S27"], status="unverified"),
]

EVENTS += [
    ev(560, "1/18", "09:20", "驹场代表团系约 300 人示威；11:00 明大和泉约 50 人正门前静坐，驹场学生加入超 100 人。", ["S1"]),
    ev(575, "1/18", "09:35", "神田：明大学生会馆出发约 150 人袭御茶之水站前派出所，破玻璃约 15 分后退去。", ["S1"], prec="分钟"),
    ev(590, "1/18", "09:50", "神田：中大社学同约 100 人掘 YMCA 前铺石，袭御茶之水与骏河台下派出所。", ["S1"], prec="分钟"),
    ev(660, "1/18", "11:00", "神田：日大共斗约 50 人＋社学同约 150 人示威，正午前机动队发射催泪弹。", ["S1"]),
    ev(810, "1/18", "13:30", "神田：逃入明大/中大者约 1,500 人喊「警视厅攻击」；东大从机动队 900 人增派，以 2,000 人阻止。", ["S1"], prec="分钟"),
    ev(1070, "1/18", "17:50", "神田：私服警官 1 人被带入明大学生会馆，机动队约 200 人突入救出。", ["S1"], prec="分钟"),
    ev(1200, "1/18", "20:00", "神田：主力撤回中大，决议「明日再攻东大」，22 时解散。", ["S1"]),
    ev(1980, "1/19", "09:00", "神田：明大·日大过夜约 800 人行动开始，御茶之水站与明大通一带街垒 10 处。", ["S1"], prec="分钟"),
    ev(2210, "1/19", "12:50", "神田：御茶之水桥拦停都电、赶下司机车掌；本乡2丁目冲突，至夜 75 人逮捕。", ["S1"], prec="分钟"),
    ev(2562, "1/19", "18:42", "神田：本乡2·3丁目两次冲突，街垒维持至 22 时。", ["S1"], prec="分钟"),
    ev(2760, "1/19", "22:00", "神田：机动队趁总会后撤离时一齐推进，街垒撤除。", ["S1"]),
]

# --------------------------------------------------------------------------
# 数字
# --------------------------------------------------------------------------
def fig(side, metric, value, qualifier, scope, note, src, status="published_account"):
    return dict(side=side, metric=metric, value=value, qualifier=qualifier, scope=scope,
                note=note, sources=src, evidence_status=status)

FIGURES = [
    fig("机动队", "出动兵力", 8500, "人", "1969-01-18 06:30 总合警备本部", "第1—第8机动队 8,000＋私服 500；不是同一时刻投入正面的人数。", ["S1"]),
    fig("机动队", "出动兵力（細目）", 8513, "人", "18 日全日", "S34 細目：8 队 4,678＋另两方面 2,565＋预备与干部 1,000 餘；与 S1 总数差 13 人。", ["S34"], "source_conflict"),
    fig("机动队", "战车·放水车", 12, "辆", "18 日", "S34 作 12 辆水龙车；S1 只作「10 数台」。", ["S34", "S1"], "source_conflict"),
    fig("机动队", "催泪弹", 10000, "发", "18 日", "朝日新闻引述（二手，C 级）；S34 作 10,528 发、瓦斯銃 500 支。", ["S27", "S34"], "unverified"),
    fig("机动队", "警察側负伤", 653, "人", "18—19 日", "国会答辩（荒木萬壽夫 1969-03-25）：「六百五十三名、内入院 37 名」。", ["S2"]),
    fig("全共斗", "讲堂内逮捕", 397, "人", "19 日", "S34 数字；S1 未给馆内总数，只给「200 人以上」与分楼层逮捕。", ["S34"]),
    fig("全共斗", "讲堂内逮捕（另说）", 374, "人", "19 日", "S35 数字。", ["S35"], "source_conflict"),
    fig("全共斗", "屋顶逮捕", 90, "人", "19 日 17:30", "S34：「頂层平台上約 90 名青年学生全部被捕」。", ["S34"]),
    fig("全共斗", "本乡构内逮捕", 273, "人", "18 日", "S1 日末统计。", ["S1"]),
    fig("全共斗", "大讲堂逮捕", 469, "人", "19 日", "S1 日末「其他」栏。", ["S1"]),
    fig("全共斗", "检举总数", 633, "人", "18—19 日", "警视厅记录（S34 引）；其中东大生 38 人。", ["S34"]),
    fig("全共斗", "检举总数（另说）", 983, "人", "18—19 日", "S35 数字（含神田）。", ["S35"], "source_conflict"),
    fig("全共斗", "起訴", 607, "人", "最終", "最高裁刑事局；1969-03 时点 509 人。", ["S3"]),
    fig("全共斗", "学生负伤（重伤）", 76, "人", "18—19 日", "S34：「失明 1 人、重伤 76 人」；另「面部被瓦斯弹击中者 18 名」。", ["S34"]),
    fig("全共斗", "东大事件受理", 984, "人", "1969-01-09—19", "犯罪白书（檢察阶段受理，非逮捕数）。", ["S41"]),
    fig("市民", "物件損害", 450000000, "日元", "18—19 日", "国会答辩（冈沢完治 1969-03-19）：「四億五千萬圆」。", ["S2"]),
]

# --------------------------------------------------------------------------
# 缺口
# --------------------------------------------------------------------------
GAPS = [
    ("各层人数", "讲堂 3—5 层各派人数与屋頂 90 人的派系构成", "S34/S35 均未給；S1 只給分楼层逮捕", "B01"),
    ("指揮系統", "学生側总指揮与各派部队的实际指揮關係", "S34 称本乡学生队长對党派部队无指揮权；上层未见成文命令", "B02"),
    ("闭回路", "馆内厕所·飲水·补给的实际状况", "S34 明确「连水都沒有儲备」；S1 只記 06:45 停水", "B03"),
    ("警方計劃", "警备实施要領（部队分区、时刻表）", "未公开；东京都公文书馆/情报公开請求", "B04"),
    ("照片", "1969-01-18/19 现场照片", "版权在共同通信/朝日，仅限法人", "B05"),
    ("现场直播", "NHK 是否「现场直播」及其节目名", "S46 两日节目表无独立现场直播；仅特别节目与新闻焦点", "B06"),
    ("时刻異文", "18 日中止时刻（17:10/17:30/17:40）、19 日結束（17:45/17:46）", "S1 与 S34 直接冲突，并列不裁决", "B07"),
]

# --------------------------------------------------------------------------
# 写 pack
# --------------------------------------------------------------------------
def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def scenario_obj():
    return {
        "id": SCEN_ID,
        "name": BATTLE,
        "track": "全共斗（守）／警视厅机动队（攻）",
        "kind": "都市内构内要塞攻防（逐馆解除→逐层制压）",
        "scope": "1969-01-18 06:30 至 1969-01-19 18:00 的构内攻防；含列品馆·法学部研究室·法文2号馆·医学部·教育学部等逐馆解除，以及神田（御茶之水）方面的兵力抽调。1/20 以后只作收束节点。",
        "aliases": ["安田講堂攻防戦", "東大安田講堂事件", "安田講堂落城"],
        "sources": ["S1", "S34", "S35", "S41", "S43", "S46", "S2", "S3", "S27"],
        "forces": [
            {"side": f["side"], "unit": f["unit"], "description": f["desc"],
             "sources": f["src"], "evidence_status": "published_account",
             "source_locator": {}}
            for f in FORCES
        ],
        "events": [
            {"date": e["date"], "time_label": e["time_label"], "precision": e["precision"],
             "event": e["event"], "sources": e["sources"], "evidence_status": e["evidence_status"],
             "source_locator": {}}
            for e in EVENTS
        ],
        "figures": [
            {"side": f["side"], "metric": f["metric"], "value": f["value"], "qualifier": f["qualifier"],
             "scope": f["scope"], "note": f["note"], "sources": f["sources"],
             "evidence_status": f["evidence_status"]}
            for f in FIGURES
        ],
        "outcome": "19 日 17:45 钟楼屋顶最后数人被捕，安田讲堂被制压；本乡构内 273（18 日）＋469（19 日）逮捕，检举总数据警视厅作 633，其中东大生 38 人。攻方达成「解除占据」目标，但抽调 900 人赴神田使正面攻勢在 18 日未能决著。",
        "geography": "本乡构内（文京区本乡7-3-1）；正门（西）—银杏并木—安田讲堂—御殿下（东）为东西軸线。讲堂正面朝西，1·2 层在崖下、3 层以上在台地，正面玄関在 3 层（与 1 层高差約 6 m）。坐標为现代 OSM 輪廓与史料方位推定，不是 1969 年測量圖。",
        "equipment": "攻方：放水车·装甲车·催泪弹·直升机·电锯·电钻·绳索·扩声器。守方：燃烧瓶·投石·硫酸·竹枪·石膏·手制火焰喷射器·角材·桌椅街垒·铁扉焊接。",
        "modeling": "教学目標：比較（1）逐馆解除的順序對讲堂攻略时刻的影響；（2）13:30 抽调 900 人赴神田的代價；（3）停电停水与街垒修复的此消彼长。反事实每次只改一个条件，保留相同初始兵力与时刻表。",
        "uncertainties": [
            "各层人数与屋頂派系构成未詳（S34/S35 均缺）。",
            "18 日中止时刻：S1 17:30／S34 17:10，并列。",
            "馆内 397（S34）／374（S35）／「約 400」三說。",
            "检举 633（S34）／983（S35）。",
            "神田方面細节（街垒 10 處、75 人逮捕）仅 S1 一家，未见警方文书。",
        ],
        "points": ["yasuda_hall", "main_gate", "akamon", "ryuokomon", "ikenohata", "yayoi",
                   "houbun2", "houbun1", "reppinkan", "igakubu_center", "igakubu_honkan",
                   "kogakubu1", "kyoyo_gym", "ochanomizu"],
        "time_step": "30分钟",
        "geometry": {
            "contact_km": 0.05,
            "control_radius_km": 0.04,
            "encircle_radius_km": 0.30,
            "retreat_check_km": 0.40,
            "sealed_ratio_encircled": 0.85,
            "sealed_ratio_partial": 0.50,
            "terrain_factor": 1.35,
        },
        "preset_note": "几何參数按校園尺度（数百公尺）縮放；contact_km 只判「是否接觸」，不是射程。",
        "parameter_status": "teaching_estimate",
    }


def build():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(CORPUS, exist_ok=True)
    os.makedirs(ADJ, exist_ok=True)
    os.makedirs(GENT, exist_ok=True)

    # --- scenarios.json ---
    sc = scenario_obj()
    write_json(os.path.join(DATA, "scenarios.json"), {
        "schema_version": SCHEMA_VERSION,
        "title": "Gentactix-DSH 战役包·安田讲堂攻防战（1969.01.18—01.19）",
        "checked": CHECKED,
        "use": "公开史料核读；不是窮盡檔案，也不是学术定論。教学用几何裁决，不宣稱战損精算。",
        "scenarios": [sc],
        "evidence_levels": {
            "published_account": "公开文献记载；未核原始命令或逐人名册",
            "source_conflict": "来源有异文；不得并作唯一事实",
            "teaching_window": "教学窗口；不是已核定历史时刻",
            "unverified": "未核得；不得填零或反推确数",
        },
    })

    # --- sources.json ---
    write_json(os.path.join(DATA, "sources.json"), {
        "scope": "公开史料与官方统计核读；来源按主张逐项使用，未核档案另列缺口。",
        "sources": SOURCES,
    })

    # --- timeline.csv ---
    write_csv(os.path.join(DATA, "timeline.csv"),
              ["scenario_id", "battle", "date", "time_label", "precision", "event",
               "source_ids", "evidence_status", "variant_group", "variant"],
              [[SCEN_ID, BATTLE, e["date"], e["time_label"], e["precision"], e["event"],
                "|".join(e["sources"]), e["evidence_status"], e["variant_group"], e["variant"]]
               for e in sorted(EVENTS, key=lambda x: (x["date"], x["minute"]))])

    # --- forces.csv ---
    write_csv(os.path.join(DATA, "forces.csv"),
              ["scenario_id", "side", "unit", "description", "source_ids", "evidence_status"],
              [[SCEN_ID, f["side"], f["unit"], f["desc"], "|".join(f["src"]), "published_account"]
               for f in FORCES])

    # --- figures.csv ---
    write_csv(os.path.join(DATA, "figures.csv"),
              ["scenario_id", "side", "metric", "value", "qualifier", "scope", "source_ids",
               "note", "evidence_status"],
              [[SCEN_ID, f["side"], f["metric"], f["value"], f["qualifier"], f["scope"],
                "|".join(f["sources"]), f["note"], f["evidence_status"]] for f in FIGURES])

    # --- verification_gaps.csv ---
    write_csv(os.path.join(DATA, "verification_gaps.csv"),
              ["gap_id", "topic", "detail", "status", "next_source"],
              [[g[3], g[0], g[1] + "；" + g[2], "open", g[3]] for g in GAPS])

    # --- INDEX.md / README.md ---
    with io.open(os.path.join(DATA, "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("# 索引：安田讲堂攻防战（%s）\n\n" % SCEN_ID)
        f.write("| 文件 | 说明 |\n|---|---|\n")
        f.write("| `scenarios.json` | 编辑源（schema v%s）；forces/events/figures 全文 |\n" % SCHEMA_VERSION)
        f.write("| `sources.json` | 来源登记（S1/S2/S3/S27/S34/S35/S41/S43/S46） |\n")
        f.write("| `timeline.csv` | %d 条事件（1/18—1/20） |\n" % len(EVENTS))
        f.write("| `forces.csv` | %d 个编组 |\n" % len(FORCES))
        f.write("| `figures.csv` | %d 个数字（含异文与未核） |\n" % len(FIGURES))
        f.write("| `verification_gaps.csv` | %d 项缺口 |\n" % len(GAPS))
        f.write("\n配套：`corpus/%s.md`（史料卡）、`adjudication/%s.md`（裁决参数卡）、`gentactix/yasuda_anchors.json`（地名锚点）、`推演展示_安田讲堂.html`（可玩演示）。\n" % (BATTLE, BATTLE))

    with io.open(os.path.join(DATA, "README.md"), "w", encoding="utf-8") as f:
        f.write("# 安田讲堂攻防战：数据说明\n\n")
        f.write("本目录是 Gentactix-DSH 结构的战役包，供 RAG（corpus）与几何裁决（adjudication + geometry）使用。\n\n")
        f.write("## 与仓库其它战役的差异\n\n")
        f.write("- 尺度不同：其它战役是数十至数百公里的运动战；本战役是 **0.4 km × 0.5 km 的构内攻防**，故 `geometry` 以 0.05/0.04 km 为单位。\n")
        f.write("- 目标不同：攻方不是求歼，而是 **逐馆解除→逐层制压**；故 timeline 以「馆/层」为进展单位。\n")
        f.write("- 证据密度不同：本战役有官方逐日日志（S1）＋当事者回忆（S34）＋研究（S35），可交叉之处远多于普通战役，但也因此**异文更多**（见 figures 的 source_conflict 行）。\n\n")
        f.write("## 三条纪律\n\n")
        f.write("1. `null` 表示未核得，不得填 0，不得反推确数。\n2. `source_conflict` 行只并列，不裁决；演示里也不许把两说合成一数。\n3. hp/兵力/士气不是史料值，是教学初态；在界面上必须与史料数字分栏显示。\n")

    # --- corpus ---
    corpus_md = os.path.join(CORPUS, BATTLE + ".md")
    with io.open(corpus_md, "w", encoding="utf-8") as f:
        f.write("# 安田讲堂攻防战（1969.01.18—01.19）\n\n")
        f.write("## 一句话\n\n1969 年 1 月 18—19 日，警视厅以 8,500 人解除东京大学本乡构内被学生占据的安田讲堂等 17 栋建筑；19 日 17:45 钟楼屋顶最后数人被捕。\n\n")
        f.write("## 双方\n\n")
        f.write("- 攻方：警视厅机动队第1—第8队 8,000 人＋私服 500 人（S1）；另有装甲车、放水车 10 数台、直升机。\n")
        f.write("- 守方：东大全共斗（无執行部、代表会议制）＋中核派·社学同·反帝学评·革马派·社学同 ML 派等；讲堂内混合部队，并存的粘合劑是「共同的敵人民青」（S35）。\n")
        f.write("- 第三方：民青同（日本共產党系）守医学部本馆，与全共斗敵對（S1、S45）。\n\n")
        f.write("## 时间线（要点）\n\n")
        for e in sorted(EVENTS, key=lambda x: (x["date"], x["minute"])):
            f.write("- %s %s（%s）：%s［%s］\n" % (e["date"][5:], e["time_label"], e["evidence_status"], e["event"], "、".join(e["sources"])))
        f.write("\n## 結果\n\n" + sc["outcome"] + "\n\n")
        f.write("## 爭议\n\n")
        for u in sc["uncertainties"]:
            f.write("- " + u + "\n")
        f.write("\n## 数字（含異文）\n\n| 方 | 指标 | 值 | 口径 | 出处 | 状态 |\n|---|---|---|---|---|---|\n")
        for x in FIGURES:
            f.write("| %s | %s | %s %s | %s | %s | %s |\n" % (x["side"], x["metric"], x["value"], x["qualifier"], x["scope"], "、".join(x["sources"]), x["evidence_status"]))

    # --- adjudication ---
    adj_md = os.path.join(ADJ, BATTLE + ".md")
    with io.open(adj_md, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("battle_name: %s\n" % BATTLE)
        f.write("aliases: 安田讲堂攻防战|东大安田讲堂事件|安田讲堂落城\n")
        f.write("era: 战后日本·全共斗期（1968—1969）\n")
        f.write("time_step: 30分钟\n")
        f.write("source_ref: corpus/%s.md\n" % BATTLE)
        f.write("updated: %s\n" % CHECKED)
        f.write("validation_status: teaching_estimate\n")
        f.write("note: 校園尺度几何工作估計；不实现催泪氣体擴散、火災蔓延、楼板承載或逐人伤亡\n")
        for k, v in sc["geometry"].items():
            f.write("%s: %s\n" % (k, v))
        f.write("---\n\n")
        f.write("# 安田讲堂攻防战：裁决工作参数\n\n")
        f.write("## 使用范围\n\n建议局部回合 30 分钟；一场完整推演 01-18 06:30—01-19 18:00 共 71 回合。只对所选时段内的局部部队运行几何检查，不同日期的兵力不得叠加成「同时在场」。\n\n")
        f.write("## 计算边界\n\n`contact_km` 只判「是否接触」，不是射程；`control_radius_km` 是街垒与火力对街道的控制下限；`encircle_radius_km`/`retreat_check_km` 用于判断某馆是否被封死、退路是否还开着。`terrain_factor` 记的是「台地—崖下」的高差与楼梯瓶颈，不是坡度测量。\n\n")
        f.write("**不裁决伤亡数字。** 史料的 653／76／397 是人事统计，不是逐回合扣减表；本包只裁决「位置、接触、切断、被围、退路、崩溃」六类离散状态。\n\n")
        f.write("## 初始化与结果\n\n初态取自 1969-01-18 06:30：8,500 人已在构外集结，守方分据讲堂（1—6 层）、法研、列品馆、法文 2 号馆、医学部中央馆。兵力为教学初态，与史料数字分栏显示；未核人数保持 `null`。\n\n## 史料\n\n`corpus/%s.md`；来源登记见 `sources.json`。\n" % BATTLE)

    # --- anchors ---
    anchors = {
        "checked": CHECKED,
        "display_crs": "WGS84",
        "precision_note": "校園內点位取自现代 OSM 輪廓与史料方位推定；不是 1969 年測量圖，誤差圈为工作估計。",
        "sources": {
            "osm": {"url": "https://www.openstreetmap.org/", "license": "ODbL 1.0",
                    "attribution": "© OpenStreetMap contributors", "accessed": CHECKED},
            "gsi": {"url": "https://maps.gsi.go.jp/development/ichiran.html",
                    "license": "国土地理院コンテンツ利用規約", "attribution": "国土地理院", "accessed": CHECKED},
        },
        "points": {
            "yasuda_hall": {"name": "安田讲堂", "coordinates": [35.713428, 139.762297], "kind": "1975 年以前原位置（现存）",
                            "uncertainty_km": 0.01, "identity_sources": ["S1", "S21"],
                            "note": "正面朝西（正门·银杏并木）、背面东（御殿下）。1·2 层在崖下、3 层以上台地，正面玄関在 3 层。"},
            "main_gate": {"name": "正门", "coordinates": [35.712941, 139.759660], "kind": "构内门", "uncertainty_km": 0.01, "identity_sources": ["S1"]},
            "akamon": {"name": "赤门", "coordinates": [35.710592, 139.760359], "kind": "构内门", "uncertainty_km": 0.01, "identity_sources": ["S1"]},
            "ryuokomon": {"name": "龙冈门（推定）", "coordinates": [35.71180, 139.76400], "kind": "构内门（方位推定）", "uncertainty_km": 0.10, "identity_sources": ["S1"]},
            "ikenohata": {"name": "池之端门（推定）", "coordinates": [35.71250, 139.76470], "kind": "构内门（方位推定）", "uncertainty_km": 0.10, "identity_sources": ["S1"]},
            "yayoi": {"name": "弥生门（推定）", "coordinates": [35.71500, 139.76150], "kind": "构内门（方位推定）", "uncertainty_km": 0.10, "identity_sources": ["S1"]},
            "houbun2": {"name": "法文2号馆（推定）", "coordinates": [35.71300, 139.76060], "kind": "建物（现輪廓未收）", "uncertainty_km": 0.08, "identity_sources": ["S1"]},
            "houbun1": {"name": "法文1号馆", "coordinates": [35.713458, 139.760910], "kind": "建物（现存）", "uncertainty_km": 0.02, "identity_sources": ["S1"]},
            "reppinkan": {"name": "工学部列品馆", "coordinates": [35.71395, 139.76035], "kind": "建物（现存、今工学部本部）", "uncertainty_km": 0.03, "identity_sources": ["S1", "S22"]},
            "igakubu_center": {"name": "医学部综合中央馆", "coordinates": [35.710798, 139.763260], "kind": "建物（现存）", "uncertainty_km": 0.02, "identity_sources": ["S1"]},
            "igakubu_honkan": {"name": "医学部本馆（推定）", "coordinates": [35.71080, 139.76180], "kind": "建物（位置推定）", "uncertainty_km": 0.10, "identity_sources": ["S1"]},
            "kogakubu1": {"name": "工学部1号馆", "coordinates": [35.714231, 139.760060], "kind": "建物（现存）", "uncertainty_km": 0.02, "identity_sources": ["S1"]},
            "kyoyo_gym": {"name": "教養学部（驹场·参考）", "coordinates": [35.660500, 139.685200], "kind": "构外参考", "uncertainty_km": 0.50, "identity_sources": ["S1"]},
            "ochanomizu": {"name": "御茶之水站前（神田战场·参考）", "coordinates": [35.699000, 139.764300], "kind": "构外战场（参考点）", "uncertainty_km": 0.30, "identity_sources": ["S1"]},
        },
        "campaigns": {BATTLE: {"points": sc["points"]}},
    }
    write_json(os.path.join(GENT, "yasuda_anchors.json"), anchors)

    # --- 推演展示 HTML ---
    pack = {
        "battle": BATTLE,
        "scenario": sc,
        "sources": SOURCES,
        "forces": [dict(id="U%02d" % (i + 1), **{k: f[k] for k in
                     ("side", "unit", "desc", "n", "lat", "lng", "conf", "src", "zone")},
                     floor=f.get("floor"), sect=f.get("sect", f["side"]), nunit=f.get("nunit", "人")) for i, f in enumerate(FORCES)],
        "events": sorted(EVENTS, key=lambda x: x["minute"]),
        "zones": ZONES,
        "sites": SITES,
        "buildings": BUILDINGS,
        "floors0": FLOORS0,
        "figures": FIGURES,
        "gaps": GAPS,
    }
    tpl_path = os.path.join(OUT, "sim_template.html")
    with io.open(tpl_path, encoding="utf-8") as f:
        tpl = f.read()
    html = tpl.replace("__PACK__", json.dumps(pack, ensure_ascii=False))
    geo_path = os.path.join(OUT, "..", "data", "key_buildings.geojson")
    geo = "{\"type\":\"FeatureCollection\",\"features\":[]}"
    if os.path.exists(geo_path):
        with io.open(geo_path, encoding="utf-8") as f:
            geo = f.read()
    html = html.replace("__GEO__", geo)
    out_html = os.path.join(OUT, "推演展示_安田讲堂.html")
    with io.open(out_html, "w", encoding="utf-8") as f:
        f.write(html)

    print("scenarios.json / sources.json / 4 CSV / INDEX / README  ->", DATA)
    print("corpus ->", corpus_md)
    print("adjudication ->", adj_md)
    print("anchors ->", os.path.join(GENT, "yasuda_anchors.json"))
    print("html ->", out_html, os.path.getsize(out_html), "bytes")
    print("events:", len(EVENTS), "forces:", len(FORCES), "figures:", len(FIGURES), "gaps:", len(GAPS))


if __name__ == "__main__":
    build()
