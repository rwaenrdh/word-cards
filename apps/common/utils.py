from typing import Any, Dict, List, Tuple

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import serializers

from apps.common.types import DjangoModelType


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='inline_serializer', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def model_update(
    *,
    instance: DjangoModelType,
    fields: List[str],
    data: Dict[str, Any],
    auto_updated_at=True,
) -> Tuple[DjangoModelType, bool]:
    has_updated = False
    m2m_data = {}
    update_fields = []

    model_fields = {field.name: field for field in instance._meta.get_fields()}

    for field in fields:
        if field not in data:
            continue

        model_field = model_fields.get(field)

        assert model_field is not None, f'{field} is not part of {instance.__class__.__name__} fields.'

        if isinstance(model_field, models.ManyToManyField):
            m2m_data[field] = data[field]
            continue

        if getattr(instance, field) != data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, data[field])

    if has_updated:
        if auto_updated_at:
            if 'updated_at' in model_fields and 'updated_at' not in update_fields:
                update_fields.append('updated_at')
                instance.updated_at = timezone.now()

        instance.full_clean()
        instance.save(update_fields=update_fields)

    for field_name, value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(value)

        has_updated = True

    return instance, has_updated


def delete_object(model, **kwargs):
    obj = get_object_or_404(model, **kwargs)

    obj.delete()
