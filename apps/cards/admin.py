from django.contrib import admin

from apps.cards.models import Card, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'name', ]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'word', 'translation', ]