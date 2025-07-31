from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")

# Создаем экземпляр Celery
app = Celery("task_manager")

# Загружаем конфигурацию Celery из настроек Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим задачи в приложениях Django
app.autodiscover_tasks()
