# db_control/models.py

from sqlalchemy import (
    Column, Integer, String, DateTime,
    ForeignKey, Index
)
from sqlalchemy.orm import relationship
from .connection import Base
from datetime import datetime


# 商品マスタテーブル
class ProductMaster(Base):
    __tablename__ = "product_master"

    prd_id = Column(Integer, primary_key=True, autoincrement=True, comment="商品一意キー")
    code = Column(String(13), nullable=False, comment="商品コード（13桁）")
    name = Column(String(50), nullable=False, comment="商品名称")
    price = Column(Integer, nullable=False, comment="商品単価")

    # リレーション設定
    transaction_details = relationship("TransactionDetail", back_populates="product")
    
    # Check条件でUNIQUE制御（仕様書準拠）
    __table_args__ = (
        Index("ix_product_master_code", "code", unique=True),
    )


# 取引テーブル
class Transaction(Base):
    __tablename__ = "transactions"

    trd_id = Column(Integer, primary_key=True, autoincrement=True, comment="取引一意キー")
    datetime = Column(DateTime, nullable=False, default=datetime.now, comment="取引日時")
    emp_cd = Column(String(10), nullable=False, default="9999999999", comment="レジ担当者コード")
    store_cd = Column(String(5), nullable=False, default="30", comment="店舗コード（固定値）")
    pos_no = Column(String(3), nullable=False, default="90", comment="POS機ID（固定値：モバイルPOS）")
    total_amt = Column(Integer, nullable=False, default=0, comment="合計金額")

    details = relationship("TransactionDetail", back_populates="transaction")

    __table_args__ = (Index("ix_transactions_datetime", "datetime"),)


# 取引明細テーブル
class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    trd_id = Column(Integer, ForeignKey("transactions.trd_id", ondelete="CASCADE"), primary_key=True, comment="取引一意キー")
    dtl_id = Column(Integer, primary_key=True, comment="取引明細一意キー")

    # 外部キー設定
    prd_id = Column(Integer, ForeignKey("product_master.prd_id"), nullable=False, comment="商品一意キー")

    prd_code = Column(String(13), nullable=False, comment="商品コード")
    prd_name = Column(String(50), nullable=False, comment="商品名称")
    prd_price = Column(Integer, nullable=False, comment="商品単価")

    # リレーション設定
    product = relationship("ProductMaster", back_populates="transaction_details")
    transaction = relationship("Transaction", back_populates="details")

    __table_args__ = (Index("ix_transaction_details_prd_id", "prd_id"),)
