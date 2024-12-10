from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import CoursesConfig
from .views import (
    CourseViewSet,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')

app_name = CoursesConfig.name
urlpatterns = [
    path('', include(router.urls)),  # CRUD для курсов
    path('<int:course_id>/lessons/', LessonListAPIView.as_view(), name='lesson-list'),  # Список уроков
    path('<int:course_id>/lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),  # Детали урока
    path('<int:course_id>/lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),  # Обновление
    path('<int:course_id>/lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),  # Удаление
]
