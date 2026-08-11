# DAL/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .connection import Base


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    phone = Column(String(20))
    adress = Column(String(200), nullable=True)


    products = relationship("Product", back_populates="manufacturer")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    adress = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)

    products = relationship("Product", back_populates="supplier")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=True)
    sub_unit = Column(String(20), nullable=True)
    branch = Column(String(50), nullable=True)
    quantity = Column(Integer, default=0)
    purchase_point = Column(Integer, nullable=True)
    usage_per_month = Column(Integer, nullable=True)
    


    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)

   
    manufacturer = relationship("Manufacturer", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")