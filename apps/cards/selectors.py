from typing import Iterable

from apps.cards.models import Card, Category


def card_list(*, user) -> Iterable[Card]:
    qs = Card.objects.filter(created_by=user)

    return qs


def category_list(*, user) -> Iterable[Category]:
    qs = Category.objects.filter(created_by=user)

    return qs
