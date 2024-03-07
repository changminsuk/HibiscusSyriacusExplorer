import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

from src.utils import config


class PineconeRepository:
    @staticmethod
    async def create_record(index: str, title: str, description: str):
        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT,
        )

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder()
        docs = [
            Document(page_content=x, metadata={"title": title})
            for x in splitter.split_text(description)
        ]

        embeddings = OpenAIEmbeddings()

        vector_store = Pinecone.from_documents(docs, embeddings, index_name=index)

        return {"result": f"{title} created successfully!"}

    @staticmethod
    async def query_pinecone(param: dict):
        split_string = param["characteristics"].split(",")
        characteristics = [s.replace("+", " ").strip() for s in split_string]

        print("characteristics from chatGPT:", characteristics)

        # TODO: pinecone query logic

        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT,
        )

        return {"result": "블루 쉬폰"}
