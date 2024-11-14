from django.urls import include, path

from apps.cards.apis.cards import CardListApi
from apps.cards.apis.categories import CategoryListApi

card_patterns = [
    path('', CardListApi.as_view()),
]

category_patterns = [
    path('', CategoryListApi.as_view()),
]


urlpatterns = [
    path('cards/', include(card_patterns)),
    path('category/', include(category_patterns)),
]
