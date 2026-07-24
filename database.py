# ==========================================
# AI IT Support Genie
# Database
# ==========================================

import sqlite3
from datetime import datetime

DB_NAME = "data/chatbot.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS query_log(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        user_query TEXT,

        predicted_category TEXT,

        confidence REAL,

        sop_recommended TEXT

    )
    """)

    conn.commit()

    conn.close()


def save_query(user_query, category, confidence, sop):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO query_log(

    timestamp,

    user_query,

    predicted_category,

    confidence,

    sop_recommended

    )

    VALUES(?,?,?,?,?)

    """,

    (

    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    user_query,

    category,

    confidence,

    sop

    ))

    conn.commit()

    conn.close()