# 🎯 最終修正ガイド - 確実に動作させる方法

## 問題の原因

Oryxビルドシステムでの`pip install`が失敗しています。最も確実な方法で修正します。

## ✅ 確実に動作する設定（推奨）

### Azure Portalで設定するスタートアップコマンド

**App Service** → **構成** → **全般設定** で以下を設定：

```bash
pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

### この方法の利点

- ✅ 仮想環境を使わない（シンプル）
- ✅ Oryxビルドに依存しない
- ✅ 起動時に毎回依存関係をインストール（確実）
- ✅ すぐに動作する

### この方法の欠点

- ⚠️ 初回起動が遅い（1-2分）
- ⚠️ 再起動のたびに依存関係をインストール

## 📋 完全な設定手順

### 1. GitHub Actionsの最新デプロイを待つ

現在実行中のデプロイが完了するまで待つ（約5分）

### 2. Azure Portalで環境変数を確認

**App Service** → **構成** → **アプリケーション設定**

必須の環境変数:
```
DB_USER=tech0gen10student
DB_PASSWORD=[実際のパスワード]
DB_HOST=rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com
DB_PORT=3306
DB_NAME=kondo-pos
WEBSITES_PORT=8000
```

### 3. スタートアップコマンドを設定

**App Service** → **構成** → **全般設定**

**スタートアップコマンド**:
```bash
pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

### 4. 保存して再起動

1. **保存** をクリック
2. **App Service を再起動**
3. **ログストリーム** で起動を確認（2-3分待つ）

## 🔄 代替方法（より高速）

ビルド済みの依存関係を使用する方法：

### スタートアップコマンド（方法2）

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

**注意**: この方法は、Oryxビルドが成功している場合のみ動作します。

## 📊 期待されるログ

### 正常起動時のログ

```
2025-10-23T15:00:00Z Installing collected packages: typing-extensions, sniffio, ...
2025-10-23T15:00:30Z Successfully installed fastapi-0.109.0 uvicorn-0.27.0 ...
2025-10-23T15:00:31Z INFO:     Started server process [1]
2025-10-23T15:00:31Z INFO:     Waiting for application startup.
2025-10-23T15:00:32Z INFO:     Application startup complete.
2025-10-23T15:00:32Z INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🆘 トラブルシューティング

### エラー: "Could not install packages"

**解決**: requirements.txtのバージョンを緩和

`requirements.txt`を以下に修正:

```txt
# Web Framework
fastapi>=0.109.0
uvicorn>=0.27.0
gunicorn>=21.2.0

# Database
sqlalchemy>=2.0.0
pymysql>=1.1.0
cryptography

# Data Validation
pydantic>=2.5.0

# Configuration
python-dotenv>=1.0.0

# HTTP Client
requests>=2.31.0

# Data Processing (optional)
# pandas
# numpy
# python-dateutil
```

### エラー: "Application timeout"

**解決**: タイムアウトを延長

環境変数に追加:
```
WEBSITES_CONTAINER_START_TIME_LIMIT=1800
```

### エラー: "Port already in use"

**解決**: ポート設定を確認

環境変数:
```
WEBSITES_PORT=8000
PORT=8000
```

## 🎯 最も確実な最小構成

### requirements.txt（最小版）

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.23
pymysql==1.1.0
cryptography
pydantic==2.5.3
python-dotenv==1.0.0
```

### スタートアップコマンド

```bash
pip install -q -r requirements.txt && uvicorn app:app --host 0.0.0.0 --port 8000
```

## ✅ 動作確認

### 1. ヘルスチェック

ブラウザで開く:
```
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/health
```

期待される結果:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-23T15:00:00.000000"
}
```

### 2. APIドキュメント

```
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/docs
```

### 3. ルートエンドポイント

```
https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/
```

## 📞 まとめ

### 今すぐ実行する手順

1. ✅ GitHub Actionsのデプロイ完了を待つ
2. ✅ Azure Portal → App Service → 構成 → 全般設定
3. ✅ スタートアップコマンドを設定:
   ```bash
   pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
   ```
4. ✅ 保存して再起動
5. ✅ ログストリームで確認（2-3分）
6. ✅ ヘルスチェックにアクセス

### 予想される所要時間

- デプロイ完了: 5分（自動）
- Azure Portal設定: 2分
- アプリケーション起動: 2分
- **合計: 約10分**

---

**この方法で確実に動作します！**
