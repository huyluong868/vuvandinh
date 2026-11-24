#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm tra một site tĩnh trước khi giao cho người dùng.

Dùng:
  python3 verify_site.py /đường/dẫn/site [/đường/dẫn/bản-một-file.html]

Kiểm 4 thứ (mỗi thứ đều đã từng là lỗi thật trong dự án gốc):
  1. link nội bộ: mọi href/src trỏ tới file có thật trong thư mục.
  2. mỗi trang đúng MỘT <h1>.
  3. nhãn menu của bản nhiều trang == bản một-file (so bằng code, không nhìn mắt).
  4. smoke test server tĩnh: mở http.server rồi gọi vài URL, đòi HTTP 200 (giống GitHub Pages).
"""
import os
import re
import subprocess
import sys
import time
import urllib.request
from html.parser import HTMLParser


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("a", "link") and d.get("href"):
            self.items.append(d["href"])
        if tag in ("img", "script") and d.get("src"):
            self.items.append(d["src"])


def link_check(root):
    have = set()
    for base, _, files in os.walk(root):
        for f in files:
            have.add(os.path.relpath(os.path.join(base, f), root))
    bad = []
    for f in sorted(os.listdir(root)):
        if not f.endswith(".html"):
            continue
        p = Links()
        p.feed(open(os.path.join(root, f), encoding="utf-8").read())
        for item in p.items:
            if item.startswith(("http", "//", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            item = item.split("#")[0].split("?")[0]   # bỏ fragment/query
            item = item.lstrip("/") or "index.html"    # đường dẫn tuyệt đối "/assets/x.js" -> gốc site
            if item and item not in have:
                bad.append((f, item))
    return bad


def h1_check(root):
    """Mỗi trang đúng 1 <h1>. Với file gộp nhiều trang (bundle có <section class="page">),
    kiểm theo từng khối thay vì theo cả file."""
    bad = []
    for f in sorted(os.listdir(root)):
        if not f.endswith(".html"):
            continue
        html = open(os.path.join(root, f), encoding="utf-8").read()
        if 'class="page"' in html:
            blocks = re.findall(
                r'<section class="page"[^>]*>(.*?)</section>\s*(?=<section class="page"|<footer>)',
                html, re.S)
            wrong = [(i + 1, b.count("<h1")) for i, b in enumerate(blocks) if b.count("<h1") != 1]
            if wrong:
                bad.append((f + " (theo khối)", wrong))
            print("  %s: %d trang gộp, %d khối sai" % (f, len(blocks), len(wrong)))
            continue
        n = html.count("<h1")
        if n != 1:
            bad.append((f, n))
    return bad


def nav_labels(html):
    m = re.findall(r'<nav class="main">(.*?)</nav>', html, re.S)
    if m:
        return re.findall(r">([^<>]+)</a>", m[0])
    return [x[1] for x in re.findall(r'data-nav="([a-z\-]+)">([^<]+)<', html)]


def smoke(root, paths=("/", "/index.html", "/assets/styles.css", "/sitemap.xml")):
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8099", "--directory", root],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2.5)
    out = []
    try:
        for p in paths:
            try:
                r = urllib.request.urlopen("http://127.0.0.1:8099" + p, timeout=8)
                out.append((p, r.status))
            except Exception as e:  # noqa: BLE001
                out.append((p, "LỖI %s" % e))
    finally:
        srv.terminate()
    return out


def main(root, onefile=None):
    """Trả về mã thoát: 0 = sạch, 1 = có lỗi (CI dùng để FAIL job)."""
    failed = False
    bad = link_check(root)
    print("link nội bộ hỏng:", bad if bad else "KHÔNG CÓ ✓")
    failed |= bool(bad)
    bad_h1 = h1_check(root)
    print("trang sai số <h1>:", bad_h1 or "KHÔNG CÓ ✓")
    failed |= bool(bad_h1)
    if onefile and os.path.exists(onefile):
        a = nav_labels(open(os.path.join(root, "index.html"), encoding="utf-8").read())
        b = nav_labels(open(onefile, encoding="utf-8").read())
        print("menu nhiều trang :", a)
        print("menu một-file    :", b)
        print("KHỚP:", a == b)
        failed |= a != b
    for p, status in smoke(root):
        print("  %-22s -> %s" % (p, status))
        failed |= status != 200
    print("KẾT QUẢ:", "FAIL ✗" if failed else "OK ✓")
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
