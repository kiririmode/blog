# kiririmode.hatenablog.jp の執筆と公開

このリポジトリは、はてなブログkiririmode.hatenablog.jpのエントリをMarkdownで管理し、下書きから公開までを扱う。

## エントリと置き場

**エントリ**:
はてなブログに載る1本の文章と、それを書いたMarkdownファイル。
_Avoid_: 記事、ポスト、投稿

**entry_id**:
はてなブログがエントリに振る数字のID。エントリのファイル名と、付属ファイルの名前の先頭に使う。
_Avoid_: 記事ID、ポストID

**front matter**:
エントリの先頭にあるYAMLの部分。Title、Category、Date、URL、EditURLなどを持つ。
_Avoid_: ヘッダ、メタデータ

**下書き**:
まだ公開されていないエントリ。front matterに`Draft: true`を持ち、下書き置き場にある。
_Avoid_: ドラフト（`_draft`や`Draft`のような識別子では可）、未公開記事

**下書き置き場**:
下書きと、その付属ファイルを置くディレクトリ`kiririmode.hatenablog.jp/entry/_draft/`。

**公開済みエントリ**:
公開日のディレクトリ`kiririmode.hatenablog.jp/entry/YYYYMMDD/`にあるエントリ。
_Avoid_: 既存記事、本番記事

**付属ファイル**:
下書き置き場にある、名前が`<entry_id>-`で始まるファイル。構成図のSVGやPNGなど、そのエントリのための素材である。
_Avoid_: 添付ファイル、素材ファイル

## 公開の流れ

**公開準備**:
下書きを公開済みエントリの形に変える作業。front matterの更新、Mermaid図の画像化、公開日のディレクトリへの移動を含む。
_Avoid_: 公開処理、リリース準備

**公開**:
公開済みエントリがmainにマージされ、はてなブログに反映されること。
_Avoid_: デプロイ、投稿

## 画像

**フォトライフ**:
はてなの画像置き場「はてなフォトライフ」。エントリに載せる画像は、ここにアップロードしてURLで参照する。
_Avoid_: Photolife、Fotolife（コードの識別子では可）

**ローカルの画像参照**:
エントリの本文にある、URLではなくファイルのパスを指す画像参照（`![alt](./x.svg)`など）。フェンスで囲んだコードブロックの中のものは、Markdownの書き方の例なので含まない。

**縮小版 URL**:
フォトライフが返す、横幅450pxに縮小した画像のURL。
_Avoid_: サムネイルURL

**元の大きさの URL**:
フォトライフの画像を元の大きさで指すURL。縮小版URLの拡張子の前に`_original`を付けた形である。
_Avoid_: オリジナルURL、原寸URL
