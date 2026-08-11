# DAL/__init__.py
from .connection import engine, SessionLocal, Base
from .models import Product, Manufacturer, Supplier
from DAL import Bases
def init_db():
    # ساخت جداول در صورت عدم وجود
    Base.metadata.create_all(bind=engine)
    
    # پر کردن مقادیر اولیه در صورت خالی بودن دیتابیس
    db = SessionLocal()
    try:
        # اگر سازنده‌ای در دیتابیس نیست، از Bases پر کن
        if db.query(Manufacturer).count() == 0:
            for name in Bases.MANUFACTURERS:
                db.add(Manufacturer(name=name))
        
        # اگر تامین‌کننده‌ای در دیتابیس نیست، از Bases پر کن
        if db.query(Supplier).count() == 0:
            for name in Bases.SUPPLIERS:
                db.add(Supplier(name=name))
                
        db.commit()
    finally:
        db.close()