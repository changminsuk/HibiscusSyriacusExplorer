import logging
from http import HTTPStatus
from typing import List

import pandas as pd
from fastapi import HTTPException

from src.dtos.pinecone_dto import CreateRecordRequestDto, CreateArrangeRecordRequestDto
from src.repositories.pinecone_repository import PineconeRepository

logger = logging.getLogger(__name__)


class PineconeService:
    @staticmethod
    async def create_record(create_record_request_dto: CreateRecordRequestDto):
        """
        create a record in the index of pinecone project.
        from. POST /pinecone/createRecord API
        ---
        @param create_record_request_dto: {index: str, title: str, description: str, column: str}
        """
        index: str = create_record_request_dto.index
        title: str = create_record_request_dto.title
        description: str = create_record_request_dto.description
        column: str = create_record_request_dto.column

        # check if the title already exists in the index of pinecone project.
        # records_with_index_title = (
        #     await PineconeRepository.get_records_by_title_of_metadata(
        #         index=index, title=title
        #     )
        # )
        #
        # # if this title already exists in the index, raise an exception.
        # if records_with_index_title:
        #     exception_status = HTTPStatus.CONFLICT
        #     raise HTTPException(
        #         status_code=exception_status.value,
        #         detail=f"{exception_status.phrase}: {column}/{title} in {index} index is already exists.",
        #     )

        # check if the index exists in the pinecone project before creating a record.
        indexes = PineconeRepository.get_indexes()
        if index not in indexes:
            exception_status = HTTPStatus.NOT_FOUND
            raise HTTPException(
                status_code=exception_status.value, detail=exception_status.phrase
            )

        # create a record in the index of pinecone project.
        result = await PineconeRepository.create_record(
            index=index, description=description,
            metadata={
                "title": title,
                "column": column
            }
        )

        return result

    @staticmethod
    async def create_records(records: List[CreateRecordRequestDto]):

        # check if the index exists in the pinecone project before creating a record.
        indexes = PineconeRepository.get_indexes()
        if records[0].index not in indexes:
            exception_status = HTTPStatus.NOT_FOUND
            raise HTTPException(
                status_code=exception_status.value, detail=exception_status.phrase
            )

        # create a record in the index of pinecone project.
        result = await PineconeRepository.create_records(records=records)

        return result

    @staticmethod
    async def create_arrange_records(records: List[CreateArrangeRecordRequestDto]):

        # check if the index exists in the pinecone project before creating a record.
        indexes = PineconeRepository.get_indexes()
        if records[0].index not in indexes:
            exception_status = HTTPStatus.NOT_FOUND
            raise HTTPException(
                status_code=exception_status.value, detail=exception_status.phrase
            )

        # create a record in the index of pinecone project.
        result = await PineconeRepository.create_arrange_records(records=records)

        return result

    @staticmethod
    async def upload_excel_to_pinecone(file_path: str, index: str):
        try:
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                title = row['Title']  # assuming the excel file has a column named 'Title'
                description = row['Description']  # assuming the excel file has a column named 'Description'
                create_record_request_dto = CreateRecordRequestDto(
                    index=index,
                    title=title,
                    description=description
                )
                await PineconeService.create_record(create_record_request_dto)
            return {"result": "Excel data loaded successfully into Pinecone"}
        except Exception as e:
            logger.error(f"Error loading Excel data to Pinecone: {str(e)}")
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                detail=str(e)
            )

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

        # 각 수종 별 score 를 취합하고, score 가 높은 순으로 정렬한다.
        formatted_result = PineconeService.refactor_data(result)

        return formatted_result

    @staticmethod
    def refactor_data(result):
        # title 별로 score 를 취합한다. 이 때, 어느 colmn 에서 얼마의 score 를 받았는지도 함께 반환한다.
        formatted_result = {}
        for item in result.values():
            for data in item['matches']:
                title = data['metadata']['title']
                column = data['metadata']['column']
                score = data['score']

                # title 정보가 없으면 추가
                if title not in formatted_result:
                    formatted_result[title] = {
                        "totalScore": 0,
                        "details": {}
                    }

                formatted_result[title]["totalScore"] += score
                formatted_result[title]["details"][column] = score

        # totalScore 가 높은 순으로 정렬
        formatted_result = dict(sorted(formatted_result.items(), key=lambda x: x[1]["totalScore"], reverse=True))

        # 각 title 별로 details 를 score 가 높은 순으로 정렬한다.
        for title in formatted_result.keys():
            formatted_result[title]["details"] = dict(sorted(formatted_result[title]["details"].items(), key=lambda x: x[1], reverse=True))

        return formatted_result

    @staticmethod
    async def query_with_title(title: str):
        """
        get records by title of metadata in the index of pinecone project.
        from. GET /pinecone/queryWithTitle API
        ---
        @param title: str
        """
        result = await PineconeRepository.query_with_title(title=title)

        return result

    @staticmethod
    async def delete_column(column: str):
        """
        delete a column in the index of pinecone project.
        from. DELETE /pinecone/deleteColumn API
        ---
        @param column: str
        """
        result = await PineconeRepository.delete_column(column=column)

        return result
