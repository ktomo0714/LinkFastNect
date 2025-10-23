# Azure App Service アプリケーションエラー トラブルシューティング

## 現在の状況

**エラー**: `:( Application Error`
- ヘルスチェックエンドポイント `/health` でアプリケーションエラーが発生
- 環境変数は正しく設定されている
- デプロイは成功しているが、アプリケーションが起動していない

## 原因の可能性

1. **スタートアップコマンドが設定されていない**
2. **アプリケーション起動時のエラー**
3. **ポート設定の不一致**
4. **依存関係のインストール失敗**

## 解決手順

### 1. スタートアップコマンドの設定（最重要）

**Azure Portal** → **App Service** → **構成** → **全般設定**

#### Linux App Serviceの場合
**スタートアップコマンド** に以下を設定：
```bash
bash startup.sh
```

または、シンプルな起動方法：
```bash
gunicorn -w 2 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000 --timeout 300
```

または、Uvicorn直接起動：
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### 2. ログの確認

**App Service** → **監視** → **ログストリーム** で以下を確認：
- アプリケーションの起動ログ
- エラーメッセージ
- 依存関係のインストール状況

### 3. 診断ツールの実行

**App Service** → **開発ツール** → **SSH** または **コンソール** で：

```bash
# 現在のディレクトリを確認
pwd
ls -la

# 診断ツールを実行
python azure_diagnostic.py

# アプリケーションを手動起動してテスト
python app_startup.py
```

### 4. 環境変数の確認

**App Service** → **構成** → **アプリケーション設定** で以下が設定されているか確認：

| 名前 | 値 | 必須 |
|------|-----|------|
| `DB_USER` | `tech0gen10student` | ✓ |
| `DB_PASSWORD` | `[パスワード]` | ✓ |
| `DB_HOST` | `rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com` | ✓ |
| `DB_PORT` | `3306` | △ |
| `DB_NAME` | `kondo-pos` | ✓ |
| `WEBSITES_PORT` | `8000` | ✓ |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `1` | ✓ |

### 5. Python バージョンの確認

**App Service** → **構成** → **全般設定**
- **Python バージョン**: `3.12`

### 6. ファイアウォール設定の確認

**Azure Database for MySQL** → **接続セキュリティ**
- **Azure サービスへのアクセスを許可**: ON
- または、App ServiceのIPアドレスを許可

## クイックフィックス手順

### オプション1: シンプルな起動コマンド（推奨）

1. **スタートアップコマンド** を以下に変更：
   ```bash
   python -m gunicorn -w 2 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000 --timeout 300 --access-logfile - --error-logfile -
   ```

2. **保存** → **App Serviceを再起動**

### オプション2: Uvicorn直接起動

1. **スタートアップコマンド** を以下に変更：
   ```bash
   python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
   ```

2. **保存** → **App Serviceを再起動**

### オプション3: カスタムスタートアップスクリプト

1. **スタートアップコマンド** を以下に変更：
   ```bash
   bash startup.sh
   ```

2. **保存** → **App Serviceを再起動**

## ログの確認方法

### アプリケーションログ

**App Service** → **監視** → **App Service ログ**
- **アプリケーション ログ (ファイル システム)**: ON
- **詳細なエラー メッセージ**: ON
- **失敗した要求のトレース**: ON

### リアルタイムログ

**App Service** → **監視** → **ログストリーム**

### SSH接続

**App Service** → **開発ツール** → **SSH**

```bash
# ログファイルを確認
cat /home/LogFiles/application.log
cat /home/LogFiles/kudu-trace.log

# アプリケーションディレクトリに移動
cd /home/site/wwwroot

# ファイル確認
ls -la

# アプリケーションを手動起動
python app.py
```

## よくある問題と解決方法

### 問題1: "No module named 'app'"
**原因**: アプリケーションファイルが見つからない
**解決**: デプロイが正常に完了しているか確認

### 問題2: "Address already in use"
**原因**: ポートが既に使用されている
**解決**: `WEBSITES_PORT`を確認、または別のポートを使用

### 問題3: "Database connection failed"
**原因**: データベース接続エラー
**解決**: 
- ファイアウォール設定を確認
- 環境変数が正しく設定されているか確認
- SSL証明書が存在するか確認

### 問題4: "Application timeout"
**原因**: アプリケーションの起動に時間がかかりすぎている
**解決**: 
- タイムアウトを延長
- `WEBSITES_CONTAINER_START_TIME_LIMIT=1800`を設定

## 推奨される次のステップ

1. **スタートアップコマンドを設定**（オプション1またはオプション2）
2. **App Serviceを再起動**
3. **ログストリームで起動状況を確認**
4. **ヘルスチェックエンドポイントにアクセス**: `https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/health`
5. **問題が解決しない場合は診断ツールを実行**

## サポート情報

問題が解決しない場合は、以下の情報を収集してください：
- ログストリームの内容
- SSH経由での診断ツールの実行結果
- アプリケーションの手動起動結果
