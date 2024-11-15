from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cards.models import Category
from apps.cards.selectors import category_list
from apps.cards.services import category_create, category_update
from apps.common.permissions import IsOwner
from apps.common.utils import delete_object


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


class CategoryUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)

    def post(self, request, category_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_update(category_id=category_id, data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class CategoryDeleteApi(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, category_id):
        delete_object(Category, id=category_id)

        return Response(status=status.HTTP_200_OK)
