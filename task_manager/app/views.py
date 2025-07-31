from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from app.tasks import process_task
from app.filters import TaskFilter
from .models import Task
from .serializers import RegisterSerializer, TaskFilterSerializer, TaskSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filter_serializer = TaskFilterSerializer(data=request.query_params)
        if not filter_serializer.is_valid():
            return Response(filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Получение списка задач
        queryset = Task.objects.filter(user=request.user)
        filterset = TaskFilter(filter_serializer.validated_data, queryset=queryset)
        tasks = filterset.qs
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Проверяем ограничение на количество активных задач
        active_tasks_count = Task.objects.filter(user=request.user, status__in=['pending', 'in_progress']).count()
        if active_tasks_count >= 5:
            return Response(
                {"detail": "You can have a maximum of 5 active tasks."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем задачу
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(user=request.user)

            # Отправляем задачу в Celery
            process_task.delay(task.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут видеть свои задачи

    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)