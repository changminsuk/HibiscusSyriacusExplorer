from typing import Optional, Union

from pydantic import BaseModel, Field


class ResponseDto(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)

    success: bool = Field(description="Response status")
    message: str = Field(description="Response message")
    data: Optional[Union[str, dict]] = Field(description="Response data", default=None)


class TokenEntity(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)

    token_type: str
    payload: dict
