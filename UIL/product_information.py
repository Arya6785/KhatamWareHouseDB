# UIL/add_product_frame.py
import customtkinter as ctk
from tkinter import messagebox
from DAL import SessionLocal, Manufacturer, Suppliar
from DAL import Bases
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))
class AddProductFrame(ctk.CTkFrame):
    def __init__(self, master, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_back = on_back

        # دریافت لیست سازندگان و تامین‌کنندگان از دیتابیس یا فایل Bases
        self.manufacturers_list = self.get_manufacturers()
        self.suppliers_list = self.get_suppliers()

        # عنوان فرم
        self.title_label = ctk.CTkLabel(self, text=fa("فرم ثبت کالای جدید"), font=("Tahoma", 16, "bold"))
        self.title_label.pack(pady=(10, 15))

        # کد کالا
        self.code_entry = ctk.CTkEntry(self, placeholder_text=fa("کد کالا (مثلاً: PRD-101)"), width=320)
        self.code_entry.pack(pady=6)

        # نام کالا
        self.name_entry = ctk.CTkEntry(self, placeholder_text=fa("نام کالا"), width=320)
        self.name_entry.pack(pady=6)

        # سازنده
        self.mfg_label = ctk.CTkLabel(self, text=fa("سازنده / برند:"), font=("Tahoma", 11))
        self.mfg_label.pack(anchor="e", padx=55, pady=(4, 0))
        self.mfg_combo = ctk.CTkComboBox(self, values=self.manufacturers_list, width=320)
        self.mfg_combo.pack(pady=4)

        # تامین‌کننده
        self.supplier_label = ctk.CTkLabel(self, text=fa("تامین‌کننده:"), font=("Tahoma", 11))
        self.supplier_label.pack(anchor="e", padx=55, pady=(4, 0))
        self.supplier_combo = ctk.CTkComboBox(self, values=self.suppliers_list, width=320)
        self.supplier_combo.pack(pady=4)

        # واحد اصلی سنجش
        self.unit_label = ctk.CTkLabel(self, text=fa("واحد اصلی:"), font=("Tahoma", 11))
        self.unit_label.pack(anchor="e", padx=55, pady=(4, 0))
        self.unit_combo = ctk.CTkComboBox(self, values=Bases.UNITS, width=320)
        self.unit_combo.pack(pady=4)

        # واحد فرعی سنجش
        self.sub_unit_label = ctk.CTkLabel(self, text=fa("واحد فرعی:"), font=("Tahoma", 11))
        self.sub_unit_label.pack(anchor="e", padx=55, pady=(4, 0))
        self.sub_unit_combo = ctk.CTkComboBox(self, values=Bases.SUB_UNITS, width=320)
        self.sub_unit_combo.pack(pady=4)



        # دکمه ثبت
        self.save_button = ctk.CTkButton(
            self, 
            text="ذخیره کالا", 
            fg_color="green", 
            hover_color="darkgreen",
            width=320,
            command=self.save_product
        )
        self.save_button.pack(pady=(15, 5))

        # دکمه بازگشت به منوی اصلی
        if self.on_back:
            self.back_button = ctk.CTkButton(
                self,
                text=fa("بازگشت به منوی اصلی"),
                fg_color="gray",
                hover_color="#555555",
                width=320,
                command=self.on_back
            )
            self.back_button.pack(pady=5)

    def get_manufacturers(self):
        db = SessionLocal()
        try:
            return Bases.MANUFACTURERS
        finally:
            db.close()

    def get_suppliers(self):
        db = SessionLocal()
        try:
            return Bases.SUPPLIARS  # اصلاح نام متغیر به SUPPLIARS
        finally:
            db.close()

    def save_product(self):
        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()

        if not code or not name:
            messagebox.showwarning("خطا", fa("کد کالا و نام کالا الزامی هستند!"))
            return

        messagebox.showinfo("موفقیت", fa(f"کالای {name} با موفقیت ثبت شد."))