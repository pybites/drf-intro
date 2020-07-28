from django.contrib import admin
from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('', include('pomodoro.urls', namespace="pomodoro")),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
