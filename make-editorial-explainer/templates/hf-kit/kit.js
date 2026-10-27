/* Builds one paused, seekable GSAP timeline from window.FILM (written by scripts/build_film.py).
   Deterministic by contract: no timers, randomness or network. Spec: references/hf-kit.md. */
(function () {
  const ICONS = {
    ship: '<svg viewBox="0 0 64 64"><path d="M4 36h56l-9 14H13z" fill="#ffd166"/><rect x="18" y="22" width="20" height="14" rx="2" fill="#f4f1e8"/><rect x="40" y="27" width="12" height="9" rx="1" fill="#ff6b5e"/><rect x="24" y="13" width="5" height="9" fill="#f4f1e8"/></svg>',
    coin: '<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="26" fill="#ffd166" stroke="#fff" stroke-width="4"/><path d="M38 22c-2-2-5-3-8-2.5-4 .7-6 3.5-5 6.5 1.2 3.6 12 3 13 7.5 1 4-3 7-8 6.5-3-.3-5-1.6-6.5-3.5M32 15v34" fill="none" stroke="#0b1d2a" stroke-width="4" stroke-linecap="round"/></svg>',
    box: '<svg viewBox="0 0 64 64"><rect x="6" y="18" width="52" height="30" rx="3" fill="#7fe0c0"/><path d="M16 22v22M26 22v22M36 22v22M46 22v22" stroke="#0b1d2a" stroke-opacity=".35" stroke-width="3"/></svg>',
    barrel: '<svg viewBox="0 0 64 64"><rect x="16" y="8" width="32" height="48" rx="8" fill="#8a6a3f"/><path d="M16 22h32M16 42h32" stroke="#ffd166" stroke-width="4"/></svg>',
    port: '<svg viewBox="0 0 64 64" fill="currentColor"><rect x="6" y="52" width="52" height="5" rx="1"/><rect x="16" y="12" width="5" height="40"/><rect x="16" y="12" width="38" height="5"/><path d="M48 17v12" stroke="currentColor" stroke-width="3"/><rect x="42" y="29" width="12" height="8" rx="1"/><rect x="26" y="40" width="14" height="12" rx="1"/><rect x="42" y="44" width="12" height="8" rx="1"/></svg>',
    factory: '<svg viewBox="0 0 64 64" fill="currentColor"><path d="M6 56V30l14 8v-8l14 8v-8l14 8V10h8v46z"/><rect x="14" y="44" width="6" height="6" fill-opacity=".35"/><rect x="28" y="44" width="6" height="6" fill-opacity=".35"/></svg>',
    bank: '<svg viewBox="0 0 64 64" fill="currentColor"><path d="M32 6 6 20v5h52v-5z"/><rect x="11" y="28" width="6" height="20"/><rect x="23" y="28" width="6" height="20"/><rect x="35" y="28" width="6" height="20"/><rect x="47" y="28" width="6" height="20"/><rect x="6" y="51" width="52" height="6"/></svg>',
    building: '<svg viewBox="0 0 64 64" fill="currentColor"><path d="M14 58V10l22-4v52z"/><path d="M38 58V24l14 4v30z" fill-opacity=".7"/><path d="M20 16h4v4h-4zM28 16h4v4h-4zM20 26h4v4h-4zM28 26h4v4h-4zM20 36h4v4h-4zM28 36h4v4h-4z" fill="#0b1d2a" fill-opacity=".45"/></svg>',
    person: '<svg viewBox="0 0 64 64" fill="currentColor"><circle cx="32" cy="20" r="11"/><path d="M12 58c0-13 9-21 20-21s20 8 20 21z"/></svg>',
    doc: '<svg viewBox="0 0 64 64"><path d="M14 6h26l12 12v40H14z" fill="#f4efe3"/><path d="M40 6v12h12" fill="#d8d2c4"/><path d="M21 28h22M21 36h22M21 44h14" stroke="#0b1d2a" stroke-opacity=".5" stroke-width="3"/></svg>',
    drop: '<svg viewBox="0 0 64 64" fill="currentColor"><path d="M32 6C24 20 14 30 14 40a18 18 0 0 0 36 0C50 30 40 20 32 6z"/></svg>'
  };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const rich = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, '<em>$1</em>');
  const px = (v) => v + 'px';
  function el(parent, cls, html, css) {
    const d = document.createElement('div');
    if (cls) d.className = cls;
    if (html !== undefined) d.innerHTML = html;
    if (css) Object.assign(d.style, css);
    parent.appendChild(d);
    return d;
  }

  function context(tl, b, layer) {
    const has = (id) => id && b.cues[id] !== undefined;
    const cue = (id, fallback) => (has(id) ? b.cues[id] : b.start + fallback);
    const groupIndex = {};
    const at = (item, group, fallback, step) => {
      if (item && has(item.id)) return b.cues[item.id];
      const k = (groupIndex[group] = (groupIndex[group] === undefined ? 0 : groupIndex[group] + 1));
      return cue(group, fallback) + k * (step === undefined ? 0.3 : step);
    };
    const pop = (n, t, d) => tl.fromTo(n, { autoAlpha: 0, y: 34, scale: 0.94 }, { autoAlpha: 1, y: 0, scale: 1, duration: d || 0.5, ease: 'back.out(1.5)' }, t);
    const fade = (n, t, d) => tl.fromTo(n, { autoAlpha: 0 }, { autoAlpha: 1, duration: d || 0.4, ease: 'power2.out' }, t);
    return { tl, b, layer, cue, at, pop, fade, el: (cls, html, css, parent) => el(parent || layer, cls, html, css) };
  }

  function token(parent, icon, size) {
    const s = size || 56;
    return el(parent, 'k-token', (ICONS[icon] || ICONS.box).replace('<svg ', `<svg width="${s}" height="${s}" style="left:${-s / 2}px;top:${-s / 2}px" `));
  }

  const ITEMS = {
    head(c, it, box, t) {
      const n = c.el('k-head', rich(it.text).split(/\s+/).map((w) => `<span class="w">${w}</span>`).join(' '), it.size ? { fontSize: px(it.size) } : null, box);
      c.tl.fromTo(n.querySelectorAll('.w'), { autoAlpha: 0, y: 26 }, { autoAlpha: 1, y: 0, duration: 0.42, ease: 'power3.out', stagger: 0.06 }, t);
      return n;
    },
    big(c, it, box, t) {
      const n = c.el('k-big', rich(it.text), it.size ? { fontSize: px(it.size) } : null, box);
      c.tl.fromTo(n, { autoAlpha: 0, scale: 0.6, transformOrigin: '0% 60%' }, { autoAlpha: 1, scale: 1, duration: 0.7, ease: 'back.out(1.8)' }, t);
      return n;
    },
    label(c, it, box, t) { const n = c.el('k-label', rich(it.text), null, box); c.pop(n, t, 0.45); return n; },
    chip(c, it, box, t) {
      const mark = it.mark ? `<span class="k-mark ${it.mark}">${it.mark === 'x' ? '×' : '✓'}</span>` : '';
      const n = c.el('k-chip', mark + rich(it.text), null, box); c.pop(n, t, 0.45); return n;
    },
    card(c, it, box, t) {
      const n = c.el('k-card ' + (it.tone || '') + (it.tall ? ' tall' : ''), (it.n ? `<span class="n">${esc(it.n)}</span>` : '') + `<div class="t">${rich(it.text)}</div>`, it.size ? { fontSize: px(it.size) } : null, box);
      c.pop(n, t, 0.5); return n;
    },
    grid(c, it, box, t, byId) {
      const g = c.el('k-grid2', undefined, null, box);
      it.items.forEach((sub, k) => { const n = ITEMS.card(c, Object.assign({ tall: true }, sub), g, c.at(sub, it.id, 0.3, 0.6) ); if (sub.id) byId[sub.id] = n; });
      return g;
    },
    split(c, it, box, t) {
      const n = c.el('k-split', `<div class="blk l">${rich(it.left)}</div><div class="blk r">${rich(it.right)}</div><div class="gap"></div>`, null, box);
      const [l, r, gap] = n.children;
      c.fade(n, t, 0.4);
      const ts = c.cue(it.split, 1.2);
      c.tl.fromTo(l, { x: 0 }, { x: -44, duration: 0.9, ease: 'power3.inOut' }, ts);
      c.tl.fromTo(r, { x: 0 }, { x: 44, duration: 0.9, ease: 'power3.inOut' }, ts);
      c.tl.fromTo(gap, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, ts + 0.4);
      return n;
    },
    space(c, it, box) { return c.el('', undefined, { height: px(it.h || 24) }, box); }
  };

  function stack(c, items, opt) {
    if (!items || !items.length) return;
    const box = c.el('k-stack' + (opt.center ? ' center' : ''), undefined, opt.center ? null : { top: px(opt.top) });
    const byId = {};
    items.forEach((it, k) => {
      const t = c.at(it, it.cue || '__stack', 0.25, it.cue ? 0.35 : 0.4);
      const n = (ITEMS[it.type] || ITEMS.card)(c, it, box, t, byId);
      if (it.id) byId[it.id] = n;
    });
    const s = opt.strike;
    if (s) {
      const targets = s.items.map((id) => byId[id]).filter(Boolean);
      targets.forEach((n, k) => {
        const line = el(n, 'k-strike');
        c.tl.fromTo(line, { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: 'power3.out' }, c.cue(s.id, 1.5) + k * 0.25);
      });
      if (s.dim !== false) c.tl.to(targets, { opacity: 0.42, duration: 0.4 }, c.cue(s.id, 1.5) + targets.length * 0.25 + 0.2);
    }
  }

  function route(c, cam, r) {
    const t0 = c.cue(r.id, 0.3);
    const path = cam.querySelector(`[data-route="${r.id}"]`);
    const glow = cam.querySelector(`[data-glow="${r.id}"]`);
    [path, glow].forEach((p) => { p.style.strokeDasharray = r.len; });
    if (r.draw !== false) c.tl.fromTo([path, glow], { strokeDashoffset: r.len }, { strokeDashoffset: 0, duration: r.draw_s || 2.2, ease: 'power2.inOut' }, t0);
    const n = r.ships || 0;
    const travel = r.ship_s || 4;
    for (let k = 0; k < n; k++) {
      const s = token(cam, r.token || 'ship', r.token_size || 54);
      const p0 = r.pts[0];
      const ts = c.cue(r.ships_cue || r.id, 0.3) + k * (r.ship_gap || 0.6);
      c.tl.set(s, { x: p0[0], y: p0[1], rotation: p0[2], autoAlpha: 0 }, 0);
      c.tl.to(s, { autoAlpha: 1, duration: 0.2 }, ts);
      c.tl.to(s, { keyframes: r.pts.slice(1).map((p) => ({ x: p[0], y: p[1], rotation: p[2], duration: travel * p[3], ease: 'none' })) }, ts);
      c.tl.to(s, { autoAlpha: 0, duration: 0.25 }, ts + travel - 0.25);
    }
  }

  function map(c, v) {
    const M = v.px;
    const wrap = c.el('k-map', undefined, { top: px(M.top), height: px(M.height) });
    const cam = el(wrap, 'cam', undefined, { width: '720px', height: px(M.height) });
    const grat = M.grat.map((d) => `<path class="grat" d="${d}"/>`).join('');
    const land = M.land.map((d) => `<path class="land" d="${d}"/>`).join('');
    const routes = M.routes.map((r) => `<path class="route-glow" data-glow="${r.id}" d="${r.d}"/><path class="route" data-route="${r.id}" d="${r.d}"/>`).join('');
    cam.insertAdjacentHTML('beforeend', `<svg width="720" height="${M.height}" viewBox="0 0 720 ${M.height}">${grat}${land}${routes}</svg>`);
    M.labels.forEach((l, k) => { const n = el(cam, 'k-maplabel ' + (l.tone || ''), rich(l.text), { left: px(l.x), top: px(l.y) }); c.fade(n, c.at(l, '__labels', 0.15, 0.12), 0.5); });
    M.routes.forEach((r) => route(c, cam, r));
    M.places.forEach((p) => {
      const n = el(cam, 'k-place' + (p.side === 'left' ? ' left' : ''), `<div class="ring"></div><div class="dot"></div><div class="name">${rich(p.name || '')}</div>`, { left: px(p.x), top: px(p.y) });
      const t = c.at(p, '__places', 0.4, 0.3);
      const [ring, dot, name] = n.children;
      c.tl.fromTo(dot, { autoAlpha: 0, scale: 0 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: 'back.out(2.4)' }, t);
      c.tl.fromTo(ring, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1.7, duration: 1.1, ease: 'power2.out', repeat: 2 }, t);
      c.tl.to(ring, { autoAlpha: 0, duration: 0.3 }, t + 3.3);
      c.fade(name, t + 0.2, 0.4);
    });
    const H = M.height;
    const focus = (f) => (f.scale === 1 ? { x: 0, y: 0, scale: 1 } : { x: 360 - f.fx * f.scale, y: H / 2 - f.fy * f.scale, scale: f.scale });
    c.tl.set(cam, M.camera_start ? focus(M.camera_start) : { x: 0, y: 0, scale: 1 }, 0);
    (M.camera || []).forEach((f) => c.tl.to(cam, Object.assign(focus(f), { duration: f.d || 1.4, ease: 'power2.inOut' }), c.cue(f.cue, 0) + (f.at || 0)));
    if (v.dim) c.tl.fromTo(wrap, { opacity: 1 }, { opacity: 0.45, duration: 0.6 }, c.cue(v.dim, 0.5));
    stack(c, v.stack, { top: M.top + M.height + 28, strike: v.strike });
  }

  function flow(c, v) {
    const nodes = {};
    (v.nodes || []).forEach((n) => { nodes[n.id] = n; });
    const edgeLayer = c.el('', undefined, { position: 'absolute', inset: '0' });
    const tokenLayer = c.el('', undefined, { position: 'absolute', inset: '0' });
    const nodeLayer = c.el('', undefined, { position: 'absolute', inset: '0' });
    (v.edges || []).forEach((e) => {
      const a = nodes[e.from], z = nodes[e.to];
      const dx = z.x - a.x, dy = z.y - a.y, len = Math.hypot(dx, dy) || 1;
      const ux = dx / len, uy = dy / len;
      const ca = a.hidden ? 0 : (e.inset || 80), cz = z.hidden ? 0 : (e.inset || 80);
      const t = c.at(e, '__edges', 0.6, 0.5);
      if (e.line !== false) {
        const svg = el(edgeLayer, 'k-edge ' + (e.kind || ''), `<svg width="720" height="1280"><line x1="${a.x + ux * ca}" y1="${a.y + uy * ca}" x2="${z.x - ux * cz}" y2="${z.y - uy * cz}"/></svg>`);
        c.fade(svg, t - 0.1, 0.4);
      }
      if (e.label) {
        const lb = el(edgeLayer, 'k-elabel', rich(e.label), { left: px((a.x + z.x) / 2 + (e.label_dx || 0)), top: px((a.y + z.y) / 2 + (e.label_dy || -34)) });
        c.pop(lb, t + 0.1, 0.4);
      }
      for (let k = 0; k < (e.count === undefined ? (e.token ? 1 : 0) : e.count); k++) {
        const s = token(tokenLayer, e.token || 'box', e.size || 52);
        const ts = t + k * (e.gap || 0.4);
        const travel = e.travel || 1.3;
        const rot = e.token === 'ship' ? Math.atan2(dy, dx) * 180 / Math.PI : 0;
        c.tl.set(s, { x: a.x, y: a.y, rotation: rot, autoAlpha: 0, scale: e.scale || 1 }, 0);
        c.tl.to(s, { autoAlpha: 1, duration: 0.15 }, ts);
        c.tl.to(s, { x: z.x, y: z.y, duration: travel, ease: e.ease || 'power1.inOut' }, ts);
        if (!e.stay) c.tl.to(s, { autoAlpha: 0, duration: 0.2 }, ts + travel - 0.15);
      }
    });
    Object.values(nodes).filter((n) => !n.hidden).forEach((n) => {
      const d = el(nodeLayer, 'k-node ' + (n.tone || '') + (n.icon ? '' : ' bare'), `<div class="ic">${ICONS[n.icon] || ''}</div>` + (n.text ? `<div class="tx">${rich(n.text)}</div>` : ''), { left: px(n.x), top: px(n.y) });
      c.pop(d, c.at(n, '__nodes', 0.2, 0.25), 0.5);
      if (n.pulse) c.tl.fromTo(d.firstChild, { scale: 1 }, { scale: 1.12, duration: 0.45, yoyo: true, repeat: 3, ease: 'sine.inOut' }, c.cue(n.pulse, 1));
    });
    (v.badges || []).forEach((bd) => {
      const d = el(nodeLayer, 'k-badge ' + (bd.tone || ''), rich(bd.text), { left: px(bd.x), top: px(bd.y) });
      c.pop(d, c.at(bd, '__badges', 0.8, 0.45), 0.5);
    });
    (v.swaps || []).forEach((sw) => {
      const from = token(nodeLayer, sw.from, sw.size || 110), to = token(nodeLayer, sw.to, sw.size || 110);
      [from, to].forEach((s) => c.tl.set(s, { x: sw.x, y: sw.y }, 0));
      const t = c.cue(sw.id, 1);
      c.tl.fromTo(from, { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.45, ease: 'back.out(2)' }, t);
      c.tl.to(from, { autoAlpha: 0, scale: 0.1, rotation: 90, duration: 0.4, ease: 'power2.in' }, t + (sw.after || 1.4));
      c.tl.fromTo(to, { autoAlpha: 0, scale: 0.1, rotation: -90 }, { autoAlpha: 1, scale: 1, rotation: 0, duration: 0.6, ease: 'back.out(2)' }, t + (sw.after || 1.4) + 0.3);
    });
    stack(c, v.stack, { top: v.stack_top || 640, strike: v.strike });
  }

  const SCENES = {
    stack: (c, v) => stack(c, v.stack, { top: v.top || 170, center: v.center, strike: v.strike }),
    map,
    flow
  };

  function build(F) {
    const film = document.getElementById('film');
    if (F.theme) document.getElementById('root').classList.add('theme-' + F.theme);
    const tl = gsap.timeline({ paused: true });
    el(film, 'k-bg'); el(film, 'k-grid');
    const stages = el(film, '');
    el(film, 'k-vignette');
    const prog = el(film, 'k-progress');
    tl.fromTo(prog, { scaleX: 0 }, { scaleX: 1, duration: F.total, ease: 'none' }, 0);
    F.beats.forEach((b, i) => {
      const st = el(stages, 'k-stage'); st.id = 'beat-' + b.id;
      const drift = el(st, 'k-drift');
      const v = b.visual || {};
      const c = context(tl, b, drift);
      (SCENES[v.kind] || SCENES.stack)(c, v);
      if (v.kicker) c.fade(c.el('k-kicker', rich(v.kicker)), b.start + 0.1, 0.4);
      if (v.note) c.fade(c.el('k-note', rich(v.note)), b.start + 0.6, 0.5);
      const next = F.beats[i + 1];
      const soft = v.continue;
      tl.fromTo(st, { autoAlpha: 0, y: soft ? 0 : 70 }, { autoAlpha: 1, y: 0, duration: soft ? 0.3 : 0.5, ease: 'power3.out', immediateRender: i === 0 }, Math.max(0, b.start - (i ? 0.12 : 0)));
      if (i > 0) tl.set(st, { autoAlpha: 0 }, 0);
      if (next) tl.to(st, { autoAlpha: 0, y: next.visual && next.visual.continue ? 0 : -60, duration: 0.32, ease: 'power2.in' }, b.end - 0.2);
      tl.fromTo(drift, { scale: 1 }, { scale: v.drift === undefined ? 1.035 : v.drift, duration: b.end - b.start + 0.4, ease: 'none' }, b.start);
    });
    const caps = el(film, 'k-cap');
    F.beats.forEach((b) => b.caps.forEach((cp) => {
      const d = el(caps, 'c', cp.html);
      tl.fromTo(d, { autoAlpha: 0, y: 12 }, { autoAlpha: 1, y: 0, duration: 0.2, ease: 'power2.out' }, cp.t);
      tl.to(d, { autoAlpha: 0, duration: 0.15 }, cp.e);
    }));
    return tl;
  }

  window.__timelines = window.__timelines || {};
  const tl = build(window.FILM);
  window.__timelines[window.FILM.composition || 'main'] = tl;
  tl.seek(0);
})();
