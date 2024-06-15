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
    ## Create Serration records from an Excel file in the classify Index of HibiscusGPT project.
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
            data=result,
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
    ## Create Shape records from an Excel file in the classify Index of HibiscusGPT project.
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

        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafletCount",
    response_model=ResponseDto,
    summary="Create Leaflet Count records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaflet_count(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaflet Count records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or 'MIN' not in df.columns or 'MAX' not in df.columns or '소엽갯수' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'MIN' columns and 'MAX' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            min = row['MIN']
            max = row['MAX']

            if pd.notna(title) and pd.notna(min) and pd.notna(max):
                records.append(CreateArrangeRecordRequestDto(index="classify", title=title, min=min, max=max, column="소엽갯수"))

        # Call the PineconeService to create records
        result = await PineconeService.create_arrange_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            # data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafLength",
    response_model=ResponseDto,
    summary="Create Leaf Length records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_length(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Length records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or 'MIN' not in df.columns or 'MAX' not in df.columns or '잎길이' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'MIN' columns and 'MAX' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            min = row['MIN']
            max = row['MAX']

            if pd.notna(title) and pd.notna(min) and pd.notna(max):
                records.append(CreateArrangeRecordRequestDto(index="classify", title=title, min=min, max=max, column="잎길이"))

        # Call the PineconeService to create records
        result = await PineconeService.create_arrange_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            # data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafTip",
    response_model=ResponseDto,
    summary="Create Leaf Tip records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_tip(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Tip records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '잎끝(엽선)' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []

        # 코드와 LeafTipEnum 매핑 테이블
        mappingTable = {
            "1": LeafTipEnum.cuspidate.value,
            "2": LeafTipEnum.acute.value,
            "3": LeafTipEnum.mucronate.value,
            "5": LeafTipEnum.obtuse.value,
            "6": LeafTipEnum.rounded.value,
            "7": LeafTipEnum.emarginate.value,
            "8": LeafTipEnum.truncate.value,
            "9": LeafTipEnum.acuminate.value,
        }

        for _, row in df.iterrows():
            title = row['수종']
            description = row['코드']

            if pd.notna(title) and pd.notna(description):
                descriptionList = str(description).split(' ')
                koreanDiscriptionList = []
                for i in descriptionList:
                    koreanDiscriptionList.append(mappingTable[i])
                koreanDescription = ','.join(koreanDiscriptionList)
                records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="잎끝"))

        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafWidth",
    response_model=ResponseDto,
    summary="Create Leaf Width records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_width(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Width records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or 'MIN' not in df.columns or 'MAX' not in df.columns or '잎너비' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'MIN' columns and 'MAX' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            min = row['MIN']
            max = row['MAX']

            if pd.notna(title) and pd.notna(min) and pd.notna(max):
                records.append(CreateArrangeRecordRequestDto(index="classify", title=title, min=min, max=max, column="잎너비"))

        # Call the PineconeService to create records
        result = await PineconeService.create_arrange_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            # data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafUndersideHair",
    response_model=ResponseDto,
    summary="Create Leaf Underside Hair records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_underside_hair(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Underside Hair records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '잎뒷면털' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            description = row['코드']

            if (pd.notna(title) and pd.notna(description)) is False:
                continue

            descriptionList = str(description).split(' ')
            koreanDiscriptionList = []
            for i in descriptionList:
                koreanDiscriptionList.append(list(BasicTypeEnum)[int(i) - 1].value)
            koreanDescription = ','.join(koreanDiscriptionList)
            records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="잎뒷면털"))

        print(records)

        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafBlade",
    response_model=ResponseDto,
    summary="Create Leaf Blade records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_blade(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Blade records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '잎몸(잎모양)' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []

        # 코드와 LeafTipEnum 매핑 테이블
        mappingTable = {
            "1": LeafBladeEnum.needle.value,
            "2": LeafBladeEnum.linear.value,
            "3": LeafBladeEnum.lanceolate.value,
            "4": LeafBladeEnum.oblanceolate.value,
            "5": LeafBladeEnum.cordate.value,
            "6": LeafBladeEnum.reniform.value,
            "7": LeafBladeEnum.circular.value,
            "8": LeafBladeEnum.elliptical.value,
            "11": LeafBladeEnum.ovate.value,
            "12": LeafBladeEnum.obovate.value,
            "13": LeafBladeEnum.triangular.value,
            "16": LeafBladeEnum.dandelion.value,
            "17": LeafBladeEnum.spatulate.value,
            "18": LeafBladeEnum.rhomboid.value,
        }

        for _, row in df.iterrows():
            title = row['수종']
            description = row['코드']

            if pd.notna(title) and pd.notna(description):
                descriptionList = str(description).strip().split(' ')
                koreanDiscriptionList = []
                for i in descriptionList:
                    koreanDiscriptionList.append(mappingTable[i])
                koreanDescription = ','.join(koreanDiscriptionList)
                records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="잎몸"))

        print(records)
        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafBase",
    response_model=ResponseDto,
    summary="Create Leaf Base records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_base(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Base records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '잎밑' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []

        # 코드와 LeafTipEnum 매핑 테이블
        mappingTable = {
            "1": LeafBaseEnum.cuneate.value,
            "2": LeafBaseEnum.auriculate.value,
            "3": LeafBaseEnum.obtuse.value,
            "4": LeafBaseEnum.oblique.value,
            "5": LeafBaseEnum.acute.value,
            "6": LeafBaseEnum.decurrent.value,
            "7": LeafBaseEnum.cordate.value,
            "8": LeafBaseEnum.rounded.value,
            "9": LeafBaseEnum.peltate.value,
            "10": LeafBaseEnum.truncate.value,
            "12": LeafBaseEnum.attenuate.value,
        }

        for _, row in df.iterrows():
            title = row['수종']
            description = row['코드']

            if pd.notna(title) and pd.notna(description):
                descriptionList = str(description).strip().split(' ')
                koreanDiscriptionList = []
                for i in descriptionList:
                    koreanDiscriptionList.append(mappingTable[i])
                koreanDescription = ','.join(koreanDiscriptionList)
                records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="잎밑"))

        print(records)
        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafTopsideHair",
    response_model=ResponseDto,
    summary="Create Leaf Topside Hair records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_topside_hair(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Topside Hair records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '잎앞면털' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            description = row['코드']

            if (pd.notna(title) and pd.notna(description)) is False:
                continue

            descriptionList = str(description).split(' ')
            koreanDiscriptionList = []
            for i in descriptionList:
                koreanDiscriptionList.append(list(BasicTypeEnum)[int(i) - 1].value)
            koreanDescription = ','.join(koreanDiscriptionList)
            records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="잎앞면털"))

        print(records)

        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelLeafArrangement",
    response_model=ResponseDto,
    summary="Create Leaf Arrangement records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_leaf_arrangement(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Leaf Arrangement records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '잎차례' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []

        # 코드와 LeafTipEnum 매핑 테이블
        mappingTable = {
            "1": LeafArrangementEnum.alternate.value,
            "2": LeafArrangementEnum.opposite.value,
            "3": LeafArrangementEnum.whorled.value,
            "4": LeafArrangementEnum.clustered.value,
        }

        for _, row in df.iterrows():
            title = row['수종']
            description = row['코드']

            if pd.notna(title) and pd.notna(description):
                descriptionList = str(description).strip().split(' ')
                koreanDiscriptionList = []
                for i in descriptionList:
                    koreanDiscriptionList.append(mappingTable[i])
                koreanDescription = ','.join(koreanDiscriptionList)
                records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="잎차례"))

        print(records)
        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@pinecone_router.post(
    "/createRecordsWithExcelTooth",
    response_model=ResponseDto,
    summary="Create Tooth records from an Excel file in the classify Index of HibiscusGPT project.",
    response_description="The records have been created successfully.",
)
async def create_records_with_excel_tooth(
        file: UploadFile = File(...),
) -> ResponseDto:
    """
    ## Create Tooth records from an Excel file in the classify Index of HibiscusGPT project.
    ---
    - **file** (required) : the Excel file containing records
    """

    try:
        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        # Ensure the required columns are present
        if '수종' not in df.columns or '톱니' not in df.columns:
            raise HTTPException(status_code=400, detail="Excel file must contain 'title' and 'description' columns")

        # Create a list of CreateRecordRequestDto
        records = []
        for _, row in df.iterrows():
            title = row['수종']
            description = row['코드']

            if (pd.notna(title) and pd.notna(description)) is False:
                continue

            descriptionList = str(description).split(' ')
            koreanDiscriptionList = []
            for i in descriptionList:
                koreanDiscriptionList.append(list(BasicTypeEnum)[int(i) - 1].value)
            koreanDescription = ','.join(koreanDiscriptionList)
            records.append(CreateRecordRequestDto(index="classify", title=title, description=koreanDescription, column="톱니"))

        print(records)

        # Call the PineconeService to create records
        result = await PineconeService.create_records(records)

        return ResponseDto(
            success=True,
            message=result["result"],
            data=result,
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
