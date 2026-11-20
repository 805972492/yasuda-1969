# -*- coding: utf-8 -*-
"""移动 / 攻击「受控性」自测：把断言脚本注入推演页，在无头 Chrome 里跑真实引擎。

用法：
    python tests_control.py gen     # 生成 _t.html（内嵌断言）
    （用 Chrome --dump-dom 跑一次，输出 _dom.html）
    python tests_control.py check   # 解析 _dom.html，打印 PASS/FAIL，失败则退出码 1
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "推演展示_安田讲堂.html")

JS = r"""
<pre id="OUT" style="white-space:pre-wrap"></pre>
<script>
const R = [];
function ok(name, cond, detail){ R.push((cond?'PASS':'FAIL')+'  '+name+(detail?'   ['+detail+']':'')); }
function eq(name, a, b){ ok(name, a===b, 'got='+a+'  want='+b); }
function near(name, a, b, tol){ ok(name, Math.abs(a-b)<=tol, 'got='+a+'  want='+b+'±'+tol); }
function T(name, fn){ try{ fn(); }catch(e){ R.push('ERROR '+name+'   ['+e.message+']'); } }
function reset(side){ mode='free'; playerSide=side||'全共斗'; fresh(); }

// ---------- 一、移动是否受控 ----------
T('移动-速度上限', function(){
  reset('机动队');
  const u = S.units.find(x=>x.unit.includes('神田增派'));
  const tgt = S.sites.find(b=>b.id==='reppinkan');
  const d0 = dist(u.cur, tgt);
  u.order = {kind:'assault', id:'reppinkan'};
  execOrders();
  const d1 = dist(u.cur, tgt);
  ok('移动-单步位移≈0.55km', Math.abs((d0-d1)-0.55) < 0.02, 'd0-d1='+(d0-d1).toFixed(3));
  ok('移动-不瞬间传送', d1 > 0.15, 'd1='+d1.toFixed(3));
});

T('移动-到达后不越位', function(){
  reset('机动队');
  const u = S.units.find(x=>x.unit.includes('神田增派'));
  const tgt = S.sites.find(b=>b.id==='reppinkan');
  u.order = {kind:'assault', id:'reppinkan'};
  for(let i=0;i<12;i++) execOrders();
  const d = dist(u.cur, tgt);
  ok('移动-贴合目标不再前进', d <= 0.16, 'd='+d.toFixed(3));
});

T('移动-转移不改变归属', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('本乡增援'));
  const site = S.sites.find(b=>b.id==='ochano_police');
  u.order = {kind:'move', id:'ochano_police'};
  for(let i=0;i<8;i++) execOrders();
  eq('移动-转移命令不占地', site.holder, '机动队');
});

T('移动-玩家指挥机动队时 AI 不代令', function(){
  reset('机动队');
  for(let i=0;i<3;i++) step();
  const idle = S.units.filter(u=>u.side==='机动队' && u.alive).every(u=>!u.order);
  ok('控制权-机动队未接到命令就不动', idle);
});

T('移动-跨区机动受同一步长约束', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('驹场第8'));
  const tgt = S.sites.find(b=>b.id==='kanda_barricade');
  const d0 = dist(u.cur, tgt);
  u.order = {kind:'attack', id:'kanda_barricade'};
  execOrders();
  const d1 = dist(u.cur, tgt);
  ok('移动-反抗军单步≈0.45km', Math.abs((d0-d1)-0.45) < 0.02, 'd0-d1='+(d0-d1).toFixed(3));
});

// ---------- 二、攻击是否受控 ----------
T('攻击-未接触不扣街垒', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('神田街垒队'));
  const tgt = S.sites.find(b=>b.id==='dai2shokudo');
  const b0 = tgt.barrier;
  u.order = {kind:'attack', id:'dai2shokudo'};
  execOrders();
  eq('攻击-远处只机动', Math.round(tgt.barrier), Math.round(b0));
  ok('攻击-留下机动回执', S.log.some(l=>l.txt.indexOf('机动')>=0));
});

T('攻击-同阵营不可打', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('本乡增援'));
  const own = S.sites.find(b=>b.id==='reppinkan');
  u.cur = {lat:own.lat, lng:own.lng};
  const b0 = own.barrier;
  u.order = {kind:'attack', id:'reppinkan'};
  execOrders();
  eq('攻击-同阵营街垒不变', Math.round(own.barrier), Math.round(b0));
  ok('攻击-回执「已在本方控制下」', S.log.some(l=>l.txt.indexOf('已在本方控制下')>=0));
});

