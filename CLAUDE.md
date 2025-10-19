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

### 公開準備と公開フロー

ブログエントリを公開するには、以下のステップを実行します。

#### 下書きを公開準備する

```bash
npm run prepare-publish kiririmode.hatenablog.jp/entry/_draft/123456.md
```

このコマンドは以下を自動実行します。

- Mermaid図をPNG画像に変換
- PNG画像をはてなPhotolifeにアップロード
- Markdown内のMermaid codeblock記述を画像URL(`![](https://...)`)に置換
- PNG画像をローカルにも保存（バックアップ）
- ファイルを `kiririmode.hatenablog.jp/entry/YYYYMMDD/` ディレクトリに移動
- 元の下書きファイルを削除

**必要な環境変数**:

- `HATENA_USERNAME`: はてなID
- `HATENA_API_KEY`: はてなのAtomPub APIキー（[https://blog.hatena.ne.jp/my/config](https://blog.hatena.ne.jp/my/config)から取得）

#### 変更をコミット・プッシュ

```bash
git add kiririmode.hatenablog.jp/entry/YYYYMMDD/
git commit -m "記事を公開準備"
git push origin master
```

#### 自動公開

GitHub Actionsが自動的に以下を実行します。

- textlintによる品質チェック
- markdownlintによる構文チェック
- blogsyncによるはてなブログへの公開

**重要**: `_draft/` 配下のファイルを直接コミット・プッシュしても公開されません。必ず `npm run prepare-publish` を実行してください。

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

- **トリガー**: `master` ブランチへのpushで `kiririmode.hatenablog.jp/entry/YYYYMMDD/*.md` の変更があった場合
- **処理**:
  1. 変更されたMarkdownファイルを検出（`YYYYMMDD/` 配下のみ）
  2. Node.js 22をセットアップし、依存関係をインストール
  3. 変更されたファイルに対してtextlintとmarkdownlintを実行
  4. blogsync v0.12.0をインストール
  5. Lintが成功した場合のみ、変更されたエントリを公開
- **認証**: はてなブログの `USERNAME` と `PASSWORD` シークレットを使用

**注意**: `_draft/` 配下のファイルはCI/CDワークフローのトリガー対象外です。必ずローカルで `npm run prepare-publish` を実行してから公開してください。

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
