import jwt
import datetime
from django.conf import settings


from django.contrib.auth import authenticate
from rest_framework.request import Request

from core.utils.constant import ACCESS_TOKEN, REFRESH_TOKEN
from core.utils.exceptions.exception import TokenExceptions, UserExceptions
from users.models.token import TokenStorage
from users.models.user import User


class JWTSignInService:
    def __init__(self, request: Request, data: dict) -> None:
        self.request = request
        self.username = data.get("username")
        self.password = data.get("password")
        self.refresh_token = data.get("refresh_token")

    def sign_in(self):
        user = authenticate(
            username=self.username,
            password=self.password,
        )

        if user:
            payload = {
                "user_id": user.id,
            }
            access_token = self.generate_jwt_token(payload, ACCESS_TOKEN)
            refresh_token = self.generate_jwt_token(payload, REFRESH_TOKEN)

            token_response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            token_storage = TokenStorage.objects.filter(user=user).first()
            if token_storage is None:
                token_storage = TokenStorage.objects.create(
                    user=user,
                    refresh_token=refresh_token,
                )

            token_storage.refresh_token = refresh_token
            token_storage.save()

            return token_response

        raise UserExceptions.UserSignInFailed

    def reissue(self):

        decode_token = jwt.decode(
            self.refresh_token,
            settings.JWT_SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM,
        )

        user = User.objects.filter(id=decode_token["user_id"]).first()
        token_storage = TokenStorage.objects.filter(
            user=user, refresh_token=self.refresh_token
        ).first()

        if token_storage is None:
            raise TokenExceptions.TokenInvalid

        payload = {
            "user_id": token_storage.user.id,
        }
        access_token = self.generate_jwt_token(payload, ACCESS_TOKEN)
        refresh_token = self.generate_jwt_token(payload, REFRESH_TOKEN)

        token_storage.refresh_token = refresh_token
        token_storage.save()

        token_response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return token_response

    def generate_jwt_token(self, payload, token_type):
        if token_type == ACCESS_TOKEN:
            expired_at = datetime.datetime.now() + datetime.timedelta(hours=2)
        elif token_type == REFRESH_TOKEN:
            expired_at = datetime.datetime.now() + datetime.timedelta(weeks=2)
        else:
            raise Exception("Invalid tokenType")

        payload["exp"] = expired_at
        payload["iat"] = datetime.datetime.now()
        encoded = jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        return encoded
