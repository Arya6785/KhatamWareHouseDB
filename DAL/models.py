from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .connection import Base


# ۱. جدول واحدها (Unit & Sub-Unit)
class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)  # مثلا: کارتن
    sub_unit_name = Column(String(50), nullable=True)  # مثلا: عدد
    ratio = Column(Float, default=1.0)  # مقدار در واحد (مثلا هر کارتن = ۲۴ عدد)


# ۲. جدول بخش‌ها / انبارها (Branch)
class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)  # مثلا: آزمایشگاه، انبار مرکزی


# ۳. جدول تولیدکننده
class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)

    products = relationship("Product", back_populates="manufacturer")


# ۴. جدول تامین‌کننده
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)

    products = relationship("Product", back_populates="supplier")


# ۵. جدول اصلی کالا
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    purchase_point = Column(Integer, nullable=True)
    usage_per_month = Column(Integer, nullable=True)
    quantity = Column(Integer, default=0)

    # کلیدهای خارجی برای ارتباط با جداول پایه
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)

    # روابط (Relationships)
    unit = relationship("Unit")
    branch = relationship("Branch")
    manufacturer = relationship("Manufacturer", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")