import sqlite3
import random
import string
import json
import csv
import webbrowser
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import customtkinter as ctk
from faker import Faker
from auth import hash_password, verify_password

# Initialize Faker
fake = Faker('en_PH')

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    # Modern Professional Palette (Light / Dark adaptive tuples)
    ACCENT = ("#1E40AF", "#3B82F6")
    ACCENT_HOVER = ("#1E3A8A", "#2563EB")
    SURFACE_CARD = ("#FFFFFF", "#18181B")
    SURFACE_SUB = ("#F4F4F5", "#27272A")
    BORDER_SUBTLE = ("#E4E4E7", "#3F3F46")
    TEXT_PRIMARY = ("#09090B", "#FAFAFA")
    TEXT_MUTED = ("#52525B", "#A1A1AA")
    DANGER = ("#B91C1C", "#DC2626")
    DANGER_HOVER = ("#991B1B", "#B91B1B")
    SUCCESS = ("#15803D", "#22C55E")
    SUCCESS_HOVER = ("#166534", "#16A34A")

    def __init__(self):
        super().__init__()
        self.title("SIA2 — Utilities Suite")
        self.geometry("1220x780")
        self.minsize(1020, 680)
        self._resize_job = None
        self.nav_buttons = {}

        self._configure_treeview_style()
        self.show_login_frame()

    def _configure_treeview_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        is_dark = ctk.get_appearance_mode().lower() == "dark"
        bg = "#18181B" if is_dark else "#FFFFFF"
        fg = "#FAFAFA" if is_dark else "#18181B"
        hdr_bg = "#27272A" if is_dark else "#F4F4F5"
        hdr_fg = "#F4F4F5" if is_dark else "#18181B"
        sel_bg = "#1D4ED8" if is_dark else "#DBEAFE"
        sel_fg = "#FFFFFF" if is_dark else "#1E3A8A"
        border = "#27272A" if is_dark else "#E4E4E7"

        style.configure(
            "Modern.Treeview",
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            bordercolor=border,
            lightcolor=border,
            darkcolor=border,
            rowheight=34,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=hdr_bg,
            foreground=hdr_fg,
            relief="flat",
            padding=(10, 8),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", sel_bg)],
            foreground=[("selected", sel_fg)],
        )
        style.map(
            "Modern.Treeview.Heading",
            background=[("active", border)],
        )

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- LOGIN / REGISTER SCREEN ---
    def show_login_frame(self):
        self.clear_window()
        self.title("SIA2 — Sign In")

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        card = ctk.CTkFrame(
            outer,
            width=420,
            height=485,
            corner_radius=16,
            fg_color=self.SURFACE_CARD,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        card.pack(padx=24, pady=24)
        card.pack_propagate(False)

        badge = ctk.CTkLabel(
            card,
            text="OPTION 3B  •  WORKBENCH",
            font=("Segoe UI", 10, "bold"),
            text_color=self.ACCENT,
        )
        badge.pack(anchor="w", padx=36, pady=(32, 4))

        title = ctk.CTkLabel(
            card,
            text="Sign in to your account",
            font=("Segoe UI", 22, "bold"),
            text_color=self.TEXT_PRIMARY,
        )
        title.pack(anchor="w", padx=36)

        subtitle = ctk.CTkLabel(
            card,
            text="Access Fake Data Generator, URL Shortener & Messaging",
            font=("Segoe UI", 12),
            text_color=self.TEXT_MUTED,
        )
        subtitle.pack(anchor="w", padx=36, pady=(4, 22))

        ctk.CTkLabel(
            card,
            text="Username",
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(anchor="w", padx=36, pady=(0, 4))

        self.user_entry = ctk.CTkEntry(
            card,
            placeholder_text="Enter your username",
            width=348,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            fg_color=self.SURFACE_SUB,
            font=("Segoe UI", 12),
        )
        self.user_entry.pack(padx=36, pady=(0, 14))

        ctk.CTkLabel(
            card,
            text="Password",
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(anchor="w", padx=36, pady=(0, 4))

        self.pass_entry = ctk.CTkEntry(
            card,
            placeholder_text="Enter your password",
            show="•",
            width=348,
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            fg_color=self.SURFACE_SUB,
            font=("Segoe UI", 12),
        )
        self.pass_entry.pack(padx=36, pady=(0, 10))
        self.pass_entry.bind("<Return>", lambda _e: self.handle_login())

        self.show_pass_var = ctk.BooleanVar(value=False)
        show_pass_chk = ctk.CTkCheckBox(
            card,
            text="Show password",
            variable=self.show_pass_var,
            command=lambda: self.pass_entry.configure(show="" if self.show_pass_var.get() else "•"),
            font=("Segoe UI", 11),
            text_color=self.TEXT_MUTED,
            checkbox_width=16,
            checkbox_height=16,
            corner_radius=4,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
        )
        show_pass_chk.pack(anchor="w", padx=36, pady=(0, 18))

        login_btn = ctk.CTkButton(
            card,
            text="Sign In",
            width=348,
            height=40,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 12, "bold"),
            command=self.handle_login,
        )
        login_btn.pack(padx=36, pady=(0, 10))

        reg_btn = ctk.CTkButton(
            card,
            text="Create New Account",
            width=348,
            height=38,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 12),
            command=self.handle_register,
        )
        reg_btn.pack(padx=36)

    def handle_register(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "All fields must be filled out!")
            return
        pwd_hash, salt = hash_password(password)
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, pwd_hash, salt))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    def handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password, salt FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and verify_password(result[0], result[1], password):
            self.active_user = username
            self.title(f"SIA2 — Utilities Suite ({username})")
            self.show_main_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # --- MAIN DASHBOARD (LEFT SIDEBAR + CONTENT PANE) ---
    def show_main_dashboard(self):
        self.clear_window()
        self.nav_buttons = {}

        sidebar = ctk.CTkFrame(
            self,
            width=225,
            corner_radius=0,
            fg_color=self.SURFACE_CARD,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand_box = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand_box.pack(fill="x", padx=18, pady=(22, 18))

        ctk.CTkLabel(
            brand_box,
            text="SIA2 Suite",
            font=("Segoe UI", 18, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_box,
            text="Option 3B  •  Workbench",
            font=("Segoe UI", 11),
            text_color=self.TEXT_MUTED,
        ).pack(anchor="w")

        ctk.CTkLabel(
            sidebar,
            text="MODULES",
            font=("Segoe UI", 10, "bold"),
            text_color=self.TEXT_MUTED,
        ).pack(anchor="w", padx=20, pady=(4, 8))

        modules = [
            ("fake", "Fake Data Gen", "3B.3"),
            ("url", "URL Shortener", "3B.1"),
            ("msg", "Messaging", "3B.2"),
        ]

        for key, label_txt, code_txt in modules:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{label_txt}  ({code_txt})",
                height=38,
                corner_radius=8,
                anchor="w",
                font=("Segoe UI", 12, "bold"),
                command=lambda k=key: self.select_module(k),
            )
            btn.pack(fill="x", padx=14, pady=3)
            self.nav_buttons[key] = btn

        footer_box = ctk.CTkFrame(
            sidebar,
            corner_radius=10,
            fg_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        footer_box.pack(side="bottom", fill="x", padx=14, pady=16)

        user_label = getattr(self, "active_user", "User")
        ctk.CTkLabel(
            footer_box,
            text="Signed in as",
            font=("Segoe UI", 10),
            text_color=self.TEXT_MUTED,
        ).pack(anchor="w", padx=12, pady=(10, 0))

        ctk.CTkLabel(
            footer_box,
            text=user_label,
            font=("Segoe UI", 12, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(anchor="w", padx=12, pady=(0, 8))

        ctk.CTkButton(
            footer_box,
            text="Sign Out",
            height=32,
            corner_radius=7,
            fg_color="transparent",
            hover_color=self.SURFACE_CARD,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            text_color=self.DANGER,
            font=("Segoe UI", 11, "bold"),
            command=self.show_login_frame,
        ).pack(fill="x", padx=12, pady=(0, 12))

        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True, padx=18, pady=16)

        self.page_fake = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.page_url = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.page_msg = ctk.CTkFrame(self.content_area, fg_color="transparent")

        self.pages = {
            "fake": self.page_fake,
            "url": self.page_url,
            "msg": self.page_msg,
        }

        self.setup_fake_data_page()
        self.setup_url_page()
        self.setup_messaging_page()

        self.select_module("fake")

    def select_module(self, active_key):
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.configure(
                    fg_color=self.ACCENT,
                    hover_color=self.ACCENT_HOVER,
                    text_color="#FFFFFF",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color=self.SURFACE_SUB,
                    text_color=self.TEXT_PRIMARY,
                )

        for key, page in self.pages.items():
            page.pack_forget()
        self.pages[active_key].pack(fill="both", expand=True)

        if active_key == "fake":
            self.after(20, self._apply_responsive_columns)

    # --- MODULE 3B.3: FAKE DATA GEN (SPLIT WORKSPACE) ---
    def setup_fake_data_page(self):
        top_hdr = ctk.CTkFrame(self.page_fake, fg_color="transparent")
        top_hdr.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            top_hdr,
            text="Fake Data Generator",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            top_hdr,
            text="Choose fields, generate sample records, search, and export to CSV or JSON.",
            font=("Segoe UI", 12),
            text_color=self.TEXT_MUTED,
        ).pack(anchor="w")

        split_body = ctk.CTkFrame(self.page_fake, fg_color="transparent")
        split_body.pack(fill="both", expand=True)

        left_panel = ctk.CTkFrame(
            split_body,
            width=255,
            corner_radius=12,
            fg_color=self.SURFACE_CARD,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        left_panel.pack(side="left", fill="y", padx=(0, 12))
        left_panel.pack_propagate(False)

        right_panel = ctk.CTkFrame(split_body, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True)

        f_hdr = ctk.CTkFrame(left_panel, fg_color="transparent")
        f_hdr.pack(fill="x", padx=12, pady=(8, 3))

        ctk.CTkLabel(
            f_hdr,
            text="Fields",
            font=("Segoe UI", 12, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(side="left")

        self.selected_fields_label = ctk.CTkLabel(
            f_hdr,
            text="12 / 12",
            font=("Segoe UI", 11, "bold"),
            text_color=self.ACCENT,
        )
        self.selected_fields_label.pack(side="right")

        quick_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        quick_row.pack(fill="x", padx=12, pady=(0, 4))

        ctk.CTkButton(
            quick_row,
            text="All",
            height=22,
            corner_radius=6,
            fg_color=self.SURFACE_SUB,
            hover_color=self.BORDER_SUBTLE,
            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            command=self.select_all_fields,
        ).pack(side="left", fill="x", expand=True, padx=(0, 3))

        ctk.CTkButton(
            quick_row,
            text="Clear",
            height=22,
            corner_radius=6,
            fg_color="transparent",
            hover_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            text_color=self.TEXT_MUTED,
            font=("Segoe UI", 10),
            command=self.clear_all_fields,
        ).pack(side="left", fill="x", expand=True, padx=(3, 0))

        self.field_vars = {}
        groups = [
            ("Personal", [
                ("name", "Full Name"),
                ("birthdate", "Birthdate"),
                ("blood_type", "Blood Type"),
                ("address", "Address"),
            ]),
            ("Contact & Account", [
                ("mobile_number", "Mobile Number"),
                ("email", "Email Address"),
                ("username", "Username"),
                ("website", "Website URL"),
            ]),
            ("Work & Location", [
                ("job", "Job Title"),
                ("company", "Company"),
                ("city", "City"),
                ("country", "Country"),
            ]),
        ]

        for group_title, items in groups:
            grp_card = ctk.CTkFrame(
                left_panel,
                corner_radius=8,
                fg_color=self.SURFACE_SUB,
                border_width=1,
                border_color=self.BORDER_SUBTLE,
            )
            grp_card.pack(fill="x", padx=12, pady=1.5)

            ctk.CTkLabel(
                grp_card,
                text=group_title.upper(),
                font=("Segoe UI", 9, "bold"),
                text_color=self.TEXT_MUTED,
            ).pack(anchor="w", padx=8, pady=(3, 1))

            for key, label_text in items:
                var = ctk.BooleanVar(value=True)
                self.field_vars[key] = var
                chk = ctk.CTkCheckBox(
                    grp_card,
                    text=label_text,
                    variable=var,
                    command=self.update_field_counter,
                    font=("Segoe UI", 10.5),
                    text_color=self.TEXT_PRIMARY,
                    checkbox_width=15,
                    checkbox_height=15,
                    corner_radius=4,
                    fg_color=self.ACCENT,
                    hover_color=self.ACCENT_HOVER,
                )
                chk.pack(anchor="w", padx=8, pady=1)

            ctk.CTkFrame(grp_card, height=2, fg_color="transparent").pack()

        gen_box = ctk.CTkFrame(left_panel, fg_color="transparent")
        gen_box.pack(side="bottom", fill="x", padx=12, pady=(4, 8))

        count_row = ctk.CTkFrame(gen_box, fg_color="transparent")
        count_row.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(
            count_row,
            text="Batch Size",
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(side="left")

        self.count_entry = ctk.CTkEntry(
            count_row,
            width=66,
            height=26,
            corner_radius=6,
            justify="center",
            fg_color=self.SURFACE_SUB,
            border_color=self.BORDER_SUBTLE,
            font=("Segoe UI", 11),
        )
        self.count_entry.insert(0, "10")
        self.count_entry.pack(side="right")

        ctk.CTkButton(
            gen_box,
            text="Generate Records",
            height=32,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 11, "bold"),
            command=self.generate_and_save_data,
        ).pack(fill="x")

        toolbar = ctk.CTkFrame(
            right_panel,
            corner_radius=12,
            fg_color=self.SURFACE_CARD,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        toolbar.pack(fill="x", pady=(0, 10))

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="Search by Name, Job, City, Company...",
            width=260,
            height=34,
            corner_radius=8,
            fg_color=self.SURFACE_SUB,
            border_color=self.BORDER_SUBTLE,
            font=("Segoe UI", 11),
        )
        self.search_entry.pack(side="left", padx=(12, 8), pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_fake_table)

        ctk.CTkButton(
            toolbar,
            text="Copy",
            width=66,
            height=34,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 11),
            command=self.copy_fake_row,
        ).pack(side="left", padx=3, pady=10)

        ctk.CTkButton(
            toolbar,
            text="Delete",
            width=74,
            height=34,
            corner_radius=8,
            fg_color=self.DANGER,
            hover_color=self.DANGER_HOVER,
            font=("Segoe UI", 11),
            command=self.delete_fake_row,
        ).pack(side="left", padx=3, pady=10)

        ctk.CTkButton(
            toolbar,
            text="Clear",
            width=66,
            height=34,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 11),
            command=self.clear_fake_data,
        ).pack(side="left", padx=3, pady=10)

        ctk.CTkButton(
            toolbar,
            text="CSV",
            width=58,
            height=34,
            corner_radius=8,
            fg_color=self.SUCCESS,
            hover_color=self.SUCCESS_HOVER,
            font=("Segoe UI", 11, "bold"),
            command=self.export_fake_csv,
        ).pack(side="right", padx=(3, 12), pady=10)

        ctk.CTkButton(
            toolbar,
            text="JSON",
            width=62,
            height=34,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.SUCCESS,
            text_color=self.SUCCESS,
            font=("Segoe UI", 11, "bold"),
            command=self.export_fake_json,
        ).pack(side="right", padx=3, pady=10)

        self.tree_container = ctk.CTkFrame(
            right_panel,
            corner_radius=12,
            fg_color=self.SURFACE_CARD,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        self.tree_container.pack(fill="both", expand=True)

        meta_bar = ctk.CTkFrame(self.tree_container, fg_color="transparent")
        meta_bar.pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(
            meta_bar,
            text="Generated Records",
            font=("Segoe UI", 12, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(side="left")

        self.count_label = ctk.CTkLabel(
            meta_bar,
            text="Total Records: 0",
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_MUTED,
        )
        self.count_label.pack(side="right")

        grid_wrap = ctk.CTkFrame(self.tree_container, fg_color="transparent")
        grid_wrap.pack(fill="both", expand=True, padx=10, pady=(2, 10))

        columns = ("ID", "Name", "Address", "Birthdate", "Mobile", "Email", "Username", "Job Title", "Company", "City", "Country", "Blood Type", "Website")
        self.fake_tree = ttk.Treeview(grid_wrap, columns=columns, show="headings", style="Modern.Treeview")

        even_bg = "#1F1F23" if ctk.get_appearance_mode().lower() == "dark" else "#F8FAFC"
        odd_bg = "#18181B" if ctk.get_appearance_mode().lower() == "dark" else "#FFFFFF"
        self.fake_tree.tag_configure("evenrow", background=even_bg)
        self.fake_tree.tag_configure("oddrow", background=odd_bg)

        self.column_specs = {
            "ID": (0.45, 48, "center"),
            "Name": (1.30, 130, "w"),
            "Address": (2.50, 240, "w"),
            "Birthdate": (0.95, 100, "center"),
            "Mobile": (1.05, 110, "center"),
            "Email": (1.65, 165, "w"),
            "Username": (1.15, 115, "w"),
            "Job Title": (1.50, 150, "w"),
            "Company": (1.75, 175, "w"),
            "City": (1.05, 105, "w"),
            "Country": (1.05, 105, "w"),
            "Blood Type": (0.75, 85, "center"),
            "Website": (1.55, 155, "w"),
        }

        for col in columns:
            _, min_w, anchor = self.column_specs[col]
            self.fake_tree.heading(col, text=col)
            self.fake_tree.column(col, width=min_w, minwidth=min_w, anchor=anchor, stretch=True)

        sb_y = ttk.Scrollbar(grid_wrap, orient="vertical", command=self.fake_tree.yview)
        sb_x = ttk.Scrollbar(grid_wrap, orient="horizontal", command=self.fake_tree.xview)
        self.fake_tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        self.fake_tree.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")
        grid_wrap.grid_rowconfigure(0, weight=1)
        grid_wrap.grid_columnconfigure(0, weight=1)

        self.tree_container.bind("<Configure>", self._on_tree_container_resize)
        self.load_fake_data()

    def _on_tree_container_resize(self, event):
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(40, lambda w=event.width: self._apply_responsive_columns(w))

    def _apply_responsive_columns(self, container_width=None):
        self._resize_job = None
        if not hasattr(self, "fake_tree") or not self.fake_tree.winfo_exists():
            return
        if container_width is None:
            container_width = self.tree_container.winfo_width()
        available_width = max(container_width - 42, 600)
        cols = self.fake_tree["columns"]
        total_weight = sum(self.column_specs[c][0] for c in cols)
        for col in cols:
            weight, min_w, _ = self.column_specs[col]
            target_w = int((weight / total_weight) * available_width)
            self.fake_tree.column(col, width=max(target_w, min_w), minwidth=min_w)

    def update_field_counter(self):
        active = sum(1 for v in self.field_vars.values() if v.get())
        total = len(self.field_vars)
        self.selected_fields_label.configure(text=f"{active} / {total}")

    def select_all_fields(self):
        for var in self.field_vars.values():
            var.set(True)
        self.update_field_counter()

    def clear_all_fields(self):
        for var in self.field_vars.values():
            var.set(False)
        self.update_field_counter()

    def generate_and_save_data(self):
        try:
            num = int(self.count_entry.get())
            if num < 1:
                messagebox.showerror("Error", "Minimum count is 1.")
                return
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")
            return

        if not any(v.get() for v in self.field_vars.values()):
            messagebox.showwarning("No Fields Selected", "Please check at least one field before generating records.")
            return

        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        b_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        for _ in range(num):
            record = {
                "name": fake.name() if self.field_vars["name"].get() else "N/A",
                "address": fake.address().replace("\n", ", ") if self.field_vars["address"].get() else "N/A",
                "birthdate": str(fake.date_of_birth(minimum_age=18, maximum_age=60)) if self.field_vars["birthdate"].get() else "N/A",
                "mobile_number": fake.numerify("09#########") if self.field_vars["mobile_number"].get() else "N/A",
                "email": fake.email() if self.field_vars["email"].get() else "N/A",
                "username": fake.user_name() if self.field_vars["username"].get() else "N/A",
                "job": fake.job() if self.field_vars["job"].get() else "N/A",
                "company": fake.company() if self.field_vars["company"].get() else "N/A",
                "city": fake.city() if self.field_vars["city"].get() else "N/A",
                "country": fake.current_country() if self.field_vars["country"].get() else "N/A",
                "blood_type": random.choice(b_types) if self.field_vars["blood_type"].get() else "N/A",
                "website": fake.url() if self.field_vars["website"].get() else "N/A",
            }

            cursor.execute("""
                INSERT INTO fake_records (name, address, birthdate, mobile_number, email, username, job, company, city, country, blood_type, website)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record["name"], record["address"], record["birthdate"], record["mobile_number"],
                record["email"], record["username"], record["job"], record["company"],
                record["city"], record["country"], record["blood_type"], record["website"]
            ))

        conn.commit()
        conn.close()
        self.load_fake_data()
        messagebox.showinfo("Success", f"Generated {num} records successfully!")

    def load_fake_data(self):
        for i in self.fake_tree.get_children():
            self.fake_tree.delete(i)
        conn = sqlite3.connect("app_data.db")
        rows = conn.cursor().execute("SELECT * FROM fake_records").fetchall()
        conn.close()
        for idx, row in enumerate(rows, start=1):
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.fake_tree.insert("", "end", values=(idx, *row[1:]), tags=(row[0], row_tag))
        self.count_label.configure(text=f"Total Records: {len(rows)}")
        self.fake_tree.yview_moveto(0.0)
        self._apply_responsive_columns()

    def delete_fake_row(self):
        sel = self.fake_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a record to delete.")
            return
        rid = self.fake_tree.item(sel, "tags")[0]
        conn = sqlite3.connect("app_data.db")
        conn.cursor().execute("DELETE FROM fake_records WHERE id = ?", (rid,))
        conn.commit()
        conn.close()
        self.load_fake_data()

    def clear_fake_data(self):
        if messagebox.askyesno("Confirm", "Clear all records?"):
            conn = sqlite3.connect("app_data.db")
            conn.cursor().execute("DELETE FROM fake_records")
            conn.cursor().execute("DELETE FROM sqlite_sequence WHERE name='fake_records'")
            conn.commit()
            conn.close()
            self.load_fake_data()

    def copy_fake_row(self):
        sel = self.fake_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a record to copy.")
            return
        vals = self.fake_tree.item(sel, "values")
        row_str = " | ".join(str(v) for v in vals[1:])
        self.clipboard_clear()
        self.clipboard_append(row_str)
        messagebox.showinfo("Success", "Record copied to clipboard!")

    def export_fake_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if path:
            conn = sqlite3.connect("app_data.db")
            rows = conn.cursor().execute("SELECT * FROM fake_records").fetchall()
            conn.close()
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["ID", "Name", "Address", "Birthdate", "Mobile", "Email", "Username", "Job", "Company", "City", "Country", "Blood", "Website"])
                w.writerows(rows)
            messagebox.showinfo("Success", "Exported to CSV successfully!")

    def export_fake_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if path:
            conn = sqlite3.connect("app_data.db")
            rows = conn.cursor().execute("SELECT * FROM fake_records").fetchall()
            conn.close()
            keys = ["id", "name", "address", "birthdate", "mobile_number", "email", "username", "job", "company", "city", "country", "blood_type", "website"]
            data = [dict(zip(keys, row)) for row in rows]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "Exported to JSON successfully!")

    def filter_fake_table(self, event):
        q = self.search_entry.get().lower()
        for i in self.fake_tree.get_children():
            self.fake_tree.delete(i)
        conn = sqlite3.connect("app_data.db")
        rows = conn.cursor().execute("SELECT * FROM fake_records").fetchall()
        conn.close()
        c = 1
        for row in rows:
            if any(q in str(row[idx]).lower() for idx in [1, 6, 7, 8, 9]):
                row_tag = "evenrow" if c % 2 == 0 else "oddrow"
                self.fake_tree.insert("", "end", values=(c, *row[1:]), tags=(row[0], row_tag))
                c += 1
        self.count_label.configure(text=f"Filtered Records: {c - 1}")
        self.fake_tree.yview_moveto(0.0)
        self._apply_responsive_columns()

    # --- MODULE 3B.1: URL SHORTENER ---
    def setup_url_page(self):
        ctk.CTkLabel(
            self.page_url,
            text="URL Shortener",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.page_url,
            text="Create short links with optional custom aliases and track click analytics.",
            font=("Segoe UI", 12),
            text_color=self.TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 12))

        frame = ctk.CTkFrame(
            self.page_url,
            corner_radius=12,
            fg_color=self.SURFACE_CARD,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        frame.pack(fill="both", expand=True)

        input_card = ctk.CTkFrame(
            frame,
            corner_radius=10,
            fg_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
        )
        input_card.pack(fill="x", padx=16, pady=(14, 10))

        input_grid = ctk.CTkFrame(input_card, fg_color="transparent")
        input_grid.pack(fill="x", padx=14, pady=12)
        input_grid.grid_columnconfigure(0, weight=3)
        input_grid.grid_columnconfigure(1, weight=2)

        ctk.CTkLabel(
            input_grid,
            text="Original URL",
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 4))

        ctk.CTkLabel(
            input_grid,
            text="Custom Alias (Optional)",
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 4))

        self.orig_url_entry = ctk.CTkEntry(
            input_grid,
            placeholder_text="https://example.com/very-long-link",
            height=36,
            corner_radius=8,
            fg_color=self.SURFACE_CARD,
            border_color=self.BORDER_SUBTLE,
            font=("Segoe UI", 11),
        )
        self.orig_url_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.orig_url_entry.bind("<Return>", lambda _e: self.shorten_url())

        self.alias_entry = ctk.CTkEntry(
            input_grid,
            placeholder_text="e.g. mylink (blank = random)",
            height=36,
            corner_radius=8,
            fg_color=self.SURFACE_CARD,
            border_color=self.BORDER_SUBTLE,
            font=("Segoe UI", 11),
        )
        self.alias_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        self.alias_entry.bind("<Return>", lambda _e: self.shorten_url())

        ctk.CTkButton(
            input_grid,
            text="Shorten URL",
            width=120,
            height=36,
            corner_radius=8,
            fg_color=self.ACCENT,
            hover_color=self.ACCENT_HOVER,
            font=("Segoe UI", 12, "bold"),
            command=self.shorten_url,
        ).grid(row=1, column=2, sticky="e")

        search_bar = ctk.CTkFrame(frame, fg_color="transparent")
        search_bar.pack(fill="x", padx=16, pady=(0, 8))

        self.url_search_entry = ctk.CTkEntry(
            search_bar,
            placeholder_text="Search original URL, short link, or alias...",
            width=300,
            height=34,
            corner_radius=8,
            fg_color=self.SURFACE_SUB,
            border_color=self.BORDER_SUBTLE,
            font=("Segoe UI", 11),
        )
        self.url_search_entry.pack(side="left")
        self.url_search_entry.bind("<KeyRelease>", self.filter_url_table)

        self.url_count_label = ctk.CTkLabel(
            search_bar,
            text="Total Links: 0",
            font=("Segoe UI", 11, "bold"),
            text_color=self.TEXT_MUTED,
        )
        self.url_count_label.pack(side="right", padx=4)

        btn_row_url = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row_url.pack(side="bottom", fill="x", padx=16, pady=(8, 14))

        ctk.CTkButton(
            btn_row_url,
            text="Test Selected URL",
            height=34,
            corner_radius=8,
            fg_color=self.SUCCESS,
            hover_color=self.SUCCESS_HOVER,
            font=("Segoe UI", 11, "bold"),
            command=self.test_url,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_row_url,
            text="Copy Short URL",
            height=34,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            text_color=self.TEXT_PRIMARY,
            font=("Segoe UI", 11),
            command=self.copy_short_url,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_row_url,
            text="Delete Selected",
            height=34,
            corner_radius=8,
            fg_color=self.DANGER,
            hover_color=self.DANGER_HOVER,
            font=("Segoe UI", 11),
            command=self.delete_url,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_row_url,
            text="Clear All",
            height=34,
            corner_radius=8,
            fg_color="transparent",
            hover_color=self.SURFACE_SUB,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            text_color=self.TEXT_MUTED,
            font=("Segoe UI", 11),
            command=self.clear_urls,
        ).pack(side="right")

        url_tree_wrap = ctk.CTkFrame(frame, fg_color="transparent")
        url_tree_wrap.pack(fill="both", expand=True, padx=16, pady=(0, 4))

        columns = ("ID", "Original URL", "Shortened URL", "Clicks")
        self.url_tree = ttk.Treeview(url_tree_wrap, columns=columns, show="headings", style="Modern.Treeview")

        even_bg = "#1F1F23" if ctk.get_appearance_mode().lower() == "dark" else "#F8FAFC"
        odd_bg = "#18181B" if ctk.get_appearance_mode().lower() == "dark" else "#FFFFFF"
        self.url_tree.tag_configure("evenrow", background=even_bg)
        self.url_tree.tag_configure("oddrow", background=odd_bg)

        url_col_specs = {
            "ID": (60, "center", False),
            "Original URL": (420, "w", True),
            "Shortened URL": (250, "w", True),
            "Clicks": (90, "center", False),
        }
        for col, (w, anchor, stretch) in url_col_specs.items():
            self.url_tree.heading(col, text=col)
            self.url_tree.column(col, width=w, minwidth=w, anchor=anchor, stretch=stretch)

        sb_y = ttk.Scrollbar(url_tree_wrap, orient="vertical", command=self.url_tree.yview)
        self.url_tree.configure(yscrollcommand=sb_y.set)

        self.url_tree.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        url_tree_wrap.grid_rowconfigure(0, weight=1)
        url_tree_wrap.grid_columnconfigure(0, weight=1)

        self.load_url_data()

    def shorten_url(self):
        orig = self.orig_url_entry.get().strip()
        alias = self.alias_entry.get().strip()

        if not orig:
            messagebox.showerror("Error", "Please enter an original URL.")
            return

        if not orig.startswith("http://") and not orig.startswith("https://"):
            orig = "https://" + orig

        if alias:
            code = "".join(c for c in alias if c.isalnum() or c in ("_", "-"))
            if not code:
                messagebox.showerror("Error", "Alias must contain letters, numbers, underscores, or hyphens.")
                return
        else:
            code = "".join(random.choices(string.ascii_letters + string.digits, k=6))

        short_url = f"http://short.ly/{code}"

        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()

            exists = cursor.execute("SELECT id FROM urls WHERE short_code = ?", (short_url,)).fetchone()
            if exists:
                conn.close()
                messagebox.showerror("Duplicate Alias", f"'{short_url}' is already in use. Try another alias.")
                return

            cursor.execute(
                "INSERT INTO urls (original_url, short_code, clicks) VALUES (?, ?, ?)",
                (orig, short_url, 0),
            )
            conn.commit()
            conn.close()

            self.orig_url_entry.delete(0, "end")
            self.alias_entry.delete(0, "end")
            self.load_url_data()
            messagebox.showinfo("Success", f"URL Shortened Successfully!\n{short_url}")
        except sqlite3.OperationalError:
            self.upgrade_url_db_schema()
            self.shorten_url()

    def upgrade_url_db_schema(self):
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE urls ADD COLUMN clicks INTEGER DEFAULT 0")
            conn.commit()
        except sqlite3.OperationalError:
            pass
        conn.close()

    def load_url_data(self, query=""):
        for i in self.url_tree.get_children():
            self.url_tree.delete(i)
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        try:
            rows = cursor.execute("SELECT id, original_url, short_code, clicks FROM urls").fetchall()
        except sqlite3.OperationalError:
            self.upgrade_url_db_schema()
            rows = cursor.execute("SELECT id, original_url, short_code, clicks FROM urls").fetchall()
        conn.close()

        q = query.strip().lower()
        filtered = [
            r for r in rows
            if not q or q in str(r[1]).lower() or q in str(r[2]).lower()
        ]

        for idx, row in enumerate(filtered, start=1):
            row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.url_tree.insert("", "end", values=(idx, row[1], row[2], row[3]), tags=(row[0], row[1], row_tag))

        label_prefix = "Filtered Links" if q else "Total Links"
        self.url_count_label.configure(text=f"{label_prefix}: {len(filtered)}")

    def filter_url_table(self, _event=None):
        q = self.url_search_entry.get() if hasattr(self, "url_search_entry") else ""
        self.load_url_data(q)

    def test_url(self):
        sel = self.url_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a shortened URL to test.")
            return
        item_data = self.url_tree.item(sel, "tags")
        db_id = item_data[0]
        orig_url = item_data[1]

        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = ?", (db_id,))
        conn.commit()
        conn.close()

        self.filter_url_table()
        webbrowser.open(orig_url)

    def copy_short_url(self):
        sel = self.url_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a row to copy the shortened URL.")
            return
        vals = self.url_tree.item(sel, "values")
        short_url_val = vals[2]
        self.clipboard_clear()
        self.clipboard_append(short_url_val)
        messagebox.showinfo("Success", f"Shortened URL copied: {short_url_val}")

    def delete_url(self):
        sel = self.url_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a shortened URL to delete.")
            return
        db_id = self.url_tree.item(sel, "tags")[0]
        conn = sqlite3.connect("app_data.db")
        conn.cursor().execute("DELETE FROM urls WHERE id = ?", (db_id,))
        conn.commit()
        conn.close()
        self.filter_url_table()

    def clear_urls(self):
        if messagebox.askyesno("Confirm", "Delete all shortened URLs?"):
            conn = sqlite3.connect("app_data.db")
            conn.cursor().execute("DELETE FROM urls")
            conn.commit()
            conn.close()
            self.filter_url_table()

    # --- MODULE 3B.2: MESSAGING (SMS & EMAIL) ---
    def setup_messaging_page(self):
        ctk.CTkLabel(
            self.page_msg,
            text="Messaging Utility",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.page_msg,
            text="Simulate sending, receiving, and replying to SMS and Email messages.",
            font=("Segoe UI", 12),
            text_color=self.TEXT_MUTED,
        ).pack(anchor="w", pady=(0, 12))

        msg_tabview = ctk.CTkTabview(
            self.page_msg,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER_SUBTLE,
            fg_color=self.SURFACE_CARD,
            segmented_button_fg_color=self.SURFACE_SUB,
            segmented_button_selected_color=self.ACCENT,
            segmented_button_selected_hover_color=self.ACCENT_HOVER,
        )
        msg_tabview.pack(fill="both", expand=True)

        sms_tab = msg_tabview.add("SMS Utility")
        email_tab = msg_tabview.add("Email Utility")

        sms_frame = ctk.CTkFrame(sms_tab, fg_color=self.SURFACE_SUB, corner_radius=10, border_width=1, border_color=self.BORDER_SUBTLE)
        sms_frame.pack(fill="both", expand=True, padx=6, pady=6)

        ctk.CTkLabel(sms_frame, text="Mobile Number", font=("Segoe UI", 12, "bold"), text_color=self.TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(12, 4))
        self.sms_recipient = ctk.CTkEntry(sms_frame, placeholder_text="09123456789", width=320, height=36, corner_radius=8, fg_color=self.SURFACE_CARD, border_color=self.BORDER_SUBTLE)
        self.sms_recipient.pack(anchor="w", padx=14, pady=(0, 8))

        ctk.CTkLabel(sms_frame, text="Message Content", font=("Segoe UI", 12, "bold"), text_color=self.TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(0, 4))
        self.sms_content = ctk.CTkTextbox(sms_frame, width=440, height=78, corner_radius=8, fg_color=self.SURFACE_CARD, border_width=1, border_color=self.BORDER_SUBTLE)
        self.sms_content.pack(anchor="w", padx=14, pady=(0, 8))

        btn_row = ctk.CTkFrame(sms_frame, fg_color="transparent")
        btn_row.pack(anchor="w", padx=14, pady=(2, 8))

        ctk.CTkButton(btn_row, text="Send SMS", height=34, corner_radius=8, fg_color=self.ACCENT, hover_color=self.ACCENT_HOVER, font=("Segoe UI", 11, "bold"), command=lambda: self.send_message("SMS", "Sent")).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btn_row, text="Simulate Receive SMS", height=34, corner_radius=8, fg_color="transparent", hover_color=self.SURFACE_CARD, border_width=1, border_color=self.BORDER_SUBTLE, text_color=self.TEXT_PRIMARY, font=("Segoe UI", 11), command=lambda: self.send_message("SMS", "Received")).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="Reply", height=34, corner_radius=8, fg_color=self.SUCCESS, hover_color=self.SUCCESS_HOVER, font=("Segoe UI", 11, "bold"), command=lambda: self.send_message("SMS", "Reply")).pack(side="left", padx=4)

        self.sms_tree = ttk.Treeview(sms_frame, columns=("ID", "Action", "Number", "Message"), show="headings", height=5, style="Modern.Treeview")
        for c in ("ID", "Action", "Number", "Message"):
            self.sms_tree.heading(c, text=c)
            self.sms_tree.column(c, width=160)
        self.sms_tree.pack(fill="both", expand=True, padx=14, pady=(4, 12))

        email_frame = ctk.CTkFrame(email_tab, fg_color=self.SURFACE_CARD, corner_radius=10, border_width=1, border_color=self.BORDER_SUBTLE)
        email_frame.pack(fill="both", expand=True, padx=6, pady=6)

        ctk.CTkLabel(email_frame, text="Recipient Email", font=("Segoe UI", 12, "bold"), text_color=self.TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(12, 4))
        self.email_recipient = ctk.CTkEntry(email_frame, placeholder_text="user@example.com", width=320, height=36, corner_radius=8, fg_color=self.SURFACE_SUB, border_color=self.BORDER_SUBTLE)
        self.email_recipient.pack(anchor="w", padx=14, pady=(0, 8))

        ctk.CTkLabel(email_frame, text="Email Body", font=("Segoe UI", 12, "bold"), text_color=self.TEXT_PRIMARY).pack(anchor="w", padx=14, pady=(0, 4))
        self.email_content = ctk.CTkTextbox(email_frame, width=440, height=78, corner_radius=8, fg_color=self.SURFACE_SUB, border_width=1, border_color=self.BORDER_SUBTLE)
        self.email_content.pack(anchor="w", padx=14, pady=(0, 8))

        btn_row_e = ctk.CTkFrame(email_frame, fg_color="transparent")
        btn_row_e.pack(anchor="w", padx=14, pady=(2, 8))

        ctk.CTkButton(btn_row_e, text="Send Email", height=34, corner_radius=8, fg_color=self.ACCENT, hover_color=self.ACCENT_HOVER, font=("Segoe UI", 11, "bold"), command=lambda: self.send_message("Email", "Sent")).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btn_row_e, text="Simulate Receive Email", height=34, corner_radius=8, fg_color="transparent", hover_color=self.SURFACE_SUB, border_width=1, border_color=self.BORDER_SUBTLE, text_color=self.TEXT_PRIMARY, font=("Segoe UI", 11), command=lambda: self.send_message("Email", "Received")).pack(side="left", padx=4)

        self.email_tree = ttk.Treeview(email_frame, columns=("ID", "Action", "Recipient", "Body"), show="headings", height=5, style="Modern.Treeview")
        for c in ("ID", "Action", "Recipient", "Body"):
            self.email_tree.heading(c, text=c)
            self.email_tree.column(c, width=160)
        self.email_tree.pack(fill="both", expand=True, padx=14, pady=(4, 12))

        self.load_messages()

    def send_message(self, m_type, action):
        if m_type == "SMS":
            rec = self.sms_recipient.get().strip()
            content = self.sms_content.get("1.0", "end-1c").strip()
        else:
            rec = self.email_recipient.get().strip()
            content = self.email_content.get("1.0", "end-1c").strip()

        if not rec or not content:
            messagebox.showerror("Error", "Please fill out recipient and content fields.")
            return

        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (msg_type, action_type, sender, recipient, content) VALUES (?, ?, ?, ?, ?)",
                       (m_type, action, "SystemUser", rec, content))
        conn.commit()
        conn.close()

        if m_type == "SMS":
            self.sms_recipient.delete(0, "end")
            self.sms_content.delete("1.0", "end")
        else:
            self.email_recipient.delete(0, "end")
            self.email_content.delete("1.0", "end")

        self.load_messages()
        messagebox.showinfo("Success", f"{m_type} {action} successfully!")

    def load_messages(self):
        for i in self.sms_tree.get_children():
            self.sms_tree.delete(i)
        for i in self.email_tree.get_children():
            self.email_tree.delete(i)

        conn = sqlite3.connect("app_data.db")
        rows = conn.cursor().execute("SELECT * FROM messages").fetchall()
        conn.close()

        s_idx, e_idx = 1, 1
        for row in rows:
            _, m_type, action, _, recipient, content = row
            if m_type == "SMS":
                self.sms_tree.insert("", "end", values=(s_idx, action, recipient, content))
                s_idx += 1
            else:
                self.email_tree.insert("", "end", values=(e_idx, action, recipient, content))
                e_idx += 1


if __name__ == "__main__":
    from database import init_db
    init_db()
    app = App()
    app.mainloop()