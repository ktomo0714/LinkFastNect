import os
import sys
from pathlib import Path
from sqlalchemy import text
from .connection import engine, Base, SessionLocal, test_connection
from .models import ProductMaster, Transaction, TransactionDetail

def create_all_tables():
    """全テーブルを作成"""
    print("=" * 60)
    print("📊 データベーステーブル作成開始")
    print("=" * 60)
    
    try:
        # テーブル作成
        Base.metadata.create_all(bind=engine)
        print("✅ 全テーブルの作成に成功しました")
        
        # 作成されたテーブルの確認
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """))
            tables = result.fetchall()
            
            print("\n📋 作成されたテーブル:")
            for table in tables:
                print(f"   - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ テーブル作成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


def drop_all_tables():
    """全テーブルを削除（注意: データも全て削除されます）"""
    print("=" * 60)
    print("⚠️  全テーブル削除開始")
    print("=" * 60)
    
    response = input("本当に全テーブルを削除しますか? (yes/no): ")
    if response.lower() != 'yes':
        print("キャンセルしました")
        return False
    
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ 全テーブルの削除に成功しました")
        return True
        
    except Exception as e:
        print(f"❌ テーブル削除エラー: {e}")
        return False


def add_sample_data():
    """サンプルデータを追加"""
    print("=" * 60)
    print("📝 サンプルデータ追加開始")
    print("=" * 60)
    
    session = SessionLocal()
    
    try:
        # 既存データの削除（外部キー制約を考慮した順序）
        session.execute(text("DELETE FROM transaction_details"))
        session.execute(text("DELETE FROM transactions"))
        session.execute(text("DELETE FROM product_master"))
        session.commit()
        print("既存データを削除しました")
        
        # 商品マスタのサンプルデータ
        sample_products = [
            ProductMaster(code='1234567890123', name='おーいお茶', price=150),
            ProductMaster(code='2345678901234', name='ソフラン', price=300),
            ProductMaster(code='3456789012345', name='福島産ほうれん草', price=188),
            ProductMaster(code='4567890123456', name='タイガー歯ブラシ青', price=200),
            ProductMaster(code='5678901234567', name='四ツ谷サイダー', price=160),
            ProductMaster(code='6789012345678', name='キャンパスノートB5', price=180),
            ProductMaster(code='7890123456789', name='三菱鉛筆HB', price=120),
            ProductMaster(code='8901234567890', name='ホッチキス中型', price=450),
            ProductMaster(code='9012345678901', name='クリアファイル20枚', price=280),
            ProductMaster(code='0123456789012', name='ポストイット75mm', price=220),
        ]
        
        for product in sample_products:
            session.add(product)
        
        session.commit()
        print(f"✅ {len(sample_products)}件の商品データを追加しました")
        
        # データ確認
        products = session.query(ProductMaster).all()
        print("\n📦 登録された商品:")
        for product in products:
            print(f"   - {product}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        session.close()


def verify_database():
    """データベース構造の検証"""
    print("=" * 60)
    print("🔍 データベース検証開始")
    print("=" * 60)
    
    session = SessionLocal()
    
    try:
        # テーブル確認
        with engine.connect() as connection:
            # テーブル一覧
            result = connection.execute(text("""
                SELECT 
                    TABLE_NAME,
                    TABLE_ROWS,
                    ENGINE,
                    TABLE_COLLATION
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """))
            
            print("\n📋 テーブル情報:")
            for row in result:
                print(f"   - {row[0]}: {row[1]}行, Engine={row[2]}, Collation={row[3]}")
            
            # カラム情報
            result = connection.execute(text("""
                SELECT 
                    TABLE_NAME,
                    COUNT(*) as ColumnCount
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                GROUP BY TABLE_NAME
                ORDER BY TABLE_NAME
            """))
            
            print("\n📝 カラム数:")
            for row in result:
                print(f"   - {row[0]}: {row[1]}カラム")
            
            # インデックス確認
            result = connection.execute(text("""
                SELECT 
                    TABLE_NAME,
                    INDEX_NAME,
                    NON_UNIQUE,
                    INDEX_TYPE
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                ORDER BY TABLE_NAME, INDEX_NAME
            """))
            
            print("\n📇 インデックス情報:")
            for row in result:
                unique_str = "UNIQUE" if row[2] == 0 else "NON-UNIQUE"
                print(f"   - {row[0]}.{row[1]} ({unique_str}, {row[3]})")
            
            # 外部キー制約確認
            result = connection.execute(text("""
                SELECT 
                    CONSTRAINT_NAME,
                    TABLE_NAME,
                    REFERENCED_TABLE_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                  AND REFERENCED_TABLE_NAME IS NOT NULL
                ORDER BY TABLE_NAME
            """))
            
            print("\n🔗 外部キー制約:")
            for row in result:
                print(f"   - {row[0]}: {row[1]} -> {row[2]}")
        
        # レコード数確認
        product_count = session.query(ProductMaster).count()
        transaction_count = session.query(Transaction).count()
        detail_count = session.query(TransactionDetail).count()
        
        print("\n📊 レコード数:")
        print(f"   - product_master: {product_count}件")
        print(f"   - transactions: {transaction_count}件")
        print(f"   - transaction_details: {detail_count}件")
        
        print("\n✅ データベース検証完了")
        
    except Exception as e:
        print(f"❌ 検証エラー: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        session.close()


def main():
    """メイン処理"""
    print("\n🚀 POSシステム データベースセットアップ (MySQL版)")
    print("=" * 60)
    
    # 接続テスト
    if not test_connection():
        print("❌ データベース接続に失敗しました")
        print("\n接続情報を確認してください:")
        print(f"  - DB_HOST: {os.getenv('DB_HOST')}")
        print(f"  - DB_PORT: {os.getenv('DB_PORT')}")
        print(f"  - DB_NAME: {os.getenv('DB_NAME')}")
        print(f"  - DB_USER: {os.getenv('DB_USER')}")
        sys.exit(1)
    
    print("\n以下の操作を選択してください:")
    print("1. テーブル作成")
    print("2. サンプルデータ追加")
    print("3. データベース検証")
    print("4. 全実行（テーブル作成 → サンプルデータ追加 → 検証）")
    print("9. 全テーブル削除（危険）")
    print("0. 終了")
    
    choice = input("\n選択してください (0-4, 9): ")
    
    if choice == '1':
        create_all_tables()
    elif choice == '2':
        add_sample_data()
    elif choice == '3':
        verify_database()
    elif choice == '4':
        if create_all_tables():
            add_sample_data()
            verify_database()
    elif choice == '9':
        drop_all_tables()
    elif choice == '0':
        print("終了します")
    else:
        print("無効な選択です")


if __name__ == "__main__":
    main()

