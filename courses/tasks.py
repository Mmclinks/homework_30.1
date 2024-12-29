from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, datetime

from django.core.mail import send_mail
from celery import shared_task

@shared_task
def notify_users_about_course_update(course_id):
    from courses.models import Subscription  # Импортируем здесь, чтобы избежать циклического импорта
    from courses.models import Course  # Импортируем внутри функции, чтобы избежать проблем с импортом

    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    last_updated = course.updated_at
    if datetime.now() - last_updated < timedelta(hours=4):
        return "Course updated too recently, skipping notification."

    for subscription in subscriptions:
        send_mail(
            subject=f"Обновление курса: {course.name}",
            message="В курсе появились новые материалы!",
            from_email="admin@example.com",
            recipient_list=[subscription.user.email],
        )
    return "Emails sent successfully."



@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    ).exclude(last_login=None)  # Исключаем пользователей без даты входа

    for user in inactive_users:
        user.is_active = False
        user.save()
    return f"Deactivated {inactive_users.count()} users."