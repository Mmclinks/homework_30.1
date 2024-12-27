from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .apps import CoursesConfig
from .views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView,
                    LessonListAPIView, LessonRetrieveAPIView,
                    LessonUpdateAPIView, PaymentViewSet, SubscriptionAPIView)

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path('lessons/<int:course_id>/', views.LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:course_id>/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('lessons/<int:course_id>/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path("subscribe/", SubscriptionAPIView.as_view(), name="subscribe"),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
] + router.urls
