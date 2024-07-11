from pathlib import Path
from typing import List, Dict
from app.database.connection import Connection
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    String,
    Integer,
)


DB_LOC = Path(__file__).resolve().parent / 'database.db'


class UsCities(declarative_base()):
    __tablename__ = 'uscities'

    id = Column(Integer, nullable=True,primary_key=True, autoincrement=True)
    city = Column(String, nullable=True)
    state_id = Column(String, nullable=True)


class UsCitiesDatabase(Connection):

    def __imports__(self):
        self.db_path = DB_LOC

    def FetchStringMatchedData(self, query: str) -> List[Dict[str, str]]:

        with self.Session() as session:
            query = query.strip()
            if query:
                stmt = session.query(UsCities).filter(UsCities.city.like(f"%{query}%")).limit(50)
            else:
                stmt = session.query(UsCities).limit(50)

            results = stmt.all()

        return [
            {
                "city": row.city,
                "state_id": row.state_id
            } for row in results
        ]
