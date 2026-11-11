import sqlite3
import random
import customtkinter as ctk
from tkinter import messagebox, ttk
from faker import Faker
from auth import hash_password, verify_password

# Initialize Faker (English locale)
fake = Faker('en_PH')

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIA2 - Login System")
        self.geometry("900x650")

        self.show_login_frame()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- LOGIN / REGISTER SCREEN ---
    def show_login_frame(self):
        self.clear_window()
        self.title("SIA2 - Login System")

        frame = ctk.CTkFrame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(frame, text="Login System", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        self.user_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=250)
        self.user_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=250)
        self.pass_entry.pack(pady=10)

        self.show_pass_var = ctk.BooleanVar(value=False)
        show_pass_chk = ctk.CTkCheckBox(
            frame,
            text="Show Password",
            variable=self.show_pass_var,
            command=self.toggle_password_visibility,
            font=("Arial", 11)
        )
        show_pass_chk.pack(pady=5, anchor="w", padx=25)

        login_btn = ctk.CTkButton(frame, text="Login", command=self.handle_login)
        login_btn.pack(pady=10)

        reg_btn = ctk.CTkButton(frame, text="Register", fg_color="green", command=self.handle_register)
        reg_btn.pack(pady=5)

    def toggle_password_visibility(self):
        if self.show_pass_var.get():
            self.pass_entry.configure(show="")
        else:
            self.pass_entry.configure(show="*")

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
            self.title("SIA2 - Fake Data Generation Dashboard")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # --- MAIN DASHBOARD (Fake Data Generation) ---
    def show_dashboard(self):
        self.clear_window()

        header = ctk.CTkLabel(self, text="Fake Data Generation Dashboard (Option 3B.3)", font=("Arial", 18, "bold"))
        header.pack(pady=10, padx=20, anchor="w")

        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=20, pady=5)

        gen_btn = ctk.CTkButton(control_frame, text="Generate Records", command=self.generate_and_save_data)
        gen_btn.pack(side="left", padx=5, pady=10)

        self.count_entry = ctk.CTkEntry(control_frame, width=60, justify="center")
        self.count_entry.insert(0, "10")
        self.count_entry.pack(side="left", padx=5, pady=10)

        del_selected_btn = ctk.CTkButton(control_frame, text="Delete Selected", fg_color="#d9534f", command=self.delete_selected_row)
        del_selected_btn.pack(side="left", padx=5, pady=10)

        clear_btn = ctk.CTkButton(control_frame, text="Clear All Data", fg_color="orange", text_color="black",
                                  command=self.clear_all_data)
        clear_btn.pack(side="left", padx=5, pady=10)

        export_btn = ctk.CTkButton(control_frame, text="Export to CSV", fg_color="green", command=self.export_to_csv)
        export_btn.pack(side="left", padx=5, pady=10)

        logout_btn = ctk.CTkButton(control_frame, text="Logout", fg_color="red", command=self.show_login_frame)
        logout_btn.pack(side="right", padx=5, pady=10)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=5)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search by Name or Job...", width=300)
        self.search_entry.pack(side="left", padx=0)
        self.search_entry.bind("<KeyRelease>", self.filter_table)

        self.count_label = ctk.CTkLabel(search_frame, text="Total Records: 0", font=("Arial", 12, "bold"))
        self.count_label.pack(side="right", padx=5)

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_table()
        self.load_data_to_table()

    def create_table(self):
        columns = ("ID", "Name", "Address", "Birthdate", "Mobile", "Email", "Username", "Job Title", "Company", "City", "Country", "Blood Type", "Website")

        table_container = ctk.CTkFrame(self.tree_frame)
        table_container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_container, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="w", stretch=False)

        scrollbar_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

    def generate_and_save_data(self):
        try:
            num_records = int(self.count_entry.get())
            if num_records < 10:
                messagebox.showerror("Invalid Input", "Minimum records to generate must be at least 10.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for record count.")
            return

        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()

        blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        for _ in range(num_records):
            name = fake.name()
            address = fake.address().replace("\n", ", ")
            birthdate = str(fake.date_of_birth(minimum_age=18, maximum_age=60))
            mobile = fake.numerify(text="09#########")
            email = fake.email()
            username = fake.user_name()
            job = fake.job()
            company = fake.company()
            city = fake.city()
            country = fake.current_country()
            blood_type = random.choice(blood_types)  # Pinalitan para maiwasan ang error
            website = fake.url()

            cursor.execute("""
                INSERT INTO fake_records (name, address, birthdate, mobile_number, email, username, job, company, city, country, blood_type, website)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, address, birthdate, mobile, email, username, job, company, city, country, blood_type, website))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Successfully generated and saved {num_records} new fake records!")
        self.load_data_to_table()

    def delete_selected_row(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record from the table to delete.")
            return

        if messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected record?"):
            item_tags = self.tree.item(selected_item, "tags")
            record_id = item_tags[0]

            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fake_records WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Selected record has been deleted.")
            self.load_data_to_table()

    def clear_all_data(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete all records?"):
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fake_records")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='fake_records'")
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "All records have been cleared and ID reset to 1.")
            self.load_data_to_table()

    def export_to_csv(self):
        import csv
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fake_records")
            rows = cursor.fetchall()
            conn.close()

            columns = ["ID", "Name", "Address", "Birthdate", "Mobile", "Email", "Username", "Job Title", "Company", "City", "Country", "Blood Type", "Website"]

            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)

            messagebox.showinfo("Success", f"Data successfully exported to {file_path}!")

    def filter_table(self, event):
        query = self.search_entry.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fake_records")
        rows = cursor.fetchall()
        conn.close()

        count = 0
        display_index = 1
        for row in rows:
            if query in str(row[1]).lower() or query in str(row[6]).lower():
                display_row = (display_index, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
                self.tree.insert("", "end", values=display_row, tags=(row[0],))
                count += 1
                display_index += 1

        self.count_label.configure(text=f"Total Records: {count}")

    def load_data_to_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fake_records")
        rows = cursor.fetchall()
        conn.close()

        count = 0
        for index, row in enumerate(rows, start=1):
            display_row = (index, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            self.tree.insert("", "end", values=display_row, tags=(row[0],))
            count += 1

        self.count_label.configure(text=f"Total Records: {count}")


if __name__ == "__main__":
    from database import init_db

    init_db()
    app = App()
    app.mainloop()