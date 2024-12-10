from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", max_length=255, blank=True
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
    city = models.CharField(max_length=100, blank=True, null=True)  # Поле для города

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Убираем 'username' из обязательных полей

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     if not self.username:  # Если username не задан, используем email
    #         self.username = self.email
    #     super(CustomUser, self).save(*args, **kwargs)
