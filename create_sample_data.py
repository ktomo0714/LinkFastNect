#!/usr/bin/env python3
"""
POSシステム用サンプルデータ作成スクリプト
仕様書に準拠したテストデータを生成します
"""

from db_control.connection import SessionLocal, test_connection
from db_control.models import ProductMaster, Transaction, TransactionDetail
from datetime import datetime, timedelta
import random

def create_sample_data():
    """サンプルデータを作成"""
    if not test_connection():
        print("❌ データベース接続に失敗しました")
        return False
    
    session = SessionLocal()
    
    try:
        print("=" * 60)
        print("📦 サンプルデータ作成開始")
        print("=" * 60)
        
        # 既存データをクリア
        print("🗑️  既存データをクリア中...")
        session.query(TransactionDetail).delete()
        session.query(Transaction).delete()
        session.query(ProductMaster).delete()
        session.commit()
        
        # 商品マスタデータ作成
        print("🛍️  商品マスタデータ作成中...")
        products_data = [
            {"code": "1234567890123", "name": "コーラ（500ml）", "price": 150},
            {"code": "2345678901234", "name": "お茶（500ml）", "price": 120},
            {"code": "3456789012345", "name": "コーヒー（350ml）", "price": 180},
            {"code": "4567890123456", "name": "サンドイッチ", "price": 350},
            {"code": "5678901234567", "name": "おにぎり（梅干し）", "price": 120},
            {"code": "6789012345678", "name": "おにぎり（鮭）", "price": 150},
            {"code": "7890123456789", "name": "チョコレート", "price": 100},
            {"code": "8901234567890", "name": "ガム", "price": 80},
            {"code": "9012345678901", "name": "アイスクリーム", "price": 200},
            {"code": "0123456789012", "name": "カップラーメン", "price": 250},
        ]
        
        products = []
        for data in products_data:
            product = ProductMaster(**data)
            session.add(product)
            products.append(product)
        
        session.commit()
        print(f"   ✅ {len(products)}件の商品を登録しました")
        
        # 取引データ作成（過去30日分）
        print("💳 取引データ作成中...")
        transactions_created = 0
        
        for day in range(30):
            # 1日あたり5-15件の取引をランダムに生成
            num_transactions = random.randint(5, 15)
            
            for _ in range(num_transactions):
                # 取引作成
                transaction = Transaction(
                    datetime=datetime.now() - timedelta(days=day, hours=random.randint(8, 20), minutes=random.randint(0, 59)),
                    emp_cd=f"{random.randint(1000000000, 9999999999)}",
                    store_cd="30",  # 固定値
                    pos_no="90",    # 固定値
                    total_amt=0
                )
                session.add(transaction)
                session.flush()
                
                # 取引明細作成（1-5個の商品）
                num_items = random.randint(1, 5)
                selected_products = random.sample(products, num_items)
                total_amount = 0
                
                for idx, product in enumerate(selected_products, start=1):
                    detail = TransactionDetail(
                        trd_id=transaction.trd_id,
                        dtl_id=idx,
                        prd_id=product.prd_id,
                        prd_code=product.code,
                        prd_name=product.name,
                        prd_price=product.price
                    )
                    session.add(detail)
                    total_amount += product.price
                
                # 合計金額更新
                transaction.total_amt = total_amount
                transactions_created += 1
        
        session.commit()
        print(f"   ✅ {transactions_created}件の取引を登録しました")
        
        # 統計情報表示
        print("\n📊 作成されたデータ統計:")
        product_count = session.query(ProductMaster).count()
        transaction_count = session.query(Transaction).count()
        detail_count = session.query(TransactionDetail).count()
        total_sales = session.query(Transaction).with_entities(
            session.query(Transaction).with_entities(Transaction.total_amt).label('total')
        ).scalar() or 0
        
        print(f"   - 商品数: {product_count}件")
        print(f"   - 取引数: {transaction_count}件")
        print(f"   - 明細数: {detail_count}件")
        print(f"   - 総売上: {total_sales:,}円")
        
        print("\n✅ サンプルデータ作成完了!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        session.rollback()
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()

if __name__ == "__main__":
    create_sample_data()
