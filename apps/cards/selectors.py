from typing import Iterable

from django.contrib.auth.models import User

from apps.cards.filters import CardFilter
from apps.cards.models import Card, Category


def card_list(*, user: User, filters=None) -> Iterable[Card]:
    filters = filters or {}

    qs = Card.objects.filter(created_by=user)

    return CardFilter(filters, qs).qs


def category_list(*, user: User) -> Iterable[Category]:
    qs = Category.objects.filter(created_by=user)

    return qs
