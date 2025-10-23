# LinkFastNect - POSシステム バックエンドAPI

POSシステムのバックエンドAPIです。FastAPIとAzure MySQLデータベースを使用しています。

## 📋 概要

このプロジェクトは、POSシステムのバックエンドAPIを提供します。商品マスタの管理、取引の記録、売上統計の取得などの機能を備えています。

## 🚀 主な機能

### APIファンクション（Lv1）

1. **商品マスタ検索**
   - エンドポイント: `GET /api/product-search`
   - 商品コードで商品情報を検索

2. **購入処理**
   - エンドポイント: `POST /api/purchase`
   - 取引と取引明細の登録

3. **売上統計**
   - 売上統計、売れ筋商品、時間帯別売上など

### データベース構成

- **商品マスタ**: 商品情報の管理
- **取引**: 取引の記録
- **取引明細**: 取引の詳細情報

## 🛠️ 技術スタック

- **Web Framework**: FastAPI 0.109.0
- **ASGI Server**: Uvicorn 0.27.0 / Gunicorn 21.2.0
- **Database**: Azure Database for MySQL
- **ORM**: SQLAlchemy 2.0.23
- **Database Driver**: PyMySQL 1.1.0
- **Validation**: Pydantic 2.5.3
- **Python Version**: 3.12

## 📦 セットアップ

### 必要な環境変数

| 変数名 | 説明 | 例 |
|--------|------|-----|
| `DB_USER` | データベースユーザー名 | `tech0gen10student` |
| `DB_PASSWORD` | データベースパスワード | `[your_password]` |
| `DB_HOST` | データベースホスト | `rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com` |
| `DB_PORT` | データベースポート | `3306` |
| `DB_NAME` | データベース名 | `kondo-pos` |

### ローカル開発環境

1. **依存関係のインストール**
   ```bash
   pip install -r requirements.txt
   ```

2. **環境変数の設定**
   ```bash
   # .envファイルを作成
   cp .env.example .env
   # .envファイルを編集して実際の値を設定
   ```

3. **アプリケーションの起動**
   ```bash
   # Uvicornで起動
   uvicorn app:app --reload --port 8000
   
   # または、直接実行
   python app.py
   ```

4. **APIドキュメントにアクセス**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### データベース接続テスト

```bash
python test_db_connection.py
```

### サンプルデータの作成

```bash
python create_sample_data.py
```

## 🌐 Azure App Serviceへのデプロイ

### 自動デプロイ（GitHub Actions）

mainブランチにプッシュすると自動的にAzure App Serviceにデプロイされます。

### 手動デプロイ

詳細は以下のガイドを参照してください：
- [Azure デプロイガイド](AZURE_DEPLOYMENT_GUIDE.md)
- [Azure セットアップガイド](AZURE_SETUP_GUIDE.md)
- [Azure トラブルシューティング](AZURE_TROUBLESHOOTING.md)

### スタートアップコマンド

Azure App Serviceの設定で以下のスタートアップコマンドを設定してください：

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

詳細は[STARTUP_COMMAND_OPTIONS.txt](STARTUP_COMMAND_OPTIONS.txt)を参照してください。

## 📚 API エンドポイント

### ヘルスチェック

```
GET /health
```

レスポンス例：
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-23T13:53:15.613126"
}
```

### 商品マスタ

- `GET /api/products` - 商品一覧取得
- `GET /api/products/{product_id}` - 商品詳細取得
- `GET /api/products/code/{code}` - 商品コードで検索
- `GET /api/product-search?code={code}` - 商品マスタ検索（仕様書準拠）
- `POST /api/products` - 商品登録
- `PUT /api/products/{product_id}` - 商品更新
- `DELETE /api/products/{product_id}` - 商品削除

### 取引

- `GET /api/transactions` - 取引一覧取得
- `GET /api/transactions/{transaction_id}` - 取引詳細取得
- `POST /api/transactions` - 取引登録
- `POST /api/purchase` - 購入処理（仕様書準拠）
- `DELETE /api/transactions/{transaction_id}` - 取引削除

### 統計

- `GET /api/statistics/sales` - 売上統計
- `GET /api/statistics/top-products` - 売れ筋商品
- `GET /api/statistics/hourly-sales` - 時間帯別売上

## 🔧 診断ツール

### データベース接続診断

```bash
python azure_connection_fix.py
```

### アプリケーション診断

```bash
python azure_diagnostic.py
```

## 📁 プロジェクト構成

```
LinkFastNect/
├── app.py                      # メインアプリケーション
├── requirements.txt            # 依存関係
├── startup.sh                  # 起動スクリプト
├── gunicorn.conf.py           # Gunicorn設定
├── db_control/                # データベース関連
│   ├── connection.py          # データベース接続
│   ├── models.py              # データベースモデル
│   └── crud.py                # CRUD操作例
├── .github/workflows/         # GitHub Actions
│   └── main_*.yml             # デプロイワークフロー
├── AZURE_*.md                 # Azure関連ドキュメント
└── test_db_connection.py     # 接続テストスクリプト
```

## 🤝 コントリビューター

- @ktomo0714 - プロジェクトオーナー
- @cursoragent - Cursor Agent

## 📄 ライセンス

このプロジェクトはプライベートプロジェクトです。

## 🔗 関連リソース

- [Azure App Service](https://azure.microsoft.com/ja-jp/services/app-service/)
- [Azure Database for MySQL](https://azure.microsoft.com/ja-jp/services/mysql/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📞 サポート

問題が発生した場合は、以下のドキュメントを参照してください：
- [Azure トラブルシューティング](AZURE_TROUBLESHOOTING.md)
- [Azure デプロイガイド](AZURE_DEPLOYMENT_GUIDE.md)
- [Azure セットアップガイド](AZURE_SETUP_GUIDE.md)