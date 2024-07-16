from django.urls import path

from users.controllers.v1_login_controller import LogInAPI

urlpatterns = [
    path(
        "v1/login",
        LogInAPI.as_view(),
        name="login",
    ),
]
