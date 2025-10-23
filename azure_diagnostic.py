#!/usr/bin/env python3
"""
Azure App Service診断スクリプト
デプロイ後の問題を特定するためのツール
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """環境変数の確認"""
    print("=== Environment Check ===")
    env_vars = [
        'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME',
        'WEBSITES_PORT', 'WEBSITES_ENABLE_APP_SERVICE_STORAGE',
        'SCM_DO_BUILD_DURING_DEPLOYMENT'
    ]
    
    for var in env_vars:
        value = os.getenv(var, 'Not set')
        if 'PASSWORD' in var:
            value = '*' * len(value) if value != 'Not set' else 'Not set'
        print(f"{var}: {value}")
    print("=" * 30)

def check_files():
    """必要なファイルの確認"""
    print("=== File Check ===")
    required_files = [
        'app.py',
        'startup.sh',
        'gunicorn.conf.py',
        'requirements.txt',
        'db_control/__init__.py',
        'db_control/connection.py',
        'db_control/models.py',
        'DigiCertGlobalRootG2.crt.pem'
    ]
    
    for file in required_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"✗ {file} (missing)")
    print("=" * 20)

def check_python_packages():
    """Pythonパッケージの確認"""
    print("=== Python Packages Check ===")
    try:
        import fastapi
        print(f"✓ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"✗ FastAPI: {e}")
    
    try:
        import uvicorn
        print(f"✓ Uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"✗ Uvicorn: {e}")
    
    try:
        import gunicorn
        print(f"✓ Gunicorn: {gunicorn.__version__}")
    except ImportError as e:
        print(f"✗ Gunicorn: {e}")
    
    try:
        import sqlalchemy
        print(f"✓ SQLAlchemy: {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"✗ SQLAlchemy: {e}")
    
    try:
        import pymysql
        print(f"✓ PyMySQL: {pymysql.__version__}")
    except ImportError as e:
        print(f"✗ PyMySQL: {e}")
    
    print("=" * 35)

def check_database_connection():
    """データベース接続の確認"""
    print("=== Database Connection Check ===")
    try:
        from db_control.connection import test_connection
        if test_connection():
            print("✓ Database connection: SUCCESS")
        else:
            print("✗ Database connection: FAILED")
    except Exception as e:
        print(f"✗ Database connection error: {e}")
    print("=" * 40)

def check_app_import():
    """アプリケーションのインポート確認"""
    print("=== App Import Check ===")
    try:
        from app import app
        print("✓ App import: SUCCESS")
        print(f"  App type: {type(app)}")
    except Exception as e:
        print(f"✗ App import error: {e}")
    print("=" * 25)

def check_gunicorn_config():
    """Gunicorn設定の確認"""
    print("=== Gunicorn Config Check ===")
    try:
        import gunicorn.conf
        print("✓ Gunicorn config import: SUCCESS")
    except Exception as e:
        print(f"✗ Gunicorn config import error: {e}")
    
    # 設定ファイルの存在確認
    if Path('gunicorn.conf.py').exists():
        print("✓ gunicorn.conf.py exists")
    else:
        print("✗ gunicorn.conf.py missing")
    print("=" * 35)

def main():
    """メイン診断処理"""
    print("Azure App Service Diagnostic Tool")
    print("=" * 50)
    
    check_environment()
    check_files()
    check_python_packages()
    check_database_connection()
    check_app_import()
    check_gunicorn_config()
    
    print("\nDiagnostic completed!")
    print("If any checks failed, please review the Azure App Service configuration.")

if __name__ == "__main__":
    main()
