# UIL/main_menu.py
import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display


def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))


class MainMenu(ctk.CTkFrame):
    def __init__(self, master, on_open_base_info, on_show_products, **kwargs):
        super().__init__(master, **kwargs)
        self.on_open_base_info = on_open_base_info
        self.on_show_products = on_show_products

        # عنوان منو
        self.title_label = ctk.CTkLabel(
            self,
            text=fa("سیستم مدیریت انبار - منوی اصلی"),
            font=("Tahoma", 16, "bold")
        )
        self.title_label.pack(pady=(20, 15), padx=20)

        # دکمه ورود به صفحه اطلاعات پایه
        self.btn_base_info = ctk.CTkButton(
            self,
            text=fa(" اطلاعات پایه"),
            width=220,
            height=40,
            font=("Tahoma", 12, "bold"),
            command=self.on_open_base_info
        )
        self.btn_base_info.pack(pady=10, padx=20)

        # دکمه مشاهده لیست کالاها و موجودی
        self.show_products_button = ctk.CTkButton(
            self,
            text=fa(" لیست کالاها و موجودی"),
            width=220,
            height=40,
            font=("Tahoma", 12, "bold"),
            command=self.on_show_products
        )
        self.show_products_button.pack(pady=10, padx=20)