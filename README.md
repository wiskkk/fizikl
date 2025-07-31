# Task Manager

Task Manager — это Django-приложение с использованием **Django Rest Framework (DRF)**, **Celery** и **Docker**.  
Оно позволяет пользователям создавать задачи через API, отслеживать их статус и получать результат выполнения.  
Авторизация реализована через **JWT**.

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория
Склонируйте репозиторий на вашу локальную машину.
```bash
git clone https://github.com/your-repo/task-manager.git
cd task-manager
```

### 2. Настройка переменных окружения
Создайте файл `.env` в корне проекта и укажите необходимые переменные окружения.

### 3. Запуск контейнеров
Запустите все сервисы с помощью Docker Compose.
```bash
docker-compose up --build
```

### 4. Применение миграций
Выполните миграции для базы данных внутри контейнера.
```bash
docker exec -it <web_container_id> bash
python task_manager/manage.py migrate
```
---

## 📖 Документация API

Документация API доступна через Swagger и ReDoc:

- Swagger UI: http://localhost:8001/swagger/  
- ReDoc: http://localhost:8001/redoc/  

### Возможности API:
- **Пагинация**: список задач разбит на страницы (по умолчанию 5 задач на страницу).  
- **Фильтрация**: можно фильтровать задачи по статусу, например `GET /api/tasks/?status=completed`.  
- **Валидация**: входные данные проверяются в зависимости от типа задачи.  

---

## 🛠 Технологии
- Python 3.x  
- Django / DRF  
- Celery  
- Redis (брокер сообщений)  
- PostgreSQL  
- Docker & Docker Compose  
