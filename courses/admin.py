from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Поля, существующие в модели Course
    search_fields = ('name',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'video_url')  # Поля, существующие в модели Lesson
    search_fields = ('name', 'course__name')


from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

# Создаем интервал выполнения
schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.DAYS,
)

# Добавляем задачу
PeriodicTask.objects.get_or_create(
    interval=schedule,
    name='Deactivate inactive users',
    task='app_name.tasks.deactivate_inactive_users',
    defaults={'args': json.dumps([])},
)