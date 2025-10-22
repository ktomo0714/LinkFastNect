# app.py
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import os

from db_control.connection import get_db, test_connection
from db_control.models import ProductMaster, Transaction, TransactionDetail


# ===== Lifespan イベントハンドラー =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時処理
    print("=" * 60)
    print("🚀 POS System API 起動中...")
    print("=" * 60)
    
    if test_connection():
        print("✅ データベース接続確認完了")
    else:
        print("⚠️  データベース接続に問題があります")
    
    print("=" * 60)
    
    yield
    
    # 終了時処理
    print("=" * 60)
    print("👋 POS System API 終了")
    print("=" * 60)


# FastAPIアプリケーションの初期化
app = FastAPI(
    title="POS System API",
    description="POSシステム バックエンドAPI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Pydanticモデル（リクエスト/レスポンス） =====

class ProductResponse(BaseModel):
    prd_id: int
    code: str
    name: str
    price: int
    
    class Config:
        from_attributes = True


class TransactionDetailResponse(BaseModel):
    dtl_id: int
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int
    
    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    trd_id: int
    datetime: datetime
    emp_cd: str
    store_cd: str
    pos_no: str
    total_amt: int
    details: List[TransactionDetailResponse] = []
    
    class Config:
        from_attributes = True


class TransactionDetailCreate(BaseModel):
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int


class TransactionCreate(BaseModel):
    emp_cd: str = Field(default="9999999999", max_length=10)
    store_cd: str = Field(default="30", max_length=5)
    pos_no: str = Field(default="90", max_length=3)
    details: List[TransactionDetailCreate]


class SalesStatistics(BaseModel):
    total_transactions: int
    total_sales: int
    average_sale: int
    total_items: int


# ===== ヘルスチェック =====

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "POS System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "timestamp": datetime.now().isoformat()
    }


# ===== 商品マスタ API =====

