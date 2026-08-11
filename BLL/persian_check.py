import re
import arabic_reshaper
from bidi.algorithm import get_display

def is_persian(text: str) -> bool:
    """بررسی وجود حروف فارسی یا عربی در متن"""
    if not text:
        return False
    # بازه یونیکد (Unicode) مربوط به حروف فارسی و عربی
    persian_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    return bool(persian_pattern.search(text))

def far(text: str) -> str:
    """
    تابع هوشمند اصلاح متن:
    اگر متن شامل حروف فارسی باشد، آن را اصلاح می‌کند.
    در غیر این صورت (انگلیسی یا اعداد خالص)، متن اصلی را بدون تغییر برمی‌گرداند.
    """
    if not text:
        return ""
    
    # تبدیل به استرینگ (در صورتی که عدد ارسال شده باشد)
    text_str = str(text)
    
    # اگر حروف فارسی داشت، از reshaper رد می‌شود
    if is_persian(text_str):
        reshaped = arabic_reshaper.reshape(text_str)
        return get_display(reshaped)
    
    # اگر تماماً انگلیسی یا عدد بود، بدون تغییر برمی‌گردد
    return text_str
def fa(text):
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))



