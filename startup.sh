#!/bin/bash
# Azure App Service startup script

set -e  # エラー時に即座に終了

echo "=== Azure App Service Startup ==="
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "================================"

# 環境変数の確認
echo "=== Environment Variables ==="
echo "DB_USER: ${DB_USER:-Not set}"
echo "DB_HOST: ${DB_HOST:-Not set}"
echo "DB_NAME: ${DB_NAME:-Not set}"
echo "DB_PORT: ${DB_PORT:-3306}"
echo "WEBSITES_PORT: ${WEBSITES_PORT:-8000}"
echo "============================="

# 必要なファイルの確認
echo "=== File Check ==="
ls -la app.py startup.sh gunicorn.conf.py requirements.txt
echo "=================="

# データベース接続テスト（エラーでも続行）
echo "Testing database connection..."
python -c "
try:
    from db_control.connection import test_connection
    if test_connection():
        print('Database connection: OK')
    else:
        print('Database connection: FAILED')
except Exception as e:
    print(f'Database connection test error: {e}')
" || echo "Database connection test failed, continuing..."

# アプリケーション起動
echo "Starting POS API application..."

# Gunicornでアプリケーションを起動（失敗時はUvicornにフォールバック）
if gunicorn -c gunicorn.conf.py app:app; then
    echo "Application started with Gunicorn"
else
    echo "Gunicorn failed, trying Uvicorn..."
    exec python app_startup.py
fi