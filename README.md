# My-devin

**ローカルLLM自動開発プラットフォーム**

Mac Studio上でQwen3-coderなどの大規模言語モデル(LLM)を活用し、ソフトウェア開発を自動化・支援するプラットフォームです。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)

---

## 主な特徴

- **完全ローカル実行**: クラウドサービス不要、機密コードも安全
- **512GB RAM活用**: 超大規模モデル（32B-70B）を余裕で実行
- **マルチLLM対応**: Ollama、MLX、llama.cpp対応
- **多言語サポート**: Python、TypeScript、Go、Rust等に対応
- **エージェント型実行**: 複雑なタスクを自律的に実行
- **マルチインターフェース**: CLI、Web UI、VSCode拡張

---

## システム要件

### ハードウェア
- **Mac Studio** (Apple Silicon)
- **RAM**: 64GB以上（推奨: 128GB以上）
- **ストレージ**: 500GB以上の空き容量

### ソフトウェア
- **macOS**: 13.0 (Ventura) 以降
- **Python**: 3.11以上
- **Node.js**: 20以上
- **Git**: 2.30以上

---

## クイックスタート

### 1. 依存関係のインストール

```bash
# Homebrew（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 必須ツールのインストール
brew install python@3.11 node@20 git ollama

# Ollama起動
ollama serve
```

### 2. モデルのダウンロード

```bash
# Qwen3-coder 32Bモデル（推奨）
ollama pull qwen2.5-coder:32b

# または14Bモデル（軽量版）
ollama pull qwen2.5-coder:14b

# その他のモデル
ollama pull deepseek-coder:33b
ollama pull codellama:34b
```

### 3. プロジェクトのセットアップ

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/my-devin.git
cd my-devin

# バックエンドセットアップ
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# フロントエンドセットアップ
cd ../frontend
npm install

# CLIツールのインストール
cd ../cli
pip install -e .
```

### 4. 起動

**ターミナル1: Ollama（別ウィンドウで）**
```bash
ollama serve
```

**ターミナル2: バックエンド**
```bash
cd backend
source venv/bin/activate
python -m uvicorn src.api.main:app --reload
```

**ターミナル3: フロントエンド**
```bash
cd frontend
npm run dev
```

**ターミナル4: CLI（対話モード）**
```bash
my-devin chat
```

---

## 使い方

### CLIコマンド

```bash
# 対話型チャット
my-devin chat

# コード生成
my-devin generate "Pythonで二分探索アルゴリズムを実装" --language python

# プロジェクト解析
my-devin analyze ./my-project

# 設定確認
my-devin config show

# バージョン情報
my-devin --version
```

### Web UI

ブラウザで `http://localhost:3000` にアクセス

---

## プロジェクト構造

```
my-devin/
├── backend/           # Pythonバックエンド（FastAPI）
├── frontend/          # React + TypeScript Web UI
├── cli/               # CLIツール
├── vscode-extension/  # VSCode拡張（Phase 3）
├── config/            # 設定ファイル
├── docs/              # ドキュメント
└── scripts/           # ビルド・デプロイスクリプト
```

詳細は [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) を参照。

---

## 開発ロードマップ

### Phase 1: MVP（4週間） ✅ 進行中
- [x] プロジェクトセットアップ
- [x] 要件定義・実装計画作成
- [ ] LLM基本統合（Ollama）
- [ ] CLIベース機能
- [ ] 基本的なコード生成

### Phase 2: コア機能（6週間）
- [ ] マルチLLMバックエンド（MLX、llama.cpp）
- [ ] エージェント機能
- [ ] Web UI開発
- [ ] Git連携

### Phase 3: 高度機能（8週間）
- [ ] VSCode拡張
- [ ] プラグインシステム
- [ ] 高度なコード解析
- [ ] パフォーマンス最適化

### Phase 4: リリース（4週間）
- [ ] ドキュメント完成
- [ ] テスト・品質保証
- [ ] v1.0リリース

詳細は [REQUIREMENTS.md](./REQUIREMENTS.md) を参照。

---

## 設定

設定ファイル: `config/default.yaml`

```yaml
llm:
  provider: ollama
  default_model: qwen2.5-coder:32b

api:
  host: 0.0.0.0
  port: 8000

project:
  workspace_dir: ./workspace
```

環境変数（`.env`）:
```bash
LLM_PROVIDER=ollama
DEFAULT_MODEL=qwen2.5-coder:32b
API_PORT=8000
```

---

## よくある質問（FAQ）

### Q: どのモデルを使うべきですか？

**512GB RAM環境の場合:**
- **推奨**: Qwen2.5-coder 32B（最高品質）
- **代替**: DeepSeek-Coder 33B
- **複数モデル同時ロード可能**

### Q: Ollamaとは？

Mac向けに最適化されたLLM実行環境です。インストールと使用が簡単で、My-devinのデフォルトバックエンドです。

### Q: MLXとの違いは？

- **Ollama**: 簡単、初心者向け、すぐ使える
- **MLX**: Apple Silicon最適化、最高速、やや複雑

両方サポートしているので、切り替え可能です。

### Q: 商用利用可能ですか？

はい、MITライセンスです。ただし使用するモデルのライセンスを確認してください。

---

## 貢献

コントリビューションを歓迎します！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを作成

詳細は [CONTRIBUTING.md](./docs/CONTRIBUTING.md) を参照（作成予定）。

---

## トラブルシューティング

### Ollamaが起動しない
```bash
# Ollamaを再起動
brew services restart ollama

# または手動起動
ollama serve
```

### モデルのダウンロードが遅い
```bash
# 別のミラーを使用（中国リージョン等）
export OLLAMA_MIRRORS=https://ollama.ai
ollama pull qwen2.5-coder:32b
```

### メモリ不足エラー
- より小さいモデルを使用（7B/14B）
- 他のアプリケーションを終了
- `config/default.yaml`で`max_memory`を調整

---

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](./LICENSE) を参照してください。

---

## 関連リンク

- **Qwen3-coder**: https://github.com/QwenLM/Qwen
- **Ollama**: https://ollama.ai/
- **MLX**: https://github.com/ml-explore/mlx
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/

---

## サポート

- **Issue報告**: [GitHub Issues](https://github.com/yourusername/my-devin/issues)
- **ディスカッション**: [GitHub Discussions](https://github.com/yourusername/my-devin/discussions)
- **ドキュメント**: [docs/](./docs/)

---

## 謝辞

このプロジェクトは以下のオープンソースプロジェクトに感謝します：
- Qwen team
- Ollama team
- FastAPI
- React
- その他多数の素晴らしいOSSプロジェクト

---

**Made with ❤️ for developers who value privacy and performance**
