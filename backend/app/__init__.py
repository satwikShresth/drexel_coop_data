from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import sqlite3
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'database', 'database.db')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
)


class SqliteConn():
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

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


@app.get("/data", response_model=List[Dict[str, str]])
def get_data(db: SqliteConn = Depends(SqliteConn)):
    data = db.fetchTable('salary')
    return JSONResponse(content=data)
