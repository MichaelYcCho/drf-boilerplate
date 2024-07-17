from drf_yasg import openapi

user_login_request = openapi.Schema(
    title="Login",
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="admin",
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="admin",
        ),
    },
)
