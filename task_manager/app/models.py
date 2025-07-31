from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    TASK_TYPES = [
        ('sum', 'Sum of two numbers'),
        ('countdown', 'Countdown timer'),
    ]

    TASK_STATUSES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')  # Связь с пользователем
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)  # Тип задачи
    input_data = models.JSONField()  # Входные данные (JSON)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='pending')  # Статус задачи
    result = models.JSONField(null=True, blank=True)  # Результат задачи (JSON)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f"{self.task_type} - {self.status}"
    