T('门控-直升机不能突击且不耗补给', function(){
  reset('机动队');
  const heli = S.units.find(u=>u.unit.includes('直升机'));
  const sup0 = heli.supply;
  heli.order = {kind:'assault', id:'reppinkan'};
  const l0 = S.log.length;
  execOrders();
  ok('门控-突击被退回', S.log.some(l=>l.txt.indexOf('不具备')>=0));
  eq('门控-补给未扣', heli.supply, sup0);
  eq('门控-命令已清空', heli.order, null);
  const l1 = S.log.length;
  execOrders();
  eq('门控-同一条不重复退', S.log.length, l1);
  heli.order = {kind:'move', id:'reppinkan'};
  execOrders();
  eq('门控-直升机不能转移', heli.order, null);
});

T('门控-民青不可被玩家攻击性下令', function(){
  reset('全共斗');
  const mq = S.units.find(u=>u.side==='民青');
  ok('门控-民青无 assault/attack', !caps(mq).includes('assault') && !caps(mq).includes('attack'));
});

T('攻击-空中平台不能占领', function(){
  reset('机动队');
  const heli = S.units.find(u=>u.unit.includes('直升机'));
  const site = S.sites.find(b=>b.id==='reppinkan');
  heli.cur = {lat:site.lat, lng:site.lng};
  heli.order = {kind:'fire', id:'reppinkan'};
  for(let i=0;i<40;i++) execOrders();
  eq('攻击-归属不变', site.holder, '社学同 ML派');
  near('攻击-街垒停在 8', site.barrier, 8, 0.01);
});

T('攻击-直升机不能占楼层', function(){
  reset('机动队');
  const heli = S.units.find(u=>u.unit.includes('直升机'));
  heli.cur = {lat:HALL.lat, lng:HALL.lng};
  heli.order = {kind:'fire', id:'yasuda_hall'};
  for(let i=0;i<40;i++) execOrders();
  eq('攻击-1F 仍属守方', S.floors['1'].holder, '全共斗');
  ok('攻击-1F 街垒有下限', S.floors['1'].b >= 8, 'b='+S.floors['1'].b);
});

T('逐层-下层未清不放行', function(){
  reset('机动队');
  const p = S.units.find(u=>u.unit.includes('第7'));
  p.cur = {lat:HALL.lat, lng:HALL.lng};
  selFloor = '3';
  floorAssault('3');
  ok('逐层-3F 不接令', !p.order);
  ok('逐层-给出受阻提示', S.log.some(l=>l.txt.indexOf('受阻')>=0));
  S.floors['1'].holder = '机动队'; S.floors['2'].holder = '机动队';
  floorAssault('3');
  ok('逐层-清完下面后接令', !!p.order && p.order.kind==='floor' && p.order.f==='3');
});

T('逐层-只有 6 层依次失守', function(){
  reset('机动队');
  const p = S.units.find(u=>u.unit.includes('第7'));
  p.cur = {lat:HALL.lat, lng:HALL.lng};
  p.order = {kind:'assault', id:'yasuda_hall'};
  const first = {};
  for(let i=0;i<400;i++){
    execOrders();
    ['1','2','3','4','5','6'].forEach(k=>{ if(first[k]===undefined && S.floors[k].holder==='机动队') first[k]=i; });
  }
  const seq = ['1','2','3','4','5','6'].map(k=>first[k]);
  const ordered = seq.every((v,i)=>i===0 || (v!==undefined && v>=seq[i-1]));
  ok('逐层-易手顺序 1→6 单调', ordered, 'first='+seq.join(','));
});

T('逐层-远处警察不能下层命令或吃反击', function(){
  reset('全共斗');
  const p = S.units.find(u=>u.unit.includes('第7'));
  p.cur = {lat:35.7300, lng:139.7800};
  const n0 = p.n;
  floorCounter('1');
  eq('逐层-反击打不到远处警察', p.n, n0);
  selFloor='1'; floorAssault('1');   // 玩家是守方，这里只验证不会误触发
  ok('逐层-未误改楼层', S.floors['1'].holder==='全共斗');
});

