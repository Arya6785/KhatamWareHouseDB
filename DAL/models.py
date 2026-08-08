from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime


from .connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    branch = Column(String(100), nullable=False)

    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))

    manufacturer = relationship("Manufacturer", back_populates="products")

    suppliar_id = Column(Integer, ForeignKey('suppliars.id'))
    suppliar = relationship("Suppliar" , back_populates="products")


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    adress = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)

    Products = relationship("Product", back_populates="manufacturer")


class Suppliar(Base):
    __tablename__ = "suppliars"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    adress = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)

    Products = relationship("Product", back_populates="suppliar")
