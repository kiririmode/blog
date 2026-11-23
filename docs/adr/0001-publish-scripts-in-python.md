# 公開ワークフローのスクリプトを Python の標準ライブラリで書く

公開準備はJavaScript、画像のアップロードはPythonで書かれており、フォトライフへのアップロード処理が2か所に重複していた。縮小版URLを元の大きさのURLに直す修正も、2か所に必要だった。そこで、公開ワークフローのスクリプトをPythonに揃え、フォトライフへのアップロードを1つのモジュールにまとめる。画像のアップロードは、既にPythonの標準ライブラリだけで書かれている。公開準備をPythonに移せば、npmの依存（hatena-fotolife-api）も1つ減る。テストも標準ライブラリのunittestで書き、追加の依存を入れない。

## Consequences

npmは、textlint、markdownlint、mermaid-cliを動かすためだけに残る。`npm run prepare-publish`と`npm run upload-images`は名前と引数を変えず、Pythonのスクリプトを呼ぶ。
