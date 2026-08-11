# UIL/main_menu.py
import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))

class MainMenu(ctk.CTkFrame):
    def __init__(self, master, on_add_product, on_show_products, **kwargs):
        super().__init__(master, **kwargs)
        self.on_add_product = on_add_product
        self.on_show_products = on_show_products  # اکشن جدید برای باز کردن لیست کالاها

        # عنوان
        self.title_label = ctk.CTkLabel(
            self, 
            text=fa("سیستم مدیریت انبار - منوی اصلی"), 
            font=("Tahoma", 16, "bold")
        )
        self.title_label.pack(pady=(30, 20))

        # دکمه ثبت / اطلاعات پایه
        self.add_product_button = ctk.CTkButton(
            self, 
            text=fa("اطلاعات پایه"), 
            width=200,
            height=40,
            command=self.on_add_product
        )
        self.add_product_button.pack(pady=10, padx=20)

        # دکمه جدید: مشاهده لیست کالاها
        self.show_products_button = ctk.CTkButton(
            self, 
            text=fa("لیست کالاها و موجودی"), 
            width=200,
            height=40,
            command=self.on_show_products
        )
        self.show_products_button.pack(pady=10, padx=20)