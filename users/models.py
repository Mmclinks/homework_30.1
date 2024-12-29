from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from rest_framework.exceptions import ValidationError

from courses.models import Course, Lesson


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email обязательно.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('У суперпользователя должно быть is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('У суперпользователя должно быть is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Убираем поле username
    email = models.EmailField(
        unique=True, verbose_name="Email", max_length=255, blank=False
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите аватар",
    )
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Оставляем пустым

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Оплаченный курс")
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Оплаченный урок")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Оплата от {self.user} на сумму {self.amount}"

    def clean(self):
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError('Укажите оплаченный курс или урок.')