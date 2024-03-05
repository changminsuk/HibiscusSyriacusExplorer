from src.dtos.base_dto import BaseModel


class QueryPineconeRequestDto(BaseModel):
    characteristics: str
