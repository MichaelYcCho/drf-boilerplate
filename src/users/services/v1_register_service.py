from core.utils.exceptions.exception import UserExceptions
from users.models import User


class RegisterService:
    def __init__(self, validated_data: dict) -> None:
        self.username = validated_data["username"]
        self.password = validated_data["password"]
        self.password_confirm = validated_data["password_confirm"]
        self.email = validated_data["email"]
        self.phone = validated_data["phone"]

    def validate_password(self) -> None:
        if self.password != self.password_confirm:
            raise UserExceptions.PasswordNotMatch

    def create_user(self) -> User:
        user = User.objects.create(
            username=self.username,
            email=self.email,
            phone=self.phone,
        )
        user.set_password(self.password)
        user.save()
        return user
