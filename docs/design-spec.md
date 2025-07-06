# サイトデザイン仕様書

**作成日**: 2025-07-06
**Version**: 1.0.0

---

## 1. サイト概要

* **サイト名**: oikko のんびりAIプログラミングノート
* **ドメイン**: oikko.com（GitHub Pages）
* **目的**: AIを活用した開発記録を「のんびり」「まったり」学びたい初学者やエンジニア向けに公開

## 2. カラーパレット

| 用途        | 変数名            | 色コード    |
| --------- | -------------- | ------- |
| メイン       | --main-pink    | #F7C5CC |
| アクセント     | --accent-pink  | #FF7F9F |
| 背景（淡色）    | --bg-subtle    | #FFF5F7 |
| テキスト（メイン） | --text-main    | #444444 |
| 見出し       | --heading-pink | #D65F73 |

## 3. タイポグラフィ

* **フォント**: 'M PLUS Rounded 1c', sans-serif
* **本文**: font-size 16px（PC）、14px（mobile）
* **行間**: 1.6
* **見出し**:

  * h1: 2rem（PC）、1.6rem（mobile）
  * h2: 1.5rem（PC）、1.25rem（mobile）
  * h3: 1.2rem（PC）、1.1rem（mobile）

## 4. レイアウト

* **コンテナ幅**: max-w-3xl, margin auto
* **パディング**: main: px-4, py適宜
* **グリッド**: 単一カラム

## 5. ヘッダー／ナビゲーション

* **構成**:

  * 左端: サイトタイトル（`oikko のんびりAIプログラミングノート`）
  * 右端（PC）: リンク(`記事一覧`, `About`)
  * モバイル: ハンバーガーメニューに切替
* **Tailwind クラス**:

  * header: `sticky top-0 bg-white shadow`
  * nav(PC): `hidden md:flex space-x-6`
  * nav(mobile): `md:hidden hidden bg-white px-4 pb-4 space-y-2`

## 6. 本文スタイル

* **プローズプラグイン**: `prose prose-lg`
* **コードブロック**: `fenced_code` 拡張
* **テーブル**: `tables` 拡張
* **目次**: `toc` 拡張

## 7. フッター

* **配置**: max-w-3xl mx-auto mt-16 pb-8 text-center text-sm
* **色**: text-gray-500

## 8. レスポンシブ対応

* **ブレークポイント**: screen ≤600px
* **モバイル調整**:

  * font-size downscale
  * header内ハンバーガー表示
  * banner height縮小（180px）

## 9. ビルド／デプロイ

* **スクリプト**: `scripts/build.py`（Markdown→HTML, Jinja2）
* **デプロイ**: `scripts/upload.sh`(gh-pagesブランチ)

---

*このドキュメントはコピー＆ペーストで `docs/design-spec.md` に保存してください。*
