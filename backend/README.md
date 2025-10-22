# My-devin Backend

FastAPIベースのバックエンドサーバー

## セットアップ

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## 開発サーバー起動

```bash
python -m uvicorn src.api.main:app --reload
```

## テスト

```bash
pytest tests/ -v --cov=src
```

## APIドキュメント

起動後、以下のURLでAPIドキュメントを確認できます：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
