import sqlite3


DB_NAME = "data/emails.db"


# =========================================================
# CREATE TABLE
# =========================================================

def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        gmail_id TEXT UNIQUE,

        sender TEXT,

        subject TEXT,

        body TEXT,

        category TEXT,

        sentiment TEXT,

        priority TEXT,

        date TEXT,

        labels TEXT

    )
    """)

    conn.commit()

    conn.close()

def migrate_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get existing columns
    cursor.execute("PRAGMA table_info(emails)")

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    # Add gmail_id if missing
    if "gmail_id" not in columns:

        cursor.execute("""
            ALTER TABLE emails
            ADD COLUMN gmail_id TEXT
        """)

    # Add labels if missing
    if "labels" not in columns:

        cursor.execute("""
            ALTER TABLE emails
            ADD COLUMN labels TEXT
        """)

    conn.commit()
    conn.close()

# =========================================================
# SAVE EMAIL
# =========================================================

def save_email(
    gmail_id,
    sender,
    subject,
    body,
    category,
    sentiment,
    priority,
    date,
    labels
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO emails
        (
            gmail_id,
            sender,
            subject,
            body,
            category,
            sentiment,
            priority,
            date,
            labels
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        gmail_id,
        sender,
        subject,
        body,
        category,
        sentiment,
        priority,
        date,
        labels

    ))

    conn.commit()

    conn.close()


# =========================================================
# GET EMAILS
# =========================================================

def get_emails():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            gmail_id,
            sender,
            subject,
            body,
            category,
            sentiment,
            priority,
            date,
            labels
        FROM emails
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# DELETE SELECTED
# =========================================================

def delete_selected(email_ids):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.executemany(
        "DELETE FROM emails WHERE id=?",
        [(i,) for i in email_ids]
    )

    conn.commit()

    conn.close()


# =========================================================
# DELETE ONE
# =========================================================

def delete_email(email_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM emails WHERE id=?",
        (email_id,)
    )

    conn.commit()

    conn.close()
    
create_table()
migrate_database()
