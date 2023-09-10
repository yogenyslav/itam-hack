from time import sleep
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError as sqlalchemyOpError
from psycopg2 import OperationalError as psycopg2OpError
from logging import Logger
from . import Base
from src.utils.settings import settings
from src.utils.logging import get_logger


class SQLManager:
    instance = None

    def __init__(
        self, log: Logger = get_logger("__sql_manager__"), local: bool = False
    ):
        if local:
            self.pg_user = "pguser"
            self.pg_pass = "pgpassword"
            self.pg_host = "localhost"
            self.pg_port = 5432
            self.pg_db = "dev"
        else:
            self.pg_user = settings.postgres_user
            self.pg_pass = settings.postgres_password
            self.pg_host = settings.postgres_host
            self.pg_port = settings.postgres_port
            self.pg_db = settings.postgres_db
        self.log = log
        connected = False
        while not connected:
            try:
                self._connect()
            except (sqlalchemyOpError, psycopg2OpError):
                self.log.warning("Database connection failed, retrying...")
                sleep(2)
            else:
                connected = True
        self._update_db()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(SQLManager, cls).__new__(cls)
        return cls.instance

    def __del__(self):
        """Close the database connection when the object is destroyed"""
        self._close()

    def _connect(self) -> None:
        """Connect to the postgresql database"""
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.pg_user}:{self.pg_pass}@{self.pg_host}:{self.pg_port}\
/{self.pg_db}",
            pool_pre_ping=True,
        )
        Base.metadata.bind = self.engine
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def _close(self) -> None:
        """Closes the database connection"""
        self.session.close_all()

    def _update_db(self) -> None:
        """Create the database structure if it doesn't exist (update)"""
        # Create the tables if they don't exist
        Base.metadata.create_all(self.engine)
