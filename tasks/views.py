from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from .models import Task, FeishuUser
from .serializers import TaskSerializer, FeishuUserSerializer
from internal_db_ops.feishuservice import FeishuService
from rest_framework.decorators import api_view
from .constants import generate_reminder_card
from api.feishuapi import send_and_pin_message

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

    @action(detail=False, methods=['post'], url_path='create-task')
    def create(self, request):
        try:
            participants = request.data.get('participants')
            reminder_frequency = request.data.get('reminder_frequency')
            form_link = request.data.get('form_link')
            if not participants or not reminder_frequency or not form_link:
                return Response({"error": "Participants, reminder frequency, and form link are required"},
                                status=status.HTTP_400_BAD_REQUEST)

            FeishuService.reminder_task(participants, reminder_frequency, form_link)
            return Response({"message": "Task created and reminders set successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    @action(detail=False, methods=['post'], url_path='create_feishu_user')
    def create_feishu_user(self, request):
        name = request.data.get("name")
        mobile = request.data.get("mobile")
        if not name or not mobile:
            return Response({"error": "Name and mobile are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 调用 FeishuService.store_user_info 获取用户信息并存储到数据库
            feishu_user = FeishuService.store_user_info(mobile)
            feishu_user.name = name
            feishu_user.save()

            user_serializer = FeishuUserSerializer(feishu_user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='get_all_feishu_users')
    def get_all_feishu_users(self, request):
        users = FeishuService.get_all_feishu_users()
        user_serializer = FeishuUserSerializer(users, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='card_interaction_callback')
    def card_interaction_callback(request):
        try:
            response = FeishuService.handle_callback(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)