# -*- coding: utf-8 -*-
"""生成 data/*.csv 与 map/安田讲堂攻防战地图.html（离线可读，需联网加载底图瓦片）"""
import json, os, csv, io

BASE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(BASE)          # yasuda/
OUT = BASE
DATA = os.path.join(OUT, "data")
MAPD = os.path.join(OUT, "map")
os.makedirs(DATA, exist_ok=True)
os.makedirs(MAPD, exist_ok=True)

kb = json.load(open(os.path.join(WS, "data", "key_buildings.geojson"), encoding="utf-8"))
kbj = json.load(open(os.path.join(WS, "data", "key_buildings.json"), encoding="utf-8"))

ROLE = {
    "安田講堂": ("学生", "主战场：全共闘/各セクト守备，1/18 13:20 起强攻"),
    "法学部3号館": ("学生", "中核派・四トロ据守，15:35 屋顶逮捕121人"),
    "法学部4号館": ("学生", "法学部封鎖区"),
    "法文1号館": ("学生", "法学部・文学部共用，08:00过解除"),
    "文学部3号館": ("学生", "文学部区"),
    "医学部総合中央館": ("学生", "16人塔屋抵抗，08:30 全员逮捕"),
    "医学部3号館": ("学生", "07:20—08:30 解除"),
    "理学部1号館 西棟": ("学生", "07:10—11:30 解除+现场检证"),
    "理学部1号館 東棟": ("学生", "理学部封鎖区"),
    "理学部4号館": ("学生", "理学部区"),
    "理学部7号館": ("学生", "理学部区"),
    "東京大学教育学研究科・教育学部": ("学生", "08:15—11:20 检证，押収盾18面"),
    "経済学研究科棟": ("学生", "経済学部封鎖区"),
    "東京大学総合図書館": ("学生", "解除记录（细节未载）"),
    "工学部1号館": ("警察", "07:00过解除，逮捕1人"),
    "工学部7号館": ("警察", "07:00过解除"),
    "工学部8号館": ("警察", "07:00过解除"),
    "工学部13号館": ("警察", "工学部区"),
    "工学部前広場": ("警察", "07:40 设指挥车，向讲堂劝降"),
    "医学部前広場": ("警察", "医学部方向集结地"),
    "正門": ("警察", "主攻正面接近路（银杏并木）"),
    "赤門": ("警察", "07:05 入构；通往法学部・経済学部"),
    "銀杏並木": ("警察", "游行路线/正面接近路"),
    "第二食堂": ("中立", "构内通道节点"),
    "山上会館": ("中立", "讲堂北侧"),
    "三四郎池": ("中立", "讲堂西侧地形"),
    "御殿下グラウンド": ("中立", "讲堂东侧（背面突破口方向）"),
}

def role_of(name):
    for k, v in ROLE.items():
        if name == k or name.startswith(k):
            return v
    return ("中立", "")

# ---------- buildings.csv ----------
rows = []
for b in kbj:
    role, note = role_of(b["name"])
    rows.append([b["name"], b.get("lat"), b.get("lon"), b.get("levels") or "", role, note])
