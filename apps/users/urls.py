from django.urls import path

from apps.users.apis import UserCreateApi, UserMeApi

urlpatterns = [
    path('me/', UserMeApi.as_view()),
    path('create/', UserCreateApi.as_view()),
]
