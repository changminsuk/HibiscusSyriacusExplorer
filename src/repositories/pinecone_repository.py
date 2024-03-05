class PineconeRepository:

    @staticmethod
    async def query_pinecone(param: dict):
        split_string = param["characteristics"].split(",")
        characteristics = [s.replace('+', ' ').strip() for s in split_string]

        print('characteristics from chatGPT:', characteristics)

        # TODO: pinecone query logic
        return {"result": "블루 쉬폰"}
