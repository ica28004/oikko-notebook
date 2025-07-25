---
title: "ステップ４：Google Analyticsを導入してアクセス解析を始めよう"
date: "2025-07-04"
author: "ボス"
description: "ブログ開発シリーズ第4話。Google Analyticsを導入し、サイトのアクセス解析を始める方法を解説。測定IDの取得からトラッキングコードの埋め込み、Jinja2テンプレートの修正まで、具体的な手順を紹介します。"
---

## 🎩 今日の概要

こんにちは、**ボス**です！
ブログの記事も増えてきて、自動で公開できる仕組みも整ったね。そうなると次に気になるのは、「一体どれくらいの人が、どの記事を読んでくれているんだろう？」ということじゃないかい？

今回は、サイトのアクセス状況を分析するための必須ツール「**Google Analytics**」を導入する方法を、さっちゃん先生に教えてもらうぞ！

---

## 🤖 さっちゃんとボスの会話ログ

> **ボス**：🎩 さっちゃん、サイトを作ったはいいけど、どれくらいの人が見てくれてるのか、さっぱり分からないんだ。アクセス解析ってできないのかな？
>
> **さっちゃん**：🤖 はい、もちろんです、ボス！そんな時のために『**Google Analytics**』というGoogleが提供している無料のツールがあります。これを使えば、訪問者数や人気のページ、ユーザーがどこから来たのかなどを詳しく分析できますよ！
>
> **ボス**：🎩 おお、それはすごい！ぜひ導入したい！どうやって設定すればいいんだい？
>
> **さっちゃん**：🤖 手順は大きく分けて２つです。まずGoogle Analyticsに登録して、私たちのサイト専用の**『測定ID』**というものを取得します。次に、そのIDを埋め込んだ**トラッキングコード**をブログの全ページに設置すれば完了です！
>
> **ボス**：🎩 なるほど、なんだかできそうな気がしてきた！早速やってみよう！

---

## ▶️ 手順1：Google Analyticsで「測定ID」を取得しよう

**さっちゃん**：🤖 まずは、Google Analyticsの公式サイトにアクセスして、Googleアカウントでログインし、新しいアカウントとプロパティを作成します。

1.  [Google Analytics](https://analytics.google.com/)にアクセスします。
2.  画面の指示に従ってアカウントを作成します。（アカウント名は会社名や個人名など）
3.  プロパティを作成します。（プロパティ名はサイト名「oikko-notebook」などが分かりやすいです）
4.  ウェブサイトのURL（`blog.oikko.com`）などを入力して、「データストリーム」を作成します。

**さっちゃん**：🤖 設定が完了すると、`G-XXXXXXXXXX` のような形式の「**測定ID**」が発行されます。このIDは後で使うので、コピーしておいてくださいね。

---

## 💻 手順2：トラッキングコードをブログに追加しよう

**さっちゃん**：🤖 次に、取得した測定IDを使って、トラッキングコードをブログに埋め込みます。全ページに共通で読み込ませたいので、ベースとなるテンプレートファイルを修正します。

1.  `templates/` ディレクトリに `_ga.html` という新しいファイルを作成し、以下の内容を貼り付けてください。

```html
<!-- templates/_ga.html -->

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-XXXXXXXXXX');
</script>
```

**さっちゃん**：🤖 **重要！** 上記コードの中にある `G-XXXXXXXXXX` の部分は、手順1で取得したボス自身の測定IDに**必ず**書き換えてくださいね。

2.  `templates/_base.page.html` ファイルを開き、`</head>` タグの直前に、今作ったファイルを読み込むための1行を追加します。

```html
<!-- templates/_base.page.html -->

<head>
    ...
    <link rel="stylesheet" href="/static/css/style.css" />
    
    <!-- ↓ この行を追加 ↓ -->
    {% include "_ga.html" %}
</head>
...
```

---

## ✅ 手順3：動作を確認しよう

**さっちゃん**：🤖 これで設定は完了です！サイトを再ビルドしてデプロイした後、自分のブログにアクセスしてみてください。

その後、Google Analyticsの管理画面を開き、「レポート」→「リアルタイム」を確認します。自分のアクセスがカウントされていれば、無事に導入成功です！🎉

![Google Analyticsの測定ID画面の画像](/static/images/analytics.png)

---

## 🤔 ちょっと待った！はまりポイント

> **ボス**：🎩 さっちゃん、大変だ！リアルタイムレポートは確認できたんだけど、アナリティクスの管理画面で「タグ設定なし」って警告が出てるページがあるぞ？`about.html`みたいだ。
>
> **さっちゃん**：🤖 本当ですか、ボス！…なるほど、原因が分かりました。これは、`about.html`だけが他のページと違う方法で作られているため、トラッキングコードを埋め込んだ共通のテンプレートが読み込まれていなかったんです。
>
> **ボス**：🎩 そうだったのか！どうすれば解決できるんだい？
>
> **さっちゃん**：🤖 はい！`scripts/build.py`を少し修正して、`about.html`も他のページと同じ仕組みで生成するように変更すれば解決します。具体的には、静的ファイルをコピーする処理をやめて、Jinja2でレンダリングするようにします。
>
> **ボス**：🎩 なるほど、全てのページで共通の仕組みを使うように統一するんだね。勉強になるな。ありがとう！


## ✨ まとめ

今回はGoogle Analyticsを導入して、アクセス解析の第一歩を踏み出したね！

* Google Analyticsに登録して「測定ID」を取得した。
* トラッキングコードを共通テンプレートに埋め込んで、全ページで計測できるようにした。
* 途中で`about.html`が計測されない問題があったけど、ビルドスクリプトを修正して解決できた。
* リアルタイムレポートで、動作確認ができた。

サイト運営の新しい楽しみが増えたね！

次回は、また新しい機能を追加していくぞ。おたのしみに！
