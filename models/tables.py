from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import *
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from models.shopping_database import ShoppingDatabase

Base = declarative_base()
db = ShoppingDatabase()


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    url = Column(TEXT, comment='홈페이지 주소', nullable=False)
    name = Column(VARCHAR(255), comment='이름', nullable=False)
    price = Column(BIGINT(unsigned=True), comment='가격', nullable=False)
    courier = Column(VARCHAR(20), comment='택배사', nullable=False)
    delivery_charge = Column(BIGINT(unsigned=True), comment='배송비', nullable=False)
    arrival_date = Column(VARCHAR(20), comment='도착 날짜', nullable=False)
    arrival_probability = Column(TINYINT(unsigned=True), comment='도착 확률', nullable=True)
    benefit = Column(JSON, comment='수량', nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, comment='생성 날짜', default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, comment='업데이트 날짜', onupdate=datetime.now(), default=datetime.now())

    product_image = relationship("ProductImageModel", back_populates="product")
    product_option = relationship("ProductOptionModel", back_populates="product")


class ProductImageModel(Base):
    __tablename__ = "product_images"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    product_id = Column(BIGINT(unsigned=True), ForeignKey('products.id'), nullable=False)
    url = Column(TEXT, comment='이미지 주소', nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, comment='생성 날짜', default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, comment='업데이트 날짜', onupdate=datetime.now(), default=datetime.now())

    product = relationship("ProductModel", back_populates="product_image")


class ProductOptionModel(Base):
    __tablename__ = "product_options"
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    product_id = Column(BIGINT(unsigned=True), ForeignKey('products.id'), nullable=False)
    option = Column(
        JSON,
        comment="옵션",
        nullable=False
    )
    created_at = Column(TIMESTAMP, nullable=False, comment='생성 날짜', default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, comment='업데이트 날짜', onupdate=datetime.now(), default=datetime.now())

    product = relationship("ProductModel", back_populates="product_option")


if __name__ == '__main__':
    try:
        option = input('Choose Create or Drop[c/r/d] : ')
        if option == 'c':
            Base.metadata.create_all(db.connect)
        elif option == 'r':
            Base.metadata.drop_all(db.connect)
            Base.metadata.create_all(db.connect)
        elif option == 'd':
            Base.metadata.drop_all(db.connect)
        else:
            print('Wrong input value. Please try again.')
    except Exception as e:
        raise e
