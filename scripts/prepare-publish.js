#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { Fotolife } = require('hatena-fotolife-api');

/**
 * YAMLフロントマターからDateフィールドを抽出してYYYYMMDD形式に変換
 * @param {string} content Markdownファイルの内容
 * @returns {string} YYYYMMDD形式の日付
 */
function extractDateFromFrontMatter(content) {
  const frontMatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontMatterMatch) {
    throw new Error('Front matter not found');
  }

  const frontMatter = frontMatterMatch[1];
  const dateMatch = frontMatter.match(/^Date:\s*(.+)$/m);
  if (!dateMatch) {
    throw new Error('Date field not found in front matter');
  }

  const dateStr = dateMatch[1];
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) {
    throw new Error(`Invalid date format: ${dateStr}`);
  }

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}${month}${day}`;
}

/**
 * PNG画像をはてなPhotolifeにアップロード
 * @param {string} imagePath PNG画像ファイルのパス
 * @param {string} title 画像のタイトル
 * @returns {Promise<string>} アップロードされた画像のURL
 */
async function uploadToFotolife(imagePath, title) {
  const username = process.env.HATENA_USERNAME;
  const apikey = process.env.HATENA_API_KEY;

  if (!username || !apikey) {
    throw new Error('HATENA_USERNAME and HATENA_API_KEY environment variables are required');
  }

  const client = new Fotolife({
    type: 'wsse',
    username: username,
    apikey: apikey
  });

  const imageBuffer = fs.readFileSync(imagePath);

  try {
    const response = await client.create({
      title: title,
      image: imageBuffer
    });

    // レスポンスから画像URLを抽出
    // hatena-fotolife-apiのレスポンスには画像URLが含まれている
    return response.imageurl || response['hatena:imageurl'];
  } catch (error) {
    throw new Error(`Failed to upload image to Fotolife: ${error.message}`);
  }
}

/**
 * mmdc変換後のローカル画像参照をはてなPhotolife URLに置換
 * @param {string} content mmdc変換後のMarkdownファイルの内容
 * @param {Array<string>} pngFiles 生成されたPNGファイル名の配列（ソート済み）
 * @param {string} tempDir 一時ディレクトリのパス
 * @returns {Promise<string>} 置換後のMarkdownコンテンツ
 */
async function replaceLocalImagesWithFotolife(content, pngFiles, tempDir) {
  if (pngFiles.length === 0) {
    console.log('No PNG images to upload');
    return content;
  }

  // 環境変数のチェック
  const username = process.env.HATENA_USERNAME;
  const apikey = process.env.HATENA_API_KEY;

  if (!username || !apikey) {
    console.warn('Warning: HATENA_USERNAME and HATENA_API_KEY not set. Skipping Fotolife upload.');
    console.warn('Local PNG references will remain as-is: ![diagram](./filename.png)');
    return content;
  }

  let updatedContent = content;

  // 各PNG画像をアップロードして置換
  for (let i = 0; i < pngFiles.length; i++) {
    const pngFile = pngFiles[i];
    const pngPath = path.join(tempDir, pngFile);

    // mmdc が生成する画像参照パターン: ![diagram](./filename.png)
    const localImagePattern = `![diagram](./${pngFile})`;

    console.log(`Uploading ${pngFile} to Hatena Fotolife...`);

    try {
      const imageUrl = await uploadToFotolife(pngPath, `diagram-${i}`);
      console.log(`Uploaded: ${imageUrl}`);

      // ローカル画像参照をFotolife URLに置換
      const imageMarkdown = `![diagram](${imageUrl})`;
      updatedContent = updatedContent.replace(localImagePattern, imageMarkdown);
    } catch (error) {
      console.error(`Failed to upload ${pngFile}: ${error.message}`);
      console.warn(`Keeping local reference for ${pngFile}`);
      // エラー時はローカル参照のまま継続
    }
  }

  return updatedContent;
}

/**
 * 下書きファイルを公開準備する
 * @param {string} draftFilePath 下書きMarkdownファイルのパス
 */
async function preparePublish(draftFilePath) {
  // ファイルの存在確認
  if (!fs.existsSync(draftFilePath)) {
    throw new Error(`File not found: ${draftFilePath}`);
  }

  // Markdownファイルの読み込み
  const content = fs.readFileSync(draftFilePath, 'utf8');

  // 日付の抽出
  const yyyymmdd = extractDateFromFrontMatter(content);

  // ファイル名の取得
  const fileName = path.basename(draftFilePath);

  // 目的ディレクトリのパス
  const targetDir = path.join(
    path.dirname(path.dirname(draftFilePath)), // entry/
    yyyymmdd
  );

  // 目的ディレクトリの作成
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
    console.log(`Created directory: ${targetDir}`);
  }

  // 目的ファイルのパス
  const targetFilePath = path.join(targetDir, fileName);

  // 一時ディレクトリの作成
  const tempDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'mermaid-'));
  const tempFilePath = path.join(tempDir, fileName);

  try {
    // 一時ファイルにコピー
    fs.copyFileSync(draftFilePath, tempFilePath);

    // mermaid-cliでMermaid図をPNG化
    console.log('Converting Mermaid diagrams to PNG...');
    try {
      execSync(
        `npx -y mmdc -i "${tempFilePath}" -o "${tempFilePath}" -e png -p puppeteer-config.json`,
        { stdio: 'inherit' }
      );
    } catch (error) {
      // エラーメッセージからPuppeteer設定エラーなど致命的なエラーを検出
      const errorMessage = error.message || '';
      const isFatalError =
        errorMessage.includes('executablePath') ||
        errorMessage.includes('Browser was not found') ||
        errorMessage.includes('Failed to launch');

      if (isFatalError) {
        // 致命的なエラーの場合は処理を中断
        throw new Error(`Fatal error during Mermaid conversion: ${errorMessage}`);
      }

      // Mermaid図がない場合など軽微なエラーは無視
      console.warn('Warning: mermaid-cli execution failed or no Mermaid diagrams found');
    }

    // 生成されたPNG画像を確認
    const tempDirFiles = fs.readdirSync(tempDir);
    const pngFiles = tempDirFiles.filter(f => f.endsWith('.png')).sort();

    // PNG画像が生成されている場合、ローカル画像参照をFotolife URLに置換
    if (pngFiles.length > 0) {
      console.log(`Found ${pngFiles.length} PNG file(s), uploading to Hatena Fotolife...`);
      const tempFileContent = fs.readFileSync(tempFilePath, 'utf8');
      const updatedContent = await replaceLocalImagesWithFotolife(tempFileContent, pngFiles, tempDir);
      fs.writeFileSync(tempFilePath, updatedContent, 'utf8');
      console.log('Image references updated');
    }

    // 変換後のMarkdownを目的ディレクトリにコピー
    fs.copyFileSync(tempFilePath, targetFilePath);
    console.log(`Copied: ${targetFilePath}`);

    for (const pngFile of pngFiles) {
      const srcPng = path.join(tempDir, pngFile);
      const destPng = path.join(targetDir, pngFile);
      fs.copyFileSync(srcPng, destPng);
      console.log(`Copied image: ${destPng}`);
    }

    // 元の下書きファイルを削除
    fs.unlinkSync(draftFilePath);
    console.log(`Deleted draft: ${draftFilePath}`);

    console.log('\nPublish preparation completed!');
    console.log(`Target file: ${targetFilePath}`);
    console.log(`\nYou can now publish with:`);
    console.log(`  blogsync push ${targetFilePath}`);
  } finally {
    // 一時ディレクトリのクリーンアップ
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}

// メイン処理
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node scripts/prepare-publish.js <draft-file-path>');
    console.error('Example: node scripts/prepare-publish.js kiririmode.hatenablog.jp/entry/_draft/1234567890.md');
    process.exit(1);
  }

  const draftFilePath = args[0];

  preparePublish(draftFilePath)
    .then(() => {
      process.exit(0);
    })
    .catch(error => {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    });
}

module.exports = { preparePublish, extractDateFromFrontMatter };
