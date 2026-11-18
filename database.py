import sqlite3

def init_db():
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    # 2. Fake Records Table (12 fields)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fake_records (
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

    # 3. URL Shortener Table (3B.1) na may clicks column
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT NOT NULL,
                clicks INTEGER DEFAULT 0
            )
        """)
    # 4. Messaging Table (3B.2 - SMS & Email)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msg_type TEXT NOT NULL, -- 'SMS' o 'Email'
            action_type TEXT NOT NULL, -- 'Sent', 'Received', 'Reply'
            sender TEXT,
            recipient TEXT,
            content TEXT
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database tables initialized successfully!")