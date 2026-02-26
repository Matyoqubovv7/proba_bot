import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "bot.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            extra TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def save_registration(telegram_id: int, role: str, full_name: str, age: int, phone: str, extra: str | None):
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO registrations (telegram_id, role, full_name, age, phone, extra)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (telegram_id, role, full_name, age, phone, extra),
    )
    conn.commit()
    conn.close()

