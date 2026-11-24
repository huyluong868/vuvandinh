#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tạo bộ tư liệu để đưa lên Drive: logo, sitemap, contact sheet, zip."""
import os, glob, shutil, zipfile, unicodedata
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))  # thư mục repo (chạy được ở CI)
OUT = os.path.join(D, "deliverables")
os.makedirs(OUT, exist_ok=True)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
IVORY = (250, 247, 240); INK = (26, 24, 20); BRONZE = (138, 100, 32)
BRONZE_L = (217, 184, 119); HAIR = (220, 213, 198)

nfc = lambda s: unicodedata.normalize("NFC", s)

# ---------------------------------------------------------------- 1) LOGO
def make_logo():
    # SVG: monogram VĐ, khung mảnh, không phụ thuộc font ngoài (serif hệ thống)
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <rect width="240" height="240" fill="#faf7f0"/>
  <rect x="12" y="12" width="216" height="216" fill="none" stroke="#dcd5c6" stroke-width="2"/>
  <rect x="18" y="18" width="204" height="204" fill="none" stroke="#8a6420" stroke-width="1" opacity=".55"/>
  <text x="120" y="146" text-anchor="middle" font-family="Playfair Display, Georgia, 'DejaVu Serif', serif"
        font-size="104" font-weight="600" fill="#1a1814">VĐ</text>
  <text x="120" y="186" text-anchor="middle" font-family="Be Vietnam Pro, system-ui, sans-serif"
        font-size="15" letter-spacing="4" fill="#8a6420">ACCA · CPA · VACPA</text>
