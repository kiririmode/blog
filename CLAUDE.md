# CLAUDE.md

## プロジェクト概要

kiririmode.hatenablog.jpの技術ブログ管理システムです。Markdown形式で書かれたブログエントリを管理し、textlintによる自動品質チェック、blogsyncを使ったはてなブログへの自動公開をします。

## ブログエントリの構造

ブログエントリは以下の場所に保存されます。

```text
kiririmode.hatenablog.jp/entry/YYYYMMDD/{unix_timestamp}.md
```

- `YYYYMMDD`: 公開日
- `{unix_timestamp}`: 記事作成開始時のUNIXタイムスタンプ
- 各ファイルにはTitle、Category、Date、URL、EditURLを含むYAMLフロントマターが含まれる。

### Front Matterの形式

```yaml
---
Title: 記事タイトル
Category:
- category1
Date: 2006-11-01T14:29:16+09:00
URL: https://kiririmode.hatenablog.jp/entry/...
EditURL: https://blog.hatena.ne.jp/...
---
```

注意事項。

- 既存エントリのフロントマターは絶対に変更しないこと
- Dateフィールドが存在しないばあいは、現在時刻を上記形式で埋めること

## よく使うコマンド

### 新規エントリの作成

```bash
npm run entry
```

blogsyncを使用して新しい下書きエントリを作成します。ファイルは `kiririmode.hatenablog.jp/entry/_draft/` に数字のファイル名で作成されます。

### Lint

```bash
npm run lint path/to/file.md   # 特定のファイルをリント
```

### 公開準備と公開フロー

ブログエントリを公開するには、以下のステップを実行します。

```bash
# 下書きを準備
npm run prepare-publish kiririmode.hatenablog.jp/entry/_draft/123456.md
```

このコマンドは以下を自動実行します。

- Mermaid図をPNG画像に変換して、はてなPhotolifeにアップロード
- Markdown内のMermaid codeblock記述をはてなPhotolifeの画像URL(`![](https://...)`)に置換
- PNG画像を`kiririmode.hatenablog.jp/entry/YYYYMMDD/` ディレクトリに移動
- 元の下書きファイルを削除

#### 自動公開

GitHub Actionsがtextlint、markdownlintによる品質チェックを行い、問題なければblogsyncによるはてなブログへ公開します。

注意: `_draft/` 配下のファイルを直接コミット・プッシュしても公開されません。必ず `npm run prepare-publish` を実行してください。

## コンテンツガイドライン

docs/contents-guideline.mdに従うこと。
