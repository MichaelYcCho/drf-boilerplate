from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services.v1_jwt_sign_in_service import JWTSignInService
from core.utils.exceptions.exception import UserExceptions

from users.controllers.swaggers import user_login_request


class SignInAPI(APIView):
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

        class Meta:
            ref_name = "login_input"

    class OutputSerializer(serializers.Serializer):
        access_token = serializers.CharField()
        refresh_token = serializers.CharField()

        class Meta:
            ref_name = "login_output"

    @swagger_auto_schema(
        tags=["users"],
        operation_summary="V1 Sign In API",
        operation_description="로그인 API",
        request_body=user_login_request,
        responses={
            status.HTTP_200_OK: openapi.Response("로그인 완료"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                " or ".join(
                    [
                        UserExceptions.UserInfoDoesNotExist.default_detail,
                        UserExceptions.UserSignInFailed.default_detail,
                    ]
                )
            ),
        },
    )
    def post(self, request: Request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        service = JWTSignInService(request, input_serializer.validated_data)
        token_response = service.sign_in()
        output_serializer = self.OutputSerializer(
            data={
                "access_token": token_response["access_token"],
                "refresh_token": token_response["refresh_token"],
            }
        )
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class ReIssueAPI(APIView):
    pass
