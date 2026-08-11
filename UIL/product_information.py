import customtkinter as ctk
from tkinter import messagebox
from DAL import SessionLocal, Product, Manufacturer, Supplier, Bases
import arabic_reshaper
from bidi.algorithm import get_display
from BLL.persian_check import far


def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))


class AddProductFrame(ctk.CTkFrame):
    def __init__(self, master, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_back = on_back

        # دریافت نقشه کامل اطلاعات سازندگان و تامین‌کنندگان (شامل آی‌دی، تلفن و آدرس)
        self.mfg_data_map = self.get_manufacturers_data()
        self.sup_data_map = self.get_suppliers_data()

        # --- ۱. هدر بالا (عنوان + دکمه برگشت) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(15, 5))

        if self.on_back:
            self.back_btn = ctk.CTkButton(
                self.header_frame,
                text=fa("← بازگشت به منو"),
                fg_color="#a83232",
                hover_color="#7a2323",
                font=("Tahoma", 12, "bold"),
                width=120,
                height=38,
                command=self.on_back
            )
            self.back_btn.pack(side="right", padx=(0, 15))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=fa("فرم ثبت کالای جدید"),
            font=("Tahoma", 20, "bold")
        )
        self.title_label.pack(side="right")

        # --- ۲. کارت اصلی فرم (دو ستونه برای ابعاد 1280x750) ---
        self.form_card = ctk.CTkFrame(self, corner_radius=12)
        self.form_card.pack(fill="both", expand=True, padx=30, pady=(10, 15))
        self.form_card.grid_columnconfigure((0, 1), weight=1, uniform="col")

        # ==================== ستون راست (اطلاعات کالا و سازنده) ====================
        # کد کالا
        self.code_label = ctk.CTkLabel(self.form_card, text=fa("کد کالا (الزامی):"), font=("Tahoma", 11, "bold"))
        self.code_label.grid(row=0, column=1, sticky="e", padx=(10, 30), pady=(12, 1))
        self.code_entry = ctk.CTkEntry(self.form_card, placeholder_text=fa("مثلاً: PRD-101"), font=("Tahoma", 11), height=35)
        self.code_entry.grid(row=1, column=1, sticky="ew", padx=(10, 30), pady=(0, 6))

        # نام کالا
        self.name_label = ctk.CTkLabel(self.form_card, text=fa("نام کالا (الزامی):"), font=("Tahoma", 11, "bold"))
        self.name_label.grid(row=2, column=1, sticky="e", padx=(10, 30), pady=(4, 1))
        self.name_entry = ctk.CTkEntry(self.form_card, placeholder_text=fa("نام کامل کالا"), font=("Tahoma", 11), height=35)
        self.name_entry.grid(row=3, column=1, sticky="ew", padx=(10, 30), pady=(0, 6))

        # شعبه / بخش (Branch)
        self.branch_label = ctk.CTkLabel(self.form_card, text=fa("شعبه / بخش / انبار:"), font=("Tahoma", 11, "bold"))
        self.branch_label.grid(row=4, column=1, sticky="e", padx=(10, 30), pady=(4, 1))
        branches_list = [far(b) for b in getattr(Bases, "BRANCHES", ["مرکزی", "انبار ۱", "انبار ۲", "آزمایشگاه"])]
        self.branch_combo = ctk.CTkComboBox(self.form_card, values=branches_list, font=("Tahoma", 11), height=35)
        self.branch_combo.grid(row=5, column=1, sticky="ew", padx=(10, 30), pady=(0, 6))

        # سازنده / برند
        self.mfg_label = ctk.CTkLabel(self.form_card, text=fa("سازنده / شرکت:"), font=("Tahoma", 11, "bold"))
        self.mfg_label.grid(row=6, column=1, sticky="e", padx=(10, 30), pady=(4, 1))
        mfg_options = list(self.mfg_data_map.keys())
        self.mfg_combo = ctk.CTkComboBox(
            self.form_card, 
            values=mfg_options, 
            font=("Tahoma", 11), 
            height=35,
            command=self.on_mfg_change
        )
        self.mfg_combo.grid(row=7, column=1, sticky="ew", padx=(10, 30), pady=(0, 6))

        # تلفن سازنده
        self.mfg_phone_label = ctk.CTkLabel(self.form_card, text=fa("شماره تماس سازنده:"), font=("Tahoma", 10))
        self.mfg_phone_label.grid(row=8, column=1, sticky="e", padx=(10, 30), pady=(2, 1))
        self.mfg_phone_entry = ctk.CTkEntry(self.form_card, font=("Tahoma", 11), height=32, placeholder_text="-")
        self.mfg_phone_entry.grid(row=9, column=1, sticky="ew", padx=(10, 30), pady=(0, 6))

        # آدرس سازنده
        self.mfg_addr_label = ctk.CTkLabel(self.form_card, text=fa("آدرس شرکت سازنده:"), font=("Tahoma", 10))
        self.mfg_addr_label.grid(row=10, column=1, sticky="e", padx=(10, 30), pady=(2, 1))
        self.mfg_addr_entry = ctk.CTkEntry(self.form_card, font=("Tahoma", 11), height=32, placeholder_text="-")
        self.mfg_addr_entry.grid(row=11, column=1, sticky="ew", padx=(10, 30), pady=(0, 10))


        # ==================== ستون چپ (تامین‌کننده و واحدها) ====================
        # تامین‌کننده
        self.sup_label = ctk.CTkLabel(self.form_card, text=fa("تامین‌کننده:"), font=("Tahoma", 11, "bold"))
        self.sup_label.grid(row=0, column=0, sticky="e", padx=(30, 10), pady=(12, 1))
        sup_options = list(self.sup_data_map.keys())
        self.supplier_combo = ctk.CTkComboBox(
            self.form_card, 
            values=sup_options, 
            font=("Tahoma", 11), 
            height=35,
            command=self.on_sup_change
        )
        self.supplier_combo.grid(row=1, column=0, sticky="ew", padx=(30, 10), pady=(0, 6))

        # تلفن تامین‌کننده
        self.sup_phone_label = ctk.CTkLabel(self.form_card, text=fa("شماره تماس تامین‌کننده:"), font=("Tahoma", 10))
        self.sup_phone_label.grid(row=2, column=0, sticky="e", padx=(30, 10), pady=(2, 1))
        self.sup_phone_entry = ctk.CTkEntry(self.form_card, font=("Tahoma", 11), height=32, placeholder_text="-")
        self.sup_phone_entry.grid(row=3, column=0, sticky="ew", padx=(30, 10), pady=(0, 6))

        # آدرس تامین‌کننده
        self.sup_addr_label = ctk.CTkLabel(self.form_card, text=fa("آدرس تامین‌کننده:"), font=("Tahoma", 10))
        self.sup_addr_label.grid(row=4, column=0, sticky="e", padx=(30, 10), pady=(2, 1))
        self.sup_addr_entry = ctk.CTkEntry(self.form_card, font=("Tahoma", 11), height=32, placeholder_text="-")
        self.sup_addr_entry.grid(row=5, column=0, sticky="ew", padx=(30, 10), pady=(0, 6))

        # واحد اصلی و فرعی
        self.unit_label = ctk.CTkLabel(self.form_card, text=fa("واحد اصلی سنجش:"), font=("Tahoma", 11, "bold"))
        self.unit_label.grid(row=6, column=0, sticky="e", padx=(30, 10), pady=(4, 1))
        units_list = [far(u) for u in getattr(Bases, "UNITS", ["عدد", "کیلوگرم", "بسته"])]
        self.unit_combo = ctk.CTkComboBox(self.form_card, values=units_list, font=("Tahoma", 11), height=35)
        self.unit_combo.grid(row=7, column=0, sticky="ew", padx=(30, 10), pady=(0, 6))

        self.sub_unit_label = ctk.CTkLabel(self.form_card, text=fa("واحد فرعی سنجش:"), font=("Tahoma", 11, "bold"))
        self.sub_unit_label.grid(row=8, column=0, sticky="e", padx=(30, 10), pady=(2, 1))
        sub_units_list = [far(su) for su in getattr(Bases, "SUB_UNITS", ["عدد", "کارتن", "جین"])]
        self.sub_unit_combo = ctk.CTkComboBox(self.form_card, values=sub_units_list, font=("Tahoma", 11), height=35)
        self.sub_unit_combo.grid(row=9, column=0, sticky="ew", padx=(30, 10), pady=(0, 6))

        # نقطه سفارش و مصرف ماهانه
        self.pp_label = ctk.CTkLabel(self.form_card, text=fa("نقطه سفارش (عددی):"), font=("Tahoma", 11, "bold"))
        self.pp_label.grid(row=10, column=0, sticky="e", padx=(30, 10), pady=(2, 1))
        self.pp_entry = ctk.CTkEntry(self.form_card, placeholder_text=fa("مثلاً: 10"), font=("Tahoma", 11), height=32)
        self.pp_entry.grid(row=11, column=0, sticky="ew", padx=(30, 10), pady=(0, 10))

        # --- دکمه ذخیره کالا ---
        self.save_button = ctk.CTkButton(
            self.form_card,
            text=fa("💾 ذخیره کالا در دیتابیس"),
            fg_color="#28a745",
            hover_color="#1e7e34",
            font=("Tahoma", 13, "bold"),
            height=40,
            command=self.save_product
        )
        self.save_button.grid(row=12, column=0, columnspan=2, sticky="ew", padx=80, pady=(10, 15))

    def get_manufacturers_data(self):
        """دریافت لیست سازندگان به همراه id, phone, address"""
        db = SessionLocal()
        mapping = {fa("انتخاب نشده"): {"id": None, "phone": "", "address": ""}}
        try:
            mfgs = db.query(Manufacturer).all()
            for m in mfgs:
                if m.name:
                    mapping[far(m.name)] = {
                        "id": m.id,
                        "phone": m.phone or "",
                        "address": m.adress or ""
                    }
        except Exception:
            pass
        finally:
            db.close()
        return mapping

    def get_suppliers_data(self):
        """دریافت لیست تامین‌کنندگان به همراه id, phone, address"""
        db = SessionLocal()
        mapping = {fa("انتخاب نشده"): {"id": None, "phone": "", "address": ""}}
        try:
            sups = db.query(Supplier).all()
            for s in sups:
                if s.name:
                    mapping[far(s.name)] = {
                        "id": s.id,
                        "phone": s.phone or "",
                        "address": s.adress or ""
                    }
        except Exception:
            pass
        finally:
            db.close()
        return mapping

    def on_mfg_change(self, choice):
        """تغییر خودکار تلفن و آدرس با انتخاب سازنده"""
        info = self.mfg_data_map.get(choice, {"phone": "", "address": ""})
        self.mfg_phone_entry.delete(0, "end")
        self.mfg_phone_entry.insert(0, info["phone"])
        
        self.mfg_addr_entry.delete(0, "end")
        self.mfg_addr_entry.insert(0, info["address"])

    def on_sup_change(self, choice):
        """تغییر خودکار تلفن و آدرس با انتخاب تامین‌کننده"""
        info = self.sup_data_map.get(choice, {"phone": "", "address": ""})
        self.sup_phone_entry.delete(0, "end")
        self.sup_phone_entry.insert(0, info["phone"])

        self.sup_addr_entry.delete(0, "end")
        self.sup_addr_entry.insert(0, info["address"])

    def clear_form(self):
        """خالی کردن ورودی‌های فرم"""
        self.code_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.pp_entry.delete(0, "end")
        self.mfg_phone_entry.delete(0, "end")
        self.mfg_addr_entry.delete(0, "end")
        self.sup_phone_entry.delete(0, "end")
        self.sup_addr_entry.delete(0, "end")

    def save_product(self):
        """ذخیره کالا در دیتابیس"""
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        branch = self.branch_combo.get().strip()
        pp_raw = self.pp_entry.get().strip()

        if not code or not name:
            messagebox.showwarning("خطا", fa("کد کالا و نام کالا الزامی هستند!"))
            return

        purchase_point = None
        if pp_raw:
            if not pp_raw.isdigit():
                messagebox.showerror("خطا", fa("نقطه سفارش باید یک عدد صحیح باشد!"))
                return
            purchase_point = int(pp_raw)

        selected_mfg_text = self.mfg_combo.get()
        selected_sup_text = self.supplier_combo.get()

        mfg_id = self.mfg_data_map.get(selected_mfg_text, {}).get("id")
        sup_id = self.sup_data_map.get(selected_sup_text, {}).get("id")

        unit = self.unit_combo.get()
        sub_unit = self.sub_unit_combo.get()

        db = SessionLocal()
        try:
            existing_prod = db.query(Product).filter(Product.code == code).first()
            if existing_prod:
                messagebox.showerror("خطای تکرار", fa(f"کد کالای '{code}' قبلاً ثبت شده است!"))
                return

            new_product = Product(
                code=code,
                name=name,
                branch=branch,
                unit=unit,
                sub_unit=sub_unit,
                quantity=0,
                purchase_point=purchase_point,
                usage_per_month=None,
                manufacturer_id=mfg_id,
                supplier_id=sup_id
            )

            db.add(new_product)
            db.commit()

            messagebox.showinfo("موفقیت", fa(f"کالای '{name}' با موفقیت ثبت شد."))
            self.clear_form()

        except Exception as e:
            db.rollback()
            messagebox.showerror("خطای دیتابیس", fa(f"خطا هنگام ثبت کالا:\n{str(e)}"))
        finally:
            db.close()