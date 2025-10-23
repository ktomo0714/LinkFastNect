# 🚨 緊急修正ガイド - アプリケーションエラー解決

## 現在の状況

アプリケーションエラーが発生しています。以下の手順で**今すぐ**修正してください。

## ✅ 修正手順（5分で完了）

### ステップ1: Azure Portalでスタートアップコマンドを設定

1. **Azure Portal** (https://portal.azure.com) を開く
2. **App Service** → `app-002-gen10-step3-1-py-oshima38` をクリック
3. 左メニューから **構成** をクリック
4. **全般設定** タブをクリック
5. **スタートアップコマンド** に以下を入力：

```bash
bash azure_startup.sh
```

6. 画面上部の **保存** をクリック
7. 「構成の変更を保存しますか？」→ **はい** をクリック

### ステップ2: App Serviceを再起動

1. App Serviceの概要ページに戻る
2. 上部メニューの **再起動** をクリック
3. 「再起動しますか？」→ **はい** をクリック

### ステップ3: ログストリームで確認

1. 左メニューから **監視** → **ログストリーム** をクリック
2. 以下のようなログが表示されるまで待つ（1-2分）：

```
=== Azure App Service Startup ===
Working directory: /home/site/wwwroot
Python version: Python 3.12.11
Virtual environment found at: /home/site/wwwroot/antenv
Virtual environment activated
Starting application on port 8000...
INFO:     Application startup complete.
```

### ステップ4: 動作確認

ブラウザで以下にアクセス：
- ヘルスチェック: https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/health
- APIドキュメント: https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/docs

## 🔧 代替方法（上記で解決しない場合）

### 方法A: SSHで直接修正

1. Azure Portal → App Service → **開発ツール** → **SSH**
2. 以下のコマンドを実行：

```bash
cd /home/site/wwwroot
python -m venv antenv
source antenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8000 &
```

### 方法B: シンプルなスタートアップコマンド

スタートアップコマンドを以下に変更：

```bash
python -m pip install -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📊 確認事項チェックリスト

- [ ] GitHub Actionsのデプロイが完了している（緑色のチェックマーク）
- [ ] スタートアップコマンドが `bash azure_startup.sh` に設定されている
- [ ] 以下の環境変数が設定されている：
  - [ ] `DB_USER=tech0gen10student`
  - [ ] `DB_PASSWORD=[実際のパスワード]`
  - [ ] `DB_HOST=rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com`
  - [ ] `DB_NAME=kondo-pos`
  - [ ] `WEBSITES_PORT=8000`
- [ ] App Serviceを再起動した
- [ ] ログストリームで起動ログを確認した

## 🆘 それでも解決しない場合

### デバッグ手順

1. **SSHでファイル確認**
```bash
cd /home/site/wwwroot
ls -la
cat azure_startup.sh
cat requirements.txt
```

2. **手動で仮想環境を作成**
```bash
python -m venv antenv
source antenv/bin/activate
pip list
pip install -r requirements.txt
```

3. **アプリケーションを手動起動**
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📞 エラーメッセージ別の対処法

### エラー: "No module named uvicorn"
→ 依存関係がインストールされていません
→ SSHで手動インストール（方法A参照）

### エラー: "Application timeout"
→ 起動に時間がかかっています
→ 環境変数に追加: `WEBSITES_CONTAINER_START_TIME_LIMIT=1800`

### エラー: "Database connection failed"
→ データベース環境変数を確認
→ ファイアウォール設定を確認

## 🎯 最も確実な方法（推奨）

**スタートアップコマンド**に以下を設定（依存関係を毎回インストール）：

```bash
pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

この方法は：
- ✅ 仮想環境を使わない（シンプル）
- ✅ 毎回依存関係をインストール（確実）
- ✅ すぐに動作する

デメリット：
- ⚠️ 起動時間が少し長い（30-60秒）

## 📸 Azure Portal設定画面のスクリーンショット参考

```
┌──────────────────────────────────────────────────┐
│ App Service > 構成 > 全般設定                      │
├──────────────────────────────────────────────────┤
│                                                  │
│ スタートアップコマンド                             │
│ ┌──────────────────────────────────────────────┐ │
│ │ bash azure_startup.sh                        │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
│ または                                            │
│                                                  │
│ ┌──────────────────────────────────────────────┐ │
│ │ pip install -r requirements.txt &&           │ │
│ │ python -m uvicorn app:app --host 0.0.0.0     │ │
│ │ --port 8000 --log-level info                 │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
│ Python バージョン: 3.12                           │
│                                                  │
│ [保存]  [破棄]                                   │
└──────────────────────────────────────────────────┘
```

## ⏱️ 予想される解決時間

- Azure Portal設定変更: 2分
- App Service再起動: 1分
- アプリケーション起動: 2分
- **合計: 約5分**

---

**今すぐ実行してください！**
1. Azure Portalを開く
2. スタートアップコマンドを設定
3. 保存して再起動
4. ログストリームで確認
