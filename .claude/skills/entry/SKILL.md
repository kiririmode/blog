---
name: create-entry
allowed-tools: Read, Bash(ls:*), 
description: Blogエントリを作成する
---

# Your Skill Name

このSKILLは、読者が惹きつけられる、魅力的なブログエントリを作成するためのもの。

# Instructions

ブログエントリを作成するには、以下のステップを実行する。

1. 新規エントリの作成: 以下のコマンドで、blogsyncを使用して新しい下書きエントリのファイルを作成する。
   ファイルは `kiririmode.hatenablog.jp/entry/_draft/` に数字のファイル名で作成される。

   ```bash
   npm run entry
   ```

2. ブログエントリの構造を作成する:
   上記で作成した下書きエントリのファイルに対して、指示された内容のエントリの構造をPlanエージェントを使って策定する。
   構造ガイドライン `references/structure-guideline.md` の内容に従うこと。
3. タイトルを決める:
   タイトルガイドライン `references/title-guildeline.md` に従ってタイトルを検討し、下書きエントリのFront Matter部に記載すること。
4. 文体を鑑みて、エントリのBODYを記述する
   コンテンツガイドライン `references/contents-guideline.md` に従って、
   特にエントリ全体のリズムとユニークさがあるかに留意すること。
5. lintをかけ、エラーがあった場合は修正する。そのサイクルを、エラーが0になるまで繰り返す。

   ```bash
   npm run lint path/to/file.md
   ```

6. 下書きエントリファイルのFrontMatterにおけるDateフィールドを、現在時刻（JST）に置き換える
7. 変更をコミットする

   ```bash
   /commit
   ```
