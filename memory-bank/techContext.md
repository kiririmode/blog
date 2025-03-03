# 技術コンテキスト

## 開発環境

### 基本環境

- OS: Linux
- シェル: bash
- Node.js環境

### 開発ツール

- Visual Studio Code
- Git（バージョン管理）
- Make（タスク自動化）

## 主要技術スタック

### コンテンツ管理

- Markdown: 記事の作成
- YAML: メタデータ管理
- blogsync: Hatena Blogとの同期

### 品質管理ツール

- textlint: 文章校正ツール
  - プリセット: textlint-rule-preset-japanese
  - カスタムルール設定
- prh: 表記ゆれ対策
  - カスタム辞書による一貫性の確保

### 自動化ツール

- シェルスクリプト
  - 記事の公開プロセス
  - 品質チェック
  - ユーティリティ機能
- Makefile
  - タスクの定義
  - ビルドプロセスの自動化

### AI関連

- OpenAI API
  - 記事生成支援
  - 編集支援
  - SEO最適化

## 依存関係

### npm パッケージ

- textlint関連パッケージ
- blogsync
- その他開発依存パッケージ

### 設定ファイル

- .textlintrc: テキスト校正設定
- prh.yml: 表記ゆれルール
- blogsync.yaml: ブログ同期設定
- package.json: npm設定
- Makefile: タスク定義

## 制約事項

### 技術的制約

- Hatena Blog APIの制限
- textlintルールの制約
- デプロイメントの制限

### 運用上の制約

- 記事フォーマットの要件
- 公開プロセスの制約
- バージョン管理の要件
