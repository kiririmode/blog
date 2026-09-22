---
name: create-entry
description: Blogエントリを作成する
---

# Create-Entry Skill

このSKILLは、読者が惹きつけられる、魅力的なブログエントリを作成するためのもの。

# Instructions

ブログエントリを作成するには、以下のステップを実行する。

1. 新規エントリの作成: 以下のコマンドで新しい下書きエントリのファイルを作成する。
   ファイルは `kiririmode.hatenablog.jp/entry/_draft/` にepoch timeを示すファイル名で作成される。

   ```bash
   npm run entry
   ```

2. インタビューによるテーマの深掘り:
   `/grilling` を起動し、`references/interview-axes.md` の6軸に沿って一問一答でテーマを深掘りする。質問は1問ずつ、各問いに推奨回答を添えて提示し、ユーザーの回答を待ってから次に進む。

   「出発点」の問いでは、`references/contents-guideline.md` の「記事のモード」を参照し、回答がエッセイ型・分析型のどちらに近いかをその場で判断してユーザーに確認する。ここでモードを確定し、以降のステップで改めてモード提案は行わない。
   エッセイ型に確定した場合は `references/essay-mode-example.md` の模範例を通読し、リズム・口語表現・呼びかけ方を把握しておく。

   6軸すべてで認識の齟齬がなくなった時点でインタビューを終了する。

3. natural-japanese skillの読み込み:
   `~/.claude/skills/natural-japanese/SKILL.md` と `~/.claude/skills/natural-japanese/references/writing-constitution.md` を読み込み、文体憲法12箇条（結論から書く、見出しはメッセージ、箇条書きは真の並列のときだけ、専門用語は機能→名前の順、固有名詞・数値で接地、太字は核1箇所、濃淡をつける、同じ鋳型を繰り返さない等）を把握する。エッセイ型・分析型のどちらのモードでも読み込む。

   以降のステップ（構造プラン作成・BODY記述）は、この文体憲法を土台としつつ、`references/contents-guideline.md` のブログ固有ルール（エッセイ型の口語表現・二人称呼びかけ等）を優先する。両者が矛盾する場合は `references/contents-guideline.md` を優先する。natural-japanese側に本文の執筆自体を委ねることはしない。

4. ブログエントリの構造を作成する:
   下書きエントリファイルに対して、Plan Agentを使い、ステップ2で確定したモードとインタビューの結論、ステップ3で把握した文体憲法を踏まえた具体的なエントリを記述する計画を作成する。

   構造は次のとおりとすること。
   1. **導入部**: 課題提起から入り、背景説明、解決策の概要を提示
   2. **目次**: `[:contents]` ディレクティブを挿入
   3. **本文**:
      - `#` を大きなセクションに、`##` をサブセクションに、`###` は必要な場合のみ使用
   4. **最後に**: まとめを記述する
   テンポ・ウィットの方針は `references/voice-examples.md` を参照すること。

5. タイトルを決める:
   タイトルガイドライン `references/title-guideline.md` に従ってタイトルを検討し、下書きエントリのFront Matter部に記載すること。

6. 文体を鑑みて、エントリのBODYを記述する
   コンテンツガイドライン `references/contents-guideline.md` に従って記述する。

7. natural-japaneseによる品質診断と改善ループ:
   `/natural-japanese` を `score exp` モードで呼び出し、下書きエントリファイルを診断する（書き換えは行わず、lint・構造レビュー・読みやすさレビュー・semantic.pyによる深層検出の指摘を得る）。初回実行時はsemantic.pyの依存解決とモデルダウンロード（~1GB、cl-nagoya/ruri-v3-310m）が走ることがある。

   ```text
   /natural-japanese score exp kiririmode.hatenablog.jp/entry/_draft/<file>.md
   ```

   得られた指摘は `references/contents-guideline.md` を優先する立場で一つずつ「直す/直さない」を判断する。直した場合は該当箇所を修正し、新規の指摘が出なくなるまで「診断→修正→再診断」を繰り返す。同一の指摘が2周連続で再発する場合はそれ以上直さず、判断を確定させて次に進む。

   収束したら、`~/.claude/skills/natural-japanese/references/eval-rubric.md` の6軸ルーブリック（脱AI臭・文体の自然さ、情報密度・簡潔さ、機能性・走査性、論理の明晰性と納得感、人間味・誠実さ、自己証明力）で自己評価し、全軸90点以上・総合平均92点以上を目安に改稿する。ただし、スコアの低さがエッセイ型固有の口語表現・二人称呼びかけ等、`references/contents-guideline.md` が意図的に定める要素に起因する場合は、スコアのために文体を機械的に均さず `references/contents-guideline.md` を優先する。

   診断・判断台帳・lintのJSON出力等の中間ファイルは作業用のみとし、コミット対象には含めない。

   このSKILLは textlint（`npm run lint`）は実行しない。

8. テンポ・ウィットチェックを行う
   ステップ7のnatural-japanese診断を終えたのち、最後にこのブログ固有のテンポ・ウィットチェックを行う。書いたBODYを通読し、`references/voice-examples.md` の避けるべきパターン表・テクニック集に該当する箇所がないか確認する。問題があれば書き直す。エッセイ型の場合は、テクニック7〜9（口語化・二人称呼びかけ・問いかけリズム）も確認する。

9. 下書きエントリファイルのFrontMatterにおけるDateフィールドを、現在時刻（JST）に置き換える
10. 変更をコミットする

    ```bash
    /commit
    ```
