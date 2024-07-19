from django.urls import path

from users.controllers.v1_jwt_sign_in_controller import SignInAPI
from users.controllers.v1_register_controller import RegisterAPI

urlpatterns = [
    path(
        "v1/sign-in",
        SignInAPI.as_view(),
        name="sign-in",
    ),
    path(
        "v1/register",
        RegisterAPI.as_view(),
        name="register",
    ),
]
