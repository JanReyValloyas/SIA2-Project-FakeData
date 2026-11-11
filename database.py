import sqlite3


def init_db():
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()

    # 1. Users table (Hindi ito mabubura para ligtas ang iyong login accounts)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    # 2. I-drop at muling gawin ang fake_records para laging updated sa 12 fields
    cursor.execute("DROP TABLE IF EXISTS fake_records")

    cursor.execute("""
        CREATE TABLE fake_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            birthdate TEXT,
            mobile_number TEXT,
            email TEXT,
            username TEXT,
            job TEXT,
            company TEXT,
            city TEXT,
            country TEXT,
            blood_type TEXT,
            website TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database and tables successfully created/updated!")