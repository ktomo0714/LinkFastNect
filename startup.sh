#!/bin/bash
# Azure App Service startup script

# 環境変数の確認
echo "=== Environment Variables ==="
echo "DB_USER: ${DB_USER:-Not set}"
echo "DB_HOST: ${DB_HOST:-Not set}"
echo "DB_NAME: ${DB_NAME:-Not set}"
echo "DB_PORT: ${DB_PORT:-3306}"
echo "============================="

# データベース接続テスト
echo "Testing database connection..."
python -c "
from db_control.connection import test_connection
if test_connection():
    print('Database connection: OK')
else:
    print('Database connection: FAILED')
"

# アプリケーション起動
echo "Starting POS API application..."
exec gunicorn -c gunicorn.conf.py app:app