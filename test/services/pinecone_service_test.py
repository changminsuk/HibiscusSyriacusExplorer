import unittest
from unittest.mock import AsyncMock, patch

from src.services.pinecone_service import PineconeService


# unittest.TestCase를 상속받는 새로운 테스트 클래스를 생성합니다.
class TestPineconeService(unittest.IsolatedAsyncioTestCase):
    # query_pinecone 메소드가 비어있는 결과를 반환하는 경우를 테스트하는 메소드입니다.
    @patch(
        "src.services.pinecone_service.PineconeRepository.query_pinecone",
        new_callable=AsyncMock,
    )
    async def test_query_pinecone_empty_result(self, mock_query):
        # 테스트를 위해 query_pinecone 메소드를 모킹합니다. 이 메소드가 None을 반환하도록 설정합니다.
        mock_query.return_value = None
        param = {"characteristics": "test"}

        # query_pinecone 메소드가 예외를 발생시키는지 테스트합니다.
        with self.assertRaises(Exception):
            await PineconeService.query_pinecone(param=param)

    # query_pinecone 메소드가 비어있지 않은 결과를 반환하는 경우를 테스트하는 메소드입니다.
    @patch(
        "src.services.pinecone_service.PineconeRepository.query_pinecone",
        new_callable=AsyncMock,
    )
    async def test_query_pinecone_non_empty_result(self, mock_query):
        # 테스트를 위해 query_pinecone 메소드를 모킹합니다. 이 메소드가 비어있지 않은 결과를 반환하도록 설정합니다.
        mock_query.return_value = {"result": "블루 쉬폰"}
        param = {"characteristics": "test"}

        # query_pinecone 메소드를 호출하고 결과를 저장합니다.
        result = await PineconeService.query_pinecone(param=param)

        # 반환된 결과가 기대한 결과와 같은지 확인합니다.
        self.assertEqual(result, {"result": "블루 쉬폰"})
