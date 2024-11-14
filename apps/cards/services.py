from typing import List

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from apps.cards.models import Card, Category


def card_add_category(*, user: User, card: Card, category_id: int):
    category = get_object_or_404(Category, id=category_id)

    if category.created_by is not user:
        raise PermissionDenied()

    card.categories.add(category)


def card_create(
    *,
    user: User,
    word: str,
    translation: str,
    example: str = '',
    categories_id: List[int] | None = None,
) -> Card:
    card = Card(
        created_by=user,
        word=word,
        translation=translation,
        example=example,
    )

    card.full_clean()
    card.save()

    for category_id in categories_id:
        card_add_category(user=user, card=card, category_id=category_id)

    return card
