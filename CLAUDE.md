# CLAUDE.md

## プロジェクト概要

kiririmode.hatenablog.jpの技術ブログ管理システムです。Markdown形式で書かれたブログエントリを管理し、textlintによる自動品質チェック、blogsyncを使ったはてなブログへの自動公開をします。

## ブログエントリの構造

ブログエントリは以下の場所に保存されます。

```
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

**重要**: 既存エントリのフロントマターは絶対に変更しないこと。

## よく使うコマンド

### 新規エントリの作成

```bash
npm run entry
```

blogsyncを使用して新しい下書きエントリを作成します。ファイルは `kiririmode.hatenablog.jp/entry/_draft/` に数字のファイル名で作成されます。

### Lint

```bash
npx textlint path/to/file.md   # 特定のファイルをリント
```

### 公開

```bash
blogsync push path/to/entry.md                  # 特定のエントリを公開
blogsync push kiririmode.hatenablog.jp/_draft/123456.md  # 下書きを公開
```

## コンテンツガイドライン

### 執筆の理念

このブログは、読者に価値を提供するための独自のボイスとスタイルを持つ。

- **平易で気取らない言葉** - 堅苦しい表現を避ける
- **論理的な流れ** - 論理を飛躍させず、つながりがわかる文章
- **十分な情報量** - 表面的ではない深い内容
- **箇条書きの最小化** - AI生成感を避けるため、散文を優先

### 記事構造

1. **タイトル**: 技術要素を「と」で接続し、目的や効果を動詞で終える（例:「TerraformとLambrollを組み合わせてXを実現する」）
2. **導入部**: 課題提起から入り、背景説明、解決策の概要を提示
3. **目次**: `[:contents]` ディレクティブを挿入
4. **本文**:
   - `#` を大きなセクションに、`##` をサブセクションに、`###` は必要な場合のみ使用
   - 流れ: 概要 → 技術詳細 → 実装例 → 考察
   - 各セクションの冒頭で要点を述べる
5. **まとめ**:「まとめ」または「最後に」という見出しで、箇条書きで重要ポイント整理、今後の展望、未解決の課題を記載。

### 技術コンテンツのパターン

**コードブロック**:

````markdown
```言語名
コード
```
````

**引用**:

```markdown
> 引用文
>
> <cite>[引用元タイトル](URL)</cite>
```

**埋め込み**:

```markdown
[https://url:embed]
```

**書籍**:

```markdown
ISBN:xxxxxxxxxxxxx:detail
```

### 文体パターン

- **事実**:「〜となります」（確定的）、「〜です」（基本的な説明）、「〜できます」（機能や可能性）
- **個人の見解**:「僕は〜と考えている」「〜だろう」「〜の可能性がある」
- **課題提起**:「〜という課題がある」「〜という問題に直面する」
- **解決策**:「〜することで解決できる」「〜というアプローチが考えられる」

### 品質基準

- 文の長さ: 最大200文字を推奨
- 冗長な表現を避ける:「できる」→「できる」「〜を行う」→「〜する」
- 助詞の重複を避ける（特に「が」「は」）
- **箇条書きを最小限に** - AI生成っぽさを避けるため
- 技術用語は初出時に定義
- コマンド出力は重要な部分を強調

## 自動品質チェック

### textlint設定

以下のルールを使用。

- `preset-ja-technical-writing`: 日本語技術文書の標準
- `preset-ja-spacing`: 日本語の空白ルール
- `spellcheck-tech-word`: 技術用語のスペルチェック
- `prh`: 用語の一貫性（`prh.yml` 参照）

`.textlintrc` でホワイトリスト例外が設定されています。

- スクラムマスター
- URLとLaTeX表現
- 特定の技術用語
- 数学表記

### pre-commitフック

`.pre-commit-config.yaml` により、コミット前にmarkdownファイルへのtextlintが自動実行されます。

## CI/CDワークフロー

### ブログ公開ワークフロー (`.github/workflows/blog.yml`)

- **トリガー**: `master` ブランチへのpushで `kiririmode.hatenablog.jp/entry/**.md` の変更があった場合
- **処理**:
  1. 100コミット深度でコードをチェックアウト
  2. Node.js 22をセットアップ
  3. blogsync v0.12.0をインストール
  4. `utils/post_blog.sh` を実行し、過去5日間のエントリを公開
- **認証**: はてなブログの `USERNAME` と `PASSWORD` シークレットを使用

### Textlintワークフロー (`.github/workflows/textlint.yml`)

- **トリガー**: プルリクエスト
- **処理**:
  1. 過去5日間のファイルにtextlintを実行
  2. reviewdogを使用してレビューコメントを投稿
  3. textlintエラーで失敗

## ユーティリティスクリプト

### `utils/post_blog.sh`

過去5日間のブログエントリを公開（`POST_TARGET_DAYS` で設定可能）。日付ディレクトリを反復処理し、blogsyncでmarkdownファイルをpushします。

### `utils/textlint.sh`

過去5日間のエントリにtextlintを実行（`LINT_TARGET_DAYS` で設定可能）し、reviewdog経由でPRレビュー用に結果を報告します。

### `scripts/check.sh`

最終公開時刻（`last_publish_time` ファイルで追跡）以降の変更されたエントリにtextlintを実行します。

### `scripts/publish.sh`

最終公開以降に変更されたエントリを公開し、`last_publish_time` を更新、タイムスタンプの更新をコミットします。

## blogsync連携

blogsyncははてなブログと同期するためのコアツールです。設定は `blogsync.yaml` にあります。

```yaml
kiririmode.hatenablog.jp:
  default:
    local_root: ./
```

認証には以下の環境変数を使用。

- `BLOGSYNC_USERNAME`
- `BLOGSYNC_PASSWORD`

## 記事カテゴリ

ブログは多様なトピックをカバーし、各カテゴリ固有のパターンがあります。

- **ソースコード解説**: 概要 → 処理の流れ → コード例 → 実装の意図 → まとめ
- **インフラ構築**: 課題設定 → アプローチ比較 → フェーズ別実装 → 検証 → 運用上の注意点
- **プログラミング**: 課題 → 実装アプローチ → コード例 → 実装ポイント → 注意点
- **ツール・製品レビュー**: 概要 → 選定理由 → 使用例 → メリット・デメリット → 今後の展望
- **日常・目標記事**: より親しみやすい口調、一人称視点

## ロールと視点

技術コンテンツを書く際は、その分野のプロフェッショナルや専門家のロールを採用してください。トピックに必要な専門性を考慮し、その視点から書きつつ、親しみやすく気取らないトーンを維持してください。
