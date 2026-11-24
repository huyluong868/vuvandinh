#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tải woff2 (subset latin/latin-ext/vietnamese) và nhúng base64 vào một CSS duy nhất
để trang không còn phụ thuộc Google Fonts -> nhìn giống nhau ở mọi máy, kể cả offline."""
import base64, os, re, subprocess, sys, tempfile

D = os.path.dirname(os.path.abspath(__file__))  # thư mục repo (chạy được ở CI)
TMP = os.path.join(tempfile.gettempdir(), "vuvandinh-fonts")
SRC = os.path.join(TMP, "gf.css")
OUT = os.path.join(D, "assets", "fonts-inline.css")
CACHE = os.path.join(TMP, "bin")
GF_URL = ("https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400"
          "&family=Be+Vietnam+Pro:wght@300;400;500&display=swap")
os.makedirs(CACHE, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
KEEP = {"latin", "vietnamese"}

if not os.path.exists(SRC):  # CI sạch: tải CSS Google Fonts (lỗi mạng -> exit != 0, workflow bỏ qua)
    subprocess.run(["curl", "-sfL", "--max-time", "30", "-A", UA, GF_URL, "-o", SRC], check=True)
css = open(SRC, encoding="utf-8").read()
# tách theo comment subset: "/* vietnamese */\n@font-face{...}"
blocks = re.findall(r"/\*\s*([a-z0-9\-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", css)
print("tổng block:", len(blocks))

out = ["/* Font nhúng sẵn (base64) — Playfair Display + Be Vietnam Pro, subset latin/latin-ext/vietnamese */"]
total = 0
for subset, block in blocks:
    if subset not in KEEP:
        continue
    m = re.search(r'url\((https://fonts\.gstatic\.com[^)]+\.woff2)\)', block)
    fam = re.search(r"font-family:\s*'([^']+)'", block)
    wt = re.search(r"font-weight:\s*(\d+)", block)
    sty = re.search(r"font-style:\s*(\w+)", block)
    if wt and wt.group(1) == "700" and fam and "Playfair" in fam.group(1):
        continue  # không dùng weight 700 -> bỏ cho nhẹ
    if not (m and fam):
        continue
    url = m.group(1)
    name = fam.group(1).replace(" ", "") + "-" + (wt.group(1) if wt else "400") + \
           ("-italic" if sty and sty.group(1) == "italic" else "") + "-" + subset + ".woff2"
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        subprocess.run(["curl", "-sfL", "--max-time", "30", "-A", UA, url, "-o", path], check=True)
    data = open(path, "rb").read()
    total += len(data)
    b64 = base64.b64encode(data).decode()
    ur = re.search(r"unicode-range:\s*([^;]+);", block)
    new = ("@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
           "src:url(data:font/woff2;base64,%s) format('woff2')%s;%s}") % (
        fam.group(1), sty.group(1) if sty else "normal", wt.group(1) if wt else "400", b64,
        "" if ur else "", ("unicode-range:%s;" % ur.group(1)) if ur else "")
    out.append("/* %s · %s %s %s */" % (subset, fam.group(1), wt.group(1) if wt else "400",
                                        sty.group(1) if sty else "normal"))
    out.append(new)
    print("  +", name, round(len(data) / 1024), "KB")

open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\nđã ghi", OUT, "|", round(os.path.getsize(OUT) / 1024), "KB | woff2 gốc:", round(total / 1024), "KB")
