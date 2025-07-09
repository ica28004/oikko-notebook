# reorganize_project.py
import os
import shutil
from pathlib import Path

root = Path('.')

# 移動先定義
dest = {
    'template': 'templates',
    'style.css': 'static/css/style.css',
    'img/header_banner.png': 'static/images/header_banner.png',
    'logo.png': 'static/images/logo.png',
    'favicon.ico': 'static/favicon.ico',
    'articles/001-first-step.html': 'output/articles/001-first-step.html',
    'index.html': 'output/index.html',
    'about.html': 'output/about.html',
}

# ディレクトリ移動＆リネーム
dir_moves = {
    'template': 'templates',
}

print("📦 フォルダ構成を再整理中...")

# 1. ディレクトリ移動
for old, new in dir_moves.items():
    src = root / old
    dst = root / new
    if src.exists():
        shutil.move(str(src), str(dst))
        print(f"✅ 移動: {old}/ → {new}/")

# 2. 個別ファイル移動（static, outputへ）
for old, new in dest.items():
    src = root / old
    dst = root / new
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.move(str(src), str(dst))
        print(f"✅ 移動: {old} → {new}")
    else:
        print(f"⚠️ スキップ: {old}（存在しません）")

# 3. Markdownファイル名が不明なaboutを推測してコピー
template_about = root / "templates/about.page.html"
if template_about.exists():
    about_md = root / "posts/about.md"
    about_md.parent.mkdir(parents=True, exist_ok=True)
    if not about_md.exists():
        about_md.write_text("## About\n\nこのページはのんびり紹介文を記載します。", encoding="utf-8")
        print("📝 posts/about.md を仮作成しました（内容は後で編集してください）")

print("🎉 再構成完了！")
