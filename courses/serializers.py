from rest_framework import serializers
from .models import Course, Lesson
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'paid_course',  # Исправлено с 'course'
            'paid_lesson',  # Исправлено с 'lesson'
            'amount',
            'payment_method',
            'payment_date'  # Исправлено с 'date'
        ]