with io.open(os.path.join(DATA, "buildings.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["名称", "纬度", "経度", "层数(OSM)", "当日角色", "当日事件"])
    w.writerows(rows)

# ---------- units.csv ----------
units = [
    ["P0", "警視庁 总合警备本部", "警察", "本富士署（构外）", "", "指挥", 35.7078, 139.7596, "S1", "06:30 开设；本部人员未计入 8,500",
     "司令车・无线・现场电话", "构外自有补给", "—"],
    ["P1", "第1—第4机动队", "警察", "農学部正門→工学部", 4000, "突入", 35.7151, 139.7626, "S1", "06:50 入构，逐栋解除工学部；兵力 4,000 为按 8,500 总数推定分兵",
     "ジュラルミン盾・ガス弾・投石防护网", "随队补给车", "高"],
    ["P2", "第5—第6机动队", "警察", "竜岡門→医学部", 2000, "突入", 35.7107, 139.7645, "S1", "07:03 入构；07:20 医学部；兵力 2,000 为推定分兵",
     "ジュラルミン盾・ガス弾", "随队补给车", "高"],
    ["P3", "第7—第8机动队", "警察", "赤門→法学部・文学部", 2000, "突入", 35.7107, 139.7606, "S1", "07:05 入构；08:00 法学部；兵力 2,000 为推定分兵",
     "ジュラルミン盾・ガス弾", "随队补给车", "高"],
    ["P4", "私服警官", "警察", "构内散布", 500, "识别・取证", 35.7130, 139.7610, "S1", "8,500 人中 500",
     "私服・识别证", "—", "高"],
    ["P5", "大讲堂包围队", "警察", "正門側・银杏并木", 1500, "包围・放水", 35.7129, 139.7608, "S1", "08:00 包围；09:00 放水车10余台",
     "放水车10余台・催涙ガス弾（1万发为 C 级报道）", "水源＝构内消火栓（推定）", "高"],
    ["P6", "突入队（南・北）", "警察", "讲堂东侧御殿下", 800, "突入", 35.71342, 139.76330, "S1", "15:30 背面突入；1/19 南北夹击",
     "電気ノコ・電気ドリル・ロープ・切断機・装甲車", "随队补给", "高"],
    ["P7", "机动队 增派", "警察", "神田（明大・中大）", 900, "阻止支援部队", 35.7005, 139.7635, "S1", "1/18 13:30 增派，合计2,000人",
     "车辆机动・道路封锁器材", "车辆", "高"],
    ["S1", "東大全共闘 守备队", "学生", "安田讲堂", 400, "据守", 35.713428, 139.762297, "S1/S14", "推定300—500人，全楼累计469人被捕",
     "投石・火炎瓶・硫酸/盐酸・竹枪・石板・石膏袋・胶合板", "断水断电（06:45），靠储备水与食料", "高（决死队）"],
    ["S2", "反帝学評", "学生", "讲堂5楼南侧屋顶", "", "据守", 35.71350, 139.76225, "S1", "1/19 16:30 集合・演说；S1 未给本派人数（17:40 南侧屋顶+6楼阳台合计 60 人逮捕）",
     "投石・火炎瓶・竹枪", "同上", "高"],
    ["S3", "社学同", "学生", "讲堂6楼阳台", "", "据守", 35.71347, 139.76233, "S1", "16:30 合唱インターナショナル；S1 未给本派人数（同 60 人合计）",
     "投石・火炎瓶・竹枪", "同上", "高"],
    ["S4", "社学同ML派", "学生", "列品館", 32, "据守", 35.71395, 139.76035, "S1", "火炎放射器；2—4楼火灾；32人被捕（米田说38）",
     "火炎瓶・手製火炎放射器（ガス管）・投石", "被切断（08:50 起孤立）", "高（要塞化）"],
    ["S5", "中核派・四トロ", "学生", "法学部研究室", 121, "据守", 35.712674, 139.760260, "S1", "屋顶放火；15:35 全员121人被捕",
     "ガソリン（屋顶放火）・投石・石膏", "被切断", "高"],
    ["S6", "革マル派", "学生", "法文2号館", 14, "据守", 35.7130, 139.7606, "S1", "14人被捕（米田说12）；1/17 主力已撤离",
     "角材・投石", "被切断", "中"],
    ["S7", "医学部共斗会議派・社学同", "学生", "医学部中央館塔屋", 16, "据守", 35.710798, 139.763260, "S1", "08:30 全员逮捕",
     "竹枪・投石", "被切断", "高"],
    ["S8", "神田支援部队", "学生", "明大・中大一带", 1500, "增援（未达）", 35.7005, 139.7635, "S1", "被2,000名机动队阻止",
     "铁管・石块・油桶（就地取材）", "就地", "中（被阻后散去）"],
]
with io.open(os.path.join(DATA, "units.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ID", "单位", "阵营", "位置", "兵力", "任务", "纬度", "経度", "出处", "备注",
                "装备", "补给", "士气(推演用推定)"])
    w.writerows(units)

# ---------- casualties.csv ----------
cas = [
    ["警察侧负伤", "653", "人", "含入院37人", "荒木萬壽夫 1969-03-25 参院地方行政委員会", "S2", "官方"],
    ["警察侧死亡", "0", "人", "—", "多源", "S1/S11", "官方"],
    ["学生侧死亡", "0", "人", "—", "多源", "S1/S11", "官方"],
    ["学生侧重伤(已知)", "18", "人", "ガス銃直击致眼球/口蓋破裂", "和田静夫 1969-03-25 国会提出", "S2", "非完整统计"],
    ["学生侧总负伤", "无统计", "—", "史料缺口", "—", "—", "缺口"],
    ["逮捕(总数)", "633", "人", "警視庁记录；東大生38人", "S11 引警視庁", "S11", "官方"],
    ["逮捕(总数)", "631", "人", "共同通信口径", "共同通信写真解说", "S7", "报道"],
    ["逮捕(总数)", "约630", "人", "産経/日経口径", "S6/S15", "S6/S15", "报道"],
    ["逮捕(1/18 本郷)", "273", "人", "逐日记账", "紛争日誌", "S1", "官方(人次?)"],
    ["逮捕(1/19 大讲堂)", "469", "人", "逐日记账", "紛争日誌", "S1", "官方(人次?)"],
    ["逮捕(1/19 神田)", "75", "人", "逐日记账", "紛争日誌", "S1", "官方"],
    ["受理人員(司法)", "984", "人", "1/9—1/19 東大事件，1969-05-20现在", "犯罪白書昭和44年版", "S3", "官方"],
    ["勾留認容率(1/19)", "98.0", "%", "—", "犯罪白書昭和44年版", "S3", "官方"],
    ["起诉(1969-03)", "509", "人", "—", "西郷吉之助 1969-03-14 众院法務委員会", "S2", "官方"],
    ["起诉(最终)", "607", "人", "—", "最高裁刑事局", "S11", "官方"],
    ["一审有罪", "590", "人", "其中实刑147人", "司法统计", "S11", "官方"],
    ["最高裁上告棄却", "1978-06-30", "日", "懲役2年6月～1年4月", "朝日 1978-07-01", "S11", "报道"],
    ["校方物损", "450,000,000", "日元(1969年价)", "约4.5亿円", "岡沢完治 1969-03-19 众院文教委員会", "S2", "官方"],
    ["押収武器器材", "901", "点", "25件901点＋铺石等14袋；未发现炸药", "紛争日誌 1/19", "S1", "官方"],
    ["解除建筑", "16", "栋", "学生占据建筑", "Japan Times / 紛争日誌", "S9/S1", "报道"],
    ["入试中止", "1969年度", "—", "次年度入学者0人", "S11/S6", "S11", "官方"],
]
with io.open(os.path.join(DATA, "casualties.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["项目", "数值", "单位", "说明", "出处", "来源ID", "性质"])
    w.writerows(cas)

# ---------- timeline.csv ----------
# t = minutes since 1969-01-18 00:00
# t = minutes since 1969-01-18 00:00（负数为 1/17，>1440 为 1/20；输出时统一 +1440 改用 1/17 00:00 为基准）
SHIFT = 1440
ev17 = [
    (-840, "1/17", "10:00", "社学同约50人自理学部1号館移入大講堂（守备主体入馆）", 35.713428, 139.762297, "A", "S1", "集结"),
    (-821, "1/17", "10:19", "学部長会議（海洋研，—11:15）", 35.7128, 139.7626, "A", "S1", "校方"),
    (-758, "1/17", "11:22", "評議会（海洋研，—13:28）", 35.7128, 139.7626, "A", "S1", "校方"),
    (-780, "1/17", "11:00", "中核派约10人在庶務部入口堆石膏20袋，其中一部分搬入法研", 35.71300, 139.76030, "A", "S1", "工事"),
    (-720, "1/17", "12:00", "理学部1号館被共斗会議派再度封闭", 35.713704, 139.762982, "A", "S1", "封锁"),
    (-660, "1/17", "13:00", "中核派在庶務部入口与法研搅拌石膏与砂，强化门扉封锁", 35.71300, 139.76030, "A", "S1", "工事"),
    (-655, "1/17", "13:05", "共斗会議派完全封闭正門", 35.712941, 139.759660, "A", "S1", "封锁"),
    (-610, "1/17", "13:50", "機動隊约200人在正門前待機；フロント1人被捕", 35.712941, 139.759660, "A", "S1", "警备"),
    (-570, "1/17", "14:30", "共斗会議派约10人自鸿池组工地搬出混凝土用セキ板，运入大講堂", 35.713428, 139.762297, "A", "S1", "工事"),
    (-535, "1/17", "15:05", "有志連合学生30人在赤門附近集会，赴大講堂劝说共斗会議派", 35.710592, 139.760359, "A", "S1", "中间派"),
    (-500, "1/17", "15:40", "芝浦工大社学同系约50人在医学部本館前武装集合，与赤門附近共斗非武装学生约90人合流", 35.710798, 139.763260, "A", "S1", "增援"),
    (-410, "1/17", "17:10", "約400人（其中约200武装）按病院前—第二食堂—理学部1号館—工学部6号館—銀杏並木—大講堂路线示威，约300人参加集会", 35.713428, 139.762297, "A", "S1", "示威"),
    (-317, "1/17", "18:43", "集会结束（两回构内示威）；大講堂前立起「1・18 全国労学総決起集会」看板", 35.713428, 139.762297, "A", "S1", "集会"),
    (-225, "1/17", "20:15", "共斗会議派约100人自正門至赤門示威后返回正門", 35.712941, 139.759660, "A", "S1", "示威"),
    (-160, "1/17", "21:20", "加藤総長代行在神田学士会举行记者会（—21:45）", 35.6993, 139.7640, "A", "S1", "校方"),
    (-320, "1/17", "20:40", "日大共斗约40人（銀ヘル）自正門入构增援", 35.712941, 139.759660, "A", "S1", "增援"),
    (-270, "1/17", "21:30", "社学同约150人構内示威（大講堂前）", 35.713428, 139.762297, "A", "S1", "示威"),
    (-60,  "1/17", "23:00", "校方在构内各处立「退去勧告」看板：19日10時前禁止入构；弘報車巡回放送", 35.713428, 139.762297, "A", "S1", "交涉"),
]
ev20 = [
    (1440 + 600, "1/20", "10:00", "校方声明的退去期限届满（前一晚延长至此）", 35.713428, 139.762297, "A", "S1", "交涉"),
    (1440 + 690, "1/20", "11:30", "佐藤首相・坂田文相自竜岡門入构視察", 35.7107, 139.7645, "A", "S1", "政治"),
    (1440 + 853, "1/20", "14:13", "学部長会議（懐徳館，—15:04）；15:24 農学部図書館、21:21 懐徳館（—22:50）", 35.7128, 139.7626, "A", "S1", "校方"),
]
ev = [
    # 1/17 20:45 的出动请求仍作前史文字；1/17 的构内条目见 ev17
    (390, "1/18", "06:30", "警視庁 総合警備本部（本富士署）設置；8,000＋私服500＝8,500人配置", 35.7078, 139.7596, "A", "S1", "指挥"),
    (390, "1/18", "06:30", "送电停止（06:45 给水停止）", 35.713428, 139.762297, "A", "S1", "后勤"),
    (410, "1/18", "06:50", "農学部正門から入構、工学部方面へ", 35.7151, 139.7626, "A", "S1", "入构"),
    (423, "1/18", "07:03", "竜岡門・池の端門から入構", 35.7107, 139.7645, "A", "S1", "入构"),
    (425, "1/18", "07:05", "赤門から入構・門内に集結", 35.710592, 139.760359, "A", "S1", "入构"),
    (425, "1/18", "07:00过", "工学部各号館解除（1号館で1人逮捕）", 35.714231, 139.760060, "A", "S1", "解除"),
    (430, "1/18", "07:10", "理学部1号館解除、11:30まで現場検証", 35.713704, 139.762982, "A", "S1", "解除"),
    (432, "1/18", "07:12", "弥生門バリケード撤去", 35.7147, 139.7647, "A", "S1", "解除"),
    (440, "1/18", "07:20", "医学部1・3号館解除／中央館塔屋16人抵抗", 35.710798, 139.763260, "A", "S1", "抵抗"),
    (460, "1/18", "07:40", "工学部2号館付近に指揮車、大講堂へ退去通告", 35.7140, 139.7601, "A", "S1", "喊话"),
    (480, "1/18", "08:00", "大講堂包囲、各方向からガス弾一斉射撃、ヘリから催涙弾", 35.713428, 139.762297, "A", "S1", "攻击"),
    (480, "1/18", "08:00过", "法学部・文学部解除開始（法文2号館 革マル14人）", 35.713458, 139.760910, "A", "S1", "解除"),
    (495, "1/18", "08:15", "教育学部検証（11:20終了、盾18面押収）", 35.710989, 139.761000, "A", "S1", "解除"),
    (530, "1/18", "08:50", "列品館排除開始：火炎ビン＋手製火炎放射器", 35.71395, 139.76035, "A", "S1", "抵抗"),
    (540, "1/18", "09:00", "放水車10余台、放水開始", 35.7130, 139.7609, "A", "S1", "攻击"),
    (555, "1/18", "09:15", "教育学部に捜査令状提示、機動隊約100人が館内を一巡", 35.710989, 139.761000, "A", "S1", "解除"),
    (560, "1/18", "09:20", "法文2号館：革マル系14人が3・4階から投石、まもなく屋上で全員逮捕", 35.7130, 139.7606, "A", "S1", "解除"),
    (660, "1/18", "11:00", "装甲車で列品館バリケード突破、2—4階火災（消防車出動）", 35.71395, 139.76035, "A", "S1", "攻击"),
    (700, "1/18", "11:40", "法学部研究室：機動隊が3階まで突入、学生は屋上に集まりガソリンをまき放火", 35.71300, 139.76030, "A", "S1", "抵抗"),
    (780, "1/18", "13:00", "列品館屋上に突入、学生32人（女3・重傷2）を逮捕", 35.71395, 139.76035, "A", "S1", "逮捕"),
    (800, "1/18", "13:20", "大講堂へ本格攻撃開始（放水＋装甲車、装甲車炎上）", 35.713428, 139.762297, "A", "S1", "攻击"),
    (875, "1/18", "14:35", "大型ヘリ、屋上へドラム缶の催涙液を散布", 35.713428, 139.762297, "A", "S1", "攻击"),
    (935, "1/18", "15:35", "法学部屋上突入、学生121人全員逮捕", 35.712674, 139.760260, "A", "S1", "逮捕"),
    (920, "1/18", "15:20", "大講堂正面攻撃開始、正面玄関前面へ接近", 35.71335, 139.76210, "A", "S1", "攻击"),
    (930, "1/18", "15:30", "大講堂裏側2個所から機動隊約50人突入", 35.71350, 139.76245, "A", "S1", "攻击"),
    (980, "1/18", "16:20", "正面玄関に電気ノコでバリケード破りを試みる", 35.71335, 139.76205, "A", "S1", "攻击"),
    (970, "1/18", "16:10", "機動隊が大講堂2階まで侵入した模様", 35.713428, 139.762297, "A", "S1", "攻击"),
    (1050, "1/18", "17:30", "突入中止、突入隊一時退去（S11: 17:40 警備本部下令）", 35.713428, 139.762297, "A", "S1/S11", "转折"),
    (1140, "1/18", "19:00", "放水車を周辺配置、翌朝まで断続放水", 35.7130, 139.7610, "A", "S1", "封锁"),
    (1439, "1/18", "23:59", "本郷构内逮捕 273 人（S1「その他」日末统计，无具体时刻，此处置于日末）", 35.713428, 139.762297, "A", "S1", "统计"),
    (1290, "1/18", "21:30", "加藤総長代行声明：退去命令を1日延長し 20 日 10:00 まで", 35.713428, 139.762297, "A", "S1", "交涉"),
    (1800, "1/19", "06:00", "機動隊大講堂周辺に再集結（S1）", 35.713428, 139.762297, "A", "S1", "再开"),
    (1860, "1/19", "07:00", "放水開始、南・北両側から再突入", 35.713428, 139.762297, "A", "S1", "攻击"),
    (1980, "1/19", "09:00", "放水到達5階、ヘリ風圧攻撃、装甲車で接近", 35.71350, 139.76235, "A", "S1", "攻击"),
    (1980, "1/19", "09:20", "各階階段の厚いバリケード、電気ドリル・切断機で破る", 35.713428, 139.762297, "A", "S1", "攻击"),
    (2160, "1/19", "12:00", "2階にいた20数人を逮捕（ロープ・切断機でバリケード撤去中）", 35.713428, 139.762297, "A", "S1", "逮捕"),
    (2215, "1/19", "12:55", "3階学生部付近まで進出（正午前 2階で20余人逮捕）", 35.713428, 139.762297, "A", "S1", "攻击"),
    (2270, "1/19", "13:50", "大講堂南側 2階→3階の階段で激しい攻防", 35.71347, 139.76230, "A", "S1", "攻击"),
    (2325, "1/19", "14:45", "3階のバリケードを撤去", 35.713428, 139.762297, "A", "S1", "攻击"),
    (2340, "1/19", "15:00", "大講堂内で学生200人以上を逮捕", 35.713428, 139.762297, "A", "S1", "逮捕"),
    (2375, "1/19", "15:35", "4階→5階へ進出、北側屋上で抵抗停止", 35.713428, 139.762297, "A", "S1", "攻击"),
    (2430, "1/19", "16:30", "5階南屋上に反帝学評、6階バルコニーに社学同、合唱・演説", 35.71350, 139.76225, "A", "S1", "象征"),
    (2487, "1/19", "17:27", "時計塔に突入", 35.713428, 139.762297, "A", "S1", "终点"),
    (2500, "1/19", "17:40", "南屋上・6階バルコニー突入、学生60人逮捕（S11: 90人）", 35.71347, 139.76230, "A", "S1/S11", "逮捕"),
    (2505, "1/19", "17:45", "時計塔屋上の数人を逮捕", 35.713428, 139.762297, "A", "S1", "逮捕"),
    (2506, "1/19", "17:46", "撤除完了、事件終結（S11）", 35.713428, 139.762297, "A", "S11", "终点"),
    (2580, "1/19", "19:00", "警視庁公安部 現場検証開始", 35.713428, 139.762297, "A", "S1", "检证"),
    (2700, "1/19", "21:00", "検証終了、押収25件901点、炸药未被发现", 35.713428, 139.762297, "A", "S1", "检证"),
]
comb = sorted(ev17 + ev + ev20, key=lambda e: e[0])
with io.open(os.path.join(DATA, "timeline.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["相对分钟", "日期", "时刻", "事件", "纬度", "経度", "可信度", "出处", "类别"])
    for e in comb:
        row = list(e)
        row[0] = int(e[0]) + SHIFT          # 基准改为 1969-01-17 00:00
        w.writerow(row)

# ---------- map html ----------
features = []
for feat in kb["features"]:
    name = feat["properties"].get("name", "")
    role, note = role_of(name)
    features.append({
        "type": "Feature",
        "properties": {"name": name, "role": role, "note": note,
                       "levels": feat["properties"].get("levels") or ""},
        "geometry": feat["geometry"],
    })
geo = {"type": "FeatureCollection", "features": features}

arrows = [
    ["農学部正門→工学部", [[35.7151, 139.7626], [35.7145, 139.7619], [35.7142, 139.7601]]],
    ["赤門→法学部", [[35.71059, 139.76036], [35.7111, 139.7604], [35.7122, 139.7603], [35.71267, 139.76026]]],
    ["正門→大講堂正面", [[35.71294, 139.75966], [35.7131, 139.7606], [35.7133, 139.7616], [35.71336, 139.76205]]],
    ["御殿下→大講堂背面", [[35.7132, 139.7638], [35.7134, 139.7632], [35.7135, 139.7625]]],
    ["竜岡門→医学部", [[35.7107, 139.7645], [35.7108, 139.7633]]],
]

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>安田讲堂攻防战 1969-01-18～19 交互战术地图</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet-polylinedecorator@1.6.0/dist/leaflet.polylineDecorator.css">
<style>
 html,body{margin:0;height:100%;font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif;background:#111;}
 #app{display:flex;height:100%;}
 #map{flex:1;min-width:0;}
 #side{width:340px;background:#1b1d21;color:#e6e6e6;padding:12px;overflow-y:auto;box-sizing:border-box;}
 h1{font-size:15px;margin:0 0 6px;color:#ffb74d;}
 .sub{font-size:11px;color:#9aa0a6;margin-bottom:10px;line-height:1.5;}
 .panel{background:#23262b;border-radius:6px;padding:8px;margin-bottom:10px;}
 .clock{font-size:20px;font-weight:700;color:#ffe082;letter-spacing:0.5px;}
 .clock small{font-size:11px;color:#9aa0a6;font-weight:400;}
 input[type=range]{width:100%;}
 button{background:#2f343a;color:#e6e6e6;border:1px solid #3c4249;border-radius:4px;padding:5px 8px;font-size:12px;cursor:pointer;margin:2px 2px 0 0;}
 button:hover{background:#3a4048;}
 button.on{background:#5c3b00;border-color:#ffb74d;color:#ffd54f;}
 .legend{font-size:11px;line-height:1.9;}
 .sw{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:5px;vertical-align:-2px;}
 .evlist{font-size:11.5px;max-height:300px;overflow-y:auto;}
 .ev{padding:4px 6px;border-left:3px solid #444;margin-bottom:3px;cursor:pointer;background:#1e2126;border-radius:0 4px 4px 0;}
 .ev:hover{background:#2a2f36;}
 .ev .t{color:#ffb74d;font-weight:700;margin-right:4px;}
 .ev .k{color:#7cb342;font-size:10px;margin-left:4px;}
 .ev.dim{opacity:.3;}
 .src{font-size:10px;color:#777;margin-top:8px;line-height:1.5;}
 .leaflet-popup-content{font-size:12px;line-height:1.5;}
 .pop-role{font-weight:700;}
</style>
</head>
<body>
<div id="app">
  <div id="map"></div>
  <div id="side">
    <h1>安田讲堂攻防战 1969.1.18—1.19</h1>
    <div class="sub">实线=建筑轮廓(OSM)，红=学生据守，蓝=已解除／警察集结，灰=中立。<br>点按建筑看当日事件；拖动时间轴回放 35 小时。<br><span style="color:#7cb342">前史：1/17 20:45 加藤総長代行が警察力出動を要請（S1）</span></div>
    <div class="panel">
      <div class="clock"><span id="clock">01-18 06:00</span> <small id="phase">入构前</small></div>
      <input id="slider" type="range" min="0" max="5100" value="1830" step="5">
      <div>
        <button onclick="play()" id="playbtn">▶ 播放</button>
        <button onclick="setT(930)">1/18 15:30 突入</button>
        <button onclick="setT(2487)">1/19 17:27 时钟塔</button>
        <button onclick="setT(390)">重置</button>
      </div>
    </div>
    <div class="panel legend">
      <div><span class="sw" style="background:#d62728"></span>学生据守建筑</div>
      <div><span class="sw" style="background:#1f77b4"></span>已解除／警察集结</div>
      <div><span class="sw" style="background:#888"></span>中立建筑</div>
      <div><span class="sw" style="background:#ff7f0e"></span>安田讲堂（主战场）</div>
      <div>▶ 虚线箭头 = 机动队进攻轴线</div>
    </div>
    <div class="panel">
      <div style="font-size:12px;color:#ffb74d;margin-bottom:4px">事件（点击定位）</div>
      <div class="evlist" id="evlist"></div>
    </div>
    <div class="panel" style="font-size:11px;color:#9aa0a6">
      <div>底图：国土地理院 タイル（写真/标准图）· © OpenStreetMap contributors</div>
    </div>
    <div class="src">
      史实出处：東京大学「紛争日誌 その4」（S1）、国会会議録（S2）、犯罪白書昭和44年版（S3）、佐々淳行1996（S13）、島泰三2005（S14）。
      推定位置均标「推定」。本图不用于导航。
    </div>
  </div>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet-polylinedecorator@1.6.0/dist/leaflet.polylineDecorator.js"></script>
<script>
const GEO = __GEO__;
const EVENTS = __EVENTS__;
const ARROWS = __ARROWS__;
const UNITS = __UNITS__;

const map = L.map('map',{zoomControl:true, preferCanvas:true}).setView([35.7128,139.7618],17);
const gsiPhoto = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg',{maxZoom:19,attribution:'国土地理院 シームレス写真'});
const gsiStd = L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png',{maxZoom:19,attribution:'国土地理院 標準地図'});
const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap contributors'});
gsiPhoto.addTo(map);
L.control.layers({'地理院 写真':'x'} ,{}, {collapsed:true}).remove();
L.control.layers({'地理院 写真(默认)':gsiPhoto,'地理院 標準図':gsiStd,'OSM 街道图':osm},{},{collapsed:true,position:'topright'}).addTo(map);

const COL = {'学生':'#d62728','警察':'#1f77b4','中立':'#888888'};
function style(f){
  const name=f.properties.name;
  if(name==='安田講堂') return {color:'#ff7f0e',weight:3,fillColor:'#ff7f0e',fillOpacity:.35};
  const c=COL[f.properties.role]||'#888';
  return {color:c,weight:1,fillColor:c,fillOpacity:.22};
}
const bLayer=L.geoJSON(GEO,{style:style,
  onEachFeature:(f,l)=>{
    const p=f.properties;
    const c = p.name==='安田講堂' ? '#ff7f0e' : (COL[p.role]||'#888');
    l.bindPopup('<div class="pop-role" style="color:'+c+'">'+p.name+'</div>'+
      (p.levels?'层数：'+p.levels+'<br>':'')+
      '当日角色：'+p.role+(p.note?'<br>'+p.note:''));
    l.on('mouseover',()=>l.setStyle({weight:3}));
    l.on('mouseout',()=>l.setStyle({weight: p.name==='安田講堂'?3:1}));
  }}).addTo(map);

// 进攻轴线 + 箭头
const arrowLayer=L.layerGroup().addTo(map);
ARROWS.forEach(([label,pts])=>{
  const pl=L.polyline(pts,{color:'#00e5ff',weight:2.5,dashArray:'6 6',opacity:.9}).addTo(arrowLayer);
  pl.bindTooltip(label);
  L.polylineDecorator(pl,{patterns:[{offset:8,repeat:0,symbol:L.Symbol.arrowHead({pixelSize:8,pathOptions:{color:'#00e5ff',fillOpacity:1,weight:0}})}]}).addTo(arrowLayer);
});

// 单位
const unitLayer=L.layerGroup().addTo(map);
UNITS.forEach(u=>{
  const isP=u[2]==='警察';
  const m=L.circleMarker([u[6],u[7]],{radius:isP?7:7,color:isP?'#1f77b4':'#d62728',
     fillColor:isP?'#4fa3e3':'#e8564d',fillOpacity:.9,weight:2}).addTo(unitLayer);
  m.bindTooltip(u[1]+'（'+u[4]+'人）',{direction:'top'});
  m.bindPopup('<b>'+u[1]+'</b><br>阵营：'+u[2]+'<br>位置：'+u[3]+'<br>兵力：'+u[4]+'<br>任务：'+u[5]+'<br>备注：'+u[9]+'<br><span style="color:#888">出处：'+u[8]+'</span>');
});

// 事件
const evLayer=L.layerGroup().addTo(map);
const evMarkers=[];
EVENTS.forEach((e,i)=>{
  const m=L.circleMarker([e[4],e[5]],{radius:5,color:'#ffd54f',fillColor:'#ffe082',fillOpacity:1,weight:1.5}).addTo(evLayer);
  m.bindPopup('<b>'+e[1]+' '+e[2]+'</b><br>'+e[3]+'<br><span style="color:#888">出处：'+e[7]+'（可信度'+e[6]+'）</span>');
  evMarkers.push(m);
});

const listEl=document.getElementById('evlist');
EVENTS.forEach((e,i)=>{
  const d=document.createElement('div');
  d.className='ev';d.dataset.i=i;d.dataset.t=e[0];
  d.innerHTML='<span class="t">'+e[1]+' '+e[2]+'</span>'+e[3]+'<span class="k">'+e[8]+'</span>';
  d.onclick=()=>{setT(e[0]);map.flyTo([e[4],e[5]],18,{duration:.6});evMarkers[i].openPopup();};
  listEl.appendChild(d);
});

function fmt(t){
  const dt=new Date(Date.UTC(1969,0,17,0,0,0)+t*60000);
  return '01-'+String(dt.getUTCDate()).padStart(2,'0')+' '+
         String(dt.getUTCHours()).padStart(2,'0')+':'+String(dt.getUTCMinutes()).padStart(2,'0');
}
function phaseOf(t){
  if(t<1830)return '入构前（1/17）';
  if(t<2240)return '逐栋解除';
  if(t<2470)return '强攻讲堂（1/18）';
  if(t<3270)return '彻夜放水';
  if(t<3927)return '逐层清除（1/19）';
  if(t<4000)return '制压屋顶';
  if(t<4140)return '检证・终了';
  return '1/20 以后';
}
const slider=document.getElementById('slider');
function setT(t){
  slider.value=t;
  document.getElementById('clock').textContent=fmt(t);
  document.getElementById('phase').textContent=phaseOf(t);
  let n=0;
  EVENTS.forEach((e,i)=>{
    const on = e[0]<=t;
    if(on)n++;
    evMarkers[i].setStyle({opacity:on?1:.12,fillOpacity:on?1:.12});
    listEl.children[i].classList.toggle('dim',!on);
  });
  unitLayer.setOpacity&&unitLayer.setOpacity(1);
}
slider.oninput=()=>setT(+slider.value);
let timer=null;
function play(){
  const b=document.getElementById('playbtn');
  if(timer){clearInterval(timer);timer=null;b.textContent='▶ 播放';b.classList.remove('on');return;}
  b.textContent='⏸ 暂停';b.classList.add('on');
  timer=setInterval(()=>{
    let v=+slider.value+5;
    if(v>5100){clearInterval(timer);timer=null;b.textContent='▶ 播放';b.classList.remove('on');v=5100;}
    setT(v);
  },120);
}
setT(1830);
map.fitBounds([[35.7080,139.7585],[35.7165,139.7665]]);
</script>
</body>
</html>
"""

js_ev = []
for e in comb:
    row = list(e)
    row[0] = int(e[0]) + SHIFT
    js_ev.append(row)
html = (html.replace("__GEO__", json.dumps(geo, ensure_ascii=False))
            .replace("__EVENTS__", json.dumps(js_ev, ensure_ascii=False))
            .replace("__ARROWS__", json.dumps(arrows, ensure_ascii=False))
            .replace("__UNITS__", json.dumps(units, ensure_ascii=False)))
with io.open(os.path.join(MAPD, "安田讲堂攻防战地图.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("buildings:", len(rows), "units:", len(units), "events:", len(ev), "features:", len(features))
print("html bytes:", os.path.getsize(os.path.join(MAPD, "安田讲堂攻防战地图.html")))
