from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from users import permissions
from users.models import Payment
from users.permissions import IsModerator, IsOwnerOrReadOnly
from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwnerOrReadOnly,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwnerOrReadOnly,)
        return super().get_permissions()


class LessonListAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_id'])

    def perform_create(self, serializer):
        course = Course.objects.get(id=self.kwargs['course_id'])
        serializer.save(course=course)



class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """
        Автоматическое добавление поля "Владелец" при создании.
        """
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Просмотр урокоа.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwnerOrReadOnly)


class LessonUpdateAPIView(UpdateAPIView):
    """
    Изменение урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwnerOrReadOnly)


class LessonDestroyAPIView(DestroyAPIView):
    """
    Удаление урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, permissions.IsOwnerOrReadOnly | permissions.IsModerator)

    def perform_destroy(self, instance):
        # Здесь можно кастомизировать логику удаления, если нужно
        instance.delete()

class PaymentFilter(filters.FilterSet):
    # Фильтрация по курсу
    course = filters.ModelChoiceFilter(queryset=Course.objects.all(), field_name='course', label='Курс')
    # Фильтрация по уроку
    lesson = filters.ModelChoiceFilter(queryset=Lesson.objects.all(), field_name='lesson', label='Урок')
    # Фильтрация по способу оплаты
    payment_method = filters.ChoiceFilter(choices=[('cash', 'Наличные'), ('transfer', 'Перевод')],
                                          label='Способ оплаты')
    # Фильтрация по диапазону дат
    date = filters.DateFromToRangeFilter(field_name='date', label='Дата оплаты')

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method', 'date']



class PaymentViewSet(ModelViewSet):
    """
    ViewSet для работы с платежами.
    """

    queryset = Payment.objects.select_related("user", "course", "lesson")
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["date"]
    ordering = ["-date"]


class SubscriptionAPIView(APIView):
    """
    Контроллер для подписки на обновления курса.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "course_id is required"}, status=HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message}, status=HTTP_200_OK)