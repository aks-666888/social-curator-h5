# -*- coding: utf-8 -*-
# 6 套布局渲染：每个 layout_* 返回 (css, body) 元组
# CSS 用普通字符串 + [[占位符]]，由 _fill 注入主题色（避免 f-string 大括号冲突）
# 共享 helper 输出语义化内容块；各 layout 负责"架构"（DOM 组织/顺序/导航）差异

import math

_KEYS = ["bg", "surface", "ink", "muted", "accent", "accent2", "line", "tag", "radius", "font"]


def _fill(raw, t):
    for k in _KEYS:
        raw = raw.replace("[[" + k + "]]", t[k])
    return raw


def _svg_icon(kind, color):
    icons = {
        "walk": '<path d="M4 20 L10 12 L7 8 L13 8 L11 4 L16 4 L14 10 L18 14 L12 20 Z" fill="{c}"/>',
        "cat": '<circle cx="8" cy="10" r="5" fill="{c}"/><circle cx="16" cy="10" r="5" fill="{c}"/><path d="M6 5 L8 9 M18 5 L16 9" stroke="{c}" stroke-width="1.5"/>',
        "film": '<rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="{c}" stroke-width="1.5"/><line x1="8" y1="5" x2="8" y2="19" stroke="{c}"/><line x1="16" y1="5" x2="16" y2="19" stroke="{c}"/>',
        "podcast": '<circle cx="12" cy="13" r="5" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M9 4 L15 4 M12 2 L12 4" stroke="{c}" stroke-width="1.5"/><path d="M10 18 Q12 22 14 18" stroke="{c}" stroke-width="1.5" fill="none"/>',
        "coffee": '<path d="M5 9 H17 V15 a4 4 0 0 1 -4 4 H9 a4 4 0 0 1 -4 -4 Z" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M17 11 h2 a2 2 0 0 1 0 4 h-2" fill="none" stroke="{c}" stroke-width="1.5"/>',
        "game": '<rect x="3" y="8" width="18" height="9" rx="3" fill="none" stroke="{c}" stroke-width="1.5"/><line x1="8" y1="8" x2="8" y2="17" stroke="{c}"/><line x1="16" y1="8" x2="16" y2="17" stroke="{c}"/><circle cx="5.5" cy="12" r="1" fill="{c}"/><circle cx="18.5" cy="12" r="1" fill="{c}"/>',
        "report": '<rect x="4" y="3" width="16" height="18" rx="2" fill="none" stroke="{c}" stroke-width="1.5"/><line x1="8" y1="8" x2="16" y2="8" stroke="{c}"/><line x1="8" y1="12" x2="16" y2="12" stroke="{c}"/><line x1="8" y1="16" x2="13" y2="16" stroke="{c}"/>',
        "json": '<polyline points="9 8 6 12 9 16" fill="none" stroke="{c}" stroke-width="1.5"/><polyline points="15 8 18 12 15 16" fill="none" stroke="{c}" stroke-width="1.5"/>',
        "card": '<rect x="3" y="6" width="18" height="12" rx="2" fill="none" stroke="{c}" stroke-width="1.5"/><line x1="7" y1="10" x2="11" y2="10" stroke="{c}"/><line x1="7" y1="13" x2="14" y2="13" stroke="{c}"/>',
        "local": '<rect x="5" y="11" width="14" height="9" rx="2" fill="none" stroke="{c}" stroke-width="1.5"/><path d="M8 11 V8 a4 4 0 0 1 8 0 V11" fill="none" stroke="{c}" stroke-width="1.5"/>',
        "book": '<path d="M5 4 h11 a2 2 0 0 1 2 2 v14 H7 a2 2 0 0 0 -2 2 Z" fill="none" stroke="{c}" stroke-width="1.5"/><line x1="9" y1="8" x2="15" y2="8" stroke="{c}"/>',
        "social": '<circle cx="6" cy="12" r="2.5" fill="none" stroke="{c}" stroke-width="1.5"/><circle cx="18" cy="6" r="2.5" fill="none" stroke="{c}" stroke-width="1.5"/><circle cx="18" cy="18" r="2.5" fill="none" stroke="{c}" stroke-width="1.5"/><line x1="8" y1="11" x2="16" y2="7" stroke="{c}"/><line x1="8" y1="13" x2="16" y2="17" stroke="{c}"/>',
        "default": '<rect x="5" y="5" width="14" height="14" rx="3" fill="none" stroke="{c}" stroke-width="1.5"/>',
    }
    return '<svg viewBox="0 0 24 24" width="100%" height="100%">' + icons.get(kind, icons["default"]).format(c=color) + '</svg>'


