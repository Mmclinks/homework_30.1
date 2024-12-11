from rest_framework import viewsets, generics

from users.models import Payment
from .serializers import CourseSerializer, LessonSerializer

from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import Course, Lesson
from .serializers import PaymentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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