@app.get("/api/products", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """商品一覧取得"""
    query = db.query(ProductMaster)
    
    if search:
        query = query.filter(
            (ProductMaster.code.like(f"%{search}%")) |
            (ProductMaster.name.like(f"%{search}%"))
        )
    
    products = query.offset(skip).limit(limit).all()
    return products


@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """商品詳細取得"""
    product = db.query(ProductMaster).filter(
        ProductMaster.prd_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    return product


@app.get("/api/products/code/{code}", response_model=ProductResponse)
async def get_product_by_code(code: str, db: Session = Depends(get_db)):
    """商品コードで商品取得"""
    product = db.query(ProductMaster).filter(
        ProductMaster.code == code
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    return product


@app.post("/api/products", response_model=ProductResponse)
async def create_product(
    code: str = Query(..., min_length=13, max_length=13),
    name: str = Query(..., min_length=1, max_length=50),
    price: int = Query(..., ge=0),
    db: Session = Depends(get_db)
):
    """商品登録"""
    # 重複チェック
    existing = db.query(ProductMaster).filter(
        ProductMaster.code == code
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="商品コードが既に存在します")
    
    product = ProductMaster(code=code, name=name, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product


@app.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    price: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_db)
):
    """商品更新"""
    product = db.query(ProductMaster).filter(
        ProductMaster.prd_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    
    db.commit()
    db.refresh(product)
    
    return product


@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """商品削除"""
    product = db.query(ProductMaster).filter(
        ProductMaster.prd_id == product_id
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    db.delete(product)
    db.commit()
    
    return {"message": "商品を削除しました", "prd_id": product_id}


# ===== 取引 API =====

@app.get("/api/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    store_cd: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """取引一覧取得"""
    query = db.query(Transaction)
    
    if start_date:
        query = query.filter(Transaction.datetime >= start_date)
    if end_date:
        query = query.filter(Transaction.datetime <= end_date)
    if store_cd:
        query = query.filter(Transaction.store_cd == store_cd)
    
    transactions = query.order_by(
        Transaction.datetime.desc()
    ).offset(skip).limit(limit).all()
    
    return transactions


@app.get("/api/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """取引詳細取得"""
    transaction = db.query(Transaction).filter(
        Transaction.trd_id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="取引が見つかりません")
    
    return transaction


@app.post("/api/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):
    """取引登録"""
    if not transaction_data.details:
        raise HTTPException(status_code=400, detail="明細が必要です")
    
    # 取引作成
    transaction = Transaction(
        datetime=datetime.now(),
        emp_cd=transaction_data.emp_cd,
        store_cd=transaction_data.store_cd,
        pos_no=transaction_data.pos_no,
        total_amt=0
    )
    db.add(transaction)
    db.flush()
    
    # 明細追加
    total_amount = 0
    for idx, detail_data in enumerate(transaction_data.details, start=1):
        # 商品存在チェック
        product = db.query(ProductMaster).filter(
            ProductMaster.prd_id == detail_data.prd_id
        ).first()
        
        if not product:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail=f"商品ID {detail_data.prd_id} が見つかりません"
            )
        
        detail = TransactionDetail(
            trd_id=transaction.trd_id,
            dtl_id=idx,
            prd_id=detail_data.prd_id,
            prd_code=detail_data.prd_code,
            prd_name=detail_data.prd_name,
            prd_price=detail_data.prd_price
        )
        db.add(detail)
        total_amount += detail_data.prd_price
    
    # 合計金額更新
    transaction.total_amt = total_amount
    
    db.commit()
    db.refresh(transaction)
    
    return transaction


@app.delete("/api/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """取引削除"""
    transaction = db.query(Transaction).filter(
        Transaction.trd_id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="取引が見つかりません")
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "取引を削除しました", "trd_id": transaction_id}


# ===== 統計・分析 API =====

@app.get("/api/statistics/sales", response_model=SalesStatistics)
async def get_sales_statistics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    store_cd: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """売上統計取得"""
    query = db.query(
        func.count(Transaction.trd_id).label('count'),
        func.sum(Transaction.total_amt).label('total'),
        func.avg(Transaction.total_amt).label('average')
    )
    
    if start_date:
        query = query.filter(Transaction.datetime >= start_date)
    if end_date:
        query = query.filter(Transaction.datetime <= end_date)
    if store_cd:
        query = query.filter(Transaction.store_cd == store_cd)
    
    result = query.first()
    
    # 明細数カウント
    detail_query = db.query(func.count(TransactionDetail.dtl_id))
    if start_date or end_date or store_cd:
        detail_query = detail_query.join(Transaction)
        if start_date:
            detail_query = detail_query.filter(Transaction.datetime >= start_date)
        if end_date:
            detail_query = detail_query.filter(Transaction.datetime <= end_date)
        if store_cd:
            detail_query = detail_query.filter(Transaction.store_cd == store_cd)
    
    item_count = detail_query.scalar()
    
    return SalesStatistics(
        total_transactions=result.count or 0,
        total_sales=result.total or 0,
        average_sale=int(result.average) if result.average else 0,
        total_items=item_count or 0
    )


@app.get("/api/statistics/top-products")
async def get_top_products(
    limit: int = Query(10, ge=1, le=100),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """売れ筋商品ランキング"""
    query = db.query(
        TransactionDetail.prd_id,
        TransactionDetail.prd_name,
        func.count(TransactionDetail.prd_id).label('sales_count'),
        func.sum(TransactionDetail.prd_price).label('total_sales')
    )
    
    if start_date or end_date:
        query = query.join(Transaction)
        if start_date:
            query = query.filter(Transaction.datetime >= start_date)
        if end_date:
            query = query.filter(Transaction.datetime <= end_date)
    
    results = query.group_by(
        TransactionDetail.prd_id,
        TransactionDetail.prd_name
    ).order_by(
        func.count(TransactionDetail.prd_id).desc()
    ).limit(limit).all()
    
    return [
        {
            "prd_id": r.prd_id,
            "prd_name": r.prd_name,
            "sales_count": r.sales_count,
            "total_sales": r.total_sales
        }
        for r in results
    ]


@app.get("/api/statistics/hourly-sales")
async def get_hourly_sales(
    date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """時間帯別売上"""
    if date is None:
        date = datetime.now().date()
    
    start = datetime.combine(date, datetime.min.time())
    end = datetime.combine(date, datetime.max.time())
    
    results = db.query(
        func.hour(Transaction.datetime).label('hour'),
        func.count(Transaction.trd_id).label('count'),
        func.sum(Transaction.total_amt).label('total')
    ).filter(
        and_(
            Transaction.datetime >= start,
            Transaction.datetime <= end
        )
    ).group_by(
        func.hour(Transaction.datetime)
    ).order_by('hour').all()
    
    return [
        {
            "hour": r.hour,
            "count": r.count,
            "total": r.total or 0
        }
        for r in results
    ]


# ===== エラーハンドリング =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    
    # 環境変数からポートを取得（Azure App Serviceではポート8000を使用）
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False  # 本番環境ではFalse
    )