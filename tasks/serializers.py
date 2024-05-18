from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

# 任务序列化器定义
class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to', 'assigned_to_username', 'due_date']
        # 添加了一个额外的字段 assigned_to_username，它会返回分配给用户的用户名
