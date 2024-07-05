from typing import List, Dict
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, MetaData
from dataclasses import dataclass, asdict, fields
from sqlalchemy.orm import sessionmaker


from app.common.singleton import Singleton
import app.database.salary as salary
import app.database.uscities as uscities


class SqliteConn(Singleton, ABC):
    @abstractmethod
    def __imports__(self):
        pass

    def __init__(self):
        self.__imports__()
        if self.db_path is None:
            raise ValueError(
                "Database path must be set before creating a connection."
            )

        self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def __del__(self):
        self.engine.dispose()


class SalaryDatabase(SqliteConn):

    @dataclass(slots=True)
    class CoopSalaryTable:
        id: int
        company: str
        position: str
        salary: float
        hours: int
        experience: int
        year: int

    def __imports__(self):
        self.db_path = salary.DB_LOC

    def fetchTableData(
        self,
        start: int = None,
        end: int = None
    ) -> List[Dict]:
        with self.Session() as session:
            query = session.query(
                salary.CoopSalary.id,
                salary.Company.name.label('company'),
                salary.Position.title.label('position'),
                salary.CoopSalary.salary_per_hour.label('salary'),
                salary.CoopSalary.hours_per_week.label('hours'),
                salary.CoopSalary.experience,
                salary.CoopSalary.year
            ).join(
                salary.CompaniesPositions,
                salary.CoopSalary.company_position_id == salary.CompaniesPositions.id
            ).join(
                salary.Company,
                salary.CompaniesPositions.company_id == salary.Company.id
            ).join(
                salary.Position,
                salary.CompaniesPositions.position_id == salary.Position.id
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
            size = session.query(salary.CoopSalary).count()
        return size

    def fetchTableHeaders(
        self,
    ) -> List[str]:

        return [
            field.name.capitalize() for field in fields(self.CoopSalaryTable)
        ]


class UsCitiesDatabase(SqliteConn):

    def __imports__(self):
        self.db_path = uscities.DB_LOC
        self.schema = uscities.UsCities

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


if __name__ == "__main__":
    sal = SalaryDatabase()
    print(sal.fetchTableSize())
    print(sal.fetchTableData(0, 10))
