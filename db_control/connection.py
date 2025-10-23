import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
import urllib.parse
import sys

# 環境変数の読み込み
base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME')

# 環境変数の検証
missing_vars = []
if not DB_USER:
    missing_vars.append('DB_USER')
if not DB_PASSWORD:
    missing_vars.append('DB_PASSWORD')
if not DB_HOST:
    missing_vars.append('DB_HOST')
if not DB_NAME:
    missing_vars.append('DB_NAME')

if missing_vars:
    error_msg = f"❌ 必須の環境変数が設定されていません: {', '.join(missing_vars)}"
    print(error_msg)
    print("Azure App Serviceの「構成」→「アプリケーション設定」で以下の環境変数を設定してください:")
    for var in missing_vars:
        print(f"  - {var}")
    # 環境変数が設定されていない場合でもアプリケーションは起動させる
    # （ヘルスチェックで状態を確認できるように）
    DB_USER = DB_USER or 'dummy'
    DB_PASSWORD = DB_PASSWORD or 'dummy'
    DB_HOST = DB_HOST or 'localhost'
    DB_NAME = DB_NAME or 'dummy'

# SSL証明書のパス（Azure Database for MySQLで必要）
ssl_cert_path = base_path / 'DigiCertGlobalRootG2.crt.pem'

# パスワードをURLエンコード
encoded_password = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else ''

# MySQLのURL構築
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_password}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?charset=utf8mb4"
)

# エンジンの作成
if ssl_cert_path.exists():
    # SSL証明書がある場合
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "ssl": {
                "ssl_ca": str(ssl_cert_path)
            }
        },
        echo=True,  # SQLログ出力（本番環境ではFalse）
        pool_pre_ping=True,  # 接続の健全性チェック
        pool_recycle=3600,   # 1時間ごとに接続をリサイクル
        pool_size=5,
        max_overflow=10
    )
else:
    # SSL証明書がない場合（開発環境用）
    print("⚠️  SSL証明書が見つかりません。SSL無しで接続します。")
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10
    )

# Baseクラスの作成
Base = declarative_base()

# セッションファクトリの作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def test_connection():
    """データベース接続をテストする"""
    try:
        print(f"🔄 データベース接続テスト中...")
        print(f"   接続情報: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        print(f"   SSL証明書: {'有効' if ssl_cert_path.exists() else '無効'}")
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION() as version"))
            version = result.fetchone()
            print(f"✅ データベース接続成功!")
            print(f"   MySQL Version: {version[0]}")
            
            # データベース確認
            result = connection.execute(text("SELECT DATABASE() as db_name"))
            db_name = result.fetchone()
            print(f"   Database: {db_name[0]}")
            
            return True
    except Exception as e:
        print(f"❌ データベース接続エラー:")
        print(f"   エラー内容: {str(e)}")
        print(f"   エラータイプ: {type(e).__name__}")
        print(f"   接続情報: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        print(f"\n💡 トラブルシューティング:")
        print(f"   1. Azure App Serviceの「構成」→「アプリケーション設定」で環境変数を確認")
        print(f"   2. データベースのファイアウォール設定を確認（Azure portalで許可されているか）")
        print(f"   3. データベースの接続文字列が正しいか確認")
        print(f"   4. SSL証明書のパスが正しいか確認: {ssl_cert_path}")
        return False

def get_db():
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
