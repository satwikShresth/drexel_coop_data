import os

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Annotated
from app.database import Connection, SalaryDatabase, UsCitiesDatabase


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
)


@app.get("/salary/header", response_model=List[Dict[str, str]])
async def get_table_header(db: Connection = Depends(SalaryDatabase)):
    try:
        data = db.fetchTableHeaders()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/salary/size", response_model=int)
async def get_table_size(db: Connection = Depends(SalaryDatabase)):
    try:
        data = db.fetchTableSize()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/salary/data", response_model=List[Dict[str, str | int | float]])
async def get_table_data(
    db: Annotated[Connection, Depends(SalaryDatabase)],
    start: int = Query(0, description="Start index for fetching data"),
    end: int = Query(10, description="End index for fetching data"),
):
    try:
        data = db.fetchTableData(start, end)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/company", response_model=List[Dict[str, str]])
async def get_company_name(
    db: Annotated[Connection, Depends(SalaryDatabase)],
    query: str = Query("", min_length=0, max_length=50)
):
    try:
        data = db.FetchStringMatchedData(query)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/uscities", response_model=List[Dict[str, str]])
async def get_cities_usa_data(
    db: Annotated[Connection, Depends(UsCitiesDatabase)],
    query: str = Query("", min_length=0, max_length=50)
):
    try:
        cities_data = db.FetchStringMatchedData(query)
        return JSONResponse(content=cities_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
