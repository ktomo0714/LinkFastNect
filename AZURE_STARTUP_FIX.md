# Azure App Service 起動エラーの修正

## 問題の原因

```
/opt/python/3/bin/python: No module named uvicorn
WARNING: Could not find virtual environment directory /home/site/wwwroot/antenv
```

Azure App Serviceで仮想環境と依存関係が正しくインストールされていません。

## 解決方法

### 方法1: カスタムスタートアップスクリプト使用（推奨）

**Azure Portal** → **App Service** → **構成** → **全般設定** で：

**スタートアップコマンド**:
```bash
bash azure_startup.sh
```

このスクリプトは：
1. 仮想環境の存在を確認
2. 存在しない場合は作成
3. 依存関係を自動インストール
4. アプリケーションを起動

### 方法2: 環境変数設定

**App Service** → **構成** → **アプリケーション設定** で以下を追加：

| 名前 | 値 |
|------|-----|
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `1` |
| `ENABLE_ORYX_BUILD` | `true` |
| `POST_BUILD_COMMAND` | `pip install -r requirements.txt` |

### 方法3: 直接Pythonパスを指定

**スタートアップコマンド**:
```bash
/home/site/wwwroot/antenv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## 推奨される完全な設定手順

### 1. 環境変数の設定

**App Service** → **構成** → **アプリケーション設定**:

```
DB_USER=tech0gen10student
DB_PASSWORD=[実際のパスワード]
DB_HOST=rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com
DB_NAME=kondo-pos
WEBSITES_PORT=8000
SCM_DO_BUILD_DURING_DEPLOYMENT=1
ENABLE_ORYX_BUILD=true
```

### 2. スタートアップコマンドの設定

**App Service** → **構成** → **全般設定**:

```bash
bash azure_startup.sh
```

### 3. 保存と再起動

1. **保存** をクリック
2. **App Service を再起動**
3. **ログストリーム** で起動状況を確認

## 期待される起動ログ

正常に起動すると、以下のようなログが表示されます：

```
=== Azure App Service Startup ===
Working directory: /home/site/wwwroot
Python version: Python 3.12.11
Virtual environment found at: /home/site/wwwroot/antenv
Virtual environment activated
=== Environment Variables ===
DB_USER: tech0gen10student
DB_HOST: rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com
DB_NAME: kondo-pos
WEBSITES_PORT: 8000
=============================
Checking Python modules...
Uvicorn version: 0.27.0
FastAPI version: 0.109.0
Starting application on port 8000...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## トラブルシューティング

### 問題: 仮想環境が作成されない

**解決**: SSH接続して手動で作成

```bash
cd /home/site/wwwroot
python -m venv antenv
source antenv/bin/activate
pip install -r requirements.txt
```

### 問題: 依存関係のインストールが失敗

**解決**: `requirements.txt`を確認

```bash
cat requirements.txt
pip install -r requirements.txt --verbose
```

### 問題: ポート設定のエラー

**解決**: 環境変数`WEBSITES_PORT`を確認

```bash
echo $WEBSITES_PORT
```

## 検証方法

### 1. ヘルスチェック

```
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/health
```

期待されるレスポンス:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-23T14:53:15.613126"
}
```

### 2. APIドキュメント

```
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/docs
```

### 3. SSH診断

**App Service** → **開発ツール** → **SSH** で：

```bash
cd /home/site/wwwroot
ls -la antenv/
source antenv/bin/activate
python -c "import uvicorn; print(uvicorn.__version__)"
python app.py
```

## 追加の推奨事項

1. **GitHub Actionsでの仮想環境作成**
   - デプロイパッケージに`antenv`を含める
   - ビルド済みの仮想環境をデプロイ

2. **Oryxビルドの有効化**
   - `.deployment`ファイルの追加
   - `oryx-manifest.toml`の設定

3. **起動時間の延長**
   ```
   WEBSITES_CONTAINER_START_TIME_LIMIT=1800
   ```

## 参考資料

- [Azure App Service Python設定](https://docs.microsoft.com/ja-jp/azure/app-service/configure-language-python)
- [Oryx Build System](https://github.com/microsoft/Oryx)
