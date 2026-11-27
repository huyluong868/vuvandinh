#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sinh toàn bộ site nhiều trang cho Vũ Văn Định (Tony Vũ),
theo cấu trúc thông tin của anhdac.com (đọc từ sitemap thật của trang gốc).
CSS viết lại từ đầu, cùng hệ màu/typography với bản clone trước.
Chạy: python3 build.py
"""
import os
import html

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "Vũ Văn Định"
SITE_SUB = "Giảng viên ACCA · CFO · Cố vấn tài chính"
EMAIL = "vuvandinh.vn@gmail.com"
YEAR = "2026"

# ----------------------------------------------------------------------------- CSS
CSS = r"""
:root{
  --ivory:#faf7f0; --ivory-deep:#f2ede2; --ink:#1a1814; --ink-soft:#4a453c;
  --ink-muted:#5c5649; --hairline:#dcd5c6; --bronze:#8a6420; --bronze-deep:#5e4314;
  --bronze-light:#d9b877; --serif:"Playfair Display",Georgia,serif;
  --sans:"Be Vietnam Pro",system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{background:var(--ivory);color:var(--ink);font-family:var(--sans);font-weight:300;
  font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--serif);font-weight:500;line-height:1.2}
a{color:var(--bronze);text-decoration:none}
a:hover{color:var(--bronze-deep)}
img{max-width:100%}
.container{width:100%;max-width:1200px;margin-inline:auto;padding-inline:24px}
.col{max-width:760px;margin-inline:auto}
.eyebrow{text-transform:uppercase;letter-spacing:.2em;color:var(--bronze);font-size:12px;font-weight:400}
.rule{border-top:1px solid var(--hairline)}
.muted{color:var(--ink-muted)}
.center{text-align:center}

/* header */
header{position:sticky;top:0;z-index:40;background:rgba(250,247,240,.96);
  backdrop-filter:saturate(140%) blur(6px);border-bottom:1px solid var(--hairline)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:24px;height:72px}
.brand{font-family:var(--serif);font-size:22px;color:var(--ink)}
nav.main{display:flex;gap:26px;font-size:14px}
nav.main a{color:var(--ink-soft);white-space:nowrap}
nav.main a:hover,nav.main a[aria-current="page"]{color:var(--bronze)}
@media (max-width:940px){nav.main{display:none}}

/* hero */
.hero{padding:84px 0 64px;text-align:center}
.hero h1{font-size:clamp(36px,5.6vw,54px);font-weight:600;letter-spacing:-.02em}
.hero blockquote{font-family:var(--serif);font-style:italic;font-weight:400;
  font-size:clamp(19px,2.4vw,24px);line-height:1.55;color:var(--ink-soft);
  margin:26px auto 0;max-width:720px}
.hero p.lede{color:var(--ink-muted);margin:24px auto 0;max-width:660px}
.meta{margin-top:22px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--bronze)}
.creds{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:30px}
.chip{display:inline-block;border:1px solid var(--hairline);background:var(--ivory-deep);
  color:var(--ink-soft);font-size:13px;font-weight:400;padding:6px 12px;border-radius:999px}
.chip.solid{border-color:var(--bronze-light);background:transparent;color:var(--bronze-deep)}

/* section */
section{padding:68px 0;border-top:1px solid var(--hairline)}
.sec-head{display:flex;gap:28px;align-items:baseline;margin-bottom:34px}
.sec-num{font-size:13px;color:var(--bronze);letter-spacing:.16em;padding-top:6px}
.sec-head h2{font-size:clamp(25px,3.2vw,32px)}
.sec-head p{color:var(--ink-muted);font-size:15px;margin-top:8px}
.prose p{margin-bottom:16px}
.prose h3{font-size:20px;margin:26px 0 8px}
.prose ul{margin:0 0 16px 20px}
.prose li{margin-bottom:7px}
.prose strong{font-weight:500}

/* timeline */
.tl{display:grid;grid-template-columns:150px 1fr;gap:0 32px}
.tl > .row{display:contents}
.tl .when{color:var(--bronze);font-size:13px;letter-spacing:.06em;padding:22px 0;
  border-top:1px solid var(--hairline)}
.tl .what{padding:22px 0;border-top:1px solid var(--hairline)}
.tl .what h3{font-size:19px;margin-bottom:6px}
.tl .what p{color:var(--ink-muted);font-size:15px}
.tl > .row:first-child .when,.tl > .row:first-child .what{border-top:none;padding-top:0}
@media (max-width:640px){.tl{grid-template-columns:1fr;gap:0}
  .tl .when{border-top:1px solid var(--hairline);padding:18px 0 0}
  .tl .what{border-top:none;padding:8px 0 18px}}

/* cards */
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.grid.three{grid-template-columns:repeat(3,1fr)}
@media (max-width:900px){.grid.three{grid-template-columns:1fr}}
@media (max-width:760px){.grid{grid-template-columns:1fr}}
.card{background:var(--ivory-deep);border:1px solid var(--hairline);padding:26px 24px;border-radius:3px}
.card h3{font-size:19px;margin-bottom:4px}
.card .role{color:var(--bronze-deep);font-size:13px;letter-spacing:.04em;margin-bottom:12px}
.card p{color:var(--ink-muted);font-size:15px}
.card .more{display:inline-block;margin-top:14px;font-size:14px}
.card .idx{font-size:12px;letter-spacing:.18em;color:var(--bronze);display:block;margin-bottom:10px}
.note{color:var(--ink-muted);font-size:13px;margin-top:18px;font-style:italic}

