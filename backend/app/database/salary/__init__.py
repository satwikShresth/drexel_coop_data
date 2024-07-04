from pathlib import Path
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, INTEGER

DB_LOC = Path(__file__).resolve().parent / 'database.db'


class Salary(declarative_base()):
    __tablename__ = 'salary'

    Company = Column(String, primary_key=True, nullable=True)
    Position = Column(String, primary_key=True, nullable=True)
    Salary = Column(String, nullable=True)
    Hours = Column(INTEGER, nullable=True)
    Year = Column(INTEGER, nullable=True)
    Major = Column(String, nullable=True)
    Cycle = Column(String, nullable=True)
    Experience = Column(INTEGER, nullable=True)
