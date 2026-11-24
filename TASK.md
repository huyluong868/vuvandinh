# TASK — CI/CD + do lường cho site tĩnh (repo: huyluong868/vuvandinh)

Bối cảnh: site tĩnh 15 trang, sinh bằng `build.py` (Python, không framework). Hiện deploy tay
3 nơi: Netlify (site id 981e7178-c037-4c81-9918-6275ae023b20, domain vuvandinh.netlify.app),
Vercel (project `vuvandinh`, domain vuvandinh.vercel.app), GitHub Pages (branch `main`, thư mục gốc).

Nhánh `source` = mã nguồn build. Nhánh `main` = HTML đã build (GitHub Pages phục vụ nhánh này).
Bạn đang làm việc trong bản checkout nhánh `source`.

## Việc 1 — `.github/workflows/deploy.yml`

Yêu cầu:
1. Trigger: `push` lên nhánh `source`, và `workflow_dispatch`.
2. Job `build` (ubuntu-latest, python 3.12):
   - `pip install --quiet pillow`
   - `python build.py`  → sinh 15 file HTML + assets/styles.css
   - `python inline_fonts.py` (nếu file tồn tại; lệnh này tải font Google và nhúng base64; nếu mạng lỗi thì bỏ qua, không fail build)
   - `python make_deliverables.py` → sinh logo, favicon, sitemap
   - `python make_deploy.py` → gom ra `deploy/`
   - `python scripts/verify_site.py deploy` → FAIL job nếu có link nội bộ hỏng hoặc trang thiếu/thiếu nhiều `<h1>`
   - upload artifact `deploy/`
3. Job `deploy` (needs: build), chạy trên ubuntu-latest, chỉ khi build xanh:
   - Netlify: `npx --yes netlify-cli@latest deploy --prod --no-build --dir=deploy --site "$NETLIFY_SITE_ID" --auth "$NETLIFY_AUTH_TOKEN"`
   - Vercel: `npx --yes vercel@latest deploy --prod --yes --token "$VERCEL_TOKEN"` chạy trong thư mục `deploy`
   - GitHub Pages: đẩy nội dung `deploy/` lên nhánh `main` (dùng `git subtree` hoặc clone sạch rồi copy; commit message `build: <sha nguồn>`; dùng `GITHUB_TOKEN` với `permissions: contents: write`)
   - Mỗi bước deploy phải in URL production ra log.
4. Secrets dùng: `NETLIFY_AUTH_TOKEN`, `NETLIFY_SITE_ID`, `VERCEL_TOKEN`. Không hardcode token.
5. Thêm `permissions: contents: write` ở cấp workflow; `concurrency` để huỷ run cũ khi push mới.
6. Không dùng action bên thứ ba nếu không cần; ưu tiên `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4`.

## Việc 2 — `.gitignore`
Bỏ qua: `deploy/`, `*.html` sinh tự động ở gốc (nhưng GIỮ file trong `scripts/`), `assets/styles.css`,
`assets/fonts-inline.css`, `favicon-*.png`, `logo-*.svg`, `logo-*.png`, `deliverables/`, `.vercel/`, `.env*`.
Chú ý: `assets/img/` là ảnh nguồn → phải được commit.

## Việc 3 — `scripts/measure.py` (đo lường không cần tài khoản bên thứ ba)
Viết script Python chèn một snippet đo lường vào MỌI file HTML trong `deploy/` ngay trước `</body>`:
- Một thẻ `<script defer data-site="vuvandinh" src="/assets/analytics.js"></script>` (chỉ chèn 1 lần, idempotent — chạy lại không nhân đôi).
- Snippet phải bỏ qua khi `location.protocol === 'file:'` và khi `navigator.doNotTrack === '1'`.
Tạo luôn `assets/analytics.js` (vanilla, <1.5KB):
- Gửi 1 POST tới `https://exjuyhbiqzxhykejirkr.supabase.co/rest/v1/page_views` với header
  `apikey`/`Authorization` lấy từ một biến cấu hình đặt trong file (một hằng số `SUPABASE_ANON_KEY` ở đầu file, có comment rõ).
  Payload: `{path, referrer, ua, vw}` (path = location.pathname, referrer = document.referrer cắt 200 ký tự, ua = navigator.userAgent cắt 180, vw = window.innerWidth).
- Dùng `navigator.sendBeacon` nếu có, fallback `fetch(..., {keepalive:true})`.
- Bọc toàn bộ trong try/catch, không được làm hỏng trang.
- KHÔNG đặt cookie, KHÔNG lưu IP (server không có cột đó), KHÔNG dùng thư viện ngoài.
Thêm bước `python scripts/measure.py` vào workflow sau `make_deploy.py`, trước `verify_site.py`.

## Ràng buộc
- Không sửa logic `build.py` / `build_single_file.py` / `make_deploy.py` trừ khi bắt buộc (nếu sửa, ghi rõ lý do trong README).
- Mọi lệnh phải chạy được trên CI sạch: không phụ thuộc file có sẵn ngoài repo.
- Viết thêm mục "CI/CD" vào README.md: các secret cần đặt, cách trigger, cách rollback (revert commit trên `source`).
- Trả lời cuối cùng bằng: danh sách file đã tạo/sửa + những điểm bạn KHÔNG chắc (để người điều phối kiểm tra).