T('攻击-不重复下令也持续', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('本乡增援'));
  const tgt = S.sites.find(b=>b.id==='dai2shokudo');
  u.cur = {lat:tgt.lat, lng:tgt.lng};
  const b0 = tgt.barrier;
  u.order = {kind:'attack', id:'dai2shokudo'};
  execOrders(); const b1 = tgt.barrier;
  execOrders(); const b2 = tgt.barrier;
  ok('攻击-命令跨回合保持', b1<b0 && b2<b1, b0.toFixed(0)+'→'+b1.toFixed(0)+'→'+b2.toFixed(0));
});

T('攻击-只伤目标不波及邻馆', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('本乡增援'));
  const tgt = S.sites.find(b=>b.id==='dai2shokudo');
  const other = S.sites.find(b=>b.id==='kyoiku');
  u.cur = {lat:tgt.lat, lng:tgt.lng};
  const ob = other.barrier;
  u.order = {kind:'attack', id:'dai2shokudo'};
  execOrders();
  eq('攻击-邻馆街垒不变', Math.round(other.barrier), Math.round(ob));
});

T('攻击-守方可以夺回楼层', function(){
  reset('全共斗');
  S.floors['1'].holder = '机动队'; S.floors['1'].b = 0; S.floors['1'].n = 0;
  const u = S.units.find(x=>x.unit.includes('安田讲堂 1层'));
  u.cur = {lat:HALL.lat, lng:HALL.lng};
  u.order = {kind:'attack', id:'yasuda_hall'};
  for(let i=0;i<10 && S.floors['1'].holder!=='全共斗'; i++) execOrders();
  eq('攻击-1F 可被守方夺回', S.floors['1'].holder, '全共斗');
});

T('攻击-空中压制到位即停手', function(){
  reset('机动队');
  const heli = S.units.find(u=>u.unit.includes('直升机'));
  heli.cur = {lat:HALL.lat, lng:HALL.lng};
  heli.order = {kind:'fire', id:'yasuda_hall'};
  for(let i=0;i<40;i++) execOrders();
  eq('攻击-空中压制停在 8', Math.round(S.floors['1'].b), 8);
  eq('攻击-压满后命令结束', heli.order, null);
});

// ---------- 三、记账与不变量 ----------
T('记账-清层计被捕、无人馆不计制压', function(){
  reset('全共斗');
  const a0 = S.arrests;
  flipFloor('1');
  eq('记账-清层 1F 计 40 人', S.arrests, a0+40);
  const c0 = S.captured;
  flipSite('kogakubu1', '歷史', '解除封锁（馆内无人）');
  eq('记账-解除无人馆不计制压', S.captured, c0);
});

T('撤退-只执行一次', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('本乡增援'));
  u.morale = 80; u.order = {kind:'retreat'};
  execOrders();
  eq('撤退-命令结束', u.order, null);
  near('撤退-士气 −10', u.morale, 70, 0.01);
  u.morale = 80;
  execOrders();
  eq('撤退-不重复扣士气', u.morale, 80);
});

T('包围-断补给后守方不能修补', function(){
  reset('机动队');
  const p = S.units.find(u=>u.unit.includes('第1'));
  const site = S.sites.find(b=>b.id==='reppinkan');
  p.cur = {lat:site.lat, lng:site.lng};
  p.order = {kind:'encircle'};
  execOrders();
  ok('包围-标记生效', (site.sealedUntil||0) >= S.turn, 'sealedUntil='+site.sealedUntil);
  const ml = S.units.find(u=>u.unit.includes('列品馆'));
  const b0 = site.barrier;
  ml.order = {kind:'repair'};
  execOrders();
  eq('包围-修补被拒', Math.round(site.barrier), Math.round(b0));
  ok('包围-回执写明被包围', S.log.some(l=>l.txt.indexOf('正被包围')>=0));
});

T('加固-空地无据点被拒', function(){
  reset('全共斗');
  const u = S.units.find(x=>x.unit.includes('神田街垒队'));
  u.cur = {lat:35.7500, lng:139.8000};
  u.order = {kind:'repair'};
  execOrders();
  ok('加固-空地加固被拒', S.log.some(l=>l.txt.indexOf('附近无本方据点')>=0));
});

T('合并-人数守恒', function(){
  reset('全共斗');
  const pick = ()=>S.units.filter(u=>u.alive && u.zone==='本乡' && sideOf(u.side)==='rebel');
  const sum = a=>a.reduce((s,u)=>s+(u.n||0),0);
  const before = sum(pick());
  mergeUnits();
  eq('合并-总人数守恒', sum(pick()), before);
  ok('合并-少了一个编组', pick().length < 12);
});

