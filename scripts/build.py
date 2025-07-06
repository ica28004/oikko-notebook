#!/usr/bin/env python3
import os
import markdown
from jinja2 import Environment, FileSystemLoader

POST_DIR     = "posts"
OUTPUT_DIR   = "articles"
TEMPLATE_DIR = "template"

os.makedirs(OUTPUT_DIR, exist_ok=True)
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True
)

def render_template(template_name, out_path, **context):
    tmpl = env.get_template(template_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(tmpl.render(**context))
    print(f"Generated {out_path}")

# 記事一覧ページ
md_files = sorted([f for f in os.listdir(POST_DIR) if f.endswith(".md")])
render_template(
    "index.html",
    "index.html",
    title="記事一覧",
    articles=md_files,
    active="posts"
)

# About ページ
render_template(
    "about.html",
    "about.html",
    title="About",
    active="about"
)

# 各記事ページ
for md in md_files:
    slug = md[:-3]
    path = os.path.join(POST_DIR, md)
    text = open(path, encoding="utf-8").read()
    body = markdown.markdown(text, extensions=["fenced_code","tables","toc"])
    # ファイル名をタイトルに
    title = slug
    render_template(
        "article.html",
        os.path.join(OUTPUT_DIR, slug + ".html"),
        title=title,
        content=body,
        active="posts"
    )
