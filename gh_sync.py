#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đồng bộ deploy/ → gh-pages/ rồi commit + push lên GitHub Pages.

Dùng: python3 gh_sync.py "thông điệp commit"
Bỏ qua các file không được publish: .vercel/, .env*, .gitignore, node_modules.
"""
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "deploy")
DST = os.path.join(BASE, "gh-pages")
SKIP_DIRS = {".git", ".vercel", "node_modules"}
SKIP_FILES = {".gitignore", ".env.local"}

msg = sys.argv[1] if len(sys.argv) > 1 else "Cap nhat site"


def skip(name, is_dir):
    if is_dir:
        return name in SKIP_DIRS
    return name in SKIP_FILES or name.startswith(".env")


def mirror(src, dst):
    for name in os.listdir(dst):
        if name == ".git":
            continue
        p = os.path.join(dst, name)
        is_dir = os.path.isdir(p)
        if skip(name, is_dir):
            # xoá nếu lỡ có trong repo
            shutil.rmtree(p) if is_dir else os.remove(p)
            continue
        if is_dir and not os.path.isdir(os.path.join(src, name)):
            shutil.rmtree(p)
        elif not is_dir and not os.path.exists(os.path.join(src, name)):
            os.remove(p)
    for base, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not skip(d, True)]
        rel = os.path.relpath(base, src)
        target = dst if rel == "." else os.path.join(dst, rel)
        os.makedirs(target, exist_ok=True)
        for f in files:
            if skip(f, False):
                continue
            shutil.copy2(os.path.join(base, f), os.path.join(target, f))


mirror(SRC, DST)

# dọn rác cấm publish nếu còn sót
for junk in (".vercel", ".env.local", ".gitignore"):
    p = os.path.join(DST, junk)
    if os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.exists(p):
        os.remove(p)

env = dict(os.environ)
env.update({
    "GIT_AUTHOR_NAME": "huyluong868",
    "GIT_AUTHOR_EMAIL": "huyluong868@users.noreply.github.com",
    "GIT_COMMITTER_NAME": "huyluong868",
    "GIT_COMMITTER_EMAIL": "huyluong868@users.noreply.github.com",
})
if not os.path.isdir(os.path.join(DST, ".git")):
    subprocess.run(["git", "init", "-q"], cwd=DST, env=env, check=True)
    subprocess.run(["git", "remote", "add", "origin",
                    "https://github.com/huyluong868/vuvandinh.git"], cwd=DST, env=env, check=True)
    subprocess.run(["git", "fetch", "-q", "origin", "main"], cwd=DST, env=env)
    subprocess.run(["git", "checkout", "-q", "-B", "main", "origin/main"], cwd=DST, env=env)

for cmd in (["git", "add", "-A"], ["git", "commit", "-q", "-m", msg],
            ["git", "push", "-q", "origin", "main"]):
    r = subprocess.run(cmd, cwd=DST, env=env, capture_output=True, text=True)
    if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
        print("LỖI:", cmd, (r.stdout + r.stderr).strip()[:300])

log = subprocess.run(["git", "log", "-1", "--format=%h %s"], cwd=DST, env=env,
                     capture_output=True, text=True).stdout.strip()
print("GitHub Pages:", log)