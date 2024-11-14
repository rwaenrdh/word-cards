from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.cards.selectors import card_list
from apps.common.pagination import LimitOffsetPagination, get_paginated_response
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
