from django.db import models

from apps.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'created_by']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Card(BaseModel):
    word = models.CharField(max_length=64)
    translation = models.CharField(max_length=64)
    example = models.TextField(max_length=120, blank=True)

    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.word