/* gates (như trang chủ anhdac) */
.gates{display:grid;grid-template-columns:1fr 1fr;gap:0;border:1px solid var(--hairline)}
@media (max-width:760px){.gates{grid-template-columns:1fr}}
.gate{padding:56px 46px;min-height:260px;display:flex;flex-direction:column;justify-content:space-between}
.gate.dark{background:#171512;color:#f6f1e6}
.gate.light{background:var(--ivory-deep);color:var(--ink)}
.gate h3{font-size:clamp(24px,3vw,32px);line-height:1.25;max-width:11ch}
.gate p{font-size:14px;margin-top:14px;opacity:.78;max-width:34ch}
.gate .go{margin-top:28px;font-size:22px;color:var(--bronze-light)}
.gate.dark a{color:#f6f1e6}
.gate.light .go{color:var(--bronze)}

/* quote */
.quote{border-left:2px solid var(--bronze-light);padding:4px 0 4px 24px;margin-bottom:26px}
.quote p{font-family:var(--serif);font-style:italic;font-size:19px;color:var(--ink-soft);line-height:1.6}
.quote cite{display:block;margin-top:10px;font-style:normal;font-size:13px;color:var(--bronze)}

/* defs */
.defs{display:grid;grid-template-columns:1fr;gap:0}
.def{padding:20px 0;border-top:1px solid var(--hairline)}
.def h3{font-size:18px;margin-bottom:6px}
.def p{color:var(--ink-muted);font-size:15px}
.def:first-child{border-top:none}

/* form liên hệ (Supabase) */
.leadform{max-width:720px;margin-top:8px}
.leadform .frow{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px}
.leadform .frow.one{grid-template-columns:1fr}
@media (max-width:640px){.leadform .frow{grid-template-columns:1fr}}
.leadform label{display:block;font-size:13px;letter-spacing:.04em;color:var(--ink-muted);text-transform:uppercase}
.leadform input,.leadform select,.leadform textarea{width:100%;margin-top:6px;padding:11px 12px;border:1px solid var(--hairline);
  background:#fff;font-family:inherit;font-size:15px;color:var(--ink);border-radius:2px;text-transform:none;letter-spacing:0}
.leadform input:focus,.leadform select:focus,.leadform textarea:focus{outline:none;border-color:var(--ink)}
.leadform .req{color:#a8663a}
.btn-send{margin-top:6px;padding:12px 30px;background:var(--ink);color:#fff;border:0;border-radius:999px;
  font-family:inherit;font-size:14px;letter-spacing:.06em;text-transform:uppercase;cursor:pointer}
.btn-send:hover{opacity:.88}
.leadmsg{margin-top:12px;font-size:14px;min-height:20px;color:var(--ink-muted)}
.leadmsg.ok{color:#1d6b3f}
.leadmsg.err{color:#a03030}

/* ảnh bìa bài viết + logo bản tin */
.poststrip{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 28px}
@media (max-width:700px){.poststrip{grid-template-columns:1fr}}
.poststrip a{color:var(--ink)}
.poststrip img{width:100%;height:150px;object-fit:cover;border:1px solid var(--hairline);border-radius:3px;display:block}
.poststrip figcaption{font-size:12.5px;color:var(--ink-muted);margin-top:7px;line-height:1.45}
.newslogo{width:52px;height:52px;border-radius:999px;border:1px solid var(--hairline);vertical-align:middle;margin-right:12px}
.cover{width:100%;height:150px;object-fit:cover;border:1px solid var(--hairline);border-radius:3px;margin-bottom:14px;display:block}

/* contact */
.contact{display:flex;flex-wrap:wrap;gap:14px 40px;align-items:center}
.contact .k{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--bronze)}
.contact .v{font-size:16px;color:var(--ink-soft)}

/* footer */
footer{padding:48px 0 64px;border-top:1px solid var(--hairline)}
footer .top{display:flex;flex-wrap:wrap;gap:12px 28px;justify-content:space-between;font-size:13px;color:var(--ink-muted)}
footer .map{margin-top:26px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px 24px;font-size:13px}
@media (max-width:760px){footer .map{grid-template-columns:repeat(2,1fr)}}
footer .map a{color:var(--ink-soft)}
footer .map a:hover{color:var(--bronze)}
""".strip()

# ----------------------------------------------------------------------------- dữ liệu trang
# Mọi dữ kiện lấy từ hồ sơ đã kiểm chứng (README.md của site, FTMS Global, ATC Academy,
# slide giảng dạy công khai). Chỗ chưa có nguồn → ghi rõ "cần xác nhận", không bịa.

CHIPS = ["ACCA", "CPA Australia", "VACPA", "Ex-EY", "14 năm trong nghề", "Giảng viên từ 2016"]

NAV = [
    ("index.html", "Trang chủ"),
    ("about.html", "Giới thiệu"),
    ("work.html", "Kinh nghiệm"),
    ("competency.html", "Chuyên môn"),
    ("courses.html", "Khoá học"),
    ("blueprint.html", "Lộ trình ACCA"),
    ("students.html", "Học viên"),
    ("writing.html", "Bài viết"),
    ("contact.html", "Liên hệ"),
]

FOOTER_MAP = [
    ("index.html", "Trang chủ"), ("about.html", "Giới thiệu"), ("work.html", "Kinh nghiệm"),
    ("edu.html", "Học vấn & chứng chỉ"), ("competency.html", "Chuyên môn"),
    ("schools.html", "Nơi giảng dạy"), ("courses.html", "Khoá học"),
    ("blueprint.html", "Lộ trình ACCA"), ("philosophy.html", "Cách dạy & cách học"),
    ("library.html", "Nguồn học"), ("students.html", "Học viên nói gì"),
    ("writing.html", "Bài viết"),
    ("for-students.html", "Cho người học"), ("for-organisations.html", "Cho doanh nghiệp"),
    ("contact.html", "Liên hệ"),
]

W = {
    "vin": ("Vingroup &amp; Vinpearl", "Quản lý cấp cao",
            "Đảm nhận vai trò điều hành trong hệ sinh thái tập đoàn và chuỗi nghỉ dưỡng."),
    "vpi": ("Văn Phú Invest", "Phó ban Tài chính", "Mảng tài chính và quản trị vốn."),
    "vntrip": ("Vntrip", "Giám đốc Tài chính (CFO)", "Nền tảng du lịch trực tuyến."),
    "toco": ("Tocotoco Việt Nam", "Giám đốc Tài chính", "Chuỗi F&amp;B — quản trị tài chính và mở rộng chuỗi."),
    "flex": ("Flexfit", "Trưởng ban Tài chính", "Quản trị tài chính doanh nghiệp."),
    "adv": ("Cố vấn tài chính", "Startup Việt Nam", "Cố vấn tài chính cho các startup."),
}

COMPETENCY = [
    ("Performance Management (PM — F5)", "Môn ACCA Applied Skills về đo lường hiệu quả, chi phí, quyết định giá và đánh giá thành tích — đúng phần anh dạy trên lớp."),
    ("Audit and Assurance (AA — F8)", "Môn ACCA về quy trình kiểm toán, bằng chứng kiểm toán, rủi ro và báo cáo kiểm toán."),
    ("Kế toán Tài chính — Part 2", "Phần kế toán tài chính theo lộ trình ACCA mà anh đứng lớp."),
    ("Kế toán quản trị &amp; báo cáo quản trị", "Lập và phân tích báo cáo quản trị phục vụ điều hành — mảng anh dạy tại ATC Academy."),
    ("IFRS / lập báo cáo tài chính quốc tế", "Chuẩn mực báo cáo tài chính quốc tế và cách áp dụng vào doanh nghiệp Việt Nam."),
    ("CMA", "Chứng chỉ kế toán quản trị Hoa Kỳ (IMA) — anh giảng dạy song song với ACCA."),
    ("Quản trị tài chính &amp; hiệu quả kinh doanh", "Quản trị vốn, dòng tiền và đo lường hiệu quả — phần gắn với 12 năm làm CFO/trưởng ban tài chính."),
]

COURSES = [
    ("ACCA — Performance Management (PM / F5)", "Applied Skills", "Lớp luyện thi theo cấu trúc đề ACCA: lý thuyết → bài tập tình huống → đề thi thử."),
    ("ACCA — Audit and Assurance (AA / F8)", "Applied Skills", "Kiểm toán và dịch vụ đảm bảo; trọng tâm bằng chứng, rủi ro và báo cáo."),
    ("ACCA — Kế toán Tài chính Part 2", "Theo lộ trình", "Nền kế toán tài chính cho người mới bắt đầu hoặc chuyển ngành."),
    ("Kế toán Quản trị &amp; phân tích báo cáo quản trị", "Người đi làm", "Lập báo cáo quản trị, phân tích tài chính doanh nghiệp cho kế toán/quản lý."),
    ("IFRS — báo cáo tài chính quốc tế", "Người đi làm", "Áp dụng IFRS vào lập và soát xét báo cáo tài chính."),
    ("CMA — kế toán quản trị Hoa Kỳ", "Chứng chỉ quốc tế", "Ôn luyện theo khung IMA."),
    ("“Khắc hoạ chân dung CFO tương lai”", "Lớp chuyên đề", "Chuyên đề của ATC Academy dành cho người hướng tới vai trò CFO."),
]

BOOKS = [
    ("ACCA — Study Hub (chính thức)", "Syllabus, study guide, past exam papers và examiner’s report của từng môn PM, AA…", "https://www.accaglobal.com/gb/en/student/exam-support-resources.html"),
    ("IFRS Foundation", "Toàn văn chuẩn mực IFRS và tài liệu hướng dẫn áp dụng.", "https://www.ifrs.org/issued-standards/list-of-standards/"),
    ("IMA — CMA", "Khung nội dung và tài liệu ôn luyện CMA.", "https://www.imanet.org/cma-certification"),
    ("VACPA", "Hiệp hội Kiểm toán viên hành nghề Việt Nam — chuẩn mực và cập nhật nghề nghiệp.", "https://vacpa.org.vn/"),
    ("CPA Australia", "Hiệp hội Kế toán Công chứng Australia — chương trình và tài nguyên hội viên.", "https://www.cpaaustralia.com.au/"),
]


def chip_row(items, start=True):
    style = ' style="justify-content:flex-start"' if start else ""
    return '<div class="creds"%s>%s</div>' % (
        style, "".join('<span class="chip%s">%s</span>' % (" solid" if i < 3 else "", c)
                       for i, c in enumerate(items)))


def sec(num, title, sub, body, wrap_col=True):
    inner = '<div class="col">%s</div>' % body if wrap_col else body
    return """  <section id="%s">
    <div class="container">
      <div class="col">
        <div class="sec-head">
          <span class="sec-num">%s</span>
          <div><h2>%s</h2>%s</div>
        </div>
      </div>
%s
    </div>
  </section>""" % (slugify(title), num, title, ("<p>%s</p>" % sub) if sub else "", inner)


def slugify(s):
    import re, unicodedata
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def timeline(rows):
    out = ['<div class="tl">']
    for when, title, body in rows:
        out.append('  <div class="row"><div class="when">%s</div><div class="what"><h3>%s</h3><p>%s</p></div></div>'
                   % (when, title, body))
    out.append("</div>")
    return "\n".join(out)


def grid_cards(items, three=False, numbered=False):
    cls = "grid three" if three else "grid"
    out = ['<div class="%s">' % cls]
    for i, it in enumerate(items, 1):
        title, role, body, href = (list(it) + [None, None, None, None])[:4]
        out.append('<div class="card">')
        if numbered:
            out.append('<span class="idx">%02d</span>' % i)
        out.append("<h3>%s</h3>" % title)
        if role:
            out.append('<div class="role">%s</div>' % role)
        if body:
            out.append("<p>%s</p>" % body)
        if href:
            out.append('<a class="more" href="%s">Xem ↗</a>' % href)
        out.append("</div>")
    out.append("</div>")
    return "\n".join(out)


def defs(items):
    return '<div class="defs">%s</div>' % "".join(
        '<div class="def"><h3>%s</h3><p>%s</p></div>' % (t, b) for t, b in items)


def quotes(items):
    return "\n".join('<div class="quote"><p>“%s”</p><cite>%s</cite></div>' % (q, c) for q, c in items)


# ----------------------------------------------------------------------------- trang
PAGES = {}

PAGES["index.html"] = dict(
    title="Vũ Văn Định (Tony Vũ) — Giảng viên ACCA · CFO · Cố vấn tài chính",
    desc="Vũ Văn Định (Tony Vũ) — ACCA, CPA Australia, VACPA. 14 năm kiểm toán và quản trị tài chính; giảng viên ACCA từ 2016.",
    hero_eyebrow="Giảng viên &nbsp;·&nbsp; Người làm tài chính &nbsp;·&nbsp; Cố vấn",
    hero_num=None,
    h1="Học để làm được việc.",
    blockquote="14 năm làm kiểm toán và quản trị tài chính cho doanh nghiệp — và từ 2016, mang chính những bài toán đó vào lớp học ACCA.",
    lede="Vũ Văn Định — học viên và đồng nghiệp quen gọi là <strong>Tony Vũ</strong>. Hội viên ACCA, CPA Australia và VACPA; tốt nghiệp Cử nhân Đại học Kinh tế Quốc dân; hiện giảng dạy ACCA, CMA và IFRS tại FTMS Global và ATC Academy.",
    meta="Hà Nội, Việt Nam · Cuộn để bắt đầu ↓",
    chips=CHIPS,
    body="""
  <section id="vai-tro">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Ba vai trò. Một mục tiêu.</h2>
        <p>Giúp người học nắm được bản chất kế toán — tài chính, chứ không chỉ đủ điểm để đỗ.</p></div></div>
      </div>
      <div class="grid three">
        <div class="card"><span class="idx">01</span><h3>Giảng viên</h3>
          <div class="role">FTMS Global · ATC Academy</div>
          <p>Đứng lớp ACCA (PM/F5, AA/F8, Part 2), CMA, kế toán quản trị và IFRS từ 2016.</p>
          <a class="more" href="courses.html">Xem khoá học ↗</a></div>
        <div class="card"><span class="idx">02</span><h3>Người làm tài chính</h3>
          <div class="role">CFO · Trưởng ban Tài chính · Phó ban Tài chính</div>
          <p>14 năm ở các vị trí tài chính tại Vingroup &amp; Vinpearl, Văn Phú Invest, Vntrip, Tocotoco, Flexfit.</p>
          <a class="more" href="work.html">Xem kinh nghiệm ↗</a></div>
        <div class="card"><span class="idx">03</span><h3>Cố vấn</h3>
          <div class="role">Startup &amp; doanh nghiệp</div>
          <p>Cố vấn tài chính cho các startup Việt Nam; đào tạo nội bộ về kế toán quản trị và IFRS.</p>
          <a class="more" href="for-organisations.html">Cho doanh nghiệp ↗</a></div>
      </div>
    </div>
  </section>

  <section id="muc-luc">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Các chuyên mục</h2>
        <p>Toàn bộ ngôi nhà này — mỗi mục một trang riêng.</p></div></div>
      </div>
      <div class="grid">
        <div class="card"><h3>Giới thiệu</h3><p>Câu chuyện, hành trình và cách anh bước vào nghề dạy.</p><a class="more" href="about.html">Xem ↗</a></div>
        <div class="card"><h3>Kinh nghiệm điều hành</h3><p>Sáu vị trí tài chính tại các doanh nghiệp lớn của Việt Nam.</p><a class="more" href="work.html">Xem ↗</a></div>
        <div class="card"><h3>Học vấn &amp; chứng chỉ</h3><p>ACCA, CPA Australia, VACPA và nền tảng Kinh tế Quốc dân.</p><a class="more" href="edu.html">Xem ↗</a></div>
        <div class="card"><h3>Chuyên môn</h3><p>PM/F5, AA/F8, kế toán quản trị, IFRS, CMA, quản trị tài chính.</p><a class="more" href="competency.html">Xem ↗</a></div>
        <div class="card"><h3>Nơi giảng dạy</h3><p>FTMS Global Hà Nội và ATC Academy.</p><a class="more" href="schools.html">Xem ↗</a></div>
        <div class="card"><h3>Khoá học</h3><p>Các lớp ACCA, CMA, IFRS, kế toán quản trị và chuyên đề CFO.</p><a class="more" href="courses.html">Xem ↗</a></div>
        <div class="card"><h3>Lộ trình ACCA</h3><p>Cấu trúc 3 cấp của ACCA và cách đi qua nó.</p><a class="more" href="blueprint.html">Xem ↗</a></div>
        <div class="card"><h3>Cách dạy &amp; cách học</h3><p>Quan điểm giảng dạy: bản chất trước, mẹo thi sau.</p><a class="more" href="philosophy.html">Xem ↗</a></div>
        <div class="card"><h3>Nguồn học</h3><p>Tài liệu chính thức: ACCA, IFRS Foundation, IMA, VACPA, CPA Australia.</p><a class="more" href="library.html">Xem ↗</a></div>
        <div class="card"><h3>Học viên nói gì</h3><p>Phản hồi công khai từ học viên các lớp kế toán quản trị.</p><a class="more" href="students.html">Xem ↗</a></div>
        <div class="card"><h3>Nhật ký CFO</h3><p>Bản tin Substack (1.000+ người đăng ký): tài chính doanh nghiệp, chứng chỉ, chuyện nghề.</p><a class="more" href="writing.html">Xem ↗</a></div>
      </div>
    </div>
  </section>

  <section id="mon-dang-day">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Môn đang đứng lớp</h2>
        <p>Danh sách theo công bố của FTMS Global và ATC Academy.</p></div></div>
""" + chip_row(["Performance Management (PM — F5)", "Audit and Assurance (AA — F8)",
                "Kế toán Tài chính — Part 2", "Kiểm toán", "Quản trị tài chính",
                "Kế toán quản trị &amp; báo cáo quản trị", "IFRS / lập BCTC quốc tế", "CMA"]) + """
      </div>
    </div>
  </section>


  <section id="nhat-ky-cfo">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">04</span><div><h2><img class="newslogo" src="assets/img/nhatkycfo-logo.png" alt="Nhật ký CFO">Nhật ký CFO</h2>
        <p>Bản tin cá nhân trên Substack — hơn 1.000 người đăng ký. Tài chính doanh nghiệp, chứng chỉ quốc tế và chuyện đi làm quản trị.</p></div></div>
      </div>
      <div class="grid">
<div class="card"><div class="role">10/11/2026</div><h3><a href="https://tonyvux.substack.com/p/thu-gui-bo-863" target="_blank" rel="noopener">Thư gửi bố (*)</a></h3><p>Tôi đã gửi cách đây 2 năm</p></div>
<div class="card"><div class="role">05/11/2026</div><h3><a href="https://tonyvux.substack.com/p/lam-tai-chinh-ke-toan-gioi-ma-van-389" target="_blank" rel="noopener">Làm tài chính kế toán giỏi mà vẫn cứ nghèo</a></h3><p>Đừng inbox CFO xin mã chứng khoán nào ngon :))</p></div>
<div class="card"><div class="role">16/10/2026</div><h3><a href="https://tonyvux.substack.com/p/mot-vong-lap-ang-ngam-cua-dan-cong" target="_blank" rel="noopener">Một vòng lặp đáng ngẫm của dân công sở và 3 bước thực tế để không lãng phí nốt năm 2026.</a></h3><p>Thực ra là cho cả 2027 nữa</p></div>
<div class="card"><div class="role">20/09/2026</div><h3><a href="https://tonyvux.substack.com/p/book-review-i-tron-binh-ca" target="_blank" rel="noopener">BOOK REVIEW: ĐI TRỐN – BÌNH CA</a></h3><p>Cùng tác giả của quyển Quân khu Nam Đồng</p></div>
      </div>
      <div class="col">
        <p style="margin-top:22px"><a href="writing.html">Xem tất cả bài viết ↗</a> &nbsp;·&nbsp;
        <a href="https://tonyvux.substack.com/" target="_blank" rel="noopener">Đăng ký Nhật ký CFO ↗</a></p>
      </div>
    </div>
  </section>

  <section id="hoc-vien-noi-gi">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">05</span><div><h2>Học viên nói gì</h2>
        <p>Trích từ phần đánh giá công khai trên atcacademy.edu.vn.</p></div></div>
""" + quotes([("Thầy giáo rất nhiệt tình chia sẻ kiến thức và kinh nghiệm cho học viên… Cả hai khoá học mình đều thấy rất hữu ích khi áp dụng vào công việc thực tế.", "Học viên khoá Kế toán Quản trị — ATC Academy"),
             ("Thầy Tony rất dễ thương, cách chia sẻ và cách khai thác thêm kinh nghiệm làm việc từ học viên rất khéo léo và gần gũi.", "Học viên ATC Academy")]) + """
        <p class="note">Đây là hai phản hồi thật, lấy từ trang công khai của ATC Academy — không phải trích dẫn do trang này viết ra.</p>
      </div>
    </div>
  </section>

  <section id="bat-dau-tu-dau">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">06</span><div><h2>Bạn muốn bắt đầu từ đâu?</h2>
        <p>Chọn theo điều bạn đang cần.</p></div></div>
      </div>
      <div class="gates">
        <a class="gate dark" href="for-students.html">
          <div><h3>Tôi muốn tăng năng lực.</h3>
          <p>Người học ACCA/CMA, kế toán đang đi làm muốn lên kế toán trưởng, quản trị tài chính.</p></div>
          <div class="go">→</div>
        </a>
        <a class="gate light" href="for-organisations.html">
          <div><h3>Tôi cần cho đội của mình.</h3>
          <p>Đào tạo nội bộ về kế toán quản trị, IFRS, kỹ năng tài chính cho quản lý và chủ doanh nghiệp.</p></div>
          <div class="go">→</div>
        </a>
      </div>
    </div>
  </section>

  <section id="lien-he">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">07</span><div><h2>Liên hệ</h2>
        <p>Đặt lớp, mời giảng, hoặc hỏi về lộ trình ACCA / kế toán quản trị.</p></div></div>
        <div class="contact">
          <div><div class="k">Email</div><div class="v"><a href="mailto:%(EMAIL)s">%(EMAIL)s</a></div></div>
          <div><div class="k">Khu vực</div><div class="v">Hà Nội</div></div>
          <div><div class="k">Chứng chỉ</div><div class="v">ACCA · CPA Australia · VACPA</div></div>
        </div>
      </div>
    </div>
  </section>
""" % {"EMAIL": EMAIL},
)

PAGES["about.html"] = dict(
    title="Giới thiệu — Vũ Văn Định (Tony Vũ)",
    desc="Hành trình từ giảng đường Kinh tế Quốc dân tới ACCA, CPA Australia, VACPA và nghề dạy.",
    hero_eyebrow="Giới thiệu",
    h1="Về thầy",
    blockquote="14 năm làm kiểm toán và quản trị tài chính cho doanh nghiệp — và từ 2016, mang chính những bài toán đó vào lớp học ACCA.",
    lede="Trang này kể lại hành trình nghề nghiệp và cách anh đến với việc giảng dạy. Mọi mốc đều ghi nguồn ở cuối trang.",
    meta="Cập nhật 2026",
    chips=CHIPS,
    body="""
  <section id="hanh-trinh">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Hành trình</h2>
        <p>Từ kế toán — kiểm toán, tới điều hành tài chính, rồi tới lớp học.</p></div></div>
""" + timeline([
        ("Học vấn", "Cử nhân Đại học Kinh tế Quốc dân", "Nền tảng kế toán — kiểm toán, sau đó là các chứng chỉ nghề nghiệp quốc tế."),
        ("Chứng chỉ", "ACCA · CPA Australia · VACPA", "Hội viên Hiệp hội Kế toán Công chứng Anh Quốc (ACCA), Hiệp hội Kế toán Công chứng Australia (CPA Australia) và Hiệp hội Kiểm toán viên hành nghề Việt Nam (VACPA)."),
        ("14 năm", "Kiểm toán &amp; quản trị tài chính", "Các vị trí từ kiểm toán tới CFO/trưởng ban tài chính tại doanh nghiệp và tập đoàn (xem trang Kinh nghiệm)."),
        ("2021 → 2026", "ACCA mời viết tài liệu &amp; giảng Train the Trainers", "Hiệp hội Kế toán Công chứng Anh (ACCA) mời viết tài liệu và giảng chương trình đào tạo giảng viên (Train the Trainers) các năm 2021–2022 và 2024–2026."),
        ("2023 → nay", "Thỉnh giảng F5 tại Đại học Ngoại thương", "Thường xuyên thỉnh giảng môn F5 (kế toán quản trị) trong chương trình ACCA tại FTU."),
        ("2016 → nay", "Giảng viên ACCA", "Đứng lớp Kế toán Tài chính, Kiểm toán và Kế toán Quản lý của ACCA; đồng thời dạy CMA, kế toán quản trị và IFRS."),
        ("Hiện tại", "FTMS Global Hà Nội &amp; ATC Academy", "Giảng dạy và cố vấn tài chính cho doanh nghiệp, startup."),
    ]) + """
      </div>
    </div>
  </section>

  <section id="cach-lam-viec">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Cách anh làm việc</h2>
        <p>Ba điều lặp lại trong cả nghề tài chính lẫn nghề dạy.</p></div></div>
        <div class="prose">
          <p><strong>Lấy bài toán thật làm trung tâm.</strong> Kế toán quản trị và IFRS chỉ có nghĩa khi gắn với một quyết định cụ thể của doanh nghiệp: giá bán, cơ cấu chi phí, dòng tiền, hay một giao dịch cần hạch toán đúng.</p>
          <p><strong>Nói bằng số của chính học viên.</strong> Lớp học hiệu quả khi học viên mang số liệu và tình huống ở công ty mình vào, chứ không chỉ làm đề mẫu.</p>
          <p><strong>Chứng chỉ là phương tiện, không phải đích.</strong> Đỗ ACCA là kết quả; thứ ở lại lâu hơn là khả năng đọc báo cáo, đặt câu hỏi và ra quyết định.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="nguon">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Nguồn &amp; điểm cần xác nhận</h2></div></div>
        <div class="prose">
          <ul>
            <li>Chứng chỉ, học vấn, môn dạy: trang giảng viên của FTMS Global và ATC Academy (công khai).</li>
            <li>Tên gọi “Tony Vũ”: slide giảng dạy ACCA PM do chính thầy đăng công khai, và cách học viên ATC gọi.</li>
            <li>Số năm kinh nghiệm có <strong>ba mức khác nhau</strong>: chính thầy viết “14 năm” (About của Nhật ký CFO), FTMS ghi 13, ATC ghi 12 → trang này dùng “hơn 14 năm” theo lời chính thầy.</li>
            <li>“Ex-EY” và hơn 1.000 người đăng ký bản tin: theo tagline và trang chủ Nhật ký CFO.</li>
            <li>Vingroup &amp; Vinpearl: chỉ FTMS nêu, ATC không nêu → để ở mức “quản lý cấp cao”.</li>
            <li>Chưa có ảnh chân dung và chưa có số liệu “số học viên đã dạy / tỉ lệ đậu” có nguồn → cố ý không đưa vào.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["work.html"] = dict(
    title="Kinh nghiệm điều hành — Vũ Văn Định (Tony Vũ)",
    desc="Các vị trí tài chính tại Vingroup & Vinpearl, Văn Phú Invest, Vntrip, Tocotoco, Flexfit và cố vấn startup.",
    hero_eyebrow="Kinh nghiệm",
    h1="Kinh nghiệm điều hành",
    blockquote="14 năm ở các vị trí kiểm toán, quản trị tài chính và quản trị hiệu quả doanh nghiệp.",
    lede="Sáu vị trí dưới đây theo phần giới thiệu giảng viên công bố trên FTMS Global và ATC Academy.",
    meta="Danh sách công khai",
    chips=CHIPS,
    body="""
  <section id="vi-tri">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Sáu vị trí</h2>
        <p>Theo từng doanh nghiệp, không theo thứ tự thời gian.</p></div></div>
      </div>
""" + grid_cards(list(W.values())) + """
      <div class="col"><p class="note">Nguồn: trang giảng viên của FTMS Global (ftmsglobal.edu.vn/giang-vien-cma, /giang-vien-ftms) và trang khoá học của ATC Academy. FTMS ghi “hơn 13 năm”, ATC ghi “hơn 14 năm” cho cùng một người — trang này dùng mức thấp hơn để an toàn; mốc thời gian cụ thể chưa có công bố nào thống nhất giữa hai nguồn.</p></div>
    </div>
  </section>

  <section id="y-nghia">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Vì sao phần này quan trọng với lớp học</h2></div></div>
        <div class="prose">
          <p>Mỗi môn ACCA đều có phần “applied” — nơi đề bài mô tả một doanh nghiệp đang phải ra quyết định. Người từng ngồi ở ghế CFO sẽ nhận ra đề bài đó nhanh hơn: chi phí nào thực sự biến đổi, dòng tiền bị chặn ở đâu, kiểm toán viên sẽ hỏi gì trước.</p>
          <p>Đó là lý do phần kinh nghiệm điều hành được đặt cạnh phần giảng dạy trong ngôi nhà này, thay vì tách thành “hồ sơ xin việc”.</p>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["edu.html"] = dict(
    title="Học vấn & chứng chỉ — Vũ Văn Định (Tony Vũ)",
    desc="Cử nhân Đại học Kinh tế Quốc dân; hội viên ACCA, CPA Australia và VACPA.",
    hero_eyebrow="Học vấn & chứng chỉ",
    h1="Nền tảng nghề nghiệp",
    blockquote="Ba tổ chức nghề nghiệp, một nền tảng học thuật — và 12 năm dùng chúng trong công việc thật.",
    lede="ACCA, CPA Australia và VACPA là ba bộ tiêu chuẩn khác nhau; giữ cả ba nghĩa là phải làm việc được ở cả ba hệ quy chiếu.",
    meta="Chứng chỉ nghề nghiệp",
    chips=CHIPS,
    body="""
  <section id="chung-chi">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Chứng chỉ &amp; học vấn</h2></div></div>
""" + defs([
        ("Cử nhân Đại học Kinh tế Quốc dân", "Nền tảng kế toán — kiểm toán trước khi vào các chứng chỉ nghề nghiệp quốc tế."),
        ("ACCA — Hiệp hội Kế toán Công chứng Anh Quốc", "Khung 13 môn chia ba cấp: Applied Knowledge, Applied Skills, Strategic Professional; là chuẩn phổ biến nhất cho kế toán — kiểm toán tại Việt Nam và được công nhận rộng ở các công ty Big4, doanh nghiệp FDI."),
        ("CPA Australia — Hiệp hội Kế toán Công chứng Australia", "Chứng chỉ hành nghề kế toán của Australia, gồm chương trình nền tảng và 6 môn chuyên ngành sau khi tốt nghiệp."),
        ("VACPA — Hiệp hội Kiểm toán viên hành nghề Việt Nam", "Tổ chức nghề nghiệp của kiểm toán viên Việt Nam: chuẩn mực, cập nhật nghề nghiệp và quản lý hành nghề."),
    ]) + """
        <p class="note">Các mô tả chứng chỉ ở trên là thông tin công khai của từng tổ chức; phần “cá nhân” chỉ gồm: anh là hội viên của cả ba, theo công bố của FTMS Global và ATC Academy.</p>
      </div>
    </div>
  </section>

  <section id="vi-sao-ba">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Vì sao giữ ba chứng chỉ</h2></div></div>
        <div class="prose">
          <p><strong>ACCA</strong> cho ngôn ngữ chuẩn của báo cáo tài chính và kiểm toán theo IFRS — thứ học viên Việt Nam cần nhất khi làm ở doanh nghiệp có vốn nước ngoài.</p>
          <p><strong>CPA Australia</strong> bổ sung góc nhìn quản trị và đạo đức nghề nghiệp theo chuẩn Australia — hữu ích khi so sánh hai hệ tiêu chuẩn, một việc mà người làm tài chính phải làm liên tục.</p>
          <p><strong>VACPA</strong> giữ phần “luật chơi trong nước”: chuẩn mực kiểm toán Việt Nam, yêu cầu hành nghề và các quy định cập nhật.</p>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["competency.html"] = dict(
    title="Chuyên môn — Vũ Văn Định (Tony Vũ)",
    desc="PM (F5), AA (F8), kế toán tài chính Part 2, kế toán quản trị, IFRS, CMA và quản trị tài chính.",
    hero_eyebrow="Chuyên môn",
    h1="Những mảng đi sâu",
    blockquote="Một môn thi chỉ có 6–8 chủ đề, nhưng một doanh nghiệp thì không.",
    lede="Danh sách môn anh trực tiếp đứng lớp, kèm mỗi mảng dùng vào việc gì trong công việc thật.",
    meta="Theo syllabus ACCA / CMA",
    chips=CHIPS,
    body="""
  <section id="cac-mang">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Bảy mảng</h2></div></div>
      </div>
      <div class="grid">
""" + "".join('<div class="card"><h3>%s</h3><p>%s</p></div>' % (t, b) for t, b in COMPETENCY) + """
      </div>
      <div class="col"><p class="note">Mô tả môn học theo khung công khai của ACCA/IMA; phần “anh trực tiếp dạy” theo công bố của FTMS Global và ATC Academy.</p></div>
    </div>
  </section>

  <section id="khac-biet">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Phân biệt hai thứ hay bị lẫn</h2></div></div>
        <div class="prose">
          <h3>Kế toán tài chính vs Kế toán quản trị</h3>
          <p>Kế toán tài chính trả lời câu hỏi “đã xảy ra gì” cho bên ngoài (nhà đầu tư, cơ quan thuế, ngân hàng) theo chuẩn mực — IFRS, VAS. Kế toán quản trị trả lời “nên làm gì tiếp” cho bên trong doanh nghiệp: giá bán, cơ cấu chi phí, ngân sách, đo lường hiệu quả. Hai môn này trong ACCA nằm ở hai cấp khác nhau (Applied Skills và Strategic Professional).</p>
          <h3>Kiểm toán vs Soát xét</h3>
          <p>Kiểm toán đưa ra ý kiến với mức đảm bảo cao (reasonable assurance); soát xét chỉ ở mức đảm bảo giới hạn (limited assurance). Đề thi AA/F8 thường khai thác đúng ranh giới này.</p>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["schools.html"] = dict(
    title="Nơi giảng dạy — Vũ Văn Định (Tony Vũ)",
    desc="FTMS Global Hà Nội và ATC Academy — nơi anh đứng lớp ACCA, CMA, kế toán quản trị và IFRS.",
    hero_eyebrow="Nơi giảng dạy",
    h1="Đứng lớp ở đâu",
    blockquote="Hai nơi, hai cách học khác nhau: luyện thi chứng chỉ và học để làm được việc.",
    lede="Cả hai nơi đều có phần công bố công khai về thầy và các lớp anh phụ trách.",
    meta="FTMS Global · ATC Academy",
    chips=CHIPS,
    body="""
  <section id="noi-day">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Hai nơi</h2></div></div>
      </div>
      <div class="grid">
        <div class="card"><h3>FTMS Global — Hà Nội</h3><div class="role">Giảng viên ACCA</div>
          <p>Khoá học ACCA và CMA. Các môn anh phụ trách gồm Performance Management (PM/F5), Audit and Assurance (AA/F8) và Kế toán Tài chính Part 2.</p></div>
        <div class="card"><h3>ATC Academy</h3><div class="role">Giảng viên kế toán quản trị &amp; IFRS</div>
          <p>Lập và phân tích báo cáo quản trị, phân tích tài chính doanh nghiệp, IFRS và chuyên đề “Khắc hoạ chân dung CFO tương lai”.</p></div>
        <div class="card"><h3>Đại học Ngoại thương (FTU)</h3><div class="role">Thỉnh giảng F5 — từ 2023</div>
          <p>Thường xuyên thỉnh giảng môn F5 (kế toán quản trị) trong chương trình ACCA tại FTU.</p></div>
        <div class="card"><h3>ACCA — Train the Trainers</h3><div class="role">Viết tài liệu &amp; giảng 2021–2022, 2024–2026</div>
          <p>Được Hiệp hội Kế toán Công chứng Anh (ACCA) mời viết tài liệu và giảng chương trình đào tạo giảng viên.</p></div>
      </div>
      <div class="col">
        <p class="note">Danh sách giảng viên trên website của trung tâm có thể luân phiên theo khoá — kiểm lại ở nguồn chính thức khi cần dẫn chứng.</p>
      </div>
    </div>
  </section>

  <section id="doi-tuong">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Học viên của hai nơi khác nhau thế nào</h2></div></div>
        <div class="prose">
          <p><strong>Ở FTMS Global:</strong> đa số đang học để thi chứng chỉ — sinh viên, người chuyển ngành, kế toán viên muốn có ACCA. Mục tiêu rõ và có ngày thi.</p>
          <p><strong>Ở ATC Academy:</strong> đa số là người đi làm — kế toán, kế toán trưởng, quản lý tài chính — học để áp dụng vào công việc tuần sau, không để thi.</p>
          <p>Vì vậy cách dạy cũng khác: một bên cần chiến thuật làm đề, một bên cần mổ xẻ tình huống thật của chính học viên.</p>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["courses.html"] = dict(
    title="Khoá học — Vũ Văn Định (Tony Vũ)",
    desc="ACCA PM/F5, AA/F8, Part 2, kế toán quản trị, IFRS, CMA và chuyên đề CFO.",
    hero_eyebrow="Khoá học",
    h1="Các lớp đang dạy",
    blockquote="Chọn lớp theo việc bạn cần làm được, không theo tên chứng chỉ.",
    lede="Danh mục dưới đây theo các lớp đã được công bố công khai. Lịch khai giảng và học phí do trung tâm công bố — trang này không tự đặt giá.",
    meta="ACCA · CMA · IFRS · Kế toán quản trị",
    chips=CHIPS,
    body="""
  <section id="danh-muc">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Danh mục lớp</h2></div></div>
      </div>
""" + grid_cards([(t, g, b) for t, g, b in COURSES]) + """
      <div class="col"><p class="note">Muốn biết lịch khai giảng, cơ sở và học phí: liên hệ trực tiếp trung tâm hoặc thầy qua email ở trang <a href="contact.html">Liên hệ</a>.</p></div>
    </div>
  </section>

  <section id="lich-hoc">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Lịch &amp; hình thức</h2>
        <p>Theo công bố hiện hành trên trang khoá học của ATC Academy (ghi nhận 23/11/2026).</p></div></div>
        <div class="defs">
          <div class="def"><h3>Kế toán quản trị chuyên sâu</h3>
            <p>Khai giảng <strong>24/11/2026</strong> · học <strong>Thứ 3 &amp; Thứ 5</strong> · <strong>20h–21h30</strong> · <strong>12 buổi online</strong>. Nội dung: xây hệ thống báo cáo quản trị theo 6 bước, phân tích chi phí, điểm hoà vốn, lập và quản trị ngân sách; thực hành trên Excel để ra báo cáo tự động cho ban giám đốc.</p></div>
          <div class="def"><h3>Combo “Khắc hoạ chân dung CFO tương lai”</h3>
            <p>Là <strong>ghép hai khoá</strong>: Kế toán quản trị chuyên sâu (12 buổi) + Phân tích tài chính chuyên sâu (12 buổi). Hai giảng viên: <strong>Vũ Văn Định</strong> (kế toán quản trị) và <strong>Nguyễn Thành Trung</strong> (phân tích tài chính). Học xong cả hai khoá là hoàn thành lộ trình.</p></div>
          <div class="def"><h3>Học viên xem giảng thử trước khi đăng ký</h3>
            <p>Hai buổi dạy thật được công bố công khai: <em>“Phân tích điểm hòa vốn trong kế toán quản trị”</em> (2:45:48 · 4.300+ lượt xem) và <em>“Kiến thức cơ bản về BCTC theo chuẩn mực quốc tế IFRS”</em> (20:25 · 3.000+ lượt xem).</p></div>
        </div>
      </div>
    </div>
  </section>

  <section id="chi-tiet">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Chi tiết chương trình</h2>
        <p>Cấu trúc đề lấy từ syllabus &amp; study guide chính thức của ACCA; lịch và học phí theo công bố của FTMS Global.</p></div></div>
        <div class="defs">
          <div class="def"><h3>Performance Management (PM / F5) — 3 giờ, 100 điểm</h3>
            <p><strong>Section A:</strong> 15 câu trắc nghiệm (OT) × 2 điểm = 30 điểm.<br>
               <strong>Section B:</strong> 3 case, mỗi case 5 câu OT × 2 điểm = 30 điểm.<br>
               <strong>Section C:</strong> 2 câu tự luận (constructed response) × 20 điểm = 40 điểm — một câu từ mảng đo lường hiệu quả, một câu từ mảng kỹ thuật ra quyết định và/hoặc ngân sách.<br>
               Thi trên máy, thêm 10 phút đọc hướng dẫn. <strong>Điểm đạt: 50%.</strong></p></div>
          <div class="def"><h3>Audit and Assurance (AA / F8) — 3 giờ, 100 điểm</h3>
            <p><strong>Section A:</strong> 3 case × 10 điểm (mỗi case 5 câu OT × 2 điểm) = 30 điểm.<br>
               <strong>Section B:</strong> 1 câu 30 điểm + 2 câu 20 điểm = 70 điểm — tập trung vào lập kế hoạch &amp; đánh giá rủi ro, kiểm soát nội bộ, bằng chứng kiểm toán.<br>
               Thi trên máy. <strong>Điểm đạt: 50%.</strong></p></div>
          <div class="def"><h3>Lịch &amp; học phí tại FTMS Global</h3>
            <p>PM và AA khai giảng <strong>12/2026</strong> (Hà Nội và Online); lớp buổi tối và cuối tuần. Học phí niêm yết môn PM: <strong>8.850.000đ</strong>; combo 4 môn Strategic Professional 54.600.000đ; combo 9 môn (F5–P5) 78.600.000đ; combo 3 môn giảm 38%.</p></div>
          <div class="def"><h3>CMA — khác ACCA ở chỗ nào</h3>
            <p>CMA (IMA, Hoa Kỳ) thi <strong>2 phần</strong>, mỗi phần gồm trắc nghiệm và essay; nội dung nghiêng về kế toán quản trị nội bộ doanh nghiệp thay vì báo cáo tài chính — kiểm toán. Cấu trúc và lệ phí mới nhất xem trên imanet.org (trang này không chép lại con số vì IMA có thể đổi).</p></div>
        </div>
        <p class="note">Nguồn: ACCA syllabus &amp; study guide PM (S26–J27) và AA (S26–J27); ftmsglobal.edu.vn (lịch khai giảng + học phí, ghi nhận 23/11/2026). Giá và lịch có thể thay đổi — kiểm lại trước khi tư vấn học viên.</p>
      </div>
    </div>
  </section>

  <section id="chon-lop">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">04</span><div><h2>Chọn lớp theo mục tiêu</h2></div></div>
        <div class="defs">
          <div class="def"><h3>Tôi cần lấy chứng chỉ ACCA</h3><p>Bắt đầu từ nền tảng kế toán tài chính rồi vào PM và AA; mỗi môn đi kèm đề thi thử và chữa theo barem của ACCA.</p></div>
          <div class="def"><h3>Tôi đang đi làm, cần dùng ngay</h3><p>Học kế toán quản trị và IFRS: báo cáo quản trị, cơ cấu chi phí, đọc và soát xét báo cáo tài chính.</p></div>
          <div class="def"><h3>Tôi hướng tới vị trí CFO</h3><p>Đi qua cả ba trục: kế toán — quản trị tài chính — quản trị hiệu quả, và luyện nói trước ban điều hành. Chuyên đề “Khắc hoạ chân dung CFO tương lai” ở ATC Academy đi đúng hướng này.</p></div>
          <div class="def"><h3>Tôi là chủ doanh nghiệp / quản lý không chuyên tài chính</h3><p>Cần bản đồ tài chính doanh nghiệp của mình: dòng tiền, điểm hoà vốn, chi phí thực biến đổi — dạng đào tạo nội bộ (xem <a href="for-organisations.html">Cho doanh nghiệp</a>).</p></div>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["blueprint.html"] = dict(
    title="Lộ trình ACCA — Vũ Văn Định (Tony Vũ)",
    desc="Cấu trúc 3 cấp của ACCA và cách đi qua nó với người vừa học vừa làm.",
    hero_eyebrow="Lộ trình",
    h1="Đi qua ACCA",
    blockquote="Mỗi cấp trả lời một câu hỏi khác nhau — biết mình đang ở cấp nào thì bớt học dư.",
    lede="Khung dưới đây là cấu trúc chính thức của ACCA (13 môn, 3 cấp); phần gợi ý cách học là kinh nghiệm giảng dạy, không phải quy định của ACCA.",
    meta="Applied Knowledge → Applied Skills → Strategic Professional",
    chips=CHIPS,
    body="""
  <section id="ba-cap">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Ba cấp</h2>
        <p>Theo khung chương trình ACCA (accaglobal.com).</p></div></div>
      </div>
      <div class="grid three">
        <div class="card"><h3>Cấp 1 — Applied Knowledge</h3><div class="role">3 môn</div>
          <p>Kế toán kinh doanh (BT), Kế toán quản trị (MA), Kế toán tài chính (FA). Mục tiêu: hiểu ngôn ngữ kế toán. Có thể thi dạng máy tính theo từng môn.</p></div>
        <div class="card"><h3>Cấp 2 — Applied Skills</h3><div class="role">6 môn · nơi anh dạy PM và AA</div>
          <p>Quản trị kinh doanh (LW), Quản trị hiệu quả (PM/F5), Thuế (TX), Báo cáo tài chính (FR), Kiểm toán &amp; đảm bảo (AA/F8), Quản trị tài chính (FM).</p></div>
        <div class="card"><h3>Cấp 3 — Strategic Professional</h3><div class="role">2 môn bắt buộc + 2 trong 4 môn tự chọn</div>
          <p>Bắt buộc: SBL (chiến lược kinh doanh) và SBR (báo cáo chiến lược). Tự chọn: AFM, APM, ATX, AAA.</p></div>
      </div>
      <div class="col"><p class="note">Cấu trúc và mã môn ACCA có thể được hội cập nhật theo thời gian — nguồn chính thức là ACCA Study Hub.</p></div>
    </div>
  </section>

  <section id="cach-di">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Bốn quyết định quan trọng hơn việc chọn môn</h2></div></div>
        <div class="defs">
          <div class="def"><h3>Thi từng môn hay ghép cặp</h3><p>Người đi làm nên đi từng môn nhưng không nghỉ quá 3 tuần giữa các kỳ; kiến thức FR/PM hao rất nhanh nếu dừng.</p></div>
          <div class="def"><h3>Thứ tự PM — AA — FR — FM</h3><p>PM và AA là hai môn có thể học độc lập; FR nên học sau FA và trước SBR; FM học sau khi đã quen phân tích con số.</p></div>
          <div class="def"><h3>Luyện đề theo barem, không theo cảm giác</h3><p>ACCA chấm theo cấu trúc câu trả lời. Viết lại bài của mình theo barem examiner’s report là cách tăng điểm nhanh nhất.</p></div>
          <div class="def"><h3>Giữ liên tục vì động lực, không vì lịch</h3><p>Đứt quãng là kẻ thù lớn nhất — quan trọng hơn cả việc chọn môn trước.</p></div>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["philosophy.html"] = dict(
    title="Cách dạy & cách học — Vũ Văn Định (Tony Vũ)",
    desc="Quan điểm giảng dạy: bản chất trước, mẹo thi sau; dùng số liệu thật của học viên.",
    hero_eyebrow="Cách dạy &amp; cách học",
    h1="Bản chất trước, mẹo thi sau",
    blockquote="Một kỳ thi kiểm tra kế toán. Công việc kiểm tra rất nhiều thứ khác nữa.",
    lede="Trang này giữ quan điểm dạy học của lớp; nội dung hiện là bản nháp dựa trên mô tả lớp và phản hồi học viên, chờ thầy biên tập lại.",
    meta="Nháp — chờ thầy xác nhận",
    chips=CHIPS,
    body="""
  <section id="bon-nguyen-tac">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Bốn nguyên tắc đang dùng trên lớp</h2></div></div>
        <div class="defs">
          <div class="def"><h3>1. Hiểu mục đích trước khi học cách làm</h3><p>Mỗi kỹ thuật đều được mở đầu bằng câu hỏi “kỹ thuật này để làm gì”. Kế toán quản trị mà không gắn với một quyết định thì chỉ còn là công thức.</p></div>
          <div class="def"><h3>2. Số của chính mình, không số của sách</h3><p>Học viên mang báo cáo, chi phí, quy trình ở công ty mình vào bài. Cùng một khái niệm, hai doanh nghiệp cho hai câu trả lời khác nhau — đó là bài học.</p></div>
          <div class="def"><h3>3. Chấm theo barem để biết mình mất điểm ở đâu</h3><p>Không dừng ở “đúng/sai”. Viết lại câu trả lời theo cấu trúc mà hội đồng chấm điểm dùng, và ghi lại lỗi lặp.</p></div>
          <div class="def"><h3>4. Nói được trước người khác</h3><p>Kết thúc một chủ đề bằng việc trình bày lại cho người khác hiểu — người làm tài chính phải giải thích được số liệu cho người không làm tài chính.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section id="ngoai-lop">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Chia sẻ ngoài lớp học</h2>
        <p>Những chỗ thầy nói trước công chúng — bằng chứng cho phần “cách làm việc”.</p></div></div>
        <div class="defs">
          <div class="def"><h3>Toạ đàm “Định hướng nghề nghiệp trong bối cảnh hội nhập quốc tế”</h3>
            <p>Diễn giả cùng bà Nguyễn Thị Thủy (Kế toán trưởng IBM Việt Nam) và bà Lê Thị Mỹ Hạnh (khối Đào tạo ACCA), tại khoa Kế toán — Kiểm toán, <strong>Đại học Công nghiệp Hà Nội</strong>. Khi đó thầy giữ vai trò Giám đốc tài chính Vntrip. Nội dung: bối cảnh công nghệ thay đổi cách con người làm việc, và sinh viên kế toán cần chuẩn bị gì.</p>
            <p><a href="https://www.haui.edu.vn/vn/hoat-dong-sinh-vien/toa-dam-dinh-huong-nghe-nghiep-trong-boi-canh-hoi-nhap-quoc-te-cho-sinh-vien-khoa-ke-toan-kiem-toan/63720" target="_blank" rel="noopener">Đọc tin trên HaUI ↗</a></p></div>
          <div class="def"><h3>Giảng thử công khai trước khi học viên đăng ký</h3>
            <p>ATC Academy công bố nguyên buổi dạy thật của thầy để học viên xem trước: bài về điểm hoà vốn trong kế toán quản trị và bài về BCTC theo IFRS. Đây là cách minh bạch đúng — người học không phải mua trước rồi mới biết thầy dạy thế nào.</p>
            <p><a href="courses.html">Xem ở trang Khoá học ↗</a></p></div>
        </div>
      </div>
    </div>
  </section>

  <section id="cach-hoc">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Cách học cho người vừa học vừa làm</h2></div></div>
        <div class="prose">
          <ul>
            <li>Chọn 1 khung giờ cố định mỗi ngày, ngắn nhưng không bỏ — 45 phút đều đặn ăn hơn 5 giờ cuối tuần.</li>
            <li>Mỗi chủ đề làm theo vòng: đọc syllabus → làm 1 đề nhỏ → viết lại phần sai → mới sang chủ đề tiếp.</li>
            <li>Ghi “sổ lỗi” riêng: lỗi nào lặp 3 lần thì phải học lại từ gốc, không luyện thêm đề.</li>
            <li>Học nhóm 2–3 người cùng môn, mỗi tuần một người trình bày — học bằng cách dạy lại là cách nhớ lâu nhất.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["library.html"] = dict(
    title="Nguồn học — Vũ Văn Định (Tony Vũ)",
    desc="Nguồn chính thức để học ACCA, IFRS và CMA: ACCA Study Hub, IFRS Foundation, IMA, VACPA, CPA Australia.",
    hero_eyebrow="Nguồn học",
    h1="Học từ nguồn gốc",
    blockquote="Tài liệu của hội và của ban soạn chuẩn mực luôn đúng hơn bản tóm tắt lan truyền.",
    lede="Danh sách nguồn chính thức, dùng được ngay — không phải tài liệu bán khoá học.",
    meta="Nguồn chính thức",
    chips=CHIPS,
    body="""
  <section id="nguon">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Năm nguồn</h2></div></div>
      </div>
      <div class="grid">
""" + "".join(
        '<div class="card"><h3>%s</h3><p>%s</p><a class="more" href="%s" target="_blank" rel="noopener">Mở ↗</a></div>' % (t, b, u)
        for t, b, u in BOOKS) + """
      </div>
      <div class="col">
        <p class="note">Các liên kết trỏ tới website chính thức của từng tổ chức. Trang này không bán tài liệu và không chứa bản sao đề thi.</p>
      </div>
    </div>
  </section>

  <section id="thu-tu-doc">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Thứ tự đọc cho người mới</h2></div></div>
        <div class="prose">
          <ul>
            <li><strong>1.</strong> Syllabus của môn sắp học — đọc hết, không bỏ, vì đó là bản đồ đề thi.</li>
            <li><strong>2.</strong> Study guide chính thức, phần “examinable documents” để biết chuẩn mực nào được thi.</li>
            <li><strong>3.</strong> Examiner’s report của 2–3 kỳ gần nhất: nơi nói thẳng thí sinh hay mất điểm ở đâu.</li>
            <li><strong>4.</strong> Past paper/đề mẫu, làm có bấm giờ, rồi mới đọc barem.</li>
            <li><strong>5.</strong> Chuẩn mực gốc (IFRS/IAS liên quan) — chỉ đọc phần được thi, nhưng đọc nguyên văn.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["students.html"] = dict(
    title="Học viên nói gì — Vũ Văn Định (Tony Vũ)",
    desc="Phản hồi công khai của học viên các lớp kế toán quản trị tại ATC Academy.",
    hero_eyebrow="Học viên",
    h1="Học viên nói gì",
    blockquote="Phần đáng tin nhất của một trang cá nhân là những gì người khác nói, không phải những gì mình tự viết.",
    lede="Hai phản hồi dưới đây lấy nguyên văn từ phần đánh giá công khai trên atcacademy.edu.vn.",
    meta="Nguồn: ATC Academy",
    chips=CHIPS,
    body="""
  <section id="phan-hoi">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Phản hồi công khai</h2></div></div>
""" + quotes([
        ("Thầy giáo rất nhiệt tình chia sẻ kiến thức và kinh nghiệm cho học viên… Cả hai khoá học mình đều thấy rất hữu ích khi áp dụng vào công việc thực tế.", "Học viên khoá Kế toán Quản trị — ATC Academy"),
        ("Thầy Tony rất dễ thương, cách chia sẻ và cách khai thác thêm kinh nghiệm làm việc từ học viên rất khéo léo và gần gũi.", "Học viên ATC Academy"),
    ]) + """
        <p class="note">Trích nguyên văn, không thêm bớt, có ghi nguồn người nói.</p>
      </div>
    </div>
  </section>

  <section id="danh-gia">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Những gì trang này cố ý KHÔNG đưa</h2></div></div>
        <div class="prose">
          <ul>
            <li>Không có con số “đã dạy bao nhiêu học viên” hay “tỉ lệ đậu bao nhiêu %” — vì chưa có nguồn công khai nào xác nhận.</li>
            <li>Không có ảnh lớp học/kết quả thi của học viên khi chưa xin phép.</li>
            <li>Không có đánh giá do trang tự viết ra dưới dạng “học viên nói…”.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""",
)

PAGES["for-students.html"] = dict(
    title="Cho người học — Vũ Văn Định (Tony Vũ)",
    desc="Dành cho người học ACCA/CMA và kế toán đang đi làm muốn lên kế toán trưởng, quản trị tài chính.",
    hero_eyebrow="Cho người học",
    h1="Tôi muốn tăng năng lực.",
    blockquote="Học để làm được việc — chứng chỉ là hệ quả, không phải mục đích.",
    lede="Trang này dành cho sinh viên, người chuyển ngành và kế toán đang đi làm. Ba bước dưới đây là cách bắt đầu gọn nhất.",
    meta="ACCA · CMA · Kế toán quản trị",
    chips=CHIPS,
    body="""
  <section id="ba-buoc">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Ba bước bắt đầu</h2></div></div>
      </div>
      <div class="grid three">
        <div class="card"><span class="idx">01</span><h3>Xác định bạn đang ở cấp nào</h3>
          <p>Chưa biết kế toán → cấp Applied Knowledge. Đã làm kế toán 1–2 năm → vào thẳng Applied Skills. Đang làm quản trị → nhắm Strategic Professional.</p>
          <a class="more" href="blueprint.html">Xem lộ trình ↗</a></div>
        <div class="card"><span class="idx">02</span><h3>Chọn môn theo công việc</h3>
          <p>Làm kiểm toán → AA/F8. Làm quản trị/giá thành → PM/F5 và kế toán quản trị. Làm ở doanh nghiệp FDI → FR và IFRS.</p>
          <a class="more" href="competency.html">Xem chuyên môn ↗</a></div>
        <div class="card"><span class="idx">03</span><h3>Lấy nguồn gốc rồi mới luyện đề</h3>
          <p>Syllabus → study guide → examiner’s report → đề có bấm giờ → đọc barem. Không bắt đầu bằng đề.</p>
          <a class="more" href="library.html">Xem nguồn học ↗</a></div>
      </div>
    </div>
  </section>

  <section id="hoc-o-dau">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Học trực tiếp thì học ở đâu</h2></div></div>
        <div class="prose">
          <p><strong>Muốn thi lấy chứng chỉ ACCA/CMA:</strong> lớp luyện thi tại FTMS Global — PM/F5, AA/F8, Part 2.</p>
          <p><strong>Đang đi làm, cần dùng ngay:</strong> lớp kế toán quản trị, IFRS và chuyên đề CFO tại ATC Academy.</p>
          <p>Chi tiết lớp và lịch khai giảng: xem <a href="courses.html">Khoá học</a> rồi liên hệ trung tâm hoặc thầy.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="lien-he-hoc">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Hỏi trước khi đăng ký</h2>
        <p>Gửi kèm 3 thông tin này thì trả lời sẽ sát hơn.</p></div></div>
        <div class="prose">
          <ul>
            <li>Bạn đang làm gì, mấy năm kinh nghiệm, và đã học kế toán tới đâu.</li>
            <li>Mục tiêu trong 12 tháng tới: lấy chứng chỉ nào, hay giải quyết việc gì ở công ty.</li>
            <li>Bạn có bao nhiêu giờ mỗi tuần cho việc học.</li>
          </ul>
          <p><a href="mailto:%s">Gửi email cho thầy →</a></p>
        </div>
      </div>
    </div>
  </section>
""" % EMAIL,
)

PAGES["for-organisations.html"] = dict(
    title="Cho doanh nghiệp — Vũ Văn Định (Tony Vũ)",
    desc="Đào tạo nội bộ về kế toán quản trị, IFRS và kỹ năng tài chính cho quản lý, chủ doanh nghiệp.",
    hero_eyebrow="Cho doanh nghiệp",
    h1="Tôi cần cho đội của mình.",
    blockquote="Đào tạo nội bộ chỉ đáng tiền khi bài tập là số liệu thật của chính doanh nghiệp.",
    lede="Dành cho doanh nghiệp muốn nâng năng lực tài chính của đội kế toán — quản lý, hoặc của chính ban điều hành.",
    meta="Đào tạo nội bộ · Cố vấn",
    chips=CHIPS,
    body="""
  <section id="chude">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Bốn nhóm chủ đề thường được đặt</h2></div></div>
        <div class="defs">
          <div class="def"><h3>Kế toán quản trị &amp; báo cáo quản trị</h3><p>Thiết kế bộ báo cáo quản trị dùng được cho điều hành: doanh thu theo kênh, cơ cấu chi phí, điểm hoà vốn, chỉ số theo tuần/tháng.</p></div>
          <div class="def"><h3>IFRS &amp; kỹ năng soát xét báo cáo tài chính</h3><p>Nhận diện giao dịch trọng yếu, đọc chuẩn mực đúng phần cần dùng, và các lỗi hay gặp khi chuyển đổi.</p></div>
          <div class="def"><h3>Quản trị tài chính cho quản lý không chuyên</h3><p>Dành cho trưởng phòng/giám đốc không làm tài chính: đọc ba báo cáo, hiểu dòng tiền, biết con số nào của mình ảnh hưởng tới lợi nhuận.</p></div>
          <div class="def"><h3>Cố vấn tài chính &amp; lộ trình CFO</h3><p>Đồng hành cùng đội tài chính hoặc ban điều hành trong giai đoạn mở rộng, gọi vốn, hoặc tái cấu trúc chi phí.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section id="cach-lam">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Cách làm việc với doanh nghiệp</h2></div></div>
        <div class="prose">
          <ul>
            <li><strong>Khảo sát trước:</strong> 30–60 phút với ban điều hành để xác định vấn đề thật, không dạy theo giáo trình có sẵn.</li>
            <li><strong>Dùng dữ liệu của chính doanh nghiệp</strong> (đã ẩn danh nếu cần) làm bài tập — học viên giải quyết việc thật ngay trong lớp.</li>
            <li><strong>Đầu ra cụ thể:</strong> kết thúc đợt đào tạo phải có một sản phẩm dùng được — bộ báo cáo quản trị, checklist soát xét, hoặc bản trình bày cho ban điều hành.</li>
            <li><strong>Chuyển giao:</strong> tài liệu và mẫu để lại cho doanh nghiệp, không buộc phải thuê lại mới dùng được.</li>
          </ul>
          <p class="note">Nội dung và học phí được xác định theo từng doanh nghiệp.</p>
        </div>
      </div>
    </div>
  </section>

  <section id="lien-he-dn">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Liên hệ</h2></div></div>
        <div class="contact">
          <div><div class="k">Email</div><div class="v"><a href="mailto:%s">%s</a></div></div>
          <div><div class="k">Khu vực</div><div class="v">Hà Nội</div></div>
          <div><div class="k">Hình thức</div><div class="v">Tại doanh nghiệp hoặc online</div></div>
        </div>
      </div>
    </div>
  </section>
""" % (EMAIL, EMAIL),
)

PAGES["writing.html"] = dict(
    title="Nhật ký CFO — bài viết của Vũ Văn Định (Tony Vũ)",
    desc="Bản tin Nhật ký CFO trên Substack: tài chính doanh nghiệp, chứng chỉ quốc tế và chuyện đi làm quản trị. Hơn 1.000 người đăng ký.",
    hero_eyebrow="Bài viết · Nhật ký CFO",
    h1="Nhật ký CFO",
    blockquote="Giữa những lý thuyết trên sách vở và thực tế sinh tồn của một doanh nghiệp hay cá nhân là một khoảng cách rất xa.",
    lede="Bản tin cá nhân của thầy trên Substack — <strong>hơn 1.000 người đăng ký</strong>. Nơi viết những bài dài không vừa trong một buổi học: tài chính doanh nghiệp, chứng chỉ quốc tế, và chuyện đi làm quản trị.",
    meta="tonyvux.substack.com",
    chips=CHIPS,
    body="""
  <section id="ban-tin">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Bản tin này viết về gì</h2>
        <p>Lời tự giới thiệu trên trang About của bản tin.</p></div></div>
        <div class="poststrip">
          <a href="https://tonyvux.substack.com/p/thu-gui-bo-863" target="_blank" rel="noopener">
            <img src="assets/img/post-01.jpg" alt="Thư gửi bố"><figcaption>“Thư gửi bố (*)” — 10/11/2026</figcaption></a>
          <a href="https://tonyvux.substack.com/p/lam-tai-chinh-ke-toan-gioi-ma-van-389" target="_blank" rel="noopener">
            <img src="assets/img/post-02.jpg" alt="Làm tài chính kế toán giỏi mà vẫn cứ nghèo"><figcaption>“Làm tài chính kế toán giỏi mà vẫn cứ nghèo” — 05/11/2026</figcaption></a>
          <a href="https://tonyvux.substack.com/p/mot-vong-lap-ang-ngam-cua-dan-cong" target="_blank" rel="noopener">
            <img src="assets/img/post-03.jpg" alt="Một vòng lặp đáng ngẫm"><figcaption>“Một vòng lặp đáng ngẫm của dân công sở” — 16/10/2026</figcaption></a>
        </div>
        <div class="defs">
          <div class="def"><h3>Khoảng cách cần thu hẹp</h3>
            <p>“Trong 14 năm gắn bó với nghề tài chính, kế toán và kiểm toán, tôi nhận ra một điều: giữa những lý thuyết trên sách vở và thực tế sinh tồn của một doanh nghiệp hay cá nhân là một khoảng cách rất xa.” Bản tin ra đời từ chính nhu cầu thu hẹp khoảng cách đó.</p></div>
          <div class="def"><h3>“Những viên thuốc đắng”</h3>
            <p>Mô tả của chính tác giả: bài học thực chiến, đôi khi là thuốc đắng nhưng giúp giải quyết tận gốc vấn đề. Bốn nhóm nội dung: tài chính doanh nghiệp &amp; thuế · chuyện nghề &amp; vận hành · tài chính cá nhân · kinh nghiệm theo đuổi ACCA và các chứng chỉ khác.</p></div>
          <div class="def"><h3>Sáu chuyên mục</h3>
            <p><a href="https://tonyvux.substack.com/s/tai-chinh-doanh-nghiep" target="_blank" rel="noopener">Tài chính doanh nghiệp</a> · <a href="https://tonyvux.substack.com/s/hoc-tap-suot-oi" target="_blank" rel="noopener">Học tập suốt đời</a> · <a href="https://tonyvux.substack.com/s/tai-chinh-ca-nhan" target="_blank" rel="noopener">Tài chính cá nhân</a> · <a href="https://tonyvux.substack.com/s/hoc-acca" target="_blank" rel="noopener">Học ACCA</a> · <a href="https://tonyvux.substack.com/s/phat-trien-ban-than" target="_blank" rel="noopener">Phát triển bản thân</a> · <a href="https://tonyvux.substack.com/s/hanh-trinh-cua-toi" target="_blank" rel="noopener">Hành trình của tôi</a></p></div>
        </div>
        <p style="margin-top:22px"><a class="chip solid" href="https://tonyvux.substack.com/subscribe" target="_blank" rel="noopener">Đăng ký nhận bài mới ↗</a></p>
      </div>
    </div>
  </section>

  <section id="bai-moi">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Bài mới</h2>
        <p>12 bài gần nhất — bấm vào tiêu đề để đọc trên Substack.</p></div></div>
      </div>
      <div class="grid">
<div class="card"><div class="role">10/11/2026</div><h3><a href="https://tonyvux.substack.com/p/thu-gui-bo-863" target="_blank" rel="noopener">Thư gửi bố (*)</a></h3><p>Tôi đã gửi cách đây 2 năm</p></div>
<div class="card"><div class="role">05/11/2026</div><h3><a href="https://tonyvux.substack.com/p/lam-tai-chinh-ke-toan-gioi-ma-van-389" target="_blank" rel="noopener">Làm tài chính kế toán giỏi mà vẫn cứ nghèo</a></h3><p>Đừng inbox CFO xin mã chứng khoán nào ngon :))</p></div>
<div class="card"><div class="role">16/10/2026</div><h3><a href="https://tonyvux.substack.com/p/mot-vong-lap-ang-ngam-cua-dan-cong" target="_blank" rel="noopener">Một vòng lặp đáng ngẫm của dân công sở và 3 bước thực tế để không lãng phí nốt năm 2026.</a></h3><p>Thực ra là cho cả 2027 nữa</p></div>
<div class="card"><div class="role">20/09/2026</div><h3><a href="https://tonyvux.substack.com/p/book-review-i-tron-binh-ca" target="_blank" rel="noopener">BOOK REVIEW: ĐI TRỐN – BÌNH CA</a></h3><p>Cùng tác giả của quyển Quân khu Nam Đồng</p></div>
<div class="card"><div class="role">18/09/2026</div><h3><a href="https://tonyvux.substack.com/p/case-study-cuoc-ua-thi-phan-nganh" target="_blank" rel="noopener">Case study: Cuộc đua thị phần ngành bán lẻ dược phẩm - Khi quy mô không phải là tất cả</a></h3><p>Nhìn lại hành trình xoay chuyển cục diện giữa Long Châu và Pharmacity (Cập nhật đến năm 2026)</p></div>
<div class="card"><div class="role">13/08/2026</div><h3><a href="https://tonyvux.substack.com/p/tai-sao-ban-van-chet-chim-trong-ong" target="_blank" rel="noopener">Tại sao bạn vẫn chết chìm trong đống số liệu dù phao cứu sinh đã được ném tận tay?</a></h3><p>Căn bệnh thích ngồi chờ “phép màu” của dân tài chính kế toán, và cách duy nhất để tự giật lại sinh mệnh sự nghiệp của chính bạn.</p></div>
<div class="card"><div class="role">06/08/2026</div><h3><a href="https://tonyvux.substack.com/p/tai-sao-toi-am-anh-ien-cuong-voi" target="_blank" rel="noopener">Tại sao tôi ám ảnh điên cuồng với việc rửa bát</a></h3><p>(Và cách nó giúp tôi thiết kế sự nghiệp)</p></div>
<div class="card"><div class="role">27/07/2026</div><h3><a href="https://tonyvux.substack.com/p/chuyen-yeu-nghe-kiem-toan" target="_blank" rel="noopener">Chuyện yêu nghề kiểm toán</a></h3><p>Ngày mưa nhớ người yêu cũ Em Yêu (EY)</p></div>
<div class="card"><div class="role">27/06/2026</div><h3><a href="https://tonyvux.substack.com/p/tiet-kiem-la-tro-choi-cua-nguoi-ngheo" target="_blank" rel="noopener">Tiết kiệm là trò chơi của người nghèo? (Thật không?)</a></h3><p>Saving là trò chơi của người giàu, còn saving với người nghèo chỉ giúp mình bớt nghèo hơn thôi. Nghe vậy thôi chứ đó vẫn là 1 nửa của bức tranh</p></div>
<div class="card"><div class="role">15/06/2026</div><h3><a href="https://tonyvux.substack.com/p/tai-chinh-ca-nhan-9-ban-co-ang-thuc" target="_blank" rel="noopener">Tài chính cá nhân (9): bạn có đang thực sự tiết kiệm được tiền không?</a></h3><p>(Hay chỉ đang nai lưng ra để nuôi dưỡng cái tôi?)</p></div>
<div class="card"><div class="role">02/06/2026</div><h3><a href="https://tonyvux.substack.com/p/chi-tieu-sao-cho-moi-ong-tien-eu" target="_blank" rel="noopener">Chi tiêu sao cho mỗi đồng tiền đều hạnh phúc</a></h3><p>5 câu hỏi giúp bạn chi tiêu một cách khôn ngoan</p></div>
<div class="card"><div class="role">18/05/2026</div><h3><a href="https://tonyvux.substack.com/p/lam-the-nao-co-mot-su-nghiep-tai" target="_blank" rel="noopener">Làm thế nào có một sự nghiệp Tài chính kế toán thành công và dài hạn</a></h3><p>Dù làm CFO hay chỉ là kế toán tổng hợp</p></div>
      </div>
    </div>
  </section>

  <section id="doc-nhieu">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Đọc nhiều nhất</h2>
        <p>Theo số lượt thả tim trên bản tin (ghi nhận 23/11/2026).</p></div></div>
      </div>
      <div class="grid three">
<div class="card"><div class="role">240 ♥</div><h3><a href="https://tonyvux.substack.com/p/neu-ban-muon-phat-trien-ban-than" target="_blank" rel="noopener">Nếu bạn muốn phát triển bản thân trong năm 2026, có lẽ bạn cần để ý đến lời nói dối này (của toán học) và 1 sự thật của 10 năm</a></h3><p>Thực ra không chỉ 2026. Năm nào cũng vậy thôi. Same as ever.</p></div>
<div class="card"><div class="role">216 ♥</div><h3><a href="https://tonyvux.substack.com/p/tai-sao-oc-50-cuon-sach-mot-nam-co" target="_blank" rel="noopener">TẠI SAO ĐỌC 50 CUỐN SÁCH MỘT NĂM CÓ THỂ LÀ KHOẢN “ĐẦU TƯ LỖ” LỚN NHẤT CỦA BẠN?</a></h3><p>Đừng tự hào vì bạn có một kho tri thức đồ sộ. Trong báo cáo tài chính, kho hàng quá lớn là dấu hiệu của một doanh nghiệp sắp chết vì tắc dòng tiền.</p></div>
<div class="card"><div class="role">98 ♥</div><h3><a href="https://tonyvux.substack.com/p/bi-mat-cua-nhung-con-so-vi-sao-luong" target="_blank" rel="noopener">Bí mật của những con số: Vì sao lương 'trung bình 50 triệu' nhưng bạn vẫn nghèo?</a></h3><p>Cách tránh bị dữ liệu thao túng</p></div>
      </div>
      <div class="col">
        <p class="note">Danh mục lấy trực tiếp từ API của bản tin (50 bài, 22/02/2025 → 10/11/2026), không chép tay. Bài đầy đủ nằm trên Substack — trang này chỉ liệt kê tiêu đề, ngày và mô tả ngắn.</p>
      </div>
    </div>
  </section>
""",
)

LEAD_FORM = """
  <section id="gui-loi-nhan">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">03</span><div><h2>Gửi lời nhắn</h2>
        <p>Điền nhanh — dữ liệu ghi thẳng vào Supabase (Postgres), dùng để thử hạ tầng.</p></div></div>
        <form id="leadform" class="leadform" novalidate>
          <div class="frow">
            <label>Tên <span class="req">*</span><input name="name" maxlength="120" autocomplete="name" required></label>
            <label>Email<input name="email" type="email" maxlength="160" autocomplete="email"></label>
          </div>
          <div class="frow">
            <label>Điện thoại<input name="phone" maxlength="40" autocomplete="tel"></label>
            <label>Bạn đang quan tâm
              <select name="message">
                <option value="Học ACCA / CMA">Học ACCA / CMA</option>
                <option value="Mời giảng cho doanh nghiệp">Mời giảng cho doanh nghiệp</option>
                <option value="Cố vấn CFO">Cố vấn CFO</option>
                <option value="Chỉ hỏi một câu">Chỉ hỏi một câu</option>
              </select>
            </label>
          </div>
          <div class="frow one">
            <label>Ghi chú thêm<textarea name="note" rows="3" maxlength="1500" placeholder="Mục tiêu 12 tháng, số giờ học mỗi tuần…"></textarea></label>
          </div>
          <button type="submit" class="btn-send">Gửi</button>
          <p id="leadmsg" class="leadmsg" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>
  <script>
  (function () {
    var ENDPOINT = "https://exjuyhbiqzxhykejirkr.supabase.co/rest/v1/leads";
    var KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV4anV5aGJpcXp4aHlrZWppcmtyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTU0NjM3NjksImV4cCI6MjExMTAzOTc2OX0.HsoM8Q2YSPV9zERoKL-8hnpSxYVeoH3Mt_n5sCB-wFE";
    var f = document.getElementById("leadform");
    if (!f) return;
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = document.getElementById("leadmsg");
      var note = f.note.value.trim();
      var payload = {
        name: f.name.value.trim(),
        email: f.email.value.trim(),
        phone: f.phone.value.trim(),
        message: f.message.value + (note ? " — " + note : ""),
        source: "vuvandinh-test",
        user_agent: navigator.userAgent.slice(0, 180)
      };
      if (!payload.name) { msg.textContent = "Cần nhập tên."; msg.className = "leadmsg err"; return; }
      msg.textContent = "Đang gửi…"; msg.className = "leadmsg";
      fetch(ENDPOINT, {
        method: "POST",
        headers: {
          "apikey": KEY,
          "Authorization": "Bearer " + KEY,
          "Content-Type": "application/json",
          "Prefer": "return=minimal"
        },
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (r.status === 201) {
          msg.textContent = "Đã gửi. Cảm ơn bạn!";
          msg.className = "leadmsg ok";
          f.reset();
        } else {
          return r.text().then(function (t) {
            msg.textContent = "Lỗi " + r.status + ": " + t.slice(0, 140);
            msg.className = "leadmsg err";
          });
        }
      }).catch(function (err) {
        msg.textContent = "Không gửi được: " + err.message;
        msg.className = "leadmsg err";
      });
    });
  })();
  </script>
"""

PAGES["contact.html"] = dict(
    title="Liên hệ — Vũ Văn Định (Tony Vũ)",
    desc="Email, khu vực và các kênh liên hệ cho việc học, mời giảng và cố vấn tài chính.",
    hero_eyebrow="Liên hệ",
    h1="Liên hệ",
    blockquote="Đặt lớp, mời giảng, hoặc chỉ hỏi một câu về lộ trình ACCA — đều được.",
    lede="Email là kênh chính. Nếu là việc liên quan tới lớp học, gửi kèm mục tiêu và số giờ mỗi tuần để trả lời được sát.",
    meta="Hà Nội · Việt Nam",
    chips=CHIPS,
    body="""
  <section id="kenh">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">01</span><div><h2>Kênh liên hệ</h2></div></div>
        <div class="contact">
          <div><div class="k">Email</div><div class="v"><a href="mailto:%s">%s</a></div></div>
          <div><div class="k">Khu vực</div><div class="v">Hà Nội</div></div>
          <div><div class="k">Chứng chỉ</div><div class="v">ACCA · CPA Australia · VACPA</div></div>
          <div><div class="k">Bản tin</div><div class="v"><a href="https://tonyvux.substack.com/" target="_blank" rel="noopener">Nhật ký CFO — tonyvux.substack.com</a></div></div>
        </div>
      </div>
    </div>
  </section>

  <section id="gui-gi">
    <div class="container">
      <div class="col">
        <div class="sec-head"><span class="sec-num">02</span><div><h2>Gửi gì để được trả lời nhanh</h2></div></div>
        <div class="prose">
          <ul>
            <li><strong>Học viên cá nhân:</strong> đang làm gì · mục tiêu 12 tháng · giờ học mỗi tuần.</li>
            <li><strong>Doanh nghiệp:</strong> số người học · vấn đề đang gặp · thời gian dự kiến · hình thức (tại công ty hay online).</li>
            <li><strong>Trung tâm/đối tác:</strong> môn cần dạy · lịch · địa điểm.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""" % (EMAIL, EMAIL) + LEAD_FORM,
)


# ----------------------------------------------------------------------------- render
def render_head(title, desc, active):
    nav = "\n      ".join(
        '<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if u == active else "", t)
        for u, t in NAV)
    return """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="favicon-128.png">
<meta property="og:type" content="website">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Be+Vietnam+Pro:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>

<header>
  <div class="container bar">
    <a class="brand" href="index.html">Vũ Văn Định</a>
    <nav class="main">
      %(nav)s
    </nav>
  </div>
</header>
""" % {"title": html.escape(title), "desc": html.escape(desc), "nav": nav}


def render_footer(active):
    col = lambda items: "".join('<a href="%s">%s</a><br>' % (u, t) for u, t in items)
    n = (len(FOOTER_MAP) + 3) // 4
    cols = "".join('<div>%s</div>' % col(FOOTER_MAP[i * n:(i + 1) * n]) for i in range(4))
    return """
<footer>
  <div class="container">
    <div class="top">
      <span>© %(year)s Vũ Văn Định (Tony Vũ)</span>
      <span>ACCA · CPA Australia · VACPA — Giảng viên ACCA, CMA, IFRS · <a href="https://tonyvux.substack.com/" target="_blank" rel="noopener">Nhật ký CFO ↗</a></span>
    </div>
    <div class="map">
%(cols)s
    </div>
  </div>
</footer>
""" % {"year": YEAR, "cols": cols}


def build():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "styles.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    # giữ bản cũ để đối chiếu
    if os.path.exists(os.path.join(OUT, "index.html")) and not os.path.exists(os.path.join(OUT, "index-v1.html")):
        with open(os.path.join(OUT, "index.html"), encoding="utf-8") as f:
            old = f.read()
        with open(os.path.join(OUT, "index-v1.html"), "w", encoding="utf-8") as f:
            f.write(old)

    for slug, p in PAGES.items():
        hero = """
<main id="top">
  <div class="container hero">
    <span class="eyebrow">%(eyebrow)s</span>
    <h1 style="margin-top:18px">%(h1)s</h1>
    %(block)s
    <p class="lede">%(lede)s</p>
    %(meta)s
    %(chips)s
  </div>
%(body)s
</main>
""" % {
            "eyebrow": p["hero_eyebrow"],
            "h1": p["h1"],
            "block": ('<blockquote>%s</blockquote>' % p["blockquote"]) if p.get("blockquote") else "",
            "lede": p["lede"],
            "meta": ('<div class="meta">%s</div>' % p["meta"]) if p.get("meta") else "",
            "chips": chip_row(p["chips"]) if p.get("chips") else "",
            "body": p["body"],
        }
        doc = render_head(p["title"], p["desc"], slug) + hero + render_footer(slug) + "\n</body>\n</html>\n"
        with open(os.path.join(OUT, slug), "w", encoding="utf-8") as f:
            f.write(doc)
    print("Đã ghi %d trang + assets/styles.css" % len(PAGES))


if __name__ == "__main__":
    build()
