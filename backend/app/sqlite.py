from typing import List, Dict
from app.common.singleton import Singleton
import sqlite3


class SqliteConn(Singleton):
    db_path: str = None

    def __init__(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

    def fetchTableData(
        self,
        table_name: str,
        start: int = None,
        end: int = None
    ) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()

        query = f"""
            SELECT *
            FROM {table_name}
            """

        if start is not None and end is not None:
            query += f"""
                LIMIT {end - start}
                OFFSET {start}
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data

    def fetchTableSize(
        self,
        table_name: str
    ) -> int:
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        size = cursor.fetchone()[0]
        return size

    def fetchTableHeaders(
        self,
        table_name: str
    ) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        return [col[1] for col in columns_info]

    def __del__(self):
        self.conn.close()
