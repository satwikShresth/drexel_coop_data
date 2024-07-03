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


@app.get("/salary/header", response_model=List[Dict[str, str]])
async def get_table_header(db: SqliteConn = Depends(SqDatabase)):
    data = db.fetchTableHeaders('salary')
    return JSONResponse(content=data)


@app.get("/salary/size", response_model=int)
async def get_table_size(db: SqliteConn = Depends(SqDatabase)):
    data = db.fetchTableSize('salary')
    return JSONResponse(content=data)


@app.get("/salary/data", response_model=List[Dict[str, str]])
async def get_table_data(
    start: int = Query(0, description="Start index for fetching data"),
    end: int = Query(10, description="End index for fetching data"),
    db: SqliteConn = Depends(SqDatabase)
):
    data = db.fetchTableData('salary', start, end)
    return JSONResponse(content=data)


@app.get("/uscities", response_model=List[Dict[str, str]])
async def get_all_cities_usa_data(
    query: str = Query("", min_length=0, max_length=50),
    db: SqliteConn = Depends(SqUsCitiesDatabase)
):
    cursor = db.conn.cursor()

    _query = "SELECT city, state_id FROM uscities "

    if query:
        _query += f"WHERE city LIKE %{query}% "

    _query += "LIMIT 50"

    cursor.execute(_query)
    rows = cursor.fetchall()
    cursor.close()

    return JSONResponse(
        content=[
            {
                "city": row[0],
                "state_id": row[1]
            } for row in rows
        ]
    )
