from django.contrib.auth import authenticate
from rest_framework.request import Request

from core.utils.exceptions.exception import UserExceptions


class UserSignInService:
    def __init__(self, request: Request, data: dict) -> None:
        self.request = request
        self.username = data.get("username")
        self.password = data.get("password")

    def log_in(self):
        user = authenticate(
            username=self.username,
            password=self.password,
        )

        if user:
            # TODO: implement JWT token
            return

        raise UserExceptions.UserSignInFailed
