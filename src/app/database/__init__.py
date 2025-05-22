# db/__init__.py
import logging

logger = logging.getLogger(__name__)

from src.app.config import base_settings
from .config import DatabaseConfig

# Initialize configurations
db_config = DatabaseConfig(base_settings)

# Export commonly used items
Base = db_config.Base
MasterSession = db_config.MasterSession
MasterAsyncSession = db_config.MasterAsyncSession

# test engines
# test_engine = db_config.test_engine
# TestSession = db_config.TestSession

logger.info("Database is Ready!")
