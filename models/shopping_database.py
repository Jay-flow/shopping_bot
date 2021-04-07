from config import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ShoppingDatabase(Database):
    name = "shopping"

    @property
    def connect(self):
        return create_engine(
            f"mysql://{self.USER_NAME}:{self.PASSWORD}@{self.HOST}/{self.name}?charset=utf8mb4",
            echo=True
        )

    @property
    def session(self):
        if self._session is None:
            connect = create_engine(
                f"mysql://{self.USER_NAME}:{self.PASSWORD}@{self.HOST}/{self.name}?charset=utf8mb4",
                echo=True
            )
            self._session = sessionmaker(bind=connect)()
            return self._session
        return self._session
