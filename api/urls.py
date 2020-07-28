from django.urls import path

from .views import (PomodoroList, PomodoroDetail,
                    UserList, UserDetail)

app_name = 'api'
urlpatterns = [
    path('pomos/', PomodoroList.as_view()),
    path('pomos/<int:pk>/', PomodoroDetail.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
