#!/usr/bin/env python3
"""
Azure MySQLデータベース接続テストスクリプト
rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com への接続をテスト
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pymysql
import urllib.parse

def test_azure_mysql_connection():
    """Azure MySQLデータベースへの接続をテスト"""
    
    print("=" * 60)
    print("Azure MySQLデータベース接続テスト")
    print("=" * 60)
    
    # 環境変数の読み込み
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print("OK: .envファイルを読み込みました")
    else:
        print("WARNING: .envファイルが見つかりません")
        print("   環境変数から直接読み込みます")
    
    # データベース接続情報
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_NAME = os.getenv('DB_NAME', 'kondo-pos')
    
    print(f"\n接続情報:")
    print(f"   Host: {DB_HOST}")
    print(f"   Port: {DB_PORT}")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print(f"   Password: {'*' * len(DB_PASSWORD) if DB_PASSWORD else 'Not set'}")
    
    # 必須環境変数のチェック
    missing_vars = []
    if not DB_USER:
        missing_vars.append('DB_USER')
    if not DB_PASSWORD:
        missing_vars.append('DB_PASSWORD')
    
    if missing_vars:
        print(f"\nERROR: 必須の環境変数が設定されていません: {', '.join(missing_vars)}")
        print("\nAzure App Serviceで以下の環境変数を設定してください:")
        print("   - DB_USER: データベースユーザー名")
        print("   - DB_PASSWORD: データベースパスワード")
        print("   - DB_HOST: rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com")
        print("   - DB_NAME: kondo-pos")
        return False
    
    # SSL証明書の確認
    ssl_cert_path = Path('DigiCertGlobalRootG2.crt.pem')
    print(f"\nSSL証明書: {'有効' if ssl_cert_path.exists() else '無効'}")
    if ssl_cert_path.exists():
        print(f"   証明書パス: {ssl_cert_path.absolute()}")
    
    # 接続テスト（SSL有効）
    print(f"\nSSL有効で接続テスト中...")
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            ssl_ca=str(ssl_cert_path) if ssl_cert_path.exists() else None,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            charset='utf8mb4',
            connect_timeout=30
        )
        
        with connection.cursor() as cursor:
            # バージョン確認
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"SUCCESS: SSL有効接続成功!")
            print(f"   MySQL Version: {version[0]}")
            
            # データベース確認
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"   Current Database: {db_name[0]}")
            
            # テーブル一覧確認
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"   Tables: {len(tables)}個")
            for table in tables:
                print(f"     - {table[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"ERROR: SSL有効接続エラー: {e}")
        
        # SSL無効で再試行
        print(f"\nSSL無効で接続テスト中...")
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                ssl_disabled=True,
                charset='utf8mb4',
                connect_timeout=30
            )
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"SUCCESS: SSL無効接続成功!")
                print(f"   MySQL Version: {version[0]}")
            
            connection.close()
            return True
            
        except Exception as e2:
            print(f"ERROR: SSL無効接続エラー: {e2}")
            
            # エラー分析
            print(f"\nエラー分析:")
            error_str = str(e).lower()
            if "access denied" in error_str:
                print("   - 認証エラー: ユーザー名またはパスワードが間違っています")
            elif "can't connect" in error_str or "connection refused" in error_str:
                print("   - 接続エラー: ホストまたはポートが間違っているか、ファイアウォールでブロックされています")
            elif "ssl" in error_str:
                print("   - SSL証明書エラー: SSL証明書の設定に問題があります")
            elif "unknown database" in error_str:
                print("   - データベースエラー: 指定されたデータベースが存在しません")
            else:
                print(f"   - その他のエラー: {e}")
            
            return False

def create_env_file():
    """サンプル.envファイルを作成"""
    env_content = """# Azure MySQL Database Configuration
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com
DB_PORT=3306
DB_NAME=kondo-pos
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("\n.envファイルを作成しました")
    print("   実際の接続情報を入力してください")

if __name__ == "__main__":
    success = test_azure_mysql_connection()
    
    if not success:
        print(f"\n次の手順を試してください:")
        print(f"   1. Azure App Serviceの「構成」→「アプリケーション設定」で環境変数を確認")
        print(f"   2. データベースのファイアウォール設定でAzure App ServiceのIPを許可")
        print(f"   3. データベースの接続文字列が正しいか確認")
        print(f"   4. SSL証明書のダウンロードと配置")
        
        # .envファイルが存在しない場合は作成
        if not Path('.env').exists():
            create_env_file()
    
    print("=" * 60)
