from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

# 指定 Celery 应用为项目的默认应用
__all__ = ('celery_app',)
