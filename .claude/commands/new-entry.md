---
allowed-tools: Read, Bash(ls:*), 
description: 
---

このコマンドは、品質が担保された、新しいBlogエントリを作成するものです。

# 実行手順

ブログエントリを作成するには、以下のステップを実行します。

1. ブログエントリの内容を計画する
   指示された内容のエントリの作成計画をPlanエージェントを使って策定する。
   コンテンツガイドラインdocs/contents-guideline.mdの内容に従うこと。

2. 新規エントリの作成: 以下のコマンドで、blogsyncを使用して新しい下書きエントリのファイルを作成する。
   ファイルは `kiririmode.hatenablog.jp/entry/_draft/` に数字のファイル名で作成される。
   本ファイルに、上記で計画したエントリを記述する。

   ```bash
   npm run entry
   ```

3. docs/contents-guideline.mdに従っているかをレビューし、問題があれば修正する。
   特に、エントリ全体のリズム、および、ユニークさがあるかに留意すること。

4. lintをかけ、エラーがあった場合は修正する。そのサイクルを、エラーが0になるまで繰り返す。

   ```bash
   npm run lint path/to/file.md
   ```

5. 下書きエントリファイルのFrontMatterにおけるDateフィールドを、現在時刻（JST）に置き換える

6. 変更をコミットする

   ```bash
   /commit
   ```
