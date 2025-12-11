# core/logger.py

import sqlite3
from datetime import datetime
import csv
from typing import List, Tuple


class AuditLogger:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                action TEXT,
                status TEXT,
                timestamp TEXT
            )
        """)

        conn.commit()
        conn.close()

    def record(self, username: str, action: str, status: str) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO audit_log (username, action, status, timestamp)
            VALUES (?, ?, ?, ?)
        """, (username, action, status, timestamp))

        conn.commit()
        conn.close()

    def fetch_logs(self, limit: int = 1000, filters: dict = None) -> List[Tuple]:
        """
        Fetch logs from the DB.

        :param limit: maximum number of rows to return
        :param filters: optional dict with keys 'username', 'action', 'status'
        :return: list of tuples (username, action, status, timestamp)
        """
        filters = filters or {}
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        clauses = []
        params = []

        if 'username' in filters and filters['username']:
            clauses.append("username = ?")
            params.append(filters['username'])
        if 'action' in filters and filters['action']:
            clauses.append("action = ?")
            params.append(filters['action'])
        if 'status' in filters and filters['status']:
            clauses.append("status = ?")
            params.append(filters['status'])

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = f"SELECT username, action, status, timestamp FROM audit_log {where} ORDER BY id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def export_csv(self, csv_path: str, limit: int = 1000, filters: dict = None) -> None:
        rows = self.fetch_logs(limit=limit, filters=filters)
        with open(csv_path, "w", newline='', encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["username", "action", "status", "timestamp"])
            writer.writerows(rows)