</svg>'''
    open(os.path.join(OUT, "logo-tonyvu.svg"), "w", encoding="utf-8").write(svg)

    for size, name in [(512, "logo-tonyvu.png"), (128, "favicon-128.png"), (32, "favicon-32.png")]:
        im = Image.new("RGB", (size, size), IVORY); dr = ImageDraw.Draw(im)
        p = size * 0.05
        dr.rectangle([p, p, size - p, size - p], outline=HAIR, width=max(1, size // 128))
        p2 = p * 1.5
        dr.rectangle([p2, p2, size - p2, size - p2], outline=BRONZE, width=max(1, size // 256))
        f1 = ImageFont.truetype(SERIF_B, int(size * 0.44))
        t = "VĐ"
        w = dr.textlength(t, font=f1)
        dr.text(((size - w) / 2, size * 0.30), t, font=f1, fill=INK)
        if size >= 128:
            f2 = ImageFont.truetype(SANS, int(size * 0.062))
            t2 = "ACCA · CPA · VACPA"; w2 = dr.textlength(t2, font=f2)
            dr.text(((size - w2) / 2, size * 0.76), t2, font=f2, fill=BRONZE)
        im.save(os.path.join(OUT, name), optimize=True)
    # make_deploy.py lấy favicon/logo ở GỐC repo (các file này nằm trong .gitignore) -> chép ra gốc
    for name in ["logo-tonyvu.svg", "logo-tonyvu.png", "favicon-128.png", "favicon-32.png"]:
        shutil.copyfile(os.path.join(OUT, name), os.path.join(D, name))
    print("logo: ok")

# ---------------------------------------------------------------- 2) SITEMAP
PAGES = [
    ("index.html", "Trang chủ", "Hub: 3 vai trò · mục lục · môn đang dạy · học viên · 2 cổng"),
    ("about.html", "Giới thiệu", "Hành trình, cách làm việc, nguồn & điểm cần xác nhận"),
    ("work.html", "Kinh nghiệm", "6 vị trí tài chính"),
    ("edu.html", "Học vấn & chứng chỉ", "KTQD · ACCA · CPA Australia · VACPA"),
    ("competency.html", "Chuyên môn", "7 mảng + phân biệt KTTC/KTQT, kiểm toán/soát xét"),
    ("schools.html", "Nơi giảng dạy", "FTMS Global Hà Nội · ATC Academy"),
    ("courses.html", "Khoá học", "7 lớp + lịch & hình thức + chọn lớp theo mục tiêu"),
    ("blueprint.html", "Lộ trình ACCA", "3 cấp + 4 quyết định"),
    ("philosophy.html", "Cách dạy & cách học", "4 nguyên tắc + chia sẻ ngoài lớp (HaUI)"),
    ("library.html", "Nguồn học", "5 nguồn chính thức + thứ tự đọc"),
    ("students.html", "Học viên nói gì", "2 trích dẫn công khai + điều cố ý không đưa"),
    ("writing.html", "Bài viết", "Bản tin (chờ link Substack) + 5 chủ đề"),
    ("for-students.html", "Cho người học", "Cổng: 3 bước bắt đầu"),
    ("for-organisations.html", "Cho doanh nghiệp", "Cổng: 4 nhóm chủ đề + cách làm việc"),
    ("contact.html", "Liên hệ", "Email · khu vực · gửi gì để được trả lời nhanh"),
]
DOMAIN = os.environ.get("SITE_DOMAIN", "https://<domain-cua-thay>/")   # CI đặt SITE_DOMAIN; mặc định là placeholder

xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for slug, _, _ in PAGES:
    xml.append("  <url><loc>%s</loc></url>" % (DOMAIN + slug))
xml.append("</urlset>")
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")

md = ["# Sitemap — site Vũ Văn Định (Tony Vũ)", "",
      "15 trang, tĩnh, không cần server. Đối chiếu với cấu trúc của anhdac.com (33 URL trong sitemap.xml của trang gốc).", "",
      "| # | File | Trang | Nội dung |", "|---|---|---|---|"]
for i, (slug, title, desc) in enumerate(PAGES, 1):
    md.append("| %d | `%s` | %s | %s |" % (i, slug, title, desc))
md += ["", "## Đối chiếu với anhdac.com", "",
       "| anhdac.com | Site này | Ghi chú |", "|---|---|---|",
       "| `/` (splash 2 cổng) | `index.html` + 2 cổng trong trang | Giữ ý tưởng 2 cổng: người học / doanh nghiệp |",
       "| `/about` `/work` `/edu` `/competency` | `about` `work` `edu` `competency` | Tách thành 4 trang riêng |",
       "| `/schools` `/awards` | `schools` `edu` | Gộp học vấn + chứng chỉ vào `edu` |",
       "| `/blueprint` `/philosophy` `/library` | `blueprint` `philosophy` `library` | Giữ nguyên vai trò |",
       "| `/writing` | `writing.html` | **Chờ link Substack** để nạp bài |",
       "| `/masters` `/brands` `/organizations` `/cares` `/life` `/tours` | — | Cố ý không dựng: chưa có nguồn, tránh bịa |",
       "| `/family` `/hobbies` `/music` `/paintings` | — | Đời tư — không dựng cho hồ sơ nghề nghiệp |",
       "", "## Ghi chú kỹ thuật", "",
       "- Mọi trang dùng chung `assets/styles.css` (một file), sinh từ `build.py`.",
       "- Đổi email/khối lượng lớn: sửa biến trong `build.py` rồi chạy lại `python3 build.py`.",
       "- Ảnh chụp từng trang nằm trong `shots/` (đã render thật bằng trình duyệt).",
       "- Favicon + logo: `logo-tonyvu.svg`, `logo-tonyvu.png`, `favicon-128.png`.",
       "- `index-v1.html` là bản 1 trang cũ, giữ để đối chiếu."]
open(os.path.join(OUT, "sitemap.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("sitemap: ok")

# ---------------------------------------------------------------- 3) CONTACT SHEET
def contact_sheet():
    shots = sorted(glob.glob(os.path.join(D, "shots", "*.png")))
    order = [p[0].replace(".html", "") for p in PAGES if os.path.exists(os.path.join(D, "shots", p[0].replace(".html", "") + ".png"))]
    byname = {os.path.basename(s)[:-4]: s for s in shots}
    seq = [byname[n] for n in order if n in byname]
    print("ảnh có:", len(seq), "trang")
    if not seq:  # CI không có shots/ (ảnh chụp màn hình) -> bỏ qua contact sheet
        print("contact sheet: bỏ qua (không có shots/)")
        return
    TW, PAD, COLS = 400, 26, 4
    labels = {p[0].replace(".html", ""): p[1] for p in PAGES}
    thumbs = []
    for s in seq:
        im = Image.open(s).convert("RGB")
        w, h = im.size
        th = im.resize((TW, int(h * TW / w)), Image.LANCZOS)
        th = th.crop((0, 0, TW, min(th.size[1], int(TW * 1.25))))
        thumbs.append((os.path.basename(s)[:-4], th))
    rows = (len(thumbs) + COLS - 1) // COLS
    cell_h = max(t.size[1] for _, t in thumbs) + 40
    W = COLS * TW + (COLS + 1) * PAD
    H = 70 + rows * (cell_h + PAD) + PAD
    sheet = Image.new("RGB", (W, H), (16, 18, 22)); dr = ImageDraw.Draw(sheet)
    f_title = ImageFont.truetype(SERIF_B, 30); f_lab = ImageFont.truetype(SANS, 17)
    dr.text((PAD, 20), nfc("Website Vũ Văn Định (Tony Vũ) — 15 trang, render thật"), font=f_title, fill=(245, 242, 235))
    for i, (name, t) in enumerate(thumbs):
        r, c = divmod(i, COLS)
        x = PAD + c * (TW + PAD); y = 70 + r * (cell_h + PAD)
        sheet.paste(t, (x, y))
        dr.rectangle([x, y, x + TW, y + t.size[1]], outline=(70, 74, 84), width=1)
        dr.text((x + 4, y + t.size[1] + 8), "%d. %s" % (i + 1, nfc(labels.get(name, name))), font=f_lab, fill=(196, 200, 210))
    sheet.save(os.path.join(OUT, "xem-truoc-tat-ca-trang.png"), optimize=True)
    print("contact sheet:", sheet.size)

# ---------------------------------------------------------------- 4) ZIP
def make_zip():
    zp = os.path.join(OUT, "site-tonyvu.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for pat in ["*.html", "*.md", "*.py", "assets/*", "shots/*"]:
            for f in glob.glob(os.path.join(D, pat)):
                if os.path.isfile(f) and "deliverables" not in f:
                    z.write(f, os.path.relpath(f, D))
    print("zip:", round(os.path.getsize(zp) / 1e6, 1), "MB")

make_logo(); contact_sheet(); make_zip()
