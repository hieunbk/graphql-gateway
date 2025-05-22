from typing import Dict, Optional

from pydantic import Json
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettings(BaseSettings):
    """
    Base settings class. This class is used to load the settings from environment variables.
    """
    # core
    debug: bool
    environment: str
    allow_origins: list[str] = ["*"]
    # database
    db_name: str
    db_username: str
    db_password: str
    db_host: str
    db_port: int

    # cache
    # redis_url: str

    # guvicorn run
    workers: int = 3
    timeout_worker: int = 120
    loglevel: str = "info"



base_settings = BaseSettings()