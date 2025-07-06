# 第一歩：プロジェクトの骨組みを作る

初めまして、**ボス**です！
このシリーズ第1話では、Markdown → HTMLに変換するビルドスクリプトと、Jinja2＋TailwindCSSを使ったテンプレートで、最低限動く状態のサイトを構築します。

---

## 👢 プロジェクト構成を確認しよう（2025年版）

リポジトリのルート構成を再確認しましょう（主要ファイルのみ抜粋）：

```bash
oikko-notebook/
├── articles/
│   └── 001-first-step.html
├── img/
│   └── header_banner.png
├── posts/
│   └── 001-first-step.md
├── scripts/
│   └── build.py
├── style.css
└── template/
    ├── about.html
    ├── base.html
    └── index.html
```

* **posts/**：Markdownで記事を書くディレクトリ
* **articles/**：ビルド後のHTML出力先
* **template/**：Jinja2テンプレート（共通レイアウト）
* **scripts/**：ビルドスクリプトを格納
* **img/**：ヘッダ画像など素材類
* **style.css**：Tailwindに加えるカスタムスタイル

---

## 🤖 よっちゃんとボスの会話ログ

> ✨ **よっちゃん**：いまの `build.py` はどんな流れで記事を出力するんでしたっけ？
>
> **ボス**：`posts/*.md` を読み込んで HTML に変換、それを `articles/` に出力。`index.html` と `about.html` もテンプレートから出力されるよ。
>
> **よっちゃん**：出力されるタイトルはファイル名ベースにしてましたよね？
>
> **ボス**：うん、`001-first-step.md` なら `001-first-step.html` になるし、表示タイトルも "001-first-step" にしてる。
>
> **よっちゃん**：じゃあ今回の仕様反映後も、記事タイトルが画面上部に出てるか確認しておきましょう。

---

## ▶️ 手順1：ビルドを実行しよう

以下のコマンドでビルドできます：

```bash
python3 scripts/build.py
```

* `articles/001-first-step.html` が生成されます
* `index.html`, `about.html` も再出力されます

---

## 💻 手順2：テンプレート構造を確認

以下は `template/base.html` の構造サンプルです：

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>{{ title }} – oikko のんびりAIプログラミングノート</title>
  <link href="/style.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body>
  <header>… ナビなど共通部分 …</header>
  <main>
    {% block content %}{{ content | safe }}{% endblock %}
  </main>
  <footer>… フッター共通部分 …</footer>
</body>
</html>
```

* `<main>` ブロック内に記事本文が展開されます
* `title` 変数はビルドスクリプトでファイル名から自動生成

---

## ✅ まとめ

1. `scripts/build.py` を実行してビルドする
2. `index.html` と `about.html`、および `articles/*.html` を出力確認
3. Markdown記事を更新したら再ビルド

---

これでサイトの「骨組み」が完成しました！
次回は、**複数記事の自動展開**や**会話ベースの見せ方強化**について進めていきます。

おたのしみに！
