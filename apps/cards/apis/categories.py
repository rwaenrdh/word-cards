from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cards.selectors import category_list
from apps.cards.services import category_create


class CategoryListApi(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()

    def get(self, request):
        categories = category_list(user=request.user)

        data = self.OutputSerializer(categories, many=True).data

        return Response(data)


class CategoryCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_create(user=request.user, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
