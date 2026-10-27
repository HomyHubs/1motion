"""Builds scenes/hf/index.html: one continuous HyperFrames canvas for the whole film.
Reads project.json (narration, events, measured timings when present) and writes the composition.
Object ids persist across beats: #sg (Singapore marker), ship objects, camera pans between stages.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'scenes' / 'hf'
W, H, FPS = 720, 1280, 30
# Fallback beat starts (reference video seconds) used only before voice is measured.
REF_START = [0.0, 9.9, 19.4, 28.0, 41.0, 46.5, 55.6, 67.0, 82.0, 90.0, 100.0, 112.0]
REF_END = 118.5


def beat_times(doc):
    beats = doc['beats']
    out = []
    for n, b in enumerate(beats):
        if 'start_s' in b and 'slot_duration_s' in b:
            start, slot, voice = b['start_s'], b['slot_duration_s'], b['audio_duration_s']
        else:
            start = REF_START[n]
            end = REF_START[n + 1] if n + 1 < len(beats) else REF_END
            slot, voice = end - start, end - start - b['tail_s']
        text = b['narration']
        ev = {}
        for e in b['events']:
            rel = e.get('time_s')
            if rel is None:
                rel = voice * text.index(e['trigger_phrase']) / len(text)
            ev[e['target']] = round(start + rel, 3)
        parts = [p.strip() for p in re.split(r'(?<=[.?!])\s+', text) if p.strip()]
        total = sum(len(p) for p in parts)
        caps, acc = [], 0
        for p in parts:
            a = start + voice * acc / total
            acc += len(p)
            caps.append({'t': round(a, 3), 'e': round(start + voice * acc / total, 3), 'text': p})
        out.append({'id': b['id'], 'start': round(start, 3), 'end': round(start + slot, 3), 'ev': ev, 'caps': caps})
    return out


CSS = """
:root{--bg:#0a2233;--sea:#0f3b57;--card:#f3efe4;--ink:#0a2233;--lime:#c8f169;--gold:#ffd166;--red:#ff6b5e;--mute:#7fa3b8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:720px;height:1280px;overflow:hidden;background:var(--bg);font-family:'Segoe UI',Arial,sans-serif;color:#fff}
#root{position:relative;width:720px;height:1280px;overflow:hidden;background:var(--bg)}
#cam{position:absolute;left:0;top:0;width:720px}
.stage{position:absolute;left:0;width:720px;height:1280px;transform-origin:50% 50%;
 background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:60px 60px}
.abs{position:absolute}
.tag{position:absolute;left:48px;top:64px;font-size:26px;letter-spacing:.14em;color:var(--mute);font-weight:700;text-transform:uppercase}
.big{font-weight:800;line-height:1;letter-spacing:-.02em}
.card{position:absolute;border-radius:22px;background:var(--card);color:var(--ink);font-weight:700;display:flex;align-items:center;padding:0 28px;font-size:36px;line-height:1.15}
.chip{position:absolute;left:60px;width:600px;height:84px;border-radius:42px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.28);font-size:32px;font-weight:700;display:flex;align-items:center;padding:0 30px;gap:20px}
.x{color:var(--red);font-size:40px;font-weight:800}
.note{font-size:24px;color:var(--mute);font-weight:600}
.lime{color:var(--lime)}.gold{color:var(--gold)}.red{color:var(--red)}
.sea{background:var(--sea)}
#sg{position:absolute;left:0;top:0;width:0;height:0}
#sg .v{position:absolute;left:-90px;top:-90px;width:180px;height:180px;display:flex;align-items:center;justify-content:center;flex-direction:column;opacity:0}
.dot{width:56px;height:56px;border-radius:50%;background:var(--lime);box-shadow:0 0 0 14px rgba(200,241,105,.22)}
.blk{width:150px;height:120px;border-radius:14px;background:var(--lime);color:var(--ink);font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center}
.pin{width:44px;height:44px;border-radius:50% 50% 50% 0;background:var(--lime);transform:rotate(-45deg)}
.port{width:150px;height:92px;background:var(--lime);border-radius:10px;position:relative;color:var(--ink);font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center}
.refin{width:150px;height:120px;background:var(--lime);border-radius:14px;color:var(--ink);font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center;text-align:center}
.hub{width:170px;height:170px;border-radius:50%;background:var(--lime);color:var(--ink);font-weight:800;font-size:24px;display:flex;align-items:center;justify-content:center;text-align:center}
.lbl{position:absolute;font-size:24px;font-weight:700;color:#fff;white-space:nowrap}
.ship{position:absolute;width:0;height:0}
.ship i{position:absolute;left:-34px;top:-14px;width:68px;height:28px;background:var(--gold);border-radius:4px 4px 26px 26px}
.ship b{position:absolute;left:-14px;top:-30px;width:28px;height:16px;background:#fff;border-radius:3px}
.cont{position:absolute;width:26px;height:20px;border-radius:3px}
.coin{position:absolute;width:44px;height:44px;border-radius:50%;background:var(--gold);color:var(--ink);font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center;border:3px solid #fff}
#cap{position:absolute;left:36px;top:1008px;width:648px;height:190px}
#cap .c{position:absolute;left:0;top:0;width:648px;min-height:150px;padding:22px 28px;border-radius:24px;background:#fff;color:var(--ink);font-size:32px;font-weight:700;line-height:1.28;opacity:0}
"""


JS = r"""
const B = __BEATS__;
const SG = (i, y) => i * 1280 + y;
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({paused: true});
const $ = (s) => document.querySelector(s);
const world = $('#cam');
const mk = (parent, cls, css, html) => { const d = document.createElement('div'); d.className = cls; Object.assign(d.style, css || {}); if (html !== undefined) d.innerHTML = html; parent.appendChild(d); return d; };
const stages = B.map((b, i) => { const s = mk(world, 'stage', {top: (i * 1280) + 'px'}); s.id = 'st' + b.id; return s; });
const S = (i, y) => (i * 1280 + y);
const ev = (i, name, fb) => (B[i].ev[name] !== undefined ? B[i].ev[name] : (fb === undefined ? B[i].start : fb));
const pop = (el, t, d) => tl.fromTo(el, {opacity: 0, y: 40, scale: 0.94}, {opacity: 1, y: 0, scale: 1, duration: d || 0.5, ease: 'back.out(1.4)'}, t);
const fade = (el, t, d) => tl.fromTo(el, {opacity: 0}, {opacity: 1, duration: d || 0.4, ease: 'power2.out'}, t);
const slide = (el, fromVars, toVars, t, d, ease) => tl.fromTo(el, fromVars, Object.assign({duration: d || 0.8, ease: ease || 'power2.inOut'}, toVars), t);
const tag = (i, text) => { const t = mk(stages[i], 'tag', {}, text); return t; };

// ---- shared Singapore marker: one object, five looks, moves between stages ----
const sg = mk(world, '', {}); sg.id = 'sg'; sg.style.position = 'absolute'; sg.style.left = '0px'; sg.style.top = '0px';
const look = {};
['dot', 'blk', 'pin', 'port', 'refin', 'hub'].forEach(k => { const v = mk(sg, 'v'); v.dataset.v = k; look[k] = v; });
look.dot.innerHTML = '<div class="dot"></div>';
look.blk.innerHTML = '<div class="blk">SINGAPORE</div>';
look.pin.innerHTML = '<div class="pin"></div>';
look.port.innerHTML = '<div class="port">CẢNG</div>';
look.refin.innerHTML = '<div class="refin">LỌC DẦU</div>';
look.hub.innerHTML = '<div class="hub">SINGAPORE</div>';
const sgAt = (x, y, t, d) => tl.to(sg, {x: x, y: y, duration: d || 0.8, ease: 'power2.inOut'}, t);
const sgLook = (k, t, d) => { Object.keys(look).forEach(n => tl.to(look[n], {opacity: n === k ? 1 : 0, duration: d || 0.35}, t)); };
gsap.set(sg, {x: 360, y: S(0, 470)});
gsap.set(Object.values(look), {opacity: 0});

// ---- camera ----
B.forEach((b, i) => {
  if (i === 0) return;
  tl.fromTo(world, {y: -(i - 1) * 1280}, {y: -i * 1280, duration: 0.75, ease: 'power2.inOut'}, Math.max(0, b.start - 0.45));
});
gsap.set(world, {y: 0});
B.forEach((b, i) => tl.fromTo(stages[i], {scale: 1}, {scale: 1.035, duration: b.end - b.start + 0.6, ease: 'none'}, b.start));

// ---- 01 hook ----
{ const i = 0, st = stages[i];
  tag(i, 'Vì sao Singapore giàu');
  sgLook('dot', 0.05, 0.5);
  mk(st, 'lbl lime', {left: '260px', top: '560px', width: '200px', textAlign: 'center', fontSize: '28px'}, 'SINGAPORE');
  const chips = ['NHỎ HƠN SÀI GÒN', 'KHÔNG MỎ', 'MUA NƯỚC CỦA HÀNG XÓM'].map((t, n) => mk(st, 'chip', {top: (650 + n * 104) + 'px'}, '<span class="x">×</span>' + t));
  gsap.set(chips, {opacity: 0});
  chips.forEach((c, n) => pop(c, ev(i, 'chips') + n * 0.35, 0.45));
  const q = mk(st, 'card', {left: '60px', top: '980px', width: '600px', height: '120px', background: '#c8f169', fontSize: '38px', justifyContent: 'center', textAlign: 'center'}, 'GIÀU NGANG NGƯỜI MỸ?');
  const qn = mk(st, 'note', {left: '60px', top: '1110px', width: '600px', textAlign: 'center'}, 'theo video tham chiếu');
  gsap.set([q, qn], {opacity: 0}); pop(q, ev(i, 'question'), 0.55); fade(qn, ev(i, 'question') + 0.3);
}
// ---- 02 1965 ----
{ const i = 1, st = stages[i];
  tag(i, 'Mốc thời gian');
  const yr = mk(st, 'big lime', {left: '0', top: '210px', width: '720px', textAlign: 'center', fontSize: '210px'}, '1965');
  gsap.set(yr, {opacity: 0}); tl.fromTo(yr, {opacity: 0, scale: 0.7}, {opacity: 1, scale: 1, duration: 0.7, ease: 'back.out(1.6)'}, ev(i, 'year'));
  const my = mk(st, 'blk', {position: 'absolute', left: '150px', top: '600px', width: '210px', height: '140px', background: '#7fa3b8', fontSize: '28px'}, 'MALAYSIA');
  mk(st, 'lbl note', {left: '150px', top: '760px'}, 'liên bang');
  gsap.set(my, {opacity: 0}); fade(my, ev(i, 'year') + 0.4);
  sgLook('blk', ev(i, 'year') + 0.2, 0.4);
  gsap.set(sg, {x: 360, y: S(0, 470)});
  sgAt(450, S(1, 670), ev(i, 'year') - 0.4, 0.9);
  slide(my, {x: 0}, {x: -70, duration: 0.9, ease: 'power3.inOut'}, ev(i, 'split'));
  tl.to(sg, {x: 540, duration: 0.9, ease: 'power3.inOut'}, ev(i, 'split'));
  const gap = mk(st, 'abs', {left: '358px', top: '560px', width: '4px', height: '240px', background: 'repeating-linear-gradient(#ff6b5e 0 14px,transparent 14px 26px)'});
  gsap.set(gap, {opacity: 0}); fade(gap, ev(i, 'split') + 0.3);
  const nt = mk(st, 'card', {left: '60px', top: '900px', width: '600px', height: '130px', fontSize: '30px'}, 'Lý Quang Diệu khóc trên truyền hình');
  const nn = mk(st, 'note', {left: '60px', top: '1040px', width: '600px', textAlign: 'center'}, 'theo video tham chiếu');
  gsap.set([nt, nn], {opacity: 0}); pop(nt, ev(i, 'note'), 0.5); fade(nn, ev(i, 'note') + 0.3);
}
// ---- 03 cards then position ----
{ const i = 2, st = stages[i];
  tag(i, 'Xuất phát điểm');
  sgLook('dot', ev(i, 'cards') - 0.3, 0.4); sgAt(600, S(2, 130), ev(i, 'cards') - 0.5, 0.9);
  const items = ['ĐẤT ÍT', 'KHÔNG TÀI NGUYÊN', 'DÂN NGHÈO'];
  const cards = items.map((t, n) => mk(st, 'card', {left: '60px', top: (230 + n * 160) + 'px', width: '600px', height: '120px'}, t));
  gsap.set(cards, {opacity: 0});
  cards.forEach((c, n) => pop(c, ev(i, 'cards') + n * 0.4, 0.45));
  const strikes = cards.map((c, n) => mk(st, 'abs', {left: '40px', top: (290 + n * 160) + 'px', width: '640px', height: '8px', background: '#ff6b5e', borderRadius: '4px', transformOrigin: '0 50%'}));
  gsap.set(strikes, {scaleX: 0});
  strikes.forEach((s, n) => tl.to(s, {scaleX: 1, duration: 0.35, ease: 'power3.out'}, ev(i, 'strike') + n * 0.25));
  tl.to(cards, {opacity: 0.45, duration: 0.4}, ev(i, 'strike') + 0.9);
  const pos = mk(st, 'card', {left: '60px', top: '760px', width: '600px', height: '170px', background: '#c8f169', fontSize: '60px', justifyContent: 'center', letterSpacing: '.04em'}, 'VỊ TRÍ');
  gsap.set(pos, {opacity: 0}); tl.fromTo(pos, {opacity: 0, scale: 0.8}, {opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.8)'}, ev(i, 'position'));
}
// ---- 04 schematic strait map ----
{ const i = 3, st = stages[i];
  tag(i, 'Sơ đồ minh họa · không theo tỉ lệ');
  const sea = mk(st, 'abs sea', {left: '0', top: '180px', width: '720px', height: '760px'});
  mk(st, 'abs', {left: '0', top: '180px', width: '300px', height: '300px', background: '#1c5a54', clipPath: 'polygon(0 0,100% 0,60% 100%,0 100%)'});
  mk(st, 'abs', {left: '0', top: '640px', width: '300px', height: '300px', background: '#1c5a54', clipPath: 'polygon(0 0,60% 0,100% 100%,0 100%)'});
  mk(st, 'abs', {left: '420px', top: '180px', width: '300px', height: '300px', background: '#1c5a54', clipPath: 'polygon(40% 0,100% 0,100% 100%,0 100%)'});
  mk(st, 'abs', {left: '420px', top: '640px', width: '300px', height: '300px', background: '#1c5a54', clipPath: 'polygon(0 0,100% 0,100% 100%,40% 100%)'});
  mk(st, 'lbl', {left: '40px', top: '860px', fontSize: '24px', color: '#ffd166'}, 'TRUNG ĐÔNG · CHÂU ÂU');
  mk(st, 'lbl', {left: '420px', top: '210px', fontSize: '24px', color: '#ffd166'}, 'TRUNG QUỐC · NHẬT · HÀN');
  const strait = mk(st, 'lbl lime', {left: '240px', top: '560px', width: '240px', textAlign: 'center', fontSize: '28px'}, 'EO BIỂN MALACCA');
  gsap.set(strait, {opacity: 0}); fade(strait, ev(i, 'strait'));
  const ship = mk(world, 'ship', {}); ship.id = 'ship'; ship.innerHTML = '<i></i><b></b>';
  gsap.set(ship, {x: 60, y: S(3, 880), opacity: 0});
  tl.to(ship, {opacity: 1, duration: 0.3}, ev(i, 'ships'));
  tl.to(ship, {x: 250, y: S(3, 700), duration: 1.6, ease: 'none'}, ev(i, 'ships'));
  tl.to(ship, {x: 360, y: S(3, 560), duration: 1.4, ease: 'none'}, ev(i, 'ships') + 1.6);
  tl.to(ship, {x: 520, y: S(3, 400), duration: 1.6, ease: 'none'}, ev(i, 'ships') + 3.0);
  tl.to(ship, {x: 640, y: S(3, 250), duration: 1.4, ease: 'none'}, ev(i, 'ships') + 4.6);
  sgLook('pin', ev(i, 'sg') - 0.3, 0.4);
  sgAt(470, S(3, 610), ev(i, 'sg') - 0.6, 0.9);
  tl.to(sg, {scale: 1.35, duration: 0.3, yoyo: true, repeat: 1, ease: 'power2.out'}, ev(i, 'sg'));
  const lab = mk(st, 'lbl', {left: '500px', top: '690px', fontSize: '28px'}, 'Singapore');
  gsap.set(lab, {opacity: 0}); fade(lab, ev(i, 'sg') + 0.2);
}
// ---- 05 one quarter ----
{ const i = 4, st = stages[i];
  tag(i, 'Quy mô · theo video tham chiếu');
  sgLook('pin', 0, 0.01); sgAt(640, S(4, 150), B[i].start - 0.6, 0.9);
  const q = mk(st, 'big lime', {left: '0', top: '220px', width: '720px', textAlign: 'center', fontSize: '240px'}, '¼');
  gsap.set(q, {opacity: 0}); tl.fromTo(q, {opacity: 0, scale: 0.7}, {opacity: 1, scale: 1, duration: 0.7, ease: 'back.out(1.6)'}, ev(i, 'quarter'));
  mk(st, 'lbl', {left: '60px', top: '560px', width: '600px', textAlign: 'center', whiteSpace: 'normal', fontSize: '30px'}, 'hàng hóa buôn bán của cả thế giới');
  const cells = [0, 1, 2, 3].map(n => mk(st, 'abs', {left: (260 + (n % 2) * 110) + 'px', top: (700 + Math.floor(n / 2) * 110) + 'px', width: '100px', height: '100px', borderRadius: '14px', background: 'rgba(255,255,255,.14)'}));
  tl.to(cells[0], {background: '#c8f169', duration: 0.5}, ev(i, 'quarter') + 0.3);
  const row = [0, 1, 2, 3, 4].map(n => { const s = mk(world, 'ship', {}); s.innerHTML = '<i></i><b></b>'; gsap.set(s, {x: -60, y: S(4, 940 + (n % 2) * 46), opacity: 0}); return s; });
  row.forEach((s, n) => { tl.to(s, {opacity: 1, duration: 0.2}, ev(i, 'stream') + n * 0.5); tl.to(s, {x: 780, duration: 3.2, ease: 'none'}, ev(i, 'stream') + n * 0.5); });
}
// ---- 06 passing ships pay nothing; port is built ----
{ const i = 5, st = stages[i];
  tag(i, 'Tàu chạy ngang');
  const ps = mk(world, 'ship', {}); ps.innerHTML = '<i></i><b></b>'; gsap.set(ps, {x: -60, y: S(5, 330), opacity: 0});
  tl.to(ps, {opacity: 1, duration: 0.2}, ev(i, 'pass') - 0.2); tl.to(ps, {x: 780, duration: 3.6, ease: 'none'}, ev(i, 'pass') - 0.2);
  const zero = mk(st, 'big red', {left: '260px', top: '210px', width: '200px', textAlign: 'center', fontSize: '84px'}, '0 đ');
  gsap.set(zero, {opacity: 0}); pop(zero, ev(i, 'pass'), 0.4);
  sgLook('port', ev(i, 'port') - 0.2, 0.4); gsap.set(sg, {scale: 1}); sgAt(360, S(5, 640), ev(i, 'port') - 0.6, 0.9);
  const perks = ['LỚN', 'NHANH', 'PHÍ HỢP LÝ'].map((t, n) => mk(st, 'card', {left: (40 + n * 215) + 'px', top: '800px', width: '200px', height: '110px', fontSize: '26px', justifyContent: 'center', textAlign: 'center', padding: '0 8px'}, t));
  gsap.set(perks, {opacity: 0}); perks.forEach((p, n) => pop(p, ev(i, 'perks') + n * 0.5, 0.45));
}
// ---- 07 hub: big ship drops containers, small ships fan out ----
{ const i = 6, st = stages[i];
  tag(i, 'Trung chuyển container');
  sgLook('port', 0, 0.01); sgAt(360, S(6, 560), B[i].start - 0.6, 0.9);
  const big = mk(world, 'ship', {}); big.innerHTML = '<i></i><b></b>'; gsap.set(big, {x: -80, y: S(6, 560), scale: 2.2, opacity: 0});
  tl.to(big, {opacity: 1, duration: 0.2}, ev(i, 'big') - 0.2); tl.to(big, {x: 120, duration: 2.0, ease: 'power2.out'}, ev(i, 'big') - 0.2);
  const cols = ['#ff6b5e', '#ffd166', '#7fe0c0', '#c8f169'];
  const conts = cols.map((c, n) => { const k = mk(world, 'cont', {background: c}); gsap.set(k, {x: 120 + n * 8, y: S(6, 520), opacity: 0}); return k; });
  conts.forEach((k, n) => { tl.to(k, {opacity: 1, duration: 0.1}, ev(i, 'big') + 1.4 + n * 0.25); tl.to(k, {x: 340, y: S(6, 560) + n * 4, duration: 0.8, ease: 'power2.inOut'}, ev(i, 'big') + 1.4 + n * 0.25); tl.to(k, {opacity: 0, duration: 0.2}, ev(i, 'big') + 2.3 + n * 0.25); });
  const lanes = [200, 330, 460];
  const smalls = lanes.map((y, n) => { const s = mk(world, 'ship', {}); s.innerHTML = '<i></i><b></b>'; gsap.set(s, {x: 380, y: S(6, 560), scale: 1, opacity: 0}); return s; });
  smalls.forEach((s, n) => { tl.to(s, {opacity: 1, duration: 0.2}, ev(i, 'small') + n * 0.3); tl.to(s, {x: 700, y: S(6, 560 + (n - 1) * 150), duration: 1.6, ease: 'power2.inOut'}, ev(i, 'small') + n * 0.3); });
  const vn = mk(st, 'card', {left: '420px', top: '840px', width: '260px', height: '90px', fontSize: '28px', justifyContent: 'center'}, 'HÀNG VIỆT NAM');
  gsap.set(vn, {opacity: 0}); pop(vn, ev(i, 'vn'), 0.5);
  const bd = mk(st, 'card', {left: '60px', top: '960px', width: '600px', height: '100px', background: '#c8f169', fontSize: '28px', justifyContent: 'center'}, 'MỘT TRONG NHỮNG CẢNG BẬN RỘN NHẤT');
  gsap.set(bd, {opacity: 0}); pop(bd, ev(i, 'badge'), 0.5);
}
// ---- 08 oil: zero wells, crude in, refinery, products out ----
{ const i = 7, st = stages[i];
  tag(i, 'Lọc dầu');
  sgLook('refin', B[i].start - 0.3, 0.4); sgAt(360, S(7, 560), B[i].start - 0.6, 0.9);
  const nw = mk(st, 'card', {left: '60px', top: '200px', width: '600px', height: '120px', justifyContent: 'center', background: 'rgba(255,255,255,.1)', color: '#fff', border: '2px solid #ff6b5e'}, '<span class="red">0</span>&nbsp;GIỌT DẦU');
  gsap.set(nw, {opacity: 0}); pop(nw, ev(i, 'nowell'), 0.5);
  const barrels = [0, 1, 2].map(n => { const k = mk(world, 'cont', {background: '#7f6a4a', width: '30px', height: '36px', borderRadius: '8px'}); gsap.set(k, {x: 40 + n * 6, y: S(7, 520 + n * 30), opacity: 0}); return k; });
  const buy = mk(st, 'lbl gold', {left: '70px', top: '640px', fontSize: '26px'}, 'MUA dầu thô');
  gsap.set(buy, {opacity: 0}); fade(buy, ev(i, 'crude'));
  barrels.forEach((k, n) => { tl.to(k, {opacity: 1, duration: 0.1}, ev(i, 'crude') + n * 0.35); tl.to(k, {x: 290, duration: 1.0, ease: 'power2.inOut'}, ev(i, 'crude') + n * 0.35); tl.to(k, {opacity: 0, duration: 0.15}, ev(i, 'crude') + 1.15 + n * 0.35); });
  tl.to(sg, {scale: 1.12, duration: 0.5, yoyo: true, repeat: 3, ease: 'sine.inOut'}, ev(i, 'refinery'));
  const prods = ['XĂNG', 'DẦU MÁY BAY'].map((t, n) => mk(st, 'card', {left: '470px', top: (480 + n * 120) + 'px', width: '210px', height: '90px', fontSize: '24px', justifyContent: 'center', padding: '0 8px', background: '#ffd166'}, t));
  gsap.set(prods, {opacity: 0}); prods.forEach((p, n) => pop(p, ev(i, 'products') + n * 0.4, 0.45));
  const sell = mk(st, 'lbl gold', {left: '470px', top: '720px', fontSize: '26px'}, 'BÁN cho khu vực');
  gsap.set(sell, {opacity: 0}); fade(sell, ev(i, 'products') + 0.5);
}
// ---- 09 four conditions ----
{ const i = 8, st = stages[i];
  tag(i, 'Bước cuối cùng');
  sgLook('hub', B[i].start - 0.3, 0.4); sgAt(360, S(8, 240), B[i].start - 0.6, 0.9);
  const tt = mk(st, 'big', {left: '40px', top: '420px', width: '640px', textAlign: 'center', fontSize: '56px', color: '#c8f169'}, 'Làm cho tiền muốn ở lại');
  gsap.set(tt, {opacity: 0}); pop(tt, ev(i, 'title'), 0.5);
  const items = ['LUẬT RÕ RÀNG', 'XỬ NẶNG THAM NHŨNG', 'TIẾNG ANH PHỔ BIẾN', 'THUẾ THẤP'];
  const cs = items.map((t, n) => mk(st, 'card', {left: (50 + (n % 2) * 310) + 'px', top: (560 + Math.floor(n / 2) * 190) + 'px', width: '290px', height: '160px', fontSize: '28px', justifyContent: 'center', textAlign: 'center', padding: '0 12px'}, t));
  gsap.set(cs, {opacity: 0}); cs.forEach((c, n) => pop(c, ev(i, 'cards') + n * 0.9, 0.5));
}
// ---- 10 money flows to the hub; ship icon becomes a coin ----
{ const i = 9, st = stages[i];
  tag(i, 'Dòng tiền minh họa');
  sgLook('hub', 0, 0.01); sgAt(360, S(9, 600), B[i].start - 0.6, 0.9);
  const srcs = [['TẬP ĐOÀN', 60, 200], ['NGÂN HÀNG', 480, 200], ['GIỚI NHÀ GIÀU', 270, 1000]];
  const nodes = srcs.map(([t, x, y]) => mk(st, 'card', {left: x + 'px', top: y + 'px', width: '190px', height: '90px', fontSize: '24px', justifyContent: 'center', padding: '0 6px'}, t));
  gsap.set(nodes, {opacity: 0});
  pop(nodes[0], ev(i, 'hq'), 0.5); pop(nodes[1], ev(i, 'money'), 0.5); pop(nodes[2], ev(i, 'money') + 0.6, 0.5);
  const coins = [[155, 290], [575, 290], [365, 1000]].map(([x, y], n) => { const c = mk(world, 'coin', {}, '$'); gsap.set(c, {x: x - 22, y: S(9, y) - 22, opacity: 0}); return c; });
  coins.forEach((c, n) => { const t0 = (n === 0 ? ev(i, 'hq') : ev(i, 'money')) + 0.8 + (n === 2 ? 0.6 : 0); tl.to(c, {opacity: 1, duration: 0.1}, t0); tl.to(c, {x: 338, y: S(9, 600) - 22, duration: 1.1, ease: 'power2.inOut'}, t0); tl.to(c, {opacity: 0, duration: 0.15}, t0 + 1.1); });
  const sh = mk(world, 'ship', {}); sh.innerHTML = '<i></i><b></b>'; gsap.set(sh, {x: 360, y: S(9, 600), opacity: 0, scale: 1.4});
  tl.to(sh, {opacity: 1, duration: 0.3}, ev(i, 'swap') - 0.1); tl.to(sh, {opacity: 0, scale: 0.2, duration: 0.5}, ev(i, 'swap') + 1.4);
  const bigcoin = mk(world, 'coin', {width: '120px', height: '120px', fontSize: '60px'}, '$'); gsap.set(bigcoin, {x: 300, y: S(9, 600) - 60, opacity: 0, scale: 0.2});
  tl.to(bigcoin, {opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.8)'}, ev(i, 'swap') + 1.5);
  const lg = mk(st, 'note', {left: '60px', top: '900px', width: '600px', textAlign: 'center'}, '$ = dòng tiền minh họa, không theo số liệu');
}
// ---- 11 three reasons ----
{ const i = 10, st = stages[i];
  tag(i, 'Tóm lại');
  sgLook('dot', B[i].start - 0.3, 0.4); sgAt(100, S(10, 240), B[i].start - 0.6, 0.9);
  const items = [['1', 'ĐỨNG ĐÚNG CHỖ', 'one'], ['2', 'BIẾN VỊ TRÍ THÀNH DỊCH VỤ AI ĐI NGANG CŨNG PHẢI DÙNG', 'two'], ['3', 'LÀM CHO TIỀN THẤY AN TOÀN ĐỂ Ở LẠI', 'three']];
  items.forEach(([n, t, k], idx) => {
    const c = mk(st, 'card', {left: '60px', top: (330 + idx * 210) + 'px', width: '600px', height: '180px', fontSize: '30px', gap: '22px'}, '<span class="big" style="font-size:84px;color:#7aa400">' + n + '</span><span>' + t + '</span>');
    gsap.set(c, {opacity: 0}); pop(c, ev(i, k), 0.55);
  });
}
// ---- 12 open question ----
{ const i = 11, st = stages[i];
  tag(i, 'Còn nơi nào nữa?');
  sgLook('dot', B[i].start - 0.3, 0.4); sgAt(360, S(11, 330), B[i].start - 0.6, 0.9);
  const q = mk(st, 'big', {left: '40px', top: '440px', width: '640px', textAlign: 'center', fontSize: '66px'}, 'Có chỗ nào làm được như vậy không?');
  gsap.set(q, {opacity: 0}); pop(q, ev(i, 'ask'), 0.6);
}

// ---- captions (sentence level, timing proportional to characters: estimated, not aligned) ----
const cap = $('#cap');
B.forEach(b => b.caps.forEach(c => {
  const d = mk(cap, 'c', {}, c.text);
  tl.fromTo(d, {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: 0.25, ease: 'power2.out'}, c.t);
  tl.to(d, {opacity: 0, duration: 0.18}, Math.max(c.t + 0.3, c.e - 0.05));
}));

window.__timelines['main'] = tl;
tl.seek(0);
"""


def build():
    doc = json.loads((ROOT / 'project.json').read_text(encoding='utf-8'))
    beats = beat_times(doc)
    total = max(b['end'] for b in beats) + 0.5
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'assets').mkdir(exist_ok=True)
    gsap = ROOT / 'assets' / 'vendor' / 'gsap.min.js'
    (OUT / 'assets' / 'gsap.min.js').write_bytes(gsap.read_bytes())
    html = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="{W}" data-height="{H}">
<div id="film" class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="0" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px">
<div id="cam"></div>
<div id="cap"></div>
</div>
</div>
<script>
{JS.replace('__BEATS__', json.dumps(beats, ensure_ascii=False))}
</script>
</body>
</html>
"""
    (OUT / 'index.html').write_text(html, encoding='utf-8')
    (OUT / 'meta.json').write_text(json.dumps({'id': 'singapore-remake', 'name': 'singapore-remake'}, indent=2) + '\n', encoding='utf-8')
    cfg = ROOT.parent.parent / 'hands' / 'hf-smoke' / 'hyperframes.json'
    if cfg.exists() and not (OUT / 'hyperframes.json').exists():
        (OUT / 'hyperframes.json').write_bytes(cfg.read_bytes())
    return total, len(beats)


if __name__ == '__main__':
    print(build())
