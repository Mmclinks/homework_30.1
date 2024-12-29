from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Course, Lesson
from users.models import Payment

class Command(BaseCommand):
    help = "Создает тестовые записи для модели Payment"

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user or not course or not lesson:
            self.stdout.write(self.style.ERROR("Проверьте наличие пользователей, курсов и уроков в базе!"))
            return

        Payment.objects.create(
            user=user,
            paid_course=course,
            amount=5000.00,
            payment_method="cash"
        )

        Payment.objects.create(
            user=user,
            paid_lesson=lesson,
            amount=1000.00,
            payment_method="transfer"
        )

        self.stdout.write(self.style.SUCCESS("Тестовые записи успешно созданы!"))
