from typing import Any

from pydantic import BaseModel, Field


class ResponseDto(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)

    success: bool = Field(description="Response status")
    message: str = Field(description="Response message")
    # data: Optional[Union[str, dict]] = Field(description="Response data", default=None)
    data: Any = Field(description="Response data", default=None)


class DetailsDto(BaseModel):
    value: float = Field(description="The similarity score for a specific attribute")

    class Config:
        schema_extra = {
            "example": {
                "톱니": 1.00587869,
                "결각": 1.00144482,
            }
        }


class SpeciesDto(BaseModel):
    totalScore: float = Field(description="The total similarity score for the species")
    details: dict[str, DetailsDto] = Field(description="Detailed similarity scores for specific attributes")

    class Config:
        schema_extra = {
            "example": {
                "totalScore": 2.00732351,
                "details": {
                    "톱니": {"value": 1.00587869},
                    "결각": {"value": 1.00144482}
                }
            }
        }


class GPTQueryResponseDataDto(BaseModel):
    species: dict[str, SpeciesDto] = Field(description="Mapping of species names to their similarity scores")

    class Config:
        schema_extra = {
            "example": {
                "찰피나무": {
                    "totalScore": 2.00732351,
                    "details": {
                        "톱니": {"value": 1.00587869},
                        "결각": {"value": 1.00144482}
                    }
                },
                "잣나무": {
                    "totalScore": 1.8713784809999998,
                    "details": {
                        "잎차례": {"value": 1.0039922},
                        "잎길이": {"value": 0.867386281}
                    }
                }
            }
        }


class GPTQueryResponseDto(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)

    success: bool = Field(description="Response status")
    message: str = Field(description="Response message")
    data: GPTQueryResponseDataDto = Field(description="Response data", default=None)

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Succeeded in inferring the species that are similar to the input image.",
                "data": {
                    "찰피나무": {
                        "totalScore": 2.00732351,
                        "details": {
                            "톱니": {"value": 1.00587869},
                            "결각": {"value": 1.00144482}
                        }
                    },
                    "잣나무": {
                        "totalScore": 1.8713784809999998,
                        "details": {
                            "잎차례": {"value": 1.0039922},
                            "잎길이": {"value": 0.867386281}
                        }
                    }
                }
            }
        }


class TokenEntity(BaseModel):
    def __init__(self, **data):
        super().__init__(**data)

    token_type: str
    payload: dict
