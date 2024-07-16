from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services.v1_login_service import UserSignInService


class LogInAPI(APIView):
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

        class Meta:
            ref_name = "login_input"

    class OutputSerializer(serializers.Serializer):
        token = serializers.CharField()

        class Meta:
            ref_name = "login_output"

    def post(self, request: Request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        service = UserSignInService(request, input_serializer.validated_data)
        token = service.log_in()
        output_serializer = self.OutputSerializer(data={"token": token.key})
        output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
