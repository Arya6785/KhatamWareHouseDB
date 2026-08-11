# main.py
import customtkinter as ctk
from DAL import init_db
from UIL.main_menu import MainMenu
from UIL.product_information import AddProductFrame
import arabic_reshaper
from bidi.algorithm import get_display
from UIL.product_list_frame import ProductListFrame  # وارد کردن فریم جدول محصولات

def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))
# ۱. ساخت دیتابیس در صورت عدم وجود
init_db()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(fa("سیستم مدیریت انبار"))     
        self.geometry("1280x750")  # اندازه پنجره
        self.resizable(False, False)

        # متغیری برای نگهداری فریم فعلی
        self.current_frame = None

        # نمایش منوی اصلی در ابتدا
        self.show_main_menu()

    def show_main_menu(self):
        """نمایش منوی اصلی"""
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        self.current_frame = MainMenu(self, on_add_product=self.show_add_product_frame , on_show_products=self.show_product_list_frame)
        self.current_frame.pack(fill="both", expand=True, padx=15, pady=15)

    def show_add_product_frame(self):
        """تغییر صفحه به فرم ثبت کالا"""
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        self.current_frame = AddProductFrame(self, on_back=self.show_main_menu)
        self.current_frame.pack(fill="both", expand=True, padx=15, pady=15)
    def show_product_list_frame(self):
        """نمایش فریم جدول محصولات"""
        if self.current_frame is not None:
            self.current_frame.destroy()

        # پاس دادن متد show_main_menu به پارامتر on_back
        self.current_frame = ProductListFrame(self, on_back=self.show_main_menu)
        self.current_frame.pack(fill="both", expand=True)
if __name__ == "__main__":
    app = App()
    app.mainloop()