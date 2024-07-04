from typing import List, Dict, Any
from abc import ABC
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from app.common.singleton import Singleton

import app.database.uscities as uscities
import app.database.salary as salary


class SqliteConn(Singleton, ABC):
    db_path: str = None
    schema: DeclarativeMeta = None

    def __init__(self):
        if self.db_path is None:
            raise ValueError(
                "Database path must be set before creating a connection.")

        self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def fetchTableData(
        self,
        start: int = None,
        end: int = None
    ) -> List[Dict[str, Any]]:
        with self.Session() as session:
            query = session.query(self.schema)

            if start is not None and end is not None:
                query = query.offset(start).limit(end - start)

            rows = query.all()
            columns = self.schema.__table__.columns.keys()
            data = [
                dict(
                    zip(columns, [getattr(row, col)for col in columns])
                ) for row in rows
            ]

        return data

    def fetchTableSize(
        self,
    ) -> int:
        with self.Session() as session:
            size = session.query(self.schema).count()
        return size

    def fetchTableHeaders(
        self,
    ) -> List[str]:
        return [col.name for col in self.schema.__table__.columns]

    def __del__(self):
        self.engine.dispose()


class SalaryDatabase(SqliteConn):
    db_path = salary.DB_LOC
    schema = salary.Salary


class UsCitiesDatabase(SqliteConn):
    db_path = uscities.DB_LOC
    schema = uscities.UsCities

    def FetchStringMatchedData(self, query: str) -> List[Dict[str, str]]:
        with self.Session() as session:
            query = query.strip()
            if query:
                stmt = session.query(self.schema).filter(
                    self.schema.city.like(f"%{query}%")).limit(50)
            else:
                stmt = session.query(self.schema).limit(50)

            results = stmt.all()

        return [
            {
                "city": row.city,
                "state_id": row.state_id
            } for row in results
        ]
