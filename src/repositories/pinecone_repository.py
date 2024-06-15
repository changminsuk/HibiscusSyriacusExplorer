import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from http import HTTPStatus

import pinecone
from fastapi import HTTPException
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.utils import config


def process_param(key, value, index):
    korean_key = config.Columns[key].value

    if not value:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail=f"Missing parameter: {korean_key}",
        )

    embeddings = OpenAIEmbeddings()
    vector = embeddings.embed_query(str(value))

    result = index.query(
        vector=vector,
        top_k=5,
        include_metadata=True,
        filter={
            "column": {"$eq": korean_key},
        }
    )

    if not result["matches"]:
        return korean_key, None

    serializable_result = {
        "matches": [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in result["matches"]
        ]
    }

    return korean_key, serializable_result


class PineconeRepository:
    pinecone.init(
        api_key=config.PINECONE_API_KEY,
        environment=config.PINECONE_ENVIRONMENT,
    )

    @staticmethod
    async def create_record(index: str, description: str, metadata: dict):
        """
        create a record in the index of pinecone project.
        ---
        @param index: the name of the index (in this project, it is "classify". Because our pinecone project has only one index that is "classify")
        @param description: the description of the record
        @param metadata: the metadata of the record
        """
        try:
            splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder()
            docs = [
                Document(page_content=x, metadata=metadata)
                for x in splitter.split_text(description)
            ]

            embeddings = OpenAIEmbeddings()
            vectors = embeddings.embed_documents([doc.page_content for doc in docs])

            # Create a list of dictionaries with id, values (embeddings), and metadata
            pinecone_vectors = [
                {"id": str(uuid.uuid4()), "values": vector, "metadata": doc.metadata}
                for vector, doc in zip(vectors, docs)
            ]

            index = pinecone.Index(index)
            index.upsert(vectors=pinecone_vectors)

            # splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder()
            # docs = [
            #     Document(page_content=x, metadata={"title": title})
            #     for x in splitter.split_text(description)
            # ]
            #
            # embeddings = OpenAIEmbeddings()
            #
            # Pinecone.from_documents(docs, embeddings, index_name=index)

            return {"result": f"{metadata['title']} created successfully!"}
        except Exception as e:
            print(1, e)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(e)
            )

    @staticmethod
    def get_indexes():
        """
        get indexes from pinecone.
        """
        try:
            return pinecone.list_indexes()
        except Exception as e:
            print(2, e)
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
            index = pinecone.Index("classify")
            serializable_result_map = {}

            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(process_param, key, value, index)
                    for key, value in param.items()
                ]

                for future in as_completed(futures):
                    korean_key, result = future.result()
                    if result is not None:
                        serializable_result_map[korean_key] = result

            return serializable_result_map

        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(e)
            )
