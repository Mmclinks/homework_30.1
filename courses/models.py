from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=255, default="Курс", verbose_name="Название курса")
    preview = models.ImageField(upload_to='courses/previews/', default='courses/previews/course.png')
    description = models.TextField(verbose_name="Описание курса")

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255, default="Урок", verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока/")
    preview = models.ImageField(upload_to="lessons/previews/", default='lessons/previews/lesson.png')
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")

    def __str__(self):
        return self.name
