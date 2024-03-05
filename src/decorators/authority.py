from http import HTTPStatus

from fastapi import HTTPException

from src.dtos.base_dto import TokenEntity
from src.utils import config


def verify_authority(token_entity: TokenEntity, input_id: str):
    """
    토큰의 user_id와 입력된 id가 일치하는지 확인합니다.
    관리자 token 은 모든 id에 대해 접근 가능합니다.

    :param token_entity:
    :param input_id:
    :return:
    """
    if (
        token_entity.token_type != config.APIKeyHeader.ADMIN.value
        and token_entity.shop.id != input_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN.value, detail=HTTPStatus.FORBIDDEN.phrase
        )


def verify_admin_authority(token_entity: TokenEntity):
    """
    관리자 token 여부를 확인합니다.

    :param token_entity:
    :return:
    """
    if token_entity.token_type != config.APIKeyHeader.ADMIN.value:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN.value, detail=HTTPStatus.FORBIDDEN.phrase
        )
