import sqlite3
from typing import Optional

DB_FILE = 'processed_activities.db'

def initialize_db():
    """Initialize the database and create the processed_activities table if it doesn't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_activities (
                id INTEGER PRIMARY KEY,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def is_activity_processed(activity_id: int) -> bool:
    """Check if an activity ID has already been processed."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM processed_activities WHERE id = ?", (activity_id,))
        result = cursor.fetchone()
    return result is not None

def mark_activity_processed(activity_id: int) -> None:
    """Mark an activity as processed by storing it in the database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO processed_activities (id) VALUES (?)", (activity_id,))
        conn.commit()
