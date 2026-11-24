#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chèn snippet đo lường vào MỌI file HTML trong deploy/ ngay trước </body>.

Dùng:  python scripts/measure.py [thư-mục-deploy]      (mặc định: <repo>/deploy)

- Idempotent: trang đã có snippet thì bỏ qua (chạy lại không nhân đôi).
- Đảm bảo deploy/assets/analytics.js tồn tại (copy từ assets/analytics.js nếu thiếu/khác).
- Thoát mã 1 nếu thiếu thư mục deploy hoặc không có assets/analytics.js nguồn.
"""
import os
import re
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(REPO, "deploy")
# Đường dẫn TƯƠNG ĐỐI: GitHub Pages phục vụ site ở /<repo>/ nên "/assets/..." sẽ 404.
SNIPPET = '<script defer data-site="vuvandinh" src="assets/analytics.js"></script>'
MARK = 'data-site="vuvandinh"'
BODY_END = re.compile(r"</body\s*>", re.I)


def main():
    if not os.path.isdir(ROOT):
        sys.exit("LỖI: không thấy thư mục %s (chạy make_deploy.py trước)" % ROOT)
    src_js = os.path.join(REPO, "assets", "analytics.js")
    if not os.path.isfile(src_js):
        sys.exit("LỖI: thiếu %s" % src_js)
    dst_js = os.path.join(ROOT, "assets", "analytics.js")
    os.makedirs(os.path.dirname(dst_js), exist_ok=True)
    shutil.copyfile(src_js, dst_js)

    added = skipped = 0
    missing = []
    for base, _, files in os.walk(ROOT):
        for f in sorted(files):
            if not f.lower().endswith(".html"):
                continue
            p = os.path.join(base, f)
            with open(p, encoding="utf-8", newline="") as fh:
                html = fh.read()
            if MARK in html:
                skipped += 1
                continue
            ms = list(BODY_END.finditer(html))
            if not ms:
                missing.append(os.path.relpath(p, ROOT))
                continue
            i = ms[-1].start()  # </body> cuối cùng (bản gộp có thể chứa chuỗi "</body>" trong JS)
            html = html[:i] + SNIPPET + "\n" + html[i:]
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(html)
            added += 1
    print("measure: chèn %d trang, đã có sẵn %d, thiếu </body> %d" % (added, skipped, len(missing)))
    for m in missing:
        print("  CẢNH BÁO: không có </body>:", m)


if __name__ == "__main__":
    main()
