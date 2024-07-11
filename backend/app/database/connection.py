from abc import ABC, abstractmethod
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.common.singleton import Singleton


class Connection(Singleton, ABC):
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
