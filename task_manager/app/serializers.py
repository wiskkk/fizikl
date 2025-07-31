from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Task


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
        )
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'task_type', 'input_data', 'status', 'result', 'created_at')
        read_only_fields = ('status', 'result', 'created_at')

    def validate(self, data):
        """
        Валидация input_data в зависимости от task_type.
        """
        task_type = data.get('task_type')
        input_data = data.get('input_data')

        if task_type == 'sum':
            # Для суммы должны быть указаны два числа: a и b
            if not isinstance(input_data, dict):
                raise serializers.ValidationError("input_data must be a dictionary.")
            if 'a' not in input_data or 'b' not in input_data:
                raise serializers.ValidationError("For 'sum' task, input_data must contain 'a' and 'b'.")
            if not isinstance(input_data['a'], (int, float)) or not isinstance(input_data['b'], (int, float)):
                raise serializers.ValidationError("For 'sum' task, 'a' and 'b' must be numbers.")

        elif task_type == 'countdown':
            # Для обратного отсчёта должно быть указано количество секунд
            if not isinstance(input_data, dict):
                raise serializers.ValidationError("input_data must be a dictionary.")
            if 'seconds' not in input_data:
                raise serializers.ValidationError("For 'countdown' task, input_data must contain 'seconds'.")
            if not isinstance(input_data['seconds'], int) or input_data['seconds'] <= 0:
                raise serializers.ValidationError("For 'countdown' task, 'seconds' must be a positive integer.")

        else:
            raise serializers.ValidationError(f"Unknown task_type: {task_type}")

        return data


class TaskFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Task.TASK_STATUSES, required=False)
