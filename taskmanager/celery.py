from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 的默认设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

# 创建 Celery 应用
app = Celery('taskmanager')

# 从 Django 的设置中加载配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现每个已注册的 Django 应用中的任务
app.autodiscover_tasks()