def _radar(skills, t):
    n = len(skills)
    cx = cy = R = 130
    pts = []
    for i, (name, val) in enumerate(skills):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        x = cx + R * val * math.cos(ang)
        y = cy + R * val * math.sin(ang)
        pts.append((x, y))
    rings = ""
    for rr in [0.25, 0.5, 0.75, 1.0]:
        poly = " ".join(f"{cx+R*rr*math.cos(-math.pi/2+i*2*math.pi/n):.1f},{cy+R*rr*math.sin(-math.pi/2+i*2*math.pi/n):.1f}" for i in range(n))
        rings += f'<polygon points="{poly}" fill="none" stroke="{t["line"]}"/>'
    axes = ""
    for i in range(n):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        axes += f'<line x1="{cx}" y1="{cy}" x2="{cx+R*math.cos(ang):.1f}" y2="{cy+R*math.sin(ang):.1f}" stroke="{t["line"]}"/>'
    dpoly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    data = f'<polygon points="{dpoly}" fill="{t["accent"]}33" stroke="{t["accent"]}" stroke-width="2"/>'
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{t["accent"]}"/>' for x, y in pts)
    labels = ""
    for i, (name, _) in enumerate(skills):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        lx = cx + (R + 16) * math.cos(ang)
        ly = cy + (R + 16) * math.sin(ang)
        labels += f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{t["muted"]}" font-size="10" text-anchor="middle">{name}</text>'
    return f'<svg viewBox="0 0 260 260" width="100%" style="max-width:300px">{rings}{axes}{data}{dots}{labels}</svg>'


def h_hero(P, t):
    vibes = "".join(f"<span>{v}</span>" for v in P["vibes"])
    return f'''<div class="c-hero">
  <div class="hero-name">{P["name"]}</div>
  <div class="hero-title">{P["title"]}</div>
  <div class="hero-slogan">{P["slogan"]}</div>
  <div class="hero-vibes">{vibes}</div>
</div>'''


def h_stats(P, t):
    return '<div class="c-stats">' + "".join(
        f'<div class="c-stat"><b>{v}</b><span class="num">{n}</span><span class="unit">{u}</span></div>'
        for v, n, u in P["stats"]) + '</div>'


def h_timeline(P, t):
    rows = ""
    for yr, work, life in P["timeline"]:
        rows += f'''<div class="tl-row">
  <div class="tl-year">{yr}</div>
  <div class="tl-work"><i>事业</i>{work}</div>
  <div class="tl-life"><i>生活</i>{life}</div>
</div>'''
    return f'<div class="c-tl">{rows}</div>'


def h_bento(P, t):
    cells = ""
    for title, note, kind in P["bento"]:
        cells += f'''<div class="c-bento-item">
  <div class="b-ico">{_svg_icon(kind, t["accent"])}</div>
  <div class="b-title">{title}</div>
  <div class="b-note">{note}</div>
</div>'''
    return f'<div class="c-bento">{cells}</div>'


def h_skills(P, t):
    legend = "".join(f'<div class="sk-row"><span>{name}</span><div class="sk-bar"><i style="width:{int(val*100)}%"></i></div></div>' for name, val in P["skills"])
    return f'''<div class="c-skills">
  {_radar(P["skills"], t)}
  <div class="sk-legend">{legend}</div>
</div>'''


def h_testi(P, t):
    cards = ""
    for who, text, tag in P["testimonials"]:
        cards += f'''<div class="c-testi-card"><div class="t-text">{text}</div><div class="t-meta"><span class="t-who">{who}</span><span class="t-tag">{tag}</span></div></div>'''
    return f'<div class="c-testi">{cards}</div>'


def h_contact(P, t):
    rows = ""
    for ch, idv, ice in P["contacts"]:
        rows += f'''<div class="c-contact-row">
  <div class="cc-ch">{ch}</div>
  <div class="cc-id">{idv}</div>
  <div class="cc-ice">{ice}</div>
</div>'''
    return f'<div class="c-contact">{rows}</div>'


def _section(num, title, inner, t, cls=""):
    return f'''<section class="exhibit {cls}">
  <div class="exh-label" style="color:{t['accent2']}">Exhibit {num:02d} · {title}</div>
  {inner}
</section>'''


