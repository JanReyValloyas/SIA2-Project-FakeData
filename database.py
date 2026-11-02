import sqlite3


def init_db():
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()

    # Table para sa Login / Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    # Table para sa Fake Data (10 fields)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fake_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            birthdate TEXT,
            mobile_number TEXT,
            email TEXT,
            job TEXT,
            city TEXT,
            company TEXT,
            credit_card TEXT,
            ip_address TEXT
        )
    """)

    conn.commit()
    conn.close()


if name == "main":
    init_db()
    print("Database at tables ay matagumpay na nagawa!")