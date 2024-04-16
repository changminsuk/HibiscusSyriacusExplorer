import os
from enum import Enum

from dotenv import load_dotenv

"""
ENVIRONMENT KEYWORD
"""
ENV = "dev"
load_dotenv(dotenv_path=f".{ENV}.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

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
