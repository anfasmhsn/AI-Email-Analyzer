import sqlite3

DB_NAME = "data/emails.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        subject TEXT,
        body TEXT,
        category TEXT,
        sentiment TEXT,
        priority TEXT,
        date TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_email(
    sender,
    subject,
    body,
    category,
    sentiment,
    priority,
    date
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emails
        (
            sender,
            subject,
            body,
            category,
            sentiment,
            priority,
            date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        sender,
        subject,
        body,
        category,
        sentiment,
        priority,
        date
    ))

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