from fastapi import APIRouter, Depends

from src.dtos.base_dto import ResponseDto
from src.dtos.pinecone_dto import *
from src.services.pinecone_service import PineconeService

pinecone_router = APIRouter(
    tags=["Pinecone"],
)


@pinecone_router.get(
    "/queryPinecone",
    response_model=ResponseDto,
    summary="Upon receiving a GET request this endpoint will return species that are similar to the input image.",
    response_description="The species that are similar to the input image.",
)
async def query_pinecone(
    query_params: QueryPineconeRequestDto = Depends(),
) -> ResponseDto:
    """
    ## After extracting the characteristics of the input image,<br>CustomGPT executes a similarity search in the Pinecone DB.
    ---
    - **characteristics** (required) : the list of characteristics of the image
    """

    result = await PineconeService.query_pinecone(query_params.dict())

    return ResponseDto(success=True, message="Send email success", data=result)
