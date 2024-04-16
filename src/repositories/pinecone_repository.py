from http import HTTPStatus

import pinecone
from fastapi import HTTPException
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

from src.utils import config


class PineconeRepository:
    pinecone.init(
        api_key=config.PINECONE_API_KEY,
        environment=config.PINECONE_ENVIRONMENT,
    )

    @staticmethod
    async def create_record(index: str, title: str, description: str):
        """
        create a record in the index of pinecone project.
        ---
        @param index: the name of the index (in this project, it is "classify". Because our pinecone project has only one index that is "classify")
        @param title: the title of the record
        @param description: the description of the record
        """
        try:
            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder()
            docs = [
                Document(page_content=x, metadata={"title": title})
                for x in splitter.split_text(description)
            ]

            embeddings = OpenAIEmbeddings()

            Pinecone.from_documents(docs, embeddings, index_name=index)

            return {"result": f"{title} created successfully!"}
        except Exception as e:
            print(1, e)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(e)
            )

    @staticmethod
    async def get_indexes():
        """
        get indexes from pinecone.
        """
        try:
            return await pinecone.list_indexes()
        except Exception as e:
            print(2, e)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(e)
            )

    @staticmethod
    async def get_records_by_title_of_metadata(index: str, title: str):
        """
        get records from pinecone by title and index of metadata.
        ---
        @param index: the name of the index
        @param title: the title of the record
        """
        try:
            # create dummy vector for query that is 1536 dimension
            dummy_vector = [0.0] * 1536

            index = pinecone.Index(index)
            records = index.query(
                vector=dummy_vector,
                filter={
                    "title": {"$eq": title}
                },
                top_k=1,
                include_metadata=True
            )

            return records
        except Exception as e:
            print(3, e)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(e)
            )

    @staticmethod
    async def query_pinecone(param: dict):
        """
        query pinecone by characteristics.
        ---
        @param param: the characteristics of the image
        """
        try:
            split_string = param["characteristics"].split(",")
            characteristics = [s.replace("+", " ").strip() for s in split_string]

            print("characteristics from chatGPT:", characteristics)

            # TODO: pinecone query logic

            pinecone.init(
                api_key=config.PINECONE_API_KEY,
                environment=config.PINECONE_ENVIRONMENT,
            )

            index = pinecone.Index("classify")
            result = index.query(queries=characteristics, top_k=3)

            return {"result": "블루 쉬폰"}
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(e)
            )
