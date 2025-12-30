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

#### 変更をコミット・プッシュ

```bash
git add kiririmode.hatenablog.jp/entry/YYYYMMDD/
git commit -m "hogehoge" （conventional commitとしてください）
# PR を作成
```

#### 自動公開

GitHub Actionsがtextlint、markdownlintによる品質チェックを行い、問題なければblogsyncによるはてなブログへ公開します。

注意: `_draft/` 配下のファイルを直接コミット・プッシュしても公開されません。必ず `npm run prepare-publish` を実行してください。

## コンテンツガイドライン

### 執筆の理念

このブログは、読者に価値を提供するための独自のボイスとスタイルを持つ。

- **リズムとテンポ** - 読みやすく心地よい躍動感のある文章の流れ
- **知的なウィットとユーモア** - 言葉遊び、パラドックス、皮肉な観察、そしてユーモアとウィットを適度に織り込む
- **温かみのあるトーン** - 知的でありながらも親しみやすさを持つこと
- **自然な表現** - 狙いすぎや偉そうな言い回しを避ける
- **平易で気取らない言葉** - 堅苦しい表現を避け、親しみやすく
- **論理的な構成** - 飛躍せず、つながりが明確な展開
- **散文優先** - AI生成感を避けるため箇条書きを最小化
- **十分な深さ** - 表面的でない、価値ある情報量

### 文体

- ですます調で記述する
- 事実と想像は分ける。
  - 事実:「〜となります」（確定的）、「〜です」（基本的な説明）、「〜できます」（機能や可能性）
  - 個人の見解:「僕は〜と考えています」「〜だと思います」

### 記事構造

1. **タイトル**: 内容が一目で理解でき、読者が思わず読みたくなる訴求力のあるものにする
   - 扱う技術や課題を具体的に明示する
   - 読者が得られる価値や解決策を示す
   - 読者の「知りたい」「解決したい」という欲求を刺激する
   - 数字、具体的な成果、意外性などで訴求力を高める
   - 例:「GoのGoroutineで並行処理を10倍高速化した話」「terraformで見落としがちな3つのセキュリティリスク」
2. **導入部**: 課題提起から入り、背景説明、解決策の概要を提示
3. **目次**: `[:contents]` ディレクティブを挿入
4. **本文**:
   - `#` を大きなセクションに、`##` をサブセクションに、`###` は必要な場合のみ使用
   - 流れ: 概観 → 課題・背景 → 詳細(ここは記事内容に依存) → まとめ
5. **まとめ**: 重要ポイントを整理し記載

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

埋め込みURLの記述は以下のようにします。

```markdown
[https://url:embed]
```

### 品質基準

- 文の長さ: 最大200文字を推奨
- 冗長な表現を避ける:「できる」→「できる」「〜を行う」→「〜する」
- 助詞の重複を避ける（特に「が」「は」）
- **箇条書きを最小限に** - AI生成っぽさを避けるため
- 技術用語は初出時に定義
- コマンド出力は重要な部分を強調
