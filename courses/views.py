from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from users.models import Payment
from users.permissions import IsModerator
from .models import Course, Lesson
from .serializers import CourseSerializer

from .serializers import PaymentSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Lesson
from .serializers import LessonSerializer
from users.permissions import IsOwnerOrReadOnly

class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsModerator()]
        return [IsAuthenticatedOrReadOnly()]

class LessonListAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Lesson.objects.filter(course_id=course_id)

class LessonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrReadOnly]



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


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
    ordering_fields = ['date']
    ordering = ['date']  # Сортировка по умолчанию (по дате)
