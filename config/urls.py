from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),  # Подключение маршрутов из приложения courses
    path('api/', include('rest_framework.urls')),  # Если вы используете DRF
]