# =================== A：竖向七组件滚动（画廊风） ===================
def layout_A(P, t):
    raw = '''
    .page{max-width:680px;margin:0 auto;padding:24px 18px 80px}
    .exhibit{margin:30px 0;background:[[surface]];border:1px solid [[line]];border-radius:[[radius]];padding:22px}
    .exh-label{font-size:12px;letter-spacing:2px;margin-bottom:14px;font-weight:700}
    .hero-name{font-size:34px;font-weight:800;color:[[ink]]}
    .hero-title{font-size:16px;color:[[accent]];margin:4px 0 10px;font-weight:700}
    .hero-slogan{font-size:15px;color:[[muted]];line-height:1.7}
    .hero-vibes{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px}
    .hero-vibes span{background:[[tag]];color:[[ink]];font-size:12px;padding:5px 11px;border-radius:20px}
    .c-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
    .c-stat{background:[[tag]];border-radius:12px;padding:12px;text-align:center}
    .c-stat b{display:block;font-size:12px;color:[[muted]]}
    .c-stat .num{font-size:24px;font-weight:800;color:[[accent]]}
    .c-stat .unit{font-size:11px;color:[[muted]]}
    .c-tl .tl-row{display:grid;grid-template-columns:54px 1fr 1fr;gap:10px;padding:12px 0;border-bottom:1px dashed [[line]]}
    .tl-year{font-weight:800;color:[[accent]]}
    .tl-work i,.tl-life i{font-style:normal;font-size:10px;color:[[muted]];display:block;margin-bottom:2px}
    .c-bento{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
    .c-bento-item{background:[[tag]];border-radius:12px;padding:14px}
    .b-ico{width:34px;height:34px;margin-bottom:8px}
    .b-title{font-weight:700;color:[[ink]]}
    .b-note{font-size:12px;color:[[muted]];margin-top:4px;line-height:1.5}
    .c-skills{display:flex;flex-wrap:wrap;gap:16px;align-items:center}
    .sk-legend{flex:1;min-width:200px}
    .sk-row{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:13px;color:[[ink]]}
    .sk-bar{flex:1;height:7px;background:[[line]];border-radius:4px;overflow:hidden}
    .sk-bar i{display:block;height:100%;background:[[accent]]}
    .c-testi{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .c-testi-card{background:[[tag]];border-radius:12px;padding:14px}
    .t-text{font-size:14px;color:[[ink]];line-height:1.6}
    .t-meta{margin-top:8px;display:flex;justify-content:space-between;font-size:11px}
    .t-who{color:[[accent]];font-weight:700}
    .t-tag{color:[[muted]]}
    .c-contact-row{display:grid;grid-template-columns:64px 1fr;gap:6px 12px;padding:10px 0;border-bottom:1px solid [[line]]}
    .cc-ch{font-weight:700;color:[[accent]]}
    .cc-id{font-size:13px;color:[[ink]]}
    .cc-ice{grid-column:2;font-size:12px;color:[[muted]]}
    @media(max-width:480px){.c-stats,.c-bento,.c-testi{grid-template-columns:1fr}}
    '''
    body = f'''<div class="page">
      {_section(1,'身份 · HeroCard',h_hero(P,t),t)}
      {_section(2,'数据 · StatsBoard',h_stats(P,t),t)}
      {_section(3,'时间轴 · TimelinePro',h_timeline(P,t),t)}
      {_section(4,'兴趣 · BentoGallery',h_bento(P,t),t)}
      {_section(5,'技能 · SkillRadar',h_skills(P,t),t)}
      {_section(6,'朋友说 · Testimonial',h_testi(P,t),t)}
      {_section(7,'联系 · ContactSocial',h_contact(P,t),t)}
    </div>'''
    return _fill(raw, t), body


