from .connection import SessionLocal
from .models import ProductMaster, Transaction, TransactionDetail
from datetime import datetime

def example_operations():
    """CRUD操作の例"""
    session = SessionLocal()
    
    try:
        print("=" * 60)
        print("🧪 CRUD操作テスト")
        print("=" * 60)
        
        # ===== 商品検索 =====
        print("\n🔍 商品検索 (CODE='1234567890123'):")
        product = session.query(ProductMaster).filter_by(code='1234567890123').first()
        if product:
            print(f"   商品: {product.name}, 価格: {product.price}円")
            print(f"   辞書形式: {product.to_dict()}")
        else:
            print("   商品が見つかりませんでした")
        
        # ===== 全商品取得 =====
        print("\n📦 全商品一覧:")
        products = session.query(ProductMaster).all()
        for p in products[:5]:  # 最初の5件のみ表示
            print(f"   - {p.code}: {p.name} ({p.price}円)")
        
        # ===== 価格で絞り込み =====
        print("\n💰 200円以下の商品:")
        cheap_products = session.query(ProductMaster).filter(
            ProductMaster.price <= 200
        ).all()
        for p in cheap_products:
            print(f"   - {p.name}: {p.price}円")
        
        # ===== 取引の作成 =====
        if product:
            print("\n🛒 新規取引作成:")
            new_transaction = Transaction(
                emp_cd='1234567890',
                store_cd='30',
                pos_no='90'
            )
            session.add(new_transaction)
            session.flush()  # IDを取得するためにflush
            
            print(f"   取引ID: {new_transaction.trd_id}")
            
            # 取引明細追加
            details = []
            detail1 = TransactionDetail(
                trd_id=new_transaction.trd_id,
                dtl_id=1,
                prd_id=product.prd_id,
                prd_code=product.code,
                prd_name=product.name,
                prd_price=product.price
            )
            session.add(detail1)
            details.append(detail1)
            
            # 2個目の商品を追加
            product2 = session.query(ProductMaster).filter_by(code='5678901234567').first()
            if product2:
                detail2 = TransactionDetail(
                    trd_id=new_transaction.trd_id,
                    dtl_id=2,
                    prd_id=product2.prd_id,
                    prd_code=product2.code,
                    prd_name=product2.name,
                    prd_price=product2.price
                )
                session.add(detail2)
                details.append(detail2)
            
            # 合計金額を計算して更新
            total_amount = sum(d.prd_price for d in details)
            new_transaction.total_amt = total_amount
            
            session.commit()
            print(f"   明細数: {len(details)}")
            print(f"   合計金額: {total_amount}円")
            print(f"   税込金額: {int(total_amount * 1.1)}円")
        
        # ===== 取引履歴の取得 =====
        print("\n📜 取引履歴（最新5件）:")
        transactions = session.query(Transaction).order_by(
            Transaction.datetime.desc()
        ).limit(5).all()
        
        for t in transactions:
            print(f"   - ID:{t.trd_id}, 日時:{t.datetime.strftime('%Y-%m-%d %H:%M:%S')}, "
                  f"金額:{t.total_amt}円, 明細数:{len(t.details)}")
            for detail in t.details:
                print(f"      └ {detail.prd_name} × 1: {detail.prd_price}円")
        
        # ===== 集計クエリ =====
        print("\n📊 売上集計:")
        from sqlalchemy import func
        
        result = session.query(
            func.count(Transaction.trd_id).label('count'),
            func.sum(Transaction.total_amt).label('total'),
            func.avg(Transaction.total_amt).label('average')
        ).first()
        
        print(f"   取引件数: {result.count}件")
        print(f"   売上合計: {result.total if result.total else 0}円")
        print(f"   平均単価: {int(result.average) if result.average else 0}円")
        
    except Exception as e:
        session.rollback()
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        session.close()

if __name__ == "__main__":
    example_operations()

