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


class Columns(Enum):
    # 결각, 생김새, 소엽갯수, 잎길이, 잎끝, 잎너비, 잎뒷면털, 잎몸, 잎밑, 잎앞면털, 잎차례, 톱니
    serration = "결각"
    shape = "생김새"
    leaflet_count = "소엽갯수"
    leaf_length = "잎길이"
    leaf_tip = "잎끝"
    leaf_width = "잎너비"
    leaf_underside_hair = "잎뒷면털"
    leaf_blade = "잎몸"
    leaf_base = "잎밑"
    leaf_topside_hair = "잎앞면털"
    leaf_arrangement = "잎차례"
    tooth = "톱니"
