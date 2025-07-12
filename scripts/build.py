# scripts/build.py
import markdown
import frontmatter
import shutil
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# パス定義
ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
OUTPUT_DIR = ROOT / "output"
STATIC_DIR = ROOT / "static"
TEMPLATES_DIR = ROOT / "templates"

# サイト共通情報（テンプレート変数に渡す）
site_name = "oikko のんびりAIプログラミングノート"

# テンプレート環境
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

# 出力先初期化
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True)

# static コピー
shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")
print("✅ static/ → output/static/ にコピー完了")

# ──────────────────────────────
# 1. 記事Markdown → HTMLページ化
# ──────────────────────────────
article_template = env.get_template("article.page.html")
articles_output_dir = OUTPUT_DIR / "articles"
articles_output_dir.mkdir(parents=True)

articles = []

for md_file in POSTS_DIR.glob("*.md"):
    if md_file.stem == "about":
        continue  # about.md は専用テンプレートで処理するのでスキップ

    # メタデータとコンテンツを読み込む
    post = frontmatter.load(md_file)
    metadata = post.metadata
    content = post.content

    html_body = markdown.markdown(content, extensions=["fenced_code", "tables"])

    rendered = article_template.render(
        title=metadata.get("title", md_file.stem),
        date=metadata.get("date"),
        content=html_body,
        site_name=site_name
    )
    output_path = articles_output_dir / f"{md_file.stem}.html"
    output_path.write_text(rendered, encoding="utf-8")

    articles.append({
        "title": metadata.get("title", md_file.stem),
        "url": f"articles/{md_file.stem}.html",
        "date": metadata.get("date", "1970-01-01") # ソート用に日付も追加
    })

    print(f"📝 記事生成: {output_path.relative_to(ROOT)}")

# ──────────────────────────────
# 2. indexページ（記事一覧）
# ──────────────────────────────

# 記事を日付の降順（新しいものが上）に並び替え
articles.sort(key=lambda item: item.get("date"), reverse=True)

index_template = env.get_template("index.page.html")
index_html = index_template.render(
    articles=articles,
    site_name=site_name
)
(OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
print("📚 トップページ: output/index.html を生成")

# ──────────────────────────────
# 3. aboutページ
# ──────────────────────────────
about_md_path = POSTS_DIR / "about.md"
if about_md_path.exists():
    # about.mdを読み込んでHTMLに変換
    post = frontmatter.load(about_md_path)
    html_content = markdown.markdown(post.content, extensions=["fenced_code", "tables"])

    template = env.get_template("about.page.html")
    rendered_html = template.render(
        content=html_content,
        site_name=site_name
    )
    (OUTPUT_DIR / "about.html").write_text(rendered_html, encoding="utf-8")
    print(f"👤 アバウトページ: output/about.html を生成")
else:
    print("⚠️ posts/about.md が見つかりません。aboutページはスキップされました。")
