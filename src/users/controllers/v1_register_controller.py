from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.controllers.swaggers import user_register_request
from users.services.v1_register_service import RegisterService


class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()
        password_confirm = serializers.CharField()
        email = serializers.EmailField()
        phone = serializers.CharField()

        class Meta:
            ref_name = "register_input"

    @swagger_auto_schema(
        tags=["users"],
        operation_summary="V1 Register API",
        operation_description="회원가입",
        request_body=user_register_request,
        responses={
            status.HTTP_201_CREATED: openapi.Response("가입 완료"),
        },
    )
    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = RegisterService(serializer.validated_data)
        service.validate_password()
        service.create_user()

        return Response(status=status.HTTP_201_CREATED)
