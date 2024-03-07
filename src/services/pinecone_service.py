import logging
from http import HTTPStatus

from fastapi import HTTPException

from src.dtos.pinecone_dto import CreateRecordRequestDto
from src.repositories.pinecone_repository import PineconeRepository

logger = logging.getLogger(__name__)


class PineconeService:
    @staticmethod
    async def create_record(create_record_request_dto: CreateRecordRequestDto):
        index = create_record_request_dto.index
        title = create_record_request_dto.title
        description = create_record_request_dto.description
        result = await PineconeRepository.create_record(
            index=index, title=title, description=description
        )

        return result

    @staticmethod
    async def query_pinecone(param: dict):
        result = await PineconeRepository.query_pinecone(param=param)

        if not result:
            exception_status = HTTPStatus.NOT_FOUND
            raise HTTPException(
                status_code=exception_status.value, detail=exception_status.phrase
            )

        return result
