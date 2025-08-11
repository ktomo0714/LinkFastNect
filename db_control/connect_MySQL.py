import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベース接続情報（直接指定）
DB_USER = "tech0gen10student"
DB_PASSWORD = "vY7JZNfU"
DB_HOST = "rdbs-002-gen10-step3-1-oshima5.mysql.database.azure.com"
DB_PORT = "3306"
DB_NAME = "legotest"

# DATABASE_URLを構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# SQLAlchemyエンジンの作成（接続テストは削除してエンジンのみ作成）
engine = create_engine(
    DATABASE_URL,
    echo=False,  # ログ出力を無効化
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "ssl": {
            "ssl_disabled": False
        },
        "charset": "utf8mb4"
    }
)

# Base と SessionLocal の作成
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)