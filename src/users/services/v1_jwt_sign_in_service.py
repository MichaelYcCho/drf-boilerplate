import jwt
import datetime
from django.conf import settings


from django.contrib.auth import authenticate
from rest_framework.request import Request

from core.utils.constant import ACCESS_TOKEN, REFRESH_TOKEN
from core.utils.exceptions.exception import UserExceptions


class JWTSignInService:
    def __init__(self, request: Request, data: dict) -> None:
        self.request = request
        self.username = data.get("username")
        self.password = data.get("password")

    def sign_in(self):
        user = authenticate(
            username=self.username,
            password=self.password,
        )

        if user:
            payload = {
                "user_id": user.id,
            }
            token = self.generate_jwt_token(payload, ACCESS_TOKEN)

            return token

        raise UserExceptions.UserSignInFailed

    def generate_jwt_token(self, payload, token_type):
        if token_type == ACCESS_TOKEN:
            exp = datetime.datetime.now() + datetime.timedelta(hours=2)
        elif token_type == REFRESH_TOKEN:
            exp = datetime.datetime.now() + datetime.timedelta(weeks=2)
        else:
            raise Exception("Invalid tokenType")

        payload["exp"] = exp
        payload["iat"] = datetime.datetime.now()
        encoded = jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        return encoded
