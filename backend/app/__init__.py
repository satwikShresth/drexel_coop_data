from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from app.sqlite import SqliteConn
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
COOP_DB_PATH = os.path.join(ROOT_DIR, 'database', 'database.db')
US_CITIES_DB_PATH = os.path.join(ROOT_DIR, 'database', 'uscities.db')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
)


class SqDatabase(SqliteConn):
    db_path = COOP_DB_PATH


class SqUsCitiesDatabase(SqliteConn):
    db_path = US_CITIES_DB_PATH


@app.get("/data", response_model=List[Dict[str, str]])
async def get_data(db: SqliteConn = Depends(SqDatabase)):
    data = db.fetchTable('salary')
    return JSONResponse(content=data)


@app.get("/uscities", response_model=List[Dict[str, str]])
async def get_all_cities_usa_data(
    query: str = Query("", min_length=0, max_length=50),
    db: SqliteConn = Depends(SqUsCitiesDatabase)
):
    cursor = db.conn.cursor()
    if query:
        cursor.execute(
            "SELECT city, state_id FROM uscities WHERE city LIKE ? LIMIT 50", (f"%{query}%",))
    else:
        cursor.execute("SELECT city, state_id FROM uscities LIMIT 50")
    rows = cursor.fetchall()
    cursor.close()
    data = [{"city": row[0], "state_id": row[1]} for row in rows]
    return JSONResponse(content=data)
