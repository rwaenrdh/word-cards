from typing import Iterable

from apps.cards.models import Card


def card_list(*, user) -> Iterable[Card]:
    qs = Card.objects.filter(created_by=user)

    return qs