# =================== B：左侧固定 Hero 栏 + 右侧滚动 ===================
def layout_B(P, t):
    raw = '''
    .wrap{display:flex;gap:0;max-width:960px;margin:0 auto;min-height:100vh}
    .side{position:sticky;top:0;align-self:flex-start;width:300px;height:100vh;background:[[surface]];border-right:1px solid [[line]];padding:32px 24px;overflow:auto}
    .main{flex:1;padding:32px 28px}
    .hero-name{font-size:30px;font-weight:800;color:[[ink]]}
    .hero-title{font-size:15px;color:[[accent]];margin:6px 0 14px;font-weight:700}
    .hero-slogan{font-size:14px;color:[[muted]];line-height:1.7}
    .hero-vibes{margin-top:16px;display:flex;flex-wrap:wrap;gap:7px}
    .hero-vibes span{background:[[tag]];color:[[muted]];font-size:11px;padding:4px 10px;border-radius:14px}
    .side .c-stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:20px}
    .c-stat{background:[[tag]];border-radius:8px;padding:9px;text-align:center}
    .c-stat b{display:block;font-size:10px;color:[[muted]]}
    .c-stat .num{font-size:20px;font-weight:800;color:[[accent]]}
    .side .c-contact{margin-top:20px}
    .c-contact-row{padding:8px 0;border-bottom:1px solid [[line]];font-size:12px}
    .cc-ch{color:[[accent]];font-weight:700}
    .cc-id{color:[[ink]]}
    .cc-ice{color:[[muted]];font-size:11px;margin-top:2px}
    .block{margin-bottom:34px}
    .block h3{font-size:13px;letter-spacing:2px;color:[[accent]];border-left:3px solid [[accent]];padding-left:10px;margin-bottom:14px}
    .c-tl .tl-row{display:grid;grid-template-columns:48px 1fr;gap:10px;padding:10px 0;border-bottom:1px dashed [[line]]}
    .tl-year{font-weight:800;color:[[accent]]}
    .tl-work i,.tl-life i{font-style:normal;font-size:10px;color:[[muted]];margin-right:6px}
    .c-bento{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .c-bento-item{background:[[tag]];border-radius:10px;padding:12px}
    .b-ico{width:30px;height:30px;margin-bottom:6px}
    .b-title{font-weight:700;color:[[ink]];font-size:14px}
    .b-note{font-size:11px;color:[[muted]];margin-top:3px}
    .c-skills{display:flex;gap:16px;flex-wrap:wrap;align-items:center}
    .sk-legend{flex:1;min-width:180px}
    .sk-row{display:flex;align-items:center;gap:8px;font-size:12px;color:[[ink]];margin:5px 0}
    .sk-bar{flex:1;height:6px;background:[[line]];border-radius:3px;overflow:hidden}
    .sk-bar i{display:block;height:100%;background:[[accent]]}
    .c-testi{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .c-testi-card{background:[[tag]];border-radius:10px;padding:12px}
    .t-text{font-size:13px;color:[[ink]];line-height:1.5}
    .t-meta{margin-top:7px;display:flex;justify-content:space-between;font-size:10px}
    .t-who{color:[[accent]];font-weight:700} .t-tag{color:[[muted]]}
    @media(max-width:720px){.wrap{flex-direction:column}.side{position:relative;width:auto;height:auto;border-right:none;border-bottom:1px solid [[line]]}}
    '''
    body = f'''<div class="wrap">
      <aside class="side">
        {h_hero(P,t)}
        {h_stats(P,t)}
        {h_contact(P,t)}
      </aside>
      <main class="main">
        <div class="block"><h3>TIMELINE · 双轨</h3>{h_timeline(P,t)}</div>
        <div class="block"><h3>BENTO · 兴趣</h3>{h_bento(P,t)}</div>
        <div class="block"><h3>SKILLS · 雷达</h3>{h_skills(P,t)}</div>
        <div class="block"><h3>FRIENDS · 朋友说</h3>{h_testi(P,t)}</div>
      </main>
    </div>'''
    return _fill(raw, t), body


