import sqlite3
import random
import string
import json
import csv
from tkinter import messagebox, filedialog, ttk
import customtkinter as ctk
from faker import Faker
from auth import hash_password, verify_password

# Initialize Faker
fake = Faker('en_PH')

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIA2 - Login System")
        self.geometry("1050x720")

        self.show_login_frame()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- LOGIN / REGISTER SCREEN (Modern Card UI) ---
    def show_login_frame(self):
        self.clear_window()
        self.title("SIA2 - Login System")

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        card_frame = ctk.CTkFrame(main_frame, width=380, height=420, corner_radius=16)
        card_frame.pack(padx=20, pady=20)
        card_frame.pack_propagate(False)

        title = ctk.CTkLabel(card_frame, text="Welcome Back!", font=("Arial", 22, "bold"))
        title.pack(pady=(30, 5))

        subtitle = ctk.CTkLabel(card_frame, text="SIA2 Utilities Dashboard (3B)", font=("Arial", 12), text_color="gray")
        subtitle.pack(pady=(0, 20))

        self.user_entry = ctk.CTkEntry(card_frame, placeholder_text="Username", width=280, height=40, corner_radius=8)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(card_frame, placeholder_text="Password", show="*", width=280, height=40,
                                       corner_radius=8)
        self.pass_entry.pack(pady=10)

        self.show_pass_var = ctk.BooleanVar(value=False)
        show_pass_chk = ctk.CTkCheckBox(
            card_frame, text="Show Password", variable=self.show_pass_var,
            command=lambda: self.pass_entry.configure(show="" if self.show_pass_var.get() else "*"),
            font=("Arial", 11)
        )
        show_pass_chk.pack(pady=(5, 15), anchor="w", padx=50)

        login_btn = ctk.CTkButton(card_frame, text="Login", width=280, height=40, corner_radius=8,
                                  command=self.handle_login)
        login_btn.pack(pady=5)

        reg_btn = ctk.CTkButton(card_frame, text="Create Account / Register", fg_color="transparent", border_width=1,
                                text_color=("black", "white"), width=280, height=35, corner_radius=8,
                                command=self.handle_register)
        reg_btn.pack(pady=10)

    def handle_register(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
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
        username = self.user_entry.get()
        password = self.pass_entry.get()
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password, salt FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and verify_password(result[0], result[1], password):
            self.title("SIA2 - Utilities Dashboard (3B)")
            self.show_main_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # --- MAIN DASHBOARD WITH TABS ---
    def show_main_dashboard(self):
        self.clear_window()

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=10)

        title_lbl = ctk.CTkLabel(top_frame, text="SIA2 Utilities Dashboard (Option 3B)", font=("Arial", 18, "bold"))
        title_lbl.pack(side="left")

        logout_btn = ctk.CTkButton(top_frame, text="Logout", fg_color="red", width=80, command=self.show_login_frame)
        logout_btn.pack(side="right")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_fake = self.tabview.add("3B.3 Fake Data Gen")
        self.tab_url = self.tabview.add("3B.1 URL Shortener")
        self.tab_msg = self.tabview.add("3B.2 Messaging")

        self.setup_fake_data_tab()
        self.setup_url_tab()
        self.setup_messaging_tab()

    # --- MODULE 3B.3: FAKE DATA GEN ---
    def setup_fake_data_tab(self):
        control_frame = ctk.CTkFrame(self.tab_fake)
        control_frame.pack(fill="x", padx=10, pady=5)

        gen_btn = ctk.CTkButton(control_frame, text="Generate Records", command=self.generate_and_save_data)
        gen_btn.pack(side="left", padx=4, pady=8)

        self.count_entry = ctk.CTkEntry(control_frame, width=50, justify="center")
        self.count_entry.insert(0, "10")
        self.count_entry.pack(side="left", padx=4, pady=8)

        del_btn = ctk.CTkButton(control_frame, text="Delete Selected", fg_color="#d9534f", width=100,
                                command=self.delete_fake_row)
        del_btn.pack(side="left", padx=4, pady=8)

        clear_btn = ctk.CTkButton(control_frame, text="Clear All", fg_color="orange", text_color="black", width=80,
                                  command=self.clear_fake_data)
        clear_btn.pack(side="left", padx=4, pady=8)

        copy_btn = ctk.CTkButton(control_frame, text="Copy Selected", fg_color="#5bc0de", text_color="black", width=100,
                                 command=self.copy_fake_row)
        copy_btn.pack(side="left", padx=4, pady=8)

        export_csv_btn = ctk.CTkButton(control_frame, text="Export CSV", fg_color="green", width=90,
                                       command=self.export_fake_csv)
        export_csv_btn.pack(side="left", padx=4, pady=8)

        export_json_btn = ctk.CTkButton(control_frame, text="Export JSON", fg_color="#2b9348", width=95,
                                        command=self.export_fake_json)
        export_json_btn.pack(side="left", padx=4, pady=8)

        search_frame = ctk.CTkFrame(self.tab_fake, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by Name, Job, City, Company...",
                                         width=320)
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self.filter_fake_table)

        self.count_label = ctk.CTkLabel(search_frame, text="Total Records: 0", font=("Arial", 12, "bold"))
        self.count_label.pack(side="right", padx=5)

        tree_container = ctk.CTkFrame(self.tab_fake)
        tree_container.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Name", "Address", "Birthdate", "Mobile", "Email", "Username", "Job Title", "Company", "City",
                   "Country", "Blood Type", "Website")
        self.fake_tree = ttk.Treeview(tree_container, columns=columns, show="headings")

        for col in columns:
            self.fake_tree.heading(col, text=col)
            self.fake_tree.column(col, width=120, anchor="w")

        sb_y = ttk.Scrollbar(tree_container, orient="vertical", command=self.fake_tree.yview)
        sb_x = ttk.Scrollbar(tree_container, orient="horizontal", command=self.fake_tree.xview)
        self.fake_tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        self.fake_tree.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        self.load_fake_data()

    def generate_and_save_data(self):
        try:
            num = int(self.count_entry.get())
            if num < 1:
                messagebox.showerror("Error", "Minimum count is 1.")
                return
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")
            return

        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        b_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        for _ in range(num):
            cursor.execute("""
                INSERT INTO fake_records (name, address, birthdate, mobile_number, email, username, job, company, city, country, blood_type, website)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fake.name(), fake.address().replace("\n", ", "),
                  str(fake.date_of_birth(minimum_age=18, maximum_age=60)),
                  fake.numerify("09#########"), fake.email(), fake.user_name(), fake.job(), fake.company(),
                  fake.city(), fake.current_country(), random.choice(b_types), fake.url()))
        conn.commit()
        conn.close()
        self.load_fake_data()
        messagebox.showinfo("Success", f"Generated {num} records successfully!")

    def load_fake_data(self):
        for i in self.fake_tree.get_children(): self.fake_tree.delete(i)
        conn = sqlite3.connect("app_data.db")
        rows = conn.cursor().execute("SELECT * FROM fake_records").fetchall()
        conn.close()
        for idx, row in enumerate(rows, start=1):
            self.fake_tree.insert("", "end", values=(idx, *row[1:]), tags=(row[0],))
        self.count_label.configure(text=f"Total Records: {len(rows)}")

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
        row_str = " | ".join(str(v) for v in vals[1:])  # Skip ID
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
                w.writerow(
                    ["ID", "Name", "Address", "Birthdate", "Mobile", "Email", "Username", "Job", "Company", "City",
                     "Country", "Blood", "Website"])
                w.writerows(rows)
            messagebox.showinfo("Success", "Exported to CSV successfully!")

    def export_fake_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if path:
            conn = sqlite3.connect("app_data.db")
            rows = conn.cursor().execute("SELECT * FROM fake_records").fetchall()
            conn.close()
            keys = ["id", "name", "address", "birthdate", "mobile_number", "email", "username", "job", "company",
                    "city", "country", "blood_type", "website"]
            data = [dict(zip(keys, row)) for row in rows]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "Exported to JSON successfully!")

    def filter_fake_table(self, event):
        q = self.search_entry.get().lower()
        for i in self.fake_tree.get_children(): self.fake_tree.delete(i)
        conn = sqlite3.connect("app_data.db")
        rows = conn.cursor().execute("SELECT * FROM fake_records").fetchall()
        conn.close()
        c = 1
        for row in rows:
            # row indices: 1:name, 6:username, 7:job, 8:company, 9:city
            if any(q in str(row[idx]).lower() for idx in [1, 6, 7, 8, 9]):
                self.fake_tree.insert("", "end", values=(c, *row[1:]), tags=(row[0],))
                c += 1
        self.count_label.configure(text=f"Filtered Records: {c - 1}")

    # --- MODULE 3B.1: URL SHORTENER ---
    def setup_url_tab(self):
        frame = ctk.CTkFrame(self.tab_url)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Original URL:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        self.orig_url_entry = ctk.CTkEntry(frame, placeholder_text="https://example.com/very-long-link", width=500)
        self.orig_url_entry.pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Custom Alias (Optional):", font=("Arial", 12)).pack(anchor="w", padx=10, pady=(5, 0))
        self.alias_entry = ctk.CTkEntry(frame, placeholder_text="e.g. mylink (blank for random)", width=300)
        self.alias_entry.pack(anchor="w", padx=10, pady=5)

        short_btn = ctk.CTkButton(frame, text="Shorten URL", fg_color="blue", command=self.shorten_url)
        short_btn.pack(anchor="w", padx=10, pady=10)

        ctk.CTkLabel(frame, text="Generated Shortened URLs & Analytics:", font=("Arial", 14, "bold")).pack(anchor="w",
                                                                                                           padx=10,
                                                                                                           pady=10)

        columns = ("ID", "Original URL", "Shortened URL", "Clicks")
        self.url_tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.url_tree.heading(col, text=col)
            self.url_tree.column(col, width=200, anchor="w")
        self.url_tree.pack(fill="both", expand=True, padx=10, pady=5)

        btn_row_url = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row_url.pack(anchor="w", padx=10, pady=10)

        test_btn = ctk.CTkButton(btn_row_url, text="Test Selected URL (Open)", fg_color="green", command=self.test_url)
        test_btn.pack(side="left", padx=5)

        copy_url_btn = ctk.CTkButton(btn_row_url, text="Copy Short URL", fg_color="#5bc0de", text_color="black",
                                     command=self.copy_short_url)
        copy_url_btn.pack(side="left", padx=5)

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
            # Clean alias characters
            code = "".join(c for c in alias if c.isalnum() or c.isin("_"))
        else:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        short_url = f"http://short.ly/{code}"

        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO urls (original_url, short_code, clicks) VALUES (?, ?, ?)", (orig, short_url, 0))
            conn.commit()
            conn.close()

            self.orig_url_entry.delete(0, 'end')
            self.alias_entry.delete(0, 'end')
            self.load_url_data()
            messagebox.showinfo("Success", f"URL Shortened Successfully!\n{short_url}")
        except sqlite3.OperationalError:
            # Fallback kung wala pa ang clicks column sa lumang database table
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

    def load_url_data(self):
        for i in self.url_tree.get_children(): self.url_tree.delete(i)
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        try:
            rows = cursor.execute("SELECT id, original_url, short_code, clicks FROM urls").fetchall()
        except sqlite3.OperationalError:
            self.upgrade_url_db_schema()
            rows = cursor.execute("SELECT id, original_url, short_code, clicks FROM urls").fetchall()
        conn.close()

        for idx, row in enumerate(rows, start=1):
            # row: (db_id, orig, short, clicks)
            self.url_tree.insert("", "end", values=(idx, row[1], row[2], row[3]), tags=(row[0], row[1]))

    def test_url(self):
        import webbrowser
        sel = self.url_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a shortened URL to test.")
            return
        item_data = self.url_tree.item(sel, "tags")
        db_id = item_data[0]
        orig_url = item_data[1]

        # Increment click count in database
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = ?", (db_id,))
        conn.commit()
        conn.close()

        self.load_url_data()
        webbrowser.open(orig_url)

    def copy_short_url(self):
        sel = self.url_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a row to copy the shortened URL.")
            return
        vals = self.url_tree.item(sel, "values")
        short_url_val = vals[2]  # Shortened URL column
        self.clipboard_clear()
        self.clipboard_append(short_url_val)
        messagebox.showinfo("Success", f"Shortened URL copied: {short_url_val}")

    # --- MODULE 3B.2: MESSAGING (SMS & EMAIL) ---
    def setup_messaging_tab(self):
        msg_tabview = ctk.CTkTabview(self.tab_msg)
        msg_tabview.pack(fill="both", expand=True, padx=10, pady=10)

        sms_tab = msg_tabview.add("SMS Utility")
        email_tab = msg_tabview.add("Email Utility")

        # SMS Sub-Tab
        sms_frame = ctk.CTkFrame(sms_tab)
        sms_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(sms_frame, text="Mobile Number:", font=("Arial", 12)).pack(anchor="w", padx=10)
        self.sms_recipient = ctk.CTkEntry(sms_frame, placeholder_text="09123456789", width=300)
        self.sms_recipient.pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(sms_frame, text="Message Content:", font=("Arial", 12)).pack(anchor="w", padx=10)
        self.sms_content = ctk.CTkTextbox(sms_frame, width=400, height=80)
        self.sms_content.pack(anchor="w", padx=10, pady=5)

        btn_row = ctk.CTkFrame(sms_frame, fg_color="transparent")
        btn_row.pack(anchor="w", padx=10, pady=5)

        ctk.CTkButton(btn_row, text="Send SMS", fg_color="blue", command=lambda: self.send_message("SMS", "Sent")).pack(
            side="left", padx=5)
        ctk.CTkButton(btn_row, text="Simulate Receive SMS", fg_color="orange", text_color="black",
                      command=lambda: self.send_message("SMS", "Received")).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="Reply", fg_color="green", command=lambda: self.send_message("SMS", "Reply")).pack(
            side="left", padx=5)

        self.sms_tree = ttk.Treeview(sms_frame, columns=("ID", "Action", "Number", "Message"), show="headings",
                                     height=5)
        for c in ("ID", "Action", "Number", "Message"):
            self.sms_tree.heading(c, text=c)
            self.sms_tree.column(c, width=150)
        self.sms_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Email Sub-Tab
        email_frame = ctk.CTkFrame(email_tab)
        email_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(email_frame, text="Recipient Email:", font=("Arial", 12)).pack(anchor="w", padx=10)
        self.email_recipient = ctk.CTkEntry(email_frame, placeholder_text="user@example.com", width=300)
        self.email_recipient.pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(email_frame, text="Email Body:", font=("Arial", 12)).pack(anchor="w", padx=10)
        self.email_content = ctk.CTkTextbox(email_frame, width=400, height=80)
        self.email_content.pack(anchor="w", padx=10, pady=5)

        btn_row_e = ctk.CTkFrame(email_frame, fg_color="transparent")
        btn_row_e.pack(anchor="w", padx=10, pady=5)

        ctk.CTkButton(btn_row_e, text="Send Email", fg_color="blue",
                      command=lambda: self.send_message("Email", "Sent")).pack(side="left", padx=5)
        ctk.CTkButton(btn_row_e, text="Simulate Receive Email", fg_color="orange", text_color="black",
                      command=lambda: self.send_message("Email", "Received")).pack(side="left", padx=5)

        self.email_tree = ttk.Treeview(email_frame, columns=("ID", "Action", "Recipient", "Body"), show="headings",
                                       height=5)
        for c in ("ID", "Action", "Recipient", "Body"):
            self.email_tree.heading(c, text=c)
            self.email_tree.column(c, width=150)
        self.email_tree.pack(fill="both", expand=True, padx=10, pady=10)

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
        cursor.execute(
            "INSERT INTO messages (msg_type, action_type, sender, recipient, content) VALUES (?, ?, ?, ?, ?)",
            (m_type, action, "SystemUser", rec, content))
        conn.commit()
        conn.close()

        # Clear inputs after sending
        if m_type == "SMS":
            self.sms_recipient.delete(0, 'end')
            self.sms_content.delete("1.0", 'end')
        else:
            self.email_recipient.delete(0, 'end')
            self.email_content.delete("1.0", 'end')

        self.load_messages()
        messagebox.showinfo("Success", f"{m_type} {action} successfully!")

    def load_messages(self):
        for i in self.sms_tree.get_children(): self.sms_tree.delete(i)
        for i in self.email_tree.get_children(): self.email_tree.delete(i)

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