#!/usr/bin/env bash
# deploy_local.sh — đẩy bản deploy/ lên Vercel + Cloudflare Workers bằng CLI trên máy này
# (đường tắt khi không muốn push, vì mỗi lần push = 1 deploy production Netlify = 15 credit).
#
# Vì sao phải `vercel link` mỗi lần:
#   make_deploy.py xoá và tạo lại toàn bộ thư mục deploy/, kéo theo .vercel/project.json.
#   Thiếu file đó, `vercel deploy` coi đây là project mới và tạo project rác tên "deploy"
#   (deploy-khaki-chi.vercel.app) thay vì cập nhật vuvandinh.vercel.app.
#
# Dùng:
#   scripts/deploy_local.sh            # chỉ deploy bản đang có trong deploy/
#   scripts/deploy_local.sh --build    # build lại trước (build.py + single-file + make_deploy + measure + verify)
set -uo pipefail
export PATH=/opt/data/.npm-global/bin:/opt/data/.local/bin:$PATH

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEP="$ROOT/deploy"

if [ "${1:-}" = "--build" ]; then
  cd "$ROOT" || exit 1
  echo "== build =="
  python3 build.py || exit 1
  python3 build_single_file.py || exit 1        # bản one-file KHÔNG tự sinh khi build.py chạy
  python3 make_deploy.py || exit 1
  python3 scripts/measure.py || exit 1
  python3 scripts/verify_site.py deploy || exit 1
fi

[ -d "$DEP" ] || { echo "thiếu $DEP — chạy: python3 make_deploy.py" >&2; exit 1; }

echo "== Vercel =="
cd "$DEP" || exit 1
vercel link --yes --project vuvandinh >/dev/null 2>&1 || { echo "vercel link thất bại" >&2; exit 1; }
vercel deploy --prod --yes 2>&1 | grep -E 'Production|Aliased|Error' || true
rm -f .env.local                                  # chứa OIDC token, không để lại trong cây

echo "== Cloudflare (tài khoản tạm, link sống 60 phút) =="
cd "$ROOT/deploy-cf" || exit 1
CI=1 WRANGLER_SEND_METRICS=false wrangler deploy --temporary 2>&1 \
  | grep -E 'Claim within|Claim URL|workers\.dev|Error' || true

echo
echo "Kiểm chứng nhanh:"
for u in https://vuvandinh.vercel.app https://vuvandinh-cf-test.rigorous-sushi.workers.dev; do
  printf "  %-56s %s\n" "$u" "$(curl -sL -o /dev/null -w '%{http_code}' "$u/")"
done