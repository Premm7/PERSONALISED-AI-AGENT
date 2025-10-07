# reminder_db.py
import sqlite3
from datetime import datetime
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "reminders.db")

def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note TEXT NOT NULL,
        remind_at TEXT NOT NULL,
        triggered INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    return conn

_conn = init_db()

def add_reminder(note, remind_at_str):
    c = _conn.cursor()
    c.execute("INSERT INTO reminders (note, remind_at, triggered) VALUES (?, ?, 0)", (note, remind_at_str))
    _conn.commit()
    return c.lastrowid

def get_due_reminders():
    """
    Returns list of (id, note, remind_at) where remind_at <= now and triggered == 0
    """
    now = datetime.now().isoformat()
    c = _conn.cursor()
    c.execute("SELECT id, note, remind_at FROM reminders WHERE triggered = 0 AND remind_at <= ?", (now,))
    rows = c.fetchall()
    return rows

def mark_triggered(reminder_id):
    c = _conn.cursor()
    c.execute("UPDATE reminders SET triggered = 1 WHERE id = ?", (reminder_id,))
    _conn.commit()
