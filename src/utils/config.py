import os
from enum import Enum

from dotenv import load_dotenv

"""
ENVIRONMENT KEYWORD
"""
ENV = "dev"
load_dotenv(dotenv_path=f".{ENV}.env")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS"))

"""
DOMAIN KEYWORD
"""
LOCAL_DOMAIN = "http://localhost:3000"
DEV_DOMAIN = "http://43.200.107.196"

"""
TOKEN KEYWORD
"""


class APIKeyHeader(Enum):
    USER = "Bearer"
    ADMIN = "Admin"
