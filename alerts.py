import sqlite3

DB_NAME = "alerts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        target_price REAL NOT NULL,
        active INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    conn.close()

def add_alert(email, origin, destination, target_price):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO alerts (email, origin, destination, target_price)
    VALUES (?, ?, ?, ?)
    """, (email, origin.upper(), destination.upper(), target_price))

    conn.commit()
    conn.close()
