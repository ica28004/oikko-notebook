#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oikko-notebook 静的サイトジェネレータ

このスクリプトは、`posts`ディレクトリ内のMarkdownファイルを読み込み、
HTMLページを生成して`output`ディレクトリに出力します。

主な使用ライブラリ:
- markdown: MarkdownをHTMLに変換します。
- python-frontmatter: Markdownファイルの先頭にあるメタデータ（YAML Front Matter）を解析します。
- Jinja2: HTMLテンプレートエンジン。テンプレートとデータを組み合わせて最終的なHTMLを生成します。
- pathlib: ファイルシステムのパスをオブジェクト指向で操作します。
"""
import markdown  # MarkdownからHTMLへの変換
import frontmatter  # Markdownのメタデータ（frontmatter）を読み込む
import shutil  # ファイル・ディレクトリ操作（コピー、削除など）
import os  # OS依存の機能を利用
from pathlib import Path  # ファイルパスをオブジェクトとして扱う
from jinja2 import Environment, FileSystemLoader  # HTMLテンプレートエンジン
from datetime import datetime # 現在時刻の取得

# --- パス定義 ---
# スクリプトの場所を基準に、プロジェクトの各ディレクトリへのパスを定義します。
ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"  # 記事のMarkdownファイルが置かれているディレクトリ
OUTPUT_DIR = ROOT / "output"  # 生成されたHTMLなどが出力されるディレクトリ
STATIC_DIR = ROOT / "static"  # CSSや画像などの静的ファイルが置かれているディレクトリ
TEMPLATES_DIR = ROOT / "templates"  # Jinja2テンプレートが置かれているディレクトリ

# --- サイト共通情報 ---
# テンプレート内で共通して使用する変数を定義します。
site_name = "oikko のんびりAIプログラミングノート"
base_url = "https://blog.oikko.com" # サイトマップ用のベースURL

# --- Jinja2テンプレート環境の準備 ---
# TEMPLATES_DIRを読み込み元として、Jinja2の環境を初期化します。
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

# --- 出力先ディレクトリの初期化 ---
# ビルドを始める前に、古い出力ファイルが残らないようにoutputディレクトリを一度削除し、再作成します。
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True)

# --- 静的ファイルのコピー ---
# CSSや画像など、処理が不要な静的ファイルをそのままoutputディレクトリにコピーします。
shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")
print("✅ static/ → output/static/ にコピー完了")

# ──────────────────────────────
# 1. 記事Markdown → HTMLページ化
# ──────────────────────────────
article_template = env.get_template("article.page.html")  # 記事ページ用のテンプレートを読み込む
articles_output_dir = OUTPUT_DIR / "articles"  # 記事HTMLの出力先ディレクトリ
articles_output_dir.mkdir(parents=True)  # 出力先ディレクトリを作成

articles = []  # トップページの一覧表示用に、各記事の情報を格納するリスト
sitemap_pages = [] # サイトマップ生成用に、各ページの情報を格納するリスト

# postsディレクトリ内のすべてのMarkdownファイルをループ処理
for md_file in POSTS_DIR.glob("*.md"):
    # about.mdは記事一覧に含めず、専用の処理を行うため、ここではスキップします。
    if md_file.stem == "about":
        continue

    # frontmatterライブラリを使って、Markdownファイルからメタデータと本文を分離して読み込む
    # YAMLの解析エラーなどが発生した場合でも、スクリプト全体が停止しないようにする
    try:
        post = frontmatter.load(md_file)
    except Exception as e:
        print(f"❌ エラー: {md_file.relative_to(ROOT)} のメタデータの読み込みに失敗しました。")
        print(f"   詳細: {e}")
        continue # エラーがあったファイルはスキップして、次のファイルの処理を続ける

    metadata = post.metadata  # ---で囲まれた部分（title, dateなど）
    content = post.content  # 本文

    # Markdownの本文をHTMLに変換。fenced_codeでコードブロック、tablesで表を有効にする。
    html_body = markdown.markdown(content, extensions=["fenced_code", "tables"])

    rendered = article_template.render(
        title=metadata.get("title", md_file.stem),
        date=metadata.get("date"),
        content=html_body,
        site_name=site_name,
        description=metadata.get("description") # メタディスクリプションをテンプレートに渡す
    )
    # 変換後のHTMLをファイルに書き出す
    output_path = articles_output_dir / f"{md_file.stem}.html"
    output_path.write_text(rendered, encoding="utf-8")

    # トップページ（index.html）で記事一覧を生成するために、必要な情報をリストに追加する
    articles.append({
        "title": metadata.get("title", md_file.stem),
        "url": f"articles/{md_file.stem}.html",
        "date": metadata.get("date", "1970-01-01") # ソート用に日付も追加
    })

    # サイトマップ用に記事ページの情報を追加
    sitemap_pages.append({
        "url": f"{base_url}/articles/{md_file.stem}.html",
        "lastmod": metadata.get("date", datetime.now().strftime('%Y-%m-%d'))
    })

    print(f"📝 記事生成: {output_path.relative_to(ROOT)}")

# ──────────────────────────────
# 2. indexページ（記事一覧）の生成
# ──────────────────────────────

# 記事リストを日付の降順（新しいものが上）に並び替える
articles.sort(key=lambda item: item.get("date"), reverse=True)

index_template = env.get_template("index.page.html")  # トップページ用のテンプレートを読み込む
# テンプレートに記事リストとサイト名を渡して、最終的なHTMLを生成する
index_html = index_template.render(
    articles=articles,
    site_name=site_name,
    # descriptionは渡さない（ベーステンプレートのデフォルト値を使用）
)
# 生成したHTMLを output/index.html として書き出す
(OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
print("📚 トップページ: output/index.html を生成")

# サイトマップにトップページの情報を追加
sitemap_pages.append({
    "url": f"{base_url}/index.html",
    "lastmod": datetime.now().strftime('%Y-%m-%d')
})

# ──────────────────────────────
# 3. aboutページの生成
# ──────────────────────────────
about_md_path = POSTS_DIR / "about.md"
if about_md_path.exists():
    # about.mdを読み込み、メタデータと本文を分離
    post = frontmatter.load(about_md_path)
    # 本文をHTMLに変換
    html_content = markdown.markdown(post.content, extensions=["fenced_code", "tables"])

    template = env.get_template("about.page.html")
    rendered_html = template.render(
        content=html_content,
        site_name=site_name,
        description=post.metadata.get("description") # aboutページのメタディスクリプションを渡す
    )
    # 生成したHTMLを output/about.html として書き出す
    (OUTPUT_DIR / "about.html").write_text(rendered_html, encoding="utf-8")
    print(f"👤 アバウトページ: output/about.html を生成")

    # サイトマップにアバウトページの情報を追加
    sitemap_pages.append({
        "url": f"{base_url}/about.html",
        "lastmod": datetime.now().strftime('%Y-%m-%d')
    })
else:
    print("⚠️ posts/about.md が見つかりません。aboutページはスキップされました。")

# ──────────────────────────────
# 4. サイトマップの生成
# ──────────────────────────────
sitemap_template = env.get_template("sitemap.xml.j2")
sitemap_xml = sitemap_template.render(pages=sitemap_pages)
(OUTPUT_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
print("🗺️ サイトマップ: output/sitemap.xml を生成")
