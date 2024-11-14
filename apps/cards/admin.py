from django.contrib import admin

from apps.cards.models import Card, Category

admin.site.register(Card)
admin.site.register(Category)
