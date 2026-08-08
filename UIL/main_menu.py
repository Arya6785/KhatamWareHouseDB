# UIL/main_menu.py
import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))
class MainMenu(ctk.CTkFrame):
    def __init__(self, master, on_add_product, **kwargs):
        super().__init__(master, **kwargs)
        self.on_add_product = on_add_product

        self.title_label = ctk.CTkLabel(self, text=fa("سیستم مدیریت انبار - منوی اصلی"), font=("Tahoma", 16, "bold"))
        self.title_label.pack(pady=(30, 20))

        # دکمه ثبت کالای جدید
        self.add_product_button = ctk.CTkButton(
            self, 
            text=fa("اطلاعات پایه"), 
            width=200,
            height=40,
            command=self.on_add_product
        )
        self.add_product_button.pack(pady=10, padx=20)