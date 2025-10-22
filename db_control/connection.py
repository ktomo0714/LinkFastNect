import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
import urllib.parse

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

# SSL証明書のパス（Azure Database for MySQLで必要）
ssl_cert_path = base_path / 'DigiCertGlobalRootG2.crt.pem'

# パスワードをURLエンコード
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

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
        print(f"❌ データベース接続エラー: {e}")
        print(f"   接続情報: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        return False

def get_db():
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
