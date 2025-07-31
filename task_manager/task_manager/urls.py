from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from app.views import RegisterView, TaskDetailView, TaskView


schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="API для управления задачами",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение JWT токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление JWT токена
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/tasks/', TaskView.as_view(), name='tasks'),  # Создание задачи
    path('api/tasks/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),  # Подробная информация о задаче
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Документация
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