# =================== C：全局 Bento 拼贴（极简模块） ===================
def layout_C(P, t):
    raw = '''
    .page{max-width:760px;margin:0 auto;padding:20px 14px 70px}
    .bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(90px,auto);gap:12px}
    .cell{background:[[surface]];border:1px solid [[line]];border-radius:[[radius]];padding:16px;overflow:hidden}
    .cell.hero{grid-column:span 4;background:[[accent]];color:#000}
    .cell.hero .hero-name{font-size:30px;font-weight:800}
    .cell.hero .hero-title{color:#000;opacity:.7;font-weight:700;margin:4px 0}
    .cell.hero .hero-slogan{font-size:14px;opacity:.85;line-height:1.6}
    .cell.hero .hero-vibes{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px}
    .cell.hero .hero-vibes span{background:#00000022;color:#000;font-size:11px;padding:4px 9px;border-radius:12px}
    .cell.stats{grid-column:span 4;display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
    .cell.stats .c-stat{text-align:center}
    .cell.stats .c-stat b{display:block;font-size:10px;color:[[muted]]}
    .cell.stats .c-stat .num{font-size:20px;font-weight:800;color:[[accent]]}
    .cell.stats .c-stat .unit{font-size:10px;color:[[muted]]}
    .cell.tl{grid-column:span 2}
    .cell.bento-g{grid-column:span 2}
    .cell.skills{grid-column:span 2}
    .cell.testi{grid-column:span 4;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
    .cell.contact{grid-column:span 4}
    .c-tl .tl-row{display:grid;grid-template-columns:40px 1fr;gap:6px;padding:7px 0;border-bottom:1px dashed [[line]];font-size:12px}
    .tl-year{font-weight:800;color:[[accent]]}
    .tl-work i,.tl-life i{font-style:normal;font-size:9px;color:[[muted]];margin-right:4px}
    .c-bento{display:grid;grid-template-columns:1fr 1fr;gap:8px}
    .c-bento-item{background:[[tag]];border-radius:10px;padding:10px}
    .b-ico{width:26px;height:26px;margin-bottom:5px}
    .b-title{font-weight:700;color:[[ink]];font-size:13px}
    .b-note{font-size:10px;color:[[muted]]}
    .c-skills{display:block}
    .sk-legend .sk-row{display:flex;font-size:11px;color:[[ink]];margin:4px 0}
    .sk-bar{flex:1;height:6px;background:[[line]];border-radius:3px;overflow:hidden;margin-left:6px}
    .sk-bar i{display:block;height:100%;background:[[accent]]}
    .c-testi-card{background:[[tag]];border-radius:10px;padding:10px}
    .t-text{font-size:12px;color:[[ink]];line-height:1.4}
    .t-meta{margin-top:6px;font-size:9px;display:flex;justify-content:space-between}
    .t-who{color:[[accent]];font-weight:700} .t-tag{color:[[muted]]}
    .c-contact-row{display:grid;grid-template-columns:60px 1fr;gap:4px 10px;padding:7px 0;border-bottom:1px solid [[line]];font-size:12px}
    .cc-ch{color:[[accent]];font-weight:700} .cc-id{color:[[ink]]}
    .cc-ice{grid-column:2;color:[[muted]];font-size:10px}
    @media(max-width:560px){.bento{grid-template-columns:repeat(2,1fr)}.cell.hero,.cell.stats,.cell.testi,.cell.contact{grid-column:span 2}.cell.tl,.cell.bento-g,.cell.skills{grid-column:span 2}.cell.stats{grid-template-columns:repeat(3,1fr)}}
    '''
    testi_cards = "".join(
        f'<div class="c-testi-card"><div class="t-text">{tx}</div><div class="t-meta"><span class="t-who">{w}</span><span class="t-tag">{g}</span></div></div>'
        for w, tx, g in P["testimonials"])
    body = f'''<div class="page"><div class="bento">
      <div class="cell hero">{h_hero(P,t)}</div>
      <div class="cell stats">{h_stats(P,t)}</div>
      <div class="cell tl"><b style="color:[[accent]];font-size:12px">TIMELINE</b>{h_timeline(P,t)}</div>
      <div class="cell bento-g"><b style="color:[[accent]];font-size:12px">BENTO</b>{h_bento(P,t)}</div>
      <div class="cell skills"><b style="color:[[accent]];font-size:12px">SKILLS</b>{h_skills(P,t)}</div>
      <div class="cell testi"><b style="color:[[accent]];font-size:12px;grid-column:3">FRIENDS</b>{testi_cards}</div>
      <div class="cell contact">{h_contact(P,t)}</div>
    </div></div>'''
    return _fill(raw, t), _fill(body, t)


