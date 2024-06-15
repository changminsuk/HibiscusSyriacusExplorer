from fastapi import APIRouter, Body, Depends

from src.dtos.base_dto import ResponseDto
from src.dtos.pinecone_dto import *
from src.services.pinecone_service import PineconeService

pinecone_router = APIRouter(
    tags=["Pinecone"],
)


@pinecone_router.post(
    "/createRecord",
    response_model=ResponseDto,
    summary="Create a record in the classify Index of HibiscusGPT project.",
    response_description="The record has been created successfully.",
)
async def create_record(
        request_body: CreateRecordRequestDto = Body(...),
) -> ResponseDto:
    """
    ## Create a record in the classify Index of HibiscusGPT project.
    ---
    - **request_body** (required) : the record to be created
    """

    result = await PineconeService.create_record(request_body)

    return ResponseDto(
        success=True,
        message="Succeeded in creating a record in the classify Index of HibiscusGPT project.",
        data=result,
    )


@pinecone_router.get(
    "/queryPinecone",
    response_model=ResponseDto,
    summary="Upon receiving a GET request this endpoint will return species that are similar to the input image."
            "leaflet_count : -1 ~ 25, leaf_length : -1 ~ 50, leaf_width : -1 ~ 30",
    response_description="The species that are similar to the input image.",
)
async def query_pinecone(
        query_params: QueryPineconeRequestDto = Depends(),
) -> ResponseDto:
    """
    ## After extracting the characteristics of the input image,<br>CustomGPT executes a similarity search in the Pinecone DB.

    ## EVERY PARAMETER IS REQUIRED.
    """

    result = await PineconeService.query_pinecone(query_params.dict())

    return ResponseDto(
        success=True,
        message="Succeeded in inferring the species that are similar to the input image.",
        data=result,
    )
