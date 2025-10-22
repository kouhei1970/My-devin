# クイックスタートガイド

My-devinを今すぐ使い始めるためのガイドです。

---

## 前提条件

✅ LM Studioがインストール済み
✅ Qwen2.5-Coder 32Bモデルをダウンロード済み
✅ LM Studioサーバーが起動中（http://localhost:1234）

---

## 1. セットアップ（初回のみ）

### バックエンドのセットアップ

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### CLIツールのインストール

```bash
cd cli
pip install -e .
```

### 確認

```bash
my-devin --help
```

---

## 2. 基本的な使い方

### 対話モード（チャット）

```bash
# 一般的なチャット
my-devin chat

# 組み込み開発モード
my-devin chat --mode embedded
```

**対話例:**
```
You: FreeRTOSでLEDを点滅させるタスクを作って