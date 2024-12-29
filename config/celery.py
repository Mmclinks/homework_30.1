from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Загружаем настройки из settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматическое обнаружение задач в приложениях
app.autodiscover_tasks()
