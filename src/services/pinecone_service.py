import logging
from http import HTTPStatus

from fastapi import HTTPException

from src.dtos.pinecone_dto import CreateRecordRequestDto
from src.repositories.pinecone_repository import PineconeRepository

logger = logging.getLogger(__name__)


class PineconeService:
    @staticmethod
    async def create_record(create_record_request_dto: CreateRecordRequestDto):
        """
        create a record in the index of pinecone project.
        from. POST /pinecone/createRecord API
        ---
        @param create_record_request_dto: {index: str, title: str, description: str}
        """
        index = create_record_request_dto.index
        title = create_record_request_dto.title
        description = create_record_request_dto.description

        # check if the title already exists in the index of pinecone project.
        records_with_index_title = (
            await PineconeRepository.get_records_by_title_of_metadata(
                index=index, title=title
            )
        )

        # if this title already exists in the index, raise an exception.
        if records_with_index_title:
            exception_status = HTTPStatus.CONFLICT
            raise HTTPException(
                status_code=exception_status.value,
                detail=f"{exception_status.phrase}: {title} in {index} index is already exists.",
            )

        # check if the index exists in the pinecone project before creating a record.
        indexes = await PineconeRepository.get_indexes()
        if index not in indexes:
            exception_status = HTTPStatus.NOT_FOUND
            raise HTTPException(
                status_code=exception_status.value, detail=exception_status.phrase
            )

        # create a record in the index of pinecone project.
        result = await PineconeRepository.create_record(
            index=index, title=title, description=description
        )

        return result

    @staticmethod
    async def query_pinecone(param: dict):
        """
        query pinecone with the given parameters.
        from. GET /pinecone/queryPinecone API
        ---
        @param param: {characteristics: str}
        """
        result = await PineconeRepository.query_pinecone(param=param)

        if not result:
            exception_status = HTTPStatus.NOT_FOUND
            raise HTTPException(
                status_code=exception_status.value, detail=exception_status.phrase
            )

        return result
