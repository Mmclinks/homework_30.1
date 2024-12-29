from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, status

from rest_framework.generics import (DestroyAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from users import permissions
from users.permissions import IsModerator, IsOwnerOrReadOnly
from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer
from django.conf import settings
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Payment
from .serializers import PaymentSerializer
from .service import create_product, create_price, create_checkout_session


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


stripe.api_key = settings.STRIPE_API_KEY


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.select_related("user", "course", "lesson")
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({"error": "course_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        # Создаем продукт в Stripe
        stripe_product = create_product(course)
        product_id = stripe_product['id']

        # Создаем цену для продукта в Stripe
        price = create_price(product_id, int(course.price * 100))  # Цена в копейках
        price_id = price['id']

        # Создаем сессию для оплаты через Stripe
        session = create_checkout_session(price_id, success_url="https://yourdomain.com/success/",
                                          cancel_url="https://yourdomain.com/cancel/")

        # Сохраняем данные о платеже в базе
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            stripe_session_id=session['id'],
            stripe_price_id=price_id,
            payment_url=session['url'],
            amount=course.price,
            status="pending"  # Можно обновлять позже по статусу сессии
        )

        # Отправляем пользователю ссылку для оплаты
        return Response({"payment_url": session['url']}, status=status.HTTP_200_OK)


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


class PaymentStatusView(APIView):
    """
    Просмотр статуса платежа через Stripe.
    """

    def get(self, request, session_id, *args, **kwargs):
        # Получаем статус сессии через Stripe
        session = stripe.checkout.Session.retrieve(session_id)

        # Обновляем статус платежа в нашей системе
        payment = Payment.objects.get(stripe_session_id=session_id)
        payment.status = session['payment_status']
        payment.save()

        return Response({"status": session['payment_status']}, status=status.HTTP_200_OK)
