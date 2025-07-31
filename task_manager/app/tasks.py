from celery import shared_task
from .models import Task
import time


@shared_task
def process_task(task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.status = "in_progress"
        task.save()

        # Логика выполнения задачи
        if task.task_type == "sum":
            a = task.input_data.get("a", 0)
            b = task.input_data.get("b", 0)
            result = {"sum": a + b}
        elif task.task_type == "countdown":
            seconds = task.input_data.get("seconds", 0)
            time.sleep(seconds)
            result = {"message": "Countdown completed"}
        else:
            result = {"error": "Invalid task type"}
            task.status = "error"
            task.result = result
            task.save()
            return

        # Сохраняем результат
        task.status = "completed"
        task.result = result
        task.save()
    except Task.DoesNotExist:
        pass
