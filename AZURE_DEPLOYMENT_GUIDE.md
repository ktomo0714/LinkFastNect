# Azure App Service デプロイガイド

## デプロイエラーの解決

### 問題の概要
Azure App ServiceへのデプロイでZIP Deployが失敗する問題を解決します。

### 原因
1. Python バージョンの不一致（3.11 vs 3.12）
2. Azure App Service用の起動設定が不適切
3. 環境変数の設定が不完全

### 解決手順

#### 1. Azure App Serviceの設定確認

**Azure Portal** で以下の設定を確認・設定してください：

1. **App Service** → **構成** → **アプリケーション設定**
2. 以下の環境変数を設定：

| 名前 | 値 | 説明 |
|------|-----|------|
| `DB_USER` | `tech0gen10student` | データベースユーザー名 |
| `DB_PASSWORD` | `[実際のパスワード]` | データベースパスワード |
| `DB_HOST` | `rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com` | データベースホスト |
| `DB_PORT` | `3306` | データベースポート |
| `DB_NAME` | `kondo-pos` | データベース名 |
| `WEBSITES_PORT` | `8000` | アプリケーションポート |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `1` | デプロイ時のビルド有効化 |

#### 2. スタートアップコマンドの設定

**App Service** → **構成** → **全般設定** で以下を設定：

- **スタートアップコマンド**: `bash startup.sh`

#### 3. Python バージョンの確認

**App Service** → **構成** → **全般設定** で以下を確認：

- **Python バージョン**: `3.12`

### デプロイファイルの説明

#### 新規追加ファイル

1. **`gunicorn.conf.py`**
   - Gunicornの設定ファイル
   - Azure App Service用に最適化

2. **`web.config`**
   - IIS用の設定ファイル（Windows App Service用）

3. **`.azure/appsettings.json`**
   - Azure App Service用の環境変数テンプレート

4. **`.azure/deployment.yaml`**
   - デプロイメント設定

#### 修正ファイル

1. **`startup.sh`**
   - 環境変数確認とデータベース接続テストを追加
   - Gunicorn設定ファイルを使用

2. **`.github/workflows/main_app-002-gen10-step3-1-py-oshima38.yml`**
   - Python バージョンを3.12に修正
   - デプロイパッケージ作成を改善

### デプロイ後の確認

#### 1. ヘルスチェック
```
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/health
```

正常な場合のレスポンス：
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-23T13:53:15.613126"
}
```

#### 2. ログの確認
**App Service** → **監視** → **ログストリーム** で以下を確認：
- 環境変数が正しく読み込まれているか
- データベース接続が成功しているか
- アプリケーションが正常に起動しているか

#### 3. API エンドポイントの確認
```
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/docs
```

### トラブルシューティング

#### よくある問題

1. **環境変数が読み込まれない**
   - Azure Portalで環境変数を再設定
   - アプリケーションを再起動

2. **データベース接続エラー**
   - ファイアウォール設定を確認
   - 接続文字列が正しいか確認

3. **アプリケーションが起動しない**
   - スタートアップコマンドを確認
   - ログでエラー内容を確認

4. **デプロイが失敗する**
   - GitHub Actionsのログを確認
   - ファイルサイズや権限を確認

### 手動デプロイ（緊急時）

GitHub Actionsが失敗した場合の手動デプロイ手順：

1. **Azure CLI** でログイン
2. **ZIPファイル** を作成
3. **az webapp deployment** でデプロイ

```bash
# Azure CLI ログイン
az login

# ZIPファイル作成
zip -r deploy.zip . -x '*.git*' -x '*venv*' -x '*.env*' -x '*__pycache__*'

# デプロイ
az webapp deployment source config-zip \
  --resource-group [リソースグループ名] \
  --name app-002-gen10-step3-1-py-oshima38 \
  --src deploy.zip
```

### 参考情報

- [Azure App Service Python デプロイ](https://docs.microsoft.com/ja-jp/azure/app-service/quickstart-python)
- [Gunicorn 設定](https://docs.gunicorn.org/en/stable/configure.html)
- [Azure App Service 環境変数](https://docs.microsoft.com/ja-jp/azure/app-service/configure-common)
