#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gom gói deploy/ để đẩy lên GitHub Pages hoặc Netlify (chạy sau mỗi lần build)."""
import os
import shutil

D = os.path.dirname(os.path.abspath(__file__))
DEP = os.path.join(D, "deploy")

shutil.rmtree(DEP, ignore_errors=True)
os.makedirs(os.path.join(DEP, "assets"), exist_ok=True)

# các trang (bỏ index-v1.html = bản backup)
for f in sorted(os.listdir(D)):
    if f.endswith(".html") and f != "index-v1.html":
        shutil.copy(os.path.join(D, f), os.path.join(DEP, f))

# toàn bộ assets/ (css + img)
for base, _, files in os.walk(os.path.join(D, "assets")):
    rel = os.path.relpath(base, D)
    os.makedirs(os.path.join(DEP, rel), exist_ok=True)
    for f in files:
        shutil.copy(os.path.join(base, f), os.path.join(DEP, rel, f))

for f in ["favicon-32.png", "favicon-128.png", "logo-tonyvu.svg",
          "logo-tonyvu.png", "tony-vu-website.html"]:
    src = os.path.join(D, f)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(DEP, f))

# sitemap.xml: bản trong deliverables có placeholder domain
sm = os.path.join(D, "deliverables", "sitemap.xml")
if os.path.exists(sm):
    shutil.copy(sm, os.path.join(DEP, "sitemap.xml"))

open(os.path.join(DEP, ".nojekyll"), "w").write("")
open(os.path.join(DEP, "README.md"), "w", encoding="utf-8").write(
    "# Website Vũ Văn Định (Tony Vũ)\n\n"
    "Site tĩnh 15 trang, sinh từ `build.py`. Deploy: `netlify deploy --prod --no-build --dir=deploy` "
    "hoặc bật GitHub Pages (branch main / root).\n")

n = len([f for f in os.listdir(DEP) if os.path.isfile(os.path.join(DEP, f))])
print("deploy/ : %d file ở gốc + assets/styles.css" % n)