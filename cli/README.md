# My-devin CLI

コマンドラインインターフェース

## インストール

```bash
cd cli
pip install -e .
```

## 使い方

```bash
# 対話型チャット
my-devin chat

# コード生成
my-devin generate "Pythonで二分探索を実装" --language python

# プロジェクト解析
my-devin analyze ./my-project

# ヘルプ
my-devin --help
```

## コマンド一覧

- `chat`: 対話型チャットモード
- `generate`: コード生成
- `analyze`: プロジェクト解析
- `config`: 設定管理
