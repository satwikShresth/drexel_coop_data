from pathlib import Path
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import declarative_base

DB_LOC = Path(__file__).resolve().parent / 'database.db'

Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)


class Major(Base):
    __tablename__ = 'majors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class CoopCycle(Base):
    __tablename__ = 'coop_cycles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class CoopSalary(Base):
    __tablename__ = 'coop_salaries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_position_id = Column(
        Integer,
        ForeignKey('companies_positions.id'),
        nullable=False
    )

    cycle_id = Column(
        Integer,
        ForeignKey('coop_cycles.id'),
        nullable=False
    )
    salary_per_hour = Column(Float, nullable=False)
    hours_per_week = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


class CompaniesPositions(Base):
    __tablename__ = 'companies_positions'
    __table_args__ = (
        UniqueConstraint(
            'company_id',
            'position_id',
            name='_company_position_uc'
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
