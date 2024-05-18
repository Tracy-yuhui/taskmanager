from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# 创建默认路由
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 包含所有任务相关的 URL
]
