#!/bin/bash
#
# Claude Code のインストールとプラグイン設定
#

set -euo pipefail

# Claude Code のインストール
if ! command -v claude &> /dev/null; then
    echo "Installing Claude Code..."
    curl -fsSL https://claude.ai/install.sh | bash
fi

echo "Claude Code setup complete!"
