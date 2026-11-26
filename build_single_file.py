#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gộp 15 trang thành MỘT file HTML tự tương tác (hash router, không cần server).
Kết quả: tony-vu-website.html  — mở là dùng được, bấm menu chuyển trang như site thật.
"""
import os, re, json

import os
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "tony-vu-website.html")
PAGES = [
    ("index.html", "Trang chủ"), ("about.html", "Giới thiệu"), ("work.html", "Kinh nghiệm"),
    ("edu.html", "Học vấn & chứng chỉ"), ("competency.html", "Chuyên môn"),
    ("schools.html", "Nơi giảng dạy"), ("courses.html", "Khoá học"),
    ("blueprint.html", "Lộ trình ACCA"), ("philosophy.html", "Cách dạy & cách học"),
    ("library.html", "Nguồn học"), ("students.html", "Học viên nói gì"),
    ("writing.html", "Bài viết"), ("for-students.html", "Cho người học"),
    ("for-organisations.html", "Cho doanh nghiệp"), ("contact.html", "Liên hệ"),
]
slug_of = {f: f[:-5] for f, _ in PAGES}
TITLE_OF = {f: t for f, t in PAGES}

css = open(os.path.join(D, "assets", "styles.css"), encoding="utf-8").read()
fonts_css = open(os.path.join(D, "assets", "fonts-inline.css"), encoding="utf-8").read()

import base64 as _b64
def _inline_images(html):
    """Nhúng ảnh cục bộ thành data URI để bản một-file không phụ thuộc thư mục assets/."""
    import re as _re, os as _os
    def sub(m):
        rel = m.group(1)
        p = _os.path.join(D, rel)
        if not _os.path.exists(p):
            return m.group(0)
        mime = "image/png" if p.lower().endswith(".png") else "image/jpeg"
        return 'src="data:%s;base64,%s"' % (mime, _b64.b64encode(open(p, "rb").read()).decode())
    return _re.sub(r'src="(assets/img/[^"]+)"', sub, html)


def body_of(path, strip_hero=False):
    src = open(path, encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", src, re.S)
    m = re.search(r"<body[^>]*>(.*)</body>", src, re.S)
    body = m.group(1)
    body = re.sub(r"<header>.*?</header>", "", body, flags=re.S)
    body = re.sub(r"<footer>.*?</footer>", "", body, flags=re.S)
    # bỏ <main> lồng trong <section> (sai chuẩn, gây nhịp lạ)
    body = re.sub(r"</?main[^>]*>", "", body)
    # bỏ khối hero lặp lại nội dung splash — CHỈ ở trang chủ
    if strip_hero:
        body = re.sub(r'<div class="container hero">.*?</div>\s*(?=<section)', "", body, flags=re.S)
    # đổi link trang .html -> hash route
    body = re.sub(r'href="([a-z0-9\-]+)\.html"', lambda x: 'href="#/%s"' % x.group(1), body)
    body = body.replace('href="index.html"', 'href="#/"')
    return title.group(1) if title else "", _inline_images(body.strip())



pages_html, titles = [], {}
for f, label in PAGES:
    t, b = body_of(os.path.join(D, f))
    slug = slug_of[f]
    titles[slug] = t
    pages_html.append('<section class="page" id="page-%s" data-slug="%s">\n%s\n</section>' % (slug, slug, b))

NAV_FILES = ["index.html", "about.html", "work.html", "competency.html", "courses.html",
             "blueprint.html", "students.html", "writing.html", "contact.html"]
NAV_PAGES = [x for x in PAGES if x[0] in NAV_FILES]  # đúng bằng menu của bản nhiều trang
NAV_LABEL = {"students.html": "Học viên"}          # nhãn ngắn đúng như bản nhiều trang
nav = "\n      ".join(
    '<a href="#/%s" data-nav="%s">%s</a>' % ((slug_of[f] if slug_of[f] != "index" else ""), slug_of[f], NAV_LABEL.get(f, label))
    for f, label in NAV_PAGES)
ALL_LINKS = "\n".join('<a href="#/%s">%s</a>' % (slug_of[f] if slug_of[f] != "index" else "", TITLE_OF[f])
                      for f, _ in PAGES)
FOOT_MAP = "\n".join('<a href="#/%s">%s</a>' % (slug_of[f] if slug_of[f] != "index" else "", TITLE_OF[f])
                     for f, _ in PAGES)

HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vũ Văn Định (Tony Vũ) — website</title>
<meta name="description" content="Website Vũ Văn Định (Tony Vũ) — giảng viên ACCA, CPA Australia, VACPA. 15 trang: giới thiệu, kinh nghiệm, chuyên môn, khoá học, lộ trình ACCA, học viên, liên hệ.">
<style>
/* ==== FONT NHÚNG SẴN (base64) — không phụ thuộc Google Fonts, chạy offline ==== */
%(fonts)s
/* ==== CSS chính ==== */
%(css)s
/* ---- thêm cho bản một-file ---- */
/* .page là khung chứa cả trang -> không được ăn padding/border của 'section' */
.page{display:none;padding:0 !important;border-top:0 !important}
.page.active{display:block;animation:fade .25s ease}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
/* không có JavaScript (Drive preview, khung xem file, chế độ chặn JS): hiển thị TẤT CẢ trang, không mất nội dung */
body:not(.js-ready) .page{display:block}
body:not(.js-ready) .page::before{content:'';display:block;border-top:1px solid var(--hairline);margin:26px 0}
</style>
</head>
<body>
<header>
  <div class="container bar">
    <a class="brand" href="#/">Vũ Văn Định</a>
    <nav class="main">
      %(nav)s
    </nav>
  </div>
</header>

%(pages)s

<footer>
  <div class="container">
    <div class="top">
      <span>© 2026 Vũ Văn Định (Tony Vũ)</span>
      <span>ACCA · CPA Australia · VACPA — Giảng viên ACCA, CMA, IFRS</span>
    </div>
    <div class="map">
      %(footmap)s
    </div>
  </div>
</footer>

<script>
document.body.classList.add('js-ready');
const TITLES = %(titles)s;
const pages = [...document.querySelectorAll('.page')];
const links = [...document.querySelectorAll('[data-nav], footer .map a')];
function slug(){ return decodeURIComponent(location.hash.replace(/^#\\/?/, '')).replace(/\\.html$/, ''); }
function show(s){
  if(!pages.some(p => p.dataset.slug === s)) s = 'index';
  pages.forEach(p => p.classList.toggle('active', p.dataset.slug === s));
  links.forEach(a => {
    const t = (a.getAttribute('href')||'').replace(/^#\\/?/, '') || 'index';
    if (t === s) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
  });
  document.body.dataset.page = s;
  document.title = TITLES[s] || document.title;
  window.scrollTo({top:0, behavior:'instant' in window ? 'instant' : 'auto'});
}
function route(){ show(slug() || 'index'); }
addEventListener('hashchange', route);
route();
// đổi link trang trong nội dung bài (phòng khi còn sót .html)
document.querySelectorAll('a[href$=".html"]').forEach(a => {
  a.setAttribute('href', '#/' + a.getAttribute('href').replace('.html',''));
});
</script>
</body>
</html>
""" % {"fonts": fonts_css, "css": css, "nav": nav, "pages": "\n".join(pages_html),
       "footmap": FOOT_MAP, "titles": json.dumps(titles, ensure_ascii=False)}

open(OUT, "w", encoding="utf-8").write(HTML)
print("đã tạo", OUT, round(os.path.getsize(OUT) / 1024), "KB |",
      len(pages_html), "trang |", len(FOOT_MAP.split("\n")), "link trong bản đồ")
