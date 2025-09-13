import sqlite3

def init_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
              text TEXT NOT NULL,
              color TEXT NOT NULL
            )
        """)
    conn.commit()
    conn.close()