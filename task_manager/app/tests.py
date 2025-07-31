from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_task(self):
        url = reverse('tasks')
        data = {
            "task_type": "sum",
            "input_data": {"a": 5, "b": 10}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_tasks(self):
        Task.objects.create(user=self.user, task_type="sum", input_data={"a": 5, "b": 10}, status="completed")
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_task_detail(self):
        task = Task.objects.create(user=self.user, task_type="sum", input_data={"a": 5, "b": 10}, status="completed")
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        
    def test_create_invalid_task(self):
        url = reverse('task-create')
        invalid_data = {
            "task_type": "sum",
            "input_data": {
                "a": "five",  # Некорректное значение
                "b": 10
            }
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('input_data', response.data)