# =================== D：时间轴脊背贯穿 ===================
def layout_D(P, t):
    raw = '''
    .page{max-width:720px;margin:0 auto;padding:24px 16px 80px}
    .spine{position:relative;padding-left:30px}
    .spine::before{content:"";position:absolute;left:9px;top:0;bottom:0;width:3px;background:[[accent]];border-radius:2px}
    .node{position:relative;margin:22px 0;background:[[surface]];border:1px solid [[line]];border-radius:[[radius]];padding:18px}
    .node::before{content:"";position:absolute;left:-26px;top:22px;width:14px;height:14px;background:[[accent]];border:3px solid [[bg]];border-radius:50%}
    .node-year{font-size:13px;font-weight:800;color:[[accent]];margin-bottom:8px}
    .node h3{font-size:13px;letter-spacing:1px;color:[[muted]];margin:0 0 10px}
    .hero-name{font-size:32px;font-weight:800;color:[[ink]]}
    .hero-title{font-size:15px;color:[[accent]];font-weight:700;margin:4px 0 10px}
    .hero-slogan{font-size:14px;color:[[muted]];line-height:1.7}
    .hero-vibes{margin-top:12px;display:flex;flex-wrap:wrap;gap:7px}
    .hero-vibes span{background:[[tag]];color:[[ink]];font-size:11px;padding:4px 10px;border-radius:14px}
    .c-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:6px}
    .c-stat{background:[[tag]];border-radius:10px;padding:10px;text-align:center}
    .c-stat b{display:block;font-size:10px;color:[[muted]]}
    .c-stat .num{font-size:22px;font-weight:800;color:[[accent]]}
    .c-bento{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:6px}
    .c-bento-item{background:[[tag]];border-radius:10px;padding:11px}
    .b-ico{width:28px;height:28px;margin-bottom:5px}
    .b-title{font-weight:700;color:[[ink]];font-size:13px}
    .b-note{font-size:10px;color:[[muted]]}
    .c-skills{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
    .sk-legend{flex:1;min-width:170px}
    .sk-row{display:flex;align-items:center;gap:6px;font-size:12px;color:[[ink]];margin:4px 0}
    .sk-bar{flex:1;height:6px;background:[[line]];border-radius:3px;overflow:hidden}
    .sk-bar i{display:block;height:100%;background:[[accent]]}
    .c-testi{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:6px}
    .c-testi-card{background:[[tag]];border-radius:10px;padding:11px}
    .t-text{font-size:13px;color:[[ink]];line-height:1.5}
    .t-meta{margin-top:6px;font-size:10px;display:flex;justify-content:space-between}
    .t-who{color:[[accent]];font-weight:700} .t-tag{color:[[muted]]}
    .c-contact-row{display:grid;grid-template-columns:60px 1fr;gap:4px 10px;padding:8px 0;border-bottom:1px solid [[line]];font-size:12px}
    .cc-ch{color:[[accent]];font-weight:700} .cc-id{color:[[ink]]}
    .cc-ice{grid-column:2;color:[[muted]];font-size:10px}
    @media(max-width:480px){.c-stats,.c-bento,.c-testi{grid-template-columns:1fr}}
    '''
    nodes = f'<div class="node">{h_hero(P,t)}</div>'
    nodes += f'<div class="node"><div class="node-year">数据快照</div><h3>STATSBOARD</h3>{h_stats(P,t)}</div>'
    for yr, work, life in P["timeline"]:
        nodes += f'''<div class="node"><div class="node-year">{yr}</div>
          <div class="tl-work" style="font-size:13px;color:[[ink]];margin:4px 0"><i style="font-style:normal;font-size:10px;color:[[muted]]">事业</i>{work}</div>
          <div class="tl-life" style="font-size:13px;color:[[ink]]"><i style="font-style:normal;font-size:10px;color:[[muted]]">生活</i>{life}</div>
        </div>'''
    nodes += f'<div class="node"><div class="node-year">兴趣档案</div><h3>BENTOGALLERY</h3>{h_bento(P,t)}</div>'
    nodes += f'<div class="node"><div class="node-year">能力雷达</div><h3>SKILLRADAR</h3>{h_skills(P,t)}</div>'
    nodes += f'<div class="node"><div class="node-year">朋友证言</div><h3>TESTIMONIAL</h3>{h_testi(P,t)}</div>'
    nodes += f'<div class="node"><div class="node-year">找我玩</div><h3>CONTACTSOCIAL</h3>{h_contact(P,t)}</div>'
    body = f'<div class="page"><div class="spine">{nodes}</div></div>'
    # 注意：body 里用了 [[ink]] 等占位，需同样 fill
    body = _fill(body, t)
    return _fill(raw, t), body


