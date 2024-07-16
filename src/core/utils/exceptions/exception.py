from __future__ import annotations

from rest_framework import status
from rest_framework.exceptions import APIException


class BaseExceptions:
    pass


class UserExceptions:
    class NotFoundUser(APIException):
        error_code = 100001
        status_code = status.HTTP_404_NOT_FOUND
        default_detail = "존재하지 않는 유저입니다"

    class UserSignInFailed(APIException):
        error_code = 100002
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "로그인에 실패했습니다"

    class UserInfoDoesNotExist(APIException):
        error_code = 100003
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "유저 ID 또는 비밀번호가 일치하지 않습니다"

    class PasswordNotMatch(APIException):
        error_code = 100004
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "비밀번호가 일치하지 않습니다"


class AuctionExceptions:
    class NotFoundAuction(APIException):
        error_code = 200001
        status_code = status.HTTP_404_NOT_FOUND
        default_detail = "일치하는 경매차량이 존재하지 않습니다"

    class NotEnoughImages(APIException):
        error_code = 200002
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = "이미지는 5장 이상이어야합니다"
