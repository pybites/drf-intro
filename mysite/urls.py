from django.contrib import admin
from django.urls import path, include

app_name = 'mysite'
urlpatterns = [
    path('api/', include('api.urls', namespace="api")),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
