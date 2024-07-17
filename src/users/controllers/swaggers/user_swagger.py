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


user_register_request = openapi.Schema(
    title="Register",
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="test_register",
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="test_register",
        ),
        "password_confirm": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="test_register",
        ),
        "email": openapi.Schema(
            type=openapi.TYPE_STRING, example="test_register@gmail.com"
        ),
        "phone": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="01012345678",
        ),
    },
)
