# My-devin

**組み込みシステム開発特化 - ローカルLLM自動開発プラットフォーム**

Mac Studio上でQwen3-coderなどの大規模言語モデル(LLM)を活用し、**C++と組み込みシステム開発を中心とした**ソフトウェア開発を自動化・支援するプラットフォームです。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://isocpp.org/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FreeRTOS](https://img.shields.io/badge/RTOS-FreeRTOS-green.svg)](https://www.freertos.org/)

---

## 主な特徴

### 🔧 組み込み開発特化
- **C++主要対応**: MISRA C++, CERT C++準拠の安全なコード生成
- **RTOS完全対応**: FreeRTOS, Zephyr, Mbed OS, RIOT等
- **マイコン幅広くサポート**: STM32, ESP32, nRF52, RP2040等
- **ペリフェラル制御**: GPIO, UART, I2C, SPI, ADC, PWM, DMA
- **リアルタイム制約対応**: タスク管理、割り込み処理、メモリ最適化
- **低消費電力最適化**: スリープモード制御、電源管理

### 💻 一般機能
- **完全ローカル実行**: クラウドサービス不要、機密コードも安全
- **512GB RAM活用**: 超大規模モデル（32B-70B）を余裕で実行
- **マルチLLM対応**: LM Studio（推奨）, Ollama、MLX
- **多言語サポート**: C++, Python, TypeScript, Go, Rust等
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

### 1. LM Studioのインストール

```bash
# LM Studioをダウンロード＆インストール
# https://lmstudio.ai/ から最新版をダウンロード
# または Homebrew Cask経由
brew install --cask lm-studio
```

### 2. LM Studioでモデルをダウンロード

1. **LM Studioを起動**
2. **Search**タブで以下のモデルを検索＆ダウンロード：
   - `Qwen/Qwen2.5-Coder-32B-Instruct-GGUF` (推奨: Q4_K_M 量子化)
   - または `Qwen/Qwen2.5-Coder-14B-Instruct-GGUF` (軽量版)
   - または `deepseek-ai/DeepSeek-Coder-V2-Instruct-GGUF`

3. **Local Server**タブでモデルをロード
   - ポート: `1234`（デフォルト）
   - モデルを選択して「Start Server」

### 3. 開発ツールのインストール

```bash
# Homebrew（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 必須ツールのインストール
brew install python@3.11 node@20 git
```

### 4. プロジェクトのセットアップ

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

### 5. 起動

**ステップ1: LM Studioでサーバー起動**
- LM Studioを開く
- Local Serverタブで「Start Server」をクリック
- サーバーが http://localhost:1234 で起動

**ターミナル1: バックエンド**
```bash
cd backend
source venv/bin/activate
python -m uvicorn src.api.main:app --reload
```

**ターミナル2: フロントエンド**
```bash
cd frontend
npm run dev
```

**ターミナル3: CLI（対話モード）**
```bash
my-devin chat
```

---

## 使い方

### CLIコマンド

#### 組み込み開発（C++/RTOS）

```bash
# FreeRTOSタスク生成
my-devin generate \
  "FreeRTOSでLEDを点滅させるタスクを作成" \
  --language cpp \
  --rtos freertos \
  --target stm32f4

# UART通信コード生成
my-devin generate \
  "STM32F4のUART2で115200bpsでデータ送信" \
  --language cpp \
  --target stm32f4

# I2Cセンサー読み取り
my-devin generate \
  "ESP32でI2CからBME280センサーを読み取る" \
  --language cpp \
  --target esp32

# 割り込み処理生成
my-devin generate \
  "タイマー2の割り込みでFreeRTOSタスクに通知" \
  --language cpp \
  --rtos freertos

# 組み込み特化チャット
my-devin chat --mode embedded
```

#### 一般的な開発

```bash
# 対話型チャット
my-devin chat

# Pythonコード生成
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
- [ ] LLM基本統合（LM Studio）
- [ ] CLIベース機能
- [ ] 基本的なコード生成

### Phase 2: コア機能（6週間）
- [ ] マルチLLMバックエンド（Ollama、MLX）
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
  provider: lm-studio  # lm-studio, ollama, mlx
  default_model: qwen2.5-coder-32b-instruct

  # LM Studio設定
  lm_studio:
    base_url: http://localhost:1234/v1
    timeout: 300

api:
  host: 0.0.0.0
  port: 8000

project:
  workspace_dir: ./workspace
```