T('控制权-各派都在可下令列表', function(){
  reset('全共斗');
  const rb = S.units.filter(u=>u.alive && sideOf(u.side)==='rebel');
  ok('控制权-反抗军编组 ≥10', rb.length>=10, 'n='+rb.length);
  ok('控制权-含反帝学评', rb.some(u=>u.sect==='反帝学评'));
  ok('控制权-含神田/驹场部队', rb.some(u=>u.zone==='神田') && rb.some(u=>u.zone==='驹场'));
});

T('跨区-神田据点可夺取', function(){
  reset('全共斗');
  const k = S.units.find(u=>u.unit.includes('神田街垒队'));
  const cop = S.sites.find(b=>b.id==='ochano_police');
  k.order = {kind:'attack', id:'ochano_police'};
  for(let i=0;i<25 && cop.holder!=='全共斗'; i++) execOrders();
  eq('跨区-派出所转手', cop.holder, '全共斗');
});

T('民青-反击只打敌方', function(){
  reset('全共斗');
  const mq = S.units.find(u=>u.side==='民青');
  const reb = S.units.find(u=>u.side==='全共斗' && u.n!==null && u.alive);
  reb.cur = {lat:mq.cur.lat, lng:mq.cur.lng};
  const n0 = reb.n;
  aiMingqing();
  ok('民青-反击敌方', reb.n < n0, reb.n+' < '+n0);
  const mq2 = S.units.filter(u=>u.side==='民青' && u.alive)[0];
  const m1 = mq2.n;
  aiMingqing();
  eq('民青-不误伤友军', mq2.n, m1);
});

// ---------- 四、长跑不变量 ----------
T('长跑-95 回合不变量', function(){
  reset('全共斗');
  for(let i=0;i<95;i++) step();
  eq('长跑-时钟与回合一致', S.t, T0 + S.turn*STEP);
  eq('长跑-完整性告警为零', S.flags.length, 0);
  ok('长跑-人数不为负', S.units.every(u=>u.n===null || u.n>=0));
  ok('长跑-士气/补给在界内', S.units.every(u=>u.morale>=0 && u.morale<=100 && u.supply>=0 && u.supply<=100));
  ok('长跑-街垒不为负', S.sites.every(b=>b.barrier>=0) && ['1','2','3','4','5','6'].every(k=>S.floors[k].b>=0));
  ok('长跑-没有 NaN', S.units.every(u=>!isNaN(u.morale) && !isNaN(u.supply)));
  eq('长跑-警方始终没打民青（医学部本馆）', S.sites.find(b=>b.id==='igaku_h').holder, '民青');
  eq('长跑-警方始终没打民青（教育学部）', S.sites.find(b=>b.id==='kyoiku').holder, '民青');
  eq('长跑-讲堂终局归警方', S.sites.find(b=>b.id==='yasuda_hall').holder, '机动队');
});

T('剧本-95 回合基线', function(){
  mode='script'; playerSide='全共斗'; fresh();
  for(let i=0;i<95;i++) step();
  eq('剧本-讲堂 6F 全失守', ['1','2','3','4','5','6'].map(k=>S.floors[k].holder).join(','), '机动队,机动队,机动队,机动队,机动队,机动队');
  eq('剧本-教育学部走验证', S.sites.find(b=>b.id==='kyoiku').holder, '机动队');
  eq('剧本-告警为零', S.flags.length, 0);
});

// 输出
const pass = R.filter(x=>x.indexOf('PASS')===0).length;
document.getElementById('OUT').textContent = R.join('\n') + '\n---\nSUMMARY ' + pass + ' / ' + R.length;
</script>
"""


def gen():
    h = io.open(HTML, encoding="utf-8").read()
    h = h.replace("</body>", JS + "\n</body>")
    out = os.path.join(HERE, "_t.html")
    io.open(out, "w", encoding="utf-8").write(h)
    print("wrote", out, len(h))


def check():
    dom = io.open(os.path.join(HERE, "_dom.html"), encoding="utf-8", errors="replace").read()
    m = re.search(r'<pre id="OUT"[^>]*>(.*?)</pre>', dom, re.S)
    if not m:
        print("no OUT block found")
        return 1
    text = m.group(1)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    print(text)
    return 0 if ("FAIL" not in text and "ERROR" not in text) else 1


if __name__ == "__main__":
    if sys.argv[1] == "gen":
        gen()
    else:
        sys.exit(check())
