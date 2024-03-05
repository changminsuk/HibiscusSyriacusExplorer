import logging
from http import HTTPStatus

from fastapi import HTTPException

from src.repositories.pinecone_repository import PineconeRepository

logger = logging.getLogger(__name__)


class PineconeService:

    @staticmethod
    async def query_pinecone(param: dict):
        result = await PineconeRepository.query_pinecone(param=param)

        if not result:
            exception_status = HTTPStatus.NOT_FOUND
            raise HTTPException(
                status_code=exception_status.value, detail=exception_status.phrase
            )

        return result
