#!/usr/bin/env python3
"""
Azure App Service用の代替起動スクリプト
Gunicornが失敗した場合の代替手段
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """アプリケーションを起動"""
    print("=== Azure App Service Alternative Startup ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Environment variables:")
    for key in ['DB_USER', 'DB_HOST', 'DB_NAME', 'DB_PORT', 'WEBSITES_PORT']:
        print(f"  {key}: {os.getenv(key, 'Not set')}")
    print("=" * 50)
    
    # 必要なファイルの確認
    required_files = ['app.py', 'requirements.txt']
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file} found")
        else:
            print(f"✗ {file} missing")
    
    # データベース接続テスト
    try:
        from db_control.connection import test_connection
        if test_connection():
            print("✓ Database connection: OK")
        else:
            print("✗ Database connection: FAILED")
    except Exception as e:
        print(f"✗ Database connection test error: {e}")
    
    # ポート設定
    port = int(os.getenv('WEBSITES_PORT', '8000'))
    host = "0.0.0.0"
    
    print(f"Starting application on {host}:{port}")
    
    # Uvicornでアプリケーションを起動
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        reload=False
    )

if __name__ == "__main__":
    main()
