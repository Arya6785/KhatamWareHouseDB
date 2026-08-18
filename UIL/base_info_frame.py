import customtkinter as ctk
from tkinter import messagebox, ttk
from DAL import SessionLocal, Unit, Branch, Manufacturer, Supplier
import arabic_reshaper
from bidi.algorithm import get_display

from DAL.models import Product


def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))


class BaseInfoFrame(ctk.CTkFrame):
    def __init__(self, master, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_back = on_back
        
        # --- هدر صفحه ---
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=(15, 5))

        if self.on_back:
            self.back_btn = ctk.CTkButton(
                self.header,
                text=fa("← بازگشت به منو"),
                fg_color="#a83232",
                hover_color="#7a2323",
                font=("Tahoma", 12, "bold"),
                width=110,
                command=self.on_back
            )
            self.back_btn.pack(side="right", padx=(0, 15))

        self.title_label = ctk.CTkLabel(
            self.header,
            text=fa("مدیریت اطلاعات پایه"),
            font=("Tahoma", 20, "bold")
        )
        self.title_label.pack(side="right")

        # --- ایجاد تب‌ها ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_units = self.tabview.add(fa("واحدها"))
        self.tab_branches = self.tabview.add(fa("نام بخش‌ها"))
        self.tab_mfgs = self.tabview.add(fa("تولیدکنندگان"))
        self.tab_sups = self.tabview.add(fa("تامین‌کنندگان"))
        self.tab_products = self.tabview.add(fa("محصولات"))  # اضافه کردن تب مدیریت محصولات
    

        # تعریف فرم‌های هر تب
        self._setup_units_tab()
        self._setup_branches_tab()
        self._setup_mfgs_tab()
        self._setup_sups_tab()
        self._setup_products_tab()  # اضافه کردن تب مدیریت محصولات

    # ---------------- ۱. مدیریت واحدها ----------------
    def _setup_units_tab(self):
        frame = self.tab_units

        ctk.CTkLabel(frame, text=fa("نام واحد اصلی (مثلاً کارتن):"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(10, 2))
        unit_name_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        unit_name_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("نام واحد فرعی (مثلاً عدد):"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        sub_unit_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        sub_unit_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("تعداد در واحد (ضریب):"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        ratio_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300, placeholder_text="1")
        ratio_ent.pack(pady=2)

        def save_unit():
            u_name = unit_name_ent.get().strip()
            su_name = sub_unit_ent.get().strip()
            ratio_raw = ratio_ent.get().strip() or "1"

            if not u_name:
                messagebox.showwarning("خطا", fa("نام واحد اصلی الزامی است."))
                return

            try:
                ratio_val = float(ratio_raw)
            except ValueError:
                messagebox.showerror("خطا", fa("ضریب باید عددی باشد."))
                return

            db = SessionLocal()
            try:
                new_u = Unit(name=u_name, sub_unit_name=su_name, ratio=ratio_val)
                db.add(new_u)
                db.commit()
                messagebox.showinfo("موفقیت", fa("واحد جدید با موفقیت ثبت شد."))
                unit_name_ent.delete(0, "end")
                sub_unit_ent.delete(0, "end")
                ratio_ent.delete(0, "end")
            finally:
                db.close()

        ctk.CTkButton(frame, text=fa("ذخیره واحد"), fg_color="green", command=save_unit, width=200).pack(pady=20)

    # ---------------- ۲. مدیریت بخش‌ها ----------------
    def _setup_branches_tab(self):
        frame = self.tab_branches

        ctk.CTkLabel(frame, text=fa("نام بخش / انبار:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(20, 2))
        branch_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        branch_ent.pack(pady=5)

        def save_branch():
            b_name = branch_ent.get().strip()
            if not b_name:
                messagebox.showwarning("خطا", fa("نام بخش الزامی است."))
                return

            db = SessionLocal()
            try:
                db.add(Branch(name=b_name))
                db.commit()
                messagebox.showinfo("موفقیت", fa("بخش جدید ثبت شد."))
                branch_ent.delete(0, "end")
            except Exception:
                db.rollback()
                messagebox.showerror("خطا", fa("این بخش قبلاً ثبت شده است."))
            finally:
                db.close()

        ctk.CTkButton(frame, text=fa("ذخیره بخش"), fg_color="green", command=save_branch, width=200).pack(pady=20)

    # ---------------- ۳. مدیریت تولیدکنندگان ----------------
    def _setup_mfgs_tab(self):
        frame = self.tab_mfgs

        ctk.CTkLabel(frame, text=fa("نام شرکت تولیدکننده:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(10, 2))
        name_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        name_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("شماره تماس:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        phone_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        phone_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("آدرس:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        addr_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        addr_ent.pack(pady=2)

        def save_mfg():
            name = name_ent.get().strip()
            if not name:
                messagebox.showwarning("خطا", fa("نام تولیدکننده الزامی است."))
                return

            db = SessionLocal()
            try:
                db.add(Manufacturer(name=name, phone=phone_ent.get().strip(), address=addr_ent.get().strip()))
                db.commit()
                messagebox.showinfo("موفقیت", fa("تولیدکننده ثبت شد."))
                name_ent.delete(0, "end")
                phone_ent.delete(0, "end")
                addr_ent.delete(0, "end")
            finally:
                db.close()

        ctk.CTkButton(frame, text=fa("ذخیره تولیدکننده"), fg_color="green", command=save_mfg, width=200).pack(pady=20)

    # ---------------- ۴. مدیریت تامین‌کنندگان ----------------
    def _setup_sups_tab(self):
        frame = self.tab_sups

        ctk.CTkLabel(frame, text=fa("نام تامین‌کننده:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(10, 2))
        name_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        name_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("شماره تماس:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        phone_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        phone_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("آدرس:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        addr_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        addr_ent.pack(pady=2)

        def save_sup():
            name = name_ent.get().strip()
            if not name:
                messagebox.showwarning("خطا", fa("نام تامین‌کننده الزامی است."))
                return

            db = SessionLocal()
            try:
                db.add(Supplier(name=name, phone=phone_ent.get().strip(), address=addr_ent.get().strip()))
                db.commit()
                messagebox.showinfo("موفقیت", fa("تامین‌کننده ثبت شد."))
                name_ent.delete(0, "end")
                phone_ent.delete(0, "end")
                addr_ent.delete(0, "end")
            finally:
                db.close()

        ctk.CTkButton(frame, text=fa("ذخیره تامین‌کننده"), fg_color="green", command=save_sup, width=200).pack(pady=20)

    def _setup_products_tab(self):
        frame = self.tab_products

        ctk.CTkLabel(frame, text=fa("نام محصول:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(10, 2))
        name_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        name_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("کد محصول:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        code_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        code_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("نقطه سفارش:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        reorder_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        reorder_ent.pack(pady=2)

        ctk.CTkLabel(frame, text=fa("میزان مصرف ماهانه:"), font=("Tahoma", 11)).pack(anchor="e", padx=20, pady=(8, 2))
        consumption_ent = ctk.CTkEntry(frame, font=("Tahoma", 11), width=300)
        consumption_ent.pack(pady=2)


        def save_product():
            frame = self.tab_products
            name = name_ent.get().strip()
            code = code_ent.get().strip()
            reorder = reorder_ent.get().strip()
            consumption = consumption_ent.get().strip()

            if not name or not code:
                messagebox.showwarning("خطا", fa("نام و کد محصول الزامی است."))
                return

            db = SessionLocal()
            try:
                db.add(Product(name=name, code=code, purchase_point=reorder, usage_per_month=consumption))
                db.commit()
                messagebox.showinfo("موفقیت", fa("محصول ثبت شد."))
                name_ent.delete(0, "end")
                code_ent.delete(0, "end")
                reorder_ent.delete(0, "end")
                consumption_ent.delete(0, "end")
            finally:
                db.close()
        ctk.CTkButton(frame, text=fa("ذخیره محصول"), fg_color="green", command=save_product, width=200).pack(pady=20)

        # ... ادامه فرم ثبت محصول