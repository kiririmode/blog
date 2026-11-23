# CLAUDE.md

## プロジェクト概要

kiririmode.hatenablog.jpの技術ブログ管理システムです。Markdown形式で書かれたブログエントリを管理し、textlintによる自動品質チェック、blogsyncを使ったはてなブログへの自動公開をします。

## ブログエントリの構造

ブログエントリは以下の場所に保存されます。

```text
kiririmode.hatenablog.jp/entry/YYYYMMDD/{entry_id}.md
```

- `YYYYMMDD`: 公開日
- `{entry_id}`: はてなブログのエントリID（数字。`npm run entry`で下書きを作成した時点で採番される）
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

- 公開済みエントリのfront matterは絶対に変更しないこと
- 下書きのfront matterは、`npm run prepare-publish`が更新する。`Draft`の行を消し、`Date`を公開時刻にする
- Dateフィールドが存在しないばあいは、現在時刻を上記形式で埋めること

## よく使うコマンド

### 新規エントリの作成

```bash
npm run entry
```

blogsyncを使用して新しい下書きエントリを作成します。ファイルは`kiririmode.hatenablog.jp/entry/_draft/`に数字のファイル名で作成されます。

### Lint

```bash
npm run lint path/to/file.md   # 特定のファイルをリント
```

### 画像の掲載

```bash
npm run upload-images kiririmode.hatenablog.jp/entry/_draft/123456.md
```

本文の`![alt](./123456-figure.svg)`のようなローカルの画像参照を、フォトライフが返すURLに置き換える。画像は、`<entry_id>-`で始まる名前にして下書き置き場へ置く。

### 公開準備と公開フロー

```bash
npm run prepare-publish kiririmode.hatenablog.jp/entry/_draft/123456.md
```

front matterの更新、Mermaid図の画像化、付属ファイルを含む公開日のディレクトリへの移動をまとめて実行する。ローカルの画像参照が残っていると止まるので、先に`upload-images`を実行する。詳細は`python3 scripts/prepare_publish.py --help`を参照すること。

公開は、`kiririmode.hatenablog.jp/entry/YYYYMMDD/*.md`をmainへマージしたときに起きる。GitHub Actions（`.github/workflows/blog.yml`）がlintのあとblogsyncで、はてなブログのエントリを上書きする。成否は`publish`ジョブの「Post changed entries」ステップで、blogsyncのPUTが200を返しているかで確かめる。

注意: `_draft/`配下のファイルを直接コミット・プッシュしても公開されません。必ず`npm run prepare-publish`を実行してください。

## コンテンツガイドライン

.claude/skills/create-entry/references/contents-guideline.mdに従うこと。

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues of kiririmode/blog (via the `gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