環境変数（`.env`）:
```bash
LLM_PROVIDER=lm-studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
DEFAULT_MODEL=qwen2.5-coder-32b-instruct
API_PORT=8000
```

---

## よくある質問（FAQ）

### Q: どのモデルを使うべきですか？

**512GB RAM環境の場合:**
- **推奨**: Qwen2.5-coder 32B（最高品質）
- **代替**: DeepSeek-Coder 33B
- **複数モデル同時ロード可能**

### Q: LM Studioとは？

GUI付きのLLM実行環境で、以下の特徴があります：
- **直感的なGUI**: モデルのダウンロード・管理が簡単
- **OpenAI互換API**: 標準的なAPI仕様で統合が容易
- **Mac最適化**: Apple Silicon向けに最適化
- **初心者に最適**: セットアップが簡単で、すぐに使い始められる

My-devinのデフォルトバックエンドです。

### Q: 他のLLMバックエンドは使えますか？

はい、以下もサポート予定です：
- **LM Studio**: GUI付き、初心者向け（推奨）
- **Ollama**: CLI志向、シンプル
- **MLX**: Apple Silicon最適化、最高速、上級者向け

設定ファイルで簡単に切り替え可能です。

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

### LM Studioのサーバーに接続できない

**原因と対処法:**
1. **LM Studioが起動していない**
   - LM Studioアプリを開き、Local Serverタブで「Start Server」をクリック

2. **ポートが異なる**
   - LM Studioのポート設定を確認（デフォルト: 1234）
   - `.env`ファイルの`LM_STUDIO_BASE_URL`を更新

3. **モデルがロードされていない**
   - LM StudioのLocal Serverタブでモデルを選択
   - 「Load Model」をクリック

### モデルのダウンロードが遅い
- LM Studio内でダウンロード速度を確認
- 量子化レベルを下げる（Q8 → Q4_K_M → Q4_0）
- 安定したWi-Fi/有線接続を使用

### メモリ不足エラー
- より小さいモデルを使用（32B → 14B → 7B）
- 量子化レベルを下げる（Q8 → Q4）
- 他のアプリケーションを終了
- `config/default.yaml`で`max_memory`を調整

### API接続エラー
```bash
# LM Studioサーバーが稼働中か確認
curl http://localhost:1234/v1/models

# 正常なレスポンス例:
# {"object":"list","data":[{"id":"qwen2.5-coder-32b-instruct",...}]}
```

---

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](./LICENSE) を参照してください。

---

## 関連リンク

### LLM実行環境
- **LM Studio**: https://lmstudio.ai/ (推奨LLM実行環境)
- **Qwen3-coder**: https://github.com/QwenLM/Qwen
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **Ollama**: https://ollama.ai/ (代替LLM実行環境)
- **MLX**: https://github.com/ml-explore/mlx

### 組み込み開発
- **FreeRTOS**: https://www.freertos.org/
- **Zephyr Project**: https://www.zephyrproject.org/
- **Mbed OS**: https://os.mbed.com/
- **RIOT OS**: https://www.riot-os.org/

### マイコン・開発環境
- **STM32**: https://www.st.com/en/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus.html
- **STM32CubeMX**: https://www.st.com/en/development-tools/stm32cubemx.html
- **ESP-IDF**: https://docs.espressif.com/projects/esp-idf/
- **Nordic nRF Connect SDK**: https://www.nordicsemi.com/Products/Development-software/nrf-connect-sdk
- **Raspberry Pi Pico SDK**: https://github.com/raspberrypi/pico-sdk

### C++リソース
- **MISRA C++**: https://www.misra.org.uk/
- **CERT C++ Coding Standard**: https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682
- **C++ Core Guidelines**: https://isocpp.github.io/CppCoreGuidelines/

### 開発ツール
- **ARM GCC Toolchain**: https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain
- **OpenOCD**: http://openocd.org/
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
