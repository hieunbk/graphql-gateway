from datetime import timedelta, datetime
from typing import Dict, Any, Optional

from jose import jwt
from passlib.context import CryptContext

from src.app.database import MasterSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_master_session():
    """Get the write db session object"""
    db = MasterSession()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()



def hash_password(password: str) -> str:
    """Hash the password"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Verify the password"""
    return pwd_context.verify(plain_password, hashed_password)


