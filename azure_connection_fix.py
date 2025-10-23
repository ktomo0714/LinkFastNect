#!/usr/bin/env python3
"""
Azure App Service用データベース接続修正版
環境変数の設定と接続テストを行う
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pymysql
import urllib.parse

def check_azure_environment():
    """Azure App Service環境の確認"""
    print("=" * 60)
    print("Azure App Service環境確認")
    print("=" * 60)
    
    # Azure App Service環境変数の確認
    azure_env_vars = [
        'WEBSITE_SITE_NAME',
        'WEBSITE_RESOURCE_GROUP',
        'WEBSITE_INSTANCE_ID',
        'APPSETTING_DB_USER',
        'APPSETTING_DB_PASSWORD',
        'APPSETTING_DB_HOST',
        'APPSETTING_DB_NAME'
    ]
    
    print("Azure App Service環境変数:")
    for var in azure_env_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var:
                print(f"   {var}: {'*' * len(value)}")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: Not set")
    
    # データベース接続情報の取得
    DB_USER = os.getenv('DB_USER') or os.getenv('APPSETTING_DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD') or os.getenv('APPSETTING_DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST') or os.getenv('APPSETTING_DB_HOST', 'rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_NAME = os.getenv('DB_NAME') or os.getenv('APPSETTING_DB_NAME', 'kondo-pos')
    
    print(f"\nデータベース接続情報:")
    print(f"   Host: {DB_HOST}")
    print(f"   Port: {DB_PORT}")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print(f"   Password: {'*' * len(DB_PASSWORD) if DB_PASSWORD else 'Not set'}")
    
    return DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def test_database_connection(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    """データベース接続テスト"""
    print(f"\nデータベース接続テスト中...")
    
    # SSL証明書の確認
    ssl_cert_path = Path('DigiCertGlobalRootG2.crt.pem')
    print(f"SSL証明書: {'有効' if ssl_cert_path.exists() else '無効'}")
    
    try:
        # SSL有効で接続テスト
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
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"SUCCESS: データベース接続成功!")
            print(f"   MySQL Version: {version[0]}")
            
            # テーブル確認
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"   テーブル数: {len(tables)}個")
            for table in tables:
                print(f"     - {table[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"ERROR: データベース接続エラー: {e}")
        
        # エラー分析
        error_str = str(e).lower()
        if "access denied" in error_str:
            print("   原因: 認証エラー - ユーザー名またはパスワードが間違っています")
        elif "can't connect" in error_str or "connection refused" in error_str:
            print("   原因: 接続エラー - ホストまたはポートが間違っているか、ファイアウォールでブロックされています")
        elif "ssl" in error_str:
            print("   原因: SSL証明書エラー - SSL証明書の設定に問題があります")
        elif "unknown database" in error_str:
            print("   原因: データベースエラー - 指定されたデータベースが存在しません")
        else:
            print(f"   原因: その他のエラー - {e}")
        
        return False

def create_azure_env_template():
    """Azure App Service用の環境変数テンプレートを作成"""
    template = """# Azure App Service用環境変数設定
# Azure Portal > App Service > 構成 > アプリケーション設定 で設定してください

# データベース接続情報
DB_USER=tech0gen10student
DB_PASSWORD=your_password_here
DB_HOST=rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com
DB_PORT=3306
DB_NAME=kondo-pos

# または、APPSETTING_プレフィックス付きで設定
APPSETTING_DB_USER=tech0gen10student
APPSETTING_DB_PASSWORD=your_password_here
APPSETTING_DB_HOST=rdbs-002-gen10-step3-2-oshima5.mysql.database.azure.com
APPSETTING_DB_NAME=kondo-pos
"""
    
    with open('azure_env_template.txt', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("\nAzure App Service用環境変数テンプレートを作成しました: azure_env_template.txt")

def main():
    """メイン処理"""
    # 環境変数の読み込み
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print("OK: .envファイルを読み込みました")
    
    # Azure環境の確認
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME = check_azure_environment()
    
    # 必須環境変数のチェック
    if not DB_USER or not DB_PASSWORD:
        print("\nERROR: 必須の環境変数が設定されていません")
        print("Azure App Serviceの「構成」→「アプリケーション設定」で以下を設定してください:")
        print("   - DB_USER または APPSETTING_DB_USER")
        print("   - DB_PASSWORD または APPSETTING_DB_PASSWORD")
        print("   - DB_HOST または APPSETTING_DB_HOST")
        print("   - DB_NAME または APPSETTING_DB_NAME")
        
        create_azure_env_template()
        return False
    
    # データベース接続テスト
    success = test_database_connection(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    
    if success:
        print("\nSUCCESS: データベース接続が正常に動作しています")
        print("Azure App Serviceでの接続エラーは環境変数の設定問題の可能性があります")
    else:
        print("\nERROR: データベース接続に失敗しました")
        print("上記のエラー分析を参考に設定を確認してください")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    main()
