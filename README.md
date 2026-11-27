# Website Vũ Văn Định (Tony Vũ) — mã nguồn

Site tĩnh 15 trang, sinh bằng `build.py` (Python, không framework).

- Nhánh `source` = mã nguồn build (nhánh làm việc).
- Nhánh `main` = HTML đã build, GitHub Pages phục vụ nhánh này. **Không sửa tay** — CI ghi đè.

## CI/CD

Workflow: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

Pipeline: `build.py` → `inline_fonts.py` (tuỳ chọn) → `make_deliverables.py` → `make_deploy.py` →
`scripts/measure.py` → `scripts/verify_site.py deploy` (fail nếu link nội bộ hỏng / sai số `<h1>`) →
deploy lần lượt 3 nơi (mỗi nơi độc lập: một nơi lỗi không chặn nơi khác, nhưng job vẫn đỏ): Netlify, Vercel, GitHub Pages (nhánh `main`).

### Secrets cần đặt (Settings → Secrets and variables → Actions)

| Secret | Dùng cho |
|---|---|
| `NETLIFY_AUTH_TOKEN` | Netlify personal access token |
| `NETLIFY_SITE_ID` | `981e7178-c037-4c81-9918-6275ae023b20` |
| `VERCEL_TOKEN` | Vercel token (project `vuvandinh`) |

GitHub Pages dùng `GITHUB_TOKEN` có sẵn (workflow khai báo `permissions: contents: write`).
Không có token nào được hardcode trong repo.

### Trigger

- Tự động: push lên nhánh `source`. Push mới sẽ huỷ run cũ đang chạy (`concurrency`).
- Thủ công: tab Actions → *Build & Deploy* → *Run workflow* (chọn nhánh `source`).

### Rollback

Revert commit lỗi trên `source` rồi push; CI build + deploy lại bản cũ lên cả 3 nơi:

```bash
git checkout source && git revert <sha-lỗi> && git push origin source
```

(Nhánh `main` là bản build tự sinh, mỗi commit `build: <sha nguồn>` tương ứng một commit nguồn.)

### Đo lường lượt xem

`scripts/measure.py` chèn `<script defer data-site="vuvandinh" src="/assets/analytics.js">` vào mọi
HTML trong `deploy/` (idempotent). `assets/analytics.js` gửi `{path, referrer, ua, vw}` tới bảng Supabase
`page_views`; không cookie, không IP, bỏ qua `file:` và Do-Not-Track.
**Phải dán Supabase anon key vào hằng `SUPABASE_ANON_KEY`** ở đầu file; chưa dán thì script không gửi gì.

### Thay đổi ngoài `build.py` / `make_deploy.py` (và lý do)

`build.py`, `build_single_file.py`, `make_deploy.py` **không bị sửa**. Các file khác phải sửa để chạy được trên CI sạch:

- `make_deliverables.py`: đường dẫn `/opt/data/user/sites/tony-vu-about` hardcode → tính từ vị trí file.
- `inline_fonts.py`: như trên; nếu chưa có CSS Google Fonts thì tự tải (trước đây đọc file cache cục bộ).
- `scripts/verify_site.py`: (1) trả mã thoát ≠ 0 khi lỗi — trước đó luôn thoát 0 nên không fail được job;
  (2) hiểu link tuyệt đối `/assets/...` và bỏ `#fragment`/`?query`, nếu không `/assets/analytics.js` bị báo hỏng.

## Bản thứ 4: Cloudflare Workers (static assets) — đã test 27/11/2026

Không cần Pages, không cần API token cho lần thử: `wrangler deploy --temporary` tạo **tài khoản tạm**, deploy
xong có URL `*.workers.dev` sống **60 phút**, trong đó claim được để giữ vĩnh viễn.

```bash
# cấu hình: repo/deploy-cf/wrangler.jsonc  (assets.directory trỏ ../deploy)
cd /opt/data/sites/tony-vu-about/deploy-cf
wrangler deploy --temporary          # in ra Claim URL + hạn claim
```

Kết quả lần chạy: https://vuvandinh-cf-test.rigorous-sushi.workers.dev
- 10/10 trang 200, 194 link nội bộ 0 hỏng, `index.html` md5 khớp bản local, ảnh `cf-cache-status: HIT`
- Form liên hệ gửi thật → 1 dòng trong `public.leads` (`source=vuvandinh-test`)

**Khác biệt so với 3 bản kia:** Workers assets tự đổi `/contact.html` → **307 → `/contact`** (clean URL).
Đừng đặt `html_handling: "none"` để giữ đuôi `.html` — làm vậy thì `/` trả 404 vì `index.html` không còn
được map. Muốn URL giống hệt Vercel/Netlify thì phải thêm `_redirects` với `/ /index.html 200`.

**Muốn giữ site thật:** claim tài khoản tạm trong 60 phút, hoặc tạo API token (Workers Scripts: Edit) rồi
`wrangler deploy` bằng `CLOUDFLARE_API_TOKEN`.
