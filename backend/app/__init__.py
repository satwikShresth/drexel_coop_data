import os

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from app.sqlite import SalaryDatabase, UsCitiesDatabase, SqliteConn


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
)


@app.get("/salary/header", response_model=List[Dict[str, str]])
async def get_table_header(db: SqliteConn = Depends(SalaryDatabase)):
    try:
        data = db.fetchTableHeaders()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/salary/size", response_model=int)
async def get_table_size(db: SqliteConn = Depends(SalaryDatabase)):
    try:
        data = db.fetchTableSize()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/salary/data", response_model=List[Dict[str, str]])
async def get_table_data(
    start: int = Query(0, description="Start index for fetching data"),
    end: int = Query(10, description="End index for fetching data"),
    db: SqliteConn = Depends(SalaryDatabase)
):
    try:
        data = db.fetchTableData(start, end)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/uscities", response_model=List[Dict[str, str]])
async def get_cities_usa_data(
    query: str = Query("", min_length=0, max_length=50),
    db: SqliteConn = Depends(UsCitiesDatabase)
):
    try:
        cities_data = db.FetchStringMatchedData(query, db)
        return JSONResponse(content=cities_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
