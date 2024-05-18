from django.db import models
from django.contrib.auth.models import User

# 任务模型定义
class Task(models.Model):
    # 任务状态选项
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
    ]
    title = models.CharField(max_length=255)  # 任务标题
    description = models.TextField()  # 任务描述
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 任务状态
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)  # 分配任务给用户
    due_date = models.DateTimeField()  # 任务截止日期

    def __str__(self):
        return self.title  # 返回任务标题作为模型的字符串表示
