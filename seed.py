import random
from DAL import SessionLocal, init_db, Product, Manufacturer, Supplier

# داده‌های پایه
MANUFACTURERS = ["Roche", "Abbotte", "دلتا درمان", "کاریزمهر", "من", "سامان تجهیز", "ایده ال تشخیص آتیه"]
SUPPLIERS = ["پخش مهرگان", "فرداور", "پارس پیوند"]
UNITS = ["کیت", "عدد", "میلی لیتر", "سی سی", "میلی گرم", "گرم", "لیتر", "بسته", "ویال", "دستگاه"]
SUB_UNITS = ["عدد", "میلی لیتر", "سی سی", "میلی گرم", "گرم", "لیتر", "ویال", "دستگاه"]

# لیست نمونه نام کالاها برای تست
SAMPLE_PRODUCTS = [
    "کیت استخراج DNA",
    "محیط کشت کشت سلولی",
    "محلول شستشوی سلولی",
    "سرم فیزیولوژی نپید",
    "دستگاه الایزا ریدر",
    "ویال آنتی‌بادی IgG",
    "کیت سنجش قند خون",
    "محلول بافر PBS",
    "لوله خون‌گیری خلاء",
    "ماده شیمیایی متانول HPLC",
    "محیط کشت بلاد آگار",
    "دستگاه سانتریفیوژ دور بالا",
    "پیپت مدرج ۱۰ میلی‌لیتر",
    "کیت تشخیص سریع کرونا",
    "محلول فرمالین ۱۰ درصد"
]

def seed_database():
    init_db()  # مطمئن شدن از ساخت جدول‌ها
    db = SessionLocal()

    try:
        print("🌱 در حال افزودن سازندگان...")
        mfg_objects = []
        for name in MANUFACTURERS:
            mfg = db.query(Manufacturer).filter(Manufacturer.name == name).first()
            if not mfg:
                mfg = Manufacturer(name=name)
                db.add(mfg)
                db.flush()
            mfg_objects.append(mfg)

        print("🌱 در حال افزودن تامین‌کنندگان...")
        supplier_objects = []
        for name in SUPPLIERS:
            sup = db.query(Supplier).filter(Supplier.name == name).first()
            if not sup:
                sup = Supplier(name=name)
                db.add(sup)
                db.flush()
            supplier_objects.append(sup)

        print("🌱 در حال ساخت داده‌های تصادفی محصولات...")
        for i, prod_name in enumerate(SAMPLE_PRODUCTS, start=101):
            # تولید کد کالای تصادفی مثل PRD-101
            code = f"PRD-{i}"

            # اگر کالا قبلا وجود نداشته اضافه کن
            existing_prod = db.query(Product).filter(Product.code == code).first()
            if not existing_prod:
                random_mfg = random.choice(mfg_objects)
                random_sup = random.choice(supplier_objects)
                random_unit = random.choice(UNITS)
                random_sub_unit = random.choice(SUB_UNITS)

                product = Product(
                    code=code,
                    name=prod_name,
                    manufacturer_id=random_mfg.id,
                    supplier_id=random_sup.id,
                    unit=random_unit,
                    sub_unit=random_sub_unit
                )
                db.add(product)

        db.commit()
        print("✅ ۱۵ داده تصادفی با موفقیت در دیتابیس ثبت شد!")

    except Exception as e:
        db.rollback()
        print(f"❌ خطا در افزودن داده‌ها: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()