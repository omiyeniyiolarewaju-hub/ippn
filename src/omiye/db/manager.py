import sqlite3
import json
from omiye.config import Config
from omiye.core.models import CrimeReport

class DatabaseManager:
    def __init__(self, db_path=Config.DATABASE_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crime_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crime_type TEXT,
                    date TEXT,
                    time TEXT,
                    location TEXT,
                    complainant TEXT,
                    suspects TEXT,
                    weapons TEXT,
                    victims TEXT,
                    items_stolen TEXT,
                    summary TEXT,
                    raw_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_report(self, report: CrimeReport):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO crime_reports (
                    crime_type, date, time, location, complainant, 
                    suspects, weapons, victims, items_stolen, summary, raw_text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                report.crime_type,
                report.date,
                report.time,
                report.location,
                report.complainant,
                json.dumps(report.suspects),
                json.dumps(report.weapons),
                json.dumps(report.victims),
                json.dumps(report.items_stolen),
                report.summary,
                report.raw_text
            ))
            conn.commit()
            return cursor.lastrowid
