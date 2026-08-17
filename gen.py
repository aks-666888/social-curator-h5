# -*- coding: utf-8 -*-
# 社交策展名片 H5 生成器：用默认 persona（虚构示例）+ 6 套主题/架构配置，输出 6 个单文件 H5
import json
from persona import P
from themes import THEMES
from layouts import LAYOUTS

BASE = """
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:var(--font);line-height:1.5;-webkit-font-smoothing:antialiased}
img,svg{max-width:100%}
a{color:inherit}
@keyframes fu{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion: no-preference){
  .exhibit,.hall,.node,.cell,.bub,.block{animation:fu .6s ease both}
}
@media (prefers-reduced-motion: reduce){
  *{animation:none!important;transition:none!important}
}
"""

for t in THEMES:
    lay = LAYOUTS[t["layout"]]
    css, body = lay(P, t)
    root = "\n".join(f"--{k}:{v};" for k, v in t.items() if k not in ("id", "name", "cn", "layout", "desc"))
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{P['name']} · {t['name']} 社交策展名片</title>
<style>
:root{{{root}}}
{BASE}
{css}
</style>
</head>
<body>
{body}
</body>
</html>"""
    fn = f"E:/data/social-curator-h5/examples/{t['id']}.html"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK", t["id"], t["name"], "->", fn, len(html), "bytes")
print("DONE: 6 themes generated")
