# UIL/widgets.py
import customtkinter as ctk

class SearchableComboBox(ctk.CTkComboBox):
    def __init__(self, master, values=None, fa_func=None, **kwargs):
        self.fa_func = fa_func
        self.raw_values = values if values else []
        
        # نگهداری نقشه‌ی تبدیل متن نمایش به متن خام
        self.display_to_raw = {}
        formatted_values = self._build_formatted_list(self.raw_values)
        
        super().__init__(master, values=formatted_values, **kwargs)
        self._entry.bind("<KeyRelease>", self._on_key_release)

    def _build_formatted_list(self, items):
        """تبدیل لیست خام به نمایش ظاهری و حفظ نقشه نگاشت"""
        self.display_to_raw.clear()
        formatted = []
        for item in items:
            disp = self.fa_func(item) if self.fa_func else item
            formatted.append(disp)
            self.display_to_raw[disp] = item
        return formatted

    def update_values(self, new_raw_values):
        """به‌روزرسانی لیست گزینه‌ها"""
        self.raw_values = new_raw_values
        self.configure(values=self._build_formatted_list(self.raw_values))

    def get_raw_value(self):
        """
        دریافت متن اصلی برای ذخیره در دیتابیس:
        اگر از لیست انتخاب شده باشد، متن خام اصلی برمی‌گردد.
        اگر اسم جدیدی تایپ شده باشد، همان متن تایپ‌شده برمی‌گردد.
        """
        val = self.get().strip()
        return self.display_to_raw.get(val, val)

    def _on_key_release(self, event):
        # نادیده گرفتن کلیدهای جهت‌نما و مدیریتی
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab", "Shift_L", "Shift_R", "Control_L", "Control_R"):
            return

        typed = self.get().strip().lower()

        # اگر هیچی تایپ نشده بود، کل لیست نشان داده شود
        if not typed:
            filtered_raw = self.raw_values
        else:
            # فیلتر کردن گزینه‌های موجود بر اساس متن تایپ‌شده
            filtered_raw = [
                item for item in self.raw_values 
                if typed in str(item).lower()
            ]

        # به‌روزرسانی لیست کشویی (اگر پیدا نشد، لیست خالی می‌شود و تایپ کاربر خراب نمی‌شود)
        display_values = self._build_formatted_list(filtered_raw)
        self.configure(values=display_values)