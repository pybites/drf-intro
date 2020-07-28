from django.urls import path

from .views import PomodoroList, PomodoroDetail

app_name = 'api'
urlpatterns = [
    path('', PomodoroList.as_view()),
    path('<int:pk>/', PomodoroDetail.as_view()),
]
