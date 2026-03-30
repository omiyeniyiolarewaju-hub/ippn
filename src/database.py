import sqlite3
import json
import os

class DatabaseManager:
    def __init__(self, db_path="outputs/omiye.db"):
        self.db_path = db_path
        # Ensure outputs directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        """Initialize SQLite database and create tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    narrative TEXT,
                    structured_data TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_report(self, source, narrative, structured_data):
        """Save report entry to the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reports (source, narrative, structured_data) VALUES (?, ?, ?)",
                (source, narrative, json.dumps(structured_data))
            )
            conn.commit()
            return cursor.lastrowid
