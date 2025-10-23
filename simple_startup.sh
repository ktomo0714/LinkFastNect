#!/bin/bash
# シンプルなAzure App Service起動スクリプト

echo "=== Simple Startup Script ==="
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"

# 環境変数の表示
echo "Environment variables:"
echo "  DB_USER: ${DB_USER:-Not set}"
echo "  DB_HOST: ${DB_HOST:-Not set}"
echo "  WEBSITES_PORT: ${WEBSITES_PORT:-8000}"

# ポート設定
PORT=${WEBSITES_PORT:-8000}

# アプリケーションを起動
echo "Starting application on port ${PORT}..."
exec python -m uvicorn app:app --host 0.0.0.0 --port $PORT --log-level info
