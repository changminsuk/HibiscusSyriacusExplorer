from src.dtos.base_dto import BaseModel


class CreateRecordRequestDto(BaseModel):
    index: str = "classify"
    title: str = "청단심계 | 홑꽃-신청조"
    description: str = "연한 푸른색의 꽃잎이 약간 겹치는 청단심계 홑꽃이다."


class QueryPineconeRequestDto(BaseModel):
    characteristics: str
