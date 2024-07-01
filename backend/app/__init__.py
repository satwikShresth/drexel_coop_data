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
    allow_origins=["*"],  # Adjust this to your specific frontend origin if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        yield conn
    finally:
        conn.close()


def fetch_data_from_db(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, str]]:
    cursor = conn.cursor()
    query = f'SELECT * FROM "{table_name}"'
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    return data


@app.get("/data", response_model=List[Dict[str, str]])
def get_data(db: sqlite3.Connection = Depends(get_db)):
    table_name = 'salary'
    data = fetch_data_from_db(db, table_name)
    return JSONResponse(content=data)
