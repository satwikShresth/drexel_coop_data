from pathlib import Path
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, ForeignKey

DB_LOC = Path(__file__).resolve().parent / 'database.db'

class Company(declarative_base()):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    positions = relationship('Position', back_populates='company')


class Position(declarative_base()):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', back_populates='positions')
