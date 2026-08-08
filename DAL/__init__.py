# DAL/__init__.py

from .connection import engine, SessionLocal, Base
from .models import Product, Manufacturer, Suppliar

def init_db():
    """این تابع تمام جداول تعریف شده در models.py را در دیتابیس می‌سازد"""
    Base.metadata.create_all(bind=engine)