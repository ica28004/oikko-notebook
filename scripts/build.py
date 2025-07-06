#!/usr/bin/env python3
# scripts/build.py

import os
import markdown
from jinja2 import Environment, FileSystemLoader

# --- 設定 ---
POST_DIR     = "posts"        # Markdown原稿ディレクトリ
OUTPUT_DIR   = "articles"     # HTML出力ディレクトリ
TEMPLATE_DIR = "template"     # Jinja2テンプレートディレクトリ

# 出力先ディレクトリがなければ作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Jinja2 環境構築
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True
)

# --- 記事ページ生成（Markdown -> HTML） ---
article_template = env.get_template("base.html")
for md_file in sorted(os.listdir(POST_DIR)):
    if not md_file.endswith(".md"):
        continue
    md_path = os.path.join(POST_DIR, md_file)
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()
    html_body = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "toc"]
    )
    first_line = md_text.splitlines()[0]
    title = first_line.lstrip("# ").strip() if first_line.startswith("#") else "oikko のんびりAIプログラミングノート"
    rendered = article_template.render(
        title=title,
        content=html_body
    )
    out_file = md_file.replace(".md", ".html")
    with open(os.path.join(OUTPUT_DIR, out_file), "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Generated {OUTPUT_DIR}/{out_file}")

# --- トップページ生成（index.html） ---
index_template = env.get_template("index.html")
md_list = [f for f in sorted(os.listdir(POST_DIR)) if f.endswith(".md")]
rendered_index = index_template.render(
    title="oikko のんびりAIプログラミングノート",
    articles=md_list
)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(rendered_index)
print("Generated index.html")

# --- Aboutページ生成（about.html） ---
about_template = env.get_template("about.html")
rendered_about = about_template.render(title="About Us：ボスとよっちゃん")
with open("about.html", "w", encoding="utf-8") as f:
    f.write(rendered_about)
print("Generated about.html")
