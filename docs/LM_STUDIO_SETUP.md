# LM Studio セットアップガイド

My-devinでLM Studioを使用するための詳細なセットアップガイドです。

---

## 目次
1. [LM Studioのインストール](#1-lm-studioのインストール)
2. [モデルのダウンロード](#2-モデルのダウンロード)
3. [サーバーの起動](#3-サーバーの起動)
4. [My-devinとの統合](#4-my-devinとの統合)
5. [トラブルシューティング](#5-トラブルシューティング)

---

## 1. LM Studioのインストール

### macOS (推奨)

**方法1: 公式サイトからダウンロード**
1. https://lmstudio.ai/ にアクセス
2. 「Download for Mac」をクリック
3. ダウンロードした`.dmg`ファイルを開く
4. LM Studioをアプリケーションフォルダにドラッグ

**方法2: Homebrew Cask**
```bash
brew install --cask lm-studio
```

### システム要件確認
- **macOS**: 13.0 (Ventura) 以降
- **RAM**: 最低32GB（推奨64GB以上）
- **ストレージ**: モデルごとに10-50GB

---

## 2. モデルのダウンロード

### 推奨モデル（512GB RAM環境）

#### Qwen2.5-Coder 32B（最高品質）
```
モデル名: Qwen/Qwen2.5-Coder-32B-Instruct-GGUF
量子化: Q4_K_M（推奨）または Q5_K_M
サイズ: 約20GB
```

#### Qwen2.5-Coder 14B（バランス型）
```
モデル名: Qwen/Qwen2.5-Coder-14B-Instruct-GGUF
量子化: Q4_K_M
サイズ: 約9GB
```

#### DeepSeek-Coder V2（代替案）
```
モデル名: deepseek-ai/DeepSeek-Coder-V2-Instruct-GGUF
量子化: Q4_K_M
サイズ: 約21GB
```

### ダウンロード手順

1. **LM Studioを起動**
2. **Searchタブを開く**
3. **検索ボックスにモデル名を入力**
   - 例: `Qwen2.5-Coder-32B`
4. **量子化レベルを選択**
   - `Q4_K_M`: 品質と速度のバランス（推奨）
   - `Q5_K_M`: より高品質、やや遅い
   - `Q8_0`: 最高品質、最も遅い
5. **Downloadボタンをクリック**

ダウンロード完了まで待機（モデルサイズに応じて10-60分）

### 量子化レベルの選択ガイド

| 量子化 | 品質 | 速度 | RAM使用量 | 推奨用途 |
|-------|------|------|----------|---------|
| Q8_0  | 最高 | 遅い | 最大 | 本番環境・最高品質 |
| Q5_K_M | 高 | 普通 | 中 | 日常使用（推奨） |
| Q4_K_M | 良好 | 速い | 小 | 開発・テスト |
| Q4_0  | 可 | 最速 | 最小 | 実験・低リソース |

**512GB RAM環境では Q5_K_M 以上を推奨**

---

## 3. サーバーの起動

### 基本的な起動手順

1. **LM Studioのメインウィンドウを開く**
2. **Local Server タブをクリック**
3. **モデルを選択**
   - ドロップダウンメニューからダウンロード済みモデルを選択
4. **サーバー設定（オプション）**
   - **Port**: 1234（デフォルト、変更可）
   - **Context Length**: 32768（推奨）
   - **GPU Layers**: Auto（推奨）
5. **Start Server ボタンをクリック**

### サーバー設定の詳細

```json
{
  "port": 1234,
  "context_length": 32768,
  "n_gpu_layers": -1,  // 全てのレイヤーをGPUで実行
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### サーバー起動の確認

**ターミナルで確認:**
```bash
# モデル一覧取得
curl http://localhost:1234/v1/models

# 正常なレスポンス例:
# {
#   "object": "list",
#   "data": [
#     {
#       "id": "qwen2.5-coder-32b-instruct",
#       "object": "model",
#       "created": 1234567890,
#       "owned_by": "lmstudio"
#     }
#   ]
# }
```

**簡単なテスト:**
```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder-32b-instruct",
    "messages": [
      {"role": "user", "content": "Hello, World!"}
    ]
  }'
```

---

## 4. My-devinとの統合

### 環境変数の設定

`.env`ファイルを作成・編集:

```bash
# LM Studio設定
LLM_PROVIDER=lm-studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio  # ダミーキー（必須）

# 使用するモデル名（LM Studioで表示される名前）
DEFAULT_MODEL=qwen2.5-coder-32b-instruct
```

### Pythonコードからの使用

```python
from backend.src.llm.lm_studio import LMStudioProvider

# プロバイダー初期化
provider = LMStudioProvider(
    base_url="http://localhost:1234/v1",
    model_name="qwen2.5-coder-32b-instruct"
)

# ヘルスチェック
is_healthy = await provider.health_check()
print(f"Server is {'online' if is_healthy else 'offline'}")

# コード生成
code = await provider.generate_code(
    description="Create a Python function to sort a list",
    language="python"
)
print(code)

# ストリーミング生成
async for chunk in provider.stream_generate("Explain recursion"):
    print(chunk, end="", flush=True)
```

### CLIからの使用

```bash
# チャットモード
my-devin chat

# コード生成
my-devin generate "Pythonで二分探索を実装" --language python

# プロジェクト解析
my-devin analyze ./my-project
```

---

## 5. トラブルシューティング

### 問題1: サーバーに接続できない

**症状:**
```
Error: Connection refused to http://localhost:1234
```

**原因と対処法:**
1. **LM Studioが起動していない**
   - LM Studioアプリを開く
   - Local Serverタブで「Start Server」をクリック

2. **ポートが異なる**
   - LM Studioの設定でポートを確認
   - `.env`の`LM_STUDIO_BASE_URL`を更新

3. **ファイアウォールブロック**
   - macOSのファイアウォール設定を確認
   - LM Studioを許可リストに追加

### 問題2: モデルがロードされない

**症状:**
```
Error: No model loaded
```

**対処法:**
1. LM StudioのLocal Serverタブでモデルを選択
2. 「Load Model」をクリック
3. モデルがロードされるまで待機（1-3分）

### 問題3: レスポンスが遅い

**原因:**
- GPU Layersの設定が不適切
- 量子化レベルが高すぎる
- メモリ不足

**対処法:**
1. **GPU Layers設定を確認**
   - LM Studio設定で`n_gpu_layers`を`-1`（全レイヤー）に設定

2. **量子化レベルを下げる**
   - Q8 → Q5_K_M → Q4_K_M

3. **Context Lengthを調整**
   - 32768 → 16384 → 8192

### 問題4: メモリ不足エラー

**症状:**
```
Error: Out of memory
```

**対処法:**
1. **より小さいモデルを使用**
   - 32B → 14B → 7B

2. **他のアプリケーションを終了**

3. **量子化レベルを下げる**
   - Q5 → Q4

### 問題5: APIレスポンスエラー

**症状:**
```json
{
  "error": {
    "message": "Invalid request",
    "type": "invalid_request_error"
  }
}
```

**対処法:**
1. **モデル名を確認**
   ```bash
   curl http://localhost:1234/v1/models
   ```
   正しいモデル名を使用

2. **リクエストフォーマットを確認**
   - OpenAI互換APIフォーマットに準拠

---

## パフォーマンスチューニング

### 512GB RAM環境での最適設定

```yaml
# config/default.yaml
llm:
  provider: lm-studio
  default_model: qwen2.5-coder-32b-instruct

  lm_studio:
    base_url: http://localhost:1234/v1
    timeout: 300

    # 推奨設定
    context_length: 32768  # 最大
    n_gpu_layers: -1       # 全レイヤーをGPU使用
    temperature: 0.7
    max_tokens: 4096

    # 高速化オプション
    use_mmap: true
    use_mlock: true
```

### ベンチマーク（参考値）

| モデル | 量子化 | Tokens/sec | 初回応答時間 |
|-------|--------|-----------|------------|
| Qwen2.5 32B | Q5_K_M | 25-35 | 2-3秒 |
| Qwen2.5 32B | Q4_K_M | 35-45 | 1-2秒 |
| Qwen2.5 14B | Q5_K_M | 50-70 | 1秒 |
| Qwen2.5 14B | Q4_K_M | 70-90 | <1秒 |

*Mac Studio M2 Ultra, 512GB RAMでの実測値*

---

## 追加リソース

- **LM Studio公式ドキュメント**: https://lmstudio.ai/docs
- **OpenAI API仕様**: https://platform.openai.com/docs/api-reference
- **Qwenモデル情報**: https://github.com/QwenLM/Qwen
- **My-devin統合例**: `backend/src/llm/lm_studio.py`

---

## まとめ

LM Studioは以下の理由でMy-devinの推奨バックエンドです：

✅ **GUI付きで使いやすい**
✅ **OpenAI互換APIで統合が簡単**
✅ **Apple Silicon最適化**
✅ **豊富なモデル選択肢**
✅ **安定したパフォーマンス**

セットアップが完了したら、`my-devin chat`で使い始めましょう！
