# -*- coding: utf-8 -*-
"""安田讲堂战役包结构校验（对应 Gentactix-DSH verify_* 的检查思路）。

检查：schema、必填字段、来源引用闭合、CSV 与 JSON 一致、corpus/adjudication 配套、
anchors 点位可解析、HTML 内联 JSON 可解析、null 不得为 0 的安全网。
用法：python verify_yasuda_campaign.py   （退出码 0 = 全通过）
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data", "yasuda_battle")
CORPUS = os.path.join(ROOT, "corpus")
ADJ = os.path.join(ROOT, "adjudication")
BATTLE = "安田讲堂攻防战-1969.01.18至1969.01.19"
EVIDENCE = {"published_account", "source_conflict", "teaching_window", "unverified"}
GEOM_KEYS = {"contact_km", "control_radius_km", "encircle_radius_km", "retreat_check_km",
             "sealed_ratio_encircled", "sealed_ratio_partial", "terrain_factor"}
REQ_SCENARIO = {"id", "name", "track", "kind", "scope", "sources", "forces", "events",
                "figures", "outcome", "geography", "equipment", "modeling",
                "uncertainties", "points", "time_step", "geometry"}

fails, warns, checks = [], [], 0


def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def jload(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    # ---------- scenarios ----------
    sc_path = os.path.join(DATA, "scenarios.json")
    ck(os.path.exists(sc_path), "缺 scenarios.json")
    doc = jload(sc_path)
    ck(doc.get("schema_version") == 2, "schema_version 不是 2")
    ck(isinstance(doc.get("scenarios"), list) and doc["scenarios"], "scenarios 为空")
    ck("evidence_levels" in doc, "缺 evidence_levels")
    sc = doc["scenarios"][0]
    miss = REQ_SCENARIO - set(sc)
    ck(not miss, "scenario 缺字段: %s" % sorted(miss))
    ck(sc["id"] == "YS01", "scenario id 应为 YS01")
    ck(set(sc["geometry"]) == GEOM_KEYS, "geometry 键不齐: %s" % sorted(set(sc["geometry"]) ^ GEOM_KEYS))
    for k, v in sc["geometry"].items():
        ck(isinstance(v, (int, float)) and v > 0, "geometry.%s 非正数" % k)
    ck(sc["geometry"]["sealed_ratio_encircled"] > sc["geometry"]["sealed_ratio_partial"], "封锁阈值关系错")

    # ---------- sources 闭合 ----------
    src = jload(os.path.join(DATA, "sources.json"))
    sids = set(src["sources"])
    used = set(sc["sources"])
    for f in sc["forces"]:
        used |= set(f.get("sources", []))
    for e in sc["events"]:
        used |= set(e.get("sources", []))
    for f in sc["figures"]:
        used |= set(f.get("sources", []))
    ck(used <= sids, "引用了未登记的来源: %s" % sorted(used - sids))
    for s in src["sources"].values():
        ck(s.get("title") and s.get("evidence_type"), "来源缺 title/evidence_type")

    # ---------- 枚举 ----------
    for e in sc["events"]:
        ck(e.get("evidence_status") in EVIDENCE, "event evidence_status 非法: %r" % e.get("evidence_status"))
        ck(bool(e.get("event")) and bool(e.get("date")), "event 缺正文/日期")
    for f in sc["figures"]:
        ck(f.get("evidence_status") in EVIDENCE, "figure evidence_status 非法: %r" % f.get("evidence_status"))
        ck(f.get("value") is not None, "figure %s 的值是 null（不得填 0，但也不该缺行）" % f.get("metric"))
    for f in sc["forces"]:
        ck(f.get("side") and f.get("unit") and f.get("description"), "force 字段不全: %r" % f.get("unit"))

    # ---------- CSV 与 JSON 一致 ----------
    def rows(name, header):
        p = os.path.join(DATA, name)
        ck(os.path.exists(p), "缺 %s" % name)
        with io.open(p, encoding="utf-8-sig", newline="") as f:
            r = csv.reader(f)
            head = next(r)
            ck(head == header, "%s 表头不符: %s" % (name, head))
            return list(r)

    tl = rows("timeline.csv", ["scenario_id", "battle", "date", "time_label", "precision",
                               "event", "source_ids", "evidence_status", "variant_group", "variant"])
    ck(len(tl) == len(sc["events"]), "timeline.csv 行数 %d != events %d" % (len(tl), len(sc["events"])))
    def _m(lbl):
        mm = re.match(r"^(\d{1,2}):(\d{2})$", (lbl or "").strip())
        return int(mm.group(1)) * 60 + int(mm.group(2)) if mm else -1
    keys = [(r[2], _m(r[3])) for r in tl]
    ck(keys == sorted(keys), "timeline.csv 未按日期/时刻排序（解析后分钟序）")
    for r in tl:
        ck(r[0] == "YS01" and r[1] == BATTLE, "timeline.csv scenario_id/battle 不一致")
        ck(r[7] in EVIDENCE, "timeline.csv evidence_status 非法: %s" % r[7])

    fo = rows("forces.csv", ["scenario_id", "side", "unit", "description", "source_ids", "evidence_status"])
    ck(len(fo) == len(sc["forces"]), "forces.csv 行数不符")
    ck(len({r[2] for r in fo}) == len(fo), "forces.csv 单位名重复")

    fg = rows("figures.csv", ["scenario_id", "side", "metric", "value", "qualifier", "scope",
                              "source_ids", "note", "evidence_status"])
    ck(len(fg) == len(sc["figures"]), "figures.csv 行数不符")
    for r in fg:
        ck(r[3].strip() != "", "figures.csv 有空值（应用 null 之外的口径说明）")
        ck(r[8] in EVIDENCE, "figures.csv evidence_status 非法: %s" % r[8])

    gp = rows("verification_gaps.csv", ["gap_id", "topic", "detail", "status", "next_source"])
    ck(len(gp) >= 5, "缺口表太少")
    ck(len({r[0] for r in gp}) == len(gp), "缺 gap_id 重复")

    # ---------- corpus / adjudication ----------
    cpath = os.path.join(CORPUS, BATTLE + ".md")
    ck(os.path.exists(cpath), "缺 corpus 史料卡")
    ctext = io.open(cpath, encoding="utf-8").read()
    ck(ctext.count("\n## ") >= 4, "corpus 二级标题过少（RAG 切片会太少）")
    ck("S1" in ctext, "corpus 未引 S1")

    apath = os.path.join(ADJ, BATTLE + ".md")
    ck(os.path.exists(apath), "缺 adjudication 参数卡")
    atext = io.open(apath, encoding="utf-8").read()
    fm = atext.split("---")[1] if atext.startswith("---") else ""
    for k in GEOM_KEYS:
        m = re.search(r"^%s:\s*([0-9.]+)" % k, fm, re.M)
        ck(bool(m), "adjudication 缺 %s" % k)
        if m:
            ck(abs(float(m.group(1)) - float(sc["geometry"][k])) < 1e-9, "adjudication 的 %s 与 scenarios.json 不一致" % k)

    # ---------- anchors ----------
    anch = jload(os.path.join(ROOT, "gentactix", "yasuda_anchors.json"))
    pts = anch.get("points", {})
    for p in sc["points"]:
        ck(p in pts, "points 里的 %s 在 anchors 中不存在" % p)
    for k, v in pts.items():
        lat, lng = v["coordinates"]
        ck(30 <= lat <= 46 and 128 <= lng <= 146, "anchors %s 坐标不在日本范围" % k)
    ck(anch.get("display_crs") == "WGS84", "anchors display_crs 应为 WGS84")

    # ---------- HTML ----------
    hp = os.path.join(ROOT, "推演展示_安田讲堂.html")
    ck(os.path.exists(hp), "缺推演展示 HTML")
    h = io.open(hp, encoding="utf-8").read()
    ck("__PACK__" not in h and "__GEO__" not in h, "HTML 模板占位符未被替换")
    m = re.search(r'<script id="pack" type="application/json">(.*?)</script>', h, re.S)
    ck(bool(m), "HTML 内找不到 pack JSON")
    if m:
        pack = json.loads(m.group(1))
        ck(pack["battle"] == BATTLE, "HTML pack battle 名不符")
        ck(len(pack["events"]) == len(sc["events"]), "HTML 事件数与 pack 不符")
        ck(len(pack["forces"]) == len(sc["forces"]), "HTML 编组数与 pack 不符")
    ck("leaflet" in h.lower(), "HTML 未加载 Leaflet")
    # ---------- 多战区与全域可控（对齐 m02637 要求）----------
    zs = pack.get("zones") or []
    ck(len(zs) >= 3, "zones 少于 3 个（本乡/神田/驹场）")
    zids = {z["id"] for z in zs}
    ck({"本乡", "神田", "驹场"} <= zids, "zones 缺 本乡/神田/驹场")
    bs = pack.get("buildings") or []
    ck(len(bs) >= 14, "buildings 少于 14 个")
    ck(all(b.get("zone") in zids for b in bs), "buildings 有 zone 不在 zones 内")
    ck(len({b["id"] for b in bs}) == len(bs), "buildings id 重复")
    ck(any(b.get("floors") for b in bs), "buildings 缺安田讲堂（floors=True）")
    fl = pack.get("floors0") or {}
    ck(set(fl) == {"1","2","3","4","5","6"}, "floors0 不是 1—6 层")
    fs = pack.get("forces") or []
    ck(all(f.get("zone") in zids for f in fs), "forces 有 zone 不在 zones 内")
    REBEL_SIDES = {"全共斗", "反帝学评", "社学同", "中核派", "社学同 ML派", "革马派", "明大共斗"}
    rb = [f for f in fs if f["side"] in REBEL_SIDES]
    mq = [f for f in fs if f["side"] == "民青"]
    ck(len(rb) >= 8, "守方（全共斗系各派）编组少于 8（应含讲堂各层与外区部队）")
    ck(len(mq) >= 4, "民青 编组少于 4")
    ck({"神田", "驹场"} <= {f["zone"] for f in rb}, "守方 未布置到神田/驹场（无法全域控制）")
    ck({"本乡", "驹场"} <= {f["zone"] for f in mq}, "民青 未布置到本乡/驹场（无法对抗）")
    ck(any(b["holder"] == "民青" for b in bs), "buildings 无民青据点")
    ck(all(f.get("sect") for f in fs), "forces 缺 sect 标签（派系着色用）")

    # ---------- 报告 ----------
    print("检查项：%d" % checks)
    for w in warns:
        print("WARN ", w)
    if fails:
        print("FAIL %d 项：" % len(fails))
        for f in fails:
            print("  -", f)
        return 1
    print("全部通过：schema / 来源闭合 / CSV 一致 / corpus / adjudication / anchors / HTML")
    return 0


if __name__ == "__main__":
    sys.exit(main())