# =================== E：对话气泡叙事 ===================
def layout_E(P, t):
    raw = '''
    .page{max-width:640px;margin:0 auto;padding:20px 14px 80px}
    .chat{display:flex;flex-direction:column;gap:14px}
    .bub{max-width:88%;padding:14px 16px;border-radius:18px;font-size:14px;line-height:1.6}
    .ask{align-self:flex-start;background:[[tag]];color:[[ink]];border-bottom-left-radius:4px}
    .ans{align-self:flex-end;background:[[accent]];color:#fff;border-bottom-right-radius:4px}
    .ans .hero-name{font-size:22px;font-weight:800}
    .ans .hero-title{font-size:13px;opacity:.85;font-weight:700;margin:3px 0}
    .ans .hero-slogan{font-size:13px;opacity:.92}
    .ans .hero-vibes{margin-top:10px;display:flex;flex-wrap:wrap;gap:6px}
    .ans .hero-vibes span{background:#ffffff33;font-size:11px;padding:3px 9px;border-radius:12px}
    .ans .c-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:8px}
    .ans .c-stat{background:#ffffff22;text-align:center;border-radius:10px;padding:8px}
    .ans .c-stat b{display:block;font-size:10px;opacity:.8}
    .ans .c-stat .num{font-size:19px;font-weight:800}
    .ans .c-bento{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
    .ans .c-bento-item{background:#ffffff22;border-radius:10px;padding:10px}
    .ans .b-ico{width:26px;height:26px;margin-bottom:4px}
    .ans .b-title{font-weight:700;font-size:13px} .ans .b-note{font-size:10px;opacity:.85}
    .ans .c-skills{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:6px}
    .ans .sk-legend{flex:1;min-width:160px}
    .ans .sk-row{display:flex;font-size:11px;margin:3px 0}
    .ans .sk-bar{flex:1;height:6px;background:#ffffff33;border-radius:3px;overflow:hidden;margin-left:6px}
    .ans .sk-bar i{display:block;height:100%;background:#fff}
    .ans .c-testi{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px}
    .ans .c-testi-card{background:#ffffff1a;border-radius:10px;padding:10px}
    .ans .t-text{font-size:12px;line-height:1.4}
    .ans .t-meta{margin-top:6px;font-size:9px;display:flex;justify-content:space-between;opacity:.85}
    .ans .c-contact-row{padding:7px 0;border-bottom:1px solid #ffffff33;font-size:12px}
    .ans .cc-ch{font-weight:700} .ans .cc-id{opacity:.95}
    .ans .cc-ice{font-size:10px;opacity:.8;margin-top:2px}
    .sys{align-self:center;font-size:11px;color:[[muted]];background:[[tag]];padding:4px 12px;border-radius:12px}
    @media(max-width:480px){.ans .c-stats,.ans .c-bento,.ans .c-testi{grid-template-columns:1fr}}
    '''
    body = f'''<div class="page"><div class="chat">
      <div class="sys">你和{P['name']}的对话</div>
      <div class="bub ask">你是干啥的？给我整张能交朋友的卡片呗。</div>
      <div class="bub ans">{h_hero(P,t)}</div>
      <div class="bub ask">有点意思。你平时都折腾些啥？</div>
      <div class="bub ans">{h_stats(P,t)}</div>
      <div class="bub ask">这几年怎么过来的？</div>
      <div class="bub ans">{h_timeline(P,t)}</div>
      <div class="bub ask">爱好呢？别光说工作。</div>
      <div class="bub ans">{h_bento(P,t)}</div>
      <div class="bub ask">你擅长啥？</div>
      <div class="bub ans">{h_skills(P,t)}</div>
      <div class="bub ask">朋友怎么评价你？</div>
      <div class="bub ans">{h_testi(P,t)}</div>
      <div class="bub ask">那去哪找你耍？</div>
      <div class="bub ans">{h_contact(P,t)}</div>
    </div></div>'''
    return _fill(raw, t), body


