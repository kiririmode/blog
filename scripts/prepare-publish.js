#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

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
 * 下書きファイルを公開準備する
 * @param {string} draftFilePath 下書きMarkdownファイルのパス
 */
function preparePublish(draftFilePath) {
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
      console.warn('Warning: mermaid-cli execution failed or no Mermaid diagrams found');
      // Mermaid図がない場合もエラーとしない
    }

    // 変換後のMarkdownを目的ディレクトリにコピー
    fs.copyFileSync(tempFilePath, targetFilePath);
    console.log(`Copied: ${targetFilePath}`);

    // 生成されたPNG画像を目的ディレクトリにコピー
    const tempDirFiles = fs.readdirSync(tempDir);
    const pngFiles = tempDirFiles.filter(f => f.endsWith('.png'));

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

  try {
    preparePublish(draftFilePath);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { preparePublish, extractDateFromFrontMatter };
