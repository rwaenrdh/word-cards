from typing import List

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import exceptions

from apps.cards.models import Card, Category
from apps.common.utils import model_update


def card_add_category(*, user: User, card: Card, category_id: int):
    category = get_object_or_404(Category, id=category_id)

    if category.created_by != user:
        raise PermissionDenied()

    card.categories.add(category)


@transaction.atomic
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

    categories_id = categories_id or []

    for category_id in categories_id:
        card_add_category(user=user, card=card, category_id=category_id)

    return card


def category_create(*, user: User, name: str) -> Category:
    category = Category(created_by=user, name=name)

    try:
        category.full_clean()
    except ValidationError:
        raise exceptions.ValidationError({'name': 'Category with such name already exists.'})

    category.save()

    return category


def category_update(*, category_id: int, data) -> Category:
    category = get_object_or_404(Category, id=category_id)

    non_side_effect_fields = ['name']

    category, has_updated = model_update(instance=category, fields=non_side_effect_fields, data=data)

    return category
