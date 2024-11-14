from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cards.selectors import card_list
from apps.cards.services import card_create, card_update
from apps.common.pagination import LimitOffsetPagination, get_paginated_response
from apps.common.permissions import IsOwner
from apps.common.utils import inline_serializer


class CardListApi(APIView):
    permission_classes = [IsAuthenticated]

    class Pagination(LimitOffsetPagination):
        default_limit = 25

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        word = serializers.CharField()
        translation = serializers.CharField()
        example = serializers.CharField()
        categories = inline_serializer(many=True, fields={
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
        })

    def get(self, request):
        cards = card_list(user=request.user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=cards,
            request=request,
            view=self,
        )


class CardCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        word = serializers.CharField(max_length=64)
        translation = serializers.CharField(max_length=64)
        example = serializers.CharField(required=False, max_length=120)
        categories_id = serializers.ListField(
            required=False,
            child=serializers.IntegerField(),
        )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_create(user=request.user, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class CardUpdateApi(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    class InputSerializer(serializers.Serializer):
        word = serializers.CharField(required=False)
        translation = serializers.CharField(required=False)
        example = serializers.CharField(required=False)
        categories_id = serializers.ListField(required=False)

    def post(self, request, card_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_update(card_id=card_id, data=serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
