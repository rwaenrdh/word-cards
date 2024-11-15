from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.services import user_create


class UserCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserMeApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        username = serializers.CharField()

    def get(self, request):
        data = self.OutputSerializer(request.user).data

        return Response(data)
