import logging.config
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers.pinecone_router import pinecone_router

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "logging.conf")
logging.config.fileConfig(config_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

description = """
## 🌺 This document is an API docs for the CustomGPT backend system for classifying Hibiscus syriacus
---
## 📌 API List
### Pinecone
* **CRUD items**
"""


def create_app() -> FastAPI:
    fast_api_app = FastAPI(
        title="Hibiscus syriacus Explorer backend API",
        description=description,
        version="0.1.0",
        servers=[
            {
                "url": "https://hibiscussyriacusexplorer.store",
            }
        ],
    )

    # CORS 미들웨어 설정

    fast_api_app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
            # config.LOCAL_DOMAIN,  # LOCAL_DOMAIN = "http://localhost:3000"
            # config.DEV_DOMAIN,  # DEV_DOMAIN = "http://43.200.107.196"
        ],
        allow_credentials=True,
        allow_methods=["*"],  # 모든 HTTP 메소드 허용.
        allow_headers=["*"],  # 모든 HTTP 헤더 허용.
    )

    fast_api_app.include_router(pinecone_router, prefix="/pinecone")

    return fast_api_app


app = create_app()
