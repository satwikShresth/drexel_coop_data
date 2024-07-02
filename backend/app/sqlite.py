from typing import List, Dict
from app.singleton import Singleton
import sqlite3


class SqliteConn(Singleton):
    db_path: str = None

    def __init__(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

    def fetchTable(self, name) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()
        query = f'SELECT * FROM "{name}"'
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data

    def __del__(self):
        self.conn.close()