# =================== F：展厅分区 + 顶部导航 ===================
def layout_F(P, t):
    raw = '''
    .nav{position:sticky;top:0;z-index:9;background:[[surface]];border-bottom:1px solid [[line]];display:flex;gap:6px;overflow-x:auto;padding:12px 14px}
    .nav a{text-decoration:none;color:[[ink]];font-size:12px;background:[[tag]];padding:6px 12px;border-radius:16px;white-space:nowrap}
    .nav a:hover{background:[[accent]];color:#fff}
    .page{max-width:720px;margin:0 auto;padding:24px 16px 80px}
    .hall{margin:34px 0;scroll-margin-top:60px}
    .hall-h{font-size:15px;font-weight:800;color:[[accent2]];margin-bottom:14px;display:flex;align-items:center;gap:8px}
    .hall-h::before{content:"";width:10px;height:10px;border-radius:50%;background:[[accent]]}
    .hero-name{font-size:32px;font-weight:800;color:[[ink]]}
    .hero-title{font-size:15px;color:[[accent]];font-weight:700;margin:4px 0 10px}
    .hero-slogan{font-size:14px;color:[[muted]];line-height:1.7}
    .hero-vibes{margin-top:12px;display:flex;flex-wrap:wrap;gap:7px}
    .hero-vibes span{background:[[tag]];color:[[ink]];font-size:11px;padding:4px 10px;border-radius:14px}
    .c-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
    .c-stat{background:[[tag]];border-radius:12px;padding:12px;text-align:center}
    .c-stat b{display:block;font-size:10px;color:[[muted]]}
    .c-stat .num{font-size:22px;font-weight:800;color:[[accent]]}
    .c-tl .tl-row{display:grid;grid-template-columns:48px 1fr 1fr;gap:8px;padding:10px 0;border-bottom:1px dashed [[line]];font-size:13px}
    .tl-year{font-weight:800;color:[[accent]]}
    .tl-work i,.tl-life i{font-style:normal;font-size:10px;color:[[muted]];display:block}
    .c-bento{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
    .c-bento-item{background:[[tag]];border-radius:12px;padding:13px}
    .b-ico{width:30px;height:30px;margin-bottom:6px}
    .b-title{font-weight:700;color:[[ink]]} .b-note{font-size:11px;color:[[muted]];margin-top:3px}
    .c-skills{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
    .sk-legend{flex:1;min-width:180px}
    .sk-row{display:flex;align-items:center;gap:6px;font-size:12px;color:[[ink]];margin:4px 0}
    .sk-bar{flex:1;height:6px;background:[[line]];border-radius:3px;overflow:hidden}
    .sk-bar i{display:block;height:100%;background:[[accent]]}
    .c-testi{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .c-testi-card{background:[[tag]];border-radius:12px;padding:13px}
    .t-text{font-size:13px;color:[[ink]];line-height:1.5}
    .t-meta{margin-top:7px;font-size:10px;display:flex;justify-content:space-between}
    .t-who{color:[[accent]];font-weight:700} .t-tag{color:[[muted]]}
    .c-contact-row{display:grid;grid-template-columns:60px 1fr;gap:4px 10px;padding:9px 0;border-bottom:1px solid [[line]];font-size:12px}
    .cc-ch{color:[[accent]];font-weight:700} .cc-id{color:[[ink]]}
    .cc-ice{grid-column:2;color:[[muted]];font-size:10px}
    @media(max-width:480px){.c-stats,.c-bento,.c-testi{grid-template-columns:1fr}}
    '''
    nav = '<div class="nav"><a href="#h1">① 身份</a><a href="#h2">② 数据</a><a href="#h3">③ 时间轴</a><a href="#h4">④ 作品</a><a href="#h5">⑤ 技能</a><a href="#h6">⑥ 朋友</a><a href="#h7">⑦ 联系</a></div>'
    body = f'''{nav}<div class="page">
      <div class="hall" id="h1"><div class="hall-h">1 号厅 · 身份</div>{h_hero(P,t)}</div>
      <div class="hall" id="h2"><div class="hall-h">2 号厅 · 数据快照</div>{h_stats(P,t)}</div>
      <div class="hall" id="h3"><div class="hall-h">3 号厅 · 成长时间轴</div>{h_timeline(P,t)}</div>
      <div class="hall" id="h4"><div class="hall-h">4 号厅 · 兴趣作品</div>{h_bento(P,t)}</div>
      <div class="hall" id="h5"><div class="hall-h">5 号厅 · 能力雷达</div>{h_skills(P,t)}</div>
      <div class="hall" id="h6"><div class="hall-h">6 号厅 · 朋友证言</div>{h_testi(P,t)}</div>
      <div class="hall" id="h7"><div class="hall-h">7 号厅 · 联系策展人</div>{h_contact(P,t)}</div>
    </div>'''
    return _fill(raw, t), body


LAYOUTS = {"A": layout_A, "B": layout_B, "C": layout_C, "D": layout_D, "E": layout_E, "F": layout_F}
