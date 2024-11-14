from django.urls import include, path

from apps.cards.apis.cards import CardListApi

card_patterns = [
    path('', CardListApi.as_view()),
]

urlpatterns = [
    path('cards/', include(card_patterns)),
]
