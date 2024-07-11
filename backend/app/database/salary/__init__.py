from pathlib import Path
from typing import List, Dict
from app.database.connection import Connection
from sqlalchemy.orm import declarative_base
import locale
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Float,
    UniqueConstraint,
)

from dataclasses import (
    dataclass,
    asdict,
    fields
)

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
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


class SalaryDatabase(Connection):

    @dataclass(slots=True)
    class CoopSalaryTable:
        id: int
        company: str
        position: str
        salary: float | str
        hours: int
        experience: int | str
        year: int

        def __post_init__(self):
            self.salary = locale.currency(self.salary, grouping=True)
            self.experience = self.intToOrdinal(self.experience)

        def intToOrdinal(self, n: int) -> str:
            """
            Convert an integer to its ordinal representation.

            :param n: Integer to convert.
            :return: Ordinal string representation of the integer.
            """
            if 10 <= n % 100 <= 20:
                suffix = 'th'
            else:
                suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
            return f"{n}{suffix}"

    def __imports__(self):
        self.db_path = DB_LOC

    def fetchTableData(
        self,
        start: int = None,
        end: int = None
    ) -> List[Dict]:
        with self.Session() as session:
            query = session.query(
                CoopSalary.id,
                Company.name.label('company'),
                Position.title.label('position'),
                CoopSalary.salary_per_hour.label('salary'),
                CoopSalary.hours_per_week.label('hours'),
                CoopSalary.experience,
                CoopSalary.year
            ).join(
                CompaniesPositions,
                CoopSalary.company_position_id == CompaniesPositions.id
            ).join(
                Company,
                CompaniesPositions.company_id == Company.id
            ).join(
                Position,
                CompaniesPositions.position_id == Position.id
            )

            if start is not None:
                query = query.offset(start)

            if end is not None:
                query = query.limit(end-start)

            results = query.all()

        return [
            asdict(
                self.CoopSalaryTable(*row)
            ) for row in results
        ]

    def fetchTableSize(
        self,
    ) -> int:

        with self.Session() as session:
            size = session.query(CoopSalary).count()
        return size

    def fetchTableHeaders(
        self,
    ) -> List[str]:

        return [
            field.name.capitalize() for field in fields(self.CoopSalaryTable)
        ]

    def FetchStringMatchedData(
        self,
        query: str
    ) -> List[Dict[str, str]]:

        with self.Session() as session:
            query = query.strip()
            if query:
                stmt = session.query(Company).filter(
                    Company.name.like(f"%{query}%")).limit(50)
            else:
                stmt = session.query(Company).limit(50)

            results = stmt.all()

        return [row.name for row in results]
