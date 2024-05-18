from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Task Manager!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # 假设你的API在一个叫做`api`的Django应用中
    path('', home),  # 添加根路径
    path('tasks/', include('tasks.urls')),

]

