from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .tasks import notify_users_about_course_update

class Course(models.Model):
    name = models.CharField(max_length=255, default="Курс", verbose_name="Название курса")
    preview = models.ImageField(upload_to='courses/previews/', default='courses/previews/course.png')
    description = models.TextField(verbose_name="Описание курса")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255, default="Урок", verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")  # Исправил описание
    preview = models.ImageField(upload_to="lessons/previews/", default='lessons/previews/lesson.png')
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Владелец"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_update = self.pk is not None  # Проверяем, существует ли объект
        super().save(*args, **kwargs)  # Сохраняем изменения
        if is_update:
            notify_users_about_course_update.delay(self.course.id)


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используем AUTH_USER_MODEL
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"Подписка пользователя {self.user.username} на курс {self.course.name}"
