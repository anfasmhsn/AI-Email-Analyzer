import sqlite3

DB_NAME = "data/emails.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            category TEXT,
            sentiment TEXT,
            priority TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_email(email, category, sentiment, priority):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emails
        (email, category, sentiment, priority)
        VALUES (?, ?, ?, ?)
    """, (email, category, sentiment, priority))

    conn.commit()
    conn.close()


def get_emails():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM emails")

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_email(email_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM emails WHERE id=?",
        (email_id,)
    )

    conn.commit()
    conn.close()