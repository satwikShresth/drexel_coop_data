from pathlib import Path
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

DB_LOC = Path(__file__).resolve().parent / 'database.db'


class UsCities(declarative_base()):
    __tablename__ = 'uscities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=True)
    state_id = Column(String, nullable=True)
