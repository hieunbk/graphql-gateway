import logging
from typing import List

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool, StaticPool
from src.app.config import base_settings

logger = logging.getLogger(__name__)


class DatabaseConfig:
    POSTGRES_INDEXES_NAMING_CONVENTION = {
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }

    def __init__(self, settings):
        self.settings = settings
        self.metadata = MetaData(naming_convention=self.POSTGRES_INDEXES_NAMING_CONVENTION)
        self.Base = declarative_base(metadata=self.metadata)

        # Initialize engines and sessions
        self.master_engine = self._create_master_engine()
        self.replica_engines = self._create_replica_engines()
        self.MasterSession = self._create_master_session()


        # Initialize test engines
        self.test_engine = self._create_test_engine()
        self.replica_test_engines = self._create_test_replica_engines()
        self.TestSession = self._create_test_session()

        # Initialize async engines and sessions
        self.master_async_engine = self._create_master_async_engine()
        self.MasterAsyncSession = self._create_master_async_session()

    @property
    def DATABASE_URL_FORMAT(self) -> str:
        return "postgresql+psycopg2://{username}:{password}@{address}/{db_name}"

    def _create_database_url(self, address: str) -> str:
        return self.DATABASE_URL_FORMAT.format(
            username=self.settings.db_username,
            password=self.settings.db_password,
            address=address,
            db_name=self.settings.db_name,
        )

    def _create_engine(self, url: str) -> Engine:
        return create_engine(
            url,
            poolclass=QueuePool,
            pool_size=3,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            connect_args={"options": f"-c timezone={base_settings.tz}"}
        )

    def _create_master_engine(self) -> Engine:
        url = self._create_database_url(self.settings.db_address)
        return self._create_engine(url)

    def _create_replica_engines(self) -> List[Engine]:
        return [
            self._create_engine(self._create_database_url(address))
            for address in self.settings.db_address_replica
        ]

    def _create_master_session(self) -> sessionmaker:
        return sessionmaker(autocommit=False, autoflush=False, bind=self.master_engine)

    def _create_test_engine(self) -> Engine:
        url = self._create_database_url(self.settings.db_address) + "-test"
        return create_engine(url, poolclass=StaticPool)

    def _create_test_replica_engines(self) -> List[Engine]:
        return [
            self._create_engine(self._create_database_url(address) + "-test")
            for address in self.settings.db_address_replica
        ]

    def _create_test_session(self) -> sessionmaker:
        return sessionmaker(autoflush=True, autocommit=False, bind=self.test_engine)


    def _create_master_async_engine(self) -> AsyncEngine:
        url = self._create_database_url(self.settings.db_address)
        return create_async_engine(
            url,
            echo=self.settings.debug,
            # poolclass=QueuePool,
            # pool_size=3,
            # max_overflow=2,
            # pool_timeout=30,
            # pool_recycle=1800,
            # pool_pre_ping=True,
            # connect_args={"options": f"-c timezone={base_settings.tz}"}
        )


    def _create_master_async_session(self):
        return sessionmaker(
            bind=self._create_master_async_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )