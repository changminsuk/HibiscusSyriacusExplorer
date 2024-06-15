from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Body, Depends, UploadFile, File, HTTPException

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


@pinecone_router.post(
    "/createRecordsWithExcelSerration",
    response_model=ResponseDto,
    summary="Create Serration records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_serration(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '결각' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            description = row['결각']

            if pd.notna(title) and pd.notna(description):
                descriptionList = str(description).split(' ')
                koreanDiscriptionList = []
                for i in descriptionList:
                    koreanDiscriptionList.append(list(BasicTypeEnum)[int(i) - 1].value)
                koreanDescription = ','.join(koreanDiscriptionList)
                records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="결각"))

        print(records)

        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            # data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelShape",
    response_model=ResponseDto,
    summary="Create Shape records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_shape(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '생김새' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            description = row['생김새']

            if pd.notna(title) and pd.notna(description):
                descriptionList = str(description).split(' ')
                koreanDiscriptionList = []
                for i in descriptionList:
                    koreanDiscriptionList.append(list(ShapeEnum)[int(i) - 1].value)
                koreanDescription = ','.join(koreanDiscriptionList)
                records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="생김새"))

        print(records)

        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            # data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@pinecone_router.get(
    "/queryWithTitle",
    response_model=ResponseDto,
    summary="Upon receiving a GET request this endpoint will return species that are similar to the input title.",
    response_description="The species that are similar to the input title.",
)
async def query_with_title(
        query_params: QueryWithTitleRequestDto = Depends(),
) -> ResponseDto:
    """
    ## After extracting the characteristics of the input title,<br>CustomGPT executes a similarity search in the Pinecone DB.

    ## EVERY PARAMETER IS REQUIRED.
    """

    result = await PineconeService.query_with_title(query_params.dict()["title"])

    return ResponseDto(
        success=True,
        message="Succeeded in inferring the species that are similar to the input title.",
        data=result,
    )


@pinecone_router.delete(
    "/deleteColumn",
    response_model=ResponseDto,
    summary="Delete the index in the Pinecone project.",
    response_description="The index has been deleted successfully.",
)
async def delete_column(
        request_body: DeleteColumnRequestDto = Body(...),
) -> ResponseDto:
    """
    ## Delete the index in the Pinecone project.
    ---
    - **request_body** (required) : the index to be deleted
    """

    result = await PineconeService.delete_column(request_body.column)

    return ResponseDto(
        success=True,
        message="Succeeded in deleting the index in the Pinecone project.",
        data=result,
    )
