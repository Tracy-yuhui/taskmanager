from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer

# 任务视图集定义
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  # 获取所有任务
    serializer_class = TaskSerializer  # 指定使用的序列化器

    # 自定义 API 端点，用于获取指定用户的所有任务
    @action(detail=False, methods=['get'], url_path='user-tasks/(?P<user_id>\d+)')
    def user_tasks(self, request, user_id=None):
        user = User.objects.get(id=user_id)
        tasks = Task.objects.filter(assigned_to=user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 自定义 API 端点，用于批量更新任务状态
    @action(detail=False, methods=['post'], url_path='bulk-update-status')
    def bulk_update_status(self, request):
        task_ids = request.data.get('task_ids', [])
        new_status = request.data.get('status', '')
        tasks = Task.objects.filter(id__in=task_ids)
        tasks.update(status=new_status)
        return Response({'message': '任务状态已批量更新'}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # 自定义 create 方法，以便更改创建任务时的请求和响应格式
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': '任务创建成功',
            'task': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # 自定义 update 方法，以便更改更新任务时的请求和响应格式
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': '任务更新成功',
            'task': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        # 自定义 destroy 方法，以便更改删除任务时的响应格式
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': '任务已删除'
        }, status=status.HTTP_204_NO_CONTENT)
