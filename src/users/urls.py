from django.urls import path

from users.controllers.v1_login_controller import LogInAPI
from users.controllers.v1_register_controller import RegisterAPI

urlpatterns = [
    path(
        "v1/register",
        RegisterAPI.as_view(),
        name="register",
    ),
    path(
        "v1/login",
        LogInAPI.as_view(),
        name="login",
    ),
]
