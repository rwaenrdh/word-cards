from django.urls import include, path

from apps.cards.apis.cards import CardCreateApi, CardListApi
from apps.cards.apis.categories import CategoryCreateApi, CategoryListApi, CategoryUpdateApi

card_patterns = [
    path('create/', CardCreateApi.as_view()),
    path('', CardListApi.as_view()),
]

category_patterns = [
    path('create/', CategoryCreateApi.as_view()),
    path('<int:category_id>/update/', CategoryUpdateApi.as_view()),
    path('', CategoryListApi.as_view()),
]


urlpatterns = [
    path('cards/', include(card_patterns)),
    path('categories/', include(category_patterns)),
]
