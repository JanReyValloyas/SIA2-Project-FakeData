import sqlite3
import customtkinter as ctk
from tkinter import messagebox, ttk
from faker import Faker
from auth import hash_password, verify_password

# Initialize Faker (English locale)
fake = Faker('en_PH')

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def init(self):
        super().init()
        self.title("SIA 2 Mini Project - Fake Data Generator")
        self.geometry("900x600")

        self.show_login_frame()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- LOGIN / REGISTER SCREEN ---
    def show_login_frame(self):
        self.clear_window()

        frame = ctk.CTkFrame(self, width=400, height=400)
        frame.pack(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        title = ctk.CTkLabel(frame, text="Login System", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        self.user_entry = ctk.CTkEntry(frame, placeholder_text="Username")
        self.user_entry.pack(pady=10, width=250)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.pass_entry.pack(pady=10, width=250)

        login_btn = ctk.CTkButton(frame, text="Login", command=self.handle_login)
        login_btn.pack(pady=10)

        reg_btn = ctk.CTkButton(frame, text="Register", fg_color="green", command=self.handle_register)
        reg_btn.pack(pady=5)

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
            cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
                           (username, pwd_hash, salt))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
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
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # --- MAIN DASHBOARD (Fake Data Generation) ---
    def show_dashboard(self):
        self.clear_window()

        # Header
        header = ctk.CTkLabel(self, text="Fake Data Generation Dashboard (Option 3B.3)", font=("Arial", 18, "bold"))
        header.pack(pady=15)

        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=20, pady=10)

        gen_btn = ctk.CTkButton(control_frame, text="Generate 10+ Fake Records", command=self.generate_and_save_data)
        gen_btn.pack(side="left", padx=10, pady=10)

        logout_btn = ctk.CTkButton(control_frame, text="Logout", fg_color="red", command=self.show_login_frame)
        logout_btn.pack(side="right", padx=10, pady=10)

        # Table / Treeview for Data Display
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_table()
        self.load_data_to_table()

        def create_table(self):
            columns = ("ID", "Name", "Address", "Birthdate", "Mobile", "Email", "Job", "City", "Company", "Card", "IP")
            self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")

            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)

            scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)

            self.tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        def generate_and_save_data(self):
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()

            # Generate 10 records with 10 fields each
            for _ in range(10):
                name = fake.name()
                address = fake.address().replace("\n", ", ")
                birthdate = str(fake.date_of_birth(minimum_age=18, maximum_age=60))
                mobile = fake.phone_number()
                email = fake.email()
                job = fake.job()
                city = fake.city()
                company = fake.company()
                credit_card = fake.credit_card_number(card_type='visa')
                ip = fake.ipv4()

                cursor.execute("""
                        INSERT INTO fake_records (name, address, birthdate, mobile_number, email, job, city, company, credit_card, ip_address)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (name, address, birthdate, mobile, email, job, city, company, credit_card, ip))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Successfully generated and saved 10 new fake records!")
            self.load_data_to_table()

        def load_data_to_table(self):
            for item in self.tree.get_children():
                self.tree.delete(item)

            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fake_records")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                self.tree.insert("", "end", values=row)

    if name == "main":
        from database import init_db
        init_db()
        app = App()
        app.mainloop()