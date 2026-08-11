import os
import webbrowser
import tempfile
import customtkinter as ctk
from tkinter import ttk
from DAL import SessionLocal, Product
from BLL.persian_check import fa


class ProductListFrame(ctk.CTkFrame):
    def __init__(self, master, on_back=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_back = on_back

        # ۱. تعریف تمام ستون‌ها و معادل فارسی آن‌ها (متن خام فارسی برای HTML)
        self.columns_info_raw = {
            "id": "شناسه",
            "code": "کد کالا",
            "name": "نام کالا",
            "manufacturer": "سازنده",
            "supplier": "تامین‌کننده",
            "branch": "شعبه / انبار",
            "unit": "واحد اصلی",
            "sub_unit": "واحد فرعی",
            "quantity": "موجودی",
            "purchase_point": "نقطه سفارش",
            "usage_per_month": "مصرف ماهانه"
        }

        # ترتیب نمایش ستون‌ها از چپ به راست در جدول (شناسه ثابت در منتهی‌الیه راست)
        self.all_cols = [
            "usage_per_month",
            "purchase_point",
            "quantity",
            "sub_unit",
            "unit",
            "branch",
            "supplier",
            "manufacturer",
            "name",
            "code",
            "id"  # همیشه در سمت راست
        ]

        # ستون‌های قابل حذف/نمایش (بدون شناسه)
        self.toggleable_cols = [
            "code",
            "name",
            "manufacturer",
            "supplier",
            "branch",
            "unit",
            "sub_unit",
            "quantity",
            "purchase_point",
            "usage_per_month"
        ]

        self.col_vars = {}
        # ذخیره داده‌های خام (بدون reshaping) برای چاپ صحیح در HTML
        self.raw_products_data = []

        # --- ۲. هدر بالا (عنوان + دکمه پرینت) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 5))
        if self.on_back:
            self.back_btn = ctk.CTkButton(
                self.header_frame,
                text=fa(" بازگشت به منوی اصلی"),
                fg_color="#a83232",
                hover_color="#7a2323",
                font=("Tahoma", 12, "bold"),
                width=110,
                height=38,
                command=self.on_back
            )
            self.back_btn.pack(side="right", padx=(0, 15))
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=fa("مدیریت و مشاهده کالاها"),
            font=("Tahoma", 20, "bold")
        )
        self.title_label.pack(side="right")

        # دکمه پرینت / چاپ
        self.print_btn = ctk.CTkButton(
            self.header_frame,
            text=fa("🖨️ چاپ / خروجی پرینت"),
            fg_color="#1f6aa5",
            hover_color="#144870",
            font=("Tahoma", 13, "bold"),
            height=38,
            command=self.print_report
        )
        self.print_btn.pack(side="left")

        # --- ۳. فریم فیلتر و انتخاب ستون‌ها ---
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(fill="x", padx=20, pady=10)

        self.filter_label = ctk.CTkLabel(
            self.filter_frame,
            text=fa("ستون‌های اختیاری:"),
            font=("Tahoma", 12, "bold")
        )
        self.filter_label.pack(side="right", padx=(10, 5), pady=10)

        # چک‌باکس «همه»
        self.all_var = ctk.BooleanVar(value=True)
        self.all_chk = ctk.CTkCheckBox(
            self.filter_frame,
            text=fa("همه"),
            variable=self.all_var,
            command=self.toggle_all_columns,
            font=("Tahoma", 12, "bold")
        )
        self.all_chk.pack(side="right", padx=6, pady=10)

        # ساخت چک‌باکس‌ها برای ستون‌های اختیاری
        for col_key in reversed(self.toggleable_cols):
            col_name_fa = self.columns_info_raw[col_key]
            var = ctk.BooleanVar(value=True)
            self.col_vars[col_key] = var

            chk = ctk.CTkCheckBox(
                self.filter_frame,
                text=fa(col_name_fa),
                variable=var,
                command=self.update_visible_columns,
                font=("Tahoma", 11)
            )
            chk.pack(side="right", padx=6, pady=10)

        # --- ۴. فریم جدول ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._setup_treeview_style()

        # ساخت Treeview
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=self.all_cols,
            show="headings",
            selectmode="browse"
        )

        # تنظیم عناوین و عرض ستون‌ها
        for col_key in self.all_cols:
            self.tree.heading(col_key, text=fa(self.columns_info_raw[col_key]))
            align = "center" if col_key in ["id", "code", "unit", "sub_unit", "quantity", "purchase_point", "usage_per_month"] else "e"
            
            # عرض پایه برای حالت معمولی
            base_width = 60 if col_key == "id" else (150 if col_key in ["name", "manufacturer", "supplier", "branch"] else 95)
            
            # stretch=True باعث می‌شود ستون‌ها با کم/زیاد شدن بقیه ستون‌ها، کل عرض صفحه را بپوشانند
            self.tree.column(col_key, width=base_width, minwidth=50, anchor=align, stretch=True)
        # اسکرول‌بارها
        self.scrollbar_y = ctk.CTkScrollbar(self.table_frame, orientation="vertical", command=self.tree.yview)
        self.scrollbar_x = ctk.CTkScrollbar(self.table_frame, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side="left", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="right", fill="both", expand=True)
       

        self.load_data()


    def _setup_treeview_style(self):
        """تنظیمات ظاهری: افزایش سایز فونت و ارتفاع سطرها برای خوانایی بهتر"""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="#ffffff",
            fieldbackground="#2b2b2b",
            rowheight=40,            # افزایش ارتفاع سطرها
            font=("Tahoma", 15)       # فونت درشت‌تر برای محتوای جدول
        )

        style.configure(
            "Treeview.Heading",
            background="#1a1a1a",
            foreground="#3B8ED0",
            font=("Tahoma", 15, "bold"),  # فونت درشت‌تر برای عناوین
            relief="flat"
        )

        style.map("Treeview", background=[("selected", "#1f538d")])
        style.map("Treeview.Heading", background=[("active", "#2a2a2a")])

    def toggle_all_columns(self):
        """فعال/غیرفعال کردن همه ستون‌های اختیاری"""
        state = self.all_var.get()
        for var in self.col_vars.values():
            var.set(state)
        self.update_visible_columns()

    def update_visible_columns(self):
        """اعمال تغییرات نمایش ستون‌ها و بازپخش عرض آن‌ها برای پر کردن کامل صفحه"""
        visible_cols = [col for col in self.all_cols if col == "id" or self.col_vars.get(col, ctk.BooleanVar(value=True)).get()]
        
        # ۱. بروزرسانی لیست ستون‌های نمایشی
        self.tree["displaycolumns"] = visible_cols

        # ۲. فعال‌کردن stretch برای ستون‌های مرئی جهت پر کردن کل پهنای جدول
        for col in self.all_cols:
            if col in visible_cols:
                # ستون‌های مرئی کش می‌آیند تا فضای خالی ایجاد نشود
                self.tree.column(col, stretch=True)
            else:
                # ستون‌های مخفی کش نمی‌آیند
                self.tree.column(col, stretch=False)

        # ۳. تنظیم وضعیت چک‌باکس "همه"
        all_checked = all(self.col_vars[col].get() for col in self.toggleable_cols)
        self.all_var.set(all_checked)
    def load_data(self):
        """دریافت داده‌ها از دیتابیس با تمام فیلدها"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.raw_products_data.clear()

        self.tree.tag_configure("evenrow", background="#2b2b2b")
        self.tree.tag_configure("oddrow", background="#242424")

        db = SessionLocal()
        try:
            products = db.query(Product).all()

            for idx, p in enumerate(products):
                mfg_name = p.manufacturer.name if getattr(p, 'manufacturer', None) else "-"
                sup_name = p.supplier.name if getattr(p, 'supplier', None) else "-"
                branch_name = p.branch if getattr(p, 'branch', None) else "-"

                # ۱. ذخیره داده‌های خام برای HTML (بدون تبدیل با fa)
                raw_item = {
                    "id": str(p.id),
                    "code": str(p.code),
                    "name": str(p.name),
                    "manufacturer": str(mfg_name),
                    "supplier": str(sup_name),
                    "branch": str(branch_name),
                    "unit": str(p.unit or "-"),
                    "sub_unit": str(p.sub_unit or "-"),
                    "quantity": str(p.quantity if p.quantity is not None else 0),
                    "purchase_point": str(p.purchase_point if p.purchase_point is not None else "-"),
                    "usage_per_month": str(p.usage_per_month if p.usage_per_month is not None else "-")
                }
                self.raw_products_data.append(raw_item)

                # ۲. ساخت مقادیر نمایش داده‌شده در تکینتر (با تبدیل fa)
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert(
                    "",
                    "end",
                    tags=(tag,),
                    values=(
                        p.usage_per_month if p.usage_per_month is not None else "-",
                        p.purchase_point if p.purchase_point is not None else "-",
                        p.quantity if p.quantity is not None else 0,
                        fa(p.sub_unit or "-"),
                        fa(p.unit or "-"),
                        fa(branch_name),
                        fa(sup_name),
                        fa(mfg_name),
                        fa(p.name),
                        p.code,
                        p.id
                    )
                )
        finally:
            db.close()

    def print_report(self):
        """تولید خروجی پرینت استاندارد HTML با فونت درشت و متن تمیز فارسی"""
        display_cols = self.tree["displaycolumns"]
        if display_cols == ("#all",) or not display_cols:
            visible_cols = self.all_cols
        else:
            visible_cols = list(display_cols)

        # ساخت سرستون‌ها به زبان فارسی تمیز (بدون fa)
        headers_html = "".join([f"<th>{self.columns_info_raw[col]}</th>" for col in reversed(visible_cols)])

        # ساخت ردیف‌ها بر اساس داده‌های خام بدون بهم‌ریختگی
        rows_html = ""
        for raw_item in self.raw_products_data:
            row_cells = []
            for col in reversed(visible_cols):
                val = raw_item.get(col, "-")
                row_cells.append(f"<td>{val}</td>")
            rows_html += f"<tr>{''.join(row_cells)}</tr>"

        # قالب HTML با فونت درشت، امکان زوم و چیدمان کاملاً استاندارد
        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>گزارش موجودی انبار</title>
            <style>
                body {{
                    font-family: 'Tahoma', 'Segoe UI', Arial, sans-serif;
                    padding: 30px;
                    direction: rtl;
                    font-size: 16px; /* فونت درشت‌تر برای خوانایی کامل */
                    background-color: #fff;
                    color: #000;
                }}
                h2 {{
                    text-align: center;
                    color: #222;
                    margin-bottom: 25px;
                    font-size: 22px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }}
                th, td {{
                    border: 1px solid #444;
                    padding: 12px 14px; /* فضای بیشتر داخل سلول‌ها */
                    text-align: center;
                    font-size: 15px;
                }}
                th {{
                    background-color: #e6e6e6;
                    color: #000;
                    font-weight: bold;
                    font-size: 16px;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                .print-btn {{
                    padding: 10px 20px;
                    margin-bottom: 20px;
                    font-size: 15px;
                    font-weight: bold;
                    background-color: #1f6aa5;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                @media print {{
                    .print-btn {{ display: none; }}
                    body {{ padding: 0; font-size: 14px; }}
                    th, td {{ padding: 8px 10px; }}
                }}
            </style>
        </head>
        <body>
            <h2>گزارش لیست کالاها و موجودی انبار</h2>
            <button class="print-btn" onclick="window.print()">🖨️ پرینت / ذخیره به‌صورت PDF</button>
            <table>
                <thead>
                    <tr>{headers_html}</tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </body>
        </html>
        """

        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "inventory_report.html")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        webbrowser.open(f"file://{file_path}")