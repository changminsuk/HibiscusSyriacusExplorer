from enum import Enum

from pydantic import BaseModel, Field


class CreateRecordRequestDto(BaseModel):
    index: str = "classify"
    title: str
    description: str
    column: str


class CreateArrangeRecordRequestDto(BaseModel):
    index: str = "classify"
    title: str
    min: float
    max: float
    column: str


class BasicTypeEnum(str, Enum):
    present = "있음"
    absent = "없음"
    unknown = "모름"


class ShapeEnum(str, Enum):
    single = "단엽"
    compound = "복엽"


class LeafTipEnum(str, Enum):
    cuspidate = "점첨두"
    acute = "예두"
    mucronate = "급첨두"
    obtuse = "둔두"
    rounded = "원두"
    emarginate = "요두"
    truncate = "평두"
    acuminate = "미두"
    unknown = "모름"


class LeafBladeEnum(str, Enum):
    needle = "침형"
    linear = "선형"
    lanceolate = "피침형"
    oblanceolate = "도피침형"
    cordate = "심장형"
    reniform = "신장형"
    circular = "원형"
    elliptical = "타원형"
    ovate = "난형"
    obovate = "도란형"
    triangular = "삼각형"
    dandelion = "민들레형"
    spatulate = "주걱형"
    rhomboid = "능형"
    unknown = "모름"


class LeafBaseEnum(str, Enum):
    cuneate = "유저"
    auriculate = "설저"
    obtuse = "둔저"
    oblique = "왜저"
    acute = "예저"
    decurrent = "순저"
    cordate = "심장저"
    rounded = "원저"
    peltate = "관천저"
    truncate = "평저"
    attenuate = "극저"
    unknown = "모름"


class LeafArrangementEnum(str, Enum):
    alternate = "어긋나기"
    opposite = "마주나기"
    whorled = "돌려나기"
    clustered = "모여나기"
    unknown = "모름"


class QueryPineconeRequestDto(BaseModel):
    serration: BasicTypeEnum = Field(BasicTypeEnum.unknown, description="결각은 있음, 없음, 모름 중 하나여야 합니다.")
    shape: ShapeEnum = Field(ShapeEnum.single, description="생김새는 단엽 또는 복엽 중 하나여야 합니다.")
    leaflet_count: float = Field(-1, description="소엽갯수는 -1에서 25 사이의 값이어야 합니다.")
    leaf_length: float = Field(-1, description="잎길이는 -1에서 50 사이의 값이어야 합니다.(cm)")
    leaf_tip: LeafTipEnum = Field(LeafTipEnum.unknown, description="잎끝은 미두, 점첨두, 예두, 급첨두, 둔두, 원두, 요두, 평두, 모름 중 하나여야 합니다.")
    leaf_width: float = Field(-1, description="잎너비는 -1에서 30 사이의 값이어야 합니다.(cm)")
    leaf_underside_hair: BasicTypeEnum = Field(BasicTypeEnum.unknown, description="잎뒷면털은 있음, 없음, 모름 중 하나여야 합니다.")
    leaf_blade: LeafBladeEnum = Field(LeafBladeEnum.unknown,
                                      description="잎날은 침형, 선형, 피침형, 난형, 능형, 삼각형, 심장형, 신장형, 도피침형, 도란형, 주걱형, 민들레형, 원형, 타원형, 모름 중 하나여야 합니다.")
    leaf_base: LeafBaseEnum = Field(LeafBaseEnum.unknown, description="잎밑부분은 유저, 둔저, 원저, 왜저, 평저, 예저, 설저, 극저, 심장저, 순저, 관천저 중 하나여야 합니다.")
    leaf_topside_hair: BasicTypeEnum = Field(BasicTypeEnum.unknown, description="잎앞면털은 있음, 없음, 모름 중 하나여야 합니다.")
    leaf_arrangement: LeafArrangementEnum = Field(LeafArrangementEnum.unknown, description="잎차례는 어긋나기, 마주나기, 돌려나기, 모여나기, 모름 중 하나여야 합니다.")
    tooth: BasicTypeEnum = Field(BasicTypeEnum.unknown, description="톱니는 있음, 없음, 모름 중 하나여야 합니다.")


class QueryWithTitleRequestDto(BaseModel):
    title: str


class DeleteColumnRequestDto(BaseModel):
    column: str
