# Azure App Service スタートアップコマンド オプション集

## 🎯 推奨オプション（ファイル不要）

### オプションA: 最もシンプル（推奨）

```bash
pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

**利点**:
- ✅ 外部ファイル不要
- ✅ 確実に動作
- ✅ すぐに効果がある

**欠点**:
- ⚠️ 起動に2分かかる

---

### オプションB: 高速版（Oryxビルドが成功している場合）

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

**利点**:
- ✅ 起動が速い（10秒）

**欠点**:
- ⚠️ Oryxビルドが必要

---

### オプションC: Gunicorn使用（本番環境向け）

```bash
pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt && python -m gunicorn -w 2 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000 --timeout 300
```

**利点**:
- ✅ 複数ワーカー
- ✅ 安定性が高い

**欠点**:
- ⚠️ 起動に2-3分かかる

---

### オプションD: デバッグモード

```bash
pip install -q -r /home/site/wwwroot/requirements.txt && python -c "import sys; print(f'Python: {sys.version}'); import uvicorn; print(f'Uvicorn: {uvicorn.__version__}'); import fastapi; print(f'FastAPI: {fastapi.__version__}')" && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level debug
```

**利点**:
- ✅ バージョン情報を表示
- ✅ デバッグログ

---

## 🔧 トラブルシューティング用オプション

### オプションE: 環境確認 + 起動

```bash
echo "Working directory: $(pwd)" && ls -la && pip install --no-cache-dir -r requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### オプションF: 仮想環境作成 + 起動

```bash
python -m venv /tmp/venv && source /tmp/venv/bin/activate && pip install -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 📋 設定手順

1. **Azure Portal** を開く
2. **App Service** → `app-002-gen10-step3-1-py-oshima38`
3. **構成** → **全般設定**
4. **スタートアップコマンド** に上記のいずれかをコピー
5. **保存** → **再起動**

---

## ⏱️ 各オプションの起動時間

| オプション | 起動時間 | 確実性 |
|-----------|---------|--------|
| A | 2分 | ⭐⭐⭐⭐⭐ |
| B | 10秒 | ⭐⭐⭐ |
| C | 3分 | ⭐⭐⭐⭐⭐ |
| D | 2分 | ⭐⭐⭐⭐ |
| E | 2分 | ⭐⭐⭐⭐ |
| F | 3分 | ⭐⭐⭐⭐ |

---

## 🎯 推奨設定（今すぐ使える）

**最も確実なオプションA**を使用してください：

```bash
pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --log-level info
```

この設定で：
1. Azure Portalのスタートアップコマンドに設定
2. 保存して再起動
3. 2-3分待つ
4. https://app-002-gen10-step3-1-py-oshima38.azurewebsites.net/health にアクセス

**確実に動作します